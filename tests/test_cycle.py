"""Software-only cycle tests: literal samples, fake time, no equipment."""

from dataclasses import FrozenInstanceError
import unittest
from unittest.mock import patch

from tv_autocal.cycle import (
    CommandReply, CycleState, MeasurementController, MeterSample,
    Phase, SimulatedMeter, SimulatedTV, TVStep,
)
from tv_autocal.simulation import FakeClock


class CycleTests(unittest.TestCase):
    def make_controller(self, samples=None, steps=(), **options):
        clock = FakeClock()
        tv = SimulatedTV(50, steps)
        meter = SimulatedMeter(samples if samples is not None else (
            MeterSample((20.0, 21.0, 22.0)),
            MeterSample((23.0, 24.0, 25.0)),
            MeterSample((19.0, 21.0, 23.0)),
        ))
        controller = MeasurementController(clock, tv, meter, **options)
        return controller, clock, tv, meter

    def baseline(self, controller, clock):
        controller.start_baseline()
        clock.advance(2000)
        self.assertEqual(controller.poll(), CycleState.READY)

    def test_baseline_change_restore_complete_event_order(self):
        c, clock, tv, meter = self.make_controller()
        c.start_baseline()
        self.assertEqual(c.original_level, 50)
        self.assertEqual(tv.commands, ())
        self.assertEqual([e.action for e in c.events], [
            "begin", "inspect", "capture_original", "exit", "wait",
        ])
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.READY)
        c.measure_change(49)
        self.assertTrue(c.restoration_required)
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.READY)
        c.restore()
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.COMPLETE)
        self.assertEqual(tv.commands, (49, 50))
        self.assertEqual(tv.level, 50)
        self.assertFalse(tv.menu_open)
        self.assertFalse(c.restoration_required)
        self.assertEqual(meter.reads, 3)
        self.assertEqual([r.phase for r in c.records], [Phase.BASELINE, Phase.CHANGE, Phase.RESTORE])
        self.assertEqual([r.xyz for r in c.records], [(20.0, 21.0, 22.0), (23.0, 24.0, 25.0), (19.0, 21.0, 23.0)])
        self.assertEqual([r.read_started_ms for r in c.records], [2000, 4000, 6000])
        self.assertEqual([e.action for e in c.events if e.phase is Phase.CHANGE], [
            "begin", "set", "reply", "inspect", "exit", "wait", "read", "accepted",
        ])

    def test_baseline_inspection_precedes_ground_truth_check_and_original_capture(self):
        c, _, _, _ = self.make_controller()
        original_inspect, original_level = SimulatedTV.inspect, SimulatedTV.level
        accesses = []

        def observe(tv):
            accesses.append("inspect")
            self.assertIsNone(c.original_level)
            return original_inspect(tv)

        def ground_truth(tv):
            accesses.append("ground_truth")
            self.assertIsNone(c.original_level)
            return original_level.fget(tv)

        with patch.object(SimulatedTV, "inspect", observe), patch.object(SimulatedTV, "level", property(ground_truth)):
            c.start_baseline()
        self.assertEqual(accesses, ["inspect", "ground_truth"])
        self.assertEqual(c.original_level, 50)
        self.assertEqual([(e.action, e.detail, e.phase) for e in c.events[1:3]], [
            ("inspect", "50", Phase.BASELINE), ("capture_original", "50", Phase.BASELINE),
        ])

    def test_poll_neither_advances_time_nor_reads_before_wait_boundary(self):
        c, clock, _, meter = self.make_controller()
        c.start_baseline()
        initial_events = c.events
        for _ in range(5):
            self.assertEqual(c.poll(), CycleState.WAITING)
        self.assertEqual(clock.milliseconds, 0)
        self.assertEqual(c.events, initial_events)
        clock.advance(1999)
        self.assertEqual(c.poll(), CycleState.WAITING)
        self.assertEqual(meter.reads, 0)
        clock.advance(1)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual(meter.reads, 1)

    def test_ready_waits_for_explicit_next_action(self):
        c, clock, tv, meter = self.make_controller()
        self.baseline(c, clock)
        records = c.records
        clock.advance(100_000)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual(c.records, records)
        self.assertEqual(tv.commands, ())
        self.assertEqual(meter.reads, 1)

    def test_read_delay_starts_when_read_is_actually_requested(self):
        c, clock, _, meter = self.make_controller((MeterSample((1, 2, 3), after_ms=50),))
        c.start_baseline()
        clock.advance(3000)
        self.assertEqual(c.poll(), CycleState.READING)
        self.assertEqual(meter.reads, 1)
        clock.advance(49)
        self.assertEqual(c.poll(), CycleState.READING)
        clock.advance(1)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual(c.records[0].read_started_ms, 3000)
        self.assertEqual(c.records[0].completed_ms, 3050)

    def test_exact_read_deadline_is_late(self):
        c, clock, _, _ = self.make_controller((MeterSample((1, 2, 3), after_ms=100),), read_timeout_ms=100)
        c.start_baseline()
        clock.advance(2000)
        c.poll()
        clock.advance(99)
        self.assertEqual(c.poll(), CycleState.READING)
        clock.advance(1)
        self.assertEqual(c.poll(), CycleState.STOPPED)
        self.assertFalse(c.records[0].accepted)
        self.assertIn("deadline", c.records[0].reason)
        self.assertEqual(c.records[0].sample_due_ms, 2100)
        self.assertEqual(c.records[0].read_deadline_ms, 2100)

    def test_sample_before_deadline_survives_delayed_poll(self):
        c, clock, _, _ = self.make_controller((MeterSample((1, 2, 3), after_ms=99),), read_timeout_ms=100)
        c.start_baseline()
        clock.advance(2000)
        c.poll()
        clock.advance(1000)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual(c.records[0].xyz, (1, 2, 3))
        record = c.records[0]
        self.assertEqual(record.sample_due_ms, 2099)
        self.assertEqual(record.read_deadline_ms, 2100)
        self.assertEqual(record.completed_ms, 3000)
        self.assertLess(record.sample_due_ms, record.read_deadline_ms)
        self.assertLess(record.read_deadline_ms, record.completed_ms)

    def test_missing_and_nonfinite_measurements_stop_and_retain_raw_input(self):
        for xyz in (None, (1, float("nan"), 2), (float("inf"), 1, 2), (1, 2, float("-inf"))):
            with self.subTest(xyz=xyz):
                c, clock, _, meter = self.make_controller((MeterSample(xyz),))
                c.start_baseline()
                clock.advance(2000)
                self.assertEqual(c.poll(), CycleState.STOPPED)
                self.assertIs(c.records[0].xyz, xyz)
                self.assertFalse(c.records[0].accepted)
                c.poll()
                self.assertEqual(meter.reads, 1)

    def test_finite_zero_and_negative_values_are_diagnostic_not_accuracy_claims(self):
        c, clock, _, _ = self.make_controller((MeterSample((0, -0.001, 0)),))
        self.baseline(c, clock)
        self.assertEqual(c.records[0].xyz, (0, -0.001, 0))
        self.assertTrue(c.records[0].simulated)
        self.assertIn("never calibration", c.records[0].purpose)

    def test_meter_error_keeps_value_and_error(self):
        c, clock, _, _ = self.make_controller((MeterSample((1, 2, 3), error="fixture error"),))
        c.start_baseline()
        clock.advance(2000)
        c.poll()
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertEqual(c.records[0].xyz, (1, 2, 3))
        self.assertIn("fixture error", c.records[0].reason)

    def test_exhausted_script_is_not_an_implicit_measurement(self):
        c, clock, _, meter = self.make_controller(())
        c.start_baseline()
        clock.advance(2000)
        c.poll()
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertIn("script exhausted", c.records[0].reason)
        self.assertEqual(meter.reads, 1)

    def test_failed_baseline_menu_inspection_prevents_exit_wait_and_read(self):
        for step in (TVStep(menu_available=False), TVStep(menu_value=49)):
            with self.subTest(step=step):
                c, clock, _, meter = self.make_controller(steps=(step,))
                c.start_baseline()
                self.assertEqual(c.state, CycleState.STOPPED)
                self.assertEqual(c.records[0].phase, Phase.BASELINE)
                self.assertIsNone(c.original_level)
                self.assertEqual(c.records[0].target_level, step.menu_value)
                self.assertIsNone(c.records[0].read_started_ms)
                self.assertNotIn("capture_original", [e.action for e in c.events])
                self.assertNotIn("exit", [e.action for e in c.events])
                if step.menu_available:
                    self.assertIn("simulator invariant", c.records[0].reason)
                clock.advance(2000)
                c.poll()
                self.assertEqual(meter.reads, 0)

    def test_failed_baseline_exit_prevents_any_read(self):
        c, clock, tv, meter = self.make_controller(steps=(TVStep(exit_confirmed=False),))
        c.start_baseline()
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertTrue(tv.menu_open)
        self.assertFalse(c.restoration_required)
        clock.advance(60_000)
        c.poll()
        self.assertEqual(meter.reads, 0)

    def test_nack_and_unknown_can_change_fake_state_but_never_permit_read(self):
        for reply in (CommandReply.NACK, CommandReply.UNKNOWN):
            with self.subTest(reply=reply):
                c, clock, tv, meter = self.make_controller(steps=(TVStep(), TVStep(reply=reply)))
                self.baseline(c, clock)
                c.measure_change(49)
                self.assertEqual(tv.level, 49)
                self.assertTrue(c.restoration_required)
                self.assertEqual(c.state, CycleState.STOPPED)
                self.assertEqual(c.records[-1].phase, Phase.CHANGE)
                self.assertFalse(c.records[-1].accepted)
                self.assertEqual(meter.reads, 1)
                self.assertNotIn("inspect", [e.action for e in c.events if e.phase is Phase.CHANGE])

    def test_ack_without_change_is_caught_by_menu_observation(self):
        c, clock, tv, meter = self.make_controller(steps=(TVStep(), TVStep(apply=False)))
        self.baseline(c, clock)
        c.measure_change(49)
        self.assertEqual(tv.level, 50)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertIn("menu value", c.records[-1].reason)
        self.assertEqual(meter.reads, 1)

    def test_wrong_menu_observation_blocks_changed_state(self):
        c, clock, tv, _ = self.make_controller(steps=(TVStep(), TVStep(menu_value=48)))
        self.baseline(c, clock)
        c.measure_change(49)
        self.assertEqual(tv.level, 49)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertTrue(c.restoration_required)

    def test_failed_change_exit_stops_without_automatic_restore(self):
        c, clock, tv, meter = self.make_controller(steps=(TVStep(), TVStep(exit_confirmed=False)))
        self.baseline(c, clock)
        c.measure_change(49)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertEqual(tv.commands, (49,))
        self.assertEqual(meter.reads, 1)
        self.assertTrue(c.restoration_required)

    def test_restore_rejection_or_wrong_value_stays_failed(self):
        for bad in (TVStep(reply=CommandReply.UNKNOWN), TVStep(apply=False), TVStep(menu_value=48)):
            with self.subTest(bad=bad):
                c, clock, tv, meter = self.make_controller(steps=(TVStep(), TVStep(), bad))
                self.baseline(c, clock)
                c.measure_change(49)
                clock.advance(2000)
                c.poll()
                c.restore()
                self.assertEqual(c.state, CycleState.STOPPED)
                self.assertTrue(c.restoration_required)
                self.assertFalse(c.records[-1].accepted)
                self.assertEqual(c.records[-1].phase, Phase.RESTORE)
                self.assertEqual(tv.commands, (49, 50))
                self.assertEqual(meter.reads, 2)

    def test_restore_exit_failure_never_claims_completed_restoration(self):
        c, clock, tv, _ = self.make_controller(steps=(TVStep(), TVStep(), TVStep(exit_confirmed=False)))
        self.baseline(c, clock)
        c.measure_change(49)
        clock.advance(2000)
        c.poll()
        c.restore()
        self.assertEqual(tv.level, 50)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertTrue(c.restoration_required)

    def test_restore_bad_measurement_stays_failed_even_with_restored_toy_setting(self):
        c, clock, tv, _ = self.make_controller((MeterSample((1, 2, 3)), MeterSample((4, 5, 6)), MeterSample(None)))
        self.baseline(c, clock)
        c.measure_change(49)
        clock.advance(2000)
        c.poll()
        c.restore()
        clock.advance(2000)
        c.poll()
        self.assertEqual(tv.level, 50)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertTrue(c.restoration_required)

    def test_restore_reuses_baseline_patch_even_when_change_uses_a_different_patch(self):
        c, clock, _, _ = self.make_controller()
        c.start_baseline((13, 26, 51))
        clock.advance(2000)
        c.poll()
        c.measure_change(49, (255, 255, 255))
        clock.advance(2000)
        c.poll()
        c.restore()
        clock.advance(2000)
        c.poll()
        self.assertEqual(c.state, CycleState.COMPLETE)
        self.assertEqual([r.patch_rgb for r in c.records], [
            (13, 26, 51), (255, 255, 255), (13, 26, 51),
        ])

    def test_cancel_during_wait_records_attempt_without_read_or_restore(self):
        c, clock, tv, meter = self.make_controller()
        self.baseline(c, clock)
        c.measure_change(49)
        c.cancel()
        records = c.records
        clock.advance(100_000)
        c.poll()
        self.assertEqual(c.records, records)
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertEqual(tv.commands, (49,))
        self.assertEqual(meter.reads, 1)
        self.assertIsNone(c.records[-1].read_started_ms)
        self.assertIsNone(c.records[-1].sample_due_ms)
        self.assertIsNone(c.records[-1].read_deadline_ms)
        self.assertIn("cancelled", c.records[-1].reason)

    def test_cancel_during_pending_read_does_not_accept_later_sample(self):
        c, clock, _, meter = self.make_controller((MeterSample((1, 2, 3), after_ms=10),))
        c.start_baseline()
        clock.advance(2000)
        c.poll()
        c.cancel()
        clock.advance(20)
        c.poll()
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertEqual(meter.reads, 1)
        self.assertFalse(c.records[0].accepted)
        self.assertIsNone(c.records[0].xyz)
        self.assertEqual(c.records[0].read_started_ms, 2000)

    def test_cancel_before_start_and_after_complete_is_idempotent(self):
        c, _, _, meter = self.make_controller()
        c.cancel()
        original_events = c.events
        c.cancel()
        self.assertEqual(c.events, original_events)
        self.assertEqual(c.records, ())
        self.assertEqual(meter.reads, 0)
        d, clock, _, _ = self.make_controller()
        self.baseline(d, clock)
        d.restore()
        clock.advance(2000)
        d.poll()
        original_events = d.events
        d.cancel()
        self.assertEqual(d.state, CycleState.COMPLETE)
        self.assertEqual(d.events, original_events)

    def test_stopped_controller_rejects_every_continuation(self):
        c, _, tv, meter = self.make_controller()
        c.start_baseline()
        c.cancel()
        for action in (c.start_baseline, lambda: c.measure_change(49), c.repeat, c.restore):
            with self.subTest(action=action), self.assertRaises(RuntimeError):
                action()
        self.assertEqual(tv.commands, ())
        self.assertEqual(meter.reads, 0)

    def test_repeat_requires_fresh_wait_without_reopening_menu(self):
        c, clock, tv, meter = self.make_controller()
        self.baseline(c, clock)
        c.repeat()
        self.assertFalse(tv.menu_open)
        self.assertEqual([e.action for e in c.events if e.phase is Phase.REPEAT], ["begin", "wait"])
        clock.advance(1999)
        self.assertEqual(c.poll(), CycleState.WAITING)
        self.assertEqual(meter.reads, 1)
        clock.advance(1)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual(meter.reads, 2)
        self.assertEqual(tv.commands, ())

    def test_simulator_ground_truth_invariant_rejects_interference_before_repeat(self):
        c, clock, tv, meter = self.make_controller()
        self.baseline(c, clock)
        tv.prepare(None)
        c.repeat()
        self.assertEqual(c.state, CycleState.STOPPED)
        self.assertFalse(c.records[-1].accepted)
        self.assertIn("simulator invariant", c.records[-1].reason)
        self.assertEqual(meter.reads, 1)

    def test_simulator_ground_truth_invariant_rejects_interference_during_wait_or_read(self):
        for reading in (False, True):
            with self.subTest(reading=reading):
                c, clock, tv, meter = self.make_controller((MeterSample((1, 2, 3), after_ms=50),))
                c.start_baseline()
                if reading:
                    clock.advance(2000)
                    c.poll()
                tv.prepare(49)
                clock.advance(50)
                c.poll()
                self.assertEqual(c.state, CycleState.STOPPED)
                self.assertTrue(c.restoration_required)
                self.assertEqual(meter.reads, int(reading))
                self.assertFalse(c.records[-1].accepted)
                self.assertIn("simulator invariant", c.records[-1].reason)

    def test_first_setter_requires_budget_for_change_and_restoration(self):
        for limit, repeats in ((1, 0), (2, 0), (3, 1)):
            with self.subTest(limit=limit, repeats=repeats):
                c, clock, tv, meter = self.make_controller(max_attempts=limit)
                self.baseline(c, clock)
                for _ in range(repeats):
                    c.repeat()
                    clock.advance(2000)
                    c.poll()
                before = (c.events, c.records, tv.commands, tv.level, tv.menu_open, meter.reads)
                with self.assertRaisesRegex(RuntimeError, "reserved.*restoration"):
                    c.measure_change(49)
                self.assertEqual(c.state, CycleState.READY)
                self.assertFalse(c.restoration_required)
                self.assertEqual((c.events, c.records, tv.commands, tv.level, tv.menu_open, meter.reads), before)
                if limit > 1:
                    c.restore()
                    clock.advance(2000)
                    self.assertEqual(c.poll(), CycleState.COMPLETE)
                    self.assertEqual(len(c.records), limit)

    def test_last_attempt_is_reserved_after_change_and_restore_completes(self):
        c, clock, tv, meter = self.make_controller(max_attempts=3)
        self.baseline(c, clock)
        c.measure_change(49)
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.READY)
        before = (c.events, c.records, tv.commands, tv.level, tv.menu_open, meter.reads)
        for action in (c.repeat, lambda: c.measure_change(48)):
            with self.subTest(action=action), self.assertRaisesRegex(RuntimeError, "reserved.*restoration"):
                action()
            self.assertEqual(c.state, CycleState.READY)
            self.assertTrue(c.restoration_required)
            self.assertEqual((c.events, c.records, tv.commands, tv.level, tv.menu_open, meter.reads), before)
        c.restore()
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.COMPLETE)
        self.assertEqual(tv.level, 50)
        self.assertEqual(tv.commands, (49, 50))
        self.assertFalse(c.restoration_required)
        self.assertEqual([r.phase for r in c.records], [Phase.BASELINE, Phase.CHANGE, Phase.RESTORE])
        self.assertEqual(meter.reads, 3)

    def test_repeat_after_change_preserves_target_and_patch_and_allows_restore(self):
        c, clock, tv, meter = self.make_controller((MeterSample((1, 2, 3)),) * 4, max_attempts=4)
        self.baseline(c, clock)
        c.measure_change(49, (13, 26, 51))
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.READY)
        c.repeat()
        clock.advance(1999)
        self.assertEqual(c.poll(), CycleState.WAITING)
        self.assertEqual(meter.reads, 2)
        clock.advance(1)
        self.assertEqual(c.poll(), CycleState.READY)
        self.assertEqual((c.records[-1].phase, c.records[-1].target_level, c.records[-1].patch_rgb),
                         (Phase.REPEAT, 49, (13, 26, 51)))
        self.assertEqual(tv.commands, (49,))
        c.restore()
        clock.advance(2000)
        self.assertEqual(c.poll(), CycleState.COMPLETE)
        self.assertEqual(len(c.records), 4)

    def test_attempt_limit_stop_identifies_refused_phase(self):
        for phase in (Phase.REPEAT, Phase.RESTORE):
            with self.subTest(phase=phase):
                c, clock, tv, meter = self.make_controller(max_attempts=1)
                self.baseline(c, clock)
                (c.repeat if phase is Phase.REPEAT else c.restore)()
                self.assertEqual(c.state, CycleState.STOPPED)
                self.assertEqual((c.events[-1].action, c.events[-1].phase), ("stop", phase))
                self.assertIn("attempt limit", c.events[-1].detail)
                self.assertEqual(len(c.records), 1)
                self.assertEqual(tv.commands, ())
                self.assertEqual(meter.reads, 1)

    def test_invalid_rgb_and_target_rejected_before_mutation(self):
        invalid_rgb = ([], (0, 0), (0, 0, 256), (False, 0, 0), (0.5, 0, 0))
        for rgb in invalid_rgb:
            with self.subTest(rgb=rgb):
                c, _, tv, _ = self.make_controller()
                with self.assertRaises(ValueError):
                    c.start_baseline(rgb)
                self.assertEqual(c.state, CycleState.NEW)
                self.assertIsNone(c.original_level)
                self.assertEqual(c.events, ())
                self.assertFalse(tv.menu_open)
        for value in (-1, 101, True, 1.5, "49"):
            with self.subTest(value=value):
                c, clock, tv, _ = self.make_controller()
                self.baseline(c, clock)
                events = c.events
                with self.assertRaises(ValueError):
                    c.measure_change(value)
                self.assertEqual(c.state, CycleState.READY)
                self.assertEqual(c.events, events)
                self.assertEqual(tv.commands, ())

    def test_invalid_changed_patch_leaves_ready_state_untouched(self):
        c, clock, tv, _ = self.make_controller()
        self.baseline(c, clock)
        events = c.events
        with self.assertRaises(ValueError):
            c.measure_change(49, (1, 2, False))
        self.assertEqual(c.events, events)
        self.assertEqual(tv.commands, ())

    def test_timing_limits_and_attempt_limits_require_bounded_positive_integers(self):
        for name in ("wait_ms", "read_timeout_ms", "max_attempts"):
            for value in (0, -1, True, 1.5, 3_600_001):
                with self.subTest(name=name, value=value), self.assertRaises(ValueError):
                    self.make_controller(**{name: value})

    def test_external_adapters_subclasses_and_real_mode_are_rejected(self):
        class ClockSubclass(FakeClock):
            pass
        class TVSubclass(SimulatedTV):
            pass
        class MeterSubclass(SimulatedMeter):
            pass
        for clock, tv, meter in ((ClockSubclass(), SimulatedTV(), SimulatedMeter(())),
                                  (FakeClock(), TVSubclass(), SimulatedMeter(())),
                                  (FakeClock(), SimulatedTV(), MeterSubclass(())),
                                  (lambda: 0, SimulatedTV(), SimulatedMeter(()))):
            with self.subTest(clock=clock, tv=tv, meter=meter), self.assertRaises(TypeError):
                MeasurementController(clock, tv, meter)
        for options in ({"port": "COM_TEST"}, {"host": "example.invalid"}, {"real_mode": True}, {"transport": object()}):
            with self.subTest(options=options), self.assertRaises(TypeError):
                self.make_controller(**options)

    def test_records_and_snapshots_are_immutable_and_labelled(self):
        c, clock, tv, _ = self.make_controller()
        self.baseline(c, clock)
        records, events, commands = c.records, c.events, tv.commands
        with self.assertRaises(FrozenInstanceError):
            records[0].accepted = False
        with self.assertRaises(FrozenInstanceError):
            events[0].simulated = False
        self.assertTrue(all(e.simulated for e in events))
        self.assertIn("synthetic", records[0].correction)
        c.measure_change(49)
        self.assertEqual(len(records), 1)
        self.assertEqual(commands, ())
        self.assertLess(len(events), len(c.events))

    def test_fixture_validation_is_bounded_and_never_accepts_callbacks(self):
        bad_samples = ([], (MeterSample((1, 2, 3)),) * 257, (lambda: 1,))
        for samples in bad_samples:
            with self.subTest(samples=type(samples)), self.assertRaises(ValueError):
                SimulatedMeter(samples)
        for xyz in ((1, 2), [1, 2, 3], (True, 2, 3), ("1", 2, 3), (10 ** 400, 2, 3)):
            with self.subTest(xyz=type(xyz)), self.assertRaises(ValueError):
                MeterSample(xyz)
        for value in (-1, True, 1.5, 3_600_001):
            with self.subTest(delay=value), self.assertRaises(ValueError):
                MeterSample((1, 2, 3), after_ms=value)
        with self.assertRaises(ValueError):
            MeterSample((1, 2, 3), error="x" * 201)
        for initial in (-1, 101, False, 1.5):
            with self.subTest(initial=initial), self.assertRaises(ValueError):
                SimulatedTV(initial)
        for steps in ([], (TVStep(),) * 257, (lambda: 1,)):
            with self.subTest(steps=type(steps)), self.assertRaises(ValueError):
                SimulatedTV(steps=steps)
        with self.assertRaises(TypeError):
            TVStep(reply="ACK")
        with self.assertRaises(TypeError):
            TVStep(apply=1)
        with self.assertRaises(ValueError):
            TVStep(menu_value=True)


if __name__ == "__main__":
    unittest.main()
