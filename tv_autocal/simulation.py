"""One-request in-memory fake sessions. No ports, hosts, clocks or real I/O.

The injected clock is a local integer counter. Scripted replies are literal
bytes supplied by a test, never computed from the command being checked.
"""

from dataclasses import dataclass
from enum import Enum

from .exlink import ProtocolError, Reply, ReplyParser, encode, require_fixture_frame


def _nonnegative_integer(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(name + " must be a nonnegative integer")


class FakeClock:
    """Manually advanced milliseconds; deliberately has no wall-clock calls."""

    def __init__(self) -> None:
        self._milliseconds = 0

    @property
    def milliseconds(self) -> int:
        return self._milliseconds

    def advance(self, milliseconds: int) -> None:
        _nonnegative_integer(milliseconds, "Clock advance")
        self._milliseconds += milliseconds


@dataclass(frozen=True)
class ScriptedReply:
    """Synthetic bytes arriving this many milliseconds after the fake write."""

    after_ms: int
    chunk: bytes

    def __post_init__(self) -> None:
        _nonnegative_integer(self.after_ms, "Reply time")
        if type(self.chunk) is not bytes:
            raise TypeError("Scripted reply must be immutable bytes")


class Outcome(Enum):
    NEW = "not started"
    WAITING = "fake write accepted; waiting"
    ACK = "simulated acknowledgement"
    NACK = "simulated rejection"
    UNKNOWN = "unknown simulated outcome"


@dataclass(frozen=True)
class Evidence:
    """Software evidence only; there is no field asserting a TV state."""

    encoded: bool
    fake_write_accepted: bool
    outcome: Outcome
    reason: str
    simulated: bool = True


class FakeSession:
    """One write, one terminal outcome, then permanently retired.

    No transport can be injected. Unknown constructor keywords (including
    port, host and real_mode) fail in Python before any work occurs. Even a
    successful ACK retires the session; no retry or next request is possible.
    This fake's policy does not solve real serial reply correlation.
    """

    def __init__(
        self,
        clock: FakeClock,
        replies: tuple[ScriptedReply, ...] = (),
        *,
        deadline_ms: int = 2000,
        accepted_bytes: int = 7,
    ) -> None:
        if type(clock) is not FakeClock:
            raise TypeError("Only the in-memory FakeClock is supported")
        if type(replies) is not tuple or any(type(r) is not ScriptedReply for r in replies):
            raise TypeError("Replies must be a tuple of ScriptedReply records")
        _nonnegative_integer(deadline_ms, "Deadline")
        if deadline_ms == 0:
            raise ValueError("Deadline must be positive")
        _nonnegative_integer(accepted_bytes, "Accepted byte count")
        if accepted_bytes > 7:
            raise ValueError("Accepted byte count cannot exceed the seven-byte request")
        if any(a.after_ms > b.after_ms for a, b in zip(replies, replies[1:])):
            raise ValueError("Scripted replies must be ordered by arrival time")
        self._clock = clock
        self._replies = replies
        self._deadline_ms = deadline_ms
        self._accepted_bytes = accepted_bytes
        self._parser = ReplyParser()
        self._started_ms = 0
        self._next_reply = 0
        self._writes: list[bytes] = []
        self._evidence = Evidence(False, False, Outcome.NEW, "")

    @property
    def writes(self) -> tuple[bytes, ...]:
        """Requested fake writes, including a write scripted to be partial."""
        return tuple(self._writes)

    @property
    def evidence(self) -> Evidence:
        return self._evidence

    @property
    def retired(self) -> bool:
        return self._evidence.outcome not in (Outcome.NEW, Outcome.WAITING)

    def _terminal(self, outcome: Outcome, reason: str) -> Evidence:
        self._evidence = Evidence(
            self._evidence.encoded, self._evidence.fake_write_accepted, outcome, reason
        )
        return self._evidence

    def submit(self, cmd1: int, cmd2: int, cmd3: int, value: int) -> Evidence:
        return self.submit_frame(encode(cmd1, cmd2, cmd3, value))

    def submit_frame(self, frame: bytes) -> Evidence:
        if self._evidence.outcome is not Outcome.NEW:
            raise RuntimeError("A fake session permits only one request")
        require_fixture_frame(frame)
        self._evidence = Evidence(True, False, Outcome.NEW, "encoded fixture")
        self._writes.append(frame)
        if self._accepted_bytes != 7:
            return self._terminal(Outcome.UNKNOWN, "partial fake write; never resent")
        self._started_ms = self._clock.milliseconds
        self._evidence = Evidence(True, True, Outcome.WAITING, "fake write accepted")
        return self._evidence

    def receive(self, chunk: bytes) -> Evidence:
        """Direct synthetic delivery at the current fake time, for edge cases."""
        if self._replies:
            raise RuntimeError("Use poll for a scripted session; do not mix delivery modes")
        if self.retired:
            return self._evidence  # Late/duplicate bytes cannot reopen this session.
        if self._evidence.outcome is Outcome.NEW:
            return self._terminal(Outcome.UNKNOWN, "unsolicited bytes before request")
        if self._clock.milliseconds - self._started_ms >= self._deadline_ms:
            return self._terminal(Outcome.UNKNOWN, "deadline reached; reply not attributed")
        return self._receive_before_deadline(chunk)

    def _receive_before_deadline(self, chunk: bytes) -> Evidence:
        try:
            replies = self._parser.feed(chunk)
        except ProtocolError as error:
            return self._terminal(Outcome.UNKNOWN, str(error))
        if len(replies) > 1 or (replies and self._parser.buffered_bytes):
            return self._terminal(Outcome.UNKNOWN, "extra reply bytes in one delivery")
        if replies:
            outcome = Outcome.ACK if replies[0] is Reply.ACK else Outcome.NACK
            return self._terminal(outcome, "literal scripted reply; no TV state verified")
        return self._evidence

    def poll(self) -> Evidence:
        """Deliver due script entries, judging deadlines by recorded arrival time.

        An entry at the deadline is late. If polling is delayed, a complete
        reply scripted before the deadline still counts at its arrival time.
        """
        if self._evidence.outcome is not Outcome.WAITING:
            return self._evidence
        elapsed = self._clock.milliseconds - self._started_ms
        while self._next_reply < len(self._replies):
            reply = self._replies[self._next_reply]
            if reply.after_ms > elapsed or reply.after_ms >= self._deadline_ms:
                break
            self._next_reply += 1
            self._receive_before_deadline(reply.chunk)
            if self.retired:
                return self._evidence
        if elapsed >= self._deadline_ms:
            return self._terminal(Outcome.UNKNOWN, "timeout; no complete reply before deadline")
        return self._evidence

    def cancel(self) -> Evidence:
        if not self.retired:
            return self._terminal(Outcome.UNKNOWN, "cancelled; never resent")
        return self._evidence
