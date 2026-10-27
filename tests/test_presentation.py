"""Synthetic presenter tests; no monitor is enumerated or receives pixels."""

from dataclasses import FrozenInstanceError
from hashlib import sha256
import unittest
from unittest.mock import patch

from tv_autocal.presentation import DisplayTarget, ManualPresenter, PresentationReceipt
from tv_autocal.simulation import FakeClock


class PresentationTests(unittest.TestCase):
    def make_presenter(self, patches=((16, 128, 235), (0, 0, 0))):
        clock = FakeClock()
        return ManualPresenter(clock, (DisplayTarget("fixture-a"), DisplayTarget("fixture-b")), patches), clock

    def ready(self, presenter):
        presenter.select("fixture-a")
        presenter.confirm("fixture-a")

    def test_selection_confirmation_and_fake_time_do_not_render_or_advance(self):
        with patch("tv_autocal.presentation.render_patch", side_effect=AssertionError("Unexpected rendering")):
            presenter, clock = self.make_presenter()
            self.assertIs(presenter.clock, clock)
            clock.advance(5000)
            self.assertIsNone(presenter.frame)
            self.assertIsNone(presenter.current_receipt)
            with self.assertRaises(RuntimeError):
                presenter.advance()
            presenter.select("fixture-a")
            with self.assertRaises(RuntimeError):
                presenter.advance()
            with self.assertRaises(ValueError):
                presenter.confirm("fixture-b")
            presenter.confirm("fixture-a")
            self.assertTrue(presenter.confirmed)
            self.assertEqual(presenter.receipts, ())
            self.assertIsNone(presenter.frame)

    def test_explicit_advance_preserves_native_patch_and_receipt_identity(self):
        presenter, clock = self.make_presenter()
        self.ready(presenter)
        clock.advance(17)
        receipt = presenter.advance()
        frame = presenter.frame
        self.assertEqual((frame.width, frame.height, len(frame.pixels)), (3840, 2160, 24883200))
        # Independent literal corner/surround checks preserve the approved 6.25% geometry.
        for x, y in ((1440, 810), (2399, 810), (1440, 1349), (2399, 1349), (1920, 1080)):
            self.assertEqual(frame.pixel(x, y), (16, 128, 235))
        for x, y in ((1439, 810), (2400, 810), (1440, 809), (1440, 1350), (0, 0)):
            self.assertEqual(frame.pixel(x, y), (0, 0, 0))
        self.assertEqual((receipt.sequence, receipt.target.name, receipt.patch_rgb, receipt.presented_ms),
                         (1, "fixture-a", (16, 128, 235), 17))
        self.assertEqual(receipt.frame_sha256, sha256(frame.pixels).hexdigest())
        self.assertTrue(receipt.simulated)
        self.assertFalse(receipt.displayed_on_hardware)
        self.assertIs(presenter.current_receipt, receipt)
        self.assertEqual(presenter.receipts, (receipt,))
        clock.advance(1000)
        self.assertEqual(presenter.receipts, (receipt,))
        self.assertIs(presenter.frame, frame)

    def test_reselect_before_output_requires_confirmation_again(self):
        presenter, _ = self.make_presenter()
        self.ready(presenter)
        presenter.select("fixture-b")
        self.assertFalse(presenter.confirmed)
        with self.assertRaises(RuntimeError):
            presenter.advance()
        with self.assertRaises(ValueError):
            presenter.confirm("fixture-a")
        presenter.confirm("fixture-b")
        receipt = presenter.advance()
        self.assertEqual(receipt.target.name, "fixture-b")

    def test_target_and_confirmation_cannot_change_after_first_output(self):
        presenter, _ = self.make_presenter()
        self.ready(presenter)
        receipt = presenter.advance()
        for action in (lambda: presenter.select("fixture-b"), lambda: presenter.confirm("fixture-a")):
            with self.assertRaises(RuntimeError):
                action()
        self.assertEqual(presenter.receipts, (receipt,))
        self.assertEqual(presenter.selected_target.name, "fixture-a")

    def test_hold_blocks_advance_and_only_matching_release_allows_next_patch(self):
        presenter, clock = self.make_presenter()
        with self.assertRaises(ValueError):
            presenter.hold(1)
        self.ready(presenter)
        first = presenter.advance()
        token = presenter.hold(first.sequence)
        self.assertEqual(presenter.held_token, token)
        frame = presenter.frame
        clock.advance(2000)
        for action in (presenter.advance, lambda: presenter.hold(1)):
            with self.assertRaises(RuntimeError):
                action()
        with self.assertRaises(ValueError):
            presenter.release(2, token)
        self.assertEqual(presenter.held_sequence, 1)
        self.assertIs(presenter.frame, frame)
        self.assertEqual(presenter.receipts, (first,))
        presenter.release(1, token)
        second = presenter.advance()
        self.assertEqual((second.sequence, second.patch_rgb, second.presented_ms), (2, (0, 0, 0), 2000))
        self.assertIsNone(presenter.held_sequence)
        self.assertIsNone(presenter.held_token)
        self.assertEqual(presenter.frame.pixels, b"\0" * 24883200)
        self.assertEqual(presenter.receipts, (first, second))
        with self.assertRaises(ValueError):
            presenter.hold(1)

    def test_stale_token_cannot_release_a_later_hold_on_the_same_frame(self):
        presenter, _ = self.make_presenter()
        self.ready(presenter)
        receipt = presenter.advance()
        old_token = presenter.hold(receipt.sequence)
        presenter.release(receipt.sequence, old_token)
        new_token = presenter.hold(receipt.sequence)
        self.assertGreater(new_token, old_token)
        for token in (old_token, True, 0, -1, "1"):
            with self.subTest(token=token), self.assertRaises(ValueError):
                presenter.release(receipt.sequence, token)
            self.assertEqual((presenter.held_sequence, presenter.held_token), (receipt.sequence, new_token))
        with self.assertRaises(RuntimeError):
            presenter.advance()
        presenter.release(receipt.sequence, new_token)
        self.assertIsNone(presenter.held_token)

    def test_close_while_held_clears_frame_and_is_terminal_without_losing_receipts(self):
        presenter, clock = self.make_presenter()
        self.ready(presenter)
        receipt = presenter.advance()
        token = presenter.hold(1)
        presenter.close()
        self.assertTrue(presenter.closed)
        self.assertIsNone(presenter.frame)
        self.assertIsNone(presenter.current_receipt)
        self.assertIsNone(presenter.held_sequence)
        self.assertIsNone(presenter.held_token)
        self.assertEqual(presenter.receipts, (receipt,))
        clock.advance(3000)
        presenter.cancel()
        presenter.close()
        for action in (presenter.advance, lambda: presenter.select("fixture-a"),
                       lambda: presenter.confirm("fixture-a"), lambda: presenter.hold(1),
                       lambda: presenter.release(1, token)):
            with self.subTest(action=action), self.assertRaises(RuntimeError):
                action()
        self.assertEqual(presenter.receipts, (receipt,))

    def test_cancel_before_selection_never_renders(self):
        presenter, _ = self.make_presenter()
        presenter.cancel()
        self.assertTrue(presenter.closed)
        self.assertEqual(presenter.receipts, ())
        self.assertIsNone(presenter.frame)

    def test_sequence_exhaustion_does_not_repeat_clear_or_create_another_receipt(self):
        presenter, _ = self.make_presenter(((1, 2, 3),))
        self.ready(presenter)
        receipt = presenter.advance()
        frame = presenter.frame
        with self.assertRaisesRegex(RuntimeError, "exhausted"):
            presenter.advance()
        self.assertIs(presenter.frame, frame)
        self.assertEqual(presenter.receipts, (receipt,))
        self.assertFalse(presenter.closed)

    def test_unknown_or_nonnative_target_is_rejected_without_scaling_or_state_change(self):
        clock = FakeClock()
        presenter = ManualPresenter(clock, (DisplayTarget("native"), DisplayTarget("small", 1920, 1080)), ((1, 2, 3),))
        presenter.select("native")
        presenter.confirm("native")
        for name in ("small", "missing", True, None):
            with self.subTest(name=name), self.assertRaises(ValueError):
                presenter.select(name)
            self.assertEqual(presenter.selected_target.name, "native")
            self.assertTrue(presenter.confirmed)
            self.assertIsNone(presenter.frame)
        self.assertEqual(presenter.receipts, ())

    def test_fixture_input_validation_rejects_coercion_mutability_and_unbounded_lists(self):
        for name in ("", " bad", "bad ", "bad\nname", "x" * 65, True, None):
            with self.subTest(name=name), self.assertRaises(ValueError):
                DisplayTarget(name)
        for width, height in ((0, 2160), (3840, -1), (True, 2160), (3840, 1.5), (16385, 2160)):
            with self.subTest(width=width, height=height), self.assertRaises(ValueError):
                DisplayTarget("fixture", width, height)
        target = DisplayTarget("fixture")
        for targets in ([], (), (target, target), (object(),), tuple(DisplayTarget(str(i)) for i in range(17))):
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                ManualPresenter(FakeClock(), targets, ((0, 0, 0),))
        for patches in ([], (), ((0, 0, 0),) * 257, ([0, 0, 0],), ((0, 0),),
                        ((True, 0, 0),), ((0, 0, 256),), ((0, -1, 0),), ((0.0, 0, 0),)):
            with self.subTest(patches=patches), self.assertRaises(ValueError):
                ManualPresenter(FakeClock(), (target,), patches)

    def test_concrete_fakes_only_and_no_real_mode_options(self):
        class ClockSubclass(FakeClock):
            pass
        class TargetSubclass(DisplayTarget):
            pass
        for clock in (ClockSubclass(), lambda: 0, None):
            with self.subTest(clock=clock), self.assertRaises(TypeError):
                ManualPresenter(clock, (DisplayTarget("fixture"),), ((0, 0, 0),))
        with self.assertRaises(ValueError):
            ManualPresenter(FakeClock(), (TargetSubclass("fixture"),), ((0, 0, 0),))
        for options in ({"port": "COM_TEST"}, {"real_mode": True}, {"transport": lambda: None}):
            with self.subTest(options=options), self.assertRaises(TypeError):
                ManualPresenter(FakeClock(), (DisplayTarget("fixture"),), ((0, 0, 0),), **options)

    def test_receipts_and_targets_are_immutable_and_flags_cannot_be_overridden(self):
        target = DisplayTarget("fixture")
        receipt = PresentationReceipt(1, target, (1, 2, 3), 0, "a" * 64)
        with self.assertRaises(FrozenInstanceError):
            target.width = 1
        with self.assertRaises(FrozenInstanceError):
            receipt.sequence = 2
        with self.assertRaises(TypeError):
            PresentationReceipt(1, target, (1, 2, 3), 0, "a" * 64, simulated=False)
        for sequence, time, digest in ((True, 0, "a" * 64), (0, 0, "a" * 64),
                                       (1, True, "a" * 64), (1, -1, "a" * 64),
                                       (1, 0, "z" * 64), (1, 0, "A" * 64)):
            with self.subTest(sequence=sequence, time=time, digest=digest), self.assertRaises(ValueError):
                PresentationReceipt(sequence, target, (1, 2, 3), time, digest)


if __name__ == "__main__":
    unittest.main()
