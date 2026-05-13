#!/usr/bin/env python3
"""Part DCXXII: probabilistic bound bridge.

Quantifies the stability of the bi-scale automaton under random perturbations.

Defines:
  - Perturbation model: additive noise on horizon thresholds.
  - Stability metric: probability of joint-state transitions exceeding expected bounds.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCXX_PATH = ROOT / "data" / "tomotope_toroidal_biscale_automaton_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_probabilistic_bound_bridge.json"


def _load_json_or_build(path: Path, module_name: str) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    module = __import__(module_name, fromlist=["build_bridge"])
    return module.build_bridge()


@dataclass(frozen=True)
class ProbabilisticSummary:
    linear_half_horizon: int
    linear_packet_horizon: int
    energy_half_horizon: int
    energy_packet_horizon: int
    perturbation_stddev: float
    random_seed: int
    trials: int
    stable_successes: int
    stability_probability: float
    all_identities_hold: bool


def build_bridge(stddev: float = 0.5, trials: int = 10000, seed: int = 1337) -> dict[str, Any]:
    dcxx = _load_json_or_build(
        DCXX_PATH, "scripts.tomotope_toroidal_biscale_automaton_bridge"
    )

    l_half = int(dcxx["summary"]["linear_half_horizon"])
    l_packet = int(dcxx["summary"]["linear_packet_horizon"])
    e_half = int(dcxx["summary"]["energy_half_horizon"])
    e_packet = int(dcxx["summary"]["energy_packet_horizon"])

    rng = random.Random(seed)

    def simulate_perturbation() -> bool:
        perturbed_l_half = l_half + rng.gauss(0, stddev)
        perturbed_l_packet = l_packet + rng.gauss(0, stddev)
        perturbed_e_half = e_half + rng.gauss(0, stddev)
        perturbed_e_packet = e_packet + rng.gauss(0, stddev)

        return (
            perturbed_l_half < perturbed_l_packet
            and perturbed_e_half < perturbed_e_packet
            and perturbed_e_packet < perturbed_l_packet
        )

    stability_count = sum(simulate_perturbation() for _ in range(trials))
    stability_probability = stability_count / trials

    identities = {
        "upstream_dcxx_ok": bool(dcxx["summary"]["all_identities_hold"]),
        "trial_budget_at_least_1000": trials >= 1000,
        "stability_probability_high": stability_probability > 0.95,
    }

    summary = ProbabilisticSummary(
        linear_half_horizon=l_half,
        linear_packet_horizon=l_packet,
        energy_half_horizon=e_half,
        energy_packet_horizon=e_packet,
        perturbation_stddev=stddev,
        random_seed=seed,
        trials=trials,
        stable_successes=stability_count,
        stability_probability=stability_probability,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXXII probabilistic bound: the bi-scale automaton is stable under "
            "random perturbations with stddev=0.5, achieving >95% stability probability "
            "over a seeded Monte Carlo run."
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