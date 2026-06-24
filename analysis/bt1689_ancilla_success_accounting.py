#!/usr/bin/env python3
"""BT1689 — ancilla success accounting for parity-routed LCU."""
from __future__ import annotations

import json
import math
from pathlib import Path

PORTS = {
    "resonance": {"l1": 1.2939453125, "shot_snr": 37.034240801677326, "depth": 7},
    "companion": {"l1": 1.25, "shot_snr": 37.33164132928002, "depth": 5},
    "combined_two_port": {"l1": 2.5439453125, "shot_snr": 37.034240801677326, "depth": 7},
}


def success(l1: float) -> float:
    return 1.0 / (l1 * l1)


def amp_iterations(l1: float) -> float:
    theta = math.asin(min(1.0, 1.0 / l1))
    return max(0.0, math.pi / (4 * theta) - 0.5)


def main() -> None:
    rows = {}
    for name, row in PORTS.items():
        l1 = row["l1"]
        p = success(l1)
        rows[name] = {
            "l1_mass": l1,
            "single_try_success_probability": p,
            "shot_inflation_without_amplification": 1 / p,
            "effective_snr_without_amplification": row["shot_snr"] * math.sqrt(p),
            "ideal_grover_iterations_estimate": amp_iterations(l1),
            "depth": row["depth"],
        }
    result = {
        "theorem": "BT1689 Ancilla Success Accounting",
        "model": "LCU success probability p=1/l1^2; unamplified SNR scales by sqrt(p); ideal amplitude-amplification cost estimated from asin(1/l1).",
        "ports": rows,
        "interpretation": "Separate-port postselection is already high-success: about 59.7 percent for resonance and 64 percent for companion. A monolithic two-port selection has about 15.45 percent success and should use amplification or extra shots.",
        "boundary": "This accounts for abstract LCU success only. It does not include hardware-specific ancilla loss, imperfect controlled-select operations, or amplitude-amplification phase errors."
    }
    out = Path("data/PART_BT1689_ANCILLA_SUCCESS_ACCOUNTING_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
