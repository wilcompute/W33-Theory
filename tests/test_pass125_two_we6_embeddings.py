"""Regression tests for Pass 125's two W(E6) embeddings."""

from __future__ import annotations

import json
from pathlib import Path

import w33_pass125_two_we6_embeddings as pass125

ROOT = Path(__file__).resolve().parents[1]


def test_pass125_regenerates_exact_certificate() -> None:
    assert pass125.main() == 0
    data = json.loads(
        (ROOT / "w33_pass125_two_we6_embeddings.json").read_text(encoding="utf-8")
    )

    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["generators"]["PSp43_projective_order"] == 25_920
    assert data["generators"]["PGSp43_projective_order"] == 51_840
    assert data["code_embedding"]["quotient_image_order"] == 51_840
    assert data["code_embedding"]["faithful"] is True


def test_pass125_measures_code_embedding_orbits() -> None:
    data = json.loads(
        (ROOT / "w33_pass125_two_we6_embeddings.json").read_text(encoding="utf-8")
    )

    assert data["code_embedding"]["orbit_fingerprint_size_Q"] == [
        [1, 0],
        [120, 1],
        [135, 0],
    ]
    assert data["code_embedding"]["isotropic_nonzero_orbits"] == [135]
    assert data["code_embedding"]["anisotropic_orbits"] == [120]
    assert data["code_embedding"]["stabilizers"] == {
        "isotropic": 384,
        "anisotropic": 432,
    }


def test_pass125_distinguishes_pass117_embedding() -> None:
    data = json.loads(
        (ROOT / "w33_pass125_two_we6_embeddings.json").read_text(encoding="utf-8")
    )

    assert data["pass117_ordered_pair_embedding"]["isotropic_orbits"] == [
        27,
        36,
        36,
        36,
    ]
    assert data["pass117_ordered_pair_embedding"]["anisotropic_orbits"] == [
        1,
        1,
        1,
        27,
        27,
        27,
        36,
    ]
    assert "not conjugate" in data["nonconjugacy_certificate"]
