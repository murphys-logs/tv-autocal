"""Offline meter-boundary checks: inert pipes, fake processes, no Argyll launch."""

from dataclasses import FrozenInstanceError
from hashlib import sha256
from io import BytesIO
from threading import Barrier, Thread
import unittest
from unittest.mock import MagicMock, patch

from tv_autocal_tools import meter
from tv_autocal_tools.permission import HardwarePermit


VALID = b"\n Result is XYZ: 10.000000 20.000000 30.000000, Yxy: 20.000000 0.166667 0.333333\n"


def permit(plan="T-003", hardware=True):
    return HardwarePermit(plan, "a" * 40, "Synthetic authorisation fixture", "Synthetic steps",
                          "Synthetic prerequisite fixture", ("meter",), hardware)


class ImmediateThread:
    """Execute inert readers deterministically; this never launches a process."""
    def __init__(self, target, args, **kwargs):
        self.target, self.args = target, args

    def start(self):
        self.target(*self.args)

    def join(self):
        pass


class FakeProcess:
    def __init__(self, stdout=VALID, stderr=b"", code=0):
        self.stdout, self.stderr = BytesIO(stdout), BytesIO(stderr)
        self.code = code
        self.pid = 5151

    def poll(self):
        return self.code


def supervise_fixture(process, capture, notify):
    readers = meter._PipeReaders(capture)
    # Inert fixture has no launch operation; immediate-thread tests need the
    # streams attached before executing their targets synchronously.
    readers.attach(process)
    readers.start()
    return meter._supervise(process, capture, notify, readers=readers)


class ComponentMeterTests(unittest.TestCase):
    def setUp(self):
        # Every runner case keeps signal installation and process identity inert;
        # tests of individual signal phases override this fake explicitly.
        self.signal_patch = patch("signal.signal", return_value="synthetic previous handler")
        self.signal_patch.start()
        self.addCleanup(self.signal_patch.stop)
        self.pid_patch = patch.object(meter, "getpid", return_value=4242)
        self.pid_patch.start()
        self.addCleanup(self.pid_patch.stop)

    def complete(self, stdout=VALID, stderr=b"", code=0, **kwargs):
        capture = meter.TranscriptCapture(0, **kwargs)
        capture.feed("stdout", stdout, 1)
        capture.feed("stderr", stderr, 1)
        capture.end_stream("stdout", 2)
        capture.end_stream("stderr", 2)
        return capture.result(code, 3)

    def test_complete_source_format_keeps_bytes_and_fixture_provenance(self):
        result = self.complete()
        self.assertTrue(result.accepted)
        self.assertEqual(result.xyz, (10.0, 20.0, 30.0))
        self.assertEqual(result.stdout, VALID)
        self.assertTrue(result.simulated)
        self.assertEqual(result.as_dict()["stdout"], VALID.hex())
        with self.assertRaises(FrozenInstanceError):
            result.accepted = False

    def test_hardware_provenance_is_not_legacy_parser_simulation_flag(self):
        result = self.complete(simulated=False)
        self.assertTrue(result.accepted)
        self.assertFalse(result.simulated)
        self.assertNotIn("synthetic", result.reason)
        self.assertIn("never calibration", result.purpose)

    def test_x_option_requires_yxy_and_rejects_default_lab(self):
        result = self.complete(VALID.replace(b"Yxy: 20.000000 0.166667 0.333333",
                                            b"D50 Lab: 50.000000 1.000000 -2.000000"))
        self.assertFalse(result.accepted)
        self.assertIn("format", result.reason)

    def test_process_exit_and_both_eof_required(self):
        capture = meter.TranscriptCapture(0)
        capture.feed("stdout", VALID, 1)
        capture.end_stream("stdout", 2)
        self.assertFalse(capture.result(0, 2).accepted)
        capture.end_stream("stderr", 3)
        self.assertFalse(capture.result(None, 3).accepted)
        self.assertTrue(capture.result(0, 3).accepted)

    def test_failure_diagnostics_and_exit_status_override_xyz(self):
        for stdout, stderr, code in ((VALID, b"warning", 0), (VALID, b"", 1),
                                     (VALID + VALID, b"", 0), (b"calibration only\n", b"", 0)):
            with self.subTest(code=code, stderr=stderr):
                result = self.complete(stdout, stderr, code)
                self.assertFalse(result.accepted)
                self.assertEqual((result.stdout, result.stderr, result.exit_code), (stdout, stderr, code))

    def test_timeout_first_does_not_discard_late_transcript(self):
        capture = meter.TranscriptCapture(0, timeout_ms=10)
        capture.tick(10)
        capture.feed("stdout", VALID, 11)
        capture.end_stream("stdout", 12)
        capture.end_stream("stderr", 12)
        result = capture.result(0, 13)
        self.assertTrue(result.timed_out)
        self.assertFalse(result.accepted)
        self.assertEqual(result.stdout, VALID)
        self.assertTrue(result.capture_complete)

    def test_complete_at_deadline_is_late_and_one_before_passes(self):
        for completed, accepted in ((9, True), (10, False)):
            with self.subTest(completed=completed):
                capture = meter.TranscriptCapture(0, timeout_ms=10)
                capture.feed("stdout", VALID, 1)
                capture.end_stream("stdout", completed)
                capture.end_stream("stderr", completed)
                self.assertEqual(capture.result(0, completed).accepted, accepted)

    def test_cancel_keeps_later_bytes_and_cannot_be_revived(self):
        capture = meter.TranscriptCapture(0)
        capture.cancel(1)
        capture.feed("stdout", VALID, 2)
        capture.end_stream("stdout", 3)
        capture.end_stream("stderr", 3)
        result = capture.result(0, 4)
        self.assertTrue(result.cancelled)
        self.assertFalse(result.accepted)
        self.assertEqual(result.stdout, VALID)

    def test_memory_and_log_chunk_bounds_explicitly_reject_overflow(self):
        events = []
        capture = meter.TranscriptCapture(0, log=lambda kind, **fields: events.append((kind, fields)))
        capture.feed("stdout", b"x" * (meter.MAX_OUTPUT_BYTES + 7), 1)
        capture.feed("stdout", b"later", 2)
        capture.end_stream("stdout", 3)
        capture.end_stream("stderr", 3)
        result = capture.result(0, 4)
        self.assertEqual(len(result.stdout), meter.MAX_OUTPUT_BYTES)
        self.assertEqual(result.stdout_dropped, 12)
        self.assertFalse(result.capture_complete)
        self.assertFalse(result.accepted)
        chunks = [fields["data_hex"] for kind, fields in events if kind == "meter_output"]
        self.assertTrue(all(len(value) <= meter.CHUNK_BYTES * 2 for value in chunks))
        self.assertEqual(sum(kind == "meter_overflow" for kind, _ in events), 1)

    def test_log_failure_does_not_stop_bounded_capture(self):
        def broken(*args, **kwargs):
            raise OSError("synthetic full disk")
        result = self.complete(log=broken)
        self.assertEqual(result.stdout, VALID)
        self.assertFalse(result.log_complete)
        self.assertFalse(result.accepted)

    def test_stream_error_is_not_eof(self):
        capture = meter.TranscriptCapture(0)
        capture.feed("stdout", VALID, 1)
        capture.end_stream("stdout", 2)
        capture.end_stream("stderr", 2, error=True)
        self.assertFalse(capture.result(0, 3).capture_complete)

    def test_time_and_stream_validation(self):
        capture = meter.TranscriptCapture(10)
        with self.assertRaises(ValueError):
            capture.tick(9)
        with self.assertRaises(TypeError):
            capture.feed("other", b"", 10)
        with self.assertRaises(TypeError):
            capture.feed("stdout", "text", 10)
        capture.end_stream("stdout", 10)
        with self.assertRaises(RuntimeError):
            capture.feed("stdout", b"later", 10)
        for timeout in (0, 60001, True):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                meter.TranscriptCapture(0, timeout_ms=timeout)

    def test_environment_copy_removes_both_case_insensitive_defaults(self):
        before = {"Path": "fixture", "ARGYLL_COLMTER_CAL_SPEC_SET": "private",
                  "argyll_colmter_cor_matrix": "private2", "OTHER": "retained"}
        after = meter.isolated_environment(before)
        self.assertEqual(after, {"Path": "fixture", "OTHER": "retained"})
        self.assertEqual(len(before), 4)

    def test_missing_permit_cannot_read_files_or_spawn(self):
        with patch.object(meter, "_verified_executable") as verify, patch.object(meter, "_spawn") as spawn:
            for supplied in (None, permit(hardware=False), permit("T-006")):
                with self.subTest(supplied=supplied), self.assertRaises((TypeError, PermissionError)):
                    meter.run_meter(supplied, executable="unused", sha256="unused",
                                    attempt_log="unused", log=lambda *a, **k: None)
            verify.assert_not_called()
            spawn.assert_not_called()

    def test_attestations_and_windows_required_before_files_or_spawn(self):
        with patch.object(meter, "_verified_executable") as verify, patch.object(meter, "_spawn") as spawn:
            with patch.object(meter, "platform", "other"), self.assertRaises(RuntimeError):
                self.run_fixture()
            with patch.object(meter, "platform", "win32"):
                for field in ("isolated", "exit_confirmed", "discovery_confirmed"):
                    with self.subTest(field=field), self.assertRaises(PermissionError):
                        self.run_fixture(**{field: False})
            verify.assert_not_called()
            spawn.assert_not_called()

    def run_fixture(self, **overrides):
        kwargs = dict(executable=r"C:\fixture\spotread.exe", sha256="a" * 64,
                      attempt_log="local/T-003/fixture.log", log=lambda *a, **k: None,
                      isolated=True, exit_confirmed=True, discovery_confirmed=True,
                      notify=lambda message: None)
        kwargs.update(overrides)
        return meter.run_meter(permit(), **kwargs)

    def test_launch_uses_fixed_argv_fresh_wait_and_isolated_environment(self):
        current = [0]
        events = []
        def advance(seconds):
            current[0] = min(2000, current[0] + round(seconds * 1000))
        process = FakeProcess()
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value=r"C:\fixture\spotread.exe"), \
                patch.object(meter, "_reserve_attempt_log", return_value=r"C:\fixture\local\T-003\attempt.log"), \
                patch.object(meter, "_now_ms", side_effect=lambda: current[0]), \
                patch.object(meter, "sleep", side_effect=advance), \
                patch.object(meter, "_spawn", return_value=process) as spawn, \
                patch.dict("os.environ", {"ARGYLL_COLMTER_CAL_SPEC_SET": "fixture"}):
            result = self.run_fixture(log=lambda kind, **fields: events.append((kind, fields)))
        self.assertTrue(result.accepted)
        self.assertFalse(result.simulated)
        self.assertEqual(spawn.call_args.args[0], [r"C:\fixture\spotread.exe", "-O", "-e", "-x",
                                                "-Y", "n", r"C:\fixture\local\T-003\attempt.log"])
        self.assertNotIn("ARGYLL_COLMTER_CAL_SPEC_SET", spawn.call_args.args[1])
        intent = next(fields for kind, fields in events if kind == "meter_launch_intent")
        self.assertGreaterEqual(intent["wait_completed_ms"] - intent["wait_started_ms"], 2000)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_log_failure_before_launch_prevents_process(self):
        def broken(*args, **kwargs):
            raise OSError("synthetic disk failure")
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_spawn") as spawn, self.assertRaises(OSError):
            self.run_fixture(log=broken)
        spawn.assert_not_called()

    def test_launch_failure_is_recorded_without_retry(self):
        events = []
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000, 2000]), \
                patch.object(meter, "_spawn", side_effect=OSError("synthetic failure")) as spawn, \
                self.assertRaises(OSError):
            self.run_fixture(log=lambda kind, **fields: events.append(kind))
        self.assertEqual(spawn.call_count, 1)
        self.assertEqual(events[-1], "meter_launch_failed")

    def test_supervisor_keeps_output_after_keyboard_cancel(self):
        process = FakeProcess()
        process.poll = MagicMock(side_effect=[KeyboardInterrupt, None, 0])
        capture = meter.TranscriptCapture(0)
        notices = []
        with patch("threading.Thread", ImmediateThread), patch.object(meter, "_now_ms", return_value=1), \
                patch.object(meter, "sleep"), patch.object(process, "kill", create=True) as kill:
            result = supervise_fixture(process, capture, notices.append)
        self.assertTrue(result.cancelled)
        self.assertFalse(result.accepted)
        self.assertEqual(result.stdout, VALID)
        kill.assert_not_called()
        self.assertEqual(len(notices), 1)

    def test_supervisor_reports_timeout_and_drains_without_kill(self):
        process = FakeProcess()
        process.poll = MagicMock(side_effect=[None, 0])
        capture = meter.TranscriptCapture(0, timeout_ms=10)
        notices = []
        with patch("threading.Thread", ImmediateThread), patch.object(meter, "_now_ms", return_value=10), \
                patch.object(meter, "sleep"), patch.object(process, "kill", create=True) as kill:
            result = supervise_fixture(process, capture, notices.append)
        self.assertTrue(result.timed_out)
        self.assertFalse(result.accepted)
        self.assertEqual(result.stdout, VALID)
        self.assertEqual(len(notices), 1)
        kill.assert_not_called()

    def test_executable_validation_rejects_bad_paths_before_reading(self):
        with patch.object(meter, "Path") as path:
            for value in ("spotread.exe", r"\\host\share\spotread.exe", r"C:\fixture\other.exe"):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    meter._verified_executable(value, "a" * 64)
            path.assert_not_called()

    def test_executable_hash_must_match_file_bytes(self):
        fake_path = MagicMock()
        fake_path.__str__.return_value = r"C:\fixture\spotread.exe"
        fake_path.name = "spotread.exe"
        fake_path.is_file.return_value = True
        fake_path.open.return_value.__enter__.side_effect = lambda: BytesIO(b"inert fixture")
        with patch.object(meter, "Path") as path:
            path.return_value.resolve.return_value = fake_path
            meter._verified_executable(r"C:\fixture\spotread.exe", sha256(b"inert fixture").hexdigest())
            with self.assertRaises(ValueError):
                meter._verified_executable(r"C:\fixture\spotread.exe", "0" * 64)

    def test_actual_reader_threads_drain_both_inert_pipes_concurrently(self):
        rendezvous = Barrier(2)
        class PairedPipe(BytesIO):
            waited = False
            def read(self, count):
                if not self.waited:
                    self.waited = True
                    rendezvous.wait(timeout=2)
                return super().read(count)
        process = FakeProcess()
        process.stdout = PairedPipe(VALID)
        process.stderr = PairedPipe(b"")
        result = supervise_fixture(process, meter.TranscriptCapture(meter._now_ms()), lambda text: None)
        self.assertTrue(result.accepted)
        self.assertEqual(result.stdout, VALID)

    def test_reader_start_failure_prevents_launch(self):
        class FailedThread(ImmediateThread):
            def start(self):
                raise RuntimeError("synthetic thread-resource failure")
            def is_alive(self):
                return False
        events = []
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000, 2000]), \
                patch("threading.Thread", FailedThread), patch.object(meter, "_spawn") as spawn, \
                self.assertRaises(RuntimeError):
            self.run_fixture(log=lambda kind, **fields: events.append(kind))
        spawn.assert_not_called()
        self.assertEqual(events[-1], "meter_capture_start_failed")

    def test_second_reader_start_failure_releases_first_without_launch(self):
        threads = []
        class FailsSecond(Thread):
            def start(self):
                if self.name.endswith("stderr"):
                    raise RuntimeError("synthetic second-reader failure")
                threads.append(self)
                super().start()
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000, 2000]), \
                patch("threading.Thread", FailsSecond), patch.object(meter, "_spawn") as spawn, \
                self.assertRaises(RuntimeError):
            self.run_fixture()
        spawn.assert_not_called()
        self.assertEqual(len(threads), 1)
        self.assertFalse(threads[0].is_alive())

    def test_launch_defers_control_c_until_readers_own_process(self):
        handlers = []
        def install(number, handler):
            handlers.append(handler)
            return "previous"
        process = FakeProcess()
        def spawn(argv, env):
            handlers[0](None, None)
            return process
        times = iter([0])
        with patch("signal.signal", side_effect=install), \
                patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=lambda: next(times, 2000)), \
                patch.object(meter, "_spawn", side_effect=spawn), patch.object(meter, "sleep"):
            result = self.run_fixture()
        self.assertTrue(result.cancelled)
        self.assertEqual(result.stdout, VALID)
        self.assertTrue(result.child_exit_confirmed)
        self.assertTrue(result.readers_complete)
        self.assertEqual(handlers[-1], "previous")

    def test_notification_failure_does_not_abandon_child_or_capture(self):
        def broken(message):
            raise OSError("synthetic closed status pipe")
        process = FakeProcess()
        with patch("threading.Thread", ImmediateThread), patch.object(meter, "_now_ms", return_value=10):
            result = supervise_fixture(process, meter.TranscriptCapture(0, timeout_ms=10), broken)
        self.assertFalse(result.accepted)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.stdout, VALID)

    def test_pipe_close_failure_is_recorded_as_incomplete(self):
        class BadClose(BytesIO):
            def close(self):
                raise OSError("synthetic close failure")
        process = FakeProcess()
        process.stderr = BadClose(b"")
        try:
            with patch("threading.Thread", ImmediateThread), patch.object(meter, "_now_ms", return_value=1):
                result = supervise_fixture(process, meter.TranscriptCapture(0), lambda text: None)
        finally:
            BytesIO.close(process.stderr)  # Dispose of the inert failing-close fixture.
        self.assertFalse(result.accepted)
        self.assertFalse(result.capture_complete)

    def signal_fixture(self, phase=None, *, broken_log=False, broken_notice=False):
        """Call the real runner with inert signal/process/file/thread boundaries."""
        events, notices = [], []
        binding = {"handler": "previous", "restored": False}

        def install(number, handler):
            previous = binding["handler"]
            if phase == "restore" and handler == "previous":
                interrupt()
            binding["handler"] = handler
            binding["restored"] = handler == "previous"
            return previous

        def interrupt():
            self.assertFalse(binding["restored"])
            binding["handler"](None, None)
            binding["handler"](None, None)

        def audit(kind, **fields):
            events.append((kind, fields))
            if (phase == "cancel-log" and kind == "meter_cancel"
                    or phase == "exit-log" and kind == "meter_exit"):
                interrupt()
            if broken_log and kind == "meter_started":
                raise OSError("synthetic post-launch journal failure")

        def notify(message):
            notices.append(message)
            if broken_notice:
                raise OSError("synthetic status output failure")

        class SignalPipe(BytesIO):
            def __init__(self, data, name):
                super().__init__(data)
                self.name = name

            def close(self):
                if not self.closed and phase == self.name + "-close":
                    interrupt()
                super().close()

        process = FakeProcess()
        process.stdout, process.stderr = SignalPipe(VALID, "stdout"), SignalPipe(b"", "stderr")
        process.kill, process.terminate, process.send_signal = MagicMock(), MagicMock(), MagicMock()

        def poll():
            if phase == "poll":
                interrupt()
            return 0

        process.poll = poll

        class Readers:
            def __init__(self, capture):
                self.capture = capture
                self.lock = MagicMock()
                self.done = {"stdout": False, "stderr": False}

            def start(self):
                pass

            def attach(self, attached):
                if phase == "attach":
                    interrupt()
                for name in self.done:
                    self.capture.feed(name, getattr(attached, name).read(), 2000)
                    self.capture.end_stream(name, 2000)
                    self.done[name] = True

            def join(self):
                if phase == "join":
                    interrupt()

            def abort(self):
                pass

        def spawn(argv, env):
            if phase in {"spawn", "cancel-log"}:
                interrupt()
            return process

        original_result = meter.TranscriptCapture.result
        result_interrupted = []

        def make_result(capture, exit_code, now_ms):
            result = original_result(capture, exit_code, now_ms)
            if phase == "result" and not result_interrupted:
                result_interrupted.append(True)
                interrupt()
            return result

        with patch("signal.signal", side_effect=install), \
                patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000] + [2000] * 100), \
                patch.object(meter, "getpid", return_value=4242), \
                patch.object(meter.TranscriptCapture, "result", make_result), \
                patch.object(meter, "_PipeReaders", Readers), \
                patch.object(meter, "_spawn", side_effect=spawn), patch.object(meter, "sleep"):
            result = self.run_fixture(log=audit, notify=notify)
        self.assertTrue(binding["restored"])
        process.kill.assert_not_called()
        process.terminate.assert_not_called()
        process.send_signal.assert_not_called()
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)
        return result, events, notices

    def test_repeated_sigint_is_latched_through_launch_supervision_and_cleanup(self):
        for phase in ("spawn", "attach", "poll", "cancel-log", "join",
                      "stdout-close", "stderr-close", "exit-log", "result", "restore"):
            with self.subTest(phase=phase):
                result, events, _ = self.signal_fixture(phase)
                self.assertFalse(result.accepted)
                self.assertTrue(result.cancelled)
                self.assertEqual(result.stdout, VALID)
                self.assertTrue(result.capture_complete)
                self.assertTrue(result.child_exit_confirmed)
                self.assertTrue(result.readers_complete)
                self.assertEqual(sum(kind == "meter_cancel" for kind, _ in events), 1)

    def test_wrapper_child_identity_and_lifecycle_are_distinct(self):
        result, events, notices = self.signal_fixture()
        self.assertTrue(result.accepted)
        self.assertEqual((result.wrapper_pid, result.child_pid), (4242, 5151))
        started = next(fields for kind, fields in events if kind == "meter_started")
        exited = next(fields for kind, fields in events if kind == "meter_child_exit")
        completed = next(fields for kind, fields in events if kind == "meter_exit")
        self.assertFalse(started["child_exit_confirmed"])
        self.assertFalse(exited["readers_complete"])
        self.assertTrue(completed["child_exit_confirmed"])
        self.assertTrue(completed["readers_complete"])
        self.assertEqual((completed["wrapper_pid"], completed["child_pid"]), (4242, 5151))
        self.assertIn("Wrapper PID 4242", notices[0])
        self.assertIn("meter child PID 5151", notices[0])
        self.assertEqual(result.as_dict()["child_pid"], 5151)

    def test_transcript_alone_does_not_claim_observed_process_lifecycle(self):
        result = self.complete()
        self.assertIsNone(result.wrapper_pid)
        self.assertIsNone(result.child_pid)
        self.assertIsNone(result.child_exit_confirmed)
        self.assertIsNone(result.readers_complete)

    def test_post_launch_log_and_notice_failures_do_not_abandon_capture(self):
        for options in ({"broken_log": True}, {"broken_notice": True}):
            with self.subTest(options=options):
                result, _, _ = self.signal_fixture(**options)
                self.assertFalse(result.accepted)
                self.assertEqual(result.stdout, VALID)
                self.assertTrue(result.child_exit_confirmed)
                self.assertTrue(result.readers_complete)

    def test_signal_registration_failure_prevents_child_launch(self):
        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000, 2000]), \
                patch("signal.signal", side_effect=ValueError("synthetic registration failure")), \
                patch.object(meter, "_spawn") as spawn, self.assertRaises(ValueError):
            self.run_fixture()
        spawn.assert_not_called()

    def test_sigint_latched_before_spawn_prevents_launch_and_restores_handler(self):
        handlers = []

        def install(number, handler):
            handlers.append(handler)
            if callable(handler):
                handler(None, None)
            return "previous"

        with patch.object(meter, "platform", "win32"), \
                patch.object(meter, "_verified_executable", return_value="fixture"), \
                patch.object(meter, "_reserve_attempt_log", return_value="fixture.log"), \
                patch.object(meter, "_now_ms", side_effect=[0, 2000, 2000]), \
                patch("signal.signal", side_effect=install), \
                patch.object(meter, "_spawn") as spawn, self.assertRaises(KeyboardInterrupt):
            self.run_fixture()
        spawn.assert_not_called()
        self.assertEqual(handlers[-1], "previous")

    def test_child_exit_does_not_finish_before_output_reader_completion(self):
        capture = meter.TranscriptCapture(0)
        capture.feed("stdout", VALID, 1)
        capture.end_stream("stdout", 1)
        process = FakeProcess()
        process.poll = MagicMock(return_value=0)
        readers = MagicMock()
        readers.done = {"stdout": True, "stderr": False}
        notices = []

        def finish_reader(seconds):
            self.assertTrue(capture.child_exit_confirmed)
            self.assertFalse(capture.readers_complete)
            readers.join.assert_not_called()
            capture.end_stream("stderr", 2)
            readers.done["stderr"] = True

        with patch.object(meter, "_now_ms", return_value=2), \
                patch.object(meter, "sleep", side_effect=finish_reader):
            result = meter._supervise(process, capture, notices.append, readers=readers)
        self.assertTrue(result.accepted)
        self.assertTrue(result.readers_complete)
        self.assertEqual(process.poll.call_count, 1)
        self.assertEqual(len(notices), 1)
        self.assertIn("output readers are still outstanding", notices[0])

    def test_explicit_keyboardinterrupt_during_cleanup_rejects_and_retries_cleanup(self):
        capture = meter.TranscriptCapture(0)
        capture.feed("stdout", VALID, 1)
        capture.end_stream("stdout", 1)
        capture.end_stream("stderr", 1)
        process = FakeProcess()
        original_close = process.stdout.close
        close_calls = []

        def close():
            close_calls.append(None)
            if len(close_calls) == 1:
                raise KeyboardInterrupt
            original_close()

        process.stdout.close = MagicMock(side_effect=close)
        readers = MagicMock()
        readers.done = {"stdout": True, "stderr": True}
        readers.join.side_effect = [KeyboardInterrupt, None]
        with patch.object(meter, "_now_ms", return_value=2):
            result = meter._supervise(process, capture, lambda text: None, readers=readers)
        self.assertTrue(result.cancelled)
        self.assertFalse(result.accepted)
        self.assertTrue(result.child_exit_confirmed)
        self.assertTrue(result.readers_complete)
        self.assertEqual(readers.join.call_count, 2)
        self.assertEqual(process.stdout.close.call_count, 2)


if __name__ == "__main__":
    unittest.main()
