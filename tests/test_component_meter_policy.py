"""Source-model regressions; all process, input-file and clock boundaries inert.

The model describes V3.5.0 application dispatch, not native ReadFile, the binary,
USB calls or driver shutdown. No real subprocess or temporary file is created.
"""

from io import BytesIO
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from tv_autocal_tools import meter


# Independently transcribed selected branch: spotread.c:2189-2207,2969-2970.
PROMPT = (b"\nPlace instrument on spot to be measured,\n"
          b"and hit [A-Z] to read white and setup FWA compensation (keyed to letter)\n"
          b"[a-z] to read and make FWA compensated reading from keyed reference\n"
          b"'r' to set reference, 's' to save spectrum,\n"
          b"'f' to report cal. refresh rate, 'F' to measure refresh rate\n"
          b"'h' to toggle high res., 'k' to do a calibration\n"
          b"Hit ESC or Q to exit, any other key to take a reading: ")
READING = b"\n Result is XYZ: 10.000000 20.000000 30.000000, Yxy: 20.000000 0.166667 0.333333\n"
DIAGNOSTICS = {
    "misread": b"\n\nSpot read failed due to misread (Sample is out of range)\n",
    "comms": b"\n\nSpot read failed due to communication problem.\n",
    "abort": b"\n\nSpot read stopped at user request!\n",
}
RETRY_PROMPT = b"Hit Esc or Q to give up, any other key to retry:"


class SourceProcess:
    """One selected read_sample dispatch; q skips application retry, code=0.

    empty_con_chars and immediate trigger do not consume noninteractive FILE
    input. Other responses take a second successful sample in this finite fake.
    """
    def __init__(self, response, outcome):
        self.samples, self.input_reads, self.pid = 1, 0, 5151
        output = PROMPT
        if outcome in DIAGNOSTICS:
            output += DIAGNOSTICS[outcome] + RETRY_PROMPT
            self.input_reads += 1
            char = response.read(10)[:1]
            if char not in (b"q", b"Q", b"\x1b", b"\x03"):
                self.samples += 1
                output += PROMPT + READING
            output += b"\n"
        elif outcome == "success":
            output += READING
        elif outcome in ("needs-cal", "wrong-position"):
            # spotread.c:2313-2326 can continue without next_con_char.
            self.samples += 1
            output += (b"Spot read failed because instruments needs calibration.\n"
                       if outcome == "needs-cal" else
                       b"Spot read failed due to the sensor being in the wrong position\n")
            output += PROMPT + READING
        elif outcome == "initial-cal":
            self.samples = 0
            output = b"\nSpot read needs a calibration before continuing\n"
        elif outcome == "fatal":
            output += b"\n\nGot fatal error 'Synthetic fatal' (Synthetic detail)\n"
        else:
            raise AssertionError("unsupported source-model outcome")
        self.stdout, self.stderr = BytesIO(output), BytesIO()

    def poll(self):
        return 0  # Upstream cleanup returns zero after these give-up branches.


def complete(output):
    capture = meter.TranscriptCapture(0)
    capture.feed("stdout", output, 1)
    capture.end_stream("stdout", 2)
    capture.end_stream("stderr", 2)
    return capture.result(0, 3)


class MeterPolicyTests(unittest.TestCase):
    def spawn(self, outcome, response=None):
        response = response if response is not None else BytesIO()
        with patch.object(meter, "TemporaryFile", return_value=response) as temporary, \
                patch("subprocess.Popen", side_effect=lambda *a, **k: SourceProcess(k["stdin"], outcome)) as popen:
            process = meter._spawn(["inert.exe"], meter.isolated_environment({}))
        temporary.assert_called_once_with(mode="w+b")
        self.assertFalse(popen.call_args.kwargs["shell"])
        self.assertIs(popen.call_args.kwargs["stdin"], response)
        self.assertEqual(popen.call_args.kwargs["env"]["ARGYLL_NOT_INTERACTIVE"], "1")
        return process, response

    def test_success_does_not_consume_give_up_response(self):
        process, response = self.spawn("success")
        try:
            self.assertEqual(process.input_reads, 0)
            self.assertEqual(response.read(), b"q\n")
            self.assertTrue(complete(process.stdout.read()).accepted)
        finally:
            response.close()

    def test_misread_comms_and_abort_give_up_without_application_retry(self):
        for outcome in DIAGNOSTICS:
            with self.subTest(outcome=outcome):
                process, response = self.spawn(outcome)
                try:
                    self.assertEqual((process.samples, process.input_reads), (1, 1))
                    self.assertFalse(complete(process.stdout.read()).accepted)
                    self.assertEqual(response.tell(), 2)
                finally:
                    response.close()

    def test_uncontrolled_retry_cannot_turn_error_into_accepted_reading(self):
        for outcome in DIAGNOSTICS:
            for supplied in (b"", b" ", b"\n"):
                with self.subTest(outcome=outcome, supplied=supplied):
                    process = SourceProcess(BytesIO(supplied), outcome)
                    self.assertEqual(process.samples, 2)
                    output = process.stdout.read()
                    self.assertIn(READING, output)
                    self.assertFalse(complete(output).accepted)

    def test_nonprompting_continuations_do_not_consume_q_and_cannot_pass(self):
        for outcome, samples in (("needs-cal", 2), ("wrong-position", 2),
                                 ("initial-cal", 0), ("fatal", 1)):
            with self.subTest(outcome=outcome):
                process, response = self.spawn(outcome)
                try:
                    self.assertEqual((process.samples, process.input_reads), (samples, 0))
                    self.assertEqual(response.read(), b"q\n")
                    self.assertEqual(process.poll(), 0)
                    self.assertFalse(complete(process.stdout.read()).accepted)
                finally:
                    response.close()

    def test_calibration_position_and_unknown_prompts_reject_later_success(self):
        for text in (b"Spot read needs a calibration before continuing\n",
                     b"Calibration complete\n", b"Sensor position changed\n",
                     b"Spot read failed due to the sensor being in the wrong position\n",
                     b"Place instrument on calibration tile\n", b"Got fatal error\n",
                     b"Hit Esc or Q to give up, any other key to retry:", b"unexpected\n"):
            for output in (text + PROMPT + READING, PROMPT + text + READING,
                           PROMPT + READING + text):
                with self.subTest(text=text, output=output):
                    self.assertFalse(complete(output).accepted)

    def test_exact_success_prompt_required_and_crlf_supported(self):
        self.assertTrue(complete(PROMPT + READING).accepted)
        self.assertTrue(complete((PROMPT + READING).replace(b"\n", b"\r\n")).accepted)
        for output in (READING, PROMPT[1:] + READING, PROMPT + PROMPT + READING,
                       PROMPT[:-1] + READING, PROMPT + READING[:-1]):
            self.assertFalse(complete(output).accepted)

    def test_partial_diagnostic_chunks_never_escape_strict_final_grammar(self):
        for boundary in range(len(b"Spot read stopped at user request!")):
            capture = meter.TranscriptCapture(0)
            output = PROMPT + READING + b"Spot read stopped at user request!\n"
            split = len(PROMPT + READING) + boundary
            capture.feed("stdout", output[:split], 1)
            capture.feed("stdout", output[split:], 2)
            capture.end_stream("stdout", 3)
            capture.end_stream("stderr", 3)
            self.assertFalse(capture.result(0, 4).accepted)

    def test_inherited_mode_removed_case_insensitively_even_empty_and_zero(self):
        for value in ("", "0", "1", "unexpected"):
            original = {"ARGYLL_NOT_INTERACTIVE": value, "argyll_not_interactive": value,
                        "Argyll_Not_Interactive": value, "OTHER": "kept"}
            self.assertEqual(meter.isolated_environment(original),
                             {"ARGYLL_NOT_INTERACTIVE": "1", "OTHER": "kept"})
            self.assertEqual(len(original), 4)

    def test_input_preparation_failures_prevent_any_launch(self):
        for stage in ("write", "short-write", "flush", "seek", "wrong-seek"):
            response = MagicMock()
            response.write.return_value, response.seek.return_value = 2, 0
            if stage == "short-write":
                response.write.return_value = 1
            elif stage == "wrong-seek":
                response.seek.return_value = 1
            else:
                getattr(response, stage).side_effect = OSError("synthetic input failure")
            with self.subTest(stage=stage), patch.object(meter, "TemporaryFile", return_value=response), \
                    patch("subprocess.Popen") as popen, self.assertRaises(OSError):
                meter._spawn([], {})
            popen.assert_not_called()
            response.close.assert_called_once()

    def test_input_allocation_and_spawn_failure_prevent_or_clean_up_input(self):
        with patch.object(meter, "TemporaryFile", side_effect=OSError("no resource")), \
                patch("subprocess.Popen") as popen, self.assertRaises(OSError):
            meter._spawn([], {})
        popen.assert_not_called()
        response = BytesIO()
        with patch.object(meter, "TemporaryFile", return_value=response), \
                patch("subprocess.Popen", side_effect=OSError("no process")), self.assertRaises(OSError):
            meter._spawn([], {})
        self.assertTrue(response.closed)

    def test_input_closes_after_child_and_readers_and_close_failure_rejects(self):
        for failed in (False, True):
            events = []
            capture = meter.TranscriptCapture(0, log=lambda kind, **fields: events.append(kind))
            capture.feed("stdout", PROMPT + READING, 1)
            capture.end_stream("stdout", 1)
            capture.end_stream("stderr", 1)
            response = MagicMock()
            readers = MagicMock()
            readers.done = {"stdout": True, "stderr": True}
            def close():
                self.assertTrue(capture.child_exit_confirmed)
                self.assertTrue(capture.readers_complete)
                readers.join.assert_called_once()
                events.append("input-close-attempt")
                if failed:
                    raise OSError("synthetic close failure")
            response.close.side_effect = close
            process = SimpleNamespace(stdout=BytesIO(), stderr=BytesIO(), poll=lambda: 0,
                                      _component_response_input=response)
            with self.subTest(failed=failed), patch.object(meter, "_now_ms", return_value=2):
                result = meter._supervise(process, capture, lambda text: None, readers=readers)
                self.assertEqual(result.accepted, not failed)
            response.close.assert_called_once()
            self.assertLess(events.index("meter_child_exit"), events.index("meter_readers_complete"))
            self.assertLess(events.index("meter_readers_complete"), events.index("input-close-attempt"))
            self.assertLess(events.index("input-close-attempt"), events.index("meter_wrapper_complete"))
            self.assertLess(events.index("meter_wrapper_complete"), events.index("meter_exit"))


if __name__ == "__main__":
    unittest.main()
