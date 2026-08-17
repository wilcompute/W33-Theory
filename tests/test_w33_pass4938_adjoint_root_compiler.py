"""Focused native-GAP regression for the Pass-4938 adjoint root compiler."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass4938_adjoint_root_compiler.g"
FROZEN = ROOT / "data" / "PART_W33_PASS4938_ADJOINT_ROOT_COMPILER.json"
PASS_LINE = "Pass 4938 adjoint root compiler: 44/44 checks; status=PASS"

EXPECTED_CHECKS = {
    "adjoint_dimension_10",
    "adjoint_to_symmetric_bijection",
    "classifier_tuple_separates_17",
    "congruence_rank_group_orbit_count_7",
    "congruence_rank_group_orbit_sizes_exact",
    "congruence_rank_group_order_24261120",
    "congruence_rank_group_pgsp_index_468",
    "congruence_rank_type_atlas_exact",
    "even_discriminant_constant_on_orbits",
    "forward_directed_cayley_connected",
    "forward_directed_cayley_diameter_5",
    "forward_distance_distribution_exact",
    "forward_inverse_classes_disjoint",
    "forward_rank_discriminant_formula_all_offsets",
    "forward_root_class_size_40",
    "forward_root_class_spans_10",
    "full_cayley_spectrum_exact",
    "orbit_eigenvalue_atlas_exact",
    "pgsp_action_order_51840",
    "pgsp_orbit_count_17",
    "pgsp_orbit_sizes_exact",
    "psp_action_order_25920",
    "psp_orbit_count_21",
    "psp_orbit_sizes_exact",
    "psp_refines_exactly_four_odd_rank_orbits",
    "psp_split_classes_are_negative_pairs",
    "root_formula_40_times_2",
    "root_lifts_are_symplectic_order_3",
    "root_lifts_form_40_C3_subgroups",
    "root_opcode_span_rank_10",
    "root_orbit_is_exact_rank_one_set",
    "root_orbit_size_80",
    "root_orbit_square_zero",
    "signed_root_cayley_connected",
    "signed_root_cayley_diameter_4",
    "signed_root_distance_distribution_exact",
    "signed_root_distance_equals_rank",
    "square_zero_rank2_pair_split_by_discriminant",
    "trace_pairing_nondegenerate",
    "trace_pairing_pgsp_invariant",
    "transition_detailed_balance",
    "transition_matrix_exact",
    "transition_polynomial_exact",
    "transition_rows_sum_80",
}


def _assert_exact_payload(payload: dict[str, object]) -> None:
    assert payload["schema"] == "w33.pass4938.adjoint_root_compiler.v1"
    assert payload["status"] == "PASS"

    assert payload["adjoint_symmetric_bridge"] == {
        "map": "X |-> JX from sp4(F3) to Sym4(F3)",
        "dimension": 10,
        "trace_pairing": "Tr(XY)",
        "trace_pairing_rank": 10,
        "trace_pairing_determinant_mod_3": 1,
    }
    assert payload["primitive_opcodes"] == {
        "set": "all rank-one X in sp4(F3)",
        "count": 80,
        "law": "X^2=0; T=I+X is a symplectic transvection of order 3",
        "root_subgroups_C3": 40,
        "PGSp_orbit_sizes": [80],
        "PSp_chiral_split": [40, 40],
        "span_dimension": 10,
    }

    classifier = payload["pgsp_classifier"]
    assert classifier["orbit_count"] == 17
    assert classifier["orbit_sizes"] == [
        1,
        80,
        240,
        480,
        540,
        540,
        1080,
        1080,
        4320,
        4320,
        5184,
        5184,
        5760,
        6480,
        6480,
        8640,
        8640,
    ]
    rows = classifier["rows"]
    assert len(rows) == 17
    assert [row["size"] for row in rows] == classifier["orbit_sizes"]
    assert len(
        {
            (
                row["rank"],
                tuple(row["characteristic_polynomial"]),
                tuple(row["minimal_polynomial"]),
                row["even_discriminant"],
            )
            for row in rows
        }
    ) == 17
    assert rows[2]["rank"] == rows[3]["rank"] == 2
    assert rows[2]["characteristic_polynomial"] == rows[3][
        "characteristic_polynomial"
    ]
    assert rows[2]["minimal_polynomial"] == rows[3]["minimal_polynomial"]
    assert [rows[2]["even_discriminant"], rows[3]["even_discriminant"]] == [1, 2]

    signed = payload["signed_root_cayley_compiler"]
    assert signed["vertices"] == 3**10 == 59049
    assert signed["degree"] == 80
    assert signed["diameter"] == 4
    assert signed["distance_distribution"] == [1, 80, 2340, 18720, 37908]
    assert signed["spectrum"] == [
        [-28, 780],
        [-10, 16848],
        [-1, 18800],
        [8, 21060],
        [26, 1560],
        [80, 1],
    ]
    assert sum(multiplicity for _, multiplicity in signed["spectrum"]) == 59049
    assert len(signed["orbit_transition_matrix"]) == 17
    assert all(sum(row) == 80 for row in signed["orbit_transition_matrix"])
    assert signed["quotient_characteristic_polynomial"] == (
        "(t-80)(t-26)^2(t-8)^5(t+1)^4(t+10)^3(t+28)^2"
    )

    chirality = payload["chirality_refinement"]
    assert chirality["PGSp_class_count"] == 17
    assert chirality["PSp_class_count"] == 21
    assert chirality["split_PGSp_indices"] == [2, 9, 13, 16]
    assert chirality["PGSp_to_PSp_size_refinement"][1] == [40, 40]
    assert chirality["PGSp_to_PSp_size_refinement"][8] == [2160, 2160]
    assert chirality["PGSp_to_PSp_size_refinement"][12] == [2880, 2880]
    assert chirality["PGSp_to_PSp_size_refinement"][15] == [4320, 4320]

    assert payload["forward_root_compiler"] == {
        "opcode_count": 40,
        "root_discriminant": 2,
        "inverse_rule": "two repeats give 2X=-X",
        "diameter": 5,
        "distance_distribution": [1, 40, 820, 10920, 30420, 16848],
        "compile_length": (
            "rank(JX) when disc(JX)=root_discriminant^rank, "
            "otherwise rank(JX)+1"
        ),
    }
    assert payload["symmetry_firewall"] == {
        "constructed_linear_rank_group": "S |-> a P^T S P, P in GL4(3), a in F3^x",
        "order": 24261120,
        "index_over_PGSp": 468,
        "orbit_count": 7,
        "orbit_sizes": [1, 80, 780, 1560, 16848, 18720, 21060],
        "information_loss": (
            "21 PSp classes -> 17 PGSp classes -> 7 rank/type classes -> "
            "6 Cayley eigenvalues"
        ),
        "warning": "rank adjacency alone does not identify the PGSp controller",
    }

    assert any("BT881 owns" in item for item in payload["prior_art"])
    assert any("arXiv:1410.7184" in item for item in payload["prior_art"])
    assert "468 times larger than PGSp" in payload["boundary"]
    assert "No HoloBox opcode" in payload["boundary"]
    assert payload["checks"] == {name: True for name in EXPECTED_CHECKS}


def test_native_gap_rebuild_matches_frozen_certificate(tmp_path: Path) -> None:
    gap = shutil.which("gap")
    assert gap is not None, "native GAP is required for Pass 4938"

    completed = subprocess.run(
        [gap, "-q", "-b", str(SOURCE)],
        cwd=tmp_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    assert completed.returncode == 0, completed.stdout[-6000:]
    assert PASS_LINE in completed.stdout.splitlines(), completed.stdout[-6000:]
    assert "Syntax warning" not in completed.stdout

    rebuilt = tmp_path / "data" / "PART_W33_PASS4938_ADJOINT_ROOT_COMPILER.json"
    rebuilt_bytes = rebuilt.read_bytes()
    assert rebuilt_bytes == FROZEN.read_bytes()
    _assert_exact_payload(json.loads(rebuilt_bytes))
