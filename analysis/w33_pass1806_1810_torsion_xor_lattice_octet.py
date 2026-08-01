#!/usr/bin/env python3
"""Passes 1806--1810: reconciliation addenda for the frame/octet five-frontier packet.

The heavy exact reconstruction remains in the historical collision worker
``w33_pass1611_1615_torsion_xor_lattice_octet.py``.  This wrapper preserves that
verified implementation while assigning the surviving nonduplicative results to
an unambiguous namespace after the late parallel Passes 1612--1616 and 1701--1705
landed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "analysis" / "w33_pass1611_1615_torsion_xor_lattice_octet.py"
OUT = ROOT / "data" / "w33_pass1806_1810_torsion_xor_lattice_octet.json"
XOR_OUT = ROOT / "data" / "w33_pass1807_bockstein_independent.xor"


def load_legacy():
    spec = importlib.util.spec_from_file_location("pass1611_collision_worker", LEGACY)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def certificate(write_xor: bool = True) -> dict[str, Any]:
    legacy = load_legacy()
    previous_xor = legacy.XOR_OUT
    legacy.XOR_OUT = XOR_OUT
    try:
        base = legacy.certificate(write_xor=write_xor)
    finally:
        legacy.XOR_OUT = previous_xor

    p1 = base["pass1611"]
    p2 = base["pass1612"]
    p3 = base["pass1613"]
    p4 = base["pass1614"]
    p5 = base["pass1615"]

    return {
        "schema": "w33.pass1806_1810.v1",
        "status": base["status"],
        "checks": base["checks"],
        "parallel_reconciliation": {
            "primary_packet": "Passes 1701-1705",
            "statement": (
                "This addendum does not relabel the primary Loewy, minimal-240-XOR, "
                "chiral-packing, determinant-two, or rank-45 results. It freezes "
                "complementary exact data and resolves the late namespace collision."
            ),
        },
        "pass1806": {
            "module": p1["module"],
            "dimension": p1["dimension"],
            "alternative_composition_series": p1["composition_factors"],
            "composition_factor_multiset": sorted(p1["composition_factors"]),
            "socle_chain_dimensions": p1["socle_series_dimensions"],
            "factors": p1["factors"],
            "reconciliation": (
                "The order 1,8,1,6,14 is an exact composition series. Its multiset "
                "agrees with the primary Loewy packet 1|(6+8)|1|14; composition-series "
                "order inside the 6+8 middle layer is not a conflict."
            ),
            "boundary": "No Brauer-character label beyond dimensions is asserted.",
        },
        "pass1807": {
            "selected_octet_columns": p2["selected_octet_columns"],
            "per_color_new_rank": p2["per_color_new_rank"],
            "symmetric_xor_equations": p2["native_xor_equations"],
            "independent_global_rank_gain": p2["global_rank_after"] - p2["global_rank_before"],
            "cross_color_redundancy_dimension": p2["native_xor_equations"] - (
                p2["global_rank_after"] - p2["global_rank_before"]
            ),
            "all_exact8_equations": p2["all_exact8_equations"],
            "global_rank_before": p2["global_rank_before"],
            "global_rank_after": p2["global_rank_after"],
            "fixed_rank_before": p2["fixed_rank_before"],
            "fixed_rank_after": p2["fixed_rank_after"],
            "xor_sha256": p2["xor_sha256"],
            "reconciliation": (
                "The 270-clause file is color-symmetric, not globally minimal. Exactly "
                "30 directions are redundant modulo the frame-partition equations; the "
                "primary minimal exporter keeps 240."
            ),
            "boundary": p2["boundary"],
        },
        "pass1808": {
            "single_cover_signature": p3["single_cover_signature"],
            "four_packing_signature": p3["four_packing_signature"],
            "remaining_300_frame_signature": p3["remaining_300_frame_signature"],
            "theorem": (
                "For every exact cover x, J^T x = 8*1. Therefore all cover orbits and "
                "all four-packings have identical linear Bockstein signatures; torsion "
                "cannot distinguish extendibility."
            ),
        },
        "pass1809": {
            "unsigned_coordinate_snf": p4["unsigned_coordinate_snf"],
            "signed_coordinate_snf": p4["signed_coordinate_snf"],
            "saturated_bridge_determinant": p4["saturated_bridge_determinant"],
            "parity_functional": p4["parity_functional"],
            "missing_vector_weight": p4["missing_vector_weight"],
            "missing_vector_norm2": p4["missing_vector_norm2"],
            "missing_vector_sha256": p4["missing_vector_sha256"],
            "theorem": (
                "Beyond det=2, this freezes a primitive representative of the unique "
                "missing orientation-parity coset."
            ),
        },
        "pass1810": {
            **p5,
            "theorem": (
                "The five Gram values are not an association scheme; the full rank-32 "
                "frame orbital algebra is essential. The modular collapse is "
                "characteristic-sensitive."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--no-xor", action="store_true")
    args = parser.parse_args()
    cert = certificate(write_xor=not args.no_xor)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": cert["status"], "checks": sum(cert["checks"].values()), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
