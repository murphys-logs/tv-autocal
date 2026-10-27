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

    The backend must expose check_geometry, bind, show, confirm, mainloop,
    schedule and close. It owns the actual platform boundary; callers are not
    sandboxed. The public hardware entry point always constructs the real one.
    """

    def __init__(self, window, sequence: tuple, log) -> None:
        self.window = window
        self.sequence = validate_sequence(sequence)
        self.log = log
        self.confirmed = False
        self.closed = False
        self.index = 0
        self._pressed: set[str] = set()
        self.error: Exception | None = None
        self._started_ns = monotonic_ns()

    def _record(self, kind: str, **fields) -> None:
        self.log(kind, elapsed_ms=(monotonic_ns() - self._started_ns) // 1_000_000,
                 hardware=True, **fields)

    def close(self, reason: str) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            self.window.close()
        finally:
            self._record("presenter_closed", reason=reason, frames=self.index)

    def _failure(self, error: Exception) -> None:
        if self.error is None:
            self.error = error
        try:
            self.close("failure: " + type(error).__name__)
        except Exception:
            # The original failure remains visible; closure was attempted first.
            pass

    def press(self, key: str) -> None:
        if self.closed or key in self._pressed:
            return
        self._pressed.add(key)
        try:
            if key == "Escape":
                self.close("owner requested stop")
                return
            if key not in ("c", "C", "space", "Right"):
                return
            self.window.check_geometry()
            if key in ("c", "C"):
                if not self.confirmed:
                    self._record("presenter_target_confirmed")
                    self.window.confirm()
                    self.confirmed = True
                return
            if not self.confirmed:
                return
            if self.index == len(self.sequence):
                self.close("manual advance after final pattern")
                return
            item = self.sequence[self.index]
            frame = render_pattern(item) if type(item) is str else render_patch(item)
            # Intention is durable before handing pixels to a window backend.
            self._record("pattern_present_intent", sequence=self.index + 1,
                         pattern=item, width=frame.width, height=frame.height,
                         sha256=sha256(frame.pixels).hexdigest())
            self.window.show(frame)
            self.index += 1
            self._record("pattern_buffer_applied", sequence=self.index,
                         evidence="window update only; not measured light or HDMI verification")
            if type(item) is str:
                generation = self.index
                self.window.schedule(60_000, lambda: self.expire_visual(generation))
        except Exception as error:
            self._failure(error)

    def release(self, key: str) -> None:
        self._pressed.discard(key)

    def watchdog(self) -> None:
        if self.closed:
            return
        try:
            self.window.check_geometry()
            self.window.schedule(200, self.watchdog)
        except Exception as error:
            self._failure(error)

    def expire(self) -> None:
        if not self.closed:
            try:
                self.close("three-hour presenter lifetime reached; no automatic continuation")
            except Exception as error:
                self._failure(error)

    def expire_visual(self, generation: int) -> None:
        if not self.closed and self.index == generation:
            try:
                self.close("60-second visual-pattern limit reached; no automatic advance")
            except Exception as error:
                self._failure(error)

    def run(self) -> None:
        try:
            self.window.check_geometry()
            self.window.bind(self.press, self.release, lambda: self.press("Escape"))
            self.window.schedule(200, self.watchdog)
            self.window.schedule(MAX_DURATION_SECONDS * 1000, self.expire)
            self.window.mainloop()
        except Exception as error:
            self._failure(error)
        finally:
            if not self.closed:
                try:
                    self.close("window loop ended")
                except Exception as error:
                    self._failure(error)
        if self.error is not None:
            raise self.error


def run_presenter(permit: HardwarePermit, *, x: int, y: int, sequence: tuple, log) -> None:
    """Future owner-operated entry point. No default window or display scan.

    A valid permit is an owner attestation, not proof of physical prerequisites.
    Initially shows target-confirmation text. C confirms; each separate Space or
    Right press advances once. Escape closes. Every frame keeps native pixels.
    """
    if type(permit) is not HardwarePermit:
        raise TypeError("A concrete hardware permit is required")
    permit.require("present")
    _validate_position(x, y)
    validate_plan_sequence(permit.plan, sequence)
    if not callable(log):
        raise TypeError("A durable audit callback is required")
    if platform != "win32":
        raise RuntimeError("The physical presenter supports Windows only")
    log("presenter_open_intent", hardware=True, x=x, y=y, width=WIDTH, height=HEIGHT,
        sequence=sequence, plan=permit.plan, revision=permit.revision)
    window = _open_window(x, y)
    PresenterController(window, sequence, log).run()


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

    def check(hwnd: int, x: int, y: int) -> None:
        if not user32.AreDpiAwarenessContextsEqual(user32.GetThreadDpiAwarenessContext(), context):
            raise RuntimeError("Per-monitor V2 DPI awareness changed during presentation")
        client, origin = wintypes.RECT(), wintypes.POINT(0, 0)
        if not user32.GetClientRect(hwnd, ctypes.byref(client)) or not user32.ClientToScreen(
            hwnd, ctypes.byref(origin)
        ):
            raise RuntimeError("Cannot verify physical client rectangle")
        if (client.left, client.top, client.right, client.bottom, origin.x, origin.y) != (
            0, 0, WIDTH, HEIGHT, x, y
        ):
            raise RuntimeError("Native client geometry changed; no scaling fallback")
        monitor = user32.MonitorFromWindow(hwnd, 0)  # No nearest-monitor fallback.
        info = MonitorInfo()
        info.cbSize = ctypes.sizeof(info)
        if not monitor or not user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            raise RuntimeError("Cannot verify the selected window's monitor")
        area = info.rcMonitor
        if (area.left, area.top, area.right, area.bottom) != (x, y, x + WIDTH, y + HEIGHT):
            raise RuntimeError("Window must exactly cover one native 3840x2160 monitor")

    return check


def _open_window(x: int, y: int):
    check = _native_geometry()  # Must precede Tk/window creation.
    import tkinter as tk
    return _TkWindow(tk, check, x, y)


class _TkWindow:
    def __init__(self, tk, geometry_check, x: int, y: int) -> None:
        self.tk, self.geometry_check, self.x, self.y = tk, geometry_check, x, y
        self.root = tk.Tk()
        self.closed = False
        self.image = None
        try:
            self.root.withdraw()
            self.root.overrideredirect(True)
            self.root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
            self.root.configure(background="black", cursor="none")
            self.root.resizable(False, False)
            self.label = tk.Label(self.root, background="black", foreground="white",
                                  borderwidth=0, highlightthickness=0, padx=0, pady=0,
                                  text="Check the intended 3840x2160 screen.\n"
                                       "C: confirm target. Space/Right: next pattern. Esc: stop.\n"
                                       "No reading while this confirmation is visible.")
            self.label.place(x=0, y=0, width=WIDTH, height=HEIGHT)
            self.root.deiconify()
            self.root.update_idletasks()
            self.check_geometry()
            self.root.focus_set()
        except Exception:
            self.close()
            raise

    def check_geometry(self) -> None:
        if self.closed:
            raise RuntimeError("Presenter window is closed")
        self.geometry_check(self.root.winfo_id(), self.x, self.y)

    def confirm(self) -> None:
        self.label.configure(text="")

    def show(self, frame) -> None:
        self.check_geometry()
        payload = b"P6\n3840 2160\n255\n" + frame.pixels
        image = self.tk.PhotoImage(master=self.root, data=payload, format="PPM", gamma=1.0)
        if (image.width(), image.height()) != (WIDTH, HEIGHT):
            raise RuntimeError("Tk image dimensions differ from the native frame")
        self.label.configure(text="", image=image)
        self.image = image  # Tk needs a live Python reference to retain pixels.
        self.root.update_idletasks()
        self.check_geometry()

    def bind(self, press, release, close) -> None:
        self.root.bind("<KeyPress>", lambda event: press(event.keysym))
        self.root.bind("<KeyRelease>", lambda event: release(event.keysym))
        self.root.protocol("WM_DELETE_WINDOW", close)

    def mainloop(self) -> None:
        self.root.mainloop()

    def schedule(self, milliseconds: int, callback) -> None:
        self.root.after(milliseconds, callback)

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            self.image = None
            self.root.destroy()
