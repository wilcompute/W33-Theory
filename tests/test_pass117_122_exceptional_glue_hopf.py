"""Focused regression for Passes 98-103."""

from __future__ import annotations

import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(module: str, artifact: str) -> dict:
    loaded = importlib.import_module(module)
    assert loaded.main() == 0
    return json.loads((ROOT / artifact).read_text(encoding="utf-8"))


def test_pass98_e6_embedding_and_branching() -> None:
    data = run("w33_pass117_o8_e6_embedding", "w33_pass117_o8_e6_embedding.json")
    assert data["pair_stabilizer_order"] == 51840
    assert data["weyl_e6_orbits_on_anisotropic"] == [1, 1, 1, 27, 27, 27, 36]


def test_pass99_exact_lattice_quotient() -> None:
    data = run(
        "w33_pass118_lattice_intersection", "w33_pass118_lattice_intersection.json"
    )
    assert data["quotient"]["order"] == 256
    assert data["determinants"]["scaled_intersection"] == 2**8 * 3**10 * 5


def test_pass100_exact_mass() -> None:
    data = run("w33_pass119_exact_2adic_mass", "w33_pass119_exact_2adic_mass.json")
    assert data["validation"]["sqrt2_E8_pmass_ratio"] == "1"
    assert float(data["exact_genus_mass_approx"]) > 1e80


def test_pass101_anisotropic_srg() -> None:
    data = run("w33_pass120_srg120_anisotropic", "w33_pass120_srg120_anisotropic.json")
    assert data["parameters"] == [120, 63, 30, 36]
    assert data["spectrum"] == {"-9": 35, "3": 84, "63": 1}


def test_pass102_theta_newforms() -> None:
    data = run("w33_pass121_weight20_theta", "w33_pass121_weight20_theta.json")
    assert data["theta_coefficients_q0_to_q20"][:4] == [1, 80, 14640, 5403840]
    assert data["newform_coefficients"] == {
        "a2_plus_512": "6784/279",
        "a2_minus_512": "86400/3403",
    }


def test_pass103_finite_hopf_boundary() -> None:
    run("w33_pass117_o8_e6_embedding", "w33_pass117_o8_e6_embedding.json")
    run("w33_pass120_srg120_anisotropic", "w33_pass120_srg120_anisotropic.json")
    data = run("w33_pass122_hopf_synthesis", "w33_pass122_hopf_synthesis.json")
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
