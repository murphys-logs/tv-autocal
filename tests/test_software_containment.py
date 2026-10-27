"""Run every new functional case with file/device/process/network calls guarded."""

from contextlib import ExitStack
import os
import unittest
from unittest.mock import patch

import test_cycle
import test_renderer
import test_renderer_cycle_integration


class SoftwareContainmentTests(unittest.TestCase):
    def test_new_functional_suites_do_not_access_hardware_or_files(self):
        # Imports and static inspection are separate checks. Test fixtures and
        # demo output use memory only. This is not a security sandbox for Python.
        targets = ("builtins.open", "io.open", "os.open", "os.system", "subprocess.Popen",
                   "socket.socket", "socket.create_connection", "socket.getaddrinfo")
        suite = unittest.TestSuite(
            unittest.defaultTestLoader.loadTestsFromTestCase(case)
            for case in (test_renderer.RendererTests, test_cycle.CycleTests,
                         test_renderer_cycle_integration.RendererCycleIntegrationTests)
        )
        expected = suite.countTestCases()
        with ExitStack() as stack:
            for target in targets:
                stack.enter_context(patch(target, side_effect=AssertionError("Unexpected I/O: " + target)))
            if hasattr(os, "startfile"):
                stack.enter_context(patch("os.startfile", side_effect=AssertionError("Unexpected OS launch")))
            result = unittest.TestResult()
            suite.run(result)
        self.assertGreater(expected, 0)
        self.assertEqual(result.testsRun, expected)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(result.skipped, [])


if __name__ == "__main__":
    unittest.main()
