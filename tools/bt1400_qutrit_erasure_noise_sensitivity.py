#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def case(name: str, eraser_efficiency: float, branch_visibility: float, distinguishability: float, phase_sigma_rad: float) -> dict:
    phase_factor = math.exp(-(phase_sigma_rad ** 2))
    gamma = max(0.0, min(1.0, branch_visibility * (1.0 - distinguishability) * phase_factor))
    p_success = eraser_efficiency / 3.0
    p0 = (1.0 + 2.0 * gamma) / 3.0
    p1 = (1.0 - gamma) / 3.0
    return {
        "name": name,
        "eraser_efficiency": eraser_efficiency,
        "branch_visibility": branch_visibility,
        "branch_distinguishability": distinguishability,
        "phase_sigma_rad": phase_sigma_rad,
        "phase_factor": phase_factor,
        "coherence_gamma": gamma,
        "eraser_success_probability": p_success,
        "conditional_l1_coherence": 2.0 * gamma,
        "interferometer_port_probabilities": [p0, p1, p1],
        "fringe_contrast_p0_minus_p1": p0 - p1
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1400_qutrit_erasure_noise_sensitivity.json")
    ns = ap.parse_args()
    rows = [
        case("ideal", 1.0, 1.0, 0.0, 0.0),
        case("baseline", 0.90, 0.96, 0.03, 0.05),
        case("conservative", 0.75, 0.90, 0.10, 0.15),
        case("bad_distinguishability", 0.75, 0.90, 0.35, 0.15),
        case("bad_phase", 0.75, 0.90, 0.10, 0.45)
    ]
    checks = {
        "ideal_recovers_bt1396": abs(rows[0]["conditional_l1_coherence"] - 2.0) < 1e-12 and rows[0]["interferometer_port_probabilities"][0] == 1.0,
        "baseline_passes_visibility_gate": rows[1]["coherence_gamma"] > 0.90 and rows[1]["interferometer_port_probabilities"][0] > 0.93,
        "conservative_passes_visibility_gate": rows[2]["coherence_gamma"] > 0.75 and rows[2]["interferometer_port_probabilities"][0] > 0.83,
        "bad_distinguishability_fails_strong_gate": rows[3]["coherence_gamma"] < 0.60,
        "bad_phase_degrades_below_conservative": rows[4]["coherence_gamma"] < rows[2]["coherence_gamma"],
        "all_probabilities_normalized": all(abs(sum(r["interferometer_port_probabilities"]) - 1.0) < 1e-12 for r in rows)
    }
    result = {
        "bt": 1400,
        "title": "Qutrit quantum-erasure readout noise sensitivity",
        "verified": all(checks.values()),
        "checks": checks,
        "model": "rho_route has diagonal 1/3 and off-diagonal coherence gamma/3; gamma=visibility*(1-distinguishability)*exp(-sigma_phi^2)",
        "rows": rows,
        "gates": {
            "strong_readout": "coherence_gamma >= 0.90 and port0 >= 0.93",
            "conservative_readout": "coherence_gamma >= 0.75 and port0 >= 0.83"
        },
        "boundary": "Parametric visibility/readout model only. It is not a full optical interferometer simulation with detector dark counts or mode mismatch matrices."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1400, "verified": result["verified"], "baseline_gamma": rows[1]["coherence_gamma"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
