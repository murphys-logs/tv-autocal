"""Entry-point and journal checks using memory only; no equipment or GUI."""

from contextlib import ExitStack, redirect_stdout
from dataclasses import replace
from io import BytesIO, StringIO
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tv_autocal import meter_output, renderer
from tv_autocal_tools import cli
from tv_autocal_tools import meter, presenter, receipt, serial_tool
from tv_autocal_tools.journal import Journal, JournalError, private_path
from tv_autocal_tools.permission import HardwarePermit, permit_from_dict


PERMIT = HardwarePermit("T-003", "a" * 40, "Synthetic test authorisation; no equipment",
                        "fixture steps", "fixture evidence", ("present", "meter"))


class MemoryFile(BytesIO):
    def fileno(self):
        return 123

    def close(self):
        self.saved = self.getvalue()
        super().close()


class ComponentEntryTests(unittest.TestCase):
    def armed_run(self, tool, extra, *, failure=None, meter_result=None, receipts=None):
        """Exercise CLI wiring with inert boundaries, never a real hardware call."""
        plan = "T-006" if tool == "serial" else "T-003"
        record = {"plan": plan, "revision": "a" * 40, "authorisation": "synthetic fixture",
                  "steps": "fixture", "evidence": "fixture", "actions": [tool]}
        events = []

        class FakeJournal:
            def __init__(self, path):
                self.path = path

            def __call__(self, kind, **fields):
                events.append((kind, fields))

            def close(self):
                events.append(("closed", {}))

        with ExitStack() as stack:
            stack.enter_context(patch.object(Path, "open", return_value=BytesIO(json.dumps(record).encode())))
            stack.enter_context(patch.object(cli, "Journal", FakeJournal))
            stack.enter_context(patch.object(cli, "source_fingerprints", return_value={"fixture.py": "b" * 64}))
            window = stack.enter_context(patch.object(presenter, "run_presenter", side_effect=failure))
            measurement = stack.enter_context(patch.object(meter, "run_meter", return_value=meter_result))
            serial = stack.enter_context(patch.object(serial_tool, "run_serial", return_value=serial_tool.SerialResult(
                True, True, True, "fixture completed", 5, 15, 0, ((None, 1, 10), (2, 3, 20), (4, 5, 30)))))
            stack.enter_context(patch.object(receipt, "read_receipt", side_effect=receipts))
            stack.enter_context(redirect_stdout(StringIO()))
            arguments = [tool, "--hardware", "--permit", "local/fixture.json",
                         "--confirm", "RUN " + plan + " " + "a" * 40,
                         "--log", "local/evidence.log"] + extra
            if failure:
                with self.assertRaisesRegex(RuntimeError, "fixture failure"):
                    cli.main(arguments)
                code = None
            else:
                code = cli.main(arguments)
            return code, events, window, measurement, serial

    def test_armed_presenter_cli_dispatch_is_explicit_and_fake_only(self):
        code, events, window, measurement, serial = self.armed_run("present", ["--x", "0", "--y", "0"])
        self.assertEqual(code, 0)
        window.assert_called_once()
        self.assertEqual(window.call_args.kwargs["sequence"], ((128, 128, 128),))
        measurement.assert_not_called()
        serial.assert_not_called()
        self.assertEqual([x[0] for x in events], ["authorisation", "software_identity", "closed"])

    def test_armed_cli_records_backend_failure_before_journal_closure(self):
        _, events, _, _, _ = self.armed_run("present", ["--x", "0", "--y", "0"],
                                          failure=RuntimeError("fixture failure"))
        self.assertEqual(events[-2][0], "tool-aborted")
        self.assertEqual(events[-2][1]["error_type"], "RuntimeError")
        self.assertEqual(events[-1][0], "closed")

    def test_meter_cli_compares_presentation_evidence_and_retains_rejected_raw_result(self):
        capture = meter.TranscriptCapture(0, timeout_ms=100)
        raw = b"Result is XYZ: 1 2 3, Yxy: 2 .1 .2\n"
        capture.feed("stdout", raw, 1)
        capture.end_stream("stdout", 2)
        capture.end_stream("stderr", 2)
        result = capture.result(0, 2)
        evidence = SimpleNamespace(as_dict=lambda: {"sequence": 1, "rgb": (128, 128, 128)})
        extra = ["--attempt-log", "local/T-003/attempt.log", "--purpose", "initial-access",
                 "--presentation-log", "local/presenter.log", "--presentation-sequence", "1",
                 "--rgb", "128,128,128", "--isolated", "--exit-confirmed", "--discovery-confirmed"]
        for changed in (False, True):
            with self.subTest(changed=changed):
                after = ValueError("presentation closed") if changed else evidence
                code, events, _, measurement, _ = self.armed_run(
                    "meter", extra, meter_result=result, receipts=[evidence, after])
                self.assertEqual(code, 2 if changed else 0)
                measurement.assert_called_once()
                summary = next(fields for name, fields in events if name == "meter_result")
                self.assertEqual(summary["accepted"], not changed)
                self.assertEqual(summary["stdout_bytes"], len(raw))
                self.assertNotIn("stdout", summary)
                self.assertEqual(result.stdout, raw)

    def test_serial_cli_uses_closed_complete_result_and_records_outcome(self):
        code, events, window, measurement, serial = self.armed_run(
            "serial", ["--port", "COM_TEST", "--menu-window-ms", "5000", "--prerequisites-confirmed"])
        self.assertEqual(code, 0)
        serial.assert_called_once()
        self.assertEqual(serial.call_args.kwargs["menu_window_ms"], 5000)
        window.assert_not_called()
        measurement.assert_not_called()
        self.assertTrue(next(fields for name, fields in events if name == "serial_result")["accepted"])

    def test_permit_is_disabled_by_default_and_scoped_to_plan_action(self):
        with self.assertRaises(PermissionError):
            PERMIT.require("present")
        replace(PERMIT, hardware=True).require("present")
        replace(PERMIT, hardware=True).require("meter")
        for permit, action in ((replace(PERMIT, hardware=True), "serial"),
                               (replace(PERMIT, hardware=True, plan="T-008"), "meter"),
                               (replace(PERMIT, hardware=True, actions=("present",)), "meter"),
                               (replace(PERMIT, hardware=1), "present")):
            with self.subTest(permit=permit, action=action), self.assertRaises(PermissionError):
                permit.require(action)

    def test_permit_needs_full_commit_text_and_exact_confirmation(self):
        for field, value in (("revision", "short"), ("revision", "G" * 40),
                             ("authorisation", ""), ("steps", " "), ("evidence", "x" * 4097),
                             ("actions", ()), ("actions", ("serial",))):
            with self.subTest(field=field), self.assertRaises(PermissionError):
                replace(PERMIT, hardware=True, **{field: value}).require("present")
        record = {"plan": "T-003", "revision": "a" * 40, "authorisation": "fixture",
                  "steps": "fixture", "evidence": "fixture", "actions": ["meter"]}
        permit = permit_from_dict(record, hardware=True, confirmation="RUN T-003 " + "a" * 40)
        permit.require("meter")
        with self.assertRaises(PermissionError):
            permit_from_dict(record, hardware=True, confirmation="yes")
        with self.assertRaises(ValueError):
            permit_from_dict({**record, "hardware": True}, hardware=True, confirmation="yes")

    def test_default_and_unarmed_tools_never_open_files_devices_or_processes(self):
        targets = ("builtins.open", "io.open", "os.open", "os.system", "subprocess.Popen",
                   "socket.socket", "socket.create_connection", "socket.getaddrinfo")
        with ExitStack() as stack:
            for target in targets:
                stack.enter_context(patch(target, side_effect=AssertionError("Unexpected I/O: " + target)))
            for arguments in ([], ["simulate"], ["present"], ["meter"], ["serial"]):
                with self.subTest(arguments=arguments), redirect_stdout(StringIO()) as output:
                    self.assertEqual(cli.main(arguments), 0)
                    value = json.loads(output.getvalue())
                    self.assertEqual(value["mode"], "simulation")
                    self.assertFalse(value["hardware_operated"])
                    self.assertFalse(value["hardware_adapters_exercised"])
                    self.assertEqual(value["frame"]["patch"], {"x": 1440, "y": 810, "width": 960, "height": 540})
                    self.assertEqual(value["frame"]["area_percent"], 6.25)

    def test_incomplete_opt_in_fails_before_any_local_or_device_open(self):
        with patch("io.open", side_effect=AssertionError("Unexpected open")):
            for args in (["meter", "--hardware"], ["serial", "--hardware", "--port", "COM_TEST"],
                         ["present", "--permit", "local/fixture.json"]):
                with self.subTest(args=args), self.assertRaises(PermissionError):
                    cli.main(args)

    def test_private_paths_reject_external_traversal_and_wrong_extension(self):
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(private_path("local/fixture.log", suffix=".log"), root / "local/fixture.log")
        for value in ("../elsewhere.log", "local/../../elsewhere.log", "fixture.log",
                      "local/fixture.txt", "local", "local/fixture.log:secret", "local/NUL.log",
                      "local/COM1.log", "local/lpt9.log", "local/AUX/sub.log", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                private_path(value, suffix=".log")

    def test_visual_and_patch_sequences_reuse_existing_manifest(self):
        options = cli.parser().parse_args(["present", "--sequence", "t003"])
        grey = (128, 128, 128)
        self.assertEqual(cli.sequence_for(options), (grey,) + tuple((x, x, x) for x in renderer.T003_RANGE_CODES) + (grey,))
        options = cli.parser().parse_args(["present", "--sequence", "t005-optical"])
        sequence = cli.sequence_for(options)
        self.assertEqual(sequence[:12], (grey,) + tuple((x, x, x) for x in renderer.T005_NEUTRAL_CODES) + (grey,))
        self.assertEqual(sequence[12:16], ((204, 0, 0), (230, 0, 0), (242, 0, 0), (255, 0, 0)))
        self.assertEqual(sequence[-1], grey)
        options = cli.parser().parse_args(["present", "--sequence", "t005-visual"])
        self.assertEqual(cli.sequence_for(options), tuple(x.name for x in renderer.pattern_manifest()))

    def test_measurement_context_cannot_mislabel_a_different_patch_as_reference(self):
        for plan, purpose, rgb in (("T-003", "initial-access", (255, 255, 255)),
                                   ("T-003", "warmup-30", (0, 0, 0)),
                                   ("T-003", "range", (128, 128, 128)),
                                   ("T-005", "middle-reference", (255, 0, 0)),
                                   ("T-005", "neutral", (255, 0, 0)),
                                   ("T-005", "primary", (255, 255, 0)),
                                   ("T-005", "primary", (0, 0, 128)),
                                   ("T-003", "unknown", (128, 128, 128))):
            with self.subTest(plan=plan, purpose=purpose, rgb=rgb), self.assertRaises(ValueError):
                cli.validate_measurement_context(plan, purpose, rgb)
        cli.validate_measurement_context("T-003", "warmup-40", (128, 128, 128))
        cli.validate_measurement_context("T-003", "range", (0, 0, 0))
        cli.validate_measurement_context("T-005", "primary", (0, 230, 0))

    def test_journal_is_exclusive_flushes_every_event_and_reserves_final_record(self):
        stream = MemoryFile()
        with patch.object(Path, "mkdir"), patch.object(Path, "open", return_value=stream) as opening, \
                patch("tv_autocal_tools.journal.os.fsync") as syncing:
            log = Journal(private_path("local/fixture.log", suffix=".log"), max_bytes=8192)
            opening.assert_called_once_with("xb")
            log("write-intent", bytes_hex="08220d00002d9c", mode="fixture")
            self.assertEqual(syncing.call_count, 1)
            with self.assertRaises(JournalError):
                log("large", text="x" * 8192)
            with self.assertRaises(JournalError):
                log("must-not-recover")
            log.close()
            log.close()
        records = [json.loads(line) for line in stream.saved.splitlines()]
        self.assertEqual([item["event"] for item in records], ["write-intent", "journal-close"])
        self.assertFalse(records[-1]["complete"])
        self.assertLessEqual(len(stream.saved), 8192)

    def test_journal_disk_failure_is_terminal(self):
        stream = MemoryFile()
        with patch.object(Path, "mkdir"), patch.object(Path, "open", return_value=stream), \
                patch("tv_autocal_tools.journal.os.fsync", side_effect=OSError("fixture full disk")):
            log = Journal(private_path("local/fixture.log", suffix=".log"))
            with self.assertRaises(JournalError):
                log("write-intent")
            with self.assertRaises(JournalError):
                log("later-write")
            with self.assertRaises(JournalError):
                log.close()
        self.assertTrue(stream.closed)


if __name__ == "__main__":
    unittest.main()
