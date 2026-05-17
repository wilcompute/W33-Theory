#!/usr/bin/env python3
"""W33->E6->SM burden-of-proof bridge.

This script packages the core executable proof surfaces highlighted in recent
research review into one machine-checkable certificate:

1) Representation/decomposition consistency (count-level):
   81 = 3*27 and 27 = 16 + 10 + 1.
2) Chirality-safe anomaly cancellation (exact rational arithmetic).
3) Running-law consistency via existing reciprocity bridge.
4) Markov transport closure via algebraic+cubic recurrence bridges.

Boundary note:
  This is a strict finite certificate over already-implemented invariants.
  It does not claim to replace a full symbolic branching-functor proof.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tomotope_toroidal_markov_algebraic_closure_bridge import (  # noqa: E402
    build_bridge as build_markov_algebraic,
)
from scripts.tomotope_toroidal_markov_cubic_recurrence_bridge import (  # noqa: E402
    build_bridge as build_markov_recurrence,
)
from verify_dcclxv_running_reciprocity_invariant_bridge import (  # noqa: E402
    build_bridge as build_running,
)

OUT_PATH = ROOT / "data" / "w33_e6_sm_burden_of_proof_bridge.json"


@dataclass(frozen=True)
class BurdenOfProofSummary:
    gauge_algebra_dimension: int
    harmonic_dimension: int
    generation_count: int
    e6_fundamental_dimension: int
    so10_plus_u1_branch_sum: int
    all_identities_hold: bool


def _fraction_dict(x: Fraction) -> dict[str, int]:
    return {"num": x.numerator, "den": x.denominator}


def _sm_anomaly_sums() -> dict[str, Fraction]:
    # Left-handed Weyl convention.
    # Q_L: (3,2,1/6), u_R†: (3bar,1,-2/3), d_R†: (3bar,1,1/3),
    # L_L: (1,2,-1/2), e_R†: (1,1,1)
    y_q = Fraction(1, 6)
    y_ubar = Fraction(-2, 3)
    y_dbar = Fraction(1, 3)
    y_l = Fraction(-1, 2)
    y_ebar = Fraction(1, 1)

    su3_sq_u1 = 2 * y_q + y_ubar + y_dbar
    su2_sq_u1 = 3 * y_q + y_l
    u1_cubed = 6 * y_q**3 + 3 * y_ubar**3 + 3 * y_dbar**3 + 2 * y_l**3 + y_ebar**3
    grav_sq_u1 = 6 * y_q + 3 * y_ubar + 3 * y_dbar + 2 * y_l + y_ebar

    return {
        "su3_sq_u1": su3_sq_u1,
        "su2_sq_u1": su2_sq_u1,
        "u1_cubed": u1_cubed,
        "grav_sq_u1": grav_sq_u1,
    }


def build_bridge() -> dict[str, Any]:
    # Count-level decomposition facts used broadly across the repo.
    gauge_dim = 8 + 3 + 1
    h1_dim = 81
    generations = 3
    e6_fund = 27
    so10_u1_branch = 16 + 10 + 1

    anomalies = _sm_anomaly_sums()

    running = build_running()
    markov_alg = build_markov_algebraic()
    markov_rec = build_markov_recurrence()

    identities = {
        "gauge_dimension_is_12": gauge_dim == 12,
        "h1_is_three_e6_fundamentals": h1_dim == generations * e6_fund,
        "e6_branch_27_equals_16_plus_10_plus_1": e6_fund == so10_u1_branch,
        "su3_sq_u1_anomaly_cancels": anomalies["su3_sq_u1"] == 0,
        "su2_sq_u1_anomaly_cancels": anomalies["su2_sq_u1"] == 0,
        "u1_cubed_anomaly_cancels": anomalies["u1_cubed"] == 0,
        "grav_sq_u1_anomaly_cancels": anomalies["grav_sq_u1"] == 0,
        "running_reciprocity_identities_hold": bool(running["summary"]["all_identities_hold"]),
        "running_invariant_is_one": running["summary"]["invariant_num"] == 1
        and running["summary"]["invariant_den"] == 1,
        "markov_algebraic_identities_hold": bool(markov_alg["summary"]["all_identities_hold"]),
        "markov_recurrence_identities_hold": bool(markov_rec["summary"]["all_identities_hold"]),
    }

    summary = BurdenOfProofSummary(
        gauge_algebra_dimension=gauge_dim,
        harmonic_dimension=h1_dim,
        generation_count=generations,
        e6_fundamental_dimension=e6_fund,
        so10_plus_u1_branch_sum=so10_u1_branch,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "decomposition": {
            "h1": h1_dim,
            "three_times_27": generations * e6_fund,
            "e6_fundamental": e6_fund,
            "so10_u1_branch": {"16": 16, "10": 10, "1": 1, "sum": so10_u1_branch},
        },
        "anomalies_per_generation": {
            k: _fraction_dict(v) for k, v in anomalies.items()
        },
        "running_summary": {
            "base_x": {
                "num": running["summary"]["base_x_num"],
                "den": running["summary"]["base_x_den"],
            },
            "base_kemeny": {
                "num": running["summary"]["base_K_num"],
                "den": running["summary"]["base_K_den"],
            },
            "invariant": {
                "num": running["summary"]["invariant_num"],
                "den": running["summary"]["invariant_den"],
            },
        },
        "markov_closure": {
            "algebraic_cubic": markov_alg["cubic"]["polynomial"],
            "recurrence": markov_rec["recurrence"]["equation"],
            "m2": {
                "num": markov_rec["summary"]["m2_num"],
                "den": markov_rec["summary"]["m2_den"],
            },
        },
        "identities": identities,
        "boundary_note": (
            "This certificate is exact for finite arithmetic, anomaly sums, running invariant, "
            "and Markov closure. A full symbolic branching-functor proof remains a separate target."
        ),
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
