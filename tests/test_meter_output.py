"""Authored transcript fixtures, never captured or measured equipment data."""

from dataclasses import FrozenInstanceError
import unittest

from tv_autocal.meter_output import MAX_OUTPUT_BYTES, parse_meter_output


VALID = b"\n Result is XYZ: 10.000000 20.000000 30.000000, D50 Lab: 50.000000 1.000000 -2.000000\n"


class MeterOutputTests(unittest.TestCase):
    def test_source_format_extracts_xyz_and_retains_exact_raw_bytes(self):
        stdout = b"Place instrument on the test patch.\r\n" + VALID.replace(b"\n", b"\r\n")
        result = parse_meter_output(stdout, b"", 0)
        self.assertTrue(result.accepted)
        self.assertEqual(result.xyz, (10.0, 20.0, 30.0))
        self.assertEqual(result.output_format, "D50 Lab")
        self.assertIs(result.stdout, stdout)
        self.assertEqual((result.stderr, result.exit_code), (b"", 0))
        self.assertTrue(result.simulated)
        self.assertIn("never calibration data", result.purpose)
        with self.assertRaises(FrozenInstanceError):
            result.accepted = False

    def test_source_prompt_branch_with_both_result_forms_and_line_endings(self):
        # S-043, ArgyllCMS V3.5.0 spectro/spotread.c:2189-2207.
        # One authored manual/no-reference/no-target/no-switch fixture branch,
        # with SALONEINSTLIB unset; not a captured or predicted Spyder5 transcript.
        # numlib/numsup.c:208,223 defines fl_end as the empty string.
        prompt = (
            b"\nPlace instrument on spot to be measured,\n"
            b"and hit [A-Z] to read white and setup FWA compensation (keyed to letter)\n"
            b"[a-z] to read and make FWA compensated reading from keyed reference\n"
            b"'r' to set reference, 's' to save spectrum,\n"
            b"'f' to report cal. refresh rate, 'F' to measure refresh rate\n"
            b"'h' to toggle high res., 'k' to do a calibration\n"
            b"Hit ESC or Q to exit, any other key to take a reading: "
        )
        results = (
            ("D50 Lab", VALID),
            ("Yxy", b"\n Result is XYZ: 10.000000 20.000000 30.000000, "
             b"Yxy: 20.000000 0.166667 0.333333\n"),
        )
        for output_format, result_line in results:
            for newline in (b"\n", b"\r\n"):
                with self.subTest(output_format=output_format, newline=newline):
                    stdout = (prompt + result_line).replace(b"\n", newline)
                    result = parse_meter_output(stdout, b"", 0)
                    self.assertTrue(result.accepted)
                    self.assertEqual(result.xyz, (10.0, 20.0, 30.0))
                    self.assertEqual(result.output_format, output_format)
                    self.assertIs(result.stdout, stdout)
                    self.assertEqual((result.stderr, result.exit_code), (b"", 0))
                    self.assertTrue(result.simulated)

    def test_numeric_fixture_notation_and_finite_zero_negative_values(self):
        stdout = b" Result is XYZ: -0.5 +2e1 .0, D50 Lab: 1. 2E-2 -3\n"
        result = parse_meter_output(stdout, b"", 0)
        self.assertTrue(result.accepted)
        self.assertEqual(result.xyz, (-0.5, 20.0, 0.0))

    def test_planned_x_option_yxy_format_extracts_xyz_without_confusing_yxy(self):
        stdout = b" Result is XYZ: 10.000000 20.000000 30.000000, Yxy: 20.000000 0.166667 0.333333\n"
        result = parse_meter_output(stdout, b"", 0)
        self.assertTrue(result.accepted)
        self.assertEqual(result.xyz, (10.0, 20.0, 30.0))
        self.assertEqual(result.output_format, "Yxy")
        self.assertEqual(result.stdout, stdout)
        invalid = parse_meter_output(stdout.replace(b"0.166667", b"NaN"), b"", 0)
        self.assertFalse(invalid.accepted)
        self.assertIsNone(invalid.output_format)

    def test_result_must_be_complete_and_unique(self):
        for stdout in (b"", b"ordinary prompt\n", VALID[:-1], VALID + VALID,
                       VALID + b"Result is XYZ: 1 2\n", b"Result is XYZ: 1 2\n"):
            with self.subTest(stdout=stdout):
                result = parse_meter_output(stdout, b"", 0)
                self.assertFalse(result.accepted)
                self.assertIsNone(result.xyz)
                self.assertIsNone(result.output_format)
                self.assertEqual(result.stdout, stdout)

    def test_alternate_and_reference_modes_are_rejected(self):
        for stdout in (VALID.replace(b"D50 Lab:", b"D65 Lab:"),
                       VALID.replace(b"D50 Lab:", b"LCh:"),
                       VALID.replace(b"D50 Lab:", b"Yuv:"),
                       b"Result is Y: 20, L*: 50\n",
                       b"Reference is now XYZ: 1 2 3 Lab: 4 5 6\n" + VALID,
                       b"Making result XYZ: 1 2 3, D50 Lab: 4 5 6 white reference.\n" + VALID,
                       b"Preset ref. XYZ 1 2 3, D50 Lab 4 5 6\n" + VALID):
            with self.subTest(stdout=stdout):
                self.assertFalse(parse_meter_output(stdout, b"", 0).accepted)

    def test_malformed_result_fields_or_suffix_cannot_be_ignored(self):
        for stdout in (VALID.replace(b"20.000000", b"twenty"),
                       VALID.replace(b"20.000000", b"20,0"),
                       VALID.replace(b", D50", b" 40, D50"),
                       VALID.replace(b" -2.000000", b""),
                       VALID.replace(b"Result is", b"result is"),
                       VALID.replace(b"\n", b" junk\n"),
                       VALID + b"result is invalid\n",
                       VALID + b" Result isXYZ: 4 5 6\n",
                       VALID + b" Result XYZ: 4 5 6\n",
                       VALID + b" Result\n"):
            with self.subTest(stdout=stdout):
                self.assertFalse(parse_meter_output(stdout, b"", 0).accepted)

    def test_nonfinite_numeric_fields_are_rejected(self):
        for field in (b"10.000000", b"-2.000000"):
            for value in (b"NaN", b"inf", b"-Infinity", b"1e9999"):
                with self.subTest(field=field, value=value):
                    self.assertFalse(parse_meter_output(VALID.replace(field, value), b"", 0).accepted)

    def test_exit_timeout_cancellation_and_stderr_override_plausible_xyz(self):
        for exit_code, stderr, options in (
            (None, b"", {}), (1, b"", {}), (-1, b"", {}),
            (0, b"warning details", {}), (0, b"\n", {}),
            (0, b"", {"timed_out": True}), (0, b"", {"cancelled": True}),
            (0, b"", {"timed_out": True, "cancelled": True}),
        ):
            with self.subTest(exit_code=exit_code, stderr=stderr, options=options):
                result = parse_meter_output(VALID, stderr, exit_code, **options)
                self.assertFalse(result.accepted)
                self.assertIsNone(result.xyz)
                self.assertEqual((result.stdout, result.stderr, result.exit_code), (VALID, stderr, exit_code))

    def test_diagnostics_fail_closed_but_ordinary_abort_prompt_is_allowed(self):
        for diagnostic in (b"Warning: suspect sample\n", b"Spot read got abort or error from calibrate\n",
                           b"Measurement failed\n", b"failure\n", b"Aborted\n"):
            with self.subTest(diagnostic=diagnostic):
                self.assertFalse(parse_meter_output(VALID + diagnostic, b"", 0).accepted)
        self.assertTrue(parse_meter_output(b"Press escape to abort.\n" + VALID, b"", 0).accepted)

    def test_unsupported_encoding_and_control_characters_rejected(self):
        for extra in (b"\xff", b"\x00", b"\x1b", b"\x7f", b"\x1c"):
            with self.subTest(extra=extra):
                stdout = extra + b"\n" + VALID
                result = parse_meter_output(stdout, b"", 0)
                self.assertFalse(result.accepted)
                self.assertEqual(result.stdout, stdout)

    def test_size_limit_is_exact_and_oversized_inputs_raise_without_truncation(self):
        stdout = b" " * (MAX_OUTPUT_BYTES - len(VALID)) + VALID
        self.assertTrue(parse_meter_output(stdout, b"", 0).accepted)
        self.assertEqual(len(parse_meter_output(VALID, b"x" * MAX_OUTPUT_BYTES, 0).stderr), MAX_OUTPUT_BYTES)
        for output, error in ((stdout + b"\n", b""), (VALID, b"x" * (MAX_OUTPUT_BYTES + 1))):
            with self.subTest(lengths=(len(output), len(error))), self.assertRaises(ValueError):
                parse_meter_output(output, error, 0)

    def test_invalid_call_types_and_hardware_options_are_rejected(self):
        for stdout, stderr, code in ((VALID.decode(), b"", 0), (bytearray(VALID), b"", 0),
                                     (VALID, "", 0), (VALID, b"", False), (VALID, b"", 0.0)):
            with self.subTest(values=(stdout, stderr, code)), self.assertRaises(TypeError):
                parse_meter_output(stdout, stderr, code)
        for options in ({"timed_out": 1}, {"cancelled": None}, {"port": "COM_TEST"},
                        {"real_mode": True}, {"process": lambda: None}):
            with self.subTest(options=options), self.assertRaises(TypeError):
                parse_meter_output(VALID, b"", 0, **options)


if __name__ == "__main__":
    unittest.main()
