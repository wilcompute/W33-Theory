"""Live CKM seed reset against the current vertex generator.

The later CKM/CP bridge stack was built on ``data/w33_yukawa_blocks.json`` as
if that file were the current generator output. After the repo changes, that
assumption stopped being safe.

This module rechecks the live vertex-pair generator directly and identifies the
winning pair inside the canonical local E6 chart. The new picture is sharper:

- the current best real CKM seed is no longer a same-row ``U2`` self-anchor;
- it is a cross-row quark/lepton bridge on the shared charged slice ``z = 2``;
- the exact winning pair is ``Q_2_1`` against ``L_2``; and
- the old ``U2`` anchor summaries are now stale-cache statements rather than
  live generator facts.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_live_ckm_seed_bridge_summary.json"
TOL = 1e-12

from exploration.w33_finite_spectral_triple import canonical_generation_basis
from scripts.w33_yukawa_blocks import (
    _build_hodge_and_generations,
    build_generation_profiles,
    ckm_error,
    cubic_form_on_h27,
    compute_ckm_and_jarlskog,
    h27_affine_coord,
)
from e8_embedding_group_theoretic import build_w33


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _coord_to_slot() -> dict[tuple[int, int, int], str]:
    artifact = json.loads((ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json").read_text(encoding="utf-8"))
    coords = {
        int(key): (tuple(int(x) for x in value["u"]), int(value["z"]))
        for key, value in artifact["e6id_to_heisenberg"].items()
    }
    source_to_slot = {state.source_i27: state.slot for state in canonical_generation_basis()}
    return {
        (u[0], u[1], z): source_to_slot[index]
        for index, (u, z) in coords.items()
    }


def _slot_family_label(slot: str) -> str | None:
    if slot.startswith("Q_"):
        return slot.split("_")[1]
    if slot.startswith("L_"):
        return slot.split("_")[1]
    return None


def _slot_component_label(slot: str) -> str | None:
    if slot.startswith("Q_"):
        return slot.split("_")[2]
    return None


def _row_label(a: int) -> str:
    return {
        0: "lepton_higgs_singlet_row",
        1: "quark_triplet_row",
        2: "right_color_row",
    }[a]


def _yukawa_full_builder() -> tuple[list[tuple[int, int, int, int]], list[np.ndarray], list[Any]]:
    hodge, _triangles, edges, gens = _build_hodge_and_generations()
    n_w33, vertices_w33, adjacency_w33, _ = build_w33()
    h27_indices_global = [
        index
        for index in range(n_w33)
        if index != 0 and index not in set(adjacency_w33[0])
    ]
    h27_vertices = [vertices_w33[index] for index in h27_indices_global]
    _h27, local_tris, generation_profiles = build_generation_profiles(hodge, edges, gens, v0=0)
    return h27_vertices, generation_profiles, local_tris


def _yukawa_full(
    generation_profiles: list[np.ndarray],
    local_tris: list[Any],
    vertex_index: int,
) -> np.ndarray:
    vev = np.zeros(27, dtype=float)
    vev[vertex_index] = 1.0
    yukawa = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(a, 3):
            value = cubic_form_on_h27(None, local_tris, generation_profiles[a], generation_profiles[b], vev)
            yukawa[a, b] = value
            yukawa[b, a] = value
    return yukawa


@lru_cache(maxsize=1)
def _full_vertex_scan() -> list[dict[str, Any]]:
    h27_vertices, generation_profiles, local_tris = _yukawa_full_builder()
    coord_to_slot = _coord_to_slot()
    results: list[dict[str, Any]] = []

    yukawas = []
    for index in range(27):
        matrix = _yukawa_full(generation_profiles, local_tris, index)
        if np.allclose(matrix, 0, atol=TOL):
            yukawas.append(None)
        else:
            yukawas.append(matrix)

    for up_index, up_matrix in enumerate(yukawas):
        if up_matrix is None:
            continue
        up_coord = tuple(int(value) for value in h27_affine_coord(h27_vertices[up_index]))
        up_slot = coord_to_slot[up_coord]
        for down_index, down_matrix in enumerate(yukawas):
            if down_index == up_index or down_matrix is None:
                continue
            down_coord = tuple(int(value) for value in h27_affine_coord(h27_vertices[down_index]))
            down_slot = coord_to_slot[down_coord]
            ckm_matrix, jarlskog = compute_ckm_and_jarlskog(up_matrix, down_matrix)
            results.append(
                {
                    "ckm_error": float(ckm_error(ckm_matrix)),
                    "jarlskog": float(jarlskog),
                    "up_index": up_index,
                    "down_index": down_index,
                    "up_coord": up_coord,
                    "down_coord": down_coord,
                    "up_slot": up_slot,
                    "down_slot": down_slot,
                    "up_block": up_coord[0],
                    "down_block": down_coord[0],
                    "up_row_label": _row_label(up_coord[0]),
                    "down_row_label": _row_label(down_coord[0]),
                    "same_z_sheet": up_coord[2] == down_coord[2],
                    "shared_z": up_coord[2] if up_coord[2] == down_coord[2] else None,
                    "up_family": _slot_family_label(up_slot),
                    "down_family": _slot_family_label(down_slot),
                    "up_component": _slot_component_label(up_slot),
                    "down_component": _slot_component_label(down_slot),
                    "V_CKM": np.abs(ckm_matrix).tolist(),
                }
            )

    results.sort(key=lambda item: item["ckm_error"])
    return results


def _min_by_predicate(results: list[dict[str, Any]], predicate) -> dict[str, Any]:
    candidates = [item for item in results if predicate(item)]
    if not candidates:
        raise ValueError("Expected nonempty candidate family")
    return min(candidates, key=lambda item: item["ckm_error"])


@lru_cache(maxsize=1)
def build_live_ckm_seed_summary() -> dict[str, Any]:
    current_blocks = _load_json("w33_yukawa_blocks.json")
    stale_anchor = _load_json("w33_middle_family_anchor_bridge_summary.json")
    stale_parity = _load_json("w33_parity_odd_anchor_bridge_summary.json")
    results = _full_vertex_scan()

    best = results[0]
    best_same_quark_row = _min_by_predicate(
        results,
        lambda item: item["up_block"] == 1 and item["down_block"] == 1,
    )
    best_same_family_two = _min_by_predicate(
        results,
        lambda item: item["up_family"] == "2" and item["down_family"] == "2",
    )
    best_shared_z2 = _min_by_predicate(
        results,
        lambda item: item["same_z_sheet"] and item["shared_z"] == 2,
    )

    block_pair_minima: dict[str, float] = {}
    for up_block in range(3):
        for down_block in range(3):
            candidate = _min_by_predicate(
                results,
                lambda item, ub=up_block, db=down_block: item["up_block"] == ub and item["down_block"] == db,
            )
            block_pair_minima[f"{up_block}->{down_block}"] = float(candidate["ckm_error"])

    live_best_matches_cached = (
        int(current_blocks["vertex_scan_best"]["vi_up"]) == best["up_index"]
        and int(current_blocks["vertex_scan_best"]["vj_down"]) == best["down_index"]
        and tuple(int(value) for value in current_blocks["vertex_scan_best"]["v_up_affine"]) == best["up_coord"]
        and tuple(int(value) for value in current_blocks["vertex_scan_best"]["v_dn_affine"]) == best["down_coord"]
        and abs(float(current_blocks["vertex_scan_best"]["ckm_error"]) - best["ckm_error"]) < TOL
    )

    stale_anchor_claim = stale_anchor["middle_family_anchor_theorem"][
        "best_vertex_level_quark_scan_anchors_both_sectors_on_block_u2"
    ]
    stale_parity_claim = stale_parity["parity_odd_anchor_bridge_theorem"][
        "current_quark_frontier_is_anchor_bridge_not_cp_phase_solution"
    ]
    live_u2_anchor_condition = best["up_block"] == 1 and best["down_block"] == 1

    return {
        "status": "ok",
        "live_cached_match": live_best_matches_cached,
        "live_best_seed": {
            "ckm_error": best["ckm_error"],
            "jarlskog": best["jarlskog"],
            "up_index": best["up_index"],
            "down_index": best["down_index"],
            "up_coord": list(best["up_coord"]),
            "down_coord": list(best["down_coord"]),
            "up_slot": best["up_slot"],
            "down_slot": best["down_slot"],
            "up_row_label": best["up_row_label"],
            "down_row_label": best["down_row_label"],
            "same_z_sheet": best["same_z_sheet"],
            "shared_z": best["shared_z"],
            "V_CKM": best["V_CKM"],
        },
        "comparison_modes": {
            "best_same_quark_row_seed": {
                key: value
                for key, value in best_same_quark_row.items()
                if key in {"ckm_error", "up_coord", "down_coord", "up_slot", "down_slot", "shared_z"}
            },
            "best_family_two_seed": {
                key: value
                for key, value in best_same_family_two.items()
                if key in {"ckm_error", "up_coord", "down_coord", "up_slot", "down_slot", "shared_z"}
            },
            "best_shared_z2_seed": {
                key: value
                for key, value in best_shared_z2.items()
                if key in {"ckm_error", "up_coord", "down_coord", "up_slot", "down_slot", "shared_z"}
            },
            "block_pair_minima": block_pair_minima,
        },
        "stale_anchor_summaries": {
            "cached_middle_anchor_claim": bool(stale_anchor_claim),
            "cached_parity_anchor_claim": bool(stale_parity_claim),
            "live_u2_anchor_condition": live_u2_anchor_condition,
        },
        "live_ckm_seed_theorem": {
            "cached_yukawa_blocks_now_match_the_live_generator": live_best_matches_cached,
            "live_best_pair_is_q2_1_against_l2": (
                best["up_slot"] == "Q_2_1" and best["down_slot"] == "L_2"
            ),
            "live_best_pair_links_quark_row_to_lepton_higgs_row": (
                best["up_block"] == 1 and best["down_block"] == 0
            ),
            "live_best_pair_sits_on_the_shared_charged_z2_sheet": (
                best["same_z_sheet"] is True and best["shared_z"] == 2
            ),
            "second_family_survives_as_the_live_seed_but_not_as_a_same_row_self_anchor": (
                best["up_family"] == "2"
                and best["down_family"] == "2"
                and best["up_block"] == 1
                and best["down_block"] == 0
            ),
            "cross_row_q_l_seed_beats_the_best_same_quark_row_anchor": (
                best["ckm_error"] + TOL < best_same_quark_row["ckm_error"]
            ),
            "the_old_u2_u2_anchor_claim_is_now_stale_cache_not_live_generator_fact": (
                stale_anchor_claim
                and stale_parity_claim
                and not live_u2_anchor_condition
            ),
        },
        "interpretive_read": (
            "The refreshed generator no longer supports the cached same-row U2 "
            "anchor as the live quark frontier. The best real CKM seed is a "
            "cross-row bridge from the quark row to the lepton/Higgs row on the "
            "shared charged slice z=2, with exact winner Q_2_1 against L_2."
        ),
        "bridge_verdict": (
            "The current CKM frontier has reset. After rerunning the live "
            "vertex-pair generator, the best real seed is not a U2 self-anchor "
            "inside the quark row. It is the charged cross-row pair Q_2_1 vs "
            "L_2 on the common z=2 sheet, with CKM error 0.1764. The old middle-"
            "anchor and parity-odd-anchor summaries remain useful as cached "
            "historical reductions, but they are no longer the live generator "
            "facts after the repo changes."
        ),
        "source_files": [
            "scripts/w33_yukawa_blocks.py",
            "data/w33_yukawa_blocks.json",
            "data/w33_middle_family_anchor_bridge_summary.json",
            "data/w33_parity_odd_anchor_bridge_summary.json",
            "artifacts/e6_cubic_affine_heisenberg_model.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_live_ckm_seed_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
