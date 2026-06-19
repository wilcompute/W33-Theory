#!/usr/bin/env python3
"""BT1312 - Recursive pulse-energy scaling.

BT1309 found that the full atlas activates qutrit-axis and delay-hop controls
in exact 1:1 balance: 1620 and 1620 pulses.  BT1312 checks that the balance is
scale invariant across the recursive W33 shell tower.

For I_n = (40^n - 1)/39 instances, the active pulse vector is:

    (1620 I_n, 1620 I_n).

So the active control families stay balanced at every depth; only the total
number of instances scales.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1312_recursive_pulse_energy_scaling.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def instances(level: int) -> int:
    return (40**level - 1) // 39


def build_payload() -> dict[str, Any]:
    bt1309 = load_json("data/bt1309_photonic_pulse_budget.json")
    bt1311 = load_json("data/bt1311_mirror_admission_control.json")

    base = bt1309["full_atlas_active_budget"]
    rows = []
    for level in range(1, 7):
        count = instances(level)
        qutrit = base["active_qutrit_axis_pulses"] * count
        delay = base["active_delay_hop_pulses"] * count
        idle = base["idle_windows"] * count
        reserved = base["reserved_total_windows"] * count
        rows.append(
            {
                "level": level,
                "w33_instances": count,
                "qutrit_axis_pulses": qutrit,
                "delay_hop_pulses": delay,
                "active_total_pulses": qutrit + delay,
                "idle_windows": idle,
                "reserved_windows": reserved,
                "active_family_ratio": "1:1",
                "compute_utilization": "3/4",
                "mirror_transport_utilization": "1/4",
            }
        )

    checks = {
        "bt1309_verified": bt1309["verified"] is True,
        "bt1311_verified": bt1311["verified"] is True,
        "base_active_families_balanced": base["active_qutrit_axis_pulses"]
        == base["active_delay_hop_pulses"]
        == 1620,
        "all_levels_keep_one_to_one_active_balance": all(
            row["qutrit_axis_pulses"] == row["delay_hop_pulses"] for row in rows
        ),
        "all_levels_keep_three_quarter_compute": all(
            row["active_total_pulses"] * 4 == row["reserved_windows"] * 3
            for row in rows
        ),
        "all_levels_keep_one_quarter_idle": all(
            row["idle_windows"] * 4 == row["reserved_windows"] for row in rows
        ),
        "level6_instance_count_matches_bt1305": rows[-1]["w33_instances"] == 105025641,
        "level6_pulse_vector_is_scaled_base": rows[-1]["qutrit_axis_pulses"]
        == 1620 * 105025641
        and rows[-1]["delay_hop_pulses"] == 1620 * 105025641,
    }

    payload = {
        "theorem": "BT1312 recursive pulse-energy scaling",
        "verified": all(checks.values()),
        "checks": checks,
        "scaling_rows": rows,
        "scale_law": {
            "w33_instances": "I_n = (40^n - 1) / 39",
            "active_pulse_vector": "(1620 I_n, 1620 I_n)",
            "idle_windows": "1080 I_n",
            "reserved_windows": "4320 I_n",
            "interpretation": (
                "Recursive growth multiplies the balanced local control vector "
                "without changing its ratios."
            ),
        },
        "architecture_reading": (
            "BT1312 proves the pulse budget is a true recursive ABI. The "
            "holonet can grow by W33 shell substitution without changing the "
            "active qutrit-axis/delay-hop balance or the 3/4 compute, 1/4 "
            "transport utilization pattern."
        ),
        "honesty_boundary": (
            "BT1312 counts symbolic control pulses. Equal pulse counts are not "
            "a claim of equal optical energy, equal loss, or thermodynamic "
            "zero cost in a physical device."
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
        raise SystemExit(f"BT1312 failed checks: {failed}")


if __name__ == "__main__":
    main()
