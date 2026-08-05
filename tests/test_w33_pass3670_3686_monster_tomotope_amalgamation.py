from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3670_3686_MONSTER_TOMOTOPE_AMALGAMATION_results.json"


def load():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_semantic_hash_and_all_checks():
    data = load()
    expected = data.pop("semantic_sha256")
    observed = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert observed == expected == "2d5fe418bb2bbee0eb479e42d22dd47d31c37f7d5f8be6b1732acf0dc1db8b78"
    assert all(data["checks"].values())


def test_chamber_and_tomotope_closure():
    data = load()
    chamber = data["chamber_association_scheme"]
    lift = data["tomotope_central_lift"]
    assert chamber["relation_12_srg"]["parameters"] == [36, 15, 6, 6]
    assert chamber["u42_suborbits"] == [1, 15, 20]
    assert lift["maximal_K4s"] == 135
    assert lift["chamber_K4_incidences"] == 540
    assert lift["K4_stabilizer_order"] == 192
    assert lift["central_quotient_order"] == 96
    assert lift["marked_generator_isomorphism"] is True
    assert lift["non_split"] is True


def test_amalgam_glue_product_and_moonshine_boundaries():
    data = load()
    amalgam = data["thick_parabolic_amalgam"]
    glue = data["nonscalar_discriminant_glue"]
    algebra = data["equivariant_product_envelope"]
    moonshine = data["prime_mckay_thompson_channels"]
    firewall = data["spectral_doppelganger_firewall"]
    assert amalgam["panel_thicknesses"] == [3, 3, 3, 3]
    assert amalgam["core_order"] == 1
    assert glue["determinant"] == 1 and glue["even"] is True
    assert glue["signature"] == [24, 24]
    assert algebra["Hom_Sym2V_to_V_dimension"] == 2
    assert algebra["associator_gcd_degree"] == 0
    assert [row["prime"] for row in moonshine["eta_channels"]] == [2, 3, 5]
    assert firewall["w33_character_norm"] == firewall["chamber_character_norm"] == 1
    assert firewall["character_inner_product"] == 0
