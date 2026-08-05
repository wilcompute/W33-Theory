#!/usr/bin/env python3
"""Compact live release certificate for Passes 3458--3471."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from analysis.bt3471_parallel_radius_reconciliation import build_certificate as reconcile

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/PART_BT3458_BT3471_FACE_TOWER_BRAUER_TOMOTOPE_results.json"


def build_certificate() -> dict:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    dependency = reconcile()
    assert raw["status"] == "PASS"
    assert len(raw["checks"]) == 12 and all(raw["checks"].values())
    assert dependency["live_covering_radius_interval"] == [389, 435]

    tower = raw["sections"]["association_scheme_and_face_tower"]
    modular = raw["sections"]["characteristic_three_descent"]
    m4 = raw["sections"]["full_M4_amplitude_compiler"]
    tomotope = raw["sections"]["tomotope_product_code"]

    return {
        "schema": "w33.bt3458_3471.face_tower_release.v1",
        "status": "PASS",
        "raw_exact_checks": raw["checks"],
        "live_boundaries": {
            "covering_radius": [389, 435],
            "chromatic_number": [10, 11],
        },
        "theorems": {
            "face_tower": [240, 120, 40],
            "pair_scheme_rank": tower["pair_scheme"]["rank"],
            "pair_scheme_valencies": tower["pair_scheme"]["valencies"],
            "W33_quotient_srg": tower["quotient"]["srg"],
            "matching_holonomy": tower["quotient"]["matching_triangle_holonomy"],
            "local_point_stabilizer": tower["local_tetrahedral_chart"]["point_stabilizer"],
            "pair_module_loewy_layers": modular["pair_module"]["endomorphism_loewy_layers"],
            "antisymmetric_decomposition": modular["antisymmetric_module"]["decomposition_dimensions"],
            "crossed_amplitude_algebra_dimension": m4["algebra_dimensions"]["plus_null_conic_dual_sign"],
            "product_code_max_projective_triples_per_dual_coset": tomotope["product_code_falsifier"]["maximum_projective_triples_in_one_dual_coset"],
            "oriented_tetrahedron_configuration": tomotope["oriented_tetrahedron_incidence"]["configuration"],
        },
        "dependency": dependency,
        "boundaries": {
            "radius": "The local level-zero Delsarte computation proves only the 389 lower bound; the 435 upper bound is verified from Pass 3486.",
            "chromatic": "The objectwise full-M4 transport compiler is not yet a ten-colour or SDP certificate.",
            "modular": "The 81-dimensional brick is not called simple without MeatAxe composition factors.",
            "tomotope": "The oriented 12_4 16_3 surface does not supply the missing 192-flag cell cocycle.",
            "hardware": "No remote synthesis, timing, or PDF result is claimed before workflow evidence completes.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(text, encoding="utf-8")
    print("PASS release certificate: face tower with live radius 389<=R<=435")
    print(text, end="")


if __name__ == "__main__":
    main()
