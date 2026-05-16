#!/usr/bin/env python3
"""Part DCCLVII: octahedral chi-square contraction bridge.

Builds on DCCLV-DCCLVI by deriving an exact quadratic-information decay law.

For the octahedral random walk with uniform equilibrium pi (|V|=6), define
for a distribution mu:
    L2sq(mu||pi) = sum_i (mu_i - pi_i)^2,
    chi2(mu||pi) = sum_i (mu_i - pi_i)^2 / pi_i = 6 * L2sq.

From DCCLV's exact modal power law P^t = P0 + (-1/2)^t P6 (t>=1), the
non-stationary component scales by (-1/2)^t. Therefore:
    L2sq_t = C * (1/4)^t,
    chi2_t = C' * (1/4)^t,
with exact one-step ratio 1/4 for t>=1.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclvii_octahedral_chi_square_contraction_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    initial_chi2: float
    first_step_chi2: float
    contraction_ratio: float
    first_step_l2sq: float
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]
    pi = np.ones(n) / n

    start = np.zeros(n)
    start[0] = 1.0

    timeline = []
    for t in range(0, 10):
        mu = start @ np.linalg.matrix_power(P, t)
        diff = mu - pi
        l2sq = float(np.dot(diff, diff))
        chi2 = float(np.sum((diff * diff) / pi))
        timeline.append(
            {
                "t": t,
                "distribution": np.round(mu, decimals=12).tolist(),
                "l2sq_to_uniform": l2sq,
                "chi2_to_uniform": chi2,
            }
        )

    l2 = [x["l2sq_to_uniform"] for x in timeline]
    chi = [x["chi2_to_uniform"] for x in timeline]

    l2_ratio = {str(t): l2[t + 1] / l2[t] for t in range(1, 9)}
    chi_ratio = {str(t): chi[t + 1] / chi[t] for t in range(1, 9)}

    c_l2 = l2[1] * 4.0
    c_chi = chi[1] * 4.0
    closed_l2 = {str(t): c_l2 * (0.25 ** t) for t in range(1, 10)}
    closed_chi = {str(t): c_chi * (0.25 ** t) for t in range(1, 10)}

    # exact relation chi2 = n * l2sq for uniform pi
    chi_l2_relation = [abs(chi[t] - n * l2[t]) for t in range(0, 10)]

    identities = {
        "initial_chi2_is_5": abs(chi[0] - 5.0) < 1e-12,
        "first_step_chi2_is_half": abs(chi[1] - 0.5) < 1e-12,
        "chi2_equals_6_times_l2sq": all(err < 1e-12 for err in chi_l2_relation),
        "l2sq_ratio_is_quarter_from_step1": all(abs(l2_ratio[str(t)] - 0.25) < 1e-10 for t in range(1, 9)),
        "chi2_ratio_is_quarter_from_step1": all(abs(chi_ratio[str(t)] - 0.25) < 1e-10 for t in range(1, 9)),
        "l2sq_matches_closed_form": all(abs(l2[t] - closed_l2[str(t)]) < 1e-10 for t in range(1, 10)),
        "chi2_matches_closed_form": all(abs(chi[t] - closed_chi[str(t)]) < 1e-10 for t in range(1, 10)),
        "quadratic_information_monotone_decay": all(chi[t + 1] < chi[t] for t in range(0, 9)),
    }

    summary = BridgeSummary(
        state_count=n,
        initial_chi2=chi[0],
        first_step_chi2=chi[1],
        contraction_ratio=0.25,
        first_step_l2sq=l2[1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "quadratic_information_definition": {
            "l2sq": "sum_i (mu_i - pi_i)^2",
            "chi2": "sum_i (mu_i - pi_i)^2 / pi_i",
            "uniform_relation": "chi2 = 6 * L2sq",
            "contraction": "for t>=1: L2sq_{t+1} = (1/4) L2sq_t and chi2_{t+1} = (1/4) chi2_t",
        },
        "timeline": timeline,
        "ratios": {
            "l2sq_ratio": {k: round(v, 12) for k, v in l2_ratio.items()},
            "chi2_ratio": {k: round(v, 12) for k, v in chi_ratio.items()},
        },
        "closed_form": {
            "l2sq": {k: round(v, 12) for k, v in closed_l2.items()},
            "chi2": {k: round(v, 12) for k, v in closed_chi.items()},
        },
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure walk has exact quadratic-information contraction: after step 1, both L2 distance squared and chi-square divergence to equilibrium decay by an exact factor 1/4 per step."
            ),
            "conditional_layer": (
                "Interpreting this finite chi-square contraction as continuum hypocoercive decay requires a scaling-limit theorem."
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
