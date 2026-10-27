"""Bounded Ex-Link fixture encoder and reply parser, with no I/O.

Protocol references and limits: docs/software/t009-prototype.md.
The allowlist is a software-fixture list, never permission to send to a TV.
"""

from enum import Enum


class ProtocolError(ValueError):
    """Invalid bytes, unsupported command, or malformed reply."""


# Only the three published S-005 fixtures. No general-purpose raw encoder.
_FIXTURE_COMMANDS = frozenset(((0, 0, 0, 1), (0, 0, 0, 2), (1, 0, 0, 25)))


def _check_command(command: tuple[int, int, int, int]) -> None:
    if any(type(value) is not int for value in command):
        raise TypeError("Command fields must be integers, not booleans or coercible values")
    if any(not 0 <= value <= 255 for value in command):
        raise ProtocolError("Command fields must be bytes in 0..255")
    if command not in _FIXTURE_COMMANDS:
        raise ProtocolError("Command is outside the software-fixture allowlist")


def encode(cmd1: int, cmd2: int, cmd3: int, value: int) -> bytes:
    """Encode one allowlisted fixture; unknown commands fail before encoding."""
    command = (cmd1, cmd2, cmd3, value)
    _check_command(command)
    payload = bytes((8, 34, *command))
    return payload + bytes((-sum(payload) % 256,))


def validate_frame(frame: bytes) -> tuple[int, int, int, int]:
    """Check structure and checksum ONLY, without assigning command meaning.

    Passing this function does not place a frame on the command allowlist.
    FakeSession.submit_frame applies the allowlist as a separate check.
    """
    if type(frame) is not bytes:
        raise TypeError("Frame must be immutable binary bytes")
    if len(frame) != 7 or frame[:2] != b"\x08\x22":
        raise ProtocolError("Expected seven bytes with header 08 22")
    if sum(frame) % 256:
        raise ProtocolError("Invalid additive checksum")
    return (frame[2], frame[3], frame[4], frame[5])


def require_fixture_frame(frame: bytes) -> bytes:
    """Validate raw bytes and apply the same allowlist used by encode."""
    _check_command(validate_frame(frame))
    return frame


class Reply(Enum):
    ACK = "simulated acknowledgement"
    NACK = "simulated rejection"


class ReplyParser:
    """Strict incremental parser: no noise skipping, queries, or resynchronising.

    At most two incomplete bytes are retained across calls. Malformed input
    poisons this parser; a caller cannot recover a successful result afterward.
    The 96-byte input limit is a prototype resource policy, not a TV limit.
    """

    MAX_CHUNK = 96

    def __init__(self) -> None:
        self._partial = bytearray()
        self._failed = False

    @property
    def buffered_bytes(self) -> int:
        return len(self._partial)

    def _fail(self, message: str) -> None:
        self._failed = True
        self._partial.clear()
        raise ProtocolError(message)

    def feed(self, chunk: bytes) -> tuple[Reply, ...]:
        if self._failed:
            raise ProtocolError("Parser is retired after malformed input")
        if type(chunk) is not bytes:
            self._fail("Reply chunks must be immutable bytes")
        if len(chunk) > self.MAX_CHUNK:
            self._fail("Reply chunk exceeds prototype limit")
        replies = []
        for value in chunk:
            position = len(self._partial)
            if position == 0 and value != 3:
                self._fail("Unexpected reply header byte")
            if position == 1 and value != 12:
                self._fail("Unexpected second reply header byte")
            if position == 2:
                if value not in (241, 255):
                    self._fail("Unsupported reply status (query replies are excluded)")
                replies.append(Reply.ACK if value == 241 else Reply.NACK)
                self._partial.clear()
            else:
                self._partial.append(value)
        return tuple(replies)

    def finish(self) -> None:
        """Declare end of standalone input; a partial reply is an error."""
        if self._failed:
            raise ProtocolError("Parser is retired after malformed input")
        if self._partial:
            self._fail("Truncated reply")
