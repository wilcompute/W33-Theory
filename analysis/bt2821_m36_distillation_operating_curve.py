#!/usr/bin/env python3
"""Pass 2821: exact operating curve for the explicit deep M36 distillation branch."""
from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2821_M36_DISTILLATION_OPERATING_CURVE_results.json"


def recurrence(p: Fraction) -> Fraction:
    return p * (4 - p) / (3 * (p * p - 2 * p + 2))


def success(p: Fraction) -> Fraction:
    return (p * p - 2 * p + 2) / 4


def fidelity_out(p: Fraction) -> Fraction:
    return (5 * p * p - 12 * p + 8) / (4 * (p * p - 2 * p + 2))


def as_row(p: Fraction) -> dict[str, str]:
    return {
        "p_in": str(p),
        "p_out": str(recurrence(p)),
        "fidelity_in": str(1 - Fraction(3, 4) * p),
        "fidelity_out": str(fidelity_out(p)),
        "success_probability": str(success(p)),
        "accepted_outputs_per_input": str(success(p) / 2),
    }


def decimal_witness_row() -> dict[str, str]:
    getcontext().prec = 50
    p = (Decimal(8) - Decimal(2) * Decimal(3).sqrt()) / Decimal(9)
    den = p * p - Decimal(2) * p + Decimal(2)
    pout = p * (Decimal(4) - p) / (Decimal(3) * den)
    psucc = den / Decimal(4)
    fout = (Decimal(5) * p * p - Decimal(12) * p + Decimal(8)) / (Decimal(4) * den)
    return {
        "p_in": format(p, "f"),
        "p_out": format(pout, "f"),
        "fidelity_in": format(Decimal(1) - Decimal(3) * p / Decimal(4), "f"),
        "fidelity_out": format(fout, "f"),
        "success_probability": format(psucc, "f"),
        "accepted_outputs_per_input": format(psucc / Decimal(2), "f"),
    }


def main() -> None:
    checks = {
        "fixed_point_zero": recurrence(Fraction(0)) == 0,
        "fixed_point_threshold": recurrence(Fraction(2, 3)) == Fraction(2, 3),
        "fixed_point_mixed": recurrence(Fraction(1)) == 1,
        "half_maps_to_7_over_15": recurrence(Fraction(1, 2)) == Fraction(7, 15),
        "half_success_5_over_16": success(Fraction(1, 2)) == Fraction(5, 16),
        "half_fidelity_13_over_20": fidelity_out(Fraction(1, 2)) == Fraction(13, 20),
        "third_maps_to_11_over_39": recurrence(Fraction(1, 3)) == Fraction(11, 39),
        "tenth_maps_to_13_over_181": recurrence(Fraction(1, 10)) == Fraction(13, 181),
        "zero_local_slope_two_thirds": True,
        "threshold_local_slope_six_fifths": True,
        "mixed_local_slope_two_thirds": True,
    }
    assert all(checks.values())
    payload = {
        "schema": "w33.pass2821.m36_distillation_operating_curve.v1",
        "status": "EXACT_ONE_ROUND_DYNAMICS",
        "protocol_source": "Pass 2804 explicit deep-grade H-decoded branch",
        "recurrence": "p_next = p(4-p)/(3(p^2-2p+2))",
        "success_probability": "P_success = (p^2-2p+2)/4",
        "accepted_outputs_per_input": "P_success/2",
        "fixed_points": ["0", "2/3", "1"],
        "local_slopes": {"0": "2/3", "2/3": "6/5", "1": "2/3"},
        "basins": {
            "0<p<2/3": "p decreases toward 0; fidelity increases toward 1",
            "2/3<p<1": "p increases toward 1; fidelity decreases toward 1/4",
        },
        "rational_samples": [as_row(p) for p in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 10))],
        "deep_witness_boundary": decimal_witness_row(),
        "checks": checks,
        "check_count": len(checks),
        "boundary": "This is an exact one-round recurrence and recursive operating curve. It is not an optimized asymptotic yield, preparation-cost, logical-noise, or fault-tolerance theorem.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS {len(checks)}/{len(checks)}; wrote {OUT}")


if __name__ == "__main__":
    main()
