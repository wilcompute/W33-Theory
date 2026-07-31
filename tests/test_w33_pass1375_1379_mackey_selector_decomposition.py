from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass1375_1379_mackey_selector_decomposition.json"


def load():
    result = json.loads(DATA.read_text())
    assert result["schema"] == "w33.pass1375_1379.mackey_selector_decomposition.compact.v1"
    assert result["status"] == "PASS"
    return result


def test_little_group_character_table():
    result = load()["pass1375_little_group_character_table"]
    assert result["dual_orbit_sizes"] == [1, 2, 4, 4, 8, 8]
    assert sum(result["dual_orbit_sizes"]) == 27
    assert result["little_group_orders"] == [16, 8, 4, 4, 2, 2]
    assert all(a * b == 16 for a, b in zip(result["dual_orbit_sizes"], result["little_group_orders"]))
    census = {int(degree): count for degree, count in result["irreducible_degree_census"].items()}
    assert sum(count for count in census.values()) == 27
    assert sum(count * degree * degree for degree, count in census.items()) == 432


def test_selector_character_and_commutant():
    result = load()["pass1376_selector_permutation_character"]
    degrees = result["constituent_degree_profile"]
    multiplicities = result["multiplicity_profile"]
    assert len(degrees) == len(multiplicities) == 14
    assert sum(d * m for d, m in zip(degrees, multiplicities)) == 120
    assert sum(m * m for m in multiplicities) == 83


def test_wedderburn_projector_identification():
    result = load()["pass1377_mackey_wedderburn_identification"]
    assert result["dimension"] == 83
    assert result["center_dimension"] == 14
    assert result["exact_projector_matches"] == 14
    assert result["wedderburn"] == "Q^7 + M2(Q)^2 + M3(Q)^3 + M4(Q) + M5(Q)"


def test_terwilliger_fusion_defect():
    result = load()["pass1378_terwilliger_fusion_explanation"]
    sizes = result["fusion_group_sizes"]
    assert len(sizes) == 10
    assert sum(sizes) == 14
    assert sum(size - 1 for size in sizes) == 4
    assert result["scalar_packet_sizes"] == [2, 2, 3]
    assert result["scalar_splitter_eigenvalue_packets"] == [[-4, -1, 2], [-3, 0], [-3, 3]]
    assert result["orbital_center_dimension"] - result["terwilliger_center_dimension"] == 4


def test_claim_boundary():
    result = load()["pass1379_boundary"]
    assert "no database table" in result["mathematics"]
    assert "no particle" in result["physics"]
