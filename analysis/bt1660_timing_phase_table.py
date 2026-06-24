#!/usr/bin/env python3
"""BT1660 timing phase table generator."""
from __future__ import annotations

import cmath
import json
import math
from pathlib import Path


def phase(value: float, tau: float) -> dict[str, float]:
    z = cmath.exp(-1j * value * tau)
    return {"real": round(z.real, 6), "imag": round(z.imag, 6)}


def main() -> None:
    sqrt2 = math.sqrt(2)
    eigenvalues = [
        0,
        3 - sqrt2,
        3 + sqrt2,
        6,
        24,
        27 - sqrt2,
        27 + sqrt2,
        30,
        33 - sqrt2,
        33 + sqrt2,
        36,
    ]
    tau30 = math.pi / 15
    table = {str(round(v, 6)): phase(v, tau30) for v in eigenvalues}
    result = {
        "theorem": "BT1660 Timing Phase Table",
        "tau_30": "pi/15",
        "coupled_phases_at_tau_30": table,
        "clock_separator_tau": "pi/6",
        "clock_separator": {
            "clock_6_phase": phase(6, math.pi / 6),
            "clock_0_phase": phase(0, math.pi / 6)
        },
        "matter_gap_tau": "pi/24",
        "matter_gap_probe": {
            "matter_24_phase": phase(24, math.pi / 24),
            "matter_30_phase": phase(30, math.pi / 24)
        }
    }
    assert result["coupled_phases_at_tau_30"]["30"]["real"] == 1.0
    assert result["clock_separator"]["clock_6_phase"]["real"] == -1.0
    assert result["clock_separator"]["clock_0_phase"]["real"] == 1.0
    out = Path("data/PART_BT1660_TIMING_PHASE_TABLE.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
