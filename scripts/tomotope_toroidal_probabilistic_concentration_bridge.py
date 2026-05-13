#!/usr/bin/env python3
"""Part DCXXV: probabilistic concentration bridge.

Builds a statistical confidence certificate on top of DCXXII stability sampling.
Uses the Wilson score lower bound for Bernoulli success probability.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCXXII_PATH = ROOT / "data" / "tomotope_toroidal_probabilistic_bound_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_probabilistic_concentration_bridge.json"


def _load_json_or_build(path: Path, module_name: str) -> dict[str, Any]:
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        summary = payload.get("summary", {})
        required = {"random_seed", "trials", "stable_successes"}
        if required.issubset(summary.keys()):
            return payload
    module = __import__(module_name, fromlist=["build_bridge"])
    return module.build_bridge()


def _wilson_lower_bound(successes: int, trials: int, z: float) -> float:
    if trials <= 0:
        raise ValueError("trials must be positive")
    phat = successes / trials
    z2 = z * z
    denom = 1.0 + z2 / trials
    center = phat + z2 / (2.0 * trials)
    margin = z * math.sqrt((phat * (1.0 - phat) + z2 / (4.0 * trials)) / trials)
    return (center - margin) / denom


@dataclass(frozen=True)
class ConcentrationSummary:
    perturbation_stddev: float
    random_seed: int
    trials: int
    stable_successes: int
    stability_probability: float
    confidence_z: float
    wilson_lower_bound: float
    all_identities_hold: bool


def build_bridge(z_value: float = 2.5758293035489004) -> dict[str, Any]:
    # z=2.5758... corresponds to ~99% two-sided confidence
    dcxxii = _load_json_or_build(
        DCXXII_PATH, "scripts.tomotope_toroidal_probabilistic_bound_bridge"
    )
    summary = dcxxii["summary"]

    trials = int(summary["trials"])
    successes = int(summary["stable_successes"])
    p = float(summary["stability_probability"])
    lower = _wilson_lower_bound(successes, trials, z_value)

    identities = {
        "upstream_dcxxii_ok": bool(summary["all_identities_hold"]),
        "trials_large_enough": trials >= 1000,
        "success_count_valid": 0 <= successes <= trials,
        "sample_probability_high": p > 0.95,
        "wilson_lower_bound_high": lower > 0.95,
        "lower_bound_not_above_sample": lower <= p,
    }

    result = ConcentrationSummary(
        perturbation_stddev=float(summary["perturbation_stddev"]),
        random_seed=int(summary["random_seed"]),
        trials=trials,
        stable_successes=successes,
        stability_probability=p,
        confidence_z=z_value,
        wilson_lower_bound=lower,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(result),
        "identities": identities,
        "notes": (
            "DCXXV concentration certificate: beyond high sample stability, the 99% "
            "Wilson lower confidence bound also clears 0.95, making the probabilistic "
            "claim statistically robust."
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
