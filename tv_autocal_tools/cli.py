"""Manual component entry points; default execution is entirely in memory."""

import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import sys

from .journal import Journal, private_path
from .permission import permit_from_dict


def _rgb(value: str) -> tuple[int, int, int]:
    try:
        parts = tuple(int(item) for item in value.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("RGB needs three integers") from error
    if len(parts) != 3 or any(not 0 <= item <= 255 for item in parts):
        raise argparse.ArgumentTypeError("RGB needs three values in 0..255")
    return parts


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Bounded component tools; simulation is the default")
    sub = result.add_subparsers(dest="tool")
    sub.add_parser("simulate", help="in-memory example; no files, windows or devices")
    for name in ("present", "meter", "serial"):
        command = sub.add_parser(name)
        command.add_argument("--hardware", action="store_true", help="requires separately authorised plan")
        command.add_argument("--permit", help="private local JSON authorisation attestation")
        command.add_argument("--confirm", help="exact RUN <plan> <full plan commit> phrase")
        command.add_argument("--log", help="new private local .log journal")
        if name == "present":
            command.add_argument("--x", type=int)
            command.add_argument("--y", type=int)
            command.add_argument("--control-x", type=int, help="explicit operator-window desktop origin on a separate display")
            command.add_argument("--control-y", type=int, help="explicit operator-window desktop origin on a separate display")
            command.add_argument("--sequence", choices=("patch", "t003", "t005-visual", "t005-optical"), default="patch")
            command.add_argument("--rgb", type=_rgb, default=(128, 128, 128))
        elif name == "meter":
            command.add_argument("--executable")
            command.add_argument("--sha256")
            command.add_argument("--attempt-log")
            command.add_argument("--presentation-log", help="active presenter's private journal")
            command.add_argument("--presentation-sequence", type=int)
            command.add_argument("--rgb", type=_rgb)
            command.add_argument("--purpose", help="plan-defined diagnostic purpose, recorded before launch")
            command.add_argument("--isolated", action="store_true", help="owner confirms both Ex-Link ends disconnected and no other non-meter serial device")
            command.add_argument("--exit-confirmed", action="store_true", help="owner confirms stable held patch, menu exit and fixed measurement configuration")
            command.add_argument("--discovery-confirmed", action="store_true", help="owner confirms earlier authorised discovery and one unambiguous Spyder5")
            command.add_argument("--wait-ms", type=int, default=2000)
            command.add_argument("--timeout-ms", type=int, default=60000)
        else:
            command.add_argument("--port")
            command.add_argument("--prerequisites-confirmed", action="store_true", help="owner attests electrical/scope/restoration/menu gates and measurement software closed")
            command.add_argument("--menu-window-ms", type=int, help="reviewed non-overlapping menu observation interval; no default")
    return result


def sequence_for(options) -> tuple:
    from tv_autocal.renderer import T003_RANGE_CODES, T005_NEUTRAL_CODES, pattern_manifest
    if options.sequence == "patch":
        return (options.rgb,)
    grey = (128, 128, 128)
    if options.sequence == "t003":
        return (grey,) + tuple((code, code, code) for code in T003_RANGE_CODES) + (grey,)
    if options.sequence == "t005-optical":
        from tv_autocal.renderer import T005_PRIMARY_CODES
        primaries = tuple(tuple(code if index == channel else 0 for index in range(3))
                          for channel in range(3) for code in T005_PRIMARY_CODES)
        return ((grey,) + tuple((code, code, code) for code in T005_NEUTRAL_CODES)
                + (grey,) + primaries + (grey,))
    return tuple(item.name for item in pattern_manifest())


def simulation_report() -> dict:
    from tv_autocal.renderer import PATCH_RECTANGLE, render_patch
    from tv_autocal.meter_output import parse_meter_output
    frame = render_patch((128, 128, 128))
    meter = parse_meter_output(b"Result is XYZ: 1 2 3, Yxy: 2 .1 .2\n", b"", 0)
    return {"mode": "simulation", "hardware_operated": False,
            "purpose": "authored diagnostic fixtures; never calibration data",
            "frame": {"width": frame.width, "height": frame.height,
                      "patch": asdict(PATCH_RECTANGLE), "area_percent": 6.25,
                      "sha256": hashlib.sha256(frame.pixels).hexdigest()},
            "meter": {"accepted": meter.accepted, "xyz": meter.xyz, "format": meter.output_format},
            "hardware_adapters_exercised": False}


def source_fingerprints() -> dict:
    """Read software identity only on an explicitly armed local run."""
    root = Path(__file__).resolve().parent.parent
    result = {}
    for package in ("tv_autocal", "tv_autocal_tools"):
        for source in sorted((root / package).glob("*.py")):
            with source.open("rb") as stream:
                content = stream.read(262145)
            if len(content) > 262144:
                raise ValueError("Software source exceeds the identity-check limit")
            result[source.relative_to(root).as_posix()] = hashlib.sha256(content).hexdigest()
    return result


def validate_measurement_context(plan: str, purpose: str, rgb: tuple) -> None:
    from tv_autocal.renderer import T003_RANGE_CODES, T005_NEUTRAL_CODES, T005_PRIMARY_CODES
    if type(rgb) is not tuple or len(rgb) != 3 or any(type(x) is not int or not 0 <= x <= 255 for x in rgb):
        raise ValueError("An explicit RGB8 measurement context is required")
    references = {"T-003": {"initial-access", "warmup-30", "warmup-35", "warmup-40", "end-check"},
                  "T-005": {"initial-reference", "middle-reference", "end-check"}}
    if plan in references and purpose in references[plan]:
        valid = rgb == (128, 128, 128)
    elif plan == "T-003" and purpose == "range":
        valid = rgb[0] in T003_RANGE_CODES and len(set(rgb)) == 1
    elif plan == "T-005" and purpose == "neutral":
        valid = rgb[0] in T005_NEUTRAL_CODES and len(set(rgb)) == 1
    elif plan == "T-005" and purpose == "primary":
        valid = sum(x != 0 for x in rgb) == 1 and max(rgb) in T005_PRIMARY_CODES
    else:
        valid = False
    if not valid:
        raise ValueError("Diagnostic purpose and RGB do not match the component plan")


def main(argv=None) -> int:
    options = parser().parse_args(argv)
    if options.tool in (None, "simulate") or not options.hardware:
        if options.tool not in (None, "simulate") and any((options.permit, options.confirm, options.log)):
            raise PermissionError("Hardware attestation/log options require explicit --hardware")
        print(json.dumps(simulation_report(), sort_keys=True))
        return 0
    if not all((options.permit, options.confirm, options.log)):
        raise PermissionError("Hardware requires --permit, --confirm and a new --log")
    permit_path = private_path(options.permit, suffix=".json")
    # Bound the configuration read; do not load an unbounded owner-local file.
    with permit_path.open("rb") as stream:
        raw = stream.read(32769)
    if len(raw) > 32768:
        raise ValueError("Permit exceeds 32 KiB")
    permit = permit_from_dict(json.loads(raw), hardware=True, confirmation=options.confirm)
    permit.require(options.tool)
    log_path = private_path(options.log, suffix=".log")
    journal = Journal(log_path)
    try:
        journal("authorisation", mode="hardware", plan=permit.plan, revision=permit.revision,
                steps=permit.steps, authorisation=permit.authorisation, evidence=permit.evidence,
                actions=permit.actions, note="Owner-supplied attestation; not proof of approval or prerequisites")
        journal("software_identity", python=sys.version.split()[0], files=source_fingerprints())
        if options.tool == "present":
            from .presenter import run_presenter
            run_presenter(permit, x=options.x, y=options.y,
                          control_x=options.control_x, control_y=options.control_y,
                          sequence=sequence_for(options), log=journal)
        elif options.tool == "meter":
            from .meter import run_meter
            from .receipt import read_receipt
            validate_measurement_context(permit.plan, options.purpose, options.rgb)
            attempt = private_path(options.attempt_log, suffix=".log")
            if attempt == log_path:
                raise ValueError("Meter native log and evidence journal must be separate")
            presentation = read_receipt(options.presentation_log, plan=permit.plan,
                                        revision=permit.revision, sequence=options.presentation_sequence,
                                        rgb=options.rgb)
            journal("measurement_context", purpose=options.purpose,
                    presentation=presentation.as_dict(),
                    note="Owner must keep this patch visible and unchanged until process closure")
            result = run_meter(permit, executable=options.executable, sha256=options.sha256,
                               attempt_log=str(attempt), log=journal, isolated=options.isolated,
                               exit_confirmed=options.exit_confirmed, wait_ms=options.wait_ms,
                               timeout_ms=options.timeout_ms, discovery_confirmed=options.discovery_confirmed)
            try:
                after = read_receipt(options.presentation_log, plan=permit.plan,
                                     revision=permit.revision, sequence=options.presentation_sequence,
                                     rgb=options.rgb)
                if after != presentation:
                    raise ValueError("Presentation receipt changed during the attempt")
            except (OSError, ValueError, TypeError) as error:
                result = replace(result, accepted=False, xyz=None,
                                 reason="Presentation evidence invalid after reading: " + str(error))
            summary = {key: value for key, value in result.as_dict().items()
                       if key not in ("stdout", "stderr", "encoding")}
            journal("meter_result", **summary, stdout_bytes=len(result.stdout), stderr_bytes=len(result.stderr))
            print(json.dumps(summary, sort_keys=True))
            return 0 if result.accepted else 2
        else:
            from .serial_tool import run_serial
            result = run_serial(permit, port=options.port, log=journal,
                                prerequisites_confirmed=options.prerequisites_confirmed,
                                menu_window_ms=options.menu_window_ms)
            summary = {**asdict(result), "accepted": result.accepted}
            journal("serial_result", **summary)
            print(json.dumps(summary, sort_keys=True))
            return 0 if result.accepted else 2
        return 0
    except (Exception, KeyboardInterrupt, SystemExit) as error:
        try:
            journal("tool-aborted", error_type=type(error).__name__, detail=str(error)[:512],
                    note="Failure reported; this event does not establish hardware closure")
        except Exception:
            pass  # Preserve the original error; failed journal closure also stays explicit.
        if isinstance(error, SystemExit):
            # A backend callback requesting exit (even exit 0) is a failed run.
            # argparse's normal help exit occurs before this hardware block.
            raise RuntimeError("Tool callback requested process exit") from error
        raise
    finally:
        journal.close()


def entrypoint() -> None:
    try:
        code = main()
    except (Exception, KeyboardInterrupt) as error:
        print("Stopped: " + str(error), file=sys.stderr)
        code = 2
    raise SystemExit(code)
