"""Hardware-free audit reproductions, deliberately outside unittest discovery.

Run from the repository root: py -3.15 -B tests/audit_ground_up.py
Reproduces the historical decoder locally; never constructs a Windows runtime.
This records a KNOWN defect, not a passing regression test for correct behavior.
Independent arithmetic uses ITU-R BT.1886-0 Annex 1 and BT.709-6 Part 1.
No downloaded source, device I/O, GUI, subprocess, network or file writes.
"""

import json
import math
from pathlib import Path
import sys

# Direct script execution puts tests/ first; select this checkout explicitly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class WouldBlock(Exception):
    """Inert substitute for an unavailable synchronous console read."""


class Console:
    def __init__(self, keys):
        self.keys = list(keys)
        self.reads = 0

    def kbhit(self):
        return bool(self.keys)

    def getwch(self):
        self.reads += 1
        if not self.keys:
            raise WouldBlock("getwch called with no available input")
        return self.keys.pop(0)


def historical_decoder(console):
    """Frozen pre-fix behavior; current regressions live in unittest tests."""
    if not console.kbhit():
        return None
    key = console.getwch()
    if key in ("\x00", "\xe0"):
        console.getwch()
        return None
    return key if key in {"b", "m", "o", "e", "c", "d", "r", "q"} else None


def console_reproduction():
    alone = Console(["\u00e0"])
    blocked = False
    try:
        historical_decoder(alone)
    except WouldBlock:
        blocked = True
    assert blocked and alone.reads == 2
    followed = Console(["\u00e0", "q"])
    decoded = historical_decoder(followed)
    assert decoded is None and followed.reads == 2 and not followed.keys
    ordinary = Console(["q"])
    assert historical_decoder(ordinary) == "q"
    return {"unavailable_second_read": blocked, "next_q_swallowed": True,
            "ordinary_q_returned": True, "native_console_tested": False, "historical_decoder_only": True}


def bt1886(v, black, white):
    """V dimensionless in [0,1]; black/white/output in cd/m2.

    Algebraically expanded Annex 1: (V*(Lw**(1/g)-Lb**(1/g))
    + Lb**(1/g))**g for nonnegative V. Does not assume measured endpoints.
    """
    if not (0 <= v <= 1 and 0 <= black < white):
        raise ValueError("invalid example endpoints or stimulus")
    return (v * (white ** (1 / 2.4) - black ** (1 / 2.4))
            + black ** (1 / 2.4)) ** 2.4


def calculations():
    # Independent literal sums, not the project's encoder implementation.
    fixtures = {"power_off": "08 22 00 00 00 01 D5",
                "power_on": "08 22 00 00 00 02 D4",
                "volume_25": "08 22 01 00 00 19 BC",
                "exit": "08 22 0D 00 00 2D 9C",
                "contrast_94": "08 22 0B 02 00 5E 6B",
                "contrast_95": "08 22 0B 02 00 5F 6A"}
    for literal in fixtures.values():
        assert sum(bytes.fromhex(literal)) % 256 == 0
    assert sum(bytes.fromhex("08 22 00 00 00 02 D6")) % 256 == 2
    assert 960 * 540 * 16 == 3840 * 2160
    assert (3840 - 960) // 2 == 1440 and (2160 - 540) // 2 == 810
    for black in (0, 0.04, 0.05, 0.10):
        assert math.isclose(bt1886(0, black, 150), black, abs_tol=1e-12)
        assert math.isclose(bt1886(1, black, 150), 150, abs_tol=1e-10)
    assert math.isclose(bt1886(0.5, 0, 150), 150 * 0.5 ** 2.4)
    # RGB->XYZ linear-light matrix independently derived by solving primary
    # columns [x/y,1,(1-x-y)/y] scaled to a D65 white with Y=1.
    primaries = ((0.64, 0.33), (0.30, 0.60), (0.15, 0.06))
    white_xyz = (0.3127 / 0.3290, 1, (1 - 0.3127 - 0.3290) / 0.3290)
    columns = [(x / y, 1, (1 - x - y) / y) for x, y in primaries]
    rows = [[columns[c][r] for c in range(3)] + [white_xyz[r]] for r in range(3)]
    for p in range(3):
        divisor = rows[p][p]
        rows[p] = [x / divisor for x in rows[p]]
        for r in range(3):
            if r != p:
                factor = rows[r][p]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[p])]
    scales = [row[3] for row in rows]
    matrix = [[columns[c][r] * scales[c] for c in range(3)] for r in range(3)]
    assert all(math.isclose(sum(row), value) for row, value in zip(matrix, white_xyz))
    return {"frame_checksums": fixtures, "bad_D6_residue": 2,
            "patch_percent": 100 * 960 * 540 / (3840 * 2160),
            "RGB_buffer_bytes": 3840 * 2160 * 3,
            "budget_pence_remaining": 2500 - 1599,
            "bt1886_cd_m2_at_150_white": {
                str(black): {str(v): round(bt1886(v, black, 150), 8)
                             for v in (0, .05, .1, .5, 1)}
                for black in (0, .04, .05, .10)},
            "linear_Rec709_to_XYZ_D65_Y1": matrix,
            "ideal_full_to_limited_128_before_quantisation": 16 + 219 * 128 / 255,
            "hypothetical_double_range_black_white": [16 + 219 * x / 255 for x in (16, 235)],
            "assumptions": "150 cd/m2 and all black levels are illustrative, not measurements"}


if __name__ == "__main__":
    print(json.dumps({"L4": console_reproduction(), "arithmetic": calculations(),
                      "equipment_operated": False}, indent=2))
