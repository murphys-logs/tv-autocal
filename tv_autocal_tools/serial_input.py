"""Lazy serial controls: bounded console stop events and mouse-only actions.

Nothing native is imported or constructed until the explicitly armed runtime
asks for it. Text is never an input route for a TV action: Windows can turn
clipboard text into otherwise ordinary-looking console key events.
"""


class ConsoleStop:
    """Consume at most 32 complete INPUT_RECORDs, never wait for a suffix."""

    def __init__(self) -> None:
        import ctypes
        # Windows wire types, independent of the machine running our fakes.
        # wchar_t/long follow the HOST ABI on LP64 Unix and are not Win32 types.
        BOOL, WORD, DWORD = ctypes.c_int32, ctypes.c_uint16, ctypes.c_uint32
        HANDLE = ctypes.c_void_p

        class Character(ctypes.Union):
            _fields_ = [("UnicodeChar", WORD), ("AsciiChar", ctypes.c_char)]

        class KeyEvent(ctypes.Structure):
            _fields_ = [("bKeyDown", BOOL), ("wRepeatCount", WORD),
                        ("wVirtualKeyCode", WORD), ("wVirtualScanCode", WORD),
                        ("uChar", Character), ("dwControlKeyState", DWORD)]

        class Event(ctypes.Union):
            # MOUSE_EVENT_RECORD is also 16 bytes, the largest event member.
            _fields_ = [("KeyEvent", KeyEvent), ("other", ctypes.c_byte * 16)]

        class InputRecord(ctypes.Structure):
            _fields_ = [("EventType", WORD), ("Event", Event)]

        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetStdHandle.argtypes = [DWORD]
        kernel.GetStdHandle.restype = HANDLE
        kernel.GetConsoleMode.argtypes = [HANDLE, ctypes.POINTER(DWORD)]
        kernel.GetConsoleMode.restype = BOOL
        kernel.ReadConsoleInputExW.argtypes = [HANDLE, ctypes.POINTER(InputRecord),
                                             DWORD, ctypes.POINTER(DWORD), WORD]
        kernel.ReadConsoleInputExW.restype = BOOL
        self.handle = kernel.GetStdHandle(-10 & 0xffffffff)  # STD_INPUT_HANDLE
        mode = DWORD()
        if not kernel.GetConsoleMode(self.handle, ctypes.byref(mode)):
            raise RuntimeError("An attached Windows console input buffer is required")
        # Do not change console modes. Processed Ctrl+C remains a Python stop;
        # redirected stdin and virtual-terminal stream mode are unsupported.
        if not mode.value & 1 or mode.value & 0x0200:
            raise RuntimeError("Processed console input without VT input is required")
        self._read = kernel.ReadConsoleInputExW
        self._ctypes, self._dword = ctypes, DWORD
        self._records = (InputRecord * 32)()

    def poll(self) -> bool:
        count = self._dword()
        # Documented CONSOLE_READ_NOWAIT removes available events and returns
        # immediately even when empty; no peek/read race or second read.
        if not self._read(self.handle, self._records, len(self._records),
                          self._ctypes.byref(count), 0x0002):
            raise RuntimeError("Console event read failed")
        if count.value > len(self._records):
            raise RuntimeError("Console returned an invalid event count")
        return any(self.is_quit(record) for record in self._records[:count.value])

    @staticmethod
    def is_quit(record) -> bool:
        if record.EventType != 1:  # KEY_EVENT, not mouse/focus/resize/menu.
            return False
        key = record.Event.KeyEvent
        return (bool(key.bKeyDown) and key.wRepeatCount > 0
                and key.wVirtualKeyCode == 0x51 and key.uChar.UnicodeChar == 0x0071
                and not key.dwControlKeyState & 0x011f)


class MouseControls:
    """One bounded Tk event turn; no keyboard/class button activation."""

    ACTIONS = {"baseline": ("b", "Observed fresh baseline 95"),
               "menu preparation": ("m", "Before opening ordinary menu"),
               "observe setting": ("o", "Observed expected setting"),
               "exit ready": ("e", "Send EXIT"),
               "confirm exit": ("c", "Confirmed menu exit"),
               "set ready": ("d", "Send Contrast 94"),
               "restore ready": ("r", "Send restore 95")}

    def __init__(self, tk, *, x: int, y: int) -> None:
        self._phase = None
        self._ready = False
        self._pressed = self._pending = None
        self._multiple = self._stopped = self.closed = False
        self._error = None
        self.root = tk.Tk()
        try:
            self.root.withdraw()
            self.root.report_callback_exception = self._callback_error
            self.root.title("TV autocal — serial controls")
            self.root.geometry(f"+{x}+{y}")
            self.root.resizable(False, False)
            self.root.protocol("WM_DELETE_WINDOW", self.stop)
            self.root.bind("<KeyPress>", self._key)
            self.root.bind("<KeyRelease>", lambda event: "break")
            tk.Label(self.root, text="Mouse controls only. Typing/paste sends nothing.\n"
                     "q or Stop closes; no automatic recovery.").pack(padx=12, pady=8)
            self.buttons = {}
            self._button_states = {}
            for key, label in [*self.ACTIONS.values(), ("q", "Stop / close")]:
                state = "normal" if key == "q" else "disabled"
                button = tk.Button(self.root, text=label, takefocus=False, state=state)
                # Remove the Button/toplevel/all binding tags entirely. This
                # excludes Space, Return, <<Invoke>>, accelerators and paste.
                button.bindtags((str(button),))
                button.bind("<ButtonPress-1>", lambda event, k=key: self._down(k))
                button.bind("<ButtonRelease-1>", lambda event, k=key: self._up(k, event))
                button.bind("<KeyPress>", self._key)
                button.bind("<KeyRelease>", lambda event: "break")
                button.pack(fill="x", padx=12, pady=3)
                self.buttons[key] = button
                self._button_states[key] = state
            self.root.deiconify()
        except BaseException:
            self.root.destroy()
            raise

    def _callback_error(self, kind, error, trace) -> None:
        self._error = error
        self.stop()

    def _key(self, event):
        if event.char == "q":
            self.stop()
        return "break"

    def stop(self) -> None:
        self._stopped = True
        self._pressed = self._pending = None

    def _allowed(self, key) -> bool:
        return key == "q" or (self.ready and self._phase in self.ACTIONS
                              and key == self.ACTIONS[self._phase][0])

    def _down(self, key) -> str:
        if key == "q":
            self.stop()  # Stop does not depend on a later release or phase.
            return "break"
        self._pressed = (key, self._phase) if self._allowed(key) else None
        return "break"

    def _up(self, key, event) -> str:
        pressed, self._pressed = self._pressed, None
        if (pressed == (key, self._phase) and self._allowed(key)
                and 0 <= event.x < event.widget.winfo_width()
                and 0 <= event.y < event.widget.winfo_height()):
            if key == "q":
                self.stop()
            elif self._pending is not None:
                self._multiple = True  # Never queue a pasted/rapid action series.
            else:
                self._pending = key
        return "break"

    @property
    def ready(self) -> bool:
        return self._ready and not self._stopped and not self.closed

    def _display_states(self) -> None:
        for key, button in self.buttons.items():
            state = "normal" if self._allowed(key) else "disabled"
            if state != self._button_states[key]:
                button.configure(state=state)
                self._button_states[key] = state

    def _disarm(self) -> None:
        self._ready = False
        self._pressed = self._pending = None
        self._multiple = False
        self._display_states()

    def poll(self, phase: str) -> str | None:
        if self.closed:
            raise RuntimeError("Serial controls are closed")
        if self._stopped:
            return "q"
        changed = phase != self._phase
        if changed:
            self._phase = phase
            self._disarm()
        self._multiple = False
        # Tcl_DoOneEvent DONT_WAIT=2. Each callback only latches intent; no
        # update()/mainloop() drains an unbounded pending input stream.
        for _ in range(32):
            if not self.root.tk.dooneevent(2):
                break
        else:
            # A batch includes redraw/map/focus work, not just user input.
            # Discard action intent and continue bounded draining next poll;
            # ordinary traffic alone must not abort after a TV adjustment.
            self._disarm()
            if self._error is not None:
                raise self._error
            return "q" if self._stopped else None
        if self._error is not None:
            raise self._error
        if self._stopped:
            return "q"
        if not self._ready:
            # Startup, phase changes and backlog must reach observed idle
            # while disabled. Require a fresh click after re-enabling.
            self._pressed = self._pending = None
            self._ready = True
            self._display_states()
            return None
        pending, self._pending = self._pending, None
        return None if self._multiple else pending

    def close(self) -> None:
        if not self.closed:
            self.stop()
            self.root.destroy()
            self.closed = True
