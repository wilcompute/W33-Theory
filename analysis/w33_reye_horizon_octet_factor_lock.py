"""Part MCXCV: Reye horizon octet-factor lock.

Continuation of MCXCII-MCXCIV with MCLXXXVI tomotope cells.

Core packets:
  C = 8   (tomotope cells, MCLXXXVI)
  N = 72  (horizon code total, MCXCII)
  A_R = 576 (Reye automorphism order, MCXCIII)
  g = 6, P = 12 (genus/parity and Reye points, MCXCII/MCXCIV)

New lock:
  A_R = C*N = C*P*g = 8*72 = 8*12*6 = 576.

Hence N/C = 9 symbols per tomotope cell and A_R/N = 8 symmetry units per
horizon symbol.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def reye_horizon_octet_factor_lock_packet() -> dict[str, object]:
    mclxxxvi = _load(ROOT / "PART_MCLXXXVI_TOMOTOPE_EDGE_CELL_FLAG_TENSOR_LOCK_results.json")
    mcxcii = _load(ROOT / "PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json")
    mcxciii = _load(ROOT / "PART_MCXCIII_REYE_TOMOTOPE_24CELL_COMMON_SPINE_results.json")
    mcxciv = _load(ROOT / "PART_MCXCIV_REYE_HORIZON_SYMMETRY_GENUS_RECIPROCITY_results.json")

    cells = int(mclxxxvi["tomotope_packet"]["cells"])                             # 8
    total = int(mcxcii["horizon_code"]["total"])                                  # 72
    reye_points = int(mcxcii["input_anchor"]["reye_points"])                       # 12
    aut_reye = int(mcxciii["symmetry_lock"]["reye_automorphism_order"])            # 576
    aut_tomotope = int(mcxciii["tomotope_match"]["tomotope_automorphism_order"])   # 96
    genus = int(mcxciv["horizon_packet"]["genus"])                                 # 6
    parity = int(mcxciv["horizon_packet"]["parity"])                               # 6

    symbols_per_cell = total // cells
    sym_units_per_symbol = aut_reye // total

    checks = {
        "cells_is_8": cells == 8,
        "horizon_total_is_72": total == 72,
        "reye_automorphism_is_576": aut_reye == 576,
        "reye_points_is_12": reye_points == 12,
        "genus_and_parity_are_6": genus == parity == 6,
        "total_equals_points_times_genus": total == reye_points * genus,
        "reye_symmetry_equals_cells_times_total": aut_reye == cells * total,
        "reye_symmetry_equals_cells_times_points_times_genus": aut_reye == cells * reye_points * genus,
        "tomotope_symmetry_equals_points_times_cells": aut_tomotope == reye_points * cells == 96,
        "symbols_per_cell_is_9": symbols_per_cell == 9,
        "symmetry_units_per_symbol_is_8": sym_units_per_symbol == 8,
        "octet_nonet_duality": cells * symbols_per_cell == total and sym_units_per_symbol * total == aut_reye,
    }

    return {
        "part": "MCXCV",
        "theorem": "Reye horizon octet-factor lock",
        "packets": {
            "cells": cells,
            "horizon_total": total,
            "reye_points": reye_points,
            "genus": genus,
            "reye_automorphism": aut_reye,
            "tomotope_automorphism": aut_tomotope,
        },
        "derived_invariants": {
            "symbols_per_cell": symbols_per_cell,
            "symmetry_units_per_symbol": sym_units_per_symbol,
            "identity": "576 = 8*72 = 8*12*6, with 72/8=9 and 576/72=8",
        },
        "finite_universality_surrogate": {
            "statement": "horizon code volume and Reye symmetry are factor-locked by the tomotope cell octet",
            "boundary": "finite combinatorial factor law; not a continuum field equation",
        },
        "claim_boundary": "finite octet-factor reciprocity on tomotope/Reye horizon packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = reye_horizon_octet_factor_lock_packet()
    out_path = ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCV: Reye Horizon Octet-Factor Lock ===")
    print(packet["derived_invariants"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
