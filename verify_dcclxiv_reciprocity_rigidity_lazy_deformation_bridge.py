#!/usr/bin/env python3
"""Part DCCLXIV: reciprocity rigidity under lazy deformation bridge.

Tests whether the exact reciprocity x*K = 1 (with x=3/13, K=13/3) persists under
one-parameter deformation of the transport operator.

Define lazy deformation
    P_lambda = (1-lambda) I + lambda P,    lambda in (0,1].
For any ergodic chain, Kemeny constant scales as
    K_lambda = K / lambda.
Therefore with fixed weak scalar x=3/13:
    x*K_lambda = 1/lambda.
Hence reciprocity xK=1 is rigid: exact only at lambda=1.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclxiv_reciprocity_rigidity_lazy_deformation_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    weak_scalar_num: int
    weak_scalar_den: int
    base_kemeny_num: int
    base_kemeny_den: int
    lambda_star_num: int
    lambda_star_den: int
    all_identities_hold: bool


def kemeny_from_transition(P: np.ndarray) -> float:
    vals = np.linalg.eigvals(P)
    vals = np.real_if_close(vals, tol=1e-10).astype(float)
    vals = np.sort(vals)[::-1]
    return float(np.sum([1.0 / (1.0 - lam) for lam in vals[1:]]))


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]
    I = np.eye(n)

    x = Fraction(3, 13)
    K0 = Fraction(13, 3)

    lambdas = [Fraction(1, 1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4)]

    rows = []
    for lam in lambdas:
        lamf = float(lam)
        Pl = (1.0 - lamf) * I + lamf * P
        K_num = kemeny_from_transition(Pl)
        K_pred = K0 / lam
        xK_pred = x * K_pred
        rows.append(
            {
                "lambda": {"num": lam.numerator, "den": lam.denominator},
                "kemeny_numeric": K_num,
                "kemeny_pred": {"num": K_pred.numerator, "den": K_pred.denominator},
                "xK_pred": {"num": xK_pred.numerator, "den": xK_pred.denominator},
                "xK_numeric": float(x) * K_num,
            }
        )

    # Solve x*(K0/lambda)=1 -> lambda = x*K0 = 1
    lambda_star = x * K0

    identities = {
        "base_reciprocity_holds_at_lambda_1": lambda_star == 1,
        "kemeny_scales_as_inverse_lambda": all(
            abs(r["kemeny_numeric"] - (r["kemeny_pred"]["num"] / r["kemeny_pred"]["den"])) < 1e-9
            for r in rows
        ),
        "xK_scales_as_inverse_lambda": all(
            abs(r["xK_numeric"] - (r["xK_pred"]["num"] / r["xK_pred"]["den"])) < 1e-9
            for r in rows
        ),
        "reciprocity_breaks_for_lambda_lt_1": all(
            (r["lambda"]["num"] == r["lambda"]["den"] and abs(r["xK_numeric"] - 1.0) < 1e-9)
            or (r["lambda"]["num"] < r["lambda"]["den"] and abs(r["xK_numeric"] - 1.0) > 1e-6)
            for r in rows
        ),
        "deformed_product_equals_1_over_lambda": all(
            abs(r["xK_numeric"] - (r["lambda"]["den"] / r["lambda"]["num"])) < 1e-9
            for r in rows
        ),
    }

    summary = BridgeSummary(
        weak_scalar_num=x.numerator,
        weak_scalar_den=x.denominator,
        base_kemeny_num=K0.numerator,
        base_kemeny_den=K0.denominator,
        lambda_star_num=lambda_star.numerator,
        lambda_star_den=lambda_star.denominator,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "deformation_definition": {
            "P_lambda": "(1-lambda)I + lambda P",
            "kemeny_scaling": "K_lambda = K/lambda",
            "product_scaling": "xK_lambda = 1/lambda",
            "rigidity_point": "xK_lambda=1 iff lambda=1",
        },
        "rows": rows,
        "bridge_claim": {
            "exact_layer": (
                "The 3/13 ↔ 13/3 reciprocity is rigid under lazy deformation: xK_lambda=1/lambda, so exact inverse pairing survives only at lambda=1 and breaks for any lambda<1."
            ),
            "conditional_layer": (
                "Extending rigidity beyond this lazy family to broader deformation classes requires an additional universality theorem."
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
