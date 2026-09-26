"""Regression for Passes 10970-10971: clock-code lattice tower and selector no-go."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / "analysis" / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P70 = load("p10970", "w33_pass10970_projective_clock_code_lattice_tower.py")
P71 = load("p10971", "w33_pass10971_clock_selector_symmetry_no_go.py")
C70 = json.loads((ROOT / "data" / "w33_pass10970_projective_clock_code_lattice_tower.json").read_text())
C71 = json.loads((ROOT / "data" / "w33_pass10971_clock_selector_symmetry_no_go.json").read_text())


def test_pass10970_certificate_passes():
    p = P70.payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())


def test_q3_recovers_tetracode_e8():
    p = C70
    assert p["q_samples"]["3"]["parameters"] == [4, 2, 3]
    assert p["q3"]["weight_enumerator"] == {"0": 1, "3": 8}
    assert p["q3"]["total_roots"] == 240
    assert p["q3"]["identification"] == "E8"
def test_q5_is_equivariant_A4_6_niemeier_glue():
    q5 = C70["q_samples"]["5"]
    n = C70["q5"]
    assert q5["parameters"] == [6, 3, 4]
    assert q5["weight_enumerator"] == {"0": 1, "4": 60, "5": 24, "6": 40}
    assert q5["minimum_nonzero_glue_coset_norm"] == "4"
    assert n["rank"] == 24
    assert n["new_roots_from_glue"] == 0
    assert n["identification"] == "Niemeier lattice N(A4^6)"
    assert n["PGL2_5_code_action"]["pgl2_order"] == 120
    assert n["PGL2_5_code_action"]["distinct_permutations"] == 120
    assert n["repo_P1F5_weld"]["S5_action_conjugate_to_PGL2_5"]


def test_lattice_rank_equals_nonzero_null_shell():
    for q in ("3", "5", "7"):
        x = C70["q_samples"][q]
        assert x["lattice_rank"] == x["null_cone"]["nonzero_null_vectors"]
        assert x["null_cone"]["nonzero_null_vectors"] == int(q) ** 2 - 1
        assert x["all_glue_cosets_even"]


def test_q3_is_only_root_creating_sample():
    qs = C70["q_samples"]
    assert qs["3"]["glue_can_create_roots_by_bound"]
    assert not qs["5"]["glue_can_create_roots_by_bound"]
    assert not qs["7"]["glue_can_create_roots_by_bound"]
def test_pass10971_certificate_passes():
    p = P71.payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())


def test_full_clock_symmetry_has_two_dimensional_commutant():
    for q in ("3", "5", "7"):
        x = C71[f"q{q}"]
        assert x["commutant_dimension"] == 2
        assert x["commutant_basis"] == ["I", "J"]
        assert not x["basis_clock_can_be_nondegenerate_eigenstate"]


def test_q3_clock_selection_breaks_S4_to_S3():
    x = C71["q3"]
    assert x["PGL2_order"] == 24
    assert x["point_stabilizer_order"] == 6
    assert x["symmetry_breaking_index"] == 4
    assert x["augmentation_dimension"] == 3
    assert x["augmentation_selector_orbit_size"] == 4


def test_q5_selector_is_pass593_augmentation_five():
    x = C71["q5"]
    assert x["PGL2_order"] == 120
    assert x["point_stabilizer_order"] == 20
    assert x["symmetry_breaking_index"] == 6
    assert x["augmentation_dimension"] == 5
    assert C71["checks"]["q5_matches_Pass593_augmentation"]
