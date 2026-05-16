#!/usr/bin/env python3
"""Part DCCLIX: octahedral exact mixing-time bridge.

Builds on DCCLV and DCCLVIII by converting exact TV contraction into a closed
mixing-time formula.

From the octahedral walk started at a vertex delta law:
- TV_0 = 5/6,
- TV_t = (2/3) * 2^{-t} for t >= 1.

Hence the exact total-variation epsilon-mixing time is
    tau(eps) = min{t : TV_t <= eps}
             = ceil(max(1, log2(2/(3 eps)))).
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_octahedral_transition_mixing_bridge import build_bridge as build_dcclv

OUT_PATH = ROOT / "data" / "dcclix_octahedral_exact_mixing_time_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    tv_t0: float
    tv_prefactor: float
    contraction_base: float
    tau_eps_0_1: int
    tau_eps_0_01: int
    all_identities_hold: bool


def tv(p: np.ndarray, q: np.ndarray) -> float:
    return 0.5 * float(np.sum(np.abs(p - q)))


def tau_formula(eps: float) -> int:
    return int(math.ceil(max(1.0, math.log2(2.0 / (3.0 * eps)))))


def tau_bruteforce(P: np.ndarray, pi: np.ndarray, eps: float, horizon: int = 64) -> int:
    n = P.shape[0]
    worst = []
    for t in range(horizon + 1):
        Pt = np.linalg.matrix_power(P, t)
        max_tv = 0.0
        for i in range(n):
            e = np.zeros(n)
            e[i] = 1.0
            max_tv = max(max_tv, tv(e @ Pt, pi))
        worst.append(max_tv)
        if max_tv <= eps:
            return t
    raise RuntimeError("horizon too small")


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]
    pi = np.ones(n) / n

    start = np.zeros(n)
    start[0] = 1.0

    tv_timeline = []
    for t in range(0, 21):
        mu = start @ np.linalg.matrix_power(P, t)
        tv_val = tv(mu, pi)
        closed = 5.0 / 6.0 if t == 0 else (2.0 / 3.0) * (2.0 ** (-t))
        tv_timeline.append(
            {
                "t": t,
                "tv": tv_val,
                "closed_form": closed,
                "difference": tv_val - closed,
            }
        )

    eps_samples = [0.25, 0.1, 0.05, 0.01, 0.001]
    mixing_table = []
    for eps in eps_samples:
        tau_f = tau_formula(eps)
        tau_b = tau_bruteforce(P, pi, eps)
        mixing_table.append(
            {
                "epsilon": eps,
                "tau_formula": tau_f,
                "tau_bruteforce": tau_b,
            }
        )

    ratios = [
        tv_timeline[t + 1]["tv"] / tv_timeline[t]["tv"]
        for t in range(1, 20)
        if tv_timeline[t]["tv"] > 1e-16
    ]

    identities = {
        "tv_t0_is_five_over_six": abs(tv_timeline[0]["tv"] - (5.0 / 6.0)) < 1e-12,
        "tv_closed_form_holds_t_ge_1": all(abs(x["difference"]) < 1e-12 for x in tv_timeline[1:]),
        "tv_ratio_is_half_for_t_ge_1": all(abs(r - 0.5) < 1e-10 for r in ratios[:10]),
        "mixing_formula_matches_bruteforce": all(row["tau_formula"] == row["tau_bruteforce"] for row in mixing_table),
        "tau_is_monotone_in_epsilon": all(
            mixing_table[i]["tau_formula"] <= mixing_table[i + 1]["tau_formula"]
            for i in range(len(mixing_table) - 1)
        ) is False,  # epsilon list decreases, so tau should nondecrease
        "tau_nondecreasing_when_epsilon_decreases": all(
            mixing_table[i]["tau_formula"] <= mixing_table[i + 1]["tau_formula"]
            for i in range(len(mixing_table) - 1)
        ),
    }

    # Replace the intentionally awkward monotonicity check with the correct one only
    identities["tau_is_monotone_in_epsilon"] = identities["tau_nondecreasing_when_epsilon_decreases"]

    summary = BridgeSummary(
        state_count=n,
        tv_t0=tv_timeline[0]["tv"],
        tv_prefactor=2.0 / 3.0,
        contraction_base=0.5,
        tau_eps_0_1=next(r["tau_formula"] for r in mixing_table if abs(r["epsilon"] - 0.1) < 1e-12),
        tau_eps_0_01=next(r["tau_formula"] for r in mixing_table if abs(r["epsilon"] - 0.01) < 1e-12),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "mixing_definition": {
            "tv_profile": "TV_0 = 5/6; TV_t = (2/3) 2^{-t} for t>=1",
            "tau_formula": "tau(eps) = ceil(max(1, log2(2/(3 eps))))",
        },
        "tv_timeline": [
            {
                "t": row["t"],
                "tv": round(row["tv"], 12),
                "closed_form": round(row["closed_form"], 12),
                "difference": round(row["difference"], 12),
            }
            for row in tv_timeline
        ],
        "mixing_table": mixing_table,
        "bridge_claim": {
            "exact_layer": (
                "Octahedral closure walk has exact TV profile TV_t=(2/3)2^{-t} (t>=1), hence exact epsilon-mixing time tau(eps)=ceil(max(1,log2(2/(3eps))))."
            ),
            "conditional_layer": (
                "Interpreting this finite exact mixing-time law as continuum equilibration time requires a scaling limit."
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
