from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5840_5846_matrix_doily_radon.py"
CERT = ROOT / "data" / "PART_W33_PASS5840_5846_MATRIX_DOILY_RADON.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass5840_5846", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_exact_replay_is_byte_stable():
    before = CERT.read_bytes()
    mod = load_module()
    mod.main()
    after = CERT.read_bytes()
    assert after == before


def test_affine_normalizer_and_center():
    d = json.loads(CERT.read_text())
    p = d["pass_5840_affine_determinant_normalizer"]
    assert p["linear_det_rank_stabilizer_order"] == 72
    assert p["left_right_GL2xGL2_order"] == 36
    assert p["transpose_coset_order"] == 36
    assert p["affine_order"] == 1152
    assert p["affine_center_order"] == 1


def test_two_primary_lattice_shadow():
    d = json.loads(CERT.read_text())
    p = d["pass_5841_two_primary_lattice_shadow"]
    assert (p["point_heavy_mod2_gram_rank"], p["point_heavy_mod2_radical_dim"]) == (6, 3)
    assert (p["line_mod2_gram_rank"], p["line_mod2_radical_dim"]) == (4, 5)
    assert p["point_heavy_discriminant_2_torsion_rank"] == 3
    assert p["line_discriminant_2_torsion_rank"] == 5


def test_all_field_radon_multiplicity():
    d = json.loads(CERT.read_text())
    rows = d["pass_5842_all_field_matrix_fourier_radon"]["checked_q"]
    for r in rows:
        q = r["q"]
        assert r["matrix_total"] == q**4
        assert r["radon_kernel"] == r["rank_one"] * (q - 2)
    assert rows[0]["q"] == 2 and rows[0]["radon_kernel"] == 0
    assert all(r["radon_kernel"] > 0 for r in rows[1:])


def test_determinant_polar_doily():
    d = json.loads(CERT.read_text())
    p = d["pass_5843_determinant_polar_two_qubit_doily"]
    assert p["points"] == 15
    assert p["polar_form_rank"] == 4
    assert p["isotropic_lines"] == 15
    assert p["rank_one_points"] == 9 and p["unit_points"] == 6
    assert p["line_type_by_rank_one_point_count"] == {"1": 9, "3": 6}


def test_grid_stabilizer_and_ruling_swap():
    d = json.loads(CERT.read_text())
    p = d["pass_5844_grid_stabilizer_and_ruling_swap"]
    assert p["Sp4_2_order"] == 720
    assert p["grid_stabilizer_order"] == 72
    assert p["grid_orbit_size"] == 10
    assert p["ruling_preserving_subgroup_order"] == 36


def test_same_order_wf4_falsifier():
    d = json.loads(CERT.read_text())
    p = d["pass_5845_order_1152_falsifier"]
    assert p["affine_determinant_group_order"] == p["independent_WF4_reflection_group_order"] == 1152
    assert p["affine_determinant_group_center_order"] == 1
    assert p["WF4_center_order"] == 2


def test_explicit_radical_dimensions():
    d = json.loads(CERT.read_text())
    assert "dimension 3+3-1=5" in d["pass_5846_explicit_radical_geometry"]["line_radical"]
