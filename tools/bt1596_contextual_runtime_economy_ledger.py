#!/usr/bin/env python3
"""BT1596: ledger for Witting communication rail versus contextual fuel rail."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1596_contextual_runtime_economy_ledger.json"
MD = ROOT / "analysis" / "BT1596_contextual_runtime_economy_ledger.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    witting = load_json("data/bt1408_witting_contextual_communication_bridge.json")
    duplex = load_json("data/bt1409_witting_duplex_admission_scheduler.json")
    delayed = load_json("data/bt1410_witting_delayed_query_frame_compiler.json")
    fuel = load_json("data/bt1595_witting_matter_fuel_bijection.json")
    hesse_loop = load_json("data/bt1594_hesse_t_universality_witness_loop.json")

    ordered_counts = witting["communication_profile"]["ordered_pair_counts"]
    frame_ticks = 72
    accepted_pairs = ordered_counts["compatible_total"]
    rejected_pairs = ordered_counts["incompatible"]
    all_pairs = ordered_counts["total"]
    same_pairs = ordered_counts["same"]
    compatible_distinct = ordered_counts["compatible_distinct"]
    basis_local = delayed["basis_local_frame_table"]
    basis_records = basis_local["records"]
    diagonal_records = basis_local["mode_histogram"]["DIAGONAL_WITNESS_APERTURE"]
    off_diagonal_records = basis_local["mode_histogram"]["OFF_DIAGONAL_DATA_HANDSHAKE"]
    extra_same_contexts = basis_local["same_ray_extra_context_options"]

    ledger = {
        "accepted_communication": {
            "frames": accepted_pairs,
            "ticks": accepted_pairs * frame_ticks,
            "rate": fraction_text(Fraction(accepted_pairs, all_pairs)),
            "meaning": "same or basis-compatible Witting ordered pairs",
        },
        "contextual_fuel": {
            "frames": rejected_pairs,
            "ticks": rejected_pairs * frame_ticks,
            "rate": fraction_text(Fraction(rejected_pairs, all_pairs)),
            "meaning": "incompatible Witting ordered pairs, now BT1595 fuel segments",
        },
        "complete_witting_pair_cycle": {
            "frames": all_pairs,
            "ticks": all_pairs * frame_ticks,
            "rate": "1/1",
            "meaning": "all delayed-query ordered pairs at one 72-tick frame each",
        },
        "basis_local_physical_table": {
            "frames": basis_records,
            "ticks": basis_records * frame_ticks,
            "rate_against_ordered_pairs": fraction_text(
                Fraction(basis_records, all_pairs)
            ),
            "meaning": "40 tetrads * 4 Alice slots * 4 Bob slots",
        },
        "same_ray_extra_contexts": {
            "frames": extra_same_contexts,
            "ticks": extra_same_contexts * frame_ticks,
            "rate_against_ordered_pairs": fraction_text(
                Fraction(extra_same_contexts, all_pairs)
            ),
            "meaning": "the extra three witness contexts for each same-ray query",
        },
    }
    checks = {
        "witting_verified": witting["verified"] is True,
        "duplex_verified": duplex["verified"] is True,
        "delayed_query_verified": delayed["verified"] is True,
        "fuel_bijection_verified": fuel["verified"] is True,
        "hesse_loop_verified": hesse_loop["verified"] is True,
        "ordered_pair_split_is_520_1080": (accepted_pairs, rejected_pairs, all_pairs)
        == (520, 1080, 1600),
        "communication_to_fuel_ratio_is_13_to_27": Fraction(
            accepted_pairs, rejected_pairs
        )
        == Fraction(13, 27),
        "accepted_plus_fuel_ticks_make_complete_cycle": ledger[
            "accepted_communication"
        ]["ticks"]
        + ledger["contextual_fuel"]["ticks"]
        == ledger["complete_witting_pair_cycle"]["ticks"],
        "fuel_ticks_equal_bt1594": ledger["contextual_fuel"]["ticks"]
        == hesse_loop["overlay_identity"]["total_ticks"]
        == 77760,
        "basis_local_table_is_480_plus_160": (off_diagonal_records, diagonal_records)
        == (480, 160),
        "same_ray_extra_contexts_are_120": extra_same_contexts
        == basis_records - accepted_pairs
        == 120,
        "duplex_rates_match": duplex["rates"]["state_accept_unique"] == "13/40"
        and duplex["rates"]["state_reject_unique"] == "27/40"
        and duplex["rates"]["basis_witness_aperture"] == "1/10",
        "hesse_outcomes_scale_with_fuel_frames": sum(
            hesse_loop["hesse_outcome_counts"].values()
        )
        == rejected_pairs * 9,
        "same_plus_compatible_distinct_are_accepted": same_pairs + compatible_distinct
        == accepted_pairs,
    }
    result = {
        "bt": 1596,
        "title": "Contextual runtime economy ledger",
        "verified": all(checks.values()),
        "source_packets": {
            "witting_bridge": "data/bt1408_witting_contextual_communication_bridge.json",
            "duplex_admission": "data/bt1409_witting_duplex_admission_scheduler.json",
            "delayed_query_frames": "data/bt1410_witting_delayed_query_frame_compiler.json",
            "fuel_bijection": "data/bt1595_witting_matter_fuel_bijection.json",
            "hesse_t_loop": "data/bt1594_hesse_t_universality_witness_loop.json",
        },
        "frame_ticks": frame_ticks,
        "ordered_pair_counts": {
            "same": same_pairs,
            "compatible_distinct": compatible_distinct,
            "accepted": accepted_pairs,
            "contextual_fuel": rejected_pairs,
            "total": all_pairs,
        },
        "runtime_ledger": ledger,
        "ratios": {
            "accepted_to_fuel": "13/27",
            "accepted_to_total": "13/40",
            "fuel_to_total": "27/40",
            "basis_witness_aperture": "1/10",
            "same_ray_extra_contexts_to_total": "3/40",
        },
        "interpretation": (
            "BT1596 turns the Witting delayed-query desk into a runtime economy. "
            "The 13/40 accepted rail is communication/control. The 27/40 rejected "
            "rail is not waste: by BT1595 it is exactly the 77760-tick contextual "
            "fuel loop carrying the Hesse/T port."
        ),
        "honesty_boundary": (
            "This is a finite scheduling/economy ledger. It does not prove "
            "cryptographic security, throughput under loss, or fault-tolerant threshold behavior."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1596 Contextual Runtime Economy Ledger\n\n"
        "BT1596 splits the complete Witting ordered-pair desk into a communication "
        "rail and a contextual-fuel rail:\n\n"
        "```text\n"
        "520 accepted pairs * 72 ticks = 37440 ticks\n"
        "1080 rejected pairs * 72 ticks = 77760 ticks\n"
        "1600 total pairs * 72 ticks = 115200 ticks\n"
        "accepted:fuel = 13:27\n"
        "```\n\n"
        "The rejected rail is exactly the BT1595/BT1594 OAM-Hesse witness loop.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1596,
                "verified": result["verified"],
                "accepted_ticks": ledger["accepted_communication"]["ticks"],
                "fuel_ticks": ledger["contextual_fuel"]["ticks"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
