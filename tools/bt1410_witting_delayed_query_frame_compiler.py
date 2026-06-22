#!/usr/bin/env python3
"""BT1410: compile the Witting delayed-query protocol into holonet frames.

Vlasov's delayed-query Witting scheme first asks which ray was queried, then
chooses a common tetrad when the two queried rays are same-or-compatible.  The
logical admission table has 520 accepted ordered pairs out of 1600.  The
physical frame compiler needs the basis-local refinement:

    40 tetrads * 4 query slots * 4 query slots = 640 records.

The 480 off-diagonal records are unique compatible pairs.  The 160 diagonal
records are the four-context witness aperture for the 40 same-ray pairs.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    load_json,
    memberships,
)

OUT = ROOT / "data" / "bt1410_witting_delayed_query_frame_compiler.json"


def build_basis_local_records(
    tetrads: list[tuple[int, int, int, int]],
) -> list[dict[str, Any]]:
    records = []
    for basis_id, tetrad in enumerate(tetrads):
        for alice_slot, alice_ray in enumerate(tetrad):
            for bob_slot, bob_ray in enumerate(tetrad):
                same_ray = alice_ray == bob_ray
                records.append(
                    {
                        "basis_id": basis_id,
                        "alice_query_ray": alice_ray,
                        "alice_query_slot": alice_slot,
                        "bob_query_ray": bob_ray,
                        "bob_query_slot": bob_slot,
                        "mode": (
                            "DIAGONAL_WITNESS_APERTURE"
                            if same_ray
                            else "OFF_DIAGONAL_DATA_HANDSHAKE"
                        ),
                        "outcome_slot_residue_domain": [0, 1, 2, 3],
                    }
                )
    return records


def build_logical_pair_records(
    pair_to_bases: dict[tuple[int, int], list[int]],
) -> tuple[list[dict[str, Any]], Counter[str]]:
    records = []
    mode_histogram: Counter[str] = Counter()
    for alice_ray in range(40):
        for bob_ray in range(40):
            common_bases = pair_to_bases.get((alice_ray, bob_ray), [])
            if alice_ray == bob_ray:
                mode = "SAME_RAY_FOUR_BASIS_APERTURE"
            elif len(common_bases) == 1:
                mode = "COMPATIBLE_UNIQUE_BASIS"
            elif not common_bases:
                mode = "INCOMPATIBLE_RETRY_SHADOW"
            else:
                raise AssertionError((alice_ray, bob_ray, common_bases))
            mode_histogram[mode] += 1
            records.append(
                {
                    "alice_query_ray": alice_ray,
                    "bob_query_ray": bob_ray,
                    "common_bases": common_bases,
                    "mode": mode,
                }
            )
    return records, mode_histogram


def slot_in_basis(tetrad: tuple[int, int, int, int], ray: int) -> int:
    return list(tetrad).index(ray)


def build_result() -> dict[str, Any]:
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    ray_to_bases, pair_to_bases = memberships(tetrads)

    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")
    bt1408 = load_json("data/bt1408_witting_contextual_communication_bridge.json")
    bt1409 = load_json("data/bt1409_witting_duplex_admission_scheduler.json")

    basis_local_records = build_basis_local_records(tetrads)
    logical_records, logical_mode_histogram = build_logical_pair_records(pair_to_bases)

    basis_tile_sizes = Counter()
    basis_mode_histograms: dict[int, Counter[str]] = {}
    for record in basis_local_records:
        basis_id = record["basis_id"]
        basis_tile_sizes[basis_id] += 1
        basis_mode_histograms.setdefault(basis_id, Counter())[record["mode"]] += 1

    logical_accepted = [
        record
        for record in logical_records
        if record["mode"] != "INCOMPATIBLE_RETRY_SHADOW"
    ]
    unique_accepted_pairs = {
        (record["alice_query_ray"], record["bob_query_ray"])
        for record in logical_accepted
    }
    basis_local_pair_options = {
        (
            record["alice_query_ray"],
            record["bob_query_ray"],
            record["basis_id"],
        )
        for record in basis_local_records
    }

    distinct_sample = next(
        record
        for record in logical_records
        if record["mode"] == "COMPATIBLE_UNIQUE_BASIS"
    )
    distinct_basis = distinct_sample["common_bases"][0]
    distinct_tetrad = tetrads[distinct_basis]

    same_sample = next(
        record
        for record in logical_records
        if record["mode"] == "SAME_RAY_FOUR_BASIS_APERTURE"
    )
    same_ray = same_sample["alice_query_ray"]

    basis_local_mode_histogram = Counter(
        record["mode"] for record in basis_local_records
    )
    checks = {
        "bt1408_key_rate_loaded": bt1408["verified"] is True
        and bt1408["communication_profile"]["rates"]["key_agreement"] == "13/40",
        "bt1409_duplex_clock_loaded": bt1409["verified"] is True
        and bt1409["rates"]["basis_witness_aperture"] == "1/10",
        "bt1374_outcome_slot_abi_loaded": bt1374["checks"][
            "transversal_is_mirror_slot_mod_4"
        ]
        is True,
        "bt1407_frame_loaded": bt1407["verified"] is True
        and bt1407["frame_identity"]
        == "48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks",
        "logical_pair_table_has_1600_records": len(logical_records) == 1600,
        "logical_pair_histogram_is_40_480_1080": dict(logical_mode_histogram)
        == {
            "SAME_RAY_FOUR_BASIS_APERTURE": 40,
            "COMPATIBLE_UNIQUE_BASIS": 480,
            "INCOMPATIBLE_RETRY_SHADOW": 1080,
        },
        "logical_acceptance_is_520_pairs": len(unique_accepted_pairs) == 520,
        "basis_local_table_has_640_records": len(basis_local_records) == 640,
        "each_basis_tile_is_4_by_4": Counter(basis_tile_sizes.values()) == {16: 40},
        "each_basis_tile_splits_4_diagonal_12_off_diagonal": all(
            hist
            == {
                "DIAGONAL_WITNESS_APERTURE": 4,
                "OFF_DIAGONAL_DATA_HANDSHAKE": 12,
            }
            for hist in basis_mode_histograms.values()
        ),
        "basis_local_mode_histogram_is_160_480": dict(basis_local_mode_histogram)
        == {
            "DIAGONAL_WITNESS_APERTURE": 160,
            "OFF_DIAGONAL_DATA_HANDSHAKE": 480,
        },
        "same_ray_extra_context_options_are_120": len(basis_local_pair_options)
        - len(unique_accepted_pairs)
        == 120,
        "distinct_compatible_pairs_have_unique_basis": all(
            len(record["common_bases"]) == 1
            for record in logical_records
            if record["mode"] == "COMPATIBLE_UNIQUE_BASIS"
        ),
        "same_ray_pairs_have_four_basis_options": all(
            len(record["common_bases"]) == 4
            for record in logical_records
            if record["mode"] == "SAME_RAY_FOUR_BASIS_APERTURE"
        ),
        "rejected_pairs_have_no_basis": all(
            not record["common_bases"]
            for record in logical_records
            if record["mode"] == "INCOMPATIBLE_RETRY_SHADOW"
        ),
    }

    return {
        "bt": 1410,
        "title": "Witting delayed-query frame compiler",
        "verified": all(checks.values()),
        "delayed_query_compiler": {
            "input": "ordered Witting query rays (alice_ray, bob_ray)",
            "reject_rule": "if the pair shares no Witting tetrad, classify as retry shadow",
            "distinct_accept_rule": (
                "if alice_ray != bob_ray and the pair is orthogonal, use the "
                "unique common tetrad as the frame basis"
            ),
            "same_accept_rule": (
                "if alice_ray == bob_ray, the pair has four common tetrads; "
                "a two-bit aperture selector chooses one witness basis"
            ),
            "frame_rule": (
                "after basis selection, open one BT1407 72-tick transaction; "
                "the later outcome slot is compiled by BT1374 as mirror_slot mod 4"
            ),
        },
        "logical_pair_table": {
            "records": len(logical_records),
            "mode_histogram": dict(logical_mode_histogram),
            "accepted_ordered_pairs": len(unique_accepted_pairs),
            "rejected_ordered_pairs": logical_mode_histogram[
                "INCOMPATIBLE_RETRY_SHADOW"
            ],
            "accept_rate": "13/40",
            "reject_rate": "27/40",
        },
        "basis_local_frame_table": {
            "records": len(basis_local_records),
            "factorization": "40 tetrads * 4 Alice query slots * 4 Bob query slots",
            "mode_histogram": dict(basis_local_mode_histogram),
            "basis_tile_histogram": {
                str(key): value
                for key, value in sorted(Counter(basis_tile_sizes.values()).items())
            },
            "same_ray_extra_context_options": len(basis_local_pair_options)
            - len(unique_accepted_pairs),
            "reading": (
                "The physical table is larger than the logical accepted-pair "
                "table only because same-ray queries are contextual apertures: "
                "each ray lives in four bases."
            ),
        },
        "sample_compilations": {
            "distinct_compatible": {
                "alice_query_ray": distinct_sample["alice_query_ray"],
                "bob_query_ray": distinct_sample["bob_query_ray"],
                "selected_basis": distinct_basis,
                "alice_query_slot": slot_in_basis(
                    distinct_tetrad, distinct_sample["alice_query_ray"]
                ),
                "bob_query_slot": slot_in_basis(
                    distinct_tetrad, distinct_sample["bob_query_ray"]
                ),
                "basis_options": distinct_sample["common_bases"],
                "mode": distinct_sample["mode"],
            },
            "same_ray": {
                "query_ray": same_ray,
                "basis_options": same_sample["common_bases"],
                "aperture_selector_domain": [0, 1, 2, 3],
                "selected_basis_if_selector_is_0": same_sample["common_bases"][0],
                "query_slot_in_each_basis": {
                    str(basis_id): slot_in_basis(tetrads[basis_id], same_ray)
                    for basis_id in same_sample["common_bases"]
                },
                "mode": same_sample["mode"],
            },
        },
        "holonet_transaction": {
            "bt1407_frame_ticks": 72,
            "bt1407_frame_identity": bt1407["frame_identity"],
            "bt1374_address_rule": bt1374["address_rule"]["formula"],
            "outcome_slot_residue_domain": [0, 1, 2, 3],
            "basis_local_table_factorization": "40*4*4=640",
            "physical_reading": (
                "The Witting 40-card desk becomes a packet admission ROM.  "
                "Off-diagonal entries carry compatible communication pairs; "
                "diagonal entries are the contextual audit apertures."
            ),
        },
        "source_bridge": {
            "vlasov_arxiv": "2503.18431",
            "external_idea": (
                "delayed query followed by classical exchange of selected states "
                "and a postponed common-basis measurement"
            ),
            "local_upgrade": (
                "the common basis is compiled into a BT1407 frame and its four "
                "outcome slots are exactly BT1374 mirror-slot residues"
            ),
        },
        "basis_local_records_sample": basis_local_records[:16],
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "basis_local_records": result["basis_local_frame_table"]["records"],
                "bt": result["bt"],
                "off_diagonal_data_records": result["basis_local_frame_table"][
                    "mode_histogram"
                ]["OFF_DIAGONAL_DATA_HANDSHAKE"],
                "same_ray_witness_records": result["basis_local_frame_table"][
                    "mode_histogram"
                ]["DIAGONAL_WITNESS_APERTURE"],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
