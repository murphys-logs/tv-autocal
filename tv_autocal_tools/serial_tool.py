"""Five manually requested T-006 frames, with one continuous bounded audit.

Importing this module opens nothing. The Windows/pySerial backend is reached
only through run_serial after an explicit permit and prerequisite attestation.
No successful reply establishes command attribution, a changed setting, or
electrical compatibility. The proposed timing policies need plan review.
"""

from dataclasses import dataclass
from re import fullmatch

from tv_autocal.exlink import ProtocolError, Reply, ReplyParser
from tv_autocal.sender_audit import CandidateCommand
from .permission import HardwarePermit


@dataclass(frozen=True)
class SerialResult:
    completed: bool
    closed: bool
    log_complete: bool
    reason: str
    writes: int
    received_bytes: int
    omitted_bytes: int
    evidence_pairs: tuple[tuple[int | None, int, int], ...]
    purpose: str = "component diagnostic only; not calibration or electrical proof"

    @property
    def accepted(self) -> bool:
        return self.completed and self.closed and self.log_complete


def _integer(value: int, low: int, high: int, name: str) -> None:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(name + " is outside the permitted integer range")


class SerialSession:
    """Pure state machine; caller supplies time, operator observations and bytes.

    operator() records intent before returning one fixed frame. write_done()
    records the count and starts the reply deadline after the complete write.
    No method dispatches bytes. Logging continues after stop until close.
    """

    def __init__(self, log, *, menu_window_ms: int, reply_ms: int = 2000,
                 quiet_ms: int = 500, settle_ms: int = 2000,
                 session_ms: int = 120000, initial_ms: int = 5000,
                 max_bytes: int = 65536, max_events: int = 2048) -> None:
        for name, value, low, high in (
            ("menu window", menu_window_ms, 1, 60000),
            ("reply timeout", reply_ms, 1, 10000),
            ("quiet interval", quiet_ms, 1, 5000),
            ("settling interval", settle_ms, 1, 60000),
            ("session limit", session_ms, 1, 600000),
            ("initial interval", initial_ms, 1, 10000),
            ("receive byte limit", max_bytes, 96, 65536),
            ("event limit", max_events, 32, 4096),
        ):
            _integer(value, low, high, name)
        if not callable(log):
            raise TypeError("An audit callback is required")
        self.log = log
        self.menu_window_ms, self.reply_ms = menu_window_ms, reply_ms
        self.quiet_ms, self.settle_ms, self.session_ms = quiet_ms, settle_ms, session_ms
        self.initial_ms, self.max_bytes, self.max_events = initial_ms, max_bytes, max_events
        self.phase = "initial quiet"
        self.reason = "session incomplete"
        self.log_complete = True
        self.closed = False
        self.writes = self.received_bytes = self.omitted_bytes = self._events = 0
        self._now = self._last_receive = self._deadline = self._ack_ms = 0
        self._settle_until = 0
        self._next_phase = ""
        self._menu_opened: int | None = None
        self._observation_generation: int | None = None
        self._setter_id: int | None = None
        self._pending: CandidateCommand | None = None
        self._parser = ReplyParser()
        self._pairs: list[tuple[int | None, int, int]] = []
        self._emit("serial_session", policy="five manual commands only", initial_ms=initial_ms,
                   reply_ms=reply_ms, quiet_ms=quiet_ms, settle_ms=settle_ms,
                   menu_window_ms=menu_window_ms, session_ms=session_ms)

    def _emit(self, kind: str, **fields) -> bool:
        if not self.log_complete:
            return False
        try:
            if self._events >= self.max_events - 2:
                self.log("serial_overflow", elapsed_ms=self._now,
                         reason="event limit; subsequent evidence incomplete")
                self.log_complete = False
                self.phase, self.reason = "stopped", "audit event capacity exceeded"
                return False
            self.log(kind, elapsed_ms=self._now, **fields)
            self._events += 1
            return True
        except Exception:
            self.log_complete = False
            self.phase, self.reason = "stopped", "audit write failed"
            return False

    def tick(self, now: int) -> None:
        _integer(now, self._now, 2**63 - 1, "monotonic elapsed time")
        self._now = now
        if self.closed or self.phase == "stopped":
            return
        if now >= self.session_ms:
            self.stop("session deadline reached")
        elif self.phase == "initial quiet" and now >= self.initial_ms:
            self.phase = "baseline"
            self._emit("serial_ready", next="b: confirm fresh baseline 95 and menu opening")
        elif self.phase == "reply" and now >= self._deadline:
            self.stop("exclusive reply deadline reached")
        elif self.phase == "ack quiet" and now >= self._ack_ms + self.quiet_ms:
            self.phase = "confirm exit" if self._pending is CandidateCommand.EXIT else "menu preparation"
            self._emit("serial_ack_window_complete", command_id=self.writes, next=self.phase)
        elif self.phase == "settling" and now >= self._settle_until:
            self.phase = self._next_phase
            if self.phase == "complete":
                self.reason = "five replies and owner observations complete; closure still pending"
            self._emit("serial_settled", next=self.phase)

    def receive(self, data: bytes, now: int) -> None:
        if self.closed:
            raise RuntimeError("Session is closed")
        if type(data) is not bytes or len(data) > ReplyParser.MAX_CHUNK:
            raise ValueError("Receive calls require at most 96 immutable bytes")
        self.tick(now)
        if not data:
            return
        self.received_bytes += len(data)
        self._last_receive = now
        room = max(0, self.max_bytes - (self.received_bytes - len(data)))
        kept = data[:room]
        if not self._emit("serial_receive", data_hex=kept.hex(), command_id=self.writes or None,
                          phase=self.phase):
            self.omitted_bytes += len(data)
        elif len(kept) != len(data):
            self.omitted_bytes += len(data) - len(kept)
            self._emit("serial_overflow", reason="receive byte capacity exceeded")
            self.log_complete = False
            self.phase, self.reason = "stopped", "receive byte capacity exceeded"
        if self.phase == "stopped":
            return
        if self.phase != "reply":
            self.stop("bytes outside the active reply window")
            return
        try:
            replies = self._parser.feed(data)
        except ProtocolError as error:
            self.stop(str(error))
            return
        if len(replies) > 1 or (replies and self._parser.buffered_bytes):
            self.stop("duplicate reply or trailing bytes")
        elif replies:
            if replies[0] is not Reply.ACK:
                self.stop("negative reply")
            else:
                self._ack_ms = now
                self.phase = "ack quiet"
                self._emit("serial_provisional_ack", command_id=self.writes)

    def operator(self, key: str, now: int) -> bytes | None:
        """Handle a single explicit key; any returned frame must be written once."""
        self.tick(now)
        if self.closed or self.phase == "stopped":
            raise RuntimeError("No action after stop or close")
        if key == "b" and self.phase == "baseline":
            self._emit("serial_owner_observation", value=95, generation=self.writes,
                       meaning="fresh baseline before initial EXIT test")
            if self.log_complete:
                self.phase = "menu preparation"
            return None
        if key == "m" and self.phase == "menu preparation":
            self._menu_opened = now
            self._emit("serial_menu_opening_boundary", before_opening_ms=now,
                       meaning="owner presses m before opening the ordinary menu")
            if self.log_complete:
                self.phase = "observe setting"
            return None
        if key == "o" and self.phase == "observe setting":
            if self._menu_opened is None or now - self._menu_opened >= self.menu_window_ms:
                self.stop("menu automatic-close exclusion interval expired")
                return None
            value = 94 if self._pending is CandidateCommand.CONTRAST94 else 95
            if self._pending in (CandidateCommand.CONTRAST94, CandidateCommand.RESTORE95):
                self._setter_id = self.writes
            self._observation_generation = self.writes
            self._emit("serial_owner_observation", value=value, generation=self.writes,
                       menu_opening_boundary_ms=self._menu_opened, setter_id=self._setter_id,
                       meaning="owner inspected exact value and no unexpected change")
            if self.log_complete:
                self.phase = "exit ready"
            return None
        if key == "c" and self.phase == "confirm exit":
            if self._menu_opened is None or now - self._menu_opened >= self.menu_window_ms:
                self.stop("menu automatic-close exclusion interval expired")
                return None
            self._pairs.append((self._setter_id, self.writes, now))
            self._emit("serial_owner_exit", setter_id=self._setter_id, exit_id=self.writes,
                       menu_opening_boundary_ms=self._menu_opened, closure_confirmed_ms=now,
                       meaning="owner confirms closure within reviewed exclusion interval")
            self._menu_opened = self._observation_generation = None
            self._next_phase = {1: "set ready", 3: "restore ready", 5: "complete"}[self.writes]
            self._settle_until = now + self.settle_ms
            if self.log_complete:
                self.phase = "settling"
            return None
        command = None
        if key == "e" and self.phase == "exit ready":
            if self._observation_generation != self.writes or self._menu_opened is None:
                self.stop("fresh menu observation is required")
                return None
            if now - self._menu_opened >= self.menu_window_ms:
                self.stop("menu automatic-close exclusion interval expired")
                return None
            command = CandidateCommand.EXIT
        elif key == "d" and self.phase == "set ready":
            command = CandidateCommand.CONTRAST94
        elif key == "r" and self.phase == "restore ready":
            command = CandidateCommand.RESTORE95
        if command is None:
            raise ValueError("Key is not permitted in the current phase")
        expected = (CandidateCommand.EXIT, CandidateCommand.CONTRAST94, CandidateCommand.EXIT,
                    CandidateCommand.RESTORE95, CandidateCommand.EXIT)
        if self.writes >= len(expected) or command is not expected[self.writes]:
            self.stop("command sequence limit")
            return None
        # The generation is invalidated before any write, even if the write fails.
        self._observation_generation = None
        self.writes += 1
        self._pending = command
        self.phase = "writing"
        if not self._emit("serial_write_intent", command_id=self.writes, command=command.name,
                          data_hex=command.value.hex(), setter_id=self._setter_id):
            return None
        return command.value

    def write_done(self, count: int | None, now: int) -> None:
        was_writing = self.phase == "writing"
        self.tick(now)
        if not was_writing:
            raise RuntimeError("No write is pending")
        self._emit("serial_write_result", command_id=self.writes, accepted_bytes=count,
                   requested_bytes=7)
        if self.phase == "stopped":
            return
        if type(count) is not int or count != 7:
            self.stop("partial or indeterminate write; no retry")
        elif self.log_complete:
            self._deadline = now + self.reply_ms
            self._parser = ReplyParser()
            self.phase = "reply"

    def write_may_start(self, now: int) -> bool:
        """Recheck timing after durable intent logging, immediately before write."""
        self.tick(now)
        if self.phase != "writing" or not self.log_complete:
            return False
        if self._pending is CandidateCommand.EXIT and (
            self._menu_opened is None or now - self._menu_opened >= self.menu_window_ms
        ):
            self.stop("menu exclusion interval expired before actual write")
            return False
        return True

    def stop(self, reason: str) -> None:
        if self.closed:
            return
        if self.phase != "stopped":
            self.phase, self.reason = "stopped", reason
            self._observation_generation = None
            self._emit("serial_stop", reason=reason, automatic_restore=False)

    def finish_close(self, *, closed: bool) -> SerialResult:
        complete = self.phase == "complete" and self.log_complete and closed
        self.closed = closed
        if not closed:
            self.reason = "port closure failed; prior outcome: " + self.reason
        if not complete and self.phase != "stopped":
            self.phase, self.reason = "stopped", "closed before complete sequence" if closed else "port closure failed"
        try:
            self.log("serial_close", elapsed_ms=self._now, closed=closed,
                     log_complete=self.log_complete, received_bytes=self.received_bytes,
                     omitted_bytes=self.omitted_bytes, completed=complete)
        except Exception:
            self.log_complete, complete = False, False
            self.reason = "closure evidence could not be logged"
        return SerialResult(complete, closed, self.log_complete, self.reason, self.writes,
                            self.received_bytes, self.omitted_bytes, tuple(self._pairs))


class _WindowsRuntime:
    """Lazy boundary; no constructor is reached by simulation or default CLI."""

    def __init__(self, port: str) -> None:
        import sys
        if sys.platform != "win32":
            raise RuntimeError("The physical sender supports Windows only")
        import serial
        import msvcrt
        import time
        if getattr(serial, "VERSION", None) != "3.5":
            raise RuntimeError("Reviewed dependency pySerial 3.5 is required")
        self._console, self._time = msvcrt, time
        self.port = serial.Serial(port=None, baudrate=9600, bytesize=8, parity="N", stopbits=1,
                                  timeout=0, write_timeout=1, xonxoff=False,
                                  rtscts=False, dsrdtr=False)
        self.port.dtr = False
        self.port.rts = False
        self.port.port = port
        self._origin = time.monotonic_ns()

    def now(self) -> int:
        return (self._time.monotonic_ns() - self._origin) // 1_000_000

    def open(self) -> None:
        self.port.open()
        # Initial silence is measured after the OS open has completed.
        self._origin = self._time.monotonic_ns()

    def key(self) -> str | None:
        if not self._console.kbhit():
            return None
        key = self._console.getwch()
        if key in ("\x00", "\xe0"):
            # msvcrt returns special keys as a prefix followed by a keycode.
            # The code may spell a command, but it is not an owner action.
            self._console.getwch()
            return None
        return key if key in {"b", "m", "o", "e", "c", "d", "r", "q"} else None

    def pause(self) -> None:
        self._time.sleep(0.01)


def run_serial(permit: HardwarePermit, *, port: str, log, prerequisites_confirmed: bool,
               menu_window_ms: int, reply_ms: int = 2000, quiet_ms: int = 500,
               settle_ms: int = 2000, close_ms: int = 500,
               session_ms: int = 120000) -> SerialResult:
    """Future owner-run T-006 session. Never call during software-only work.

    prerequisites_confirmed attests electrical and scope/restoration evidence,
    reviewed menu timing, owner presence, and all measurement/discovery programs
    closed. It is an attestation, not evidence that those prerequisites are true.
    Closing drains for a bounded interval; it cannot promise no bytes after OS
    closure or prove reply attribution. No resets, flushes or recovery sends.
    """
    if type(permit) is not HardwarePermit:
        raise TypeError("An explicit HardwarePermit is required")
    permit.require("serial")
    if prerequisites_confirmed is not True:
        raise PermissionError("T-006 electrical, scope, timing and isolation prerequisites are required")
    if type(port) is not str or fullmatch(r"COM[1-9][0-9]{0,3}", port) is None:
        raise ValueError("Use one explicitly identified COM name; URLs/scans are forbidden")
    _integer(close_ms, 1, 5000, "close drain interval")
    session = SerialSession(log, menu_window_ms=menu_window_ms, reply_ms=reply_ms,
                            quiet_ms=quiet_ms, settle_ms=settle_ms, session_ms=session_ms)
    if not session.log_complete:
        return session.finish_close(closed=True)
    # Log and validate everything before constructing/opening the physical port.
    if not session._emit("serial_open_intent", port=port, profile="9600 8N1", dtr=False,
                         rts=False, plan=permit.plan, revision=permit.revision):
        return session.finish_close(closed=True)
    try:
        runtime = _WindowsRuntime(port)
    except Exception as error:
        session.stop("serial backend unavailable: " + type(error).__name__)
        return session.finish_close(closed=True)
    opened = False
    closing_at: int | None = None
    closed = False
    try:
        runtime.open()
        opened = True
        session._emit("serial_opened", dependency="pySerial 3.5")
        print("T-006 manual sender: b=baseline95; m=before opening ordinary menu; "
              "o=observed expected value; e=EXIT; c=confirmed exit; "
              "d=Contrast94; r=restore95; q=close. "
              "No recovery sends after a stop. Watch the logged phase.")
        last_phase = ""
        while True:
            data = runtime.port.read(ReplyParser.MAX_CHUNK)
            # Timestamp observed delivery after read returns. Even a nominally
            # nonblocking OS call can cross the exclusive reply deadline.
            now = runtime.now()
            session.receive(data, now)
            if session.phase != last_phase:
                print("Phase:", session.phase, "—", session.reason)
                last_phase = session.phase
            if session.phase == "stopped" and closing_at is None:
                closing_at = now
            if closing_at is None:
                key = runtime.key()
                if key == "q":
                    if session.phase != "complete":
                        session.stop("owner stopped; manual restoration only under the plan")
                    closing_at = now
                elif key is not None:
                    # Console handling and durable audit writes can take time.
                    # Observe newly queued bytes and fresh time before dispatch.
                    session.receive(runtime.port.read(ReplyParser.MAX_CHUNK), runtime.now())
                    if session.phase == "stopped":
                        closing_at = runtime.now()
                        continue
                    try:
                        frame = session.operator(key, runtime.now())
                    except ValueError:
                        print("Key unavailable in this phase; nothing sent.")
                    else:
                        if frame is not None and session.write_may_start(runtime.now()):
                            count = runtime.port.write(frame)
                            session.write_done(count, runtime.now())
            # Final draining is performed exactly once below, including faults.
            if closing_at is not None:
                break
            runtime.pause()
    except KeyboardInterrupt:
        session.stop("owner interrupted; no recovery send")
    except Exception as error:
        session.stop("serial operation failed: " + type(error).__name__)
    finally:
        if opened:
            # A bounded final drain also covers exceptional/cancelled paths.
            # No reset_input_buffer/flush call discards evidence before close.
            start = runtime.now()
            try:
                while runtime.now() - start < close_ms:
                    session.receive(runtime.port.read(ReplyParser.MAX_CHUNK), runtime.now())
                    runtime.pause()
                session.receive(runtime.port.read(ReplyParser.MAX_CHUNK), runtime.now())
            except (Exception, KeyboardInterrupt):
                session.stop("final receive drain failed or was interrupted")
        try:
            runtime.port.close()
            closed = True
        except Exception:
            session.stop("port closure failed; owner must inspect before further work")
    return session.finish_close(closed=closed)
