"""One-command, in-memory audit of synthetic Ex-Link traffic through close.

Candidate bytes come from the proposed T-006 plan, not captured TV traffic.
This module has no transport or device option. An ACK is never setting/menu
evidence. Even a closed successful audit proves only the supplied fixture.
"""

from dataclasses import dataclass, field
from enum import Enum

from .exlink import ProtocolError, Reply, ReplyParser
from .simulation import FakeClock


class CandidateCommand(Enum):
    EXIT = bytes((8, 34, 13, 0, 0, 45, 156))
    CONTRAST94 = bytes((8, 34, 11, 2, 0, 94, 107))
    RESTORE95 = bytes((8, 34, 11, 2, 0, 95, 106))


class AuditStatus(Enum):
    NEW = "no synthetic command submitted"
    PENDING = "waiting for a supplied reply"
    ACK = "synthetic ACK; not setting or menu evidence"
    NACK = "synthetic NACK"
    UNKNOWN = "unknown or invalid synthetic outcome"
    CANCELLED = "cancelled; receive audit remains open"


@dataclass(frozen=True)
class AuditEvent:
    timestamp_ms: int
    kind: str
    data: bytes
    detail: str
    simulated: bool = field(default=True, init=False)


def _integer(value: int, minimum: int, maximum: int, name: str) -> None:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(name + " is outside its integer range")


class SenderAudit:
    """Manually fed audit, accepting exactly one allowlisted fixture command.

    `feed` timestamps arrival at the current fake clock; no implicit replay,
    drain interval or real close guarantee exists. ACK remains provisional
    until explicit close. Stopping does not stop receipt logging. On resource
    overflow, a prefix and an overflow marker are retained; `log_complete`
    becomes false and `dropped_bytes` counts data omitted through close.
    Two event slots are reserved for overflow and close, within max_events.
    """

    def __init__(self, clock: FakeClock, *, deadline_ms: int = 2000,
                 max_bytes: int = 4096, max_events: int = 256) -> None:
        if type(clock) is not FakeClock:
            raise TypeError("Only the concrete in-memory FakeClock is supported")
        _integer(deadline_ms, 1, 3_600_000, "Reply deadline")
        _integer(max_bytes, 7, 65_536, "Audit byte limit")
        _integer(max_events, 4, 1024, "Audit event limit")
        self._clock = clock
        self._deadline_ms, self._max_bytes, self._max_events = deadline_ms, max_bytes, max_events
        self._events: list[AuditEvent] = []
        self._status = AuditStatus.NEW
        self._closed = False
        self._closed_ms: int | None = None
        self._command: CandidateCommand | None = None
        self._log_complete = True
        self._retained_bytes = 0
        self._dropped_bytes = 0
        self._started_ms = 0
        self._parser = ReplyParser()
        self._append("open", b"", "simulation only; no port opened")

    @property
    def status(self) -> AuditStatus:
        return self._status

    @property
    def clock(self) -> FakeClock:
        return self._clock

    @property
    def command(self) -> CandidateCommand | None:
        return self._command

    @property
    def closed_ms(self) -> int | None:
        return self._closed_ms

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        return tuple(self._events)

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def log_complete(self) -> bool:
        return self._log_complete

    @property
    def dropped_bytes(self) -> int:
        return self._dropped_bytes

    @property
    def accepted(self) -> bool:
        """Only a closed, complete synthetic ACK audit; not hardware evidence."""
        return self._closed and self._log_complete and self._status is AuditStatus.ACK

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("The simulated audit is closed")

    def _append(self, kind: str, data: bytes, detail: str) -> bool:
        if not self._log_complete:
            self._dropped_bytes += len(data)
            return False
        available = self._max_bytes - self._retained_bytes
        if len(data) > available or len(self._events) >= self._max_events - 2:
            prefix = data[:available]
            self._events.append(AuditEvent(self._clock.milliseconds, "overflow", prefix,
                                          "incomplete audit while recording " + kind))
            self._retained_bytes += len(prefix)
            self._dropped_bytes += len(data) - len(prefix)
            self._log_complete = False
            self._status = AuditStatus.UNKNOWN
            return False
        self._events.append(AuditEvent(self._clock.milliseconds, kind, data, detail))
        self._retained_bytes += len(data)
        return True

    def _set_status(self, status: AuditStatus, reason: str) -> None:
        if self._log_complete:
            self._status = status
            self._append("status", b"", reason)

    def submit(self, command: CandidateCommand, accepted_bytes: int = 7) -> None:
        if type(command) is not CandidateCommand:
            raise TypeError("Only a named T-006 candidate fixture is supported")
        _integer(accepted_bytes, 0, 7, "Synthetic accepted byte count")
        self._require_open()
        if self._status is not AuditStatus.NEW:
            raise RuntimeError("Only one command is permitted; no retry or restart")
        self._started_ms = self._clock.milliseconds
        self._command = command
        self._status = AuditStatus.PENDING
        if not self._append("write", command.value,
                            "requested 7 bytes; synthetic accepted " + str(accepted_bytes)):
            return
        if accepted_bytes != 7:
            self._set_status(AuditStatus.UNKNOWN, "partial synthetic write; no retry")

    def feed(self, data: bytes) -> None:
        if type(data) is not bytes:
            raise TypeError("Supplied traffic must be immutable bytes")
        self._require_open()
        self.poll()
        if not data:
            return
        if not self._append("receive", data, "supplied synthetic bytes"):
            return
        if self._status is AuditStatus.NEW:
            self._set_status(AuditStatus.UNKNOWN, "unsolicited bytes before the command")
            return
        if self._status is AuditStatus.ACK:
            self._set_status(AuditStatus.UNKNOWN, "unexpected bytes after provisional ACK")
            return
        if self._status is not AuditStatus.PENDING:
            return
        try:
            replies = self._parser.feed(data)
        except ProtocolError as error:
            self._set_status(AuditStatus.UNKNOWN, str(error))
            return
        if len(replies) > 1 or (replies and self._parser.buffered_bytes):
            self._set_status(AuditStatus.UNKNOWN, "duplicate reply or trailing bytes")
        elif replies:
            status = AuditStatus.ACK if replies[0] is Reply.ACK else AuditStatus.NACK
            self._set_status(status, status.value)

    def poll(self) -> AuditStatus:
        if not self._closed and self._status is AuditStatus.PENDING:
            if self._clock.milliseconds - self._started_ms >= self._deadline_ms:
                self._set_status(AuditStatus.UNKNOWN, "exclusive reply deadline reached")
        return self._status

    def cancel(self) -> None:
        self._require_open()
        if self._status in (AuditStatus.NEW, AuditStatus.PENDING, AuditStatus.ACK):
            self._set_status(AuditStatus.CANCELLED, "cancelled; retain supplied traffic until close")

    def close(self) -> None:
        if self._closed:
            return
        self.poll()
        if self._status in (AuditStatus.NEW, AuditStatus.PENDING):
            reason = "closed without a complete reply"
            try:
                self._parser.finish()
            except ProtocolError as error:
                reason = str(error)
            self._set_status(AuditStatus.UNKNOWN, reason)
        self._closed = True
        self._closed_ms = self._clock.milliseconds
        self._events.append(AuditEvent(self._clock.milliseconds, "close", b"",
                                      "simulated close; no port or later-input guarantee"))
