import importlib.util
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_pass5744_5751_quadratic_code_overlays.py"
FROZEN = ROOT / "data/PART_W33_PASS5744_5751_QUADRATIC_CODE_OVERLAYS.json"

spec = importlib.util.spec_from_file_location("pass5744_5751", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@lru_cache(maxsize=1)
def cert():
    return mod.compute_certificate()


def frozen():
    return json.loads(FROZEN.read_text(encoding="utf-8"))


def test_exact_replay_matches_frozen_certificate():
    assert cert() == frozen()


def test_known_classical_code_is_not_misclaimed_as_novel():
    c = cert()
    assert c["pass_5744"]["parameters"] == [40, 10, 18]
    assert "prior art" in c["prior_art"]["claim_tier"]
    assert "Rodrigues" in c["prior_art"]
    assert "Kaipa_Pradhan_2024" in c["prior_art"]


def test_sparse_w33_coordinate_bridge():
    c = cert()
    assert c["pass_5745"]["C_nnz"] == 1080
    assert c["pass_5745"]["factorized_term_count"] == 442
    assert c["pass_5745"]["B_nnz"] == 10
    assert c["pass_5745"]["B_squared_is_identity"] is True


def test_css_line_geometry_and_repair():
    c = cert()
    assert c["pass_5746"]["standard_css_consequence"] == "[[40,20,4]]_3"
    assert c["pass_5747"]["minimum_projective_supports"] == 130
    assert c["pass_5747"]["minimum_vector_words"] == 260
    assert c["pass_5748"]["repair_groups_per_coordinate"] == 13
    assert c["pass_5748"]["w33_native_groups"] == 4
    assert c["pass_5748"]["ambient_nonisotropic_groups"] == 9


def test_minimum_logical_commutation_graph():
    c = cert()
    assert c["pass_5750"]["srg"] == [130, 48, 20, 16]
    assert c["pass_5750"]["w33_isotropic_induced_srg"] == [40, 12, 2, 4]


def test_reconfigurable_symplectic_overlay_family():
    c = cert()
    assert c["pass_5751"]["PGL4_order"] == 12130560
    assert c["pass_5751"]["PGSp4_order"] == 51840
    assert c["pass_5751"]["symplectic_overlays"] == 234
    assert c["pass_5751"]["distinct_overlay_matrices"] == 234
    assert c["pass_5751"]["all_overlays_same_code"] is True
    assert c["pass_5751"]["each_line_native_in_overlays"] == 72
