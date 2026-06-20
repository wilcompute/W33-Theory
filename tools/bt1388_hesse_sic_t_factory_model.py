#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def case(name: str, rate: float, pt: float, pm: float, pf: float, pr: float, ticks: int) -> dict:
    p = pt * pm * pf * pr
    return {
        "name": name,
        "token_rate_per_microframe": rate,
        "p_token": pt,
        "p_measure": pm,
        "p_feedforward": pf,
        "p_restore": pr,
        "p_success": p,
        "expected_attempts": 1.0 / p,
        "ticks_per_attempt": ticks,
        "expected_ticks": ticks / p,
        "successes_per_microframe": rate * p
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1388_hesse_sic_t_factory_model.json")
    ns = ap.parse_args()
    abi = load("data/bt1385_hesse_sic_t_port_abi.json")
    rows = [
        case("baseline", 1.0, 0.90, 0.98, 0.995, 0.999, 72),
        case("conservative", 0.5, 0.80, 0.95, 0.990, 0.995, 144),
        case("aggressive", 2.0, 0.96, 0.995, 0.999, 0.9995, 72)
    ]
    checks = {
        "abi_verified": abi["verified"] is True,
        "sic_outcomes_9": abi["resource_token"]["sic_outcomes"] == 9,
        "all_success_positive": all(r["p_success"] > 0 for r in rows),
        "baseline_expected_attempts_lt_1p2": rows[0]["expected_attempts"] < 1.2,
        "aggressive_best_throughput": rows[2]["successes_per_microframe"] > rows[0]["successes_per_microframe"] > rows[1]["successes_per_microframe"]
    }
    result = {
        "bt": 1388,
        "title": "Hesse SIC T resource factory envelope",
        "verified": all(checks.values()),
        "checks": checks,
        "rows": rows,
        "boundary": "Stochastic ABI envelope only; no physical factory certificate."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1388, "verified": result["verified"], "baseline_success": rows[0]["p_success"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
