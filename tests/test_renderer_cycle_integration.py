"""Software-only composition checks; no display or device backend is imported."""

from contextlib import redirect_stdout
from io import StringIO
import json
import unittest

from tv_autocal import demo


class RendererCycleIntegrationTests(unittest.TestCase):
    def test_demo_links_exact_patch_metadata_to_every_synthetic_attempt(self):
        report = demo.build_demo()
        self.assertTrue(report["simulated"])
        self.assertFalse(report["frame"]["presented_on_display"])
        self.assertEqual((report["frame"]["width"], report["frame"]["height"], report["frame"]["bytes"]),
                         (3840, 2160, 24883200))
        self.assertEqual(report["frame"]["patch_rgb"], (128, 128, 128))
        self.assertEqual([row["phase"] for row in report["records"]], ["baseline", "change", "restore"])
        self.assertEqual([row["target_level"] for row in report["records"]], [50, 49, 50])
        self.assertEqual([row["xyz"] for row in report["records"]],
                         [(10.0, 20.0, 30.0), (9.0, 19.0, 29.0), (10.0, 20.0, 30.0)])
        self.assertEqual([row["read_started_ms"] for row in report["records"]], [2000, 4000, 6000])
        for row in report["records"]:
            self.assertEqual(row["patch_rgb"], report["frame"]["patch_rgb"])
            self.assertTrue(row["simulated"])
            self.assertTrue(row["accepted"])
            self.assertIn("never calibration data", row["purpose"])
        self.assertEqual(report["final_level"], report["original_level"])
        self.assertFalse(report["restoration_required"])

    def test_cli_emits_only_a_json_report_and_rejects_options_before_running(self):
        for options in (("--port", "COM_TEST"), ("--real",), ("--output", "example.ppm"), []):
            with self.subTest(options=options), self.assertRaises(ValueError):
                demo.main(options)
        output = StringIO()
        with redirect_stdout(output):
            demo.main()
        report = json.loads(output.getvalue())
        self.assertTrue(report["simulated"])
        self.assertEqual(report["fake_time_ms"], 6000)
        self.assertEqual([item["name"] for item in report["visual_manifest"]],
                         ["geometry", "black", "white", "red", "green", "blue", "detail"])
        self.assertTrue(all(event["simulated"] for event in report["events"]))


if __name__ == "__main__":
    unittest.main()
