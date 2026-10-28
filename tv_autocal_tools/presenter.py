"""Manually advanced native-size Windows presenter; hardware opt-in required.

Import and validation are inert. Only run_presenter opens a window, after its
permit is checked. This does not prove HDMI codes, colour-path fidelity or light.
"""

from hashlib import sha256
from sys import platform
from time import monotonic_ns

from tv_autocal.renderer import (HEIGHT, WIDTH, T003_RANGE_CODES, T005_NEUTRAL_CODES,
                                T005_PRIMARY_CODES, pattern_manifest, render_patch, render_pattern)
from .permission import HardwarePermit


MAX_PATTERNS = 256
MAX_DURATION_SECONDS = 10800  # Proposed three-hour resource bound, not a timing result.
CONTROL_WIDTH, CONTROL_HEIGHT = 440, 220
NEXT_GUARD_MS = 1000  # Proposed input guard, not a display-settling interval.


def validate_sequence(sequence: tuple) -> tuple:
    """Copy no mutable playlist or implicit display selection into a run."""
    if type(sequence) is not tuple or not 1 <= len(sequence) <= MAX_PATTERNS:
        raise ValueError("A tuple containing 1..256 explicit patterns is required")
    names = {spec.name for spec in pattern_manifest()}
    for item in sequence:
        if type(item) is str and item in names:
            continue
        if type(item) is tuple and len(item) == 3 and all(
            type(component) is int and 0 <= component <= 255 for component in item
        ):
            continue
        raise ValueError("Use an existing visual-pattern name or an RGB8 tuple")
    return sequence


def _validate_position(x: int, y: int) -> None:
    if any(type(value) is not int or not 0 <= value <= 32767 for value in (x, y)):
        raise ValueError("Explicit nonnegative desktop x/y coordinates in 0..32767 are required")


def _overlap(a: tuple, b: tuple) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def validate_control_position(x: int, y: int, control_x: int, control_y: int) -> None:
    """Reject an overlapping requested client area without opening any window.

    Decoration bounds and a distinct monitor's work area are checked natively
    later. This arithmetic alone does not establish a usable second display.
    """
    _validate_position(x, y)
    _validate_position(control_x, control_y)
    if _overlap((x, y, x + WIDTH, y + HEIGHT),
                (control_x, control_y, control_x + CONTROL_WIDTH, control_y + CONTROL_HEIGHT)):
        raise ValueError("The operator controls must be outside the TV rectangle")


def validate_plan_sequence(plan: str, sequence: tuple) -> tuple:
    """Limit physical patterns to the existing component plans' literal codes."""
    validate_sequence(sequence)
    if plan not in ("T-003", "T-005"):
        raise ValueError("No presentation sequence is defined for this plan")
    neutral = {128, *(T003_RANGE_CODES if plan == "T-003" else T005_NEUTRAL_CODES)}
    for item in sequence:
        if type(item) is str:
            if plan == "T-005":
                continue
        elif item[0] == item[1] == item[2] and item[0] in neutral:
            continue
        elif plan == "T-005" and sum(value != 0 for value in item) == 1 and max(item) in T005_PRIMARY_CODES:
            continue
        raise ValueError("Pattern is outside this component plan's bounded allowlist")
    return sequence


class PresenterController:
    """Window-independent manual controls, exercised with an inert fake backend.

    The backend must expose check_geometry, bind, show, confirm, set_next_enabled,
    mainloop, schedule and close. It owns the actual platform boundary; callers are not
    sandboxed. The public hardware entry point always constructs the real one.
    """

    def __init__(self, window, sequence: tuple, log) -> None:
        self.window = window
        self.sequence = validate_sequence(sequence)
        self.log = log
        self.confirmed = False
        self.closed = False
        self.index = 0
        self.error: BaseException | None = None
        self._started_ns = monotonic_ns()
        self._next_pending = False
        self._next_ready_ns = 0

    def _record(self, kind: str, **fields) -> None:
        self.log(kind, elapsed_ms=(monotonic_ns() - self._started_ns) // 1_000_000,
                 hardware=True, **fields)

    def close(self, reason: str) -> None:
        if self.closed:
            return
        self.closed = True
        error = None
        try:
            self.window.close()
        except BaseException as failure:
            error = failure
        try:
            self._record("presenter_closed", reason=reason, frames=self.index,
                         close_completed=error is None)
        except BaseException as failure:
            if error is None:
                error = failure
        if error is not None:
            raise error

    def _failure(self, error: BaseException) -> None:
        if self.error is None:
            self.error = error
        try:
            self.close("failure: " + type(error).__name__)
        except BaseException:
            # The original failure remains visible; closure was attempted first.
            pass

    def press(self, key: str) -> None:
        """Keyboard input can only stop; it can never confirm or advance."""
        if key == "Escape":
            self.action("stop")

    def release(self, key: str) -> None:
        # Kept in the backend contract so it can suppress class key bindings.
        pass

    def action(self, command: str) -> None:
        """Only explicit operator-button commands reach the manual sequence."""
        if self.closed or command not in ("confirm", "next", "stop"):
            return
        try:
            if command == "stop":
                self.close("owner requested stop")
                return
            self.window.check_geometry()
            if command == "confirm":
                if not self.confirmed:
                    self._record("presenter_target_confirmed")
                    self.window.confirm()
                    self.confirmed = True
                return
            if not self.confirmed or self._next_pending:
                return
            if self.index == len(self.sequence):
                self.close("manual advance after final pattern")
                return
            # Guard the controller as well as the widget: already-queued or
            # reentrant commands must not bypass a disabled Next button.
            self._next_pending = True
            self.window.set_next_enabled(False)
            item = self.sequence[self.index]
            frame = render_pattern(item) if type(item) is str else render_patch(item)
            # Intention is durable before handing pixels to a window backend.
            self._record("pattern_present_intent", sequence=self.index + 1,
                         pattern=item, width=frame.width, height=frame.height,
                         sha256=sha256(frame.pixels).hexdigest())
            self.window.show(frame)
            if self.closed:
                # A backend callback may have stopped/failed during application.
                # Do not publish a receipt or rearm controls after that closure.
                return
            self.index += 1
            self._record("pattern_buffer_applied", sequence=self.index,
                         evidence="window update only; not measured light or HDMI verification")
            self._next_ready_ns = monotonic_ns() + NEXT_GUARD_MS * 1_000_000
            self.window.schedule(NEXT_GUARD_MS, self.release_next)
            if type(item) is str:
                generation = self.index
                self.window.schedule(60_000, lambda: self.expire_visual(generation))
        except BaseException as error:
            self._failure(error)

    def release_next(self) -> None:
        """Re-enable only after application plus the guard; never advance."""
        if self.closed or not self._next_pending:
            return
        try:
            remaining = self._next_ready_ns - monotonic_ns()
            if remaining > 0:
                self.window.schedule((remaining + 999_999) // 1_000_000, self.release_next)
                return
            self.window.check_geometry()
            self.window.set_next_enabled(True)
            self._next_pending = False
        except BaseException as error:
            self._failure(error)

    def watchdog(self) -> None:
        if self.closed:
            return
        try:
            self.window.check_geometry()
            self.window.schedule(200, self.watchdog)
        except BaseException as error:
            self._failure(error)

    def expire(self) -> None:
        if not self.closed:
            try:
                self.close("three-hour presenter lifetime reached; no automatic continuation")
            except BaseException as error:
                self._failure(error)

    def expire_visual(self, generation: int) -> None:
        if not self.closed and self.index == generation:
            try:
                self.close("60-second visual-pattern limit reached; no automatic advance")
            except BaseException as error:
                self._failure(error)

    def run(self) -> None:
        try:
            self.window.check_geometry()
            self.window.bind(self.press, self.release, lambda: self.action("stop"),
                             self.action, self._failure)
            self.window.schedule(200, self.watchdog)
            self.window.schedule(MAX_DURATION_SECONDS * 1000, self.expire)
            self.window.mainloop()
        except BaseException as error:
            self._failure(error)
        finally:
            if not self.closed:
                try:
                    self.close("window loop ended")
                except BaseException as error:
                    self._failure(error)
        if self.error is not None:
            raise self.error


def run_presenter(permit: HardwarePermit, *, x: int, y: int, control_x: int,
                  control_y: int, sequence: tuple, log) -> None:
    """Future owner-operated entry point. No default window or display scan.

    A valid permit is an owner attestation, not proof of physical prerequisites.
    A separate visible operator window has mouse-only confirm/next/stop buttons.
    Typing cannot confirm or advance. Escape closes either window. Every frame
    keeps native pixels; operator controls must fit another monitor's work area.
    """
    if type(permit) is not HardwarePermit:
        raise TypeError("A concrete hardware permit is required")
    permit.require("present")
    validate_control_position(x, y, control_x, control_y)
    validate_plan_sequence(permit.plan, sequence)
    if not callable(log):
        raise TypeError("A durable audit callback is required")
    if platform != "win32":
        raise RuntimeError("The physical presenter supports Windows only")
    log("presenter_open_intent", hardware=True, x=x, y=y, width=WIDTH, height=HEIGHT,
        control_x=control_x, control_y=control_y, control_width=CONTROL_WIDTH,
        control_height=CONTROL_HEIGHT, sequence=sequence, plan=permit.plan,
        revision=permit.revision)
    window = _open_window(x, y, control_x, control_y)
    try:
        PresenterController(window, sequence, log).run()
    except BaseException:
        try:
            window.close()
        except BaseException:
            pass
        raise


def _native_geometry():
    """Load user32 only inside the explicit physical run path."""
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    user32.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
    user32.SetProcessDpiAwarenessContext.restype = wintypes.BOOL
    user32.GetThreadDpiAwarenessContext.argtypes = []
    user32.GetThreadDpiAwarenessContext.restype = ctypes.c_void_p
    user32.AreDpiAwarenessContextsEqual.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    user32.AreDpiAwarenessContextsEqual.restype = wintypes.BOOL
    context = ctypes.c_void_p(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
    user32.SetProcessDpiAwarenessContext(context)
    if not user32.AreDpiAwarenessContextsEqual(user32.GetThreadDpiAwarenessContext(), context):
        raise RuntimeError("Per-monitor V2 DPI awareness could not be established")

    class MonitorInfo(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

    user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.GetClientRect.restype = wintypes.BOOL
    user32.ClientToScreen.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.POINT)]
    user32.ClientToScreen.restype = wintypes.BOOL
    user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
    user32.MonitorFromWindow.restype = wintypes.HANDLE
    user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MonitorInfo)]
    user32.GetMonitorInfoW.restype = wintypes.BOOL
    user32.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    user32.GetAncestor.restype = wintypes.HWND
    user32.GetWindowRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    user32.GetWindowRect.restype = wintypes.BOOL

    def ensure_dpi() -> None:
        if not user32.AreDpiAwarenessContextsEqual(user32.GetThreadDpiAwarenessContext(), context):
            raise RuntimeError("Per-monitor V2 DPI awareness changed during presentation")

    def monitor_info(hwnd: int):
        monitor = user32.MonitorFromWindow(hwnd, 0)  # No nearest-monitor fallback.
        info = MonitorInfo()
        info.cbSize = ctypes.sizeof(info)
        if not monitor or not user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            raise RuntimeError("Cannot verify the selected window's monitor")
        return info

    def check(hwnd: int, x: int, y: int) -> None:
        ensure_dpi()
        client, origin = wintypes.RECT(), wintypes.POINT(0, 0)
        if not user32.GetClientRect(hwnd, ctypes.byref(client)) or not user32.ClientToScreen(
            hwnd, ctypes.byref(origin)
        ):
            raise RuntimeError("Cannot verify physical client rectangle")
        if (client.left, client.top, client.right, client.bottom, origin.x, origin.y) != (
            0, 0, WIDTH, HEIGHT, x, y
        ):
            raise RuntimeError("Native client geometry changed; no scaling fallback")
        info = monitor_info(hwnd)
        area = info.rcMonitor
        if (area.left, area.top, area.right, area.bottom) != (x, y, x + WIDTH, y + HEIGHT):
            raise RuntimeError("Window must exactly cover one native 3840x2160 monitor")

    def check_control(hwnd: int, x: int, y: int) -> None:
        ensure_dpi()
        # Tk's client HWND can sit inside a decorated top-level wrapper. Include
        # the real outer titlebar/borders, not just the button client rectangle.
        outer = user32.GetAncestor(hwnd, 2)  # GA_ROOT, not GA_ROOTOWNER.
        rectangle = wintypes.RECT()
        if not outer or not user32.GetWindowRect(outer, ctypes.byref(rectangle)):
            raise RuntimeError("Cannot verify the operator window's outer rectangle")
        bounds = (rectangle.left, rectangle.top, rectangle.right, rectangle.bottom)
        television = (x, y, x + WIDTH, y + HEIGHT)
        info = monitor_info(outer)
        monitor = info.rcMonitor
        work = info.rcWork
        if (rectangle.right <= rectangle.left or rectangle.bottom <= rectangle.top
                or _overlap(bounds, television)
                or _overlap((monitor.left, monitor.top, monitor.right, monitor.bottom), television)
                or not (work.left <= rectangle.left < rectangle.right <= work.right
                        and work.top <= rectangle.top < rectangle.bottom <= work.bottom)):
            raise RuntimeError("Operator window must fit another monitor's work area without TV overlap")

    return check, check_control


def _open_window(x: int, y: int, control_x: int, control_y: int):
    checks = _native_geometry()  # Must precede Tk/window creation.
    import tkinter as tk
    return _TkWindow(tk, checks, x, y, control_x, control_y)


class _TkWindow:
    def __init__(self, tk, checks, x: int, y: int, control_x: int, control_y: int) -> None:
        self.tk, self.x, self.y = tk, x, y
        self.geometry_check, self.control_check = checks
        self.closed = False
        self.image = None
        self.display = None
        self._press = lambda key: None
        self._action = lambda command: None
        self._failure = None
        self._pending_error = None
        self.root = tk.Tk()
        try:
            self.root.report_callback_exception = self._callback_exception
            self.root.withdraw()
            self.root.title("TV autocal — presenter controls")
            self.root.geometry(f"{CONTROL_WIDTH}x{CONTROL_HEIGHT}+{control_x}+{control_y}")
            self.root.resizable(False, False)
            self.instructions = tk.Label(self.root, text="Check the intended TV before confirming.\n"
                                         "Use the mouse buttons below. Typing does not advance.\n"
                                         "Stop or Escape closes both windows.")
            self.instructions.pack(pady=12)
            self.buttons = {}
            for name, text in (("confirm", "Confirm TV target"), ("next", "Next pattern"),
                               ("stop", "Stop presentation")):
                button = tk.Button(self.root, text=text, takefocus=False,
                                   state="disabled" if name == "next" else "normal",
                                   command=lambda selected=name: self._action(selected))
                # Widget bindings run before the Button class's Space/Return
                # handlers. Suppress both edges; ordinary typing cannot invoke.
                button.bind("<KeyPress>", self._key)
                button.bind("<KeyRelease>", lambda event: "break")
                button.pack(pady=3)
                self.buttons[name] = button
            self.root.bind("<KeyPress>", self._key)
            self.root.bind("<KeyRelease>", lambda event: "break")
            self.display = tk.Toplevel(self.root)
            self.display.withdraw()
            self.display.overrideredirect(True)
            self.display.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
            self.display.configure(background="black", cursor="none")
            self.display.resizable(False, False)
            self.label = tk.Label(self.display, background="black", foreground="white",
                                  borderwidth=0, highlightthickness=0, padx=0, pady=0,
                                  text="Check the intended 3840x2160 screen.\n"
                                       "Confirm using the separate presenter controls.\n"
                                       "No reading while this confirmation is visible.")
            self.label.place(x=0, y=0, width=WIDTH, height=HEIGHT)
            self.display.bind("<KeyPress>", self._key)
            self.display.bind("<KeyRelease>", lambda event: "break")
            # Verify the operator controls before showing anything on the TV.
            # Native decoration bounds may not exist until the controls map.
            self.root.deiconify()
            self.root.update_idletasks()
            self._raise_pending()
            self._check_control_layout()
            self.control_check(self.root.winfo_id(), x, y)
            self.display.deiconify()
            self.root.update_idletasks()
            self._raise_pending()
            self.check_geometry()
        except BaseException:
            try:
                self.close()
            except BaseException:
                pass
            raise

    def _raise_pending(self) -> None:
        if self._pending_error is not None:
            raise self._pending_error

    def _callback_exception(self, error_type, error, traceback) -> None:
        if self._pending_error is None:
            self._pending_error = error
        if self._failure is not None:
            self._failure(error)
        else:
            try:
                self.close()
            except BaseException:
                pass

    def _key(self, event):
        if event.keysym == "Escape":
            self._press("Escape")
        return "break"

    def check_geometry(self) -> None:
        if self.closed:
            raise RuntimeError("Presenter window is closed")
        self._check_control_layout()
        self.geometry_check(self.display.winfo_id(), self.x, self.y)
        self.control_check(self.root.winfo_id(), self.x, self.y)

    def _check_control_layout(self) -> None:
        # Requested dimensions reflect packed text/buttons at the current Tk
        # scaling. A fixed client area must not silently clip a control.
        required = (self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        available = (self.root.winfo_width(), self.root.winfo_height())
        if any(need <= 0 or need > min(actual, limit)
               for need, actual, limit in zip(required, available, (CONTROL_WIDTH, CONTROL_HEIGHT))):
            raise RuntimeError("Operator controls do not fit; display scaling/layout needs review")

    def set_next_enabled(self, enabled: bool) -> None:
        self.buttons["next"].configure(state="normal" if enabled else "disabled")

    def confirm(self) -> None:
        self.label.configure(text="")
        self.buttons["confirm"].configure(state="disabled")
        self.instructions.configure(text="TV target confirmed. Click Next pattern when authorised.\n"
                                    "Keep the held TV image unobstructed.\n"
                                    "Stop or Escape closes both windows.")
        self.root.update_idletasks()
        self._raise_pending()
        self.check_geometry()
        self.set_next_enabled(True)

    def show(self, frame) -> None:
        self.check_geometry()
        payload = b"P6\n3840 2160\n255\n" + frame.pixels
        image = self.tk.PhotoImage(master=self.display, data=payload, format="PPM", gamma=1.0)
        if (image.width(), image.height()) != (WIDTH, HEIGHT):
            raise RuntimeError("Tk image dimensions differ from the native frame")
        self.label.configure(text="", image=image)
        self.image = image  # Tk needs a live Python reference to retain pixels.
        self.root.update_idletasks()
        self.check_geometry()

    def bind(self, press, release, close, action, failure) -> None:
        self._press, self._action, self._failure = press, action, failure
        self.root.protocol("WM_DELETE_WINDOW", close)
        self.display.protocol("WM_DELETE_WINDOW", close)
        self._raise_pending()

    def mainloop(self) -> None:
        self.root.mainloop()

    def schedule(self, milliseconds: int, callback) -> None:
        self.root.after(milliseconds, callback)

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            self.image = None
            error = None
            if self.display is not None:
                try:
                    self.display.destroy()
                except BaseException as failure:
                    error = failure
            try:
                self.root.destroy()
            except BaseException as failure:
                if error is None:
                    error = failure
            if error is not None:
                # A failed destroy must not leave callbacks running indefinitely
                # before the controller can propagate the failure. Quitting the
                # loop is not proof that either native window was destroyed.
                try:
                    self.root.quit()
                except BaseException:
                    pass
                raise error
