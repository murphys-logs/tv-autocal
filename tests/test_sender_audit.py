"""Authored synthetic fixtures; no received hardware traffic or I/O."""

from dataclasses import FrozenInstanceError
import unittest

from tv_autocal.exlink import ProtocolError, require_fixture_frame, validate_frame
from tv_autocal.sender_audit import AuditStatus, CandidateCommand, SenderAudit
from tv_autocal.simulation import FakeClock


ACK = b"\x03\x0c\xf1"
NACK = b"\x03\x0c\xff"


class SenderAuditTests(unittest.TestCase):
    def make_audit(self, **options):
        clock = FakeClock()
        return SenderAudit(clock, **options), clock

    def test_candidate_bytes_match_literal_plan_and_do_not_extend_old_allowlist(self):
        fixtures = ((CandidateCommand.EXIT, b"\x08\x22\x0d\x00\x00\x2d\x9c"),
                    (CandidateCommand.CONTRAST94, b"\x08\x22\x0b\x02\x00\x5e\x6b"),
                    (CandidateCommand.RESTORE95, b"\x08\x22\x0b\x02\x00\x5f\x6a"))
        for command, frame in fixtures:
            with self.subTest(command=command):
                self.assertEqual(command.value, frame)
                self.assertEqual(sum(frame) % 256, 0)
                validate_frame(frame)
                with self.assertRaises(ProtocolError):
                    require_fixture_frame(frame)
                audit, _ = self.make_audit()
                audit.submit(command)
                self.assertEqual(audit.events[-1].data, frame)

    def test_every_split_ack_is_provisional_until_close(self):
        for split in range(4):
            with self.subTest(split=split):
                audit, clock = self.make_audit()
                self.assertIs(audit.clock, clock)
                self.assertIsNone(audit.command)
                self.assertIsNone(audit.closed_ms)
                audit.submit(CandidateCommand.EXIT)
                self.assertIs(audit.command, CandidateCommand.EXIT)
                clock.advance(1999)
                audit.feed(ACK[:split])
                audit.feed(ACK[split:])
                self.assertEqual(audit.status, AuditStatus.ACK)
                self.assertFalse(audit.accepted)
                audit.close()
                self.assertTrue(audit.accepted)
                self.assertTrue(audit.log_complete)
                self.assertEqual(audit.closed_ms, 1999)
                self.assertEqual(audit.events[-1].kind, "close")

    def test_late_bytes_after_ack_are_retained_and_invalidate_success(self):
        audit, clock = self.make_audit()
        audit.submit(CandidateCommand.EXIT)
        audit.feed(ACK)
        clock.advance(2500)
        audit.feed(NACK)
        audit.feed(b"noise")
        audit.close()
        self.assertEqual(audit.status, AuditStatus.UNKNOWN)
        self.assertFalse(audit.accepted)
        self.assertEqual([e.data for e in audit.events if e.kind == "receive"], [ACK, NACK, b"noise"])
        self.assertEqual(audit.events[-1].timestamp_ms, 2500)

    def test_nack_and_noise_stop_but_keep_receiving_until_close(self):
        for data, expected in ((NACK, AuditStatus.NACK), (b"noise", AuditStatus.UNKNOWN)):
            with self.subTest(data=data):
                audit, _ = self.make_audit()
                audit.submit(CandidateCommand.CONTRAST94)
                audit.feed(data)
                audit.feed(ACK)
                self.assertEqual(audit.status, expected)
                audit.close()
                self.assertEqual([e.data for e in audit.events if e.kind == "receive"], [data, ACK])
                self.assertFalse(audit.accepted)

    def test_duplicate_and_partial_trailing_replies_fail(self):
        for data in (ACK + ACK, ACK + NACK, ACK + b"\x03", ACK + b"bad"):
            with self.subTest(data=data):
                audit, _ = self.make_audit()
                audit.submit(CandidateCommand.EXIT)
                audit.feed(data)
                self.assertEqual(audit.status, AuditStatus.UNKNOWN)
                audit.close()
                self.assertFalse(audit.accepted)
                self.assertIn(data, [e.data for e in audit.events])

    def test_partial_write_records_request_and_count_without_retry(self):
        for accepted in range(7):
            with self.subTest(accepted=accepted):
                audit, _ = self.make_audit()
                audit.submit(CandidateCommand.CONTRAST94, accepted)
                self.assertEqual(audit.status, AuditStatus.UNKNOWN)
                self.assertEqual(audit.events[1].data, CandidateCommand.CONTRAST94.value)
                self.assertIn("accepted " + str(accepted), audit.events[1].detail)
                audit.feed(ACK)
                with self.assertRaises(RuntimeError):
                    audit.submit(CandidateCommand.RESTORE95)
                audit.close()
                self.assertFalse(audit.accepted)

    def test_exact_deadline_and_later_reply_cannot_revive_success(self):
        for when in (2000, 2001):
            with self.subTest(when=when):
                audit, clock = self.make_audit()
                audit.submit(CandidateCommand.EXIT)
                clock.advance(when)
                audit.feed(ACK)
                self.assertEqual(audit.status, AuditStatus.UNKNOWN)
                audit.close()
                self.assertIn(ACK, [e.data for e in audit.events])
                self.assertFalse(audit.accepted)

    def test_silence_or_incomplete_reply_cannot_pass_on_close(self):
        for data in (b"", b"\x03", b"\x03\x0c"):
            with self.subTest(data=data):
                audit, _ = self.make_audit()
                audit.submit(CandidateCommand.EXIT)
                audit.feed(data)
                audit.close()
                self.assertEqual(audit.status, AuditStatus.UNKNOWN)
                self.assertFalse(audit.accepted)

    def test_poll_only_observes_time_and_stops_without_a_reply(self):
        audit, clock = self.make_audit()
        audit.submit(CandidateCommand.EXIT)
        clock.advance(1999)
        self.assertEqual(audit.poll(), AuditStatus.PENDING)
        self.assertEqual(clock.milliseconds, 1999)
        clock.advance(1)
        self.assertEqual(audit.poll(), AuditStatus.UNKNOWN)
        events = audit.events
        audit.poll()
        self.assertEqual(audit.events, events)

    def test_cancel_keeps_all_supplied_data_and_never_restores_or_retries(self):
        for stage in ("new", "pending", "ack"):
            with self.subTest(stage=stage):
                audit, _ = self.make_audit()
                if stage != "new":
                    audit.submit(CandidateCommand.EXIT)
                if stage == "ack":
                    audit.feed(ACK)
                audit.cancel()
                before = audit.events
                audit.cancel()
                self.assertEqual(audit.events, before)
                audit.feed(NACK)
                self.assertEqual(audit.status, AuditStatus.CANCELLED)
                audit.close()
                self.assertEqual(len([e for e in audit.events if e.kind == "write"]), int(stage != "new"))
                self.assertFalse(audit.accepted)

    def test_unsolicited_input_prevents_any_submission(self):
        audit, _ = self.make_audit()
        audit.feed(ACK)
        with self.assertRaises(RuntimeError):
            audit.submit(CandidateCommand.EXIT)
        audit.close()
        self.assertEqual([e.kind for e in audit.events], ["open", "receive", "status", "close"])

    def test_close_is_idempotent_and_rejects_later_data_or_commands(self):
        audit, _ = self.make_audit()
        audit.submit(CandidateCommand.EXIT)
        audit.feed(ACK)
        audit.close()
        before = audit.events
        audit.close()
        self.assertEqual(audit.events, before)
        for action in (lambda: audit.feed(ACK), lambda: audit.submit(CandidateCommand.EXIT), audit.cancel):
            with self.assertRaises(RuntimeError):
                action()
        self.assertEqual(audit.events, before)

    def test_byte_overflow_retains_prefix_marks_gap_and_preserves_close_marker(self):
        audit, _ = self.make_audit(max_bytes=10)
        audit.submit(CandidateCommand.EXIT)
        audit.feed(ACK + NACK)
        audit.feed(b"extra")
        audit.close()
        self.assertFalse(audit.log_complete)
        self.assertFalse(audit.accepted)
        self.assertEqual(audit.status, AuditStatus.UNKNOWN)
        self.assertEqual(audit.dropped_bytes, 8)
        self.assertEqual(sum(len(e.data) for e in audit.events), 10)
        self.assertEqual(audit.events[-2].kind, "overflow")
        self.assertEqual(audit.events[-2].data, ACK)
        self.assertEqual(audit.events[-1].kind, "close")

    def test_event_overflow_is_explicit_and_bounded_even_with_more_input(self):
        audit, _ = self.make_audit(max_events=4)
        audit.submit(CandidateCommand.EXIT)
        audit.feed(ACK)
        audit.feed(NACK)
        audit.cancel()
        audit.close()
        self.assertEqual(len(audit.events), 4)
        self.assertEqual([e.kind for e in audit.events], ["open", "write", "overflow", "close"])
        self.assertEqual(audit.dropped_bytes, 3)
        self.assertFalse(audit.log_complete)
        self.assertFalse(audit.accepted)

    def test_status_event_overflow_rejects_even_when_every_byte_is_retained(self):
        audit, _ = self.make_audit(max_events=5)
        audit.submit(CandidateCommand.EXIT)
        audit.feed(ACK)
        audit.close()
        self.assertEqual([e.kind for e in audit.events],
                         ["open", "write", "receive", "overflow", "close"])
        self.assertEqual(audit.events[1].data, CandidateCommand.EXIT.value)
        self.assertEqual(audit.events[2].data, ACK)
        self.assertIn("recording status", audit.events[3].detail)
        self.assertEqual(audit.events[3].data, b"")
        self.assertEqual(audit.dropped_bytes, 0)
        self.assertFalse(audit.log_complete)
        self.assertEqual(audit.status, AuditStatus.UNKNOWN)
        self.assertFalse(audit.accepted)

    def test_invalid_inputs_fail_before_mutation_and_hardware_options_are_absent(self):
        audit, _ = self.make_audit()
        before = audit.events
        for command in (b"raw", "EXIT", 1, True, None):
            with self.assertRaises(TypeError):
                audit.submit(command)
        for value in (-1, 8, True, 1.0, "7"):
            with self.assertRaises(ValueError):
                audit.submit(CandidateCommand.EXIT, value)
        for data in (bytearray(ACK), "ACK", 1, None):
            with self.assertRaises(TypeError):
                audit.feed(data)
        self.assertEqual(audit.events, before)
        self.assertEqual(audit.status, AuditStatus.NEW)
        for options in ({"port": "COM_TEST"}, {"real_mode": True}, {"transport": lambda: None}):
            with self.assertRaises(TypeError):
                SenderAudit(FakeClock(), **options)

    def test_constructor_bounds_and_snapshots_are_immutable(self):
        for name, values in (("deadline_ms", (0, 3_600_001, True)),
                             ("max_bytes", (6, 65_537, False)),
                             ("max_events", (3, 1025, 4.0))):
            for value in values:
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.make_audit(**{name: value})
        class OtherClock(FakeClock):
            pass
        for clock in (OtherClock(), lambda: 0, None):
            with self.assertRaises(TypeError):
                SenderAudit(clock)
        audit, _ = self.make_audit()
        snapshot = audit.events
        self.assertIsInstance(snapshot, tuple)
        with self.assertRaises(FrozenInstanceError):
            snapshot[0].kind = "changed"
        self.assertTrue(snapshot[0].simulated)
        audit.submit(CandidateCommand.EXIT)
        self.assertEqual(len(snapshot), 1)


if __name__ == "__main__":
    unittest.main()
