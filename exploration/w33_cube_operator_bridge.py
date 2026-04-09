#!/usr/bin/env python3
"""Local cube operator bridge for the canonical W(3,3) E6 packet.

This script packages two operator-level facts that emerged from the local
Heisenberg/Steinberg analysis:

1. The canonical hypercharge operator on the 27-state E6 packet has an exact
   local cube formula on the `(u1,u2,z) in F3^2 x F3` chart.
2. The clean Higgs pair `H_2, Hbar_2` is the charged origin fiber and carries
   the unique minimal left-right Yukawa support.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_finite_spectral_triple import canonical_generation_basis
from exploration.w33_fermionic_connes_sector import build_clean_higgs_geometry_summary


def _source_coords() -> dict[int, tuple[tuple[int, int], int]]:
    data = json.loads((ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json").read_text(encoding="utf-8"))
    return {
        int(key): (tuple(int(x) for x in value["u"]), int(value["z"]))
        for key, value in data["e6id_to_heisenberg"].items()
    }


def _cube_data() -> dict[str, Any]:
    coords = _source_coords()
    basis = canonical_generation_basis()

    charge6 = np.zeros((3, 3, 3), dtype=int)
    slot_cube: dict[tuple[int, int, int], str] = {}
    for state in basis:
        (u1, u2), z = coords[state.source_i27]
        charge6[u1, u2, z] = int(6 * state.hypercharge)
        slot_cube[(u1, u2, z)] = state.slot

    return {"charge6": charge6, "slot_cube": slot_cube}


def _hypercharge_base(u1: int, z: int) -> int:
    table = {
        (0, 0): 0,
        (0, 1): 3,
        (0, 2): -3,
        (1, 0): -2,
        (1, 1): 1,
        (1, 2): 1,
        (2, 0): 2,
        (2, 1): -4,
        (2, 2): 2,
    }
    return table[(u1, z)]


def _u2_character(u2: int) -> int:
    return {0: 0, 1: 1, 2: -1}[u2]


def _z_character(z: int) -> int:
    return {0: 1, 1: -1, 2: 0}[z]


def hypercharge_formula_summary() -> dict[str, Any]:
    cube = _cube_data()["charge6"]

    base = np.zeros_like(cube)
    defect = np.zeros_like(cube)
    predicted = np.zeros_like(cube)
    for u1 in range(3):
        for u2 in range(3):
            for z in range(3):
                base[u1, u2, z] = _hypercharge_base(u1, z)
                defect[u1, u2, z] = 3 * int(u1 == 0) * _u2_character(u2) * _z_character(z)
                predicted[u1, u2, z] = base[u1, u2, z] + defect[u1, u2, z]

    return {
        "charge6_cube_layers": [cube[:, :, z].tolist() for z in range(3)],
        "base_cube_layers": [base[:, :, z].tolist() for z in range(3)],
        "defect_cube_layers": [defect[:, :, z].tolist() for z in range(3)],
        "formula_theorem": {
            "hypercharge_6y_equals_base_plus_electroweak_defect": bool(np.array_equal(cube, predicted)),
            "rows_u1_1_and_u1_2_depend_only_on_row_and_layer": bool(
                np.array_equal(cube[1], base[1]) and np.array_equal(cube[2], base[2])
            ),
            "all_u2_dependence_is_concentrated_on_electroweak_row_u1_0": bool(
                np.array_equal(defect[1], np.zeros((3, 3), dtype=int))
                and np.array_equal(defect[2], np.zeros((3, 3), dtype=int))
            ),
            "row0_defect_factorizes_as_u2_character_times_z_character": bool(
                np.array_equal(defect[0], 3 * np.outer([0, 1, -1], [1, -1, 0]))
            ),
        },
        "formula_text": (
            "6Y(u1,u2,z) = B(u1,z) + 3·1_{u1=0}·chi_u2(u2)·chi_z(z), "
            "where B depends only on row/layer, chi_u2=(0,1,-1), and chi_z=(1,-1,0)."
        ),
    }


def build_cube_operator_bridge_summary() -> dict[str, Any]:
    return {
        "status": "ok",
        "hypercharge": hypercharge_formula_summary(),
        "clean_higgs": build_clean_higgs_geometry_summary(),
    }


def main() -> None:
    summary = build_cube_operator_bridge_summary()

    print("W33 CUBE OPERATOR BRIDGE")
    print("=" * 72)
    print(summary["hypercharge"]["formula_text"])
    print("hypercharge theorem:")
    for key, value in summary["hypercharge"]["formula_theorem"].items():
        print(f"  {key}: {value}")
    for z, layer in enumerate(summary["hypercharge"]["charge6_cube_layers"]):
        print(f"6Y layer z={z}: {layer}")
    print("clean Higgs theorem:")
    for key, value in summary["clean_higgs"]["geometry_theorem"].items():
        print(f"  {key}: {value}")
    for slot in summary["clean_higgs"]["clean_higgs_slots"]:
        loc = summary["clean_higgs"]["slot_locations"][slot]
        print(f"{slot}: source_i27={loc['source_i27']} u={tuple(loc['u'])} z={loc['z']}")
        print(f"  support: {summary['clean_higgs']['yukawa_support'][slot]}")


if __name__ == "__main__":
    main()
