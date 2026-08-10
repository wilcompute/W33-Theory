from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass1380_1384_mackey_selector_decomposition.json"


def load():
    result = json.loads(DATA.read_text(encoding="utf-8"))
    assert result["schema"] == "w33.pass1380_1384.mackey_selector_decomposition.compact.v1"
    assert result["status"] == "PASS"
    return result


def test_little_group_character_table():
    result = load()["pass1380_little_group_character_table"]
    assert result["dual_orbit_sizes"] == [1, 2, 4, 4, 8, 8]
    assert sum(result["dual_orbit_sizes"]) == 27
    assert result["little_group_orders"] == [16, 8, 4, 4, 2, 2]
    assert all(a * b == 16 for a, b in zip(result["dual_orbit_sizes"], result["little_group_orders"]))
    census = {int(degree): count for degree, count in result["irreducible_degree_census"].items()}
    assert sum(count for count in census.values()) == 27
    assert sum(count * degree * degree for degree, count in census.items()) == 432


def test_selector_character_and_commutant():
    result = load()["pass1381_selector_permutation_character"]
    degrees = result["constituent_degree_profile"]
    multiplicities = result["multiplicity_profile"]
    assert len(degrees) == len(multiplicities) == 14
    assert sum(d * m for d, m in zip(degrees, multiplicities)) == 120
    assert sum(m * m for m in multiplicities) == 83


def test_wedderburn_projector_identification():
    result = load()["pass1382_mackey_wedderburn_identification"]
    assert result["dimension"] == 83
    assert result["center_dimension"] == 14
    assert result["exact_projector_matches"] == 14


def test_terwilliger_fusion_defect():
    result = load()["pass1383_terwilliger_fusion_explanation"]
    sizes = result["fusion_group_sizes"]
    assert len(sizes) == 10 and sum(sizes) == 14
    assert sum(size - 1 for size in sizes) == 4
    assert result["scalar_packet_sizes"] == [2, 2, 3]
    assert result["scalar_splitter_eigenvalue_packets"] == [[-4, -1, 2], [-3, 0], [-3, 3]]


def test_claim_boundary():
    result = load()["pass1384_boundary"]
    assert "no database table" in result["mathematics"]
    assert "no particle" in result["physics"]
