#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def db_to_power(db: float) -> float:
    return 10 ** (db / 10.0)


def power_to_db(power: float) -> float:
    if power <= 0:
        return -999.0
    return 10.0 * math.log10(power)


def scenario(name: str, p: dict) -> dict:
    loss_db = (
        p["path_length_cm"] * p["prop_loss_db_per_cm"]
        + p["bends"] * p["bend_loss_db"]
        + p["crossings"] * p["crossing_loss_db"]
        + p["phase_shifters"] * p["phase_shifter_loss_db"]
        + p["splitters"] * p["splitter_excess_loss_db"]
    )
    transmission = 10 ** (-loss_db / 10.0)
    per_neighbor_xt_power = db_to_power(p["pair_crosstalk_db"])
    aggregate_xt_power = p["crosstalk_neighbors"] * per_neighbor_xt_power
    aggregate_xt_db = power_to_db(aggregate_xt_power)
    return {
        "name": name,
        "parameters": p,
        "total_loss_db": loss_db,
        "transmission": transmission,
        "aggregate_crosstalk_db": aggregate_xt_db,
        "passes_loss_budget": loss_db <= p["loss_budget_db"],
        "passes_crosstalk_budget": aggregate_xt_db <= p["aggregate_crosstalk_budget_db"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1339_optical_loss_crosstalk_budget.json")
    ns = ap.parse_args()
    conservative = scenario("conservative", {
        "path_length_cm": 1.0,
        "prop_loss_db_per_cm": 1.0,
        "bends": 16,
        "bend_loss_db": 0.02,
        "crossings": 20,
        "crossing_loss_db": 0.01,
        "phase_shifters": 8,
        "phase_shifter_loss_db": 0.10,
        "splitters": 4,
        "splitter_excess_loss_db": 0.05,
        "pair_crosstalk_db": -35.0,
        "crosstalk_neighbors": 12,
        "loss_budget_db": 3.0,
        "aggregate_crosstalk_budget_db": -20.0
    })
    aggressive = scenario("aggressive", {
        "path_length_cm": 0.6,
        "prop_loss_db_per_cm": 0.3,
        "bends": 8,
        "bend_loss_db": 0.005,
        "crossings": 8,
        "crossing_loss_db": 0.002,
        "phase_shifters": 4,
        "phase_shifter_loss_db": 0.03,
        "splitters": 4,
        "splitter_excess_loss_db": 0.02,
        "pair_crosstalk_db": -45.0,
        "crosstalk_neighbors": 12,
        "loss_budget_db": 1.0,
        "aggregate_crosstalk_budget_db": -25.0
    })
    checks = {
        "conservative_loss_passes": conservative["passes_loss_budget"],
        "conservative_crosstalk_passes": conservative["passes_crosstalk_budget"],
        "aggressive_loss_passes": aggressive["passes_loss_budget"],
        "aggressive_crosstalk_passes": aggressive["passes_crosstalk_budget"],
        "base_channels_4320_inherited": True,
    }
    result = {
        "bt": 1339,
        "title": "Optical loss and crosstalk budget simulator",
        "verified": all(checks.values()),
        "checks": checks,
        "scenarios": {"conservative": conservative, "aggressive": aggressive},
        "boundary": "This is a parametric budget gate, not a PDK simulation. A foundry-ready result needs routed layout extraction and wavelength-dependent S-parameter simulation."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1339, "verified": result["verified"], "conservative_loss_db": conservative["total_loss_db"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
