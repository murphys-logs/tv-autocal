"""Read bounded presenter evidence without contacting the presenter or display.

A journal can establish only what was logged. An unclean, old journal does not
prove process liveness, freshness, current visibility, an unobstructed screen or
measured light. Owner confirmation and the physical plan remain necessary.
"""

from dataclasses import dataclass
from datetime import datetime
import json
from re import fullmatch

from .journal import private_path
from .presenter import validate_plan_sequence


MAX_JOURNAL_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class PresentationEvidence:
    path: str
    plan: str
    revision: str
    sequence: int
    rgb: tuple[int, int, int]
    frame_sha256: str
    authorisation_ns: int
    intent_ns: int
    applied_ns: int
    applied_record: int

    def as_dict(self) -> dict:
        return {"path": self.path, "plan": self.plan, "revision": self.revision,
                "sequence": self.sequence, "rgb": self.rgb, "frame_sha256": self.frame_sha256}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key in presenter journal")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("Non-finite JSON number in presenter journal")


def _integer(value, maximum=2**63 - 1) -> bool:
    return type(value) is int and 0 <= value <= maximum


def read_receipt(path: str, *, plan: str, revision: str, sequence: int,
                 rgb: tuple[int, int, int]) -> PresentationEvidence:
    """Require a matching latest, fully applied RGB frame in an open journal.

    Read again after meter completion and compare the frozen evidence. Any new
    frame, pending presentation, stop or closure rejects the affected attempt.
    Metadata events such as software_identity do not change the frame receipt.
    """
    if type(plan) is not str or plan not in ("T-003", "T-005"):
        raise ValueError("A measurement component plan is required")
    if type(revision) is not str or fullmatch(r"[0-9a-f]{40}", revision) is None:
        raise ValueError("A full reviewed plan revision is required")
    if not _integer(sequence, 256) or sequence == 0:
        raise ValueError("A presentation sequence in 1..256 is required")
    if type(rgb) is not tuple or len(rgb) != 3 or not all(_integer(value, 255) for value in rgb):
        raise ValueError("The expected RGB must be a tuple of three bytes")
    location = private_path(path, suffix=".log")
    with location.open("rb") as stream:
        raw = stream.read(MAX_JOURNAL_BYTES + 1)
    if not raw or len(raw) > MAX_JOURNAL_BYTES or not raw.endswith(b"\n"):
        raise ValueError("Presenter journal is empty, oversized or ends with a partial record")
    authorised_ns = None
    pending = None
    latest = None
    last_time = -1
    last_frame = 0
    for record_number, line in enumerate(raw.splitlines()):
        if not line or len(line) > 65536:
            raise ValueError("Malformed or oversized presenter journal record")
        try:
            entry = json.loads(line, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
        except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
            raise ValueError("Malformed presenter journal JSON") from error
        if type(entry) is not dict or not {"event", "sequence", "monotonic_ns", "fields"} <= set(entry):
            raise ValueError("Presenter journal record lacks required fields")
        if set(entry) - {"event", "sequence", "monotonic_ns", "fields", "utc"}:
            raise ValueError("Unexpected presenter journal record fields")
        if not _integer(entry["sequence"]) or entry["sequence"] != record_number:
            raise ValueError("Presenter journal sequence is missing, duplicated or reordered")
        timestamp = entry["monotonic_ns"]
        if not _integer(timestamp) or timestamp < last_time:
            raise ValueError("Presenter journal time is invalid or moves backwards")
        last_time = timestamp
        if "utc" in entry:
            utc = entry["utc"]
            if type(utc) is not str or len(utc) > 64:
                raise ValueError("Invalid presenter journal UTC timestamp")
            try:
                if datetime.fromisoformat(utc).utcoffset() is None:
                    raise ValueError("Presenter journal timestamp must include a timezone")
            except (ValueError, OverflowError) as error:
                raise ValueError("Invalid presenter journal UTC timestamp") from error
        event, fields = entry["event"], entry["fields"]
        if type(event) is not str or not 1 <= len(event) <= 96 or type(fields) is not dict:
            raise ValueError("Invalid presenter journal event")
        if any(word in event.lower() for word in ("close", "abort", "stop", "error", "fail", "overflow", "cancel")):
            raise ValueError("Presenter journal records a stop, failure or closure")
        if (any(fields.get(key) is True for key in ("aborted", "failed", "cancelled"))
                or any(fields.get(key) is False for key in ("complete", "log_complete"))
                or fields.get("error") is not None):
            raise ValueError("Presenter journal contains rejected or incomplete evidence")
        if event == "authorisation":
            if record_number != 0 or authorised_ns is not None:
                raise ValueError("Presenter authorisation must occur exactly once at the start")
            if (fields.get("mode") != "hardware" or fields.get("plan") != plan
                    or fields.get("revision") != revision or type(fields.get("actions")) is not list
                    or "present" not in fields["actions"]):
                raise ValueError("Presenter authorisation does not match the measurement plan")
            authorised_ns = timestamp
        elif authorised_ns is None:
            raise ValueError("Presenter journal has no matching authorisation")
        elif event == "pattern_present_intent":
            number = fields.get("sequence")
            pattern = fields.get("pattern")
            digest = fields.get("sha256")
            if pending is not None or not _integer(number, 256) or number != last_frame + 1:
                raise ValueError("Presenter intent is pending, duplicated or out of order")
            if (fields.get("hardware") is not True or type(fields.get("width")) is not int
                    or type(fields.get("height")) is not int or fields["width"] != 3840
                    or fields["height"] != 2160 or type(digest) is not str
                    or fullmatch(r"[0-9a-f]{64}", digest) is None):
                raise ValueError("Invalid native frame receipt")
            valid_rgb = (type(pattern) is list and len(pattern) == 3
                         and all(_integer(value, 255) for value in pattern))
            # Earlier visual-pattern receipts may precede the selected RGB patch.
            if not valid_rgb and not (type(pattern) is str and pattern in {
                "geometry", "black", "white", "red", "green", "blue", "detail"
            }):
                raise ValueError("Invalid presenter pattern")
            frame_pattern = tuple(pattern) if valid_rgb else pattern
            validate_plan_sequence(plan, (frame_pattern,))
            pending = (number, frame_pattern, digest, timestamp)
        elif event == "pattern_buffer_applied":
            if (pending is None or fields.get("hardware") is not True
                    or type(fields.get("sequence")) is not int or fields["sequence"] != pending[0]):
                raise ValueError("Applied frame has no matching presentation intent")
            last_frame = pending[0]
            latest = (*pending, timestamp, record_number)
            pending = None
    if authorised_ns is None or pending is not None or latest is None:
        raise ValueError("Presenter has no complete applied frame, or a newer intent is pending")
    number, pattern, digest, intended_ns, applied_ns, applied_record = latest
    if number != sequence or pattern != rgb:
        raise ValueError("Latest presenter frame does not match the expected sequence and RGB")
    return PresentationEvidence(str(location), plan, revision, number, rgb, digest,
                                authorised_ns, intended_ns, applied_ns, applied_record)
