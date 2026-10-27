"""Parse bounded, authored meter transcripts without starting a process.

Supported lines are the default D50 Lab and planned -x Yxy forms in ArgyllCMS
V3.5.0 spectro/spotread.c:2969-2970,2983-2984 (default label at line 636;
-x selection at 977-979). Fixtures are synthetic, not equipment recordings.
Other output modes and locales are unsupported.
No result proves the selected measurement mode, correction, units or accuracy.
"""

from dataclasses import dataclass, field
from math import isfinite
from re import IGNORECASE, compile as compile_pattern


MAX_OUTPUT_BYTES = 65_536  # Per stream; resource policy, not an Argyll limit.
_NUMBER = r"([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)"
_TRIPLE = _NUMBER + r"[ \t]+" + _NUMBER + r"[ \t]+" + _NUMBER
_RESULT = compile_pattern(r"Result is XYZ:[ \t]+" + _TRIPLE
                          + r",[ \t]+(?P<output_format>D50 Lab|Yxy):[ \t]+" + _TRIPLE)
_RESULT_MARKER = compile_pattern(r"\bresult\b", IGNORECASE)
_ERROR = compile_pattern(r"\b(?:warning|error|failed|failure|aborted)\b", IGNORECASE)
_REFERENCE = compile_pattern(r"(?:Reference is now XYZ|Making result XYZ|Preset ref\. XYZ)", IGNORECASE)


@dataclass(frozen=True)
class MeterOutput:
    """Immutable complete transcript and its software-only parsing outcome."""

    stdout: bytes
    stderr: bytes
    exit_code: int | None
    xyz: tuple[float, float, float] | None
    output_format: str | None
    accepted: bool
    reason: str
    simulated: bool = field(default=True, init=False)
    purpose: str = field(default="synthetic transcript diagnostic; never calibration data", init=False)


def parse_meter_output(
    stdout: bytes,
    stderr: bytes,
    exit_code: int | None,
    *,
    timed_out: bool = False,
    cancelled: bool = False,
) -> MeterOutput:
    """Require one complete supported XYZ result and clean process status.

    The caller supplies authored bytes and status, not a process or callback.
    Caller type/size mistakes raise; bounded rejected transcripts are retained.
    Ordinary prompt lines are tolerated; result-marked lines must parse. Explicit
    warning/error text, any stderr, reference output and unsupported result forms
    fail closed. Numeric fixtures accept signed decimal/scientific values; source
    output uses %f. The planned -x Yxy and default D50 Lab forms are supported.
    """
    if type(stdout) is not bytes or type(stderr) is not bytes:
        raise TypeError("Meter transcripts must be immutable bytes")
    if len(stdout) > MAX_OUTPUT_BYTES or len(stderr) > MAX_OUTPUT_BYTES:
        raise ValueError("Meter transcript exceeds the per-stream byte limit")
    if exit_code is not None and type(exit_code) is not int:
        raise TypeError("Exit code must be an integer or None")
    if type(timed_out) is not bool or type(cancelled) is not bool:
        raise TypeError("Timeout and cancellation flags must be bool")

    def result(reason: str, xyz: tuple[float, float, float] | None = None,
               output_format: str | None = None) -> MeterOutput:
        return MeterOutput(stdout=stdout, stderr=stderr, exit_code=exit_code, xyz=xyz,
                           output_format=output_format, accepted=xyz is not None, reason=reason)

    if cancelled:
        return result("cancelled transcript; no measurement accepted")
    if timed_out:
        return result("timed-out transcript; no measurement accepted")
    if exit_code is None:
        return result("process completion is unconfirmed")
    if exit_code != 0:
        return result("unsuccessful process exit")
    if stderr:
        return result("stderr is non-empty; review required")
    if not stdout.endswith(b"\n"):
        return result("missing or incomplete newline-terminated output")
    try:
        text = stdout.decode("ascii")
    except UnicodeDecodeError:
        return result("unsupported non-ASCII output")
    if any(ord(char) < 32 and char not in "\t\r\n" or ord(char) == 127 for char in text):
        return result("unsupported control character in output")
    if _ERROR.search(text):
        return result("warning or error diagnostic in output")
    if _REFERENCE.search(text):
        return result("reference output is outside the supported default mode")

    candidates = [line.strip() for line in text.splitlines() if _RESULT_MARKER.search(line)]
    if len(candidates) != 1:
        return result("expected exactly one result line")
    match = _RESULT.fullmatch(candidates[0])
    if match is None:
        return result("malformed or unsupported result line")
    # Group 4 is the format label; the other six groups are numeric fields.
    values = tuple(float(match.group(index)) for index in (1, 2, 3, 5, 6, 7))
    if not all(isfinite(value) for value in values):
        return result("non-finite numeric result")
    xyz = (values[0], values[1], values[2])
    return result("accepted synthetic transcript only", xyz, match.group("output_format"))
