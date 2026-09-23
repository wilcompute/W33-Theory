from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TEXT_SURFACES = [
    ROOT / "analysis/w33_e8_matter81_h27_address_operator_compiler.py",
    ROOT / "analysis/w33_qpsi_gq24_parabolic_compiler.py",
    ROOT / "analysis/w33_steiner_trinification_qpsi_normalizer.py",
    ROOT / "analysis/2026-09-21_e8_matter81_h27_address_operator_compiler.md",
    ROOT / "analysis/2026-09-22_qpsi_gq24_parabolic_compiler.md",
    ROOT / "analysis/2026-09-22_steiner_trinification_qpsi_normalizer.md",
    ROOT / "analysis/PASS20260921_e8_matter81_h27_address_operator_compiler_insert.tex",
    ROOT / "analysis/PASS20260922_qpsi_gq24_parabolic_compiler_insert.tex",
    ROOT / "analysis/PASS20260922_steiner_trinification_qpsi_normalizer_insert.tex",
    ROOT / "docs/index.html",
]

CERTIFICATES = [
    ROOT / "data/w33_e8_matter81_h27_address_operator_compiler.json",
    ROOT / "data/w33_qpsi_gq24_parabolic_compiler.json",
    ROOT / "data/w33_steiner_trinification_qpsi_normalizer.json",
]


def test_no_surface_reopens_the_compiler_that_is_now_explicit():
    banned = (
        "symmetry-changing compiler remains open",
        "symmetry-changing coordinate dictionary left open",
        "select a symmetry-changing frozen-root-to-trinification operator dictionary",
    )
    for path in TEXT_SURFACES:
        text = path.read_text(encoding="utf-8")
        for phrase in banned:
            assert phrase not in text, (path, phrase)


def test_all_three_frontiers_consume_the_minimal_54_retyping_certificate():
    minimal = json.loads(
        (ROOT / "data/w33_minimal_symmetry_changing_81_compiler.json").read_text()
    )["compiler"]
    assert minimal["symmetry_changing_coordinates"] == 54
    assert minimal["symmetry_change_lower_bound"] == 54
    assert minimal["lower_bound_saturated"] is True
    for path in CERTIFICATES:
        result = json.loads(path.read_text())
        inherited = result["minimal_symmetry_changing_compiler"]
        assert inherited["symmetry_changing_coordinates"] == 54
        assert inherited["lower_bound_saturated"] is True
        assert inherited["mapping_digest"] == minimal["mapping_digest"]
        frontier = result["equivariant_compiler_obstruction"]["surviving_frontier"]
        assert "54" in frontier
        assert "Fourier" in frontier
