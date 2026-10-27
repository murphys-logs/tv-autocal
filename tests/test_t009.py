"""Hardware-free tests: literal external expectations plus synthetic failures."""

import ast
from contextlib import ExitStack
import io
import os
from pathlib import Path
import socket
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tv_autocal import exlink, simulation
from tv_autocal.exlink import ProtocolError, Reply, ReplyParser, encode, validate_frame
from tv_autocal.simulation import FakeClock, FakeSession, Outcome, ScriptedReply


# Literal fixtures independently transcribed from S-005 and pinned S-007.
# Never build expected positive frames with the encoder under test.
POWER_OFF = bytes.fromhex("08 22 00 00 00 01 D5")
POWER_ON = bytes.fromhex("08 22 00 00 00 02 D4")
VOLUME_25 = bytes.fromhex("08 22 01 00 00 19 BC")
BAD_PUBLISHED_POWER_ON = bytes.fromhex("08 22 00 00 00 02 D6")
PERMUTED_VOLUME = bytes.fromhex("08 22 00 01 00 19 BC")
ACK = bytes.fromhex("03 0C F1")
NACK = bytes.fromhex("03 0C FF")
# Derived from S-007 const.py's Key command triple and KEY_FACTORY value.
# Checksum 8E calculated independently; retained only as a rejection fixture.
KEY_FACTORY = bytes.fromhex("08 22 0D 00 00 3B 8E")
# Derived from S-006 p.5 Factory-SVB / Expert-N/D Adj command/value rows.
FACTORY_SVB = (
    bytes.fromhex("08 22 0B 0D 00 00 BE"),
    bytes.fromhex("08 22 0B 0D 00 01 BD"),
    bytes.fromhex("08 22 0B 0D 00 02 BC"),
)


class EncoderTests(unittest.TestCase):
    def test_published_power_off(self):
        self.assertEqual(encode(0, 0, 0, 1), POWER_OFF)

    def test_published_power_on(self):
        self.assertEqual(encode(0, 0, 0, 2), POWER_ON)

    def test_published_volume_25(self):
        self.assertEqual(encode(1, 0, 0, 25), VOLUME_25)

    def test_source_checksum_discrepancy_is_rejected(self):
        with self.assertRaises(ProtocolError):
            validate_frame(BAD_PUBLISHED_POWER_ON)

    def test_every_single_byte_corruption_is_rejected(self):
        for fixture in (POWER_OFF, POWER_ON, VOLUME_25):
            for index in range(7):
                for replacement in range(256):
                    if replacement != fixture[index]:
                        corrupted = fixture[:index] + bytes((replacement,)) + fixture[index + 1:]
                        with self.assertRaises(ProtocolError):
                            validate_frame(corrupted)

    def test_wrong_lengths_headers_and_types(self):
        for value in (b"", POWER_OFF[:-1], POWER_OFF + b"\x00", b"\x22\x08" + POWER_OFF[2:]):
            with self.assertRaises(ProtocolError):
                validate_frame(value)
        for value in (bytearray(POWER_OFF), list(POWER_OFF), POWER_OFF.hex(), None):
            with self.assertRaises(TypeError):
                validate_frame(value)

    def test_bad_input_fields_and_missing_field_never_write(self):
        for field in range(4):
            for invalid in (-1, 256, True, False, 1.0, "1", None):
                values = [0, 0, 0, 1]
                values[field] = invalid
                session = FakeSession(FakeClock())
                with self.assertRaises((TypeError, ProtocolError)):
                    session.submit(*values)
                self.assertEqual(session.writes, ())
                self.assertFalse(session.evidence.encoded)
        with self.assertRaises(TypeError):
            encode(0, 0, 1)

    def test_unsupported_values_do_not_wrap_or_expand_allowlist(self):
        for command in ((0, 0, 0, 0), (0, 0, 0, 3), (1, 0, 0, 24), (1, 0, 0, 26)):
            session = FakeSession(FakeClock())
            with self.assertRaises(ProtocolError):
                session.submit(*command)
            self.assertEqual(session.writes, ())

    def test_checksum_preserving_permutation_has_no_command_permission(self):
        self.assertEqual(validate_frame(PERMUTED_VOLUME), (0, 1, 0, 25))
        session = FakeSession(FakeClock())
        with self.assertRaises(ProtocolError):
            session.submit_frame(PERMUTED_VOLUME)
        self.assertEqual(session.writes, ())

    def test_factory_key_is_rejected_with_valid_checksum(self):
        self.assertEqual(validate_frame(KEY_FACTORY), (13, 0, 0, 59))
        session = FakeSession(FakeClock())
        with self.assertRaises(ProtocolError):
            session.submit_frame(KEY_FACTORY)
        with self.assertRaises(ProtocolError):
            session.submit(13, 0, 0, 59)
        self.assertEqual(session.writes, ())

    def test_nonfixture_command_families_are_rejected(self):
        # Synthetic negative cases, not asserted meanings for these commands.
        # Every possible cmd1 outside power/volume is excluded regardless of value.
        for cmd1 in range(2, 256):
            for value in range(256):
                with self.assertRaises(ProtocolError):
                    encode(cmd1, 0, 0, value)

    def test_factory_svb_all_documented_values_rejected(self):
        for value, frame in enumerate(FACTORY_SVB):
            self.assertEqual(validate_frame(frame), (11, 13, 0, value))
            session = FakeSession(FakeClock())
            with self.assertRaises(ProtocolError):
                session.submit_frame(frame)
            with self.assertRaises(ProtocolError):
                session.submit(11, 13, 0, value)
            self.assertEqual(session.writes, ())


class ParserTests(unittest.TestCase):
    def test_ack_and_nack_whole(self):
        self.assertEqual(ReplyParser().feed(ACK), (Reply.ACK,))
        self.assertEqual(ReplyParser().feed(NACK), (Reply.NACK,))

    def test_every_split_boundary(self):
        for message, expected in ((ACK, Reply.ACK), (NACK, Reply.NACK)):
            for split in range(4):
                parser = ReplyParser()
                result = parser.feed(message[:split]) + parser.feed(message[split:])
                self.assertEqual(result, (expected,))
                parser.finish()

    def test_byte_by_byte_and_bounded_incomplete_buffer(self):
        parser = ReplyParser()
        replies = ()
        for value in ACK + NACK:
            replies += parser.feed(bytes((value,)))
            self.assertLessEqual(parser.buffered_bytes, 2)
        self.assertEqual(replies, (Reply.ACK, Reply.NACK))

    def test_concatenated_replies_in_standalone_parser(self):
        self.assertEqual(ReplyParser().feed(ACK + NACK + ACK), (Reply.ACK, Reply.NACK, Reply.ACK))

    def test_noise_reversed_header_unknown_status_and_queries_fail(self):
        for data in (b"\x00" + ACK, b"\x0c\x03\xf1", b"\x03\x0c\x00", b"\x03\x0c\xf5", ACK + b"x"):
            parser = ReplyParser()
            with self.assertRaises(ProtocolError):
                parser.feed(data)
            self.assertEqual(parser.buffered_bytes, 0)
            with self.assertRaises(ProtocolError):
                parser.feed(ACK)

    def test_partial_replies_remain_incomplete_and_finish_fails(self):
        for data in (ACK[:1], ACK[:2]):
            parser = ReplyParser()
            self.assertEqual(parser.feed(data), ())
            with self.assertRaises(ProtocolError):
                parser.finish()

    def test_oversized_and_nonbytes_chunks_fail(self):
        for data in (ACK * 33, "030cf1", bytearray(ACK), None):
            parser = ReplyParser()
            with self.assertRaises(ProtocolError):
                parser.feed(data)
            self.assertEqual(parser.buffered_bytes, 0)


class SessionTests(unittest.TestCase):
    def started(self, replies=(), **kwargs):
        clock = FakeClock()
        session = FakeSession(clock, replies, **kwargs)
        session.submit_frame(POWER_OFF)
        return clock, session

    def assert_no_second_request(self, session):
        with self.assertRaises(RuntimeError):
            session.submit_frame(POWER_ON)
        self.assertEqual(len(session.writes), 1)

    def test_ack_has_separate_evidence_and_retires(self):
        clock, session = self.started((ScriptedReply(10, ACK),))
        self.assertTrue(session.evidence.encoded)
        self.assertTrue(session.evidence.fake_write_accepted)
        self.assertEqual(session.evidence.outcome, Outcome.WAITING)
        clock.advance(10)
        evidence = session.poll()
        self.assertEqual(evidence.outcome, Outcome.ACK)
        self.assertTrue(evidence.simulated)
        self.assertTrue(session.retired)
        self.assertNotIn("tv_setting_verified", evidence.__dataclass_fields__)
        self.assertNotIn("calibration_improved", evidence.__dataclass_fields__)
        self.assert_no_second_request(session)

    def test_nack_retires(self):
        clock, session = self.started((ScriptedReply(0, NACK),))
        self.assertEqual(session.poll().outcome, Outcome.NACK)
        self.assertTrue(session.retired)
        self.assert_no_second_request(session)

    def test_no_reply_timeout_boundary(self):
        clock, session = self.started()
        clock.advance(1999)
        self.assertEqual(session.poll().outcome, Outcome.WAITING)
        clock.advance(1)
        self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)
        self.assertIn("timeout", session.evidence.reason)
        self.assert_no_second_request(session)

    def test_partial_reply_times_out(self):
        clock, session = self.started((ScriptedReply(10, ACK[:2]),))
        clock.advance(10)
        self.assertEqual(session.poll().outcome, Outcome.WAITING)
        clock.advance(1990)
        self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)

    def test_reply_just_before_deadline_succeeds_even_if_polled_later(self):
        clock, session = self.started((ScriptedReply(1999, ACK),))
        clock.advance(2100)
        self.assertEqual(session.poll().outcome, Outcome.ACK)

    def test_reply_at_or_after_deadline_is_unknown(self):
        for arrival in (2000, 2001, 3000):
            clock, session = self.started((ScriptedReply(arrival, ACK),))
            clock.advance(arrival)
            self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)
            self.assert_no_second_request(session)

    def test_split_reply_crossing_deadline_is_not_accepted(self):
        clock, session = self.started((ScriptedReply(1999, ACK[:2]), ScriptedReply(2000, ACK[2:])))
        clock.advance(2000)
        self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)

    def test_partial_fake_write_is_terminal_without_retry(self):
        for accepted in range(7):
            clock, session = self.started(accepted_bytes=accepted)
            self.assertTrue(session.evidence.encoded)
            self.assertFalse(session.evidence.fake_write_accepted)
            self.assertEqual(session.evidence.outcome, Outcome.UNKNOWN)
            session.receive(ACK)
            self.assertEqual(session.evidence.outcome, Outcome.UNKNOWN)
            self.assert_no_second_request(session)

    def test_cancellation_is_terminal(self):
        clock, session = self.started((ScriptedReply(100, ACK),))
        self.assertEqual(session.cancel().outcome, Outcome.UNKNOWN)
        clock.advance(100)
        self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)
        self.assert_no_second_request(session)

    def test_unsolicited_bytes_retire_before_any_write(self):
        session = FakeSession(FakeClock())
        self.assertEqual(session.receive(ACK).outcome, Outcome.UNKNOWN)
        with self.assertRaises(RuntimeError):
            session.submit_frame(POWER_OFF)
        self.assertEqual(session.writes, ())

    def test_duplicate_or_trailing_bytes_same_delivery_are_unknown(self):
        for reply in (ACK + ACK, ACK + NACK, ACK + ACK[:1]):
            clock, session = self.started((ScriptedReply(0, reply),))
            self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)
            self.assert_no_second_request(session)

    def test_late_and_duplicate_bytes_cannot_complete_a_future_request(self):
        for terminal in (ACK, NACK, b"noise"):
            clock, session = self.started()
            evidence = session.receive(terminal)
            clock.advance(5000)
            self.assertEqual(session.receive(ACK), evidence)
            self.assertEqual(session.poll(), evidence)
            self.assert_no_second_request(session)
        # A fresh independent fake has no inherited scripted bytes or state.
        clock, fresh = self.started()
        clock.advance(2000)
        self.assertEqual(fresh.poll().outcome, Outcome.UNKNOWN)

    def test_pending_request_cannot_be_replaced(self):
        clock, session = self.started()
        self.assert_no_second_request(session)
        self.assertEqual(session.evidence.outcome, Outcome.WAITING)

    def test_scripted_and_direct_delivery_cannot_be_mixed(self):
        clock, session = self.started((ScriptedReply(100, b"noise"),))
        with self.assertRaises(RuntimeError):
            session.receive(ACK)
        clock.advance(100)
        self.assertEqual(session.poll().outcome, Outcome.UNKNOWN)

    def test_bad_frame_never_enters_fake_write_log(self):
        for frame in (BAD_PUBLISHED_POWER_ON, PERMUTED_VOLUME, KEY_FACTORY, b"bad"):
            session = FakeSession(FakeClock())
            with self.assertRaises(ProtocolError):
                session.submit_frame(frame)
            self.assertEqual(session.writes, ())
            self.assertEqual(session.evidence.outcome, Outcome.NEW)

    def test_clock_and_script_validation(self):
        for value in (-1, 1.0, True, "1"):
            with self.assertRaises(ValueError):
                FakeClock().advance(value)
            with self.assertRaises(ValueError):
                ScriptedReply(value, ACK)
        with self.assertRaises(TypeError):
            FakeSession(lambda: 0)
        with self.assertRaises(ValueError):
            FakeSession(FakeClock(), (ScriptedReply(2, ACK), ScriptedReply(1, NACK)))
        for options in ({"deadline_ms": 0}, {"accepted_bytes": 8}):
            with self.assertRaises(ValueError):
                FakeSession(FakeClock(), **options)


class ContainmentTests(unittest.TestCase):
    def test_ports_hosts_transport_and_real_mode_are_rejected(self):
        for options in ({"port": "COM_TEST"}, {"host": "example.invalid"}, {"real_mode": True}, {"transport": object()}):
            with self.assertRaises(TypeError):
                FakeSession(FakeClock(), **options)

    def assert_application_has_no_io(self, root):
        # Include future subpackages without importing or executing their code.
        # Each module has a narrow explicit import policy. Unknown/nested files
        # get only the original harmless baseline, not every new module's imports.
        baseline = {(0, "enum"), (0, "dataclasses")}
        allowed_by_module = {
            "simulation.py": baseline | {(1, "exlink")},
            "cycle.py": baseline | {(0, "math"), (1, "simulation")},
            "presentation.py": baseline | {(0, "hashlib"), (1, "renderer"), (1, "simulation")},
            "meter_output.py": baseline | {(0, "math"), (0, "re")},
            "sender_audit.py": baseline | {(1, "exlink"), (1, "simulation")},
            "integration.py": baseline | {(1, "meter_output"), (1, "presentation"),
                                          (1, "sender_audit"), (1, "simulation")},
            "demo.py": {(0, "dataclasses"), (0, "hashlib"), (0, "json"), (0, "sys"),
                        (1, "cycle"), (1, "renderer"), (1, "simulation")},
        }
        for source in sorted(root.rglob("*.py")):
            allowed = allowed_by_module.get(source.relative_to(root).as_posix(), baseline)
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    self.fail("Unexpected import in " + str(source) + ": " + ast.unparse(node))
                if isinstance(node, ast.ImportFrom):
                    self.assertIn((node.level, node.module), allowed, str(source))
                    if node.module == "sys":
                        self.assertEqual([alias.name for alias in node.names], ["argv"], str(source))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"open", "exec", "eval", "compile", "__import__", "input"}, str(source))

    def test_application_imports_and_calls_have_no_io_capabilities(self):
        self.assert_application_has_no_io(Path(exlink.__file__).parent)

    def test_source_inspection_rejects_io_in_a_nested_package(self):
        # These are inert source fixtures: neither file is imported or executed.
        with TemporaryDirectory(prefix="t009-fixture-") as directory:
            root = Path(directory)
            (root / "__init__.py").write_text("", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            source = nested / "module.py"
            source.write_text("from enum import Enum\n", encoding="utf-8")
            self.assert_application_has_no_io(root)
            source.write_text("import socket\n", encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "Unexpected import .*import socket"):
                self.assert_application_has_no_io(root)

    def test_runtime_guards_fail_on_io_during_all_software_scenarios(self):
        # Guarded execution of every functional test after imports are loaded.
        # Guards supplement the source review; this is not a Python sandbox.
        targets = ("builtins.open", "io.open", "os.open", "os.system", "subprocess.Popen", "socket.socket", "socket.create_connection", "socket.getaddrinfo")
        with ExitStack() as stack:
            for target in targets:
                stack.enter_context(patch(target, side_effect=AssertionError("Unexpected I/O: " + target)))
            if hasattr(os, "startfile"):
                stack.enter_context(patch("os.startfile", side_effect=AssertionError("Unexpected OS launch")))
            suite = unittest.TestSuite(
                unittest.defaultTestLoader.loadTestsFromTestCase(case)
                for case in (EncoderTests, ParserTests, SessionTests)
            )
            expected_count = suite.countTestCases()
            result = unittest.TestResult()
            suite.run(result)
        self.assertEqual(result.testsRun, expected_count)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])


if __name__ == "__main__":
    unittest.main()
