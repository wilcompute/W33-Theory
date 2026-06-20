#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def queue_case(name: str, service_per_microframe: float, demand_per_microframe: float, microframes: int) -> dict:
    rho = demand_per_microframe / service_per_microframe if service_per_microframe else float("inf")
    stable = rho < 1.0
    produced = service_per_microframe * microframes
    demanded = demand_per_microframe * microframes
    slack = produced - demanded
    # M/M/1 style envelope for first-order queue risk, only meaningful if stable.
    expected_backlog = (rho * rho / (1 - rho)) if stable else float("inf")
    expected_wait_microframes = (rho / (service_per_microframe - demand_per_microframe)) if stable else float("inf")
    return {
        "name": name,
        "service_per_microframe": service_per_microframe,
        "demand_per_microframe": demand_per_microframe,
        "microframes_per_51840_window": microframes,
        "rho": rho,
        "stable": stable,
        "expected_successful_tokens_per_window": produced,
        "expected_demand_tokens_per_window": demanded,
        "expected_slack_tokens_per_window": slack,
        "expected_backlog_tokens_mm1_envelope": expected_backlog,
        "expected_wait_microframes_mm1_envelope": expected_wait_microframes
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1391_hesse_sic_t_queue_model.json")
    ns = ap.parse_args()
    factory = load("data/bt1388_hesse_sic_t_factory_model.json")
    services = {row["name"]: row["successes_per_microframe"] for row in factory["rows"]}
    microframes = 51840 // 72
    rows = [
        queue_case("baseline_light", services["baseline"], 0.25, microframes),
        queue_case("baseline_medium", services["baseline"], 0.50, microframes),
        queue_case("baseline_heavy", services["baseline"], 0.80, microframes),
        queue_case("conservative_medium", services["conservative"], 0.25, microframes),
        queue_case("aggressive_heavy", services["aggressive"], 1.25, microframes)
    ]
    checks = {
        "factory_verified": factory["verified"] is True,
        "window_has_720_microframes": microframes == 720,
        "baseline_medium_stable": rows[1]["stable"] is True,
        "baseline_heavy_stable": rows[2]["stable"] is True,
        "conservative_medium_stable": rows[3]["stable"] is True,
        "aggressive_heavy_stable": rows[4]["stable"] is True,
        "all_slack_positive": all(row["expected_slack_tokens_per_window"] > 0 for row in rows)
    }
    result = {
        "bt": 1391,
        "title": "Hesse SIC T queueing envelope over one Clifford window",
        "verified": all(checks.values()),
        "checks": checks,
        "window": {"ticks": 51840, "microframe_ticks": 72, "microframes": microframes},
        "rows": rows,
        "boundary": "Queueing envelope only. It assumes independent service and demand rates and does not model correlated optical/resource-factory faults."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1391, "verified": result["verified"], "microframes": microframes}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
