"""Private, exclusive JSON-lines journals. No file is opened at import."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from re import fullmatch
import time


class JournalError(RuntimeError):
    pass


def private_path(value: str, *, suffix: str, root: Path | None = None) -> Path:
    """Constrain owner-local files to this checkout's ignored local directory."""
    if type(value) is not str or not value or "\x00" in value:
        raise ValueError("A private local path is required")
    repository = Path(__file__).resolve().parent.parent if root is None else root.resolve()
    base = (repository / "local").resolve()
    # Reject a redirected local directory as well as traversal through its children.
    if not base.is_relative_to(repository):
        raise ValueError("The local directory must stay inside the checkout")
    candidate = Path(value)
    candidate = (repository / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()
    if candidate == base or not candidate.is_relative_to(base) or candidate.suffix != suffix:
        raise ValueError("File must be inside this checkout's local directory with suffix " + suffix)
    for part in candidate.relative_to(base).parts:
        stem = part.split(".")[0].upper()
        if (":" in part or part.endswith((" ", "."))
                or stem in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
                or fullmatch(r"(?:COM|LPT)[0-9¹²³]+", stem)):
            raise ValueError("Reserved device names, alternate streams and ambiguous paths are forbidden")
    return candidate


class Journal:
    """Bounded durable evidence; capacity or disk failure prevents further effects.

    4 KiB is reserved for a final close record. A failed journal never recovers.
    This is ordinary local file protection, not an adversarial filesystem sandbox.
    """

    def __init__(self, path: Path, *, max_bytes: int = 8 * 1024 * 1024) -> None:
        if type(max_bytes) is not int or not 8192 <= max_bytes <= 64 * 1024 * 1024:
            raise ValueError("Invalid journal limit")
        self.path = private_path(str(path), suffix=".log")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("xb")
        self._limit, self._used, self._sequence = max_bytes, 0, 0
        self._failed = False
        self._closed = False

    def __call__(self, kind: str, **fields) -> None:
        if self._closed or self._failed:
            raise JournalError("Evidence journal is closed or incomplete")
        if type(kind) is not str or not 1 <= len(kind) <= 96:
            raise ValueError("Invalid journal event kind")
        try:
            payload = json.dumps({"event": kind, "sequence": self._sequence,
                                  "monotonic_ns": time.monotonic_ns(),
                                  "utc": datetime.now(timezone.utc).isoformat(), "fields": fields},
                                 ensure_ascii=True, allow_nan=False, separators=(",", ":"))
            data = payload.encode("utf-8") + b"\n"
            if len(data) > 65536 or self._used + len(data) > self._limit - 4096:
                raise JournalError("Evidence journal capacity exceeded; stop and review")
            self._write(data)
        except Exception as error:
            self._failed = True
            if isinstance(error, JournalError):
                raise
            raise JournalError("Evidence journal write failed; stop and review") from error
        self._sequence += 1

    def _write(self, data: bytes) -> None:
        written = self._file.write(data)
        if written != len(data):
            raise JournalError("Partial evidence journal write")
        self._used += len(data)
        self._file.flush()
        os.fsync(self._file.fileno())

    def close(self) -> None:
        if self._closed:
            return
        try:
            final = json.dumps({"event": "journal-close", "sequence": self._sequence,
                                "monotonic_ns": time.monotonic_ns(),
                                "utc": datetime.now(timezone.utc).isoformat(),
                                "complete": not self._failed}, separators=(",", ":")).encode() + b"\n"
            self._write(final)
        except Exception as error:
            self._failed = True
            raise JournalError("Could not persist journal closure; audit is incomplete") from error
        finally:
            self._closed = True
            self._file.close()
