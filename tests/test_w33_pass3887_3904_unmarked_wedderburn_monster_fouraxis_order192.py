from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3887_3904_UNMARKED_WEDDERBURN_MONSTER_FOURAXIS_ORDER192_results.json"
SOURCE = ROOT / "analysis" / "w33_pass3887_3904_unmarked_wedderburn_monster_fouraxis_order192.py"
CANDIDATE = ROOT / "data" / "PART_3887_3904_MONSTER_K43_DESCENT_candidate.json"
LEDGER = ROOT / "data" / "PART_3887_3904_UNMARKED_WEDDERBURN_MONSTER_FOURAXIS_ORDER192_CLAIMS_LEDGER.json"


def load_result():
    return json.loads(RESULT.read_text())


def test_semantic_hash_and_promoted_checks():
    result = load_result()
    semantic = result.pop("semantic_sha256")
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(encoded).hexdigest() == semantic
    assert semantic == "6ef2f6c4a0fa7e52da9f4abff6d899d0250eeabde1a601d53c40052a841e7039"
    assert all(result["checks"].values())


def test_unmarked_automorphism_and_wedderburn_models():
    result = load_result()
    theorem = result["unmarked_automorphism_theorem"]
    assert theorem["axis_norm_squared"] == "480/49"
    assert theorem["unmarked_automorphism_order"] == 51840
    blocks = result["explicit_wedderburn_models"]["block_models"]
    assert {name: block["algebra_block_size"] for name, block in blocks.items()} == {
        "1": 2, "81": 1, "15a": 2, "15b": 1, "24": 3
    }
    inner = result["explicit_wedderburn_models"]["character_inner_products"]
    for left, row in inner.items():
        for right, value in row.items():
            assert value == int(left == right)


def test_four_axis_correction_and_safe_source():
    result = load_result()["four_axis_classification"]
    assert result["class_dimensions"] == [4, 5, 6, 10, 12, 14, 16, 24]
    assert result["corrected_weighted_dimension_census"] == {
        "4": 135, "5": 720, "6": 1080, "10": 16740,
        "12": 5040, "14": 27000, "16": 14040, "24": 84240,
    }
    assert len({tuple(values) for values in result["prime_stability"].values()}) == 1
    source = SOURCE.read_text()
    assert "np.einsum('kab,a,b->k'" not in source
    assert "np.tensordot(structure,x,axes=([1],[0]))" in source


def test_local_algebra_species_are_simple_and_nonunital():
    classes = load_result()["four_axis_classification"]["eight_subalgebra_isomorphism_classes"]
    assert len(classes) == 8
    for record in classes:
        dimension = record["dimension"]
        invariants = record["invariants"]
        assert invariants["multiplication_algebra"] == dimension * dimension
        assert invariants["annihilator"] == 0
        assert invariants["nucleus"] == 0
        assert invariants["trace_form_rank"] == dimension
        assert invariants["associator_ideal"] == dimension
        assert invariants["unital"] is False


def test_k43_hidden_character_and_monster_firewall():
    seed = load_result()["K43_monster_seed"]
    assert seed["incidence_character_norm"] == 23
    assert seed["known_degree_accounted"] == 280
    assert seed["orthogonal_residual_degree"] == 200
    assert seed["orthogonal_residual_character_norm"] == 4
    assert set(seed["orthogonal_residual_inner_products"].values()) == {0}
    candidate = json.loads(CANDIDATE.read_text())
    assert candidate["status"] == "PENDING"
    assert candidate["mm_strings"] == []
    assert candidate["direct_key_hits"] == 0
    assert candidate["class_fusion_artifact_sha256"] is None


def test_order_192_barcodes_and_claims_ledger():
    groups = load_result()["order192_reconciliation"]
    assert groups["W_D4_frame_and_ordered_incident_pair"]["center_order"] == 2
    assert groups["W_D4_frame_and_ordered_incident_pair"]["derived_order"] == 96
    assert groups["involution_centralizer"]["structure"] == "D8 x S4"
    assert groups["involution_centralizer"]["derived_order"] == 24
    assert groups["octonion_axis_line_stabilizer"]["center_order"] == 1
    assert groups["octonion_axis_line_stabilizer"]["order8_elements"] == 48
    assert groups["exceptional_tomotope_completion"]["structure"] == "2^4:D12"
    ledger = json.loads(LEDGER.read_text())
    assert len(ledger["withdrawn_or_corrected"]) == 1
    assert "overflowed" in ledger["withdrawn_or_corrected"][0]["reason"]
