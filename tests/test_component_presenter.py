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

    def bind(self, press, release, close, action, failure):
        self.press, self.release, self.on_close = press, release, close
        self.action, self.failure = action, failure

    def mainloop(self):
        for key in self.actions:
            self.action(key)

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
                 monitor=(0, 0, WIDTH, HEIGHT), control=(3850, 10, 4300, 260),
                 control_monitor=(3840, 0, 5760, 1080), work=(3840, 0, 5760, 1040)):
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
            area = control_monitor if handle == 2 else monitor
            for name, value in zip(("left", "top", "right", "bottom"), area):
                setattr(pointer._obj.rcMonitor, name, value)
            for name, value in zip(("left", "top", "right", "bottom"), work):
                setattr(pointer._obj.rcWork, name, value)
            return True

        def outer_rectangle(hwnd, pointer):
            for name, value in zip(("left", "top", "right", "bottom"), control):
                setattr(pointer._obj, name, value)
            return True

        self.GetClientRect = FakeFunction(rectangle)
        self.ClientToScreen = FakeFunction(position)
        self.MonitorFromWindow = FakeFunction(lambda hwnd, flags: 2 if hwnd == 200 else 1)
        self.GetMonitorInfoW = FakeFunction(monitor_info)
        self.GetAncestor = FakeFunction(lambda hwnd, flags: 200)
        self.GetWindowRect = FakeFunction(outer_rectangle)


class FakeTk:
    """No Tcl interpreter: record only widget calls and dispatch callbacks."""

    def __init__(self):
        self.calls, self.images, self.nodes = [], [], []

    def node(self, name, **options):
        toolkit = self
        class Node:
            def __init__(self):
                self.name, self.options = name, options
                self.bindings, self.protocols = {}, {}
            def __getattr__(self, method):
                def record(*args, **kwargs):
                    toolkit.calls.append((name, method, args, kwargs))
                return record
            def configure(self, **kwargs):
                self.options.update(kwargs)
                toolkit.calls.append((name, "configure", (), kwargs))
            def bind(self, event, callback):
                self.bindings[event] = callback
            def protocol(self, name, callback):
                self.protocols[name] = callback
            def winfo_id(self):
                return 99 if name == "root" else 100
        result = Node()
        self.nodes.append(result)
        return result

    def Tk(self):
        return self.node("root")

    def Toplevel(self, root):
        return self.node("display")

    def Label(self, *args, **kwargs):
        return self.node("label", **kwargs)

    def Button(self, *args, **kwargs):
        return self.node("button", **kwargs)

    def PhotoImage(self, **kwargs):
        self.images.append(kwargs)
        return SimpleNamespace(width=lambda: WIDTH, height=lambda: HEIGHT)


class ComponentPresenterTests(unittest.TestCase):
    def controller(self, sequence=((128, 128, 128),)):
        window = FakeWindow()
        events = []
        controller = presenter.PresenterController(window, sequence,
                                                    lambda kind, **data: events.append((kind, data)))
        return controller, window, events

    def tap(self, controller, command):
        controller.action(command)

    def test_hardware_disabled_before_window_backend_or_log(self):
        with patch.object(presenter, "_open_window", side_effect=AssertionError("window")):
            with self.assertRaises(PermissionError):
                presenter.run_presenter(permit(False), x=0, y=0, control_x=3840, control_y=0, sequence=((0, 0, 0),),
                                        log=lambda *a, **k: self.fail("log reached"))

    def test_wrong_permit_scope_and_types_are_rejected_before_backend(self):
        wrong = HardwarePermit("T-006", "a" * 40, "fixture", "fixture", "fixture", ("serial",), True)
        for value, error in ((wrong, PermissionError), (object(), TypeError)):
            with self.subTest(value=value), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(error):
                    presenter.run_presenter(value, x=0, y=0, control_x=3840, control_y=0, sequence=((0, 0, 0),), log=lambda *a, **k: None)
                backend.assert_not_called()

    def test_position_playlist_and_platform_fail_before_window(self):
        for x, y in ((-1, 0), (0, -1), (True, 0), (0, 32768), (0, 1.5)):
            with self.subTest(x=x, y=y), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(ValueError):
                    presenter.run_presenter(permit(), x=x, y=y, control_x=3840, control_y=0, sequence=((0, 0, 0),), log=lambda *a, **k: None)
                backend.assert_not_called()
        with patch.object(presenter, "platform", "linux"), patch.object(presenter, "_open_window") as backend:
            with self.assertRaises(RuntimeError):
                presenter.run_presenter(permit(), x=0, y=0, control_x=3840, control_y=0, sequence=((0, 0, 0),), log=lambda *a, **k: None)
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
                    presenter.run_presenter(replace(permit(), plan=plan), x=0, y=0, control_x=3840, control_y=0, sequence=sequence,
                                            log=lambda *a, **k: self.fail("log reached"))
                backend.assert_not_called()

    def test_confirmation_does_not_render_and_each_button_action_advances_once(self):
        controller, window, events = self.controller(((128, 128, 128), (255, 0, 0)))
        self.tap(controller, "next")
        self.assertEqual(window.frames, [])
        self.tap(controller, "confirm")
        self.assertTrue(window.confirmed)
        self.assertEqual(window.frames, [])
        controller.action("next")
        self.assertEqual(len(window.frames), 1)
        self.tap(controller, "next")
        self.assertEqual(len(window.frames), 2)
        self.tap(controller, "next")
        self.assertTrue(window.closed)
        self.assertEqual(len(window.frames), 2)

    def test_patch_pixels_and_native_geometry_are_preserved(self):
        controller, window, events = self.controller(((12, 34, 56),))
        self.tap(controller, "confirm")
        self.tap(controller, "next")
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
        self.tap(controller, "confirm")
        def fail(kind, **data):
            if kind == "pattern_present_intent":
                raise OSError("full log")
        controller.log = fail
        self.tap(controller, "next")
        self.assertTrue(window.closed)
        self.assertEqual(window.frames, [])
        self.assertIsInstance(controller.error, OSError)

    def test_pattern_intent_precedes_backend_and_receipt_follows(self):
        controller, window, events = self.controller()
        controller.log = lambda kind, **data: window.order.append(kind)
        self.tap(controller, "confirm")
        self.tap(controller, "next")
        self.assertEqual(window.order[-3:], ["pattern_present_intent", "show", "pattern_buffer_applied"])

    def test_geometry_failure_before_advance_stops_without_frame(self):
        controller, window, events = self.controller()
        self.tap(controller, "confirm")
        window.valid = False
        self.tap(controller, "next")
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
        self.tap(controller, "confirm")
        self.tap(controller, "next")
        milliseconds, callback = window.timers[-1]
        self.assertEqual(milliseconds, 60_000)
        self.tap(controller, "next")
        callback()
        self.assertFalse(window.closed)
        controller.expire()
        self.assertTrue(window.closed)
        controller, window, events = self.controller(("black",))
        self.tap(controller, "confirm")
        self.tap(controller, "next")
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
        window = FakeWindow(("confirm", "next", "stop"))
        events = []
        def make(x, y, control_x, control_y):
            self.assertEqual(events[0][0], "presenter_open_intent")
            self.assertEqual((x, y, control_x, control_y), (3840, 0, 0, 0))
            return window
        with patch.object(presenter, "platform", "win32"), patch.object(presenter, "_open_window", make):
            presenter.run_presenter(permit(), x=3840, y=0, control_x=0, control_y=0, sequence=((0, 0, 0),),
                                    log=lambda kind, **data: events.append((kind, data)))
        self.assertTrue(window.closed)
        self.assertEqual(len(window.frames), 1)
        self.assertEqual([value for value, _ in window.timers], [200, 10_800_000])

    def test_callback_failure_is_propagated_after_loop_closes(self):
        window = FakeWindow(("confirm", "next"))
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
                    presenter._native_geometry()[0](99, 0, 0)
                else:
                    with self.assertRaises(RuntimeError):
                        presenter._native_geometry()[0](99, 0, 0)

    def test_native_api_failure_does_not_fall_back_to_nearest_monitor(self):
        for name in ("GetClientRect", "ClientToScreen", "MonitorFromWindow", "GetMonitorInfoW"):
            native = FakeUser32()
            setattr(native, name, FakeFunction(lambda *args: 0))
            with self.subTest(name=name), patch.object(ctypes, "WinDLL", return_value=native, create=True):
                with self.assertRaises(RuntimeError):
                    presenter._native_geometry()[0](99, 0, 0)

    def test_tk_backend_uses_raw_ppm_and_no_pixel_rescaling(self):
        tk = FakeTk()
        checks = (lambda *args: None, lambda *args: None)
        with patch.object(presenter, "_native_geometry", return_value=checks), patch.dict(sys.modules, {"tkinter": tk}):
            window = presenter._open_window(0, 0, 3840, 10)
            self.assertEqual(tk.images, [])
            frame = render_patch((4, 5, 6))
            window.confirm()
            window.show(frame)
            self.assertEqual(tk.images[0]["data"], b"P6\n3840 2160\n255\n" + frame.pixels)
            self.assertEqual((tk.images[0]["format"], tk.images[0]["gamma"]), ("PPM", 1.0))
            self.assertIs(tk.images[0]["master"], window.display)
            self.assertEqual(next(kwargs for name, method, args, kwargs in tk.calls if method == "place"),
                             {"x": 0, "y": 0, "width": 3840, "height": 2160})
            self.assertFalse(any(method in ("focus_set", "focus_force") for _, method, _, _ in tk.calls))
            window.close()
            window.close()
            self.assertEqual(sum(method == "destroy" for _, method, _, _ in tk.calls), 2)

    def test_overlapping_or_invalid_control_position_fails_before_any_backend(self):
        for x, y in ((0, 0), (3800, 0), (0, 2100), (-1, 0), (True, 0), (32768, 0)):
            with self.subTest(control=(x, y)), patch.object(presenter, "_open_window") as backend:
                with self.assertRaises(ValueError):
                    presenter.run_presenter(permit(), x=0, y=0, control_x=x, control_y=y,
                                            sequence=((0, 0, 0),), log=lambda *a, **k: self.fail("log"))
                backend.assert_not_called()
        presenter.validate_control_position(0, 0, WIDTH, 0)
        presenter.validate_control_position(WIDTH, 0, 0, 0)

    def test_console_text_and_old_shortcuts_never_confirm_or_advance_in_any_phase(self):
        keys = list('python -B -m tv_autocal_tools meter --rgb 128,128,128 local/a.log')
        keys += ["c", "C", "space", "Right", "Return", "Tab", "F1", "F10"]
        for phase in ("unconfirmed", "confirmed", "holding", "closed"):
            with self.subTest(phase=phase):
                controller, window, events = self.controller()
                if phase != "unconfirmed":
                    controller.action("confirm")
                if phase in ("holding", "closed"):
                    controller.action("next")
                if phase == "closed":
                    controller.action("stop")
                before = (controller.confirmed, controller.index, controller.closed, len(events))
                for key in keys:
                    controller.press(key)
                    controller.release(key)
                self.assertEqual((controller.confirmed, controller.index, controller.closed, len(events)), before)

    def test_operator_buttons_suppress_keyboard_class_activation_but_accept_mouse_commands(self):
        tk = FakeTk()
        window = presenter._TkWindow(tk, (lambda *args: None, lambda *args: None), 0, 0, 3840, 10)
        controller = presenter.PresenterController(window, ((0, 0, 0),), lambda *a, **k: None)
        window.bind(controller.press, controller.release, lambda: controller.action("stop"),
                    controller.action, controller._failure)
        for node in (window.root, window.display, *window.buttons.values()):
            for key in ("c", "C", "space", "Right", "Return", "Tab", "a", "minus"):
                for edge in ("<KeyPress>", "<KeyRelease>"):
                    result = node.bindings[edge](SimpleNamespace(keysym=key))
                    # A break prevents subsequent Tk class/default bindings.
                    self.assertEqual(result, "break")
        self.assertFalse(controller.confirmed)
        self.assertEqual(controller.index, 0)
        window.buttons["confirm"].options["command"]()
        self.assertTrue(controller.confirmed)
        self.assertEqual(window.buttons["confirm"].options["state"], "disabled")
        self.assertEqual(window.buttons["next"].options["state"], "normal")
        window.buttons["next"].options["command"]()
        self.assertEqual(controller.index, 1)
        window.buttons["stop"].options["command"]()
        self.assertTrue(window.closed)

    def test_escape_or_window_close_stops_from_either_window_without_tv_focus(self):
        for target in ("root", "display", "button"):
            for mechanism in ("escape", "window-close"):
                if target == "button" and mechanism == "window-close":
                    continue
                with self.subTest(target=target, mechanism=mechanism):
                    tk = FakeTk()
                    window = presenter._TkWindow(tk, (lambda *args: None, lambda *args: None), 0, 0, 3840, 10)
                    controller = presenter.PresenterController(window, ((0, 0, 0),), lambda *a, **k: None)
                    window.bind(controller.press, controller.release, lambda: controller.action("stop"),
                                controller.action, controller._failure)
                    node = window.buttons["next"] if target == "button" else getattr(window, target)
                    if mechanism == "escape":
                        node.bindings["<KeyPress>"](SimpleNamespace(keysym="Escape"))
                    else:
                        node.protocols["WM_DELETE_WINDOW"]()
                    self.assertTrue(window.closed)
                    self.assertEqual(controller.index, 0)

    def test_control_outer_bounds_require_different_monitor_and_fit_work_area(self):
        configurations = (
            ({}, True),
            ({"control": (3835, 10, 4285, 260)}, False),  # Border intrudes into TV.
            ({"control": (3850, 900, 4300, 1100)}, False),  # Beyond monitor/taskbar.
            ({"control_monitor": (0, 0, WIDTH, HEIGHT)}, False),
            ({"work": (3840, 0, 5760, 200)}, False),
            ({"control": (3850, 10, 3850, 260)}, False),
        )
        for kwargs, valid in configurations:
            with self.subTest(kwargs=kwargs), patch.object(ctypes, "WinDLL", return_value=FakeUser32(**kwargs), create=True):
                check = presenter._native_geometry()[1]
                if valid:
                    check(101, 0, 0)
                else:
                    with self.assertRaises(RuntimeError):
                        check(101, 0, 0)

    def test_control_native_api_failure_has_no_fallback(self):
        for name in ("GetAncestor", "GetWindowRect", "MonitorFromWindow", "GetMonitorInfoW"):
            native = FakeUser32()
            setattr(native, name, FakeFunction(lambda *args: 0))
            with self.subTest(name=name), patch.object(ctypes, "WinDLL", return_value=native, create=True):
                with self.assertRaises(RuntimeError):
                    presenter._native_geometry()[1](101, 0, 0)

    def test_invalid_operator_geometry_closes_controls_before_tv_is_shown(self):
        tk = FakeTk()
        def invalid(*args):
            raise RuntimeError("operator overlaps")
        with self.assertRaisesRegex(RuntimeError, "operator overlaps"):
            presenter._TkWindow(tk, (lambda *args: None, invalid), 0, 0, 3840, 10)
        self.assertFalse(any(name == "display" and method == "deiconify"
                             for name, method, _, _ in tk.calls))
        self.assertEqual(sum(method == "destroy" for _, method, _, _ in tk.calls), 2)

    def test_control_move_is_checked_by_watchdog_before_further_advance(self):
        tk = FakeTk()
        allowed = [True]
        def control_check(*args):
            if not allowed[0]:
                raise RuntimeError("control moved onto TV")
        window = presenter._TkWindow(tk, (lambda *args: None, control_check), 0, 0, 3840, 10)
        controller = presenter.PresenterController(window, ((0, 0, 0),), lambda *a, **k: None)
        allowed[0] = False
        controller.watchdog()
        controller.action("confirm")
        controller.action("next")
        self.assertTrue(window.closed)
        self.assertIsInstance(controller.error, RuntimeError)
        self.assertEqual(controller.index, 0)

    def test_interrupts_in_actions_are_terminal_and_retained(self):
        for error_type in (KeyboardInterrupt, SystemExit):
            for operation in ("check_geometry", "confirm", "show", "schedule"):
                with self.subTest(error=error_type, operation=operation):
                    controller, window, events = self.controller(("black",))
                    if operation in ("show", "schedule"):
                        controller.action("confirm")
                    original = error_type("fake interrupt")
                    def fail(*args):
                        raise original
                    setattr(window, operation, fail)
                    controller.action("next" if operation in ("show", "schedule") else "confirm")
                    self.assertTrue(window.closed)
                    self.assertIs(controller.error, original)
                    previous = len(window.frames)
                    controller.action("next")
                    self.assertEqual(len(window.frames), previous)

    def test_keyboard_interrupt_inside_watchdog_or_scheduling_closes_and_propagates(self):
        for operation in ("check_geometry", "schedule"):
            controller, window, events = self.controller()
            failure = KeyboardInterrupt("watchdog")
            def fail(*args):
                raise failure
            setattr(window, operation, fail)
            controller.watchdog()
            self.assertTrue(window.closed)
            self.assertIs(controller.error, failure)
            with self.assertRaises(KeyboardInterrupt):
                controller.run()

    def test_mainloop_interrupts_are_not_reported_as_success(self):
        for error_type in (KeyboardInterrupt, SystemExit):
            controller, window, events = self.controller()
            def fail():
                raise error_type("mainloop")
            window.mainloop = fail
            with self.subTest(error=error_type), self.assertRaises(error_type):
                controller.run()
            self.assertTrue(window.closed)
            self.assertEqual(next(fields["reason"] for kind, fields in events if kind == "presenter_closed"),
                             "failure: " + error_type.__name__)

    def test_tk_reported_callback_interrupt_is_retained_and_raised_after_close(self):
        for error_type in (KeyboardInterrupt, RuntimeError):
            tk = FakeTk()
            window = presenter._TkWindow(tk, (lambda *args: None, lambda *args: None), 0, 0, 3840, 10)
            failure = error_type("Tk swallowed callback")
            def loop():
                window.root.report_callback_exception(error_type, failure, None)
            window.root.mainloop = loop
            controller = presenter.PresenterController(window, ((0, 0, 0),), lambda *a, **k: None)
            with self.subTest(error=error_type), self.assertRaises(error_type):
                controller.run()
            self.assertTrue(window.closed)
            self.assertIs(controller.error, failure)

    def test_constructor_interrupt_destroys_both_windows(self):
        tk = FakeTk()
        def interrupt(*args):
            raise KeyboardInterrupt("initial geometry")
        with self.assertRaises(KeyboardInterrupt):
            presenter._TkWindow(tk, (lambda *args: None, interrupt), 0, 0, 3840, 10)
        self.assertEqual(sum(method == "destroy" for _, method, _, _ in tk.calls), 2)

    def test_close_failure_attempts_both_windows_and_preserves_first_interrupt(self):
        tk = FakeTk()
        window = presenter._TkWindow(tk, (lambda *args: None, lambda *args: None), 0, 0, 3840, 10)
        def failure():
            raise KeyboardInterrupt("display destroy")
        window.display.destroy = failure
        with self.assertRaises(KeyboardInterrupt):
            window.close()
        self.assertTrue(any(name == "root" and method == "destroy" for name, method, _, _ in tk.calls))
        self.assertTrue(any(name == "root" and method == "quit" for name, method, _, _ in tk.calls))

    def test_both_destroy_failures_request_loop_quit_before_propagating(self):
        tk = FakeTk()
        window = presenter._TkWindow(tk, (lambda *args: None, lambda *args: None), 0, 0, 3840, 10)
        failed = []
        def display_failure():
            failed.append("display")
            raise OSError("display destroy failed")
        def root_failure():
            failed.append("root")
            raise RuntimeError("root destroy failed")
        window.display.destroy = display_failure
        window.root.destroy = root_failure
        with self.assertRaisesRegex(OSError, "display destroy failed"):
            window.close()
        self.assertEqual(failed, ["display", "root"])
        self.assertTrue(any(name == "root" and method == "quit" for name, method, _, _ in tk.calls))

    def test_close_failure_never_becomes_a_successful_controller_result(self):
        controller, window, events = self.controller()
        failure = OSError("fake native close failure")
        def fail():
            raise failure
        window.close = fail
        controller.action("stop")
        self.assertIs(controller.error, failure)
        record = next(fields for kind, fields in events if kind == "presenter_closed")
        self.assertFalse(record["close_completed"])
        with self.assertRaises(OSError):
            controller.run()


if __name__ == "__main__":
    unittest.main()
