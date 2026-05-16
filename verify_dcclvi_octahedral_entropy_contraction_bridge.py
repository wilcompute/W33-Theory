#!/usr/bin/env python3
"""Part DCCLVI: octahedral entropy-contraction bridge.

Builds on DCCLV by quantifying information decay to equilibrium for the
same octahedral random walk.

For transition operator P and uniform equilibrium pi on 6 vertices, let
mu_t = delta_i P^t from any start i. This verifier checks:
- exact one-step support spreading from 1 to 4 states,
- strict Shannon entropy growth H(mu_t),
- strict KL divergence decay D(mu_t || pi),
- exact TV half-contraction from DCCLV,
- Pinsker consistency: TV^2 <= D/2 at every tested t.

This adds an information-theoretic arrow to the closure phase-space dynamics.
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

OUT_PATH = ROOT / "data" / "dcclvi_octahedral_entropy_contraction_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    state_count: int
    equilibrium_entropy_nats: float
    initial_entropy_nats: float
    initial_kl_nats: float
    first_step_tv: float
    mixing_ratio: float
    all_identities_hold: bool


def entropy(p: np.ndarray) -> float:
    vals = p[p > 0]
    return float(-np.sum(vals * np.log(vals)))


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    vals = p[p > 0]
    qv = q[p > 0]
    return float(np.sum(vals * np.log(vals / qv)))


def tv_distance(p: np.ndarray, q: np.ndarray) -> float:
    return float(0.5 * np.sum(np.abs(p - q)))


def build_bridge() -> dict[str, Any]:
    dcclv = build_dcclv()
    P = np.array(dcclv["operators"]["P"], dtype=float)
    n = P.shape[0]
    pi = np.ones(n) / n

    start = np.zeros(n)
    start[0] = 1.0

    timeline = []
    for t in range(0, 9):
        mu = start @ np.linalg.matrix_power(P, t)
        supp = int(np.sum(mu > 1e-12))
        H = entropy(mu)
        D = kl_divergence(mu, pi)
        TV = tv_distance(mu, pi)
        timeline.append(
            {
                "t": t,
                "distribution": np.round(mu, decimals=12).tolist(),
                "support_size": supp,
                "entropy_nats": H,
                "kl_to_uniform_nats": D,
                "tv_to_uniform": TV,
                "pinsker_lhs": TV * TV,
                "pinsker_rhs": 0.5 * D,
            }
        )

    entropies = [x["entropy_nats"] for x in timeline]
    kls = [x["kl_to_uniform_nats"] for x in timeline]
    tvs = [x["tv_to_uniform"] for x in timeline]

    # For this chain from t>=1 exact half-contraction was proven in DCCLV.
    ratios = [tvs[t + 1] / tvs[t] for t in range(1, len(tvs) - 1) if tvs[t] > 1e-14]

    identities = {
        "equilibrium_entropy_is_log6": abs(entropies[-1] - math.log(6.0)) < 5e-3,
        "initial_entropy_is_zero": abs(entropies[0]) < 1e-12,
        "initial_kl_is_log6": abs(kls[0] - math.log(6.0)) < 1e-12,
        "support_expands_to_four_after_one_step": timeline[1]["support_size"] == 4,
        "entropy_is_strictly_increasing_first_four_steps": all(entropies[t + 1] > entropies[t] for t in range(0, 4)),
        "kl_is_strictly_decreasing_first_four_steps": all(kls[t + 1] < kls[t] for t in range(0, 4)),
        "tv_half_contraction_from_step1": all(abs(r - 0.5) < 1e-8 for r in ratios[:5]),
        "pinsker_holds_each_step": all(x["pinsker_lhs"] <= x["pinsker_rhs"] + 1e-12 for x in timeline),
    }

    summary = BridgeSummary(
        state_count=n,
        equilibrium_entropy_nats=entropies[-1],
        initial_entropy_nats=entropies[0],
        initial_kl_nats=kls[0],
        first_step_tv=tvs[1],
        mixing_ratio=0.5,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "information_definition": {
            "entropy": "H(mu) = -sum_i mu_i log mu_i",
            "kl": "D(mu||pi) = sum_i mu_i log(mu_i/pi_i)",
            "pinsker": "TV(mu,pi)^2 <= D(mu||pi)/2",
            "equilibrium": "pi = uniform on 6 states",
        },
        "timeline": timeline,
        "bridge_claim": {
            "exact_layer": (
                "On octahedral closure dynamics, entropy grows and KL-to-equilibrium decays while TV contracts by exact factor 1/2 from step 1 onward, giving an explicit finite information arrow toward uniform equilibrium."
            ),
            "conditional_layer": (
                "Interpreting this finite entropy production law as continuum thermodynamic irreversibility requires a scaling-limit theorem."
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
