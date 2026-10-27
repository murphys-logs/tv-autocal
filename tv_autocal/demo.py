"""Text-only demonstration: off-screen pixels and a wholly synthetic cycle.

No command-line options or physical backend exist. Running this module prints
JSON; it never opens a window, writes a file or starts another program.
"""

from dataclasses import asdict
from hashlib import sha256
from json import dumps
from sys import argv

from .cycle import CycleState, MeasurementController, MeterSample, SimulatedMeter, SimulatedTV
from .renderer import pattern_manifest, render_patch
from .simulation import FakeClock


def build_demo() -> dict:
    """Return an in-memory report; all XYZ values are explicit synthetic inputs."""
    rgb = (128, 128, 128)
    frame = render_patch(rgb)
    clock = FakeClock()
    tv = SimulatedTV(initial_level=50)
    meter = SimulatedMeter((
        MeterSample((10.0, 20.0, 30.0)),
        MeterSample((9.0, 19.0, 29.0)),
        MeterSample((10.0, 20.0, 30.0)),
    ))
    controller = MeasurementController(clock, tv, meter, wait_ms=2000)
    controller.start_baseline(rgb)
    clock.advance(2000)
    if controller.poll() is not CycleState.READY:
        raise RuntimeError("Synthetic baseline failed")
    controller.measure_change(49, rgb)
    clock.advance(2000)
    if controller.poll() is not CycleState.READY:
        raise RuntimeError("Synthetic change failed")
    controller.restore()
    clock.advance(2000)
    if controller.poll() is not CycleState.COMPLETE:
        raise RuntimeError("Synthetic restoration failed")

    records = []
    for record in controller.records:
        row = asdict(record)
        row["phase"] = record.phase.value
        records.append(row)
    events = []
    for event in controller.events:
        row = asdict(event)
        row["phase"] = event.phase.value if event.phase is not None else None
        events.append(row)
    return {
        "simulated": True,
        "notice": "Software demonstration only; XYZ supplied as literals, no equipment evidence.",
        "frame": {
            "width": frame.width, "height": frame.height,
            "format": "row-major RGB8; no alpha or row padding",
            "bytes": len(frame.pixels), "sha256": sha256(frame.pixels).hexdigest(),
            "patch_rgb": rgb, "presented_on_display": False,
        },
        "visual_manifest": [asdict(spec) for spec in pattern_manifest()],
        "state": controller.state.value,
        "original_level": controller.original_level,
        "final_level": tv.level,
        "restoration_required": controller.restoration_required,
        "wait_ms": 2000, "fake_time_ms": clock.milliseconds,
        "records": records, "events": events,
    }


def main(arguments: tuple[str, ...] = ()) -> None:
    if type(arguments) is not tuple or arguments:
        raise ValueError("This software-only demo accepts no arguments")
    print(dumps(build_demo(), indent=2, allow_nan=False))


if __name__ == "__main__":
    main(tuple(argv[1:]))
