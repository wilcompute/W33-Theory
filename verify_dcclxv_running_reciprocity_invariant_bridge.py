#!/usr/bin/env python3
"""Part DCCLXV: running reciprocity-invariant bridge.

Builds on DCCLXIV (rigidity under lazy deformation):
    x K_lambda = 1/lambda,
where x=3/13 and K_lambda = K/lambda with K=13/3.

This part extracts the exact deformation-invariant compensation law by defining
running weak scalar
    x_lambda = lambda x.
Then for all lambda in (0,1],
    x_lambda K_lambda = 1.

So reciprocity is rigid for bare x, but exactly restored by a one-parameter
running scalar map.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxiv_reciprocity_rigidity_lazy_deformation_bridge import build_bridge as build_dcclxiv

OUT_PATH = ROOT / "data" / "dcclxv_running_reciprocity_invariant_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    base_x_num: int
    base_x_den: int
    base_K_num: int
    base_K_den: int
    invariant_num: int
    invariant_den: int
    sample_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    _ = build_dcclxiv()

    x = Fraction(3, 13)
    K = Fraction(13, 3)

    lambdas = [
        Fraction(1, 1),
        Fraction(9, 10),
        Fraction(3, 4),
        Fraction(2, 3),
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 4),
    ]

    rows = []
    for lam in lambdas:
        K_lam = K / lam
        x_bare_product = x * K_lam
        x_lam = lam * x
        x_run_product = x_lam * K_lam
        rows.append(
            {
                "lambda": {"num": lam.numerator, "den": lam.denominator},
                "x_bare": {"num": x.numerator, "den": x.denominator},
                "x_running": {"num": x_lam.numerator, "den": x_lam.denominator},
                "K_lambda": {"num": K_lam.numerator, "den": K_lam.denominator},
                "bare_product": {"num": x_bare_product.numerator, "den": x_bare_product.denominator},
                "running_product": {"num": x_run_product.numerator, "den": x_run_product.denominator},
            }
        )

    identities = {
        "bare_product_is_inverse_lambda": all(
            r["bare_product"]["num"] == r["lambda"]["den"] and r["bare_product"]["den"] == r["lambda"]["num"]
            for r in rows
        ),
        "running_product_is_exactly_one": all(
            r["running_product"] == {"num": 1, "den": 1} for r in rows
        ),
        "running_scalar_is_lambda_times_x": all(
            Fraction(r["x_running"]["num"], r["x_running"]["den"]) == Fraction(r["lambda"]["num"], r["lambda"]["den"]) * x
            for r in rows
        ),
        "base_point_matches_original_reciprocity": rows[0]["lambda"] == {"num": 1, "den": 1}
        and rows[0]["bare_product"] == {"num": 1, "den": 1}
        and rows[0]["running_product"] == {"num": 1, "den": 1},
        "flow_equation_discrete_form": all(
            Fraction(r["running_product"]["num"], r["running_product"]["den"]) == 1
            for r in rows
        ),
    }

    summary = BridgeSummary(
        base_x_num=x.numerator,
        base_x_den=x.denominator,
        base_K_num=K.numerator,
        base_K_den=K.denominator,
        invariant_num=1,
        invariant_den=1,
        sample_count=len(rows),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "running_definition": {
            "base_reciprocity": "xK=1 at lambda=1 with x=3/13, K=13/3",
            "deformation": "K_lambda=K/lambda",
            "running_scalar": "x_lambda=lambda x",
            "invariant": "x_lambda K_lambda = 1",
        },
        "samples": rows,
        "bridge_claim": {
            "exact_layer": (
                "Although bare reciprocity breaks under lazy deformation (xK_lambda=1/lambda), a unique linear running scalar x_lambda=lambda x restores exact reciprocity invariant x_lambda K_lambda=1 for all sampled lambda."
            ),
            "conditional_layer": (
                "Whether the same running-law form remains unique in broader non-lazy deformation classes requires an additional universality theorem."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
