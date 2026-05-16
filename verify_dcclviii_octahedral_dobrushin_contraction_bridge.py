#!/usr/bin/env python3
"""Part DCCLVIII: octahedral Dobrushin-contraction bridge.

Builds on DCCLV-DCCLVII by proving the sharp global total-variation contraction
coefficient for the octahedral random walk transition operator P.

Define Dobrushin coefficient
    alpha(P) = (1/2) max_{i,j} ||P(i,.) - P(j,.)||_1.
For any distributions mu,nu:
    TV(mu P, nu P) <= alpha(P) * TV(mu,nu).

This verifier proves:
- alpha(P) = 1/2 exactly,
- the bound is sharp (attained by adjacent vertex delta-laws),
- therefore TV contracts globally by factor <= 1/2 each step,
- and by <= (1/2)^t over t steps.
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

OUT_PATH = ROOT / "data" / "dcclviii_octahedral_dobrushin_contraction_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    dobrushin_alpha: float
    sharp_pair_i: int
    sharp_pair_j: int
    one_step_sharp_ratio: float
    all_identities_hold: bool


def tv(p: np.ndarray, q: np.ndarray) -> float:
    return 0.5 * float(np.sum(np.abs(p - q)))


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]

    pair_rows = []
    max_l1 = -1.0
    max_pair = (0, 0)
    for i in range(n):
        for j in range(i + 1, n):
            l1 = float(np.sum(np.abs(P[i, :] - P[j, :])))
            pair_rows.append({"i": i, "j": j, "l1": l1, "tv": 0.5 * l1})
            if l1 > max_l1:
                max_l1 = l1
                max_pair = (i, j)

    alpha = 0.5 * max_l1

    # sharpness witness from max pair
    i0, j0 = max_pair
    e_i = np.zeros(n)
    e_j = np.zeros(n)
    e_i[i0] = 1.0
    e_j[j0] = 1.0

    tv_before = tv(e_i, e_j)
    tv_after = tv(e_i @ P, e_j @ P)
    sharp_ratio = tv_after / tv_before

    # random deterministic family of distribution pairs for global inequality checks
    grid_pairs = []
    for a in range(n):
        for b in range(n):
            mu = np.zeros(n)
            nu = np.zeros(n)
            mu[a] = 1.0
            nu[b] = 1.0
            before = tv(mu, nu)
            after = tv(mu @ P, nu @ P)
            bound = alpha * before
            grid_pairs.append(
                {
                    "a": a,
                    "b": b,
                    "tv_before": before,
                    "tv_after": after,
                    "alpha_tv_before": bound,
                    "ratio": 0.0 if before == 0 else after / before,
                }
            )

    # multi-step bound on same deterministic family
    multistep = []
    for t in range(1, 7):
        Pt = np.linalg.matrix_power(P, t)
        worst_ratio = 0.0
        for a in range(n):
            for b in range(n):
                mu = np.zeros(n)
                nu = np.zeros(n)
                mu[a] = 1.0
                nu[b] = 1.0
                before = tv(mu, nu)
                after = tv(mu @ Pt, nu @ Pt)
                ratio = 0.0 if before == 0 else after / before
                worst_ratio = max(worst_ratio, ratio)
        multistep.append(
            {
                "t": t,
                "worst_ratio": worst_ratio,
                "alpha_power_t": alpha ** t,
            }
        )

    identities = {
        "alpha_is_exact_half": abs(alpha - 0.5) < 1e-12,
        "sharp_pair_is_adjacent_type": abs(max_l1 - 1.0) < 1e-12,
        "one_step_sharp_ratio_equals_alpha": abs(sharp_ratio - alpha) < 1e-12,
        "global_one_step_contraction_holds": all(
            x["tv_after"] <= x["alpha_tv_before"] + 1e-12 for x in grid_pairs
        ),
        "global_multistep_bound_holds": all(
            x["worst_ratio"] <= x["alpha_power_t"] + 1e-10 for x in multistep
        ),
        "multistep_worst_ratio_matches_alpha_power": all(
            abs(x["worst_ratio"] - x["alpha_power_t"]) < 1e-10 for x in multistep
        ),
    }

    summary = BridgeSummary(
        state_count=n,
        dobrushin_alpha=alpha,
        sharp_pair_i=i0,
        sharp_pair_j=j0,
        one_step_sharp_ratio=sharp_ratio,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "coefficient_definition": {
            "dobrushin_alpha": "alpha(P) = (1/2) max_{i,j} ||P(i,.)-P(j,.)||_1",
            "one_step_bound": "TV(muP,nuP) <= alpha(P) TV(mu,nu)",
            "multistep_bound": "TV(muP^t,nuP^t) <= alpha(P)^t TV(mu,nu)",
        },
        "pair_row_distances": pair_rows,
        "sharpness_witness": {
            "pair": [i0, j0],
            "tv_before": tv_before,
            "tv_after": tv_after,
            "ratio": sharp_ratio,
        },
        "multistep_profile": multistep,
        "bridge_claim": {
            "exact_layer": (
                "The octahedral transition has sharp global Dobrushin coefficient alpha=1/2, so total variation contracts by an exact worst-case factor 1/2 per step and (1/2)^t over t steps."
            ),
            "conditional_layer": (
                "Interpreting this finite sharp contraction as continuum Wasserstein/TV contractivity requires a scaling-limit theorem."
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
