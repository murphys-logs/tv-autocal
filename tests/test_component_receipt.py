"""Synthetic presenter journals read from memory; no files or devices opened."""

from copy import deepcopy
from dataclasses import FrozenInstanceError
from io import BytesIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tv_autocal_tools.receipt import MAX_JOURNAL_BYTES, read_receipt


REVISION = "a" * 40
RGB = (128, 128, 128)


def records():
    events = [
        ("authorisation", {"mode": "hardware", "plan": "T-003", "revision": REVISION, "actions": ["present"]}),
        ("software_identity", {"python": "fixture", "files": {"fixture.py": "b" * 64}}),
        ("presenter_target_confirmed", {"hardware": True}),
        ("pattern_present_intent", {"hardware": True, "sequence": 1, "pattern": list(RGB),
                                    "width": 3840, "height": 2160, "sha256": "c" * 64}),
        ("pattern_buffer_applied", {"hardware": True, "sequence": 1}),
    ]
    return [{"event": event, "sequence": index, "monotonic_ns": index + 1,
             "utc": "2026-10-27T20:00:00+00:00", "fields": fields}
            for index, (event, fields) in enumerate(events)]


def encoded(events):
    return b"".join(json.dumps(event).encode() + b"\n" for event in events)


class ComponentReceiptTests(unittest.TestCase):
    def read(self, value=None, **changes):
        data = encoded(records() if value is None else value) if not isinstance(value, bytes) else value
        with patch.object(Path, "open", return_value=BytesIO(data)) as opening:
            result = read_receipt("local/presenter-fixture.log", **{
                "plan": "T-003", "revision": REVISION, "sequence": 1, "rgb": RGB, **changes})
            opening.assert_called_once_with("rb")
            return result

    def test_matching_immutable_receipt_and_metadata_are_not_display_proof(self):
        receipt = self.read()
        self.assertEqual((receipt.sequence, receipt.rgb, receipt.frame_sha256), (1, RGB, "c" * 64))
        self.assertEqual(set(receipt.as_dict()), {"path", "plan", "revision", "sequence", "rgb", "frame_sha256"})
        self.assertTrue(receipt.path.endswith("presenter-fixture.log"))
        self.assertEqual(self.read(), receipt)
        with self.assertRaises(FrozenInstanceError):
            receipt.sequence = 2
        changed = records()
        changed[0]["monotonic_ns"] = 0
        self.assertNotEqual(self.read(changed), receipt)

    def test_plan_revision_action_rgb_and_sequence_mismatches_reject(self):
        for changes in ({"plan": "T-005"}, {"revision": "b" * 40}, {"rgb": (255, 255, 255)}, {"sequence": 2}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.read(**changes)
        for key, value in (("actions", ["meter"]), ("mode", "simulation")):
            events = records()
            events[0]["fields"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.read(events)

    def test_newer_frame_even_with_identical_rgb_and_pending_intent_reject(self):
        events = records()
        next_intent = deepcopy(events[3])
        next_intent.update(sequence=5, monotonic_ns=6)
        next_intent["fields"]["sequence"] = 2
        with self.assertRaises(ValueError):
            self.read(events + [next_intent])
        next_applied = deepcopy(events[4])
        next_applied.update(sequence=6, monotonic_ns=7)
        next_applied["fields"]["sequence"] = 2
        with self.assertRaises(ValueError):
            self.read(events + [next_intent, next_applied])
        self.assertEqual(self.read(events + [next_intent, next_applied], sequence=2).sequence, 2)

    def test_stops_closure_abort_error_and_incomplete_markers_reject(self):
        for event, fields in (("presenter_closed", {}), ("journal-close", {}), ("tool-aborted", {}),
                              ("log-error", {}), ("metadata", {"aborted": True}),
                              ("metadata", {"log_complete": False}), ("metadata", {"error": "failed"})):
            events = records() + [{"event": event, "sequence": 5, "monotonic_ns": 6, "fields": fields}]
            with self.subTest(event=event, fields=fields), self.assertRaises(ValueError):
                self.read(events)

    def test_duplicate_reordered_missing_records_and_invalid_times_reject(self):
        for index, field, value in ((2, "sequence", 1), (2, "sequence", 3), (0, "sequence", True),
                                    (3, "monotonic_ns", -1), (4, "monotonic_ns", 2),
                                    (4, "monotonic_ns", True), (4, "monotonic_ns", 2**63),
                                    (4, "utc", "not a date"), (4, "utc", "2026-10-27T20:00:00")):
            events = records()
            events[index][field] = value
            with self.subTest(index=index, field=field, value=value), self.assertRaises(ValueError):
                self.read(events)

    def test_missing_duplicate_or_mismatched_intent_applied_pairs_reject(self):
        for index, key, value in ((3, "sequence", 2), (4, "sequence", 2),
                                  (4, "sequence", True), (4, "hardware", False)):
            events = records()
            events[index]["fields"][key] = value
            with self.subTest(index=index, key=key), self.assertRaises(ValueError):
                self.read(events)
        with self.assertRaises(ValueError):
            self.read(records()[:3])
        with self.assertRaises(ValueError):
            self.read(records()[:4])
        events = records()
        events[3]["event"] = "metadata"
        with self.assertRaises(ValueError):
            self.read(events)

    def test_native_dimensions_hash_and_pattern_types_are_required(self):
        for key, value in (("width", 1920), ("height", 1080), ("hardware", 1),
                           ("sha256", "not a digest"), ("pattern", [True, 128, 128]),
                           ("pattern", [128, 128]), ("pattern", [128, 128, 256]),
                           ("pattern", [102, 102, 102])):
            events = records()
            events[3]["fields"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.read(events)

    def test_visual_frame_may_precede_rgb_but_cannot_be_used_as_meter_patch(self):
        events = records()
        events[0]["fields"]["plan"] = "T-005"
        events[3]["fields"]["pattern"] = "geometry"
        with self.assertRaises(ValueError):
            self.read(events, plan="T-005")
        later = deepcopy(records()[3:])
        for index, event in enumerate(later, 5):
            event.update(sequence=index, monotonic_ns=index + 1)
            event["fields"]["sequence"] = 2
        self.assertEqual(self.read(events + later, plan="T-005", sequence=2).rgb, RGB)

    def test_empty_partial_invalid_json_duplicate_keys_and_oversize_reject(self):
        for data in (b"", encoded(records())[:-1], b"invalid\n", b"{}\n", b"null\n", b"\n",
                     b'{"event":"one","event":"two"}\n', b'{"value":NaN}\n', b"\xff\n",
                     b"x" * (MAX_JOURNAL_BYTES + 1), b" " * 65537 + b"\n"):
            with self.subTest(length=len(data)), self.assertRaises(ValueError):
                self.read(data)

    def test_bad_arguments_and_non_private_path_fail_before_open(self):
        for changes in ({"plan": "T-006"}, {"revision": "short"}, {"sequence": False},
                         {"sequence": 257}, {"rgb": [128, 128, 128]}):
            with self.subTest(changes=changes), patch.object(Path, "open") as opening:
                with self.assertRaises(ValueError):
                    read_receipt("local/presenter-fixture.log", **{
                        "plan": "T-003", "revision": REVISION, "sequence": 1, "rgb": RGB, **changes})
                opening.assert_not_called()
        with patch.object(Path, "open") as opening:
            with self.assertRaises(ValueError):
                read_receipt("../outside.log", plan="T-003", revision=REVISION, sequence=1, rgb=RGB)
            opening.assert_not_called()


if __name__ == "__main__":
    unittest.main()
