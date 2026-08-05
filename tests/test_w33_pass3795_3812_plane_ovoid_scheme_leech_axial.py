from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3795_3812_PLANE_OVOID_SCHEME_LEECH_AXIAL_results.json"
TRANSPORT = ROOT / "data" / "PART_3795_3812_LEECH_AXIAL_TRANSPORT.json"
LEDGER = ROOT / "data" / "PART_3795_3812_PLANE_OVOID_SCHEME_LEECH_AXIAL_CLAIMS_LEDGER.json"
EXPECTED = "be5ee56a84141a7bbc896b4cef0e8eda32167a00749dbb17f10d24d0505bdd41"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_certificate_and_source_chunks():
    result = load(RESULT)
    assert result["status"] == "PASS_EXACT_FIVE_FRONTS_THREE_CONSTRUCTIONS_MONSTER_WORDS_PENDING"
    assert result["semantic_sha256"] == EXPECTED
    assert len(result["checks"]) == 15 and all(result["checks"].values())
    for index in range(1, 5):
        assert (ROOT / "analysis" / f"_w33_pass3795_3812_impl_part{index}.pyinc").is_file()
    assert (ROOT / "analysis" / "w33_pass3795_3812_plane_ovoid_scheme_leech_axial.py").is_file()


def test_dictionary_coherent_configuration_and_flag_reconstruction():
    result = load(RESULT)
    dictionary = result["w33_plane_ovoid_dictionary"]
    assert dictionary["isomorphism_torsor_size"] == 51840
    assert dictionary["w33_lines"] == 40 and dictionary["spreads"] == 36
    scheme = result["ovoid_coherent_configuration"]
    assert scheme["fibers"] == [40, 160]
    assert scheme["ordered_pair_orbitals"] == 19
    assert scheme["intersection_tensor_shape"] == [19, 19, 19]
    assert sum(scheme["orbital_sizes"]) == 40000
    flags = result["tripod_double_fibration"]
    assert flags["blocks_in_each_partition"] == [40, 40]
    assert flags["incidence_ones"] == 160
    assert flags["reconstructed_graph_srg"] == [40, 12, 2, 4]


def test_rootless_leech_and_exact_stabilizer():
    result = load(RESULT)
    leech = result["rootless_leech_polarization"]
    assert leech["golay_parameters"] == [24, 12, 8]
    assert leech["octads"] == 759
    assert leech["gram_determinant"] == 1
    assert leech["minimum_norm"] == 4
    assert leech["exact_vectors_of_norm_at_most_2"] == 1
    assert leech["surviving_U4_2_stabilizer_order"] == 2
    transport = load(TRANSPORT)
    assert len(transport["transport"]) == 24
    assert {len(row) for row in transport["transport"]} == {24}
    assert transport["expected_axial_gram_sha256"] == leech["axial_gram_sha256"]


def test_descent_and_intrinsic_axial_census():
    result = load(RESULT)
    descent = result["finite_group_descent"]
    assert descent["full_group_order"] == 51840
    assert descent["even_subgroup_order"] == 25920
    assert sum(descent["full_element_order_census"].values()) == 51840
    axial = result["intrinsic_axial_classification"]
    assert axial["dimension"] == 24 and axial["axes"] == 45
    assert axial["full_axis_kernel_dimension"] == 21
    assert axial["pair_generated_dimensions"] == {"collinear": 2, "noncollinear": 4}
    assert axial["three_axis_universal_orbit_size"] == 2880
    assert axial["unital"] is False and axial["simple"] is True


def test_claims_remain_fail_closed():
    result = load(RESULT)
    ledger = load(LEDGER)
    assert ledger["semantic_sha256"] == EXPECTED
    assert "FAIL_CLOSED" in result["finite_group_descent"]["monster_status"]
    boundary = " ".join(ledger["fail_closed"]).lower()
    for token in ("monster", "griess", "remote ci", "hardware"):
        assert token in boundary
