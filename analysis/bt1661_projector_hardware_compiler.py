#!/usr/bin/env python3
"""BT1661 — projector hardware compiler for the BT1658 split."""
from __future__ import annotations

import json
from pathlib import Path


def eval_poly(coeffs: dict[int, float], x: float) -> float:
    return sum(c * (x ** k) for k, c in coeffs.items())


def main() -> None:
    # Polynomial projectors from BT1658, written as power-series coefficients.
    polys = {
        "P_clock_6": {1: 7 / 42, 2: -6 / 42, 3: 1 / 42},
        "P_clock_0": {0: 1.0, 1: -43 / 42, 2: 12 / 42, 3: -1 / 42},
        "P_matter_24": {1: 30 / 144, 2: -1 / 144},
        "P_matter_30": {1: -24 / 180, 2: 1 / 180},
    }
    spectra = {
        "clock": [0.0, 3 - 2**0.5, 3 + 2**0.5, 6.0],
        "matter": [0.0, 24.0, 30.0],
    }
    evals = {
        name: {str(round(x, 6)): round(eval_poly(poly, x), 12)
               for x in (spectra["clock"] if "clock" in name else spectra["matter"])}
        for name, poly in polys.items()
    }

    schedule = {
        "clock_power_block": {
            "powers_required": [0, 1, 2, 3],
            "primitive": "apply L_clock walk/block-encoding repeatedly on the 21-flag clock rail",
            "coefficients": {
                "P_clock_6": {"L": "1/6", "L2": "-1/7", "L3": "1/42"},
                "P_clock_0": {"I": "1", "L": "-43/42", "L2": "2/7", "L3": "-1/42"}
            }
        },
        "matter_power_block": {
            "powers_required": [1, 2],
            "primitive": "apply L_matter walk/block-encoding on the 40-mode matter rail",
            "coefficients": {
                "P_matter_24": {"L": "5/24", "L2": "-1/144"},
                "P_matter_30": {"L": "-2/15", "L2": "1/180"}
            }
        },
        "tensor_selectors": {
            "resonance_rank_120": "P_clock_6 tensor P_matter_24",
            "companion_rank_24": "P_clock_0 tensor P_matter_30"
        },
        "time_bin_lowering": [
            "allocate clock flag rail: 21 logical flags embedded in the 2048-bin envelope",
            "allocate matter rail: 40 logical matter modes embedded in the 2048-bin envelope",
            "realize each graph Laplacian power by repeated switch/delay/walk passes",
            "combine powers by LCU weights with analyzer phases matching the rational coefficients",
            "postselect or amplitude-estimate the resonance and companion ports"
        ]
    }

    assert evals["P_clock_6"] == {"0.0": 0.0, "1.585786": 0.0, "4.414214": 0.0, "6.0": 1.0}
    assert evals["P_clock_0"]["0.0"] == 1.0
    assert evals["P_matter_24"] == {"0.0": 0.0, "24.0": 1.0, "30.0": 0.0}
    assert evals["P_matter_30"] == {"0.0": 0.0, "24.0": 0.0, "30.0": 1.0}

    result = {
        "theorem": "BT1661 Projector Hardware Compiler",
        "projector_polynomials": polys,
        "spectral_evaluation_checks": evals,
        "compiled_schedule": schedule,
        "resource_counts": {
            "clock_logical_modes": 21,
            "matter_logical_modes": 40,
            "time_bin_envelope": 2048,
            "max_clock_walk_power": 3,
            "max_matter_walk_power": 2,
            "resonance_rank": 120,
            "companion_rank": 24
        },
        "boundary": "This compiles graph projectors to a walk-power/LCU schedule. It does not yet choose physical loss numbers for each switch or delay line."
    }
    out = Path("data/PART_BT1661_PROJECTOR_HARDWARE_COMPILER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
