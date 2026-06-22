#!/usr/bin/env python3
"""BT1411: compile Witting tetrads into physical analyzer unitaries.

BT1410 tells the holonet which Witting tetrad opens a frame.  BT1411 adds the
optical analyzer: for each tetrad B=(r0,r1,r2,r3), build the 4x4 unitary whose
rows are the conjugate Witting rays.  Then U_B |r_j> = |j>, so the four detector
slots are exactly the mirror-slot residues used by the packet ABI.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    load_json,
)

OUT = ROOT / "data" / "bt1411_witting_basis_analyzer_unitaries.json"


def analyzer_for_tetrad(
    rays: list[np.ndarray], tetrad: tuple[int, int, int, int]
) -> np.ndarray:
    return np.vstack([np.conjugate(rays[ray]) for ray in tetrad])


def support_weight(ray: np.ndarray) -> int:
    return int(np.count_nonzero(np.abs(ray) > 1e-8))


def optical_family(support_profile: list[int]) -> str:
    profile = sorted(support_profile)
    if profile == [1, 1, 1, 1]:
        return "COMPUTATIONAL_DIRECT_RAILS"
    if profile == [1, 3, 3, 3]:
        return "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER"
    if profile == [3, 3, 3, 3]:
        return "FOUR_THREE_RAIL_WITTING_ROWS"
    raise AssertionError(profile)


def token_for_entry(value: complex) -> str:
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    candidates: list[tuple[float, str]] = [(abs(value), "0")]
    roots = [
        ("1", 1),
        ("omega", omega),
        ("omega2", omega**2),
        ("-1", -1),
        ("-omega", -omega),
        ("-omega2", -(omega**2)),
    ]
    for name, root in roots:
        candidates.append((abs(value - root), name))
        candidates.append((abs(value - root / sqrt3), f"{name}/sqrt3"))
    distance, token = min(candidates, key=lambda item: item[0])
    if distance > 1e-8:
        raise AssertionError((value, distance, token))
    return token


def token_matrix(matrix: np.ndarray) -> list[list[str]]:
    return [[token_for_entry(entry) for entry in row] for row in matrix]


def build_result() -> dict[str, Any]:
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1410 = load_json("data/bt1410_witting_delayed_query_frame_compiler.json")

    analyzers = []
    max_unitarity_error = 0.0
    max_slot_error = 0.0
    family_histogram: Counter[str] = Counter()
    support_histogram: Counter[tuple[int, ...]] = Counter()
    nonzero_histogram: Counter[int] = Counter()
    token_histogram: Counter[str] = Counter()

    identity = np.eye(4, dtype=complex)
    for basis_id, tetrad in enumerate(tetrads):
        matrix = analyzer_for_tetrad(rays, tetrad)
        basis_columns = np.column_stack([rays[ray] for ray in tetrad])
        slot_map = matrix @ basis_columns
        unitarity_error = float(np.max(np.abs(matrix @ matrix.conj().T - identity)))
        slot_error = float(np.max(np.abs(slot_map - identity)))
        max_unitarity_error = max(max_unitarity_error, unitarity_error)
        max_slot_error = max(max_slot_error, slot_error)

        supports = [support_weight(rays[ray]) for ray in tetrad]
        family = optical_family(supports)
        family_histogram[family] += 1
        support_histogram[tuple(sorted(supports))] += 1
        nonzero_entries = int(np.count_nonzero(np.abs(matrix) > 1e-8))
        nonzero_histogram[nonzero_entries] += 1
        tokens = token_matrix(matrix)
        for row in tokens:
            token_histogram.update(row)

        analyzers.append(
            {
                "basis_id": basis_id,
                "tetrad": list(tetrad),
                "detector_slot_to_ray": {
                    str(slot): ray for slot, ray in enumerate(tetrad)
                },
                "support_profile": supports,
                "optical_family": family,
                "nonzero_entries": nonzero_entries,
                "zero_entries": 16 - nonzero_entries,
                "token_matrix": tokens,
                "max_unitarity_error": unitarity_error,
                "max_slot_error": slot_error,
            }
        )

    checks = {
        "bt1410_frame_compiler_loaded": bt1410["verified"] is True
        and bt1410["basis_local_frame_table"]["records"] == 640,
        "bt1374_slot_residue_loaded": bt1374["checks"][
            "transversal_is_mirror_slot_mod_4"
        ]
        is True,
        "forty_analyzers_built": len(analyzers) == 40,
        "all_analyzers_unitary": max_unitarity_error < 1e-10,
        "all_analyzers_map_basis_rays_to_detector_slots": max_slot_error < 1e-10,
        "support_families_are_1_12_27": dict(family_histogram)
        == {
            "COMPUTATIONAL_DIRECT_RAILS": 1,
            "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
            "FOUR_THREE_RAIL_WITTING_ROWS": 27,
        },
        "nonzero_histogram_is_sparse": dict(nonzero_histogram)
        == {4: 1, 10: 12, 12: 27},
        "entry_alphabet_is_witting_phase_alphabet": set(token_histogram)
        == {
            "0",
            "1",
            "1/sqrt3",
            "-1/sqrt3",
            "omega/sqrt3",
            "omega2/sqrt3",
            "-omega/sqrt3",
            "-omega2/sqrt3",
        },
        "no_analyzer_is_generic_dense_4x4": max(nonzero_histogram) == 12,
    }

    return {
        "bt": 1411,
        "title": "Witting basis analyzer unitaries",
        "verified": all(checks.values()),
        "analyzer_rule": (
            "For tetrad B=(r0,r1,r2,r3), U_B has row j equal to conjugate(r_j). "
            "Thus U_B maps Witting ray r_j to detector slot j."
        ),
        "physical_reading": (
            "BT1411 turns the BT1410 delayed-query frame choice into a single-photon "
            "four-mode analyzer.  The Witting analyzer bank is not generic dense "
            "linear optics: it has a 1+12+27 sparsity split and uses only the "
            "0, 1, and cube-root phase over sqrt(3) alphabet."
        ),
        "histograms": {
            "optical_family": dict(family_histogram),
            "support_profile": {
                ",".join(str(part) for part in key): value
                for key, value in sorted(support_histogram.items())
            },
            "nonzero_entries": {
                str(key): value for key, value in sorted(nonzero_histogram.items())
            },
            "entry_tokens": dict(sorted(token_histogram.items())),
        },
        "error_bounds": {
            "max_unitarity_error": max_unitarity_error,
            "max_slot_error": max_slot_error,
        },
        "hardware_interface": {
            "detector_slots": [0, 1, 2, 3],
            "bt1374_slot_rule": bt1374["address_rule"]["formula"],
            "bt1410_basis_local_records": bt1410["basis_local_frame_table"]["records"],
            "families": {
                "COMPUTATIONAL_DIRECT_RAILS": (
                    "direct measurement in the path-polarization computational basis"
                ),
                "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": (
                    "one rail bypasses while the orthogonal three-rail complement "
                    "is analyzed by a tritter/phase subnetwork"
                ),
                "FOUR_THREE_RAIL_WITTING_ROWS": (
                    "four contextual rows, each dark on one rail and balanced over "
                    "the other three rails"
                ),
            },
        },
        "sample_analyzers": {
            "basis_0_computational": analyzers[0],
            "basis_1_one_direct_rail": analyzers[1],
            "basis_13_contextual": analyzers[13],
        },
        "all_analyzers": analyzers,
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
                "bt": result["bt"],
                "families": result["histograms"]["optical_family"],
                "max_nonzero_entries": max(
                    int(key) for key in result["histograms"]["nonzero_entries"]
                ),
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
