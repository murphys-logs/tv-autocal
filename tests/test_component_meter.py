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
        capture = meter.TranscriptCapture(0)
        readers = MagicMock()
        readers.lock.__enter__.return_value = None
        process = FakeProcess()
        def spawn(argv, env):
            handlers[0](None, None)
            return process
        with patch("signal.signal", side_effect=install), patch.object(meter, "_spawn", side_effect=spawn), \
                patch.object(meter, "_now_ms", return_value=1):
            returned = meter._attach_launch(["fixture"], {}, capture, readers)
        self.assertIs(returned, process)
        readers.attach.assert_called_once_with(process)
        self.assertTrue(capture.cancelled)
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


if __name__ == "__main__":
    unittest.main()
