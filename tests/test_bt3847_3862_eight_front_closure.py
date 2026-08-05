import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/PART_BT3847_BT3862_EIGHT_FRONT_CLOSURE_results.json"
SEEDS = ROOT / "data/PART_BT3847_BT3862_TOP115_CYCLIC_SEEDS.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_frozen_status_and_boundaries():
    data = load_result()
    assert data["status"] == "PASS_5_FRONTS_PLUS_3_BONKERS_WITH_TWO_CORRECTIONS"
    assert data["semantic_sha256"] == "f764ac9ada894f4b076c9f2b0b09ea0466337de82bb30836cee76b0c5b5cc2e2"
    assert data["live_boundaries"] == {"cap_maximum": [63, None], "chromatic_number": [10, 11], "covering_radius": [389, 435], "cubic_transversal": [106, 177]}


def test_cubic_cap_and_orbit_code():
    data = load_result(); front = data["fronts"]["cubic_transversal_tightening"]; code = data["bonkers"]["free_cap_orbit_code"]
    assert front["new_cap_size"] == 63 and front["new_transversal_size"] == 177
    assert front["new_interval"] == [106, 177]
    assert front["radius_two_local_optimality"]["locally_optimal"] is True
    assert front["transversal_hit_profile"] == {"1": 876, "2": 2217, "3": 1947}
    assert (code["length"], code["size"], code["constant_weight"], code["minimum_hamming_distance"], code["stabilizer_order"]) == (240, 25920, 63, 62, 1)


def test_tomotope_correction():
    front = load_result()["fronts"]["tomotope_outer_extension_correction"]
    assert front["corrected_exceptional_group"] == "2^4:D12"
    assert front["exceptional_group_center_order"] == 1 and front["split"] is True and front["outer"] is True
    assert front["exact_invariants"]["normal_elementary_abelian_order"] == 16
    assert front["exact_invariants"]["ordinary_kernel_structure"] == "2^4:S3"
    assert front["exact_invariants"]["quotient_order_census"] == {"1": 1, "2": 7, "3": 2, "6": 2}


def test_complete_modular_descent():
    front = load_result()["fronts"]["modular_top115_complete_descent"]
    assert front["dimension_check"] == 115
    assert front["composition_multiset"] == {"1": 3, "5": 3, "10": 3, "14": 3, "25": 1}
    assert sum(front["successive_factor_dimensions"]) == 115 and front["all_factors_absolutely_irreducible"] is True
    seeds = json.loads(SEEDS.read_text(encoding="utf-8"))
    assert sorted(map(int, seeds)) == front["composition_series_dimensions"][1:-1]
    assert len(seeds) == 12 and all(len(vector) == 115 for vector in seeds.values())


def test_gewirtz_residual_and_petersen_blowup():
    data = load_result(); front = data["fronts"]["gewirtz_asymmetric_residual_scheme"]; blowup = data["bonkers"]["gewirtz_residual_Petersen_blowup"]
    assert front["Gewirtz_parameters"] == [56, 10, 0, 2]
    assert front["residual_subdegrees"] == [1, 24, 3, 6, 6]
    assert front["unique_invariant_degree12_union"] == [3, 4]
    assert front["W33_verdict"] == "not SRG(40,12,2,4)"
    assert (blowup["twin_classes"], blowup["class_size"], blowup["quotient_parameters"]) == (10, 4, [10, 3, 0, 1])


def test_cap_fibre_frame():
    frame = load_result()["bonkers"]["cap_fibre_orbit_frame"]
    assert frame["fibre_count"] == 40 and frame["fibre_size"] == 6 and sum(frame["count_vector"]) == 63
    assert frame["count_histogram"] == {"0": 6, "1": 17, "2": 7, "3": 9, "5": 1}
    assert frame["count_vector_orbit_size"] == 25920 and frame["count_vector_stabilizer_order"] == 1
    assert frame["W33_spectral_energies"] == {"-4": "163/8", "12": "3969/40", "2": "157/5"}
