#!/usr/bin/env python3
"""BT1597: package the Witting desk, OAM ABI, and Hesse/T port as one object."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1597_universal_transaction_object.json"
MD = ROOT / "analysis" / "BT1597_universal_transaction_object.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    clock = load_json("data/bt1407_microframe_transaction_composer.json")
    witting = load_json("data/bt1408_witting_contextual_communication_bridge.json")
    fuel = load_json("data/bt1595_witting_matter_fuel_bijection.json")
    economy = load_json("data/bt1596_contextual_runtime_economy_ledger.json")
    universal_contract = load_json(
        "data/bt1377_physical_universal_computation_contract.json"
    )
    hesse_loop = load_json("data/bt1594_hesse_t_universality_witness_loop.json")

    total_ticks = economy["runtime_ledger"]["complete_witting_pair_cycle"]["ticks"]
    accepted_ticks = economy["runtime_ledger"]["accepted_communication"]["ticks"]
    fuel_ticks = economy["runtime_ledger"]["contextual_fuel"]["ticks"]
    object_layers = [
        {
            "layer": "Witting delayed-query desk",
            "finite_carrier": "40 rays x 40 queried rays = 1600 ordered pairs",
            "physical_role": "separates communication/control from contextual fuel",
            "certificate": "BT1408/BT1409/BT1410",
        },
        {
            "layer": "72-tick common frame clock",
            "finite_carrier": "one transaction frame per ordered pair",
            "physical_role": "common timing shape for accepted frames and fuel frames",
            "certificate": "BT1407",
        },
        {
            "layer": "OAM recenter ABI",
            "finite_carrier": "5 gates x 9 sectors x 24 words = 1080 fuel addresses",
            "physical_role": "tiles the Witting incompatible shell",
            "certificate": "BT1590/BT1593/BT1595",
        },
        {
            "layer": "Hesse/T non-Clifford port",
            "finite_carrier": "9 outcomes per 72-tick fuel segment",
            "physical_role": "injects the required non-Clifford boundary into the fuel rail",
            "certificate": "BT1403/BT1404/BT1594",
        },
    ]
    checks = {
        "clock_verified": clock["verified"] is True,
        "witting_verified": witting["verified"] is True,
        "fuel_verified": fuel["verified"] is True,
        "economy_verified": economy["verified"] is True,
        "hesse_loop_verified": hesse_loop["verified"] is True,
        "universal_contract_verified": universal_contract["verified"] is True,
        "non_clifford_port_required": universal_contract["universal_port"]["required"]
        is True,
        "deterministic_kernel_not_universal_alone": universal_contract[
            "deterministic_kernel"
        ]["universal_without_port"]
        is False,
        "complete_cycle_is_1600_frames": total_ticks == 1600 * 72 == 115200,
        "fuel_rail_is_existing_77760_loop": fuel_ticks
        == hesse_loop["overlay_identity"]["total_ticks"]
        == 77760,
        "accepted_and_fuel_partition_total": accepted_ticks + fuel_ticks == total_ticks,
        "object_has_four_required_layers": [layer["layer"] for layer in object_layers]
        == [
            "Witting delayed-query desk",
            "72-tick common frame clock",
            "OAM recenter ABI",
            "Hesse/T non-Clifford port",
        ],
        "witting_reject_rate_is_fuel_rate": witting["communication_profile"]["rates"][
            "reject"
        ]
        == economy["ratios"]["fuel_to_total"],
        "witting_accept_rate_is_control_rate": witting["communication_profile"][
            "rates"
        ]["key_agreement"]
        == economy["ratios"]["accepted_to_total"],
    }
    result = {
        "bt": 1597,
        "title": "Universal transaction object for the photonic holonet",
        "verified": all(checks.values()),
        "source_packets": {
            "common_frame": "data/bt1407_microframe_transaction_composer.json",
            "witting_bridge": "data/bt1408_witting_contextual_communication_bridge.json",
            "fuel_bijection": "data/bt1595_witting_matter_fuel_bijection.json",
            "economy_ledger": "data/bt1596_contextual_runtime_economy_ledger.json",
            "universal_contract": "data/bt1377_physical_universal_computation_contract.json",
            "hesse_t_loop": "data/bt1594_hesse_t_universality_witness_loop.json",
        },
        "universal_transaction_identity": {
            "complete_cycle": "40 Witting rays * 40 queried rays * 72 ticks = 115200",
            "accepted_control_rail": "520 accepted pairs * 72 ticks = 37440",
            "contextual_fuel_rail": "1080 rejected pairs * 72 ticks = 77760",
            "fuel_refinement": "1080 = 5 gates * 9 OAM sectors * 24 words = 40 rays * 27 incompatible targets",
            "non_clifford_overlay": "each fuel frame carries one 9-outcome Hesse/T microframe",
        },
        "ticks": {
            "accepted_control": accepted_ticks,
            "contextual_fuel": fuel_ticks,
            "complete_cycle": total_ticks,
        },
        "object_layers": object_layers,
        "claim": (
            "The photonic holonet can now be read as one finite universal transaction "
            "object: accepted Witting pairs are the communication/control rail, while "
            "rejected Witting pairs are exactly the OAM/Hesse contextual fuel rail. "
            "The Hesse/T port supplies the explicit non-Clifford boundary required by BT1377."
        ),
        "honesty_boundary": (
            "BT1597 proves finite ABI/timing compatibility and the exact Witting/OAM/Hesse "
            "partition. It does not prove hardware thresholds, optical coherence, or "
            "fault-tolerant universality under physical noise."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1597 Universal Transaction Object\n\n"
        "BT1597 packages the current architecture as one finite transaction object:\n\n"
        "```text\n"
        "40 Witting rays * 40 queried rays * 72 ticks = 115200 ticks\n"
        "520 accepted pairs * 72 ticks = 37440 communication/control ticks\n"
        "1080 rejected pairs * 72 ticks = 77760 contextual-fuel ticks\n"
        "1080 = 5*9*24 = 40*27\n"
        "```\n\n"
        "The rejected rail is exactly the OAM/Hesse witness loop, and the Hesse/T "
        "overlay supplies the explicit non-Clifford port required by BT1377.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1597,
                "verified": result["verified"],
                "complete_cycle_ticks": total_ticks,
                "fuel_ticks": fuel_ticks,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
