from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass176_incidence_fixed_line_e8_bridge.json"
SCRIPT = ROOT / "analysis" / "w33_pass176_incidence_fixed_line_e8_bridge.py"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def test_pass176_certificate_is_complete():
    payload = load()
    assert payload["status"] == "PASS"
    assert len(payload["checks"]) == 26
    assert all(payload["checks"].values())


def test_incidence_is_the_objectwise_quadratic_bridge():
    bridge = load()["incidence_bridge"]
    assert bridge["domain"] == "f^perp/<f>"
    assert bridge["codomain"] == "(R cap R^perp)/<all-ones>"
    assert bridge["domain_size_before_quotient"] == 512
    assert bridge["codomain_size_before_quotient"] == 512
    assert bridge["quadratic_identities_checked"] == 512
    assert bridge["equivariance_identities_checked"] == 8192
    assert bridge["native_action_order"] == 25920
    assert bridge["isotropic_anisotropic_quotient_census"] == [136, 120]


def test_weight6_context_words_are_the_two_sheet_cover():
    cover = load()["weight6_sheet_cover"]
    assert cover == {
        "context_words": 240,
        "distinct_shadow_classes": 240,
        "fixed_translation_pairs": 120,
        "paired_support_intersection": 0,
        "route_weight20_images": 240,
    }


def test_anisotropic_polar_graph_is_the_e8_shadow_graph():
    graph = load()["anisotropic_graph"]
    assert graph["parameters"] == [120, 63, 30, 36]
    assert graph["edges"] == 3780
    assert len(graph["adjacency_digest"]) == 64


def test_route_hull_enumerator_and_fixed_image():
    payload = load()
    assert payload["spaces"]["route_hull"] == "[40,9,16]"
    assert payload["spaces"]["route_hull_weight_enumerator"] == {
        "0": 1,
        "16": 135,
        "20": 240,
        "24": 135,
        "40": 1,
    }
    assert payload["incidence_bridge"]["fixed_image"] == "all-ones"


def test_fresh_witness_matches_committed_certificate():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert json.loads(completed.stdout) == load()


def test_public_surfaces_and_scope_boundary():
    payload = load()
    boundary = payload["scope_boundary"]
    assert "native PSp(4,3)" in boundary
    assert "No equality with the full automorphism group" in boundary
    assert "not yet an integral signed E8 Gram realization" in boundary
    assert "thm:pass176-incidence-bridge" in (ROOT / "w33_paper.tex").read_text(
        encoding="utf-8"
    )
    assert 'id="pass176-incidence-fixed-line-e8-bridge"' in (
        ROOT / "docs" / "index.html"
    ).read_text(encoding="utf-8")
