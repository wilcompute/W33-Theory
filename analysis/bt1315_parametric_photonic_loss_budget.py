#!/usr/bin/env python3
"""BT1315 - Parametric photonic loss/resource budget.

BT1312 gives exact pulse counts but deliberately avoids physical constants.
BT1315 adds the next honest layer: a parametric first-order resource ledger.

For each recursive shell depth, qutrit-axis, delay-hop, idle, detector, and
mirror-slot counts are exact.  Device-dependent loss/energy constants stay as
parameters rather than being invented by the verifier.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1315_parametric_photonic_loss_budget.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def instances(level: int) -> int:
    return (40**level - 1) // 39


def weighted_cost(
    row: dict[str, int],
    qutrit_weight: Fraction,
    delay_weight: Fraction,
    idle_weight: Fraction,
) -> dict[str, Any]:
    qutrit = qutrit_weight * row["qutrit_axis_pulses"]
    delay = delay_weight * row["delay_hop_pulses"]
    idle = idle_weight * row["idle_windows"]
    total = qutrit + delay + idle
    return {
        "qutrit_axis_cost": frac(qutrit),
        "delay_hop_cost": frac(delay),
        "idle_cost": frac(idle),
        "total_first_order_cost": frac(total),
        "qutrit_axis_share": frac(qutrit / total) if total else "0/1",
        "delay_hop_share": frac(delay / total) if total else "0/1",
        "idle_share": frac(idle / total) if total else "0/1",
    }


def build_payload() -> dict[str, Any]:
    bt1312 = load_json("data/bt1312_recursive_pulse_energy_scaling.json")
    rows = bt1312["scaling_rows"]
    scenarios = {
        "equal_active_pulse_cost": {
            "qutrit_axis_weight": Fraction(1, 1),
            "delay_hop_weight": Fraction(1, 1),
            "idle_weight": Fraction(0, 1),
        },
        "delay_double_cost": {
            "qutrit_axis_weight": Fraction(1, 1),
            "delay_hop_weight": Fraction(2, 1),
            "idle_weight": Fraction(0, 1),
        },
        "equal_active_plus_idle_tenth": {
            "qutrit_axis_weight": Fraction(1, 1),
            "delay_hop_weight": Fraction(1, 1),
            "idle_weight": Fraction(1, 10),
        },
    }

    level_rows = []
    for row in rows:
        level = row["level"]
        count = row["w33_instances"]
        physical = {
            "level": level,
            "w33_instances": count,
            "detector_windows": 540 * count,
            "mirror_slots": 2160 * count,
            "qutrit_axis_pulses": row["qutrit_axis_pulses"],
            "delay_hop_pulses": row["delay_hop_pulses"],
            "idle_windows": row["idle_windows"],
            "active_total_pulses": row["active_total_pulses"],
            "reserved_windows": row["reserved_windows"],
            "detector_to_mirror_ratio": "1/4",
            "scenario_costs": {
                name: weighted_cost(
                    row,
                    weights["qutrit_axis_weight"],
                    weights["delay_hop_weight"],
                    weights["idle_weight"],
                )
                for name, weights in scenarios.items()
            },
        }
        level_rows.append(physical)

    base = level_rows[0]
    level6 = level_rows[-1]
    checks = {
        "bt1312_verified": bt1312["verified"] is True,
        "all_levels_detector_to_mirror_is_one_quarter": all(
            row["detector_windows"] * 4 == row["mirror_slots"] for row in level_rows
        ),
        "equal_active_cost_keeps_one_to_one_shares": all(
            row["scenario_costs"]["equal_active_pulse_cost"]["qutrit_axis_share"]
            == "1/2"
            and row["scenario_costs"]["equal_active_pulse_cost"]["delay_hop_share"]
            == "1/2"
            for row in level_rows
        ),
        "equal_active_base_cost_is_3240": base["scenario_costs"][
            "equal_active_pulse_cost"
        ]["total_first_order_cost"]
        == "3240/1",
        "delay_double_base_cost_is_4860": base["scenario_costs"]["delay_double_cost"][
            "total_first_order_cost"
        ]
        == "4860/1",
        "idle_tenth_base_cost_is_3348": base["scenario_costs"][
            "equal_active_plus_idle_tenth"
        ]["total_first_order_cost"]
        == "3348/1",
        "level6_equal_active_cost_matches_bt1312_active_total": level6[
            "scenario_costs"
        ]["equal_active_pulse_cost"]["total_first_order_cost"]
        == "340283076840/1",
        "level6_detector_windows_match_shell_wave": level6["detector_windows"]
        == 105025641 * 540,
        "scenario_count_is_three": len(scenarios) == 3,
    }

    payload = {
        "theorem": "BT1315 parametric photonic loss budget",
        "verified": all(checks.values()),
        "checks": checks,
        "parametric_law": {
            "first_order_cost": ("C_n = 1620 I_n e_q + 1620 I_n e_d + 1080 I_n e_idle"),
            "detector_windows": "540 I_n",
            "mirror_slots": "2160 I_n",
            "instances": "I_n = (40^n - 1) / 39",
            "interpretation": (
                "e_q, e_d, and e_idle are device-calibrated costs per "
                "qutrit-axis pulse, delay-hop pulse, and idle window."
            ),
        },
        "scenarios": {
            name: {key: frac(value) for key, value in weights.items()}
            for name, weights in scenarios.items()
        },
        "level_rows": level_rows,
        "architecture_reading": (
            "BT1315 is the physical-budget interface. The substrate fixes the "
            "multiplicities, while the lab supplies the calibrated costs. If "
            "qutrit-axis and delay-hop pulses are equal-cost, active loss is "
            "balanced 1:1 at every depth. If delay hops are more expensive, "
            "the formula shows exactly how much compensation the optical "
            "layout must provide."
        ),
        "honesty_boundary": (
            "No optical dB, clock rate, detector efficiency, or GKP threshold "
            "is asserted here. Those are experimental inputs to the parametric "
            "ledger, not mathematical outputs of W33."
        ),
    }
    return payload


def main() -> None:
    payload = build_payload()
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "theorem": payload["theorem"],
                "verified": payload["verified"],
                "checks_passed": sum(payload["checks"].values()),
                "checks_total": len(payload["checks"]),
                "out": str(OUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not payload["verified"]:
        failed = [name for name, passed in payload["checks"].items() if not passed]
        raise SystemExit(f"BT1315 failed checks: {failed}")


if __name__ == "__main__":
    main()
