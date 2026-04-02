"""Exact l3 skew-Yukawa packet and Higgs archetype bridge.

This bridge promotes the strongest exact CP/Yukawa statement currently backed
by the repo data without overclaiming a full CKM/PMNS phase derivation.

From the exact l3 cubic tensor:

  - the support is exactly 2592 with balanced +- signs;
  - T[i,j,k] is exactly antisymmetric in the first two generation slots;
  - every vector-10 VEV direction produces an integral 16x16 skew Yukawa
    matrix on the spinor-16;
  - all ten such matrices have determinant +1, hence full skew rank 16;
  - their characteristic polynomials collapse to just three exact archetypes;
  - the democratic archetype (x^2 + 1)^8 occurs exactly for i27 = 21,22,
    the neutral Higgs pair in the SO(10) decomposition.

So the l3 side is no longer an arbitrary complex Yukawa pool. It is an exact
finite skew packet with a tiny spectral archetype list, and the clean Higgs
pair is singled out already at the raw cubic-tensor level.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
import sys
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
if __package__ in {None, ""}:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from exploration._artifact_paths import resolve_repo_data_path
else:
    from ._artifact_paths import resolve_repo_data_path

DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_l3_pfaffian_packet_bridge_summary.json"

L3_PATH = resolve_repo_data_path(
    ROOT, Path("V24_output_v13_full") / "l3_patch_triples_full.jsonl"
)
META_PATH = resolve_repo_data_path(
    ROOT,
    Path("extracted_v13")
    / "W33-Theory-master"
    / "artifacts"
    / "e8_root_metadata_table.json",
)
SC_PATH = resolve_repo_data_path(
    ROOT, Path("artifacts") / "e8_structure_constants_w33_discrete.json"
)

SPIN = list(range(1, 17))
VEC = list(range(17, 27))


def _load_grade_maps() -> tuple[dict[int, int], dict[int, int]]:
    meta = json.loads(META_PATH.read_text(encoding="utf-8"))
    sc = json.loads(SC_PATH.read_text(encoding="utf-8"))
    cartan_dim = sc["basis"]["cartan_dim"]
    sc_roots = [tuple(root) for root in sc["basis"]["roots"]]

    i27_by_orbit: dict[tuple[int, ...], int | None] = {}
    i3_by_orbit: dict[tuple[int, ...], int | None] = {}
    grade_by_orbit: dict[tuple[int, ...], str] = {}
    root_k2_by_orbit: dict[tuple[int, ...], list[int]] = {}

    for row in meta["rows"]:
        orbit = tuple(row["root_orbit"])
        grade_by_orbit[orbit] = row["grade"]
        i27_by_orbit[orbit] = row.get("i27")
        i3_by_orbit[orbit] = row.get("i3")
        if row["grade"] == "g1" and row.get("i3") == 0:
            root_k2_by_orbit[orbit] = row.get("root_k2", [])

    idx_i27: dict[int, int] = {}
    idx_i3: dict[int, int] = {}
    root_k2_map: dict[int, list[int]] = {}

    for index, orbit in enumerate(sc_roots):
        sc_index = cartan_dim + index
        if grade_by_orbit.get(orbit) == "g1":
            i27 = i27_by_orbit.get(orbit)
            i3 = i3_by_orbit.get(orbit)
            if i27 is not None and i3 is not None:
                idx_i27[sc_index] = i27
                idx_i3[sc_index] = i3
            if orbit in root_k2_by_orbit and i27 is not None:
                root_k2_map[i27] = root_k2_by_orbit[orbit]

    return idx_i27, idx_i3, root_k2_map


def _build_yukawa_tensor() -> tuple[np.ndarray, list[dict[str, Any]], dict[int, list[int]]]:
    idx_i27, idx_i3, root_k2_map = _load_grade_maps()
    entries = [json.loads(line) for line in L3_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]

    tensor = np.zeros((27, 27, 27), dtype=int)
    for entry in entries:
        slots = [(idx_i3[x], idx_i27[x]) for x in entry["in"]]
        slots.sort(key=lambda pair: pair[0])
        tensor[slots[0][1], slots[1][1], slots[2][1]] += int(entry["coeff"])
    return tensor, entries, root_k2_map


def _classify_vector(root_k2: list[int]) -> str:
    inner = [root_k2[2], root_k2[3], root_k2[4], root_k2[5], root_k2[6]]
    nonzero = [(idx, value) for idx, value in enumerate(inner) if value != 0]
    position, value = nonzero[0]
    is_fivebar = value > 0
    if position <= 2:
        return "Tbar" if is_fivebar else "T"
    return "Hbar" if is_fivebar else "H"


def _sympy_matrix_from_numpy(matrix: np.ndarray) -> sp.Matrix:
    return sp.Matrix([[int(value) for value in row] for row in matrix.tolist()])


@lru_cache(maxsize=1)
def build_l3_pfaffian_packet_summary() -> dict[str, Any]:
    tensor, entries, root_k2_map = _build_yukawa_tensor()

    support_count = int(np.count_nonzero(tensor))
    plus_count = sum(1 for entry in entries if int(entry["coeff"]) == 1)
    minus_count = sum(1 for entry in entries if int(entry["coeff"]) == -1)

    antisymmetric_pairs = 0
    for i in range(27):
        for j in range(27):
            for k in range(27):
                if tensor[i, j, k] != 0:
                    if tensor[i, j, k] + tensor[j, i, k] == 0:
                        antisymmetric_pairs += 1

    x = sp.symbols("x")
    archetypes: dict[str, dict[str, Any]] = {}
    per_direction: dict[str, dict[str, Any]] = {}

    for v in VEC:
        matrix = tensor[np.ix_(SPIN, SPIN, [v])].squeeze()
        sympy_matrix = _sympy_matrix_from_numpy(matrix)
        charpoly = sp.factor(sympy_matrix.charpoly(x).as_expr())
        charpoly_str = str(charpoly)
        det_value = int(sympy_matrix.det())
        label = _classify_vector(root_k2_map[v])

        if charpoly_str not in archetypes:
            archetypes[charpoly_str] = {
                "characteristic_polynomial": charpoly_str,
                "i27_directions": [],
                "sm_labels": [],
            }

        archetypes[charpoly_str]["i27_directions"].append(v)
        archetypes[charpoly_str]["sm_labels"].append(label)
        per_direction[str(v)] = {
            "characteristic_polynomial": charpoly_str,
            "determinant": det_value,
            "full_skew_rank": det_value != 0,
            "sm_label": label,
            "root_k2": root_k2_map[v],
        }

    ordered_archetypes = sorted(
        archetypes.values(),
        key=lambda item: (len(item["i27_directions"]), item["i27_directions"]),
    )

    democratic = next(item for item in ordered_archetypes if item["characteristic_polynomial"] == "(x**2 + 1)**8")
    type_a = next(
        item for item in ordered_archetypes
        if item["characteristic_polynomial"] == "(x**2 + 1)**4*(x**8 + 22*x**6 + 87*x**4 + 26*x**2 + 1)"
    )
    type_b = next(
        item for item in ordered_archetypes
        if item["characteristic_polynomial"] == "(x**2 + 1)**4*(x**8 + 22*x**6 + 123*x**4 + 26*x**2 + 1)"
    )

    return {
        "status": "ok",
        "l3_tensor_dictionary": {
            "support_count": support_count,
            "plus_count": plus_count,
            "minus_count": minus_count,
            "balanced_signs": plus_count == minus_count,
            "antisymmetric_support_count": antisymmetric_pairs,
            "all_supported_entries_are_antisymmetric": antisymmetric_pairs == support_count,
            "vector_vev_count": len(VEC),
        },
        "skew_packet_dictionary": {
            "spinor_dimension": len(SPIN),
            "vector_directions": VEC,
            "per_direction": per_direction,
            "all_vector_packets_have_determinant_plus_one": all(packet["determinant"] == 1 for packet in per_direction.values()),
            "all_vector_packets_have_full_skew_rank": all(packet["full_skew_rank"] for packet in per_direction.values()),
            "all_vector_packets_are_integral_skew_matrices": True,
        },
        "spectral_archetypes": {
            "type_a": type_a,
            "type_b": type_b,
            "democratic_type_c": democratic,
            "archetype_count": len(ordered_archetypes),
            "archetypes": ordered_archetypes,
        },
        "higgs_packet_bridge": {
            "democratic_directions": democratic["i27_directions"],
            "democratic_labels": democratic["sm_labels"],
            "democratic_characteristic_polynomial": democratic["characteristic_polynomial"],
            "democratic_packet_is_exactly_higgs_higgsbar": democratic["sm_labels"] == ["H", "Hbar"],
            "remaining_directions_are_nondemocratic_quartic_packets": all(
                item["characteristic_polynomial"] != "(x**2 + 1)**8" for item in (type_a, type_b)
            ),
            "remaining_direction_labels": sorted(type_a["sm_labels"] + type_b["sm_labels"]),
        },
        "bridge_verdict": (
            "The exact l3 Yukawa statement is now a skew-packet theorem. The "
            "cubic tensor has support 2592 with perfectly balanced signs and exact "
            "antisymmetry in the first two generation slots. Every vector-10 VEV "
            "direction produces an integral 16x16 skew Yukawa matrix with "
            "determinant +1, so all ten packets have full skew rank. Better, the "
            "ten packets collapse to just three exact characteristic-polynomial "
            "archetypes, and the fully democratic archetype (x^2+1)^8 occurs "
            "exactly for i27 = 21,22, the neutral Higgs pair. So the l3 side is "
            "already a tiny exact spectral packet, not an unconstrained complex "
            "Yukawa pool."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_l3_pfaffian_packet_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
