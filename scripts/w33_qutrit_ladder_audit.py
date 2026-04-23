#!/usr/bin/env python3
"""Exact finite qutrit ladder audit for the W33 program.

This module packages the strongest *already-exact* finite layers that now sit
in the repo into one ladder:

1. Local 1-qutrit shell:
   the H27 neighborhood is the exact Heisenberg/MUB shell with local W(E6)
   data.
2. Global 2-qutrit kernel:
   W33 is exactly the projective two-qutrit Pauli commutation geometry, with
   the canonical operator layer and projective Clifford action.
3. Exact 3-qutrit closure:
   the ternary Golay / Heisenberg lift lands exactly on the 729-dimensional
   operator basis and traceless sl(27) layer.
4. Exact 6-qutrit backbone:
   the offline 2.Suz data embeds into Sp(12,3), giving a concrete symplectic
   Clifford backbone for the 3^{1+12} Heisenberg phase space.
5. Exact E8-side decomposition:
   independently of the qutrit kernel, the E8 root side has the exact
   72 + 6 + 162 = 240 decomposition with line orbits 36 + 27 + 27 + 27 + 1 +
   1 + 1.

The point is not to claim a new functorial E8 theorem. The point is to make the
exact ladder and its boundary explicit in one executable audit.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "pillars") not in sys.path:
    sys.path.insert(0, str(ROOT / "pillars"))

from scripts.w33_2suz_sp12_embedding import analyze as analyze_2suz_sp12_embedding
from scripts.w33_exact_lie_bridge_audit import (
    classify_lie_bridges,
    local_e6_bridge_summary,
    local_h27_affine_symmetry_summary,
    projective_symplectic_action_summary,
)
from scripts.w33_monster_3b_s12_sl27_bridge import analyze as analyze_monster_bridge
from scripts.w33_qutrit_operator_algebra import analyze as analyze_qutrit_operator_algebra

E8_E6A2_DECOMP_DATA = ROOT / "data" / "w33_e8_e6a2_decomp.json"


@lru_cache(maxsize=1)
def one_qutrit_local_layer_summary() -> Dict[str, object]:
    local_bridge = local_e6_bridge_summary()
    local_affine = local_h27_affine_symmetry_summary()

    return {
        "visible_shell_size": int(local_bridge["nonneighbor_count"]),
        "mub_class_count": int(local_bridge["mub_class_count"]),
        "mub_class_sizes": tuple(int(v) for v in local_bridge["mub_class_sizes"]),
        "fiber_count": int(local_bridge["fiber_count"]),
        "fiber_size": int(local_bridge["fiber_size"]),
        "generation_fiber_sizes": tuple(int(v) for v in local_bridge["generation_fiber_sizes"]),
        "schlafli_parameters": tuple(int(v) for v in local_bridge["schlafli_parameters"]),
        "tritangent_split": {
            "classical_total": int(local_bridge["tritangent_split"]["classical_total"]),
            "internal_shell": int(local_bridge["tritangent_split"]["internal_shell"]),
            "missing_center_cosets": int(local_bridge["tritangent_split"]["missing_center_cosets"]),
        },
        "heisenberg_sl23_order": int(local_affine["local_projective_subgroup_order"]),
        "heisenberg_gl23_order": int(local_affine["local_affine_group_order"]),
        "affine_point_stabilizer_order": int(local_affine["local_affine_point_stabilizer_order"]),
        "full_45_triads_invariant": bool(local_affine["local_affine_triads_invariant"]),
    }


@lru_cache(maxsize=1)
def two_qutrit_global_layer_summary() -> Dict[str, object]:
    operator_layer = analyze_qutrit_operator_algebra()
    projective_action = projective_symplectic_action_summary()
    local_affine = local_h27_affine_symmetry_summary()

    pauli = operator_layer["exact_pauli_algebra"]
    symplectic = operator_layer["symplectic_action"]
    hamiltonian = operator_layer["canonical_hamiltonian"]

    return {
        "weyl_basis_size": int(pauli["weyl_basis_size"]),
        "projective_point_count": int(pauli["projective_point_count"]),
        "edge_count": int(projective_action["edge_orbit_size"]),
        "generator_names": tuple(symplectic["generator_names"]),
        "all_generators_verified": bool(symplectic["all_generators_verified"]),
        "line_count": int(hamiltonian["line_count"]),
        "line_size": int(hamiltonian["line_size"]),
        "lines_per_point": int(hamiltonian["lines_per_point"]),
        "laplacian_eigenpairs": tuple(
            (int(value), int(mult)) for value, mult in hamiltonian["laplacian_eigenpairs"]
        ),
        "kernel_dimension": int(hamiltonian["kernel_dimension"]),
        "projective_group_order": int(projective_action["enumerated_group_order"]),
        "projective_point_stabilizer_order": int(projective_action["point_stabilizer_order"]),
        "full_graph_group_order": int(local_affine["full_graph_group_order"]),
    }


@lru_cache(maxsize=1)
def three_qutrit_sl27_layer_summary() -> Dict[str, object]:
    bridge = analyze_monster_bridge()
    if bridge.get("available") is not True:
        raise RuntimeError(f"monster bridge unavailable: {bridge}")

    return {
        "monster_class": str(bridge["monster"]["class"]),
        "extraspecial_order": int(bridge["monster"]["extraspecial_order"]),
        "heisenberg_irrep_dim": int(bridge["heisenberg"]["irrep_dim"]),
        "golay_codeword_count": int(bridge["golay"]["n_codewords"]),
        "golay_nonzero_count": int(bridge["golay"]["n_nonzero"]),
        "golay_lagrangian": bool(bridge["golay_lagrangian"]["symplectic_isotropic_all_pairs"]),
        "sl27_hilbert_dim": int(bridge["sl27"]["hilbert_dim"]),
        "sl27_operator_basis_dim": int(bridge["sl27"]["operator_basis_dim"]),
        "sl27_traceless_dim": int(bridge["sl27"]["traceless_dim"]),
    }


@lru_cache(maxsize=1)
def six_qutrit_backbone_summary() -> Dict[str, object]:
    sp12 = analyze_2suz_sp12_embedding()
    if sp12.get("available") is not True:
        raise RuntimeError(f"2.Suz/Sp(12,3) backbone unavailable: {sp12}")

    signature = sp12["standard_generator_signature"]
    invariant_form = sp12["invariant_form"]
    standardized = sp12["standardized_generators"]
    interpretation = sp12["interpretation"]

    return {
        "field_p": int(sp12["field_p"]),
        "phase_space_dim": int(interpretation["phase_space_dim"]),
        "qutrits_n": int(interpretation["qutrits_n"]),
        "heisenberg_irrep_dim": int(interpretation["heisenberg_irrep_dim"]),
        "ord_A": int(signature["ord_A"]),
        "ord_B": int(signature["ord_B"]),
        "ord_AB": int(signature["ord_AB"]),
        "invariant_form_nullspace_dim": int(invariant_form["nullspace_dim"]),
        "invariant_form_rank": int(invariant_form["rank"]),
        "standardized_generators_preserve_J0": bool(
            standardized["A_std_preserves_J0"] and standardized["B_std_preserves_J0"]
        ),
    }


@lru_cache(maxsize=1)
def e8_side_exact_decomposition_summary() -> Dict[str, object]:
    summary = json.loads(E8_E6A2_DECOMP_DATA.read_text(encoding="utf-8"))
    if not summary.get("T1_correct"):
        raise RuntimeError("stored E8/E6xA2 decomposition summary is not marked correct")

    return {
        "dot_pair_class_count": int(summary["T1_n_classes"]),
        "total_root_count": int(summary["T1_total_roots"]),
        "e6_root_count": int(summary["T2_e6_size"]),
        "a2_root_count": int(summary["T3_a2_total"]),
        "mixed_root_count": int(summary["T4_mixed_total"]),
        "edgepair_orbit_sizes": tuple(int(v) for v in summary["T5_ep_orbit_sizes"]),
        "line_orbit_sizes": tuple(int(v) for v in summary["T5_line_orbit_sizes"]),
        "matter_lines_per_generation": int(summary["T6_matter_lines_per_gen"]),
        "generation_count": int(summary["T6_n_generations"]),
        "structure_correct": bool(summary["T6_correct"]),
    }


@lru_cache(maxsize=1)
def classify_qutrit_ladder() -> Tuple[Dict[str, object], ...]:
    one_qutrit = one_qutrit_local_layer_summary()
    two_qutrit = two_qutrit_global_layer_summary()
    three_qutrit = three_qutrit_sl27_layer_summary()
    six_qutrit = six_qutrit_backbone_summary()
    e8_side = e8_side_exact_decomposition_summary()

    return (
        {
            "name": "local_one_qutrit_heisenberg_e6_shell",
            "layer": "1-qutrit local shell",
            "support_level": "repo-exact + classical exact",
            "depends_only_on_qutrit_kernel": True,
            "statement": (
                "The local H27 shell is an exact Heisenberg/MUB package with Schlafli "
                "parameters (27,16,10,8) and the faithful Heisenberg-GL(2,3) local symmetry."
            ),
            "evidence": one_qutrit,
        },
        {
            "name": "global_two_qutrit_pauli_clifford_kernel",
            "layer": "2-qutrit global kernel",
            "support_level": "repo-exact",
            "depends_only_on_qutrit_kernel": True,
            "statement": (
                "W33 is exactly the projective 2-qutrit Pauli commutation geometry, with "
                "canonical Hamiltonian spectrum (0^1,10^24,16^15) and the projective "
                "Clifford action of order 25920."
            ),
            "evidence": two_qutrit,
        },
        {
            "name": "three_qutrit_sl27_closure",
            "layer": "3-qutrit exact extension",
            "support_level": "repo-exact finite extension",
            "depends_only_on_qutrit_kernel": False,
            "statement": (
                "The ternary Golay / Heisenberg lift closes exactly at the 729-dimensional "
                "operator basis and the traceless 728-dimensional sl(27) layer."
            ),
            "evidence": three_qutrit,
        },
        {
            "name": "six_qutrit_sp12_clifford_backbone",
            "layer": "6-qutrit exact backbone",
            "support_level": "repo-exact finite extension",
            "depends_only_on_qutrit_kernel": False,
            "statement": (
                "The vendored 2.Suz generators embed exactly into Sp(12,3), giving a "
                "concrete 6-qutrit symplectic/Clifford backbone for the 3^{1+12} "
                "Heisenberg phase space."
            ),
            "evidence": six_qutrit,
        },
        {
            "name": "e8_side_e6_a2_decomposition",
            "layer": "E8-side exact decomposition",
            "support_level": "exact E8-side decomposition",
            "depends_only_on_qutrit_kernel": False,
            "statement": (
                "On the separate E8 side, the exact decomposition 72 + 6 + 162 = 240 and "
                "line orbits 36 + 27 + 27 + 27 + 1 + 1 + 1 are fully verified, but this "
                "still sits beyond a functorial derivation from the qutrit kernel alone."
            ),
            "evidence": e8_side,
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_qutrit_ladder()
    kernel_records = tuple(record["name"] for record in records if record["depends_only_on_qutrit_kernel"])
    extension_records = tuple(
        record["name"] for record in records if not record["depends_only_on_qutrit_kernel"]
    )
    one_qutrit = one_qutrit_local_layer_summary()
    two_qutrit = two_qutrit_global_layer_summary()
    three_qutrit = three_qutrit_sl27_layer_summary()
    six_qutrit = six_qutrit_backbone_summary()
    e8_side = e8_side_exact_decomposition_summary()
    exact_lie_bridge_names = tuple(
        record["name"]
        for record in classify_lie_bridges()
        if record["depends_only_on_qutrit_kernel"]
    )

    theorem = {
        "the_one_qutrit_local_shell_is_exact_h27_heisenberg_mub_with_local_e6_data": (
            one_qutrit["visible_shell_size"] == 27
            and one_qutrit["mub_class_sizes"] == (3, 3, 3, 3)
            and one_qutrit["fiber_count"] == 9
            and one_qutrit["fiber_size"] == 3
            and one_qutrit["schlafli_parameters"] == (27, 16, 10, 8)
            and one_qutrit["heisenberg_sl23_order"] == 648
            and one_qutrit["heisenberg_gl23_order"] == 1296
            and one_qutrit["full_45_triads_invariant"] is True
        ),
        "the_two_qutrit_global_kernel_is_exactly_w33_with_the_canonical_operator_layer": (
            two_qutrit["weyl_basis_size"] == 81
            and two_qutrit["projective_point_count"] == 40
            and two_qutrit["edge_count"] == 240
            and two_qutrit["line_count"] == 40
            and two_qutrit["line_size"] == 4
            and two_qutrit["lines_per_point"] == 4
            and two_qutrit["laplacian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
            and two_qutrit["projective_group_order"] == 25920
            and two_qutrit["full_graph_group_order"] == 51840
            and two_qutrit["all_generators_verified"] is True
        ),
        "the_three_qutrit_extension_closes_exactly_at_sl27_via_golay_heisenberg": (
            three_qutrit["monster_class"] == "3B"
            and three_qutrit["extraspecial_order"] == 3**13
            and three_qutrit["golay_codeword_count"] == 729
            and three_qutrit["golay_nonzero_count"] == 728
            and three_qutrit["heisenberg_irrep_dim"] == 729
            and three_qutrit["sl27_hilbert_dim"] == 27
            and three_qutrit["sl27_operator_basis_dim"] == 729
            and three_qutrit["sl27_traceless_dim"] == 728
            and three_qutrit["golay_lagrangian"] is True
        ),
        "the_six_qutrit_phase_space_backbone_is_exactly_visible_as_2suz_inside_sp12": (
            six_qutrit["field_p"] == 3
            and six_qutrit["phase_space_dim"] == 12
            and six_qutrit["qutrits_n"] == 6
            and six_qutrit["heisenberg_irrep_dim"] == 729
            and six_qutrit["ord_A"] == 4
            and six_qutrit["ord_B"] == 3
            and six_qutrit["ord_AB"] == 13
            and six_qutrit["invariant_form_nullspace_dim"] == 1
            and six_qutrit["invariant_form_rank"] == 12
            and six_qutrit["standardized_generators_preserve_J0"] is True
        ),
        "the_e8_side_exact_decomposition_has_72_plus_6_plus_162_and_three_27_line_orbits": (
            e8_side["dot_pair_class_count"] == 13
            and e8_side["total_root_count"] == 240
            and e8_side["e6_root_count"] == 72
            and e8_side["a2_root_count"] == 6
            and e8_side["mixed_root_count"] == 162
            and e8_side["line_orbit_sizes"] == (36, 27, 27, 27, 1, 1, 1)
            and e8_side["generation_count"] == 3
            and e8_side["matter_lines_per_generation"] == 27
            and e8_side["structure_correct"] is True
        ),
        "the_local_h27_shell_size_matches_the_exact_e8_side_generation_orbit_size": (
            one_qutrit["visible_shell_size"] == e8_side["matter_lines_per_generation"] == 27
        ),
        "the_two_qutrit_edge_count_matches_the_exact_e8_root_count": (
            two_qutrit["edge_count"] == e8_side["total_root_count"] == 240
        ),
        "the_three_qutrit_operator_basis_matches_the_six_qutrit_heisenberg_irrep": (
            three_qutrit["sl27_operator_basis_dim"] == six_qutrit["heisenberg_irrep_dim"] == 729
        ),
        "the_exact_kernel_stops_after_the_first_two_rungs": (
            kernel_records
            == (
                "local_one_qutrit_heisenberg_e6_shell",
                "global_two_qutrit_pauli_clifford_kernel",
            )
            and exact_lie_bridge_names
            == (
                "local_schlafli_e6_bridge",
                "local_h27_affine_symmetry",
                "projective_symplectic_we6_symmetry",
            )
        ),
        "the_later_rungs_are_exact_but_require_additional_finite_input_beyond_the_kernel": (
            extension_records
            == (
                "three_qutrit_sl27_closure",
                "six_qutrit_sp12_clifford_backbone",
                "e8_side_e6_a2_decomposition",
            )
        ),
    }
    theorem["the_exact_qutrit_ladder_is_closed_up_to_the_e8_side_boundary"] = all(theorem.values())

    return {
        "status": "ok",
        "one_qutrit_local_layer": one_qutrit,
        "two_qutrit_global_layer": two_qutrit,
        "three_qutrit_sl27_layer": three_qutrit,
        "six_qutrit_backbone": six_qutrit,
        "e8_side_exact_decomposition": e8_side,
        "ladder_records": records,
        "kernel_record_names": kernel_records,
        "finite_extension_record_names": extension_records,
        "qutrit_ladder_theorem": theorem,
        "boundary_note": (
            "The first two rungs are exact consequences of the qutrit kernel itself. "
            "The later finite rungs are exact but require extra finite input beyond "
            "the kernel. The remaining open wall is still the continuum/dynamical "
            "lift and the last nonlinear Yukawa spectral packet."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXI_qutrit_ladder_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Exact qutrit ladder audit")
    print(
        "  Rungs: "
        f"1q={payload['one_qutrit_local_layer']['visible_shell_size']}, "
        f"2q={payload['two_qutrit_global_layer']['projective_point_count']}, "
        f"3q={payload['three_qutrit_sl27_layer']['sl27_operator_basis_dim']}, "
        f"6q={payload['six_qutrit_backbone']['phase_space_dim']}"
    )
    print(
        "  Exact kernel names: "
        + ", ".join(payload["kernel_record_names"])
    )
    print(
        "  Later exact names: "
        + ", ".join(payload["finite_extension_record_names"])
    )
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
