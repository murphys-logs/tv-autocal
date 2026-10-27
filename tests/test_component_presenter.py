"""Offline presenter tests: every GUI/native boundary is an inert fake."""

import ctypes
from dataclasses import replace
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tv_autocal.renderer import HEIGHT, WIDTH, render_patch
from tv_autocal_tools.permission import HardwarePermit
from tv_autocal_tools import presenter


def permit(hardware=True):
    return HardwarePermit("T-003", "a" * 40, "authored test permission", "fixture steps",
                          "fixture prerequisites", ("present",), hardware)


class FakeWindow:
    def __init__(self, actions=()):
        self.actions = actions
        self.frames = []
        self.timers = []
        self.closed = False
        self.confirmed = False
        self.valid = True
        self.order = []

    def check_geometry(self):
        if not self.valid:
            raise RuntimeError("geometry mismatch")

    def bind(self, press, release, close):
        self.press, self.release, self.on_close = press, release, close

    def mainloop(self):
        for key in self.actions:
            self.press(key)
            self.release(key)

    def confirm(self):
        self.confirmed = True

    def show(self, frame):
        self.order.append("show")
        self.frames.append(frame)

    def schedule(self, ms, callback):
        self.timers.append((ms, callback))

    def close(self):
        self.closed = True


class FakeFunction:
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, *args):
        return self.callback(*args)


class FakeUser32:
    def __init__(self, *, dpi=True, client=(0, 0, WIDTH, HEIGHT), origin=(0, 0),
                 monitor=(0, 0, WIDTH, HEIGHT)):
        self.SetProcessDpiAwarenessContext = FakeFunction(lambda context: True)
        self.GetThreadDpiAwarenessContext = FakeFunction(lambda: -4)
        self.AreDpiAwarenessContextsEqual = FakeFunction(lambda a, b: dpi)

        def rectangle(hwnd, pointer):
            for name, value in zip(("left", "top", "right", "bottom"), client):
                setattr(pointer._obj, name, value)
            return True

        def position(hwnd, pointer):
            pointer._obj.x, pointer._obj.y = origin
            return True

        def monitor_info(handle, pointer):
            for name, value in zip(("left", "top", "right", "bottom"), monitor):
                setattr(pointer._obj.rcMonitor, name, value)
            return True

        self.GetClientRect = FakeFunction(rectangle)
        self.ClientToScreen = FakeFunction(position)
        self.MonitorFromWindow = FakeFunction(lambda hwnd, flags: 1)
        self.GetMonitorInfoW = FakeFunction(monitor_info)


class ComponentPresenterTests(unittest.TestCase):
    def controller(self, sequence=((128, 128, 128),)):
        window = FakeWindow()
        events = []
        controller = presenter.PresenterController(window, sequence,
                                                    lambda kind, **data: events.append((kind, data)))
        return controller, window, events

    def tap(self, controller, key):
        controller.press(key)
        controller.release(key)

    def test_hardware_disabled_before_window_backend_or_log(self):
        with patch.object(presenter, "_open_window", side_effect=AssertionError("window")):
            with self.assertRaises(PermissionError):
                presenter.run_presenter(permit(False), x=0, y=0, sequence=((0, 0, 0),),
                                        log=lambda *a, **k: self.fail("log reached"))

    def test_wrong_permit_scope_and_types_are_rejected_before_backend(self):
        wrong = HardwarePermit("T-006", "a" * 40, "fixture", "fixture", "fixture", ("serial",), True)
        for value, error in ((wrong, PermissionError), (object(), TypeError)):
            with self.subTest(value=value), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(error):
                    presenter.run_presenter(value, x=0, y=0, sequence=((0, 0, 0),), log=lambda *a, **k: None)
                backend.assert_not_called()

    def test_position_playlist_and_platform_fail_before_window(self):
        for x, y in ((-1, 0), (0, -1), (True, 0), (0, 32768), (0, 1.5)):
            with self.subTest(x=x, y=y), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(ValueError):
                    presenter.run_presenter(permit(), x=x, y=y, sequence=((0, 0, 0),), log=lambda *a, **k: None)
                backend.assert_not_called()
        with patch.object(presenter, "platform", "linux"), patch.object(presenter, "_open_window") as backend:
            with self.assertRaises(RuntimeError):
                presenter.run_presenter(permit(), x=0, y=0, sequence=((0, 0, 0),), log=lambda *a, **k: None)
            backend.assert_not_called()

    def test_playlist_is_explicit_immutable_bounded_and_literal(self):
        for sequence in ([], (), ((0, 0, 0),) * 257, ("unknown",), ([0, 0, 0],),
                         ((True, 0, 0),), ((-1, 0, 0),), ((0, 256, 0),)):
            with self.subTest(sequence=sequence), self.assertRaises(ValueError):
                presenter.validate_sequence(sequence)
        sequence = ("geometry", "detail", (1, 2, 3))
        self.assertIs(presenter.validate_sequence(sequence), sequence)

    def test_plan_allowlists_admit_only_the_component_plans_literal_patterns(self):
        t003 = tuple((code, code, code) for code in (128, 255, 51, 26, 13, 5, 0))
        t005 = ("geometry", "black", "white", "red", "green", "blue", "detail",
                (128, 128, 128), (102, 102, 102), (204, 0, 0), (0, 230, 0), (0, 0, 242))
        self.assertIs(presenter.validate_plan_sequence("T-003", t003), t003)
        self.assertIs(presenter.validate_plan_sequence("T-005", t005), t005)
        with self.assertRaises(ValueError):
            presenter.validate_plan_sequence("T-006", ((0, 0, 0),))

    def test_out_of_plan_hardware_patterns_fail_before_logging_or_backend(self):
        for plan, sequence in (("T-003", ("geometry",)), ("T-003", ((255, 0, 0),)),
                               ("T-003", ((102, 102, 102),)), ("T-005", ((32, 32, 32),)),
                               ("T-005", ((203, 0, 0),)), ("T-005", ((204, 204, 0),))):
            with self.subTest(plan=plan, sequence=sequence), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(ValueError):
                    presenter.run_presenter(replace(permit(), plan=plan), x=0, y=0, sequence=sequence,
                                            log=lambda *a, **k: self.fail("log reached"))
                backend.assert_not_called()

    def test_confirmation_does_not_render_and_each_separate_key_advances_once(self):
        controller, window, events = self.controller(((128, 128, 128), (255, 0, 0)))
        self.tap(controller, "space")
        self.assertEqual(window.frames, [])
        self.tap(controller, "c")
        self.assertTrue(window.confirmed)
        self.assertEqual(window.frames, [])
        controller.press("space")
        controller.press("space")  # Held-key repetition is not a new advance.
        self.assertEqual(len(window.frames), 1)
        controller.release("space")
        self.tap(controller, "space")
        self.assertEqual(len(window.frames), 2)
        self.tap(controller, "Right")
        self.assertTrue(window.closed)
        self.assertEqual(len(window.frames), 2)

    def test_patch_pixels_and_native_geometry_are_preserved(self):
        controller, window, events = self.controller(((12, 34, 56),))
        self.tap(controller, "c")
        self.tap(controller, "space")
        frame = window.frames[0]
        self.assertEqual((frame.width, frame.height), (3840, 2160))
        for x, y in ((1440, 810), (2399, 1349)):
            self.assertEqual(frame.pixel(x, y), (12, 34, 56))
        for x, y in ((1439, 810), (2400, 1349), (1440, 809), (2399, 1350)):
            self.assertEqual(frame.pixel(x, y), (0, 0, 0))
        intent = next(data for kind, data in events if kind == "pattern_present_intent")
        # Independently composed as 810 blank rows, 540 centred-patch rows,
        # then 810 blank rows, with 1440 black pixels on each side of the patch.
        self.assertEqual(intent["sha256"], "4897859669be943d4b5b5cb4fc8ab4d140e19e8dc0a29c5a5f13f63b1b85fe82")

    def test_log_failure_prevents_pattern_and_closes_window(self):
        controller, window, events = self.controller()
        self.tap(controller, "c")
        def fail(kind, **data):
            if kind == "pattern_present_intent":
                raise OSError("full log")
        controller.log = fail
        self.tap(controller, "space")
        self.assertTrue(window.closed)
        self.assertEqual(window.frames, [])
        self.assertIsInstance(controller.error, OSError)

    def test_pattern_intent_precedes_backend_and_receipt_follows(self):
        controller, window, events = self.controller()
        controller.log = lambda kind, **data: window.order.append(kind)
        self.tap(controller, "c")
        self.tap(controller, "space")
        self.assertEqual(window.order[-3:], ["pattern_present_intent", "show", "pattern_buffer_applied"])

    def test_geometry_failure_before_advance_stops_without_frame(self):
        controller, window, events = self.controller()
        self.tap(controller, "c")
        window.valid = False
        self.tap(controller, "space")
        self.assertTrue(window.closed)
        self.assertEqual(window.frames, [])
        self.assertIsInstance(controller.error, RuntimeError)

    def test_watchdog_stops_on_move_resize_or_monitor_mismatch(self):
        controller, window, events = self.controller()
        controller.watchdog()
        self.assertEqual(window.timers[0][0], 200)
        self.assertEqual(window.frames, [])
        window.valid = False
        window.timers[0][1]()
        self.assertTrue(window.closed)
        self.assertEqual(len(window.timers), 1)

    def test_visual_expiry_is_terminal_and_stale_timer_does_not_stop_next_frame(self):
        controller, window, events = self.controller(("geometry", (128, 128, 128)))
        self.tap(controller, "c")
        self.tap(controller, "space")
        milliseconds, callback = window.timers[-1]
        self.assertEqual(milliseconds, 60_000)
        self.tap(controller, "space")
        callback()
        self.assertFalse(window.closed)
        controller.expire()
        self.assertTrue(window.closed)
        controller, window, events = self.controller(("black",))
        self.tap(controller, "c")
        self.tap(controller, "space")
        window.timers[-1][1]()
        self.assertTrue(window.closed)
        self.assertEqual(len(window.frames), 1)

    def test_escape_and_lifetime_close_without_automatic_advance(self):
        for method in (lambda c: c.press("Escape"), lambda c: c.expire()):
            controller, window, events = self.controller()
            method(controller)
            controller.press("c")
            controller.press("space")
            self.assertTrue(window.closed)
            self.assertEqual(window.frames, [])

    def test_run_uses_only_fake_window_and_logs_open_before_backend(self):
        window = FakeWindow(("c", "space", "Escape"))
        events = []
        def make(x, y):
            self.assertEqual(events[0][0], "presenter_open_intent")
            self.assertEqual((x, y), (3840, 0))
            return window
        with patch.object(presenter, "platform", "win32"), patch.object(presenter, "_open_window", make):
            presenter.run_presenter(permit(), x=3840, y=0, sequence=((0, 0, 0),),
                                    log=lambda kind, **data: events.append((kind, data)))
        self.assertTrue(window.closed)
        self.assertEqual(len(window.frames), 1)
        self.assertEqual([value for value, _ in window.timers], [200, 10_800_000])

    def test_callback_failure_is_propagated_after_loop_closes(self):
        window = FakeWindow(("c", "space"))
        def broken_show(frame):
            raise RuntimeError("fake paint failure")
        window.show = broken_show
        controller = presenter.PresenterController(window, ((0, 0, 0),), lambda *a, **k: None)
        with self.assertRaisesRegex(RuntimeError, "fake paint failure"):
            controller.run()
        self.assertTrue(window.closed)

    def test_native_geometry_checks_use_only_fake_dll(self):
        configurations = (
            ({}, True), ({"dpi": False}, False),
            ({"client": (0, 0, 1920, 1080)}, False),
            ({"origin": (1, 0)}, False), ({"monitor": (0, 0, 7680, 2160)}, False),
        )
        for kwargs, valid in configurations:
            with self.subTest(kwargs=kwargs), patch.object(ctypes, "WinDLL", return_value=FakeUser32(**kwargs), create=True):
                if valid:
                    presenter._native_geometry()(99, 0, 0)
                else:
                    with self.assertRaises(RuntimeError):
                        presenter._native_geometry()(99, 0, 0)

    def test_native_api_failure_does_not_fall_back_to_nearest_monitor(self):
        for name in ("GetClientRect", "ClientToScreen", "MonitorFromWindow", "GetMonitorInfoW"):
            native = FakeUser32()
            setattr(native, name, FakeFunction(lambda *args: 0))
            with self.subTest(name=name), patch.object(ctypes, "WinDLL", return_value=native, create=True):
                with self.assertRaises(RuntimeError):
                    presenter._native_geometry()(99, 0, 0)

    def test_tk_backend_uses_raw_ppm_and_no_pixel_rescaling(self):
        calls = []
        class Root:
            def __getattr__(self, name):
                return lambda *args, **kwargs: calls.append((name, args, kwargs))
            def winfo_id(self):
                return 99
        class Label:
            def __init__(self, *args, **kwargs):
                calls.append(("label", args, kwargs))
            def place(self, **kwargs):
                calls.append(("place", (), kwargs))
            def configure(self, **kwargs):
                calls.append(("label_configure", (), kwargs))
        images = []
        def photo(**kwargs):
            images.append(kwargs)
            return SimpleNamespace(width=lambda: WIDTH, height=lambda: HEIGHT)
        tk = SimpleNamespace(Tk=Root, Label=Label, PhotoImage=photo)
        with patch.object(presenter, "_native_geometry", return_value=lambda *args: None), patch.dict(sys.modules, {"tkinter": tk}):
            window = presenter._open_window(0, 0)
            self.assertEqual(images, [])
            frame = render_patch((4, 5, 6))
            window.confirm()
            window.show(frame)
            self.assertEqual(images[0]["data"], b"P6\n3840 2160\n255\n" + frame.pixels)
            self.assertEqual((images[0]["format"], images[0]["gamma"]), ("PPM", 1.0))
            self.assertEqual(next(kwargs for name, args, kwargs in calls if name == "place"),
                             {"x": 0, "y": 0, "width": 3840, "height": 2160})
            window.close()
            self.assertEqual(sum(name == "destroy" for name, _, _ in calls), 1)


if __name__ == "__main__":
    unittest.main()
