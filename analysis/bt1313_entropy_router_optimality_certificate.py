#!/usr/bin/env python3
"""BT1313 - Entropy-router optimality certificate.

BT1310 proved the cyclic mirror router works.  BT1313 records the exact lower
bounds it saturates on the hard cases:

* a one-hot N-packet burst needs at least ceil(N/4) charts;
* in cyclic nonnegative displacement, that burst needs max displacement at
  least ceil(N/4)-1;
* a one-epoch mirror can admit at most 2160 packets.

The BT1310 router reaches all three bounds on the certified stress cases.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1313_entropy_router_optimality_certificate.json"
CHARTS = 540
SERVICE = 4
CAPACITY = CHARTS * SERVICE


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def frac(num: int, den: int) -> str:
    value = Fraction(num, den)
    return f"{value.numerator}/{value.denominator}"


def one_hot_certificate(packets: int) -> dict[str, Any]:
    used = math.ceil(packets / SERVICE) if packets else 0
    full_charts = packets // SERVICE
    remainder = packets % SERVICE
    sum_displacement = SERVICE * full_charts * (full_charts - 1) // 2
    if remainder:
        sum_displacement += remainder * full_charts
    max_displacement = used - 1 if used else 0
    return {
        "packets": packets,
        "minimum_nonempty_charts": used,
        "minimum_max_cyclic_displacement": max_displacement,
        "minimum_total_cyclic_displacement": sum_displacement,
        "minimum_mean_cyclic_displacement": (
            frac(sum_displacement, packets) if packets else "0/1"
        ),
    }


def lower_epoch_bound(packets: int) -> int:
    return math.ceil(packets / CAPACITY) if packets else 0


def build_payload() -> dict[str, Any]:
    bt1310 = load_json("data/bt1310_entropy_preserving_router.json")
    routed = bt1310["routed_cases"]

    one_hot_packet_counts = [1, 4, 5, 8, 9, 540, 2160]
    one_hot = {
        str(packets): one_hot_certificate(packets) for packets in one_hot_packet_counts
    }
    all_to_one = routed["all_to_one_collapse"]
    over_capacity = routed["over_capacity_five_per_chart"]

    checks = {
        "bt1310_verified": bt1310["verified"] is True,
        "all_to_one_nonempty_chart_lower_bound_saturated": all_to_one["nonempty_charts"]
        == one_hot["540"]["minimum_nonempty_charts"]
        == 135,
        "all_to_one_max_displacement_lower_bound_saturated": all_to_one[
            "max_displacement"
        ]
        == one_hot["540"]["minimum_max_cyclic_displacement"]
        == 134,
        "all_to_one_mean_displacement_lower_bound_saturated": frac(
            int(all_to_one["mean_displacement"] * 540), 540
        )
        == one_hot["540"]["minimum_mean_cyclic_displacement"]
        == "67/1",
        "single_hot_boundary_is_one_extra_displacement": routed[
            "single_hot_chart_boundary"
        ]["max_displacement"]
        == 1
        and routed["single_hot_chart_boundary"]["rejected"] == 0,
        "balanced_zero_displacement_is_minimal": routed["balanced_atlas"][
            "max_displacement"
        ]
        == 0
        and routed["balanced_atlas"]["mean_displacement"] == 0,
        "q_and_q_plus_one_zero_displacement_are_minimal": routed["q_per_chart"][
            "max_displacement"
        ]
        == 0
        and routed["saturated_q_plus_1"]["max_displacement"] == 0,
        "one_epoch_capacity_lower_bound": lower_epoch_bound(CAPACITY) == 1
        and lower_epoch_bound(CAPACITY + 1) == 2,
        "over_capacity_rejection_lower_bound_saturated": over_capacity["accepted"]
        == CAPACITY
        and over_capacity["rejected"] == 540,
        "full_capacity_one_hot_certificate_is_substrate": one_hot["2160"][
            "minimum_nonempty_charts"
        ]
        == CHARTS
        and one_hot["2160"]["minimum_max_cyclic_displacement"] == CHARTS - 1,
    }

    payload = {
        "theorem": "BT1313 entropy-router optimality certificate",
        "verified": all(checks.values()),
        "checks": checks,
        "bounds": {
            "charts": CHARTS,
            "service_slots_per_chart": SERVICE,
            "one_epoch_capacity": CAPACITY,
            "epoch_lower_bound": "ceil(total_packets / 2160)",
            "one_hot_nonempty_chart_lower_bound": "ceil(N / 4)",
            "one_hot_max_cyclic_displacement_lower_bound": "ceil(N / 4) - 1",
        },
        "one_hot_certificates": one_hot,
        "bt1310_case_comparison": {
            "balanced_atlas": routed["balanced_atlas"],
            "q_per_chart": routed["q_per_chart"],
            "saturated_q_plus_1": routed["saturated_q_plus_1"],
            "single_hot_chart_boundary": routed["single_hot_chart_boundary"],
            "all_to_one_collapse": all_to_one,
            "over_capacity_five_per_chart": over_capacity,
        },
        "architecture_reading": (
            "BT1313 upgrades BT1310 from a working routing rule to a certified "
            "boundary rule. On the all-to-one hot spot, the router uses the "
            "minimum possible number of charts and the minimum possible "
            "cyclic displacement span. On over-capacity traffic, it rejects "
            "exactly the packets that no one-epoch mirror can admit."
        ),
        "honesty_boundary": (
            "This is an optimality certificate for the finite mirror-slot "
            "model and the cyclic nonnegative router order. It is not a claim "
            "about analog optical switch timing or a globally minimum-cost "
            "routing policy under arbitrary physical costs."
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
        raise SystemExit(f"BT1313 failed checks: {failed}")


if __name__ == "__main__":
    main()
