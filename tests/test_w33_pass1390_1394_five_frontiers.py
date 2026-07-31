import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "w33_pass1390_1394_five_frontiers.json").read_text())


def test_1390_modular_localization_and_loewy():
    p = DATA["pass1390"]
    assert p["localization"] == {
        "2": {"collapsed_projectors": 13, "localizable_projectors": 1},
        "3": {"collapsed_projectors": 14, "localizable_projectors": 0},
        "5": {"collapsed_projectors": 0, "localizable_projectors": 14},
    }
    assert p["full_orbital_modular_profiles"]["2"]["radical_power_dimensions"] == [45, 16, 0]
    assert p["full_orbital_modular_profiles"]["3"]["radical_power_dimensions"] == [72, 49, 27, 14, 4, 0]
    assert p["full_orbital_modular_profiles"]["5"]["jacobson_radical_dimension"] == 0


def test_1391_intrinsic_dual_orbits():
    p = DATA["pass1391"]
    assert p["orbit_sizes"] == [1, 2, 4, 4, 8, 8]
    assert p["invariant_dual_axis"] == [1, 0, 1]
    assert p["plane_quadratic_form"] == [[2, 0], [0, 2]]
    assert [(r["size"], r["signature"]) for r in p["orbit_classification"]] == [
        (1, "zero"), (2, "hinge_charge"), (4, "neutral_diagonal"),
        (4, "neutral_axis"), (8, "charged_diagonal"), (8, "charged_axis"),
    ]


def test_1392_exact_fourier_transform():
    p = DATA["pass1392"]
    assert sum(p["block_dimensions"]) == 120
    assert p["exact_inverse_verified"] is True
    assert p["forward_basis_U"]["max_denominator"] == 54
    assert p["inverse_transform_Uinv"]["max_denominator"] == 3
    assert set(p["operator_hashes"]) == {"A", "D", "S"}


def test_1393_selector_apartment_bridge():
    p = DATA["pass1393"]
    assert p["sheet_rank"] == 81 and p["sheet_boundaryless"] is True
    assert {x["rank"] for x in p["bridge_scan"].values()} == {81}
    assert {x["bridge_rank"] for x in p["mackey_sector_bridge_ranks"]} == {
        x["source_isotypic_dimension"] for x in p["mackey_sector_bridge_ranks"]
    }


def test_1394_integral_order_commensurability():
    p = DATA["pass1394"]
    assert p["O_contained_in_selected_M"] is False
    assert p["selected_M_contained_in_O"] is False
    assert p["index_O_over_intersection"] == "4"
    assert p["discriminant_factorization"] == {"2": 72, "3": 226}
    assert p["local_discriminant_maximality_test"] == {"2": False, "3": False, "5": True}
    assert p["level_O_to_M"] == 2 and p["level_M_to_O"] == 108
