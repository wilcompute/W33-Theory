import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_4689_three_39d_carriers_are_not_isomorphic():
    d = load("PART_W33_PASS4689_THREE_39D_MODULE_COMPARISON.json")
    assert d["canonical_cross_shell_split"]["dimensions"] == [15, 24, 39]
    e = d["equivariant_comparison"]
    assert e["Hom_Hcross_to_Cap_dimension"] == 2
    assert e["ranks_of_three_nonzero_maps_Hcross_to_Cap"] == [14, 14, 14]
    assert e["Hom_Cap_to_Hcross_dimension"] == 2
    assert e["ranks_of_three_nonzero_maps_Cap_to_Hcross"] == [1, 1, 1]


def test_4690_full_sextet_affine_group():
    d = load("PART_W33_PASS4690_FULL_SEXTET_AFFINE_GROUP.json")
    assert d["translation_subgroup"]["order"] == 64
    assert d["translation_subgroup"]["structure"] == "C2^6"
    assert d["translation_subgroup"]["regular_on_transversals"] is True
    assert d["point_stabilizer"]["order"] == 2160
    assert d["point_stabilizer"]["nonzero_translation_orbits"] == [18, 45]
    assert d["affine_action"]["faithful_H_order"] == 138240


def test_4691_explicit_rootless_leech_neighbor():
    d = load("PART_W33_PASS4691_EXPLICIT_LEECH_TWO_NEIGHBOR.json")
    b = d["explicit_basis"]
    r = d["rootlessness"]
    assert b["numerator_determinant"] == 2**36
    assert b["gram_determinant"] == 1
    assert b["integral_even_gram"] is True
    assert r["all_old_roots_have_odd_v_pairing"] is True
    assert r["minimum_norm"] == 4


def test_4692_closed_c8_masses_need_embedding_invariants():
    d = load("PART_W33_PASS4692_C8_CLOSED_LOCAL_MASS_FORMULAS.json")
    z = d["same_parameter_counterexample"]
    w = z["W33"]
    q = z["dual_W33"]
    assert (w["s"], w["t"]) == (3, 3)
    assert (q["s"], q["t"]) == (3, 3)
    assert (w["rho"], w["sigma"], w["tau"]) == (0, 16, 1)
    assert (q["rho"], q["sigma"], q["tau"]) == (4, 0, 3)
    assert (w["apartment_coefficient"], w["star_coefficient"]) == (712, 180)
    assert (q["apartment_coefficient"], q["star_coefficient"]) == (728, 252)


def test_4693_support12_exact_spectrum():
    d = load("PART_W33_PASS4693_SUPPORT12_TRANSITIVITY_EXACT.json")
    assert d["subsets"] == 5_586_853_480
    assert d["distinct_weights"] == 151
    assert (d["minimum_weight"], d["minimum_count"]) == (608, 1620)
    assert (d["maximum_weight"], d["maximum_count"]) == (990, 4320)
    assert sum(int(v) for v in d["spectrum"].values()) == d["subsets"]


def test_4694_golay_affine_sixspace_is_not_orthogonal_u6():
    d = load("PART_W33_PASS4694_GOLAY_AFFINE_U6_FORM_NOGO.json")
    assert d["K_order"] == 2160
    assert d["invariant_quadratic_space_dimension"] == 0
    assert d["invariant_bilinear_space_dimension"] == 0


def test_4695_support12_minima_are_apartment_thickenings():
    d = load("PART_W33_PASS4695_SUPPORT12_MINIMA_APARTMENT_THICKENINGS.json")
    assert d["objects"] == {"apartments": 1620, "support12_minima": 1620, "thickenings_distinct": 1620}
    t = d["corner_star_thickening"]
    assert (t["size"], t["apartment_code_weight"]) == (12, 608)
    assert d["intrinsic_inverse"]["unique"] is True


def test_4696_even_apartment_subcode():
    d = load("PART_W33_PASS4696_THICKENING_SPAN_EVEN_APARTMENT_SUBCODE.json")
    c = d["coefficient_space"]
    s = d["image_subcode"]
    assert c["even_hyperplane_dimension"] == 39
    assert c["thickening_mask_rank"] == 39
    assert s["dimension"] == 38
    assert s["parameters"] == "[1620,38,270]"
    assert (s["minimum_weight"], s["minimum_words"]) == (270, 240)
