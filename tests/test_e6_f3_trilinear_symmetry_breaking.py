from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_e6_f3_trilinear_symmetry_breaking_integration():
    root = Path.cwd()
    in_json = root / "artifacts" / "e6_f3_trilinear_map.json"
    if not in_json.exists():
        pytest.skip("Missing artifacts/e6_f3_trilinear_map.json")

    out_json = root / "artifacts" / "e6_f3_trilinear_symmetry_breaking.json"
    out_md = root / "artifacts" / "e6_f3_trilinear_symmetry_breaking.md"

    cmd = [
        sys.executable,
        "tools/analyze_e6_f3_trilinear_symmetry_breaking.py",
        "--in-json",
        str(in_json),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=root,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert out_json.exists()
    assert out_md.exists()

    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["counts"]["lines"] == 12
    assert data["stabilizers"]["support"]["agl23_size"] == 432
    assert data["stabilizers"]["support"]["hessian216_size"] == 216
    assert data["stabilizers"]["full_sign"]["hessian216_with_z_affine_global_sign"] >= 1
    assert data["cross_checks"]["line_product_closed_form"]["holds"] is True
    assert data["cross_checks"]["full_sign_closed_form"]["holds"] is True
    assert (
        data["cross_checks"]["line_product_stabilizer_parametrization"]["holds"] is True
    )
    assert (
        data["cross_checks"]["line_product_stabilizer_parametrization_det1"]["holds"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_group_structure"]["dihedral_witness_found"]
        is True
    )
    assert data["cross_checks"]["line_product_group_structure"]["size"] == 12
    assert (
        data["cross_checks"]["line_product_group_structure"]["order3_element_count"]
        == 2
    )
    assert (
        data["cross_checks"]["line_product_group_structure"]["unique_c3_subgroup"]
        is True
    )
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "point_orbit_sizes"
    ] == [1, 2, 6]
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "line_orbit_sizes"
    ] == [1, 2, 3, 6]
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"]["missing_point_fixed"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"][
            "anchor_line_through_missing_orbit_size"
        ]
        == 1
    )
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "distinguished_direction_orbit_sizes_inside_family"
    ] == [1, 2]
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"][
            "qutrit_phase_space_orbit_signature_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "maps_lines_to_single_striation"
        ]
        is True
    )
    assert data["cross_checks"]["line_product_striation_action"][
        "striation_orbit_sizes"
    ] == [1, 3]
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "distinguished_striation_fixed_setwise"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_transitive"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_is_s3"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_image_size"
        ]
        == 6
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_kernel_size"
        ]
        == 2
    )
    assert data["cross_checks"]["line_product_flag_line_orbits"]["orbit_sizes"] == [
        1,
        2,
        3,
        6,
    ]
    assert data["cross_checks"]["line_product_flag_line_orbits"]["class_sizes"] == {
        "through_missing_and_in_distinguished_direction": 1,
        "not_through_missing_and_in_distinguished_direction": 2,
        "through_missing_and_not_in_distinguished_direction": 3,
        "not_through_missing_and_not_in_distinguished_direction": 6,
    }
    assert data["cross_checks"]["line_product_flag_line_orbits"][
        "class_to_orbit_count"
    ] == {
        "through_missing_and_in_distinguished_direction": 1,
        "not_through_missing_and_in_distinguished_direction": 1,
        "through_missing_and_not_in_distinguished_direction": 1,
        "not_through_missing_and_not_in_distinguished_direction": 1,
    }
    assert (
        data["cross_checks"]["line_product_flag_line_orbits"][
            "orbit_homogeneous_by_flag_class"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_line_orbits"][
            "qutrit_flag_line_orbit_signature_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"]["decomposition_holds"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "flag_stabilizer_equals_residual"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"]["shifted_rule_holds"] is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "coordinate_free_shifted_rule_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "coordinate_free_adapted_gauge_count"
        ]
        > 0
    )
    assert data["cross_checks"]["line_product_flag_geometry"][
        "unique_missing_point_from_negative_lines"
    ] == [2, 2]
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "distinguished_direction_all_positive"
        ]
        == "x"
    )
    assert data["cross_checks"]["line_product_group_structure"][
        "candidate_isomorphism"
    ].startswith("D12")
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"]["stabilizer_count"]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"][
            "non_stabilizer_count"
        ]
        == 2591
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"][
            "exact_min_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_hessian216"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_agl23"][
            "stabilizer_count"
        ]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_agl23"][
            "non_stabilizer_count"
        ]
        == 5183
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_agl23"][
            "exact_min_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_agl23"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_comparison"][
            "exact_min_sizes_match"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_hessian216"][
            "min_distinct_line_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_hessian216"][
            "min_distinct_line_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_agl23"][
            "min_distinct_line_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_agl23"][
            "min_distinct_line_certificate_size"
        ]
        == 8
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_agl23"][
            "line_distinctness_gap_vs_unconstrained"
        ]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_comparison"][
            "distinct_line_sizes_match"
        ]
        is False
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_hessian216"][
            "min_striation_complete_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_hessian216"][
            "min_striation_complete_certificate_size"
        ]
        == 7
    )
    assert data["cross_checks"]["full_sign_striation_certificate_hessian216"][
        "required_striations"
    ] == ["x", "y", "y=1x", "y=2x"]
    assert (
        data["cross_checks"]["full_sign_striation_certificate_agl23"][
            "min_striation_complete_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_agl23"][
            "min_striation_complete_certificate_size"
        ]
        == 8
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_agl23"][
            "striation_completeness_gap_vs_unconstrained"
        ]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_comparison"][
            "striation_complete_sizes_match"
        ]
        is False
    )


def test_e6_f3_trilinear_symmetry_breaking_closed_form_fixture(tmp_path: Path):
    # Minimal fixture reproducing the observed sign field on the 12 affine lines.
    lines = [
        ([[0, 0], [0, 1], [0, 2]], (-1, -1, 1)),
        ([[1, 0], [1, 1], [1, 2]], (-1, -1, 1)),
        ([[2, 0], [2, 1], [2, 2]], (1, -1, -1)),
        ([[0, 0], [1, 0], [2, 0]], (1, 1, -1)),
        ([[0, 1], [1, 1], [2, 1]], (1, -1, 1)),
        ([[0, 2], [1, 2], [2, 2]], (1, 1, 1)),
        ([[0, 0], [1, 1], [2, 2]], (1, -1, -1)),
        ([[0, 1], [1, 2], [2, 0]], (-1, -1, -1)),
        ([[0, 2], [1, 0], [2, 1]], (-1, 1, 1)),
        ([[0, 0], [1, 2], [2, 1]], (-1, 1, 1)),
        ([[0, 1], [1, 0], [2, 2]], (1, 1, 1)),
        ([[0, 2], [1, 1], [2, 0]], (1, 1, -1)),
    ]
    payload = {
        "affine_u_line_slices": [
            {
                "u_line": u_line,
                "entries": [
                    {"z_profile_over_u_line": [z, z, z], "sign_pm1": int(signs[z])}
                    for z in (0, 1, 2)
                ],
            }
            for u_line, signs in lines
        ]
    }

    in_json = tmp_path / "e6_f3_trilinear_map.json"
    out_json = tmp_path / "out.json"
    out_md = tmp_path / "out.md"
    in_json.write_text(json.dumps(payload, encoding="utf-8"), encoding="utf-8")

    cmd = [
        sys.executable,
        "tools/analyze_e6_f3_trilinear_symmetry_breaking.py",
        "--in-json",
        str(in_json),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]
    r = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=Path.cwd(),
        check=False,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["cross_checks"]["line_product_closed_form"]["holds"] is True
    assert data["cross_checks"]["full_sign_closed_form"]["holds"] is True
    assert (
        data["cross_checks"]["line_product_stabilizer_parametrization"]["holds"] is True
    )
    assert (
        data["cross_checks"]["line_product_stabilizer_parametrization_det1"]["holds"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_group_structure"]["dihedral_witness_found"]
        is True
    )
    assert data["cross_checks"]["line_product_group_structure"]["size"] == 12
    assert (
        data["cross_checks"]["line_product_group_structure"]["order3_element_count"]
        == 2
    )
    assert (
        data["cross_checks"]["line_product_group_structure"]["unique_c3_subgroup"]
        is True
    )
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "point_orbit_sizes"
    ] == [1, 2, 6]
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "line_orbit_sizes"
    ] == [1, 2, 3, 6]
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"]["missing_point_fixed"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"][
            "anchor_line_through_missing_orbit_size"
        ]
        == 1
    )
    assert data["cross_checks"]["line_product_orbit_fingerprint"][
        "distinguished_direction_orbit_sizes_inside_family"
    ] == [1, 2]
    assert (
        data["cross_checks"]["line_product_orbit_fingerprint"][
            "qutrit_phase_space_orbit_signature_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "maps_lines_to_single_striation"
        ]
        is True
    )
    assert data["cross_checks"]["line_product_striation_action"][
        "striation_orbit_sizes"
    ] == [1, 3]
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "distinguished_striation_fixed_setwise"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_transitive"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_is_s3"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_image_size"
        ]
        == 6
    )
    assert (
        data["cross_checks"]["line_product_striation_action"][
            "non_distinguished_permutation_kernel_size"
        ]
        == 2
    )
    assert data["cross_checks"]["line_product_flag_line_orbits"]["orbit_sizes"] == [
        1,
        2,
        3,
        6,
    ]
    assert data["cross_checks"]["line_product_flag_line_orbits"]["class_sizes"] == {
        "through_missing_and_in_distinguished_direction": 1,
        "not_through_missing_and_in_distinguished_direction": 2,
        "through_missing_and_not_in_distinguished_direction": 3,
        "not_through_missing_and_not_in_distinguished_direction": 6,
    }
    assert data["cross_checks"]["line_product_flag_line_orbits"][
        "class_to_orbit_count"
    ] == {
        "through_missing_and_in_distinguished_direction": 1,
        "not_through_missing_and_in_distinguished_direction": 1,
        "through_missing_and_not_in_distinguished_direction": 1,
        "not_through_missing_and_not_in_distinguished_direction": 1,
    }
    assert (
        data["cross_checks"]["line_product_flag_line_orbits"][
            "orbit_homogeneous_by_flag_class"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_line_orbits"][
            "qutrit_flag_line_orbit_signature_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"]["decomposition_holds"]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "flag_stabilizer_equals_residual"
        ]
        is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"]["shifted_rule_holds"] is True
    )
    assert (
        data["cross_checks"]["line_product_flag_geometry"][
            "coordinate_free_shifted_rule_holds"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"]["stabilizer_count"]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"][
            "exact_min_certificate_found"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_hessian216"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_agl23"][
            "exact_min_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_obstruction_certificate_comparison"][
            "exact_min_sizes_match"
        ]
        is True
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_hessian216"][
            "min_distinct_line_certificate_size"
        ]
        == 7
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_agl23"][
            "min_distinct_line_certificate_size"
        ]
        == 8
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_agl23"][
            "line_distinctness_gap_vs_unconstrained"
        ]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_distinct_line_certificate_comparison"][
            "distinct_line_sizes_match"
        ]
        is False
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_hessian216"][
            "min_striation_complete_certificate_size"
        ]
        == 7
    )
    assert data["cross_checks"]["full_sign_striation_certificate_hessian216"][
        "required_striations"
    ] == ["x", "y", "y=1x", "y=2x"]
    assert (
        data["cross_checks"]["full_sign_striation_certificate_agl23"][
            "min_striation_complete_certificate_size"
        ]
        == 8
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_agl23"][
            "striation_completeness_gap_vs_unconstrained"
        ]
        == 1
    )
    assert (
        data["cross_checks"]["full_sign_striation_certificate_comparison"][
            "striation_complete_sizes_match"
        ]
        is False
    )
