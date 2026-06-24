#!/usr/bin/env python3
"""BT1706 - symbolic retry economics for the Holonet packet ABI.

BT1703 classifies symbolic faults.  BT1706 attaches parameterized probabilities
to those fault hooks and computes expected retry, local termination, and CSS
handoff load without claiming measured hardware rates.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from bt1703_holonet_fault_propagation_simulator import build_certificate as build_faults
from bt1705_holonet_shared_bus_time_division_simulator import (
    build_certificate as build_bus,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1706_holonet_retry_economics.json"

PROFILES = {
    "nominal_low": {
        "LOSS": Fraction(1, 100000),
        "DARK_CLICK": Fraction(1, 1000000),
        "PARITY": Fraction(1, 200000),
    },
    "engineering_upper_10pct_guard": {
        "LOSS": Fraction(7, 48000),
        "DARK_CLICK": Fraction(21, 16000),
        "PARITY": Fraction(7, 24000),
    },
    "guard_budget_limit": {
        "LOSS": Fraction(7, 4800),
        "DARK_CLICK": Fraction(21, 1600),
        "PARITY": Fraction(7, 2400),
    },
}

CYCLE_FRAMES = 1600
GUARD_BUDGETS = {
    "LOSS": 168,
    "DARK_CLICK": 168,
    "PARITY": 112,
}


def fraction_json(value: Fraction) -> dict[str, Any]:
    return {
        "fraction": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def expected_by_exit(
    fault_rows: list[dict[str, Any]], rates: dict[str, Fraction]
) -> dict[str, Fraction]:
    totals: dict[str, Fraction] = {}
    for row in fault_rows:
        totals[row["exit"]] = (
            totals.get(row["exit"], Fraction(0)) + rates[row["fault_type"]]
        )
    return totals


def profile_result(
    name: str, fault_rows: list[dict[str, Any]], rates: dict[str, Fraction]
) -> dict[str, Any]:
    type_counts = Counter(row["fault_type"] for row in fault_rows)
    per_packet_type = {
        fault_type: Fraction(count) * rates[fault_type]
        for fault_type, count in type_counts.items()
    }
    per_cycle_type = {
        fault_type: value * CYCLE_FRAMES
        for fault_type, value in per_packet_type.items()
    }
    exit_totals = expected_by_exit(fault_rows, rates)
    retry_per_packet = exit_totals.get("RETRY_FRAME", Fraction(0)) + exit_totals.get(
        "LOCAL_REPROGRAM_RETRY", Fraction(0)
    )
    css_per_packet = exit_totals.get("CSS_SYNDROME_HANDOFF", Fraction(0))
    local_per_packet = exit_totals.get(
        "LOCAL_DARK_CLOSEOUT", Fraction(0)
    ) + exit_totals.get("LOCAL_DARK_REFERENCE_TERMINATION", Fraction(0))
    guard_pressure = {
        fault_type: Fraction(per_cycle_type[fault_type], GUARD_BUDGETS[fault_type])
        for fault_type in GUARD_BUDGETS
    }
    return {
        "profile": name,
        "rates": {
            fault_type: fraction_json(rate) for fault_type, rate in rates.items()
        },
        "expected_per_packet_by_fault_type": {
            fault_type: fraction_json(value)
            for fault_type, value in sorted(per_packet_type.items())
        },
        "expected_per_1600_frame_cycle_by_fault_type": {
            fault_type: fraction_json(value)
            for fault_type, value in sorted(per_cycle_type.items())
        },
        "expected_per_packet_by_exit": {
            exit_name: fraction_json(value)
            for exit_name, value in sorted(exit_totals.items())
        },
        "expected_retry_or_reprogram_per_packet": fraction_json(retry_per_packet),
        "expected_css_handoff_per_packet": fraction_json(css_per_packet),
        "expected_local_termination_per_packet": fraction_json(local_per_packet),
        "guard_budget_pressure": {
            fault_type: fraction_json(value)
            for fault_type, value in sorted(guard_pressure.items())
        },
        "within_guard_budget": all(value <= 1 for value in guard_pressure.values()),
    }


def build_certificate() -> dict[str, Any]:
    faults = build_faults()
    bus = build_bus()
    fault_rows = faults["fault_rows"]
    results = [
        profile_result(name, fault_rows, rates) for name, rates in PROFILES.items()
    ]
    checks = {
        "bt1703_verified": faults["verified"] is True,
        "bt1705_verified": bus["verified"] is True,
        "profiles_are_deterministic": [row["profile"] for row in results]
        == list(PROFILES),
        "all_profiles_within_guard_budget": all(
            row["within_guard_budget"] for row in results
        ),
        "guard_limit_reaches_unit_pressure": all(
            results[-1]["guard_budget_pressure"][fault_type]["fraction"] == "1/1"
            for fault_type in ("LOSS", "DARK_CLICK", "PARITY")
        ),
        "nominal_retry_load_is_less_than_one_packet": Fraction(
            results[0]["expected_retry_or_reprogram_per_packet"]["fraction"]
        )
        < 1,
        "css_load_comes_only_from_parity_faults": all(
            row["expected_css_handoff_per_packet"]["fraction"]
            == row["expected_per_packet_by_fault_type"]["PARITY"]["fraction"]
            for row in results
        ),
    }
    return {
        "theorem": "BT1706 Holonet Retry Economics",
        "verified": all(checks.values()),
        "breakthrough": (
            "The symbolic fault exits now have deterministic economics: for any "
            "declared loss/dark/parity rates, the verifier computes retry load, "
            "CSS handoff load, local termination load, and guard-budget pressure."
        ),
        "cycle_frames": CYCLE_FRAMES,
        "guard_budgets_per_cycle": GUARD_BUDGETS,
        "profiles": results,
        "source_certificates": [
            "data/bt1703_holonet_fault_propagation_simulator.json",
            "data/bt1705_holonet_shared_bus_time_division_simulator.json",
        ],
        "claim_boundary": [
            "Rates are input parameters, not measured hardware constants.",
            "The verifier computes ABI load once rates are supplied; it does not assert a physical threshold.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    for profile in cert["profiles"]:
        print(
            f"  {profile['profile']}: retry={profile['expected_retry_or_reprogram_per_packet']['fraction']}, "
            f"css={profile['expected_css_handoff_per_packet']['fraction']}"
        )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
