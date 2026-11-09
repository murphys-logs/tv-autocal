"""Fake console records, Tk events and clocks only; no native calls/windows."""

import ctypes
import sys
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from tv_autocal_tools.serial_input import ConsoleStop, MouseControls
from tv_autocal_tools.serial_tool import _WindowsRuntime, run_serial
from test_component_serial import FakeRuntime, Recorder, event, permit


class Function:
    def __init__(self, call):
        self.call = call

    def __call__(self, *args):
        return self.call(*args)


class Kernel:
    def __init__(self, events=(), mode=1):
        self.events = list(events)
        self.calls = []
        self.failure = False
        self.GetStdHandle = Function(lambda handle: 123)

        def get_mode(handle, pointer):
            pointer._obj.value = mode or 0
            return mode is not None

        def read(handle, records, capacity, count, flags):
            self.calls.append((handle, capacity, flags))
            n = min(capacity, len(self.events))
            for index in range(n):
                source = self.events.pop(0)
                records[index].EventType = source.EventType
                key = records[index].Event.KeyEvent
                for name in ("bKeyDown", "wRepeatCount", "wVirtualKeyCode", "dwControlKeyState"):
                    setattr(key, name, getattr(source.Event.KeyEvent, name))
                key.uChar.UnicodeChar = source.Event.KeyEvent.uChar.UnicodeChar
            count._obj.value = n
            return not self.failure

        self.GetConsoleMode = Function(get_mode)
        self.ReadConsoleInputExW = Function(read)


class Toolkit:
    def __init__(self):
        self.nodes, self.events = [], []
        self.configurations = []
        self.turns = 0
        self.destroyed = False

    def node(self, **options):
        owner = self

        class Node:
            def __init__(self):
                self.options = options
                self.bindings, self.protocols = {}, {}
                self.tags = None
                self.tk = owner

            def __getattr__(self, name):
                return lambda *args, **kwargs: None

            def bind(self, name, callback):
                self.bindings[name] = callback

            def bindtags(self, tags):
                self.tags = tags

            def protocol(self, name, callback):
                self.protocols[name] = callback

            def configure(self, **kwargs):
                self.options.update(kwargs)
                owner.configurations.append((self, kwargs))

            def winfo_width(self):
                return 200

            def winfo_height(self):
                return 40

            def destroy(self):
                owner.destroyed = True

        node = Node()
        self.nodes.append(node)
        return node

    def Tk(self):
        return self.node()

    def Label(self, *args, **kwargs):
        return self.node(**kwargs)

    def Button(self, *args, **kwargs):
        return self.node(**kwargs)

    def dooneevent(self, flags):
        if flags != 2:
            raise AssertionError("GUI poll must not wait")
        self.turns += 1
        if not self.events:
            return 0
        self.events.pop(0)()
        return 1

    def click(self, control, key, *, release=True, x=1, y=1):
        button = control.buttons[key]
        value = SimpleNamespace(widget=button, x=x, y=y)
        self.events.append(lambda: button.bindings["<ButtonPress-1>"](value))
        if release:
            self.events.append(lambda: button.bindings["<ButtonRelease-1>"](value))


class SerialInputTests(TestCase):
    def console(self, kernel):
        with patch.object(ctypes, "WinDLL", return_value=kernel, create=True):
            return ConsoleStop()

    def controls(self):
        toolkit = Toolkit()
        return MouseControls(toolkit, x=0, y=0), toolkit

    def native_runtime(self, events=()):
        # Bypass the real Windows constructor; every boundary stays inert.
        runtime = object.__new__(_WindowsRuntime)
        runtime.controls, toolkit = self.controls()
        toolkit.events = list(events)
        runtime.port = FakeRuntime().port
        runtime._console = SimpleNamespace(poll=lambda: False)
        clock = [0]
        runtime._time = SimpleNamespace(monotonic_ns=lambda: clock[0] * 1_000_000,
                                        sleep=lambda seconds: clock.__setitem__(0, clock[0] + 10))
        return runtime, toolkit, clock

    def test_nowait_abi_fixed_layout_and_one_bounded_read(self):
        kernel = Kernel()
        console = self.console(kernel)
        self.assertEqual(ctypes.sizeof(console._records._type_), 20)
        self.assertEqual(console._records._type_.Event.offset, 4)
        self.assertEqual(ctypes.sizeof(console._records[0].Event.KeyEvent), 16)
        self.assertFalse(console.poll())
        self.assertEqual(kernel.calls, [(123, 32, 2)])

    def test_win32_layout_does_not_follow_host_wchar_or_long_widths(self):
        from ctypes import wintypes
        with patch.object(wintypes, "BOOL", ctypes.c_int64), \
                patch.object(wintypes, "DWORD", ctypes.c_uint64), \
                patch.object(wintypes, "WCHAR", ctypes.c_uint32):
            console = self.console(Kernel([event("q")]))
        self.assertEqual(ctypes.sizeof(console._records._type_), 20)
        self.assertEqual(ctypes.sizeof(console._records[0].Event.KeyEvent), 16)
        self.assertTrue(console.poll())

    def test_unicode_partial_special_surrogate_then_delayed_q_is_preserved(self):
        kernel = Kernel([event("\u00e0", vk=0), event("\x00", vk=0x27), event("\ud800", vk=0)])
        console = self.console(kernel)
        self.assertFalse(console.poll())
        for _ in range(10):
            self.assertFalse(console.poll())  # Never waits for any matching suffix.
        kernel.events += [event("q")]
        self.assertTrue(console.poll())
        self.assertEqual(len(kernel.calls), 12)

    def test_special_and_paste_records_cannot_issue_actions(self):
        # Conhost clipboard synthesis can supply ordinary VK+scan/down/up.
        # No metadata heuristic makes these into TV actions.
        for text in ("bmoecdr", "\u00e0\x00\ud800", "[200~bmoecdr[201~"):
            console = self.console(Kernel([event(char, vk=ord(char.upper()) if char.isascii() else 0)
                                           for char in text]))
            self.assertFalse(console.poll())
        self.assertFalse(self.console(Kernel([event("q", vk=0x22)])).poll())

    def test_continuous_console_input_is_bounded_and_q_survives_next_batch(self):
        kernel = Kernel([event("e", vk=0x45)] * 32 + [event("q")])
        console = self.console(kernel)
        self.assertFalse(console.poll())
        self.assertEqual(len(kernel.events), 1)
        self.assertTrue(console.poll())

    def test_console_api_failure_redirected_and_vt_modes_reject(self):
        for mode in (None, 0, 0x201):
            with self.subTest(mode=mode), self.assertRaises(RuntimeError):
                self.console(Kernel(mode=mode))
        kernel = Kernel()
        console = self.console(kernel)
        kernel.failure = True
        with self.assertRaisesRegex(RuntimeError, "event read failed"):
            console.poll()

    def test_invalid_console_event_count_is_rejected_without_indexing(self):
        console = self.console(Kernel())
        def invalid_count(handle, records, capacity, count, flags):
            count._obj.value = capacity + 1
            return True
        console._read = invalid_count
        with self.assertRaisesRegex(RuntimeError, "invalid event count"):
            console.poll()

    def test_gui_and_serial_constructor_failures_cleanup_created_controls(self):
        tk = Toolkit()
        tk.Label = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fake layout"))
        with self.assertRaisesRegex(RuntimeError, "fake layout"):
            MouseControls(tk, x=0, y=0)
        self.assertTrue(tk.destroyed)
        controls, toolkit = self.controls()
        serial = SimpleNamespace(VERSION="3.5", Serial=lambda **kwargs:
                                 (_ for _ in ()).throw(OSError("fake port constructor")))
        with patch.object(sys, "platform", "win32"), \
                patch.dict(sys.modules, {"serial": serial, "tkinter": object()}), \
                patch("tv_autocal_tools.serial_input.ConsoleStop"), \
                patch("tv_autocal_tools.serial_input.MouseControls", return_value=controls):
            with self.assertRaisesRegex(OSError, "fake port constructor"):
                _WindowsRuntime("COM999", control_x=0, control_y=0)
        self.assertTrue(toolkit.destroyed)

    def test_mouse_only_controls_remove_class_and_global_bindings(self):
        controls, tk = self.controls()
        for key, button in controls.buttons.items():
            self.assertEqual(button.tags, (str(button),))
            self.assertNotIn("command", button.options)
            self.assertFalse(button.options["takefocus"])
            for char in "bmoecdr Q\r\n\x00\xe0":
                self.assertEqual(button.bindings["<KeyPress>"](SimpleNamespace(char=char)), "break")
            self.assertEqual(button.bindings["<KeyRelease>"](None), "break")
        self.assertIsNone(controls.poll("exit ready"))
        self.assertEqual(tk.turns, 1)

    def test_only_current_allowlisted_mouse_action_is_returned(self):
        for phase, (allowed, _) in MouseControls.ACTIONS.items():
            for key in "bmoecdr":
                with self.subTest(phase=phase, key=key):
                    controls, tk = self.controls()
                    controls.poll(phase)
                    tk.click(controls, key)
                    self.assertEqual(controls.poll(phase), key if key == allowed else None)
                    self.assertIsNone(controls.poll(phase))

    def test_incomplete_press_does_not_block_and_phase_change_discards_it(self):
        controls, tk = self.controls()
        controls.poll("exit ready")
        tk.click(controls, "e", release=False)
        self.assertIsNone(controls.poll("exit ready"))
        for _ in range(4):
            self.assertIsNone(controls.poll("exit ready"))
        button = controls.buttons["e"]
        tk.events.append(lambda: controls._up("e", SimpleNamespace(widget=button, x=1, y=1)))
        self.assertIsNone(controls.poll("reply"))
        self.assertIsNone(controls.poll("exit ready"))

    def test_queued_click_from_old_phase_is_discarded_before_enabling_new_phase(self):
        for previous, next_phase, key in (("initial quiet", "baseline", "b"),
                                          ("observe setting", "exit ready", "e"),
                                          ("exit ready", "reply", "e")):
            controls, tk = self.controls()
            controls.poll(previous)
            tk.click(controls, key)
            self.assertIsNone(controls.poll(next_phase))
            self.assertIsNone(controls.poll(next_phase))

    def test_outside_release_and_multiple_queued_actions_cannot_dispatch(self):
        controls, tk = self.controls()
        controls.poll("exit ready")
        tk.click(controls, "e", x=-1)
        self.assertIsNone(controls.poll("exit ready"))
        tk.click(controls, "e")
        tk.click(controls, "e")
        self.assertIsNone(controls.poll("exit ready"))

    def test_stop_wins_over_pending_action_and_remains_terminal(self):
        for stop in (lambda c: c.stop(), lambda c: c.root.protocols["WM_DELETE_WINDOW"](),
                     lambda c: c._key(SimpleNamespace(char="q"))):
            controls, tk = self.controls()
            controls.poll("exit ready")
            tk.click(controls, "e")
            tk.events.append(lambda: stop(controls))
            self.assertEqual(controls.poll("exit ready"), "q")
            tk.click(controls, "e")
            self.assertEqual(controls.poll("exit ready"), "q")
            controls.close()
            self.assertTrue(tk.destroyed)
            with self.assertRaises(RuntimeError):
                controls.poll("exit ready")

    def test_callback_failure_remains_terminal(self):
        controls, tk = self.controls()
        tk.events.append(lambda: controls._callback_error(RuntimeError, RuntimeError("fixture"), None))
        with self.assertRaisesRegex(RuntimeError, "fixture"):
            controls.poll("exit ready")
        self.assertEqual(controls.poll("exit ready"), "q")

    def test_bursts_drain_across_polls_and_require_fresh_click_after_idle(self):
        controls, tk = self.controls()
        controls.poll("exit ready")
        tk.events = [lambda: None] * 100
        tk.click(controls, "e")
        for _ in range(3):
            before = tk.turns
            self.assertIsNone(controls.poll("exit ready"))
            self.assertEqual(tk.turns - before, 32)
            self.assertFalse(controls.ready)
            self.assertEqual(controls.buttons["e"].options["state"], "disabled")
            self.assertEqual(controls.buttons["q"].options["state"], "normal")
        self.assertIsNone(controls.poll("exit ready"))
        self.assertTrue(controls.ready)
        self.assertIsNone(controls.poll("exit ready"))
        tk.click(controls, "e")
        self.assertEqual(controls.poll("exit ready"), "e")

    def test_full_turn_discards_candidate_action_instead_of_retaining_it(self):
        controls, tk = self.controls()
        controls.poll("exit ready")
        tk.click(controls, "e")
        tk.events += [lambda: None] * 30
        self.assertIsNone(controls.poll("exit ready"))
        self.assertFalse(controls.ready)
        self.assertIsNone(controls.poll("exit ready"))
        self.assertTrue(controls.ready)
        self.assertIsNone(controls.poll("exit ready"))

    def test_latest_phase_wins_while_stale_input_drains_disabled(self):
        controls, tk = self.controls()
        controls.poll("initial quiet")
        tk.events = [lambda: None] * 80
        tk.click(controls, "b")
        self.assertIsNone(controls.poll("baseline"))
        self.assertIsNone(controls.poll("menu preparation"))
        self.assertIsNone(controls.poll("menu preparation"))
        self.assertTrue(controls.ready)
        tk.click(controls, "b")
        self.assertIsNone(controls.poll("menu preparation"))
        tk.click(controls, "m")
        self.assertEqual(controls.poll("menu preparation"), "m")

    def test_quit_and_stop_remain_active_during_backlog_and_phase_change(self):
        for action in (lambda c: c._key(SimpleNamespace(char="q")),
                       lambda c: c._down("q"),
                       lambda c: c.root.protocols["WM_DELETE_WINDOW"]()):
            controls, tk = self.controls()
            tk.events = [lambda: None] * 40 + [lambda: action(controls)]
            self.assertIsNone(controls.poll("baseline"))
            self.assertEqual(controls.poll("menu preparation"), "q")
            self.assertFalse(controls.ready)

    def test_widget_states_change_only_when_enabled_action_changes(self):
        controls, tk = self.controls()
        controls.poll("baseline")
        first = len(tk.configurations)
        self.assertEqual(first, 1)
        for _ in range(100):
            self.assertIsNone(controls.poll("baseline"))
        self.assertEqual(len(tk.configurations), first)
        controls.poll("menu preparation")
        self.assertEqual(len(tk.configurations), first + 2)
        for _ in range(100):
            self.assertIsNone(controls.poll("menu preparation"))
        self.assertEqual(len(tk.configurations), first + 2)

    def test_startup_reaches_idle_before_any_port_open(self):
        runtime, tk, clock = self.native_runtime([lambda: None] * 80)
        opened = runtime.port.open
        observations = []
        runtime.port.open = lambda: (observations.append((len(tk.events), runtime.controls.ready)), opened())[1]
        runtime.open()
        self.assertEqual(observations, [(0, True)])
        self.assertEqual(clock[0], 20)
        self.assertTrue(runtime.port.opened)
        self.assertEqual(runtime.now(), 0)  # Initial quiet starts after open.

    def test_unsettled_startup_and_owner_quit_never_open_port(self):
        runtime, tk, clock = self.native_runtime([lambda: None] * 4000)
        with self.assertRaisesRegex(RuntimeError, "did not become idle"):
            runtime.open()
        self.assertFalse(runtime.port.opened)
        self.assertEqual(tk.turns, 3200)
        self.assertEqual(clock[0], 1000)
        runtime, tk, _ = self.native_runtime()
        runtime._console.poll = lambda: True
        log = Recorder()
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertFalse(runtime.port.opened)
        self.assertTrue(result.closed)
        self.assertTrue(tk.destroyed)
        self.assertIn("owner stopped before serial open", result.reason)

    def test_receive_and_deadline_checks_continue_while_gui_never_quiesces(self):
        controls, tk = self.controls()
        tk.events = [lambda: None] * 10000
        runtime, log = FakeRuntime(), Recorder()
        runtime.key = controls.poll
        read, polls = runtime.port.read, []
        runtime.port.read = lambda count: (polls.append(runtime.time), read(count))[1]
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000, session_ms=100)
        self.assertEqual(polls[:11], list(range(0, 110, 10)))
        self.assertIn("session deadline", result.reason)
        self.assertEqual(runtime.port.writes, [])
        self.assertTrue(result.closed)

    def test_input_exception_detail_is_bounded_and_kept_in_private_journal(self):
        runtime, log = FakeRuntime(), Recorder()
        detail = "synthetic callback failure " * 100
        runtime.key = lambda phase: (_ for _ in ()).throw(RuntimeError(detail))
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000)
        failure = next(fields for kind, fields in log.events if kind == "serial_failure")
        self.assertEqual(failure, {"elapsed_ms": 0, "stage": "operation", "error_type": "RuntimeError",
                                   "detail": detail[:256]})
        self.assertIn(detail[:256], result.reason)
        self.assertEqual(runtime.port.writes, [])
        self.assertTrue(result.closed)

    def test_console_q_takes_priority_over_pending_mouse_action(self):
        controls = SimpleNamespace(poll=lambda phase: self.fail("GUI must not consume q"))
        runtime = SimpleNamespace(_console=SimpleNamespace(poll=lambda: True), controls=controls)
        self.assertEqual(_WindowsRuntime.key(runtime, "exit ready"), "q")

    def test_receive_polling_and_session_deadline_continue_with_incomplete_input(self):
        kernel = Kernel([event("\u00e0", vk=0), event("\x00", vk=0x27)])
        console = self.console(kernel)
        controls, tk = self.controls()
        runtime, log = FakeRuntime(), Recorder()
        runtime.key = lambda phase: "q" if console.poll() else controls.poll(phase)
        read = runtime.port.read
        polls = []
        runtime.port.read = lambda count: (polls.append(runtime.time), read(count))[1]
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000, session_ms=100)
        self.assertIn("session deadline", result.reason)
        self.assertEqual(polls[:11], list(range(0, 110, 10)))
        self.assertTrue(result.closed)
        self.assertFalse(result.accepted)

    def test_delayed_console_quit_and_receive_are_retained_without_any_send(self):
        kernel = Kernel()
        console = self.console(kernel)
        controls, tk = self.controls()
        runtime, log = FakeRuntime(), Recorder()
        runtime.key = lambda phase: "q" if console.poll() else controls.poll(phase)
        kernel.events.append(event("\u00e0", vk=0))
        def later(rt):
            if rt.time == 100:
                kernel.events.append(event("q"))
            if rt.time == 200:
                rt.port.traffic.append(b"late")
        runtime.after_pause = later
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertEqual(runtime.time, 600)
        self.assertEqual(result.received_bytes, 4)
        self.assertEqual(runtime.port.writes, [])
        self.assertIn("owner stopped", result.reason)

    def test_reply_deadline_keeps_running_with_partial_console_input(self):
        kernel = Kernel([event("\x00", vk=0x27)])
        console = self.console(kernel)
        runtime = FakeRuntime({5000: "b", 5010: "m", 5020: "o", 5030: "e"})
        mouse_key = runtime.key
        runtime.key = lambda phase: "q" if console.poll() else mouse_key(phase)
        def silent_write(frame):
            runtime.port.writes.append(frame)
            return 7
        runtime.port.write = silent_write
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=Recorder(),
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertIn("exclusive reply deadline", result.reason)
        self.assertEqual(runtime.time, 7530)
        self.assertEqual(len(runtime.port.writes), 1)
        self.assertTrue(result.closed)

    def test_control_closure_failure_is_reported_separately_from_port_closure(self):
        runtime, log = FakeRuntime({0: "q"}), Recorder()
        runtime.close_controls = lambda: (_ for _ in ()).throw(OSError("fake close failure"))
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertTrue(result.closed)
        self.assertFalse(result.accepted)
        self.assertTrue(any(kind == "serial_controls_closed" and fields["closed"] is False
                            for kind, fields in log.events))

    def test_interrupt_during_port_close_still_closes_controls_and_rejects(self):
        runtime, log = FakeRuntime({0: "q"}), Recorder()
        runtime.port.close = lambda: (_ for _ in ()).throw(KeyboardInterrupt())
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=log,
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertTrue(runtime.controls_closed)
        self.assertFalse(result.closed)
        self.assertFalse(result.accepted)
        self.assertTrue(any(kind == "serial_controls_closed" and fields["closed"] is True
                            for kind, fields in log.events))

    def test_delayed_q_delivery_rechecks_deadline_before_accepting_complete_sequence(self):
        keys = {5000: "b", 5010: "m", 5020: "o", 5030: "e", 5550: "c",
                7550: "d", 8070: "m", 8080: "o", 8090: "e", 8610: "c",
                10610: "r", 11130: "m", 11140: "o", 11150: "e", 11670: "c", 13680: "q"}
        runtime = FakeRuntime(keys)
        read_key = runtime.key
        def delayed(phase):
            key = read_key(phase)
            if key == "q":
                runtime.time = 120000
            return key
        runtime.key = delayed
        with patch("tv_autocal_tools.serial_tool._WindowsRuntime", return_value=runtime), patch("builtins.print"):
            result = run_serial(permit(), port="COM999", control_x=0, control_y=0, log=Recorder(),
                                prerequisites_confirmed=True, menu_window_ms=10000)
        self.assertEqual(result.writes, 5)
        self.assertTrue(result.closed)
        self.assertFalse(result.accepted)
        self.assertIn("session deadline", result.reason)

    def test_missing_control_coordinates_reject_before_backend(self):
        for x, y in ((None, 0), (0, None), (False, 0), (-1, 0), (0, 32768)):
            with patch("tv_autocal_tools.serial_tool._WindowsRuntime") as factory:
                with self.assertRaises(ValueError):
                    run_serial(permit(), port="COM999", control_x=x, control_y=y, log=Recorder(),
                               prerequisites_confirmed=True, menu_window_ms=10000)
                factory.assert_not_called()
