"""Integration with authored bytes/observations only; no real adapters."""

from dataclasses import FrozenInstanceError
import unittest

from tv_autocal.integration import IntegrationState, MenuObservation, OfflineMeasurement
from tv_autocal.meter_output import MAX_OUTPUT_BYTES
from tv_autocal.presentation import DisplayTarget, ManualPresenter
from tv_autocal.sender_audit import CandidateCommand, SenderAudit
from tv_autocal.simulation import FakeClock


# Authored source-format fixture, not a captured measurement or optical model.
XYZ = b" Result is XYZ: 10.000000 20.000000 30.000000, D50 Lab: 50.000000 1.000000 -2.000000\n"
YXY = b" Result is XYZ: 10.000000 20.000000 30.000000, Yxy: 20.000000 0.166667 0.333333\n"
ACK = b"\x03\x0c\xf1"
NACK = b"\x03\x0c\xff"


class IntegrationTests(unittest.TestCase):
    def presenter(self, patches=((128, 128, 128), (51, 51, 51))):
        clock = FakeClock()
        presenter = ManualPresenter(clock, (DisplayTarget("fixture-screen"),), patches)
        presenter.select("fixture-screen")
        presenter.confirm("fixture-screen")
        presenter.advance()
        return clock, presenter

    def command(self, clock, candidate=CandidateCommand.CONTRAST94, reply=ACK, close=True):
        audit = SenderAudit(clock)
        audit.submit(candidate)
        audit.feed(reply)
        if close:
            audit.close()
        return audit

    def complete(self, attempt, clock, stdout=XYZ):
        clock.advance(2000)
        self.assertEqual(attempt.poll(), IntegrationState.READING)
        return attempt.finish(stdout, b"", 0)

    def test_manual_patch_only_read_and_repeat_need_no_tv_command(self):
        clock, presenter = self.presenter()
        observation = MenuObservation(0, 0, True)
        records = []
        for index in range(3):
            if index == 1:
                presenter.advance()
            attempt = OfflineMeasurement(clock, presenter)
            attempt.begin(observation)
            clock.advance(1999)
            self.assertEqual(attempt.poll(), IntegrationState.WAITING)
            clock.advance(1)
            self.assertEqual(attempt.poll(), IntegrationState.READING)
            records.append(attempt.finish(XYZ, b"", 0))
        self.assertEqual([r.presentation.sequence for r in records], [1, 2, 2])
        self.assertEqual([r.read_started_ms for r in records], [2000, 4000, 6000])
        self.assertEqual(len(presenter.receipts), 2)
        self.assertTrue(all(r.accepted and r.simulated for r in records))
        self.assertTrue(all(r.command is None and r.command_events == () for r in records))
        self.assertTrue(all(r.meter.stdout == XYZ and r.meter.xyz == (10, 20, 30) for r in records))
        self.assertFalse(presenter.closed)

    def test_baseline_change_restore_links_independent_observations_and_audits(self):
        clock, presenter = self.presenter(((128, 128, 128),))
        baseline = OfflineMeasurement(clock, presenter)
        baseline.begin(MenuObservation(0, 0, True, 95))
        first = self.complete(baseline, clock)
        records = [first]
        for command, level in ((CandidateCommand.CONTRAST94, 94), (CandidateCommand.RESTORE95, 95)):
            audit = self.command(clock, command)
            observation = MenuObservation(clock.milliseconds, clock.milliseconds, True, level)
            attempt = OfflineMeasurement(clock, presenter)
            attempt.begin(observation, command=audit)
            record = self.complete(attempt, clock, YXY)
            self.assertTrue(record.command_accepted)
            self.assertEqual(record.command_events, audit.events)
            self.assertEqual(record.command_closed_ms, observation.inspected_ms)
            self.assertEqual(record.meter.output_format, "Yxy")
            records.append(record)
        self.assertEqual([r.observation.observed_level for r in records], [95, 94, 95])
        self.assertEqual([r.presentation.sequence for r in records], [1, 1, 1])
        self.assertTrue(all(r.meter.xyz == (10, 20, 30) for r in records))
        # Identical literals deliberately establish no predicted optical effect.
        with self.assertRaises(FrozenInstanceError):
            records[-1].accepted = False

    def test_provisional_ack_nack_and_duplicate_cannot_enable_a_read(self):
        for case in ("unclosed", "nack", "duplicate"):
            with self.subTest(case=case):
                clock, presenter = self.presenter()
                audit = self.command(clock, reply=NACK if case == "nack" else ACK, close=False)
                if case == "duplicate":
                    audit.feed(ACK)
                if case != "unclosed":
                    audit.close()
                attempt = OfflineMeasurement(clock, presenter)
                attempt.begin(MenuObservation(0, 0, True, 94), command=audit)
                self.assertEqual(attempt.state, IntegrationState.STOPPED)
                self.assertIsNone(attempt.record.read_started_ms)
                self.assertEqual(attempt.record.command_events, audit.events)
                self.assertTrue(presenter.closed)

    def test_ack_does_not_substitute_for_setting_observation(self):
        for level in (None, 95):
            with self.subTest(level=level):
                clock, presenter = self.presenter()
                attempt = OfflineMeasurement(clock, presenter)
                attempt.begin(MenuObservation(0, 0, True, level), command=self.command(clock))
                self.assertEqual(attempt.state, IntegrationState.STOPPED)
                self.assertIn("independently observed", attempt.record.reason)

    def test_stale_command_observation_and_unconfirmed_future_exit_stop(self):
        for case in ("stale", "unconfirmed", "future"):
            with self.subTest(case=case):
                clock, presenter = self.presenter()
                clock.advance(1)
                audit = self.command(clock)
                observation = MenuObservation(0, 0, True, 94) if case == "stale" else MenuObservation(
                    1, 2 if case == "future" else 1, case != "unconfirmed", 94)
                attempt = OfflineMeasurement(clock, presenter)
                attempt.begin(observation, command=audit)
                self.assertEqual(attempt.state, IntegrationState.STOPPED)
                self.assertIsNone(attempt.record.meter)
                self.assertEqual(attempt.record.command, CandidateCommand.CONTRAST94)
                self.assertEqual(attempt.record.command_events, audit.events)

    def test_wait_starts_at_begin_after_both_receipt_and_exit(self):
        clock, presenter = self.presenter()
        clock.advance(100)
        presenter.advance()
        clock.advance(400)
        attempt = OfflineMeasurement(clock, presenter)
        attempt.begin(MenuObservation(200, 400, True))
        clock.advance(1999)
        self.assertEqual(attempt.poll(), IntegrationState.WAITING)
        clock.advance(1)
        self.assertEqual(attempt.poll(), IntegrationState.READING)
        record = attempt.finish(XYZ, b"", 0)
        self.assertEqual((record.presentation.presented_ms, record.started_ms, record.read_started_ms),
                         (100, 500, 2500))

    def test_held_frame_cannot_advance_or_be_shared_by_competing_attempt(self):
        clock, presenter = self.presenter()
        first, second = OfflineMeasurement(clock, presenter), OfflineMeasurement(clock, presenter)
        first.begin(MenuObservation(0, 0, True))
        with self.assertRaises(RuntimeError):
            presenter.advance()
        with self.assertRaises(RuntimeError):
            second.begin(MenuObservation(0, 0, True))
        self.assertEqual(second.state, IntegrationState.NEW)
        self.assertIsNone(second.record)
        self.assertTrue(self.complete(first, clock).accepted)

    def test_lost_frame_or_hold_stops_without_any_read(self):
        for close in (True, False):
            with self.subTest(close=close):
                clock, presenter = self.presenter()
                attempt = OfflineMeasurement(clock, presenter)
                attempt.begin(MenuObservation(0, 0, True))
                if close:
                    presenter.close()
                else:
                    presenter.release(1, presenter.held_token)
                    presenter.advance()
                clock.advance(2000)
                self.assertEqual(attempt.poll(), IntegrationState.STOPPED)
                self.assertIsNone(attempt.record.read_started_ms)
                self.assertEqual(presenter.frame is None, close)

    def test_reacquired_same_frame_cannot_be_consumed_or_closed_by_old_attempt(self):
        for action in ("poll", "cancel", "finish"):
            with self.subTest(action=action):
                clock, presenter = self.presenter()
                first = OfflineMeasurement(clock, presenter)
                first.begin(MenuObservation(0, 0, True))
                clock.advance(2000)
                first.poll()
                presenter.release(1, presenter.held_token)
                second = OfflineMeasurement(clock, presenter)
                second.begin(MenuObservation(0, 0, True))
                new_token = presenter.held_token
                if action == "finish":
                    first.finish(XYZ, b"", 0)
                else:
                    getattr(first, action)()
                self.assertEqual(first.state, IntegrationState.STOPPED)
                self.assertEqual(presenter.held_token, new_token)
                self.assertFalse(presenter.closed)
                self.assertTrue(self.complete(second, clock).accepted)

    def test_frame_closed_during_read_rejects_but_retains_transcript(self):
        clock, presenter = self.presenter()
        attempt = OfflineMeasurement(clock, presenter)
        attempt.begin(MenuObservation(0, 0, True))
        clock.advance(2000)
        attempt.poll()
        presenter.close()
        record = attempt.finish(XYZ, b"", 0)
        self.assertFalse(record.accepted)
        self.assertEqual(record.meter.stdout, XYZ)

    def test_exact_deadline_rejects_complete_transcript_just_before_accepts(self):
        for elapsed in (9, 10, 11):
            with self.subTest(elapsed=elapsed):
                clock, presenter = self.presenter()
                attempt = OfflineMeasurement(clock, presenter, read_timeout_ms=10)
                attempt.begin(MenuObservation(0, 0, True))
                clock.advance(2000)
                attempt.poll()
                clock.advance(elapsed)
                record = attempt.finish(XYZ, b"", 0)
                self.assertEqual(record.accepted, elapsed < 10)
                self.assertEqual(record.read_deadline_ms, 2010)
                self.assertEqual(record.meter.stdout, XYZ)

    def test_timeout_poll_and_cancel_are_terminal_without_automatic_restoration(self):
        for case in ("new", "wait", "read", "timeout"):
            with self.subTest(case=case):
                clock, presenter = self.presenter()
                attempt = OfflineMeasurement(clock, presenter, read_timeout_ms=10)
                if case != "new":
                    attempt.begin(MenuObservation(0, 0, True))
                if case in ("read", "timeout"):
                    clock.advance(2000)
                    attempt.poll()
                if case == "timeout":
                    clock.advance(10)
                    attempt.poll()
                else:
                    attempt.cancel()
                self.assertEqual(attempt.state, IntegrationState.STOPPED)
                record = attempt.record
                attempt.cancel()
                clock.advance(100000)
                attempt.poll()
                self.assertIs(attempt.record, record)
                with self.assertRaises(RuntimeError):
                    attempt.finish(XYZ, b"", 0)
                with self.assertRaises(RuntimeError):
                    attempt.begin(MenuObservation(0, 0, True))
                if case != "new":
                    self.assertTrue(presenter.closed)

    def test_meter_failure_retains_evidence_and_releases_no_next_patch(self):
        for stdout, stderr, code in ((XYZ, b"error\n", 0), (XYZ, b"", 1), (b"bad\n", b"", 0)):
            with self.subTest(code=code, stderr=stderr):
                clock, presenter = self.presenter()
                attempt = OfflineMeasurement(clock, presenter)
                attempt.begin(MenuObservation(0, 0, True))
                clock.advance(2000)
                attempt.poll()
                record = attempt.finish(stdout, stderr, code)
                self.assertFalse(record.accepted)
                self.assertEqual((record.meter.stdout, record.meter.stderr, record.meter.exit_code),
                                 (stdout, stderr, code))
                self.assertTrue(presenter.closed)
                self.assertEqual(len(presenter.receipts), 1)

    def test_invalid_transcript_input_does_not_consume_the_attempt(self):
        clock, presenter = self.presenter()
        attempt = OfflineMeasurement(clock, presenter)
        attempt.begin(MenuObservation(0, 0, True))
        with self.assertRaises(RuntimeError):
            attempt.finish(XYZ, b"", 0)
        clock.advance(2000)
        attempt.poll()
        for output in ("not bytes", b"x" * (MAX_OUTPUT_BYTES + 1)):
            with self.subTest(output_type=type(output)), self.assertRaises((TypeError, ValueError)):
                attempt.finish(output, b"", 0)
            self.assertEqual(attempt.state, IntegrationState.READING)
            self.assertIsNone(attempt.record)
            self.assertEqual(presenter.held_sequence, 1)
        self.assertTrue(attempt.finish(XYZ, b"", 0).accepted)

    def test_concrete_fixtures_same_clock_and_valid_observations_required(self):
        clock, presenter = self.presenter()
        for kwargs in ({"port": "COM_TEST"}, {"real_mode": True}, {"wait_ms": True}, {"read_timeout_ms": 0}):
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                OfflineMeasurement(clock, presenter, **kwargs)
        with self.assertRaises(ValueError):
            OfflineMeasurement(FakeClock(), presenter)
        attempt = OfflineMeasurement(clock, presenter)
        for observation, command in ((object(), None), (MenuObservation(0, 0, True), object()),
                                     (MenuObservation(0, 0, True), SenderAudit(FakeClock()))):
            with self.subTest(observation=observation), self.assertRaises((TypeError, ValueError)):
                attempt.begin(observation, command=command)
            self.assertIsNone(presenter.held_sequence)
            self.assertEqual(attempt.state, IntegrationState.NEW)
        for args in ((True, 0, True), (2, 1, True), (0, 0, 1), (0, 0, True, False)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                MenuObservation(*args)


if __name__ == "__main__":
    unittest.main()
