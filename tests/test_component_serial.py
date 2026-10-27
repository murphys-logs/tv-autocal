"""Pure serial-session fixtures and fake backend tests; never open a port."""

from dataclasses import FrozenInstanceError
from copy import deepcopy
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from tv_autocal.sender_audit import CandidateCommand
from tv_autocal_tools.permission import HardwarePermit
from tv_autocal_tools.serial_tool import SerialSession, _WindowsRuntime, run_serial


ACK = b"\x03\x0c\xf1"
NACK = b"\x03\x0c\xff"


def permit(hardware=True):
    return HardwarePermit("T-006", "a" * 40, "synthetic authorisation fixture", "fixture steps",
                          "synthetic prerequisite evidence", ("serial",), hardware)


class Recorder:
    def __init__(self, fail_kind=None):
        self.events = []
        self.fail_kind = fail_kind

    def __call__(self, kind, **fields):
        if kind == self.fail_kind:
            raise OSError("inert audit failure fixture")
        self.events.append((kind, fields))


class FakePort:
    def __init__(self):
        self.writes = []
        self.traffic = []
        self.opened = self.closed = False
        self.accepted = 7
        self.close_error = False
        self.read_error = False
        self.write_error = False

    def open(self):
        self.opened = True

    def read(self, count):
        if self.read_error:
            raise OSError("fake read error")
        if count != 96:
            raise AssertionError("unbounded read")
        return self.traffic.pop(0) if self.traffic else b""

    def write(self, frame):
        self.writes.append(frame)
        if self.write_error:
            raise OSError("fake indeterminate write")
        self.traffic.append(ACK)
        return self.accepted

    def close(self):
        if self.close_error:
            raise OSError("fake close error")
        self.closed = True


class FakeRuntime:
    def __init__(self, keys=None):
        self.port = FakePort()
        self.time = 0
        self.keys = dict(keys or {})
        self.after_pause = None

    def open(self):
        self.port.open()
        self.time = 0

    def now(self):
        return self.time

    def key(self):
        return self.keys.pop(self.time, None)

    def pause(self):
        self.time += 10
        if self.after_pause:
            self.after_pause(self)
        if self.time > 200000:
            raise AssertionError("fake loop did not terminate")


class FakeConsole:
    def __init__(self, keys):
        self.keys = list(keys)
        self.reads = 0

    def kbhit(self):
        return bool(self.keys)

    def getwch(self):
        self.reads += 1
        key = self.keys.pop(0)
        if isinstance(key, BaseException):
            raise key
        return key


class ComponentSerialTests(TestCase):
    def session(self, **kwargs):
        log = Recorder()
        return SerialSession(log, menu_window_ms=10000, **kwargs), log

    def first_exit(self, session, now=5000):
        session.operator("b", now)
        session.operator("m", now + 1)
        session.operator("o", now + 2)
        frame = session.operator("e", now + 3)
        self.assertEqual(frame, b"\x08\x22\x0d\x00\x00\x2d\x9c")
        session.write_done(7, now + 4)
        return now + 4

    def ack_confirm(self, session, now):
        session.receive(ACK, now)
        session.tick(now + 500)
        session.operator("c", now + 501)
        session.tick(now + 2501)
        return now + 2501

    def console_phase_fixtures(self):
        # Reach phases through legal actions, including each setter/EXIT
        # generation. Copies let key regressions run without advancing time.
        session, log = self.session()
        fixtures = []

        def save():
            fixtures.append(deepcopy((session, log)))

        save()
        session.tick(5000)
        save()
        session.operator("b", 5000)
        save()
        now = 5001
        for key, command in (("e", CandidateCommand.EXIT), ("d", CandidateCommand.CONTRAST94),
                             ("e", CandidateCommand.EXIT), ("r", CandidateCommand.RESTORE95),
                             ("e", CandidateCommand.EXIT)):
            if key == "e":
                session.operator("m", now)
                save()
                now += 1
                session.operator("o", now)
                save()
                now += 1
            self.assertEqual(session.operator(key, now), command.value)
            save()
            now += 1
            session.write_done(7, now)
            save()
            now += 1
            session.receive(ACK, now)
            save()
            now += 500
            session.tick(now)
            save()
            if key == "e":
                now += 1
                session.operator("c", now)
                save()
                now += 2000
                session.tick(now)
                save()
            now += 1
        session.finish_close(closed=True)
        save()
        session, log = self.session()
        session.stop("synthetic stopped-session fixture")
        save()
        session.finish_close(closed=True)
        save()
        return fixtures

    def test_special_console_keys_never_dispatch_in_any_session_phase(self):
        sequences = {"Right": "\xe0m", "End": "\xe0o", "Insert": "\xe0r", "PgDn": "\xe0q",
                     "F8": "\x00b", "F9": "\x00c", "F10": "\x00d"}
        fixtures = self.console_phase_fixtures()
        self.assertEqual({session.phase for session, _ in fixtures}, {
            "initial quiet", "baseline", "menu preparation", "observe setting", "exit ready",
            "writing", "reply", "ack quiet", "confirm exit", "settling", "set ready",
            "restore ready", "complete", "stopped",
        })
        for name, sequence in sequences.items():
            for fixture in fixtures:
                session, log = deepcopy(fixture)
                with self.subTest(key=name, phase=session.phase, writes=session.writes, closed=session.closed):
                    console = FakeConsole(sequence)
                    # Invoke only the decoder, never the Windows constructor.
                    runtime = SimpleNamespace(_console=console)
                    before = deepcopy((session.__dict__, log.events))
                    frames, decoded = [], []
                    while console.kbhit():
                        key = _WindowsRuntime.key(runtime)
                        decoded.append(key)
                        # Match run_serial's dispatch, including q outside
                        # SerialSession.operator and its wrong-phase handling.
                        if key == "q":
                            session.stop("unexpected console stop")
                        elif key is not None:
                            try:
                                frame = session.operator(key, session._now)
                            except (ValueError, RuntimeError):
                                continue
                            if frame is not None:
                                frames.append(frame)
                    self.assertEqual(decoded, [None])
                    self.assertEqual(console.reads, 2)
                    self.assertIsNone(_WindowsRuntime.key(runtime))
                    self.assertEqual(frames, [])
                    self.assertEqual(log.events, before[1])
                    # Compare all state except callback/parser object identity.
                    for field, value in before[0].items():
                        if field not in {"log", "_parser"}:
                            self.assertEqual(getattr(session, field), value, field)

    def test_console_accepts_only_exact_command_keys(self):
        for key in "bmoecdrq":
            with self.subTest(key=key):
                console = FakeConsole(key)
                self.assertEqual(_WindowsRuntime.key(SimpleNamespace(_console=console)), key)
                self.assertFalse(console.kbhit())
        for key in ("B", "M", "O", "E", "C", "D", "R", "Q", "x", "1", "\x03", "\x1b", "\r", "\n", " ", "\t"):
            with self.subTest(ignored=repr(key)):
                console = FakeConsole(key)
                self.assertIsNone(_WindowsRuntime.key(SimpleNamespace(_console=console)))
                self.assertFalse(console.kbhit())
        console = FakeConsole("\xe0mq")
        runtime = SimpleNamespace(_console=console)
        self.assertIsNone(_WindowsRuntime.key(runtime))
        self.assertEqual(_WindowsRuntime.key(runtime), "q")
        self.assertIsNone(_WindowsRuntime.key(runtime))

    def test_console_keyboard_interrupt_still_stops_and_closes_fake_session(self):
        runtime, log = FakeRuntime(), Recorder()
        runtime._console = FakeConsole([KeyboardInterrupt()])
        # Keep the actual decoder callable when replacing the constructor.
        decode = _WindowsRuntime.key
        runtime.key = lambda: decode(runtime)
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertEqual(result.reason, "owner interrupted; no recovery send")
        self.assertFalse(result.accepted)
        self.assertEqual(runtime.port.writes, [])
        self.assertTrue(runtime.port.closed)
        self.assertTrue(any(kind == "serial_stop" and "owner interrupted" in fields["reason"]
                            for kind, fields in log.events))

    def test_exact_five_frame_sequence_requires_observations_and_exit_waits(self):
        session, log = self.session()
        time = self.first_exit(session)
        time = self.ack_confirm(session, time + 1)
        for key, command in (("d", CandidateCommand.CONTRAST94),
                             ("r", CandidateCommand.RESTORE95)):
            self.assertEqual(session.operator(key, time), command.value)
            session.write_done(7, time + 1)
            session.receive(ACK, time + 2)
            session.tick(time + 502)
            session.operator("m", time + 503)
            session.operator("o", time + 504)
            self.assertEqual(session.operator("e", time + 505), CandidateCommand.EXIT.value)
            session.write_done(7, time + 506)
            time = self.ack_confirm(session, time + 507)
        self.assertEqual(session.phase, "complete")
        self.assertEqual(session.writes, 5)
        result = session.finish_close(closed=True)
        self.assertTrue(result.completed)
        self.assertTrue(result.accepted)
        self.assertEqual([(s, e) for s, e, _ in result.evidence_pairs], [(None, 1), (2, 3), (4, 5)])
        self.assertEqual([v[1]["value"] for v in log.events if v[0] == "serial_owner_observation"],
                         [95, 95, 94, 95])
        with self.assertRaises(FrozenInstanceError):
            result.completed = False

    def test_initial_five_seconds_blocks_every_send(self):
        session, _ = self.session()
        for key in ("b", "e", "d", "r"):
            with self.assertRaises(ValueError):
                session.operator(key, 4999)
        self.assertEqual(session.writes, 0)
        session.operator("b", 5000)
        self.assertEqual(session.phase, "menu preparation")

    def test_out_of_window_initial_bytes_stop_before_write(self):
        session, log = self.session()
        session.receive(ACK, 4999)
        self.assertEqual(session.phase, "stopped")
        self.assertEqual(log.events[-2][0], "serial_receive")
        with self.assertRaises(RuntimeError):
            session.operator("e", 5000)

    def test_every_ack_split_works_before_deadline(self):
        for split in range(4):
            session, _ = self.session()
            now = self.first_exit(session)
            session.receive(ACK[:split], now + 1)
            session.receive(ACK[split:], now + 2)
            session.tick(now + 502)
            self.assertEqual(session.phase, "confirm exit")

    def test_exclusive_deadline_and_raw_late_retention(self):
        for offset, expected in ((1999, "ack quiet"), (2000, "stopped")):
            session, log = self.session()
            now = self.first_exit(session)
            session.receive(ACK, now + offset)
            self.assertEqual(session.phase, expected)
            self.assertTrue(any(k == "serial_receive" and f["data_hex"] == ACK.hex()
                                for k, f in log.events))

    def test_duplicate_noise_nack_and_trailing_bytes_stop_without_recovery(self):
        for data in (ACK + ACK, ACK + b"\x03", b"noise", NACK):
            session, _ = self.session()
            now = self.first_exit(session)
            session.receive(data, now + 1)
            self.assertEqual(session.phase, "stopped")
            with self.assertRaises(RuntimeError):
                session.operator("r", now + 2)

    def test_bytes_during_ack_quiet_and_owner_inspection_are_retained_and_fatal(self):
        for offset in (2, 502):
            session, log = self.session()
            now = self.first_exit(session)
            session.receive(ACK, now + 1)
            session.receive(b"x", now + offset)
            self.assertEqual(session.phase, "stopped")
            self.assertEqual(session.received_bytes, 4)
            self.assertTrue(any(k == "serial_receive" and f["data_hex"] == "78" for k, f in log.events))

    def test_input_after_fault_continues_to_be_logged(self):
        session, log = self.session()
        session.receive(b"bad", 1)
        session.receive(ACK, 2)
        session.receive(b"tail", 3)
        self.assertEqual([f["data_hex"] for k, f in log.events if k == "serial_receive"],
                         [b"bad".hex(), ACK.hex(), b"tail".hex()])

    def test_partial_and_indeterminate_writes_stop_and_keep_counts(self):
        for count in (0, 6, None, True):
            session, log = self.session()
            session.operator("b", 5000)
            session.operator("m", 5001)
            session.operator("o", 5002)
            session.operator("e", 5003)
            session.write_done(count, 5004)
            self.assertEqual(session.phase, "stopped")
            self.assertEqual([f["accepted_bytes"] for k, f in log.events if k == "serial_write_result"], [count])

    def test_completion_count_is_kept_when_write_crosses_session_deadline(self):
        session, log = self.session(session_ms=5005)
        session.operator("b", 5000)
        session.operator("m", 5001)
        session.operator("o", 5002)
        session.operator("e", 5003)
        session.write_done(7, 5005)
        self.assertEqual(session.phase, "stopped")
        self.assertTrue(any(k == "serial_write_result" and f["accepted_bytes"] == 7 for k, f in log.events))

    def test_stale_observation_and_missing_menu_opening_cannot_send_exit(self):
        session, _ = self.session()
        session.operator("b", 5000)
        with self.assertRaises(ValueError):
            session.operator("o", 5001)
        with self.assertRaises(ValueError):
            session.operator("e", 5001)
        now = 5002
        session.operator("m", now)
        session.operator("o", now + 1)
        session.operator("e", now + 2)
        self.assertIsNone(session._observation_generation)
        with self.assertRaises(ValueError):
            session.operator("e", now + 3)

    def test_menu_exclusion_window_applies_to_send_and_closure_confirmation(self):
        for check_closure in (False, True):
            session = SerialSession(Recorder(), menu_window_ms=1000)
            session.operator("b", 5000)
            session.operator("m", 5001)
            session.operator("o", 5002)
            if check_closure:
                session.operator("e", 5003)
                session.write_done(7, 5004)
                session.receive(ACK, 5005)
                session.tick(5505)
                session.operator("c", 6001)
            else:
                session.operator("e", 6001)
            self.assertEqual(session.phase, "stopped")

    def test_settling_blocks_next_write_until_exact_boundary(self):
        session, _ = self.session()
        now = self.first_exit(session)
        session.receive(ACK, now + 1)
        session.tick(now + 501)
        session.operator("c", now + 502)
        with self.assertRaises(ValueError):
            session.operator("d", now + 2501)
        self.assertEqual(session.operator("d", now + 2502), CandidateCommand.CONTRAST94.value)

    def test_byte_and_event_overflow_are_explicit_and_bounded(self):
        session, log = self.session(max_bytes=96)
        session.receive(b"x" * 96, 1)
        session.receive(b"tail", 2)
        session.receive(b"later", 3)
        self.assertFalse(session.log_complete)
        self.assertEqual(session.omitted_bytes, 9)
        self.assertEqual(sum(len(bytes.fromhex(f["data_hex"])) for k, f in log.events
                             if k == "serial_receive"), 96)
        session, log = self.session(max_events=32)
        for n in range(100):
            session.receive(b"x", n)
        result = session.finish_close(closed=True)
        self.assertLessEqual(len(log.events), 32)
        self.assertFalse(result.log_complete)
        self.assertGreater(result.omitted_bytes, 0)

    def test_invalid_sizes_time_and_policy_arguments_fail_before_io(self):
        for name, value in (("quiet_ms", False), ("reply_ms", 0), ("settle_ms", 60001),
                            ("session_ms", -1), ("initial_ms", 10001), ("max_events", 31)):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.session(**{name: value})
        session, _ = self.session()
        for data in (bytearray(ACK), b"x" * 97):
            with self.assertRaises(ValueError):
                session.receive(data, 1)
        session.tick(10)
        with self.assertRaises(ValueError):
            session.tick(9)

    def test_permission_and_prerequisites_reject_before_backend_factory(self):
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", side_effect=AssertionError("I/O")):
            with self.assertRaises(PermissionError):
                run_serial(permit(False), port="COM999", log=Recorder(), prerequisites_confirmed=True,
                           menu_window_ms=10000)
            with self.assertRaises(PermissionError):
                run_serial(permit(), port="COM999", log=Recorder(), prerequisites_confirmed=False,
                           menu_window_ms=10000)
            for port in ("COM0", "COM01", "COM1 ", "com1", "loop://", "\\\\.\\COM1"):
                with self.subTest(port=port), self.assertRaises(ValueError):
                    run_serial(permit(), port=port, log=Recorder(), prerequisites_confirmed=True,
                               menu_window_ms=10000)

    def test_log_failure_prevents_backend_creation_or_command_write(self):
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", side_effect=AssertionError("I/O")):
            result = run_serial(permit(), port="COM999", log=Recorder("serial_open_intent"),
                                prerequisites_confirmed=True, menu_window_ms=10000)
            self.assertFalse(result.completed)
        runtime = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e"})
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=Recorder("serial_write_intent"),
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertEqual(runtime.port.writes, [])
        self.assertTrue(runtime.port.closed)
        self.assertFalse(result.log_complete)

    def test_fake_backend_happy_path_keeps_exact_sequence_and_closes(self):
        keys = {5000: "b", 5010: "m", 5020: "o", 5030: "e", 5550: "c",
                7550: "d", 8070: "m", 8080: "o", 8090: "e", 8610: "c",
                10610: "r", 11130: "m", 11140: "o", 11150: "e", 11670: "c", 13680: "q"}
        runtime, log = FakeRuntime(keys), Recorder()
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertTrue(result.completed)
        self.assertEqual(runtime.port.writes, [CandidateCommand.EXIT.value, CandidateCommand.CONTRAST94.value,
                                              CandidateCommand.EXIT.value, CandidateCommand.RESTORE95.value,
                                              CandidateCommand.EXIT.value])
        self.assertTrue(runtime.port.closed)
        self.assertEqual(runtime.time, 14180)
        self.assertEqual(log.events[-1][0], "serial_close")

    def test_fake_backend_retains_bytes_during_close_and_cannot_revive_failure(self):
        runtime, log = FakeRuntime({5000: "q"}), Recorder()
        runtime.after_pause = lambda rt: rt.port.traffic.append(ACK) if rt.time == 5200 else None
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertFalse(result.completed)
        self.assertEqual(result.received_bytes, 3)
        self.assertTrue(runtime.port.closed)

    def test_runtime_timestamps_receive_after_read_crosses_reply_deadline(self):
        # First write completes at 5030; its exclusive deadline is 7030.
        # read starts at 5040 but the fake OS delays its return to the boundary.
        for finished, provisional in ((7029, True), (7030, False), (7031, False)):
            with self.subTest(finished=finished):
                runtime = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e", finished: "q"})
                log = Recorder()
                read = runtime.port.read

                def delayed_read(count):
                    data = read(count)
                    if data:
                        runtime.time = finished
                    return data

                runtime.port.read = delayed_read
                with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
                    result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                        menu_window_ms=10000)
                self.assertEqual(any(kind == "serial_provisional_ack" for kind, _ in log.events), provisional)
                received = [fields for kind, fields in log.events if kind == "serial_receive"]
                self.assertEqual([(item["elapsed_ms"], item["data_hex"]) for item in received],
                                 [(finished, ACK.hex())])
                if not provisional:
                    self.assertIn("exclusive reply deadline", result.reason)
                self.assertEqual(len(runtime.port.writes), 1)
                self.assertTrue(result.closed)
                self.assertFalse(result.accepted)

    def test_fake_backend_write_error_and_close_failure_are_not_hidden(self):
        for close_error in (False, True):
            runtime, log = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e"}), Recorder()
            runtime.port.write_error = True
            runtime.port.close_error = close_error
            with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
                result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                    menu_window_ms=10000)
            self.assertFalse(result.completed)
            self.assertEqual(result.closed, not close_error)
            self.assertEqual(len(runtime.port.writes), 1)
            self.assertTrue(any(k == "serial_write_intent" for k, _ in log.events))

    def test_fresh_prewrite_receive_check_catches_bytes_during_console_handling(self):
        runtime, log = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e"}), Recorder()
        original_key = runtime.key

        def key_with_new_traffic():
            key = original_key()
            if key == "e":
                runtime.port.traffic.append(ACK)
            return key

        runtime.key = key_with_new_traffic
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertEqual(runtime.port.writes, [])
        self.assertFalse(result.accepted)
        self.assertEqual(result.received_bytes, 3)

    def test_menu_window_is_rechecked_after_slow_intent_logging(self):
        runtime, log = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e"}), Recorder()

        def slow_log(kind, **fields):
            log(kind, **fields)
            if kind == "serial_write_intent":
                runtime.time = 15010

        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", log=slow_log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertEqual(runtime.port.writes, [])
        self.assertFalse(result.accepted)
        self.assertIn("before actual write", result.reason)

    def test_backend_creation_failure_is_recorded_before_any_open(self):
        log = Recorder()
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", side_effect=RuntimeError("missing dependency")):
            result = run_serial(permit(), port="COM999", log=log, prerequisites_confirmed=True,
                                menu_window_ms=10000)
        self.assertFalse(result.accepted)
        self.assertTrue(result.closed)
        self.assertEqual(result.writes, 0)
        self.assertTrue(any(k == "serial_stop" and "backend unavailable" in f["reason"] for k, f in log.events))

    def test_fake_pyserial_configuration_sets_inactive_lines_before_open(self):
        from types import SimpleNamespace
        import sys
        serial = SimpleNamespace(VERSION="3.5")
        calls = []

        class UnopenedPort:
            def __init__(self, **kwargs):
                calls.append(("construct", kwargs))

            def __setattr__(self, name, value):
                calls.append((name, value))

        serial.Serial = UnopenedPort
        with patch.object(sys, "platform", "win32"), patch.dict(sys.modules, {"serial": serial, "msvcrt": object()}):
            _WindowsRuntime("COM999")
        self.assertEqual(calls[0][1], dict(port=None, baudrate=9600, bytesize=8, parity="N", stopbits=1,
                                          timeout=0, write_timeout=1, xonxoff=False, rtscts=False, dsrdtr=False))
        self.assertEqual(calls[1:], [("dtr", False), ("rts", False), ("port", "COM999")])

    def test_wrong_pyserial_version_fails_before_port_creation(self):
        from types import SimpleNamespace
        import sys
        serial = SimpleNamespace(VERSION="wrong", Serial=lambda **kwargs: self.fail("port created"))
        with patch.object(sys, "platform", "win32"), patch.dict(sys.modules, {"serial": serial, "msvcrt": object()}):
            with self.assertRaises(RuntimeError):
                _WindowsRuntime("COM999")
