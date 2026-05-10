"""Regression tests for PART CCCXXVII mass-mixing closure surface."""

from __future__ import annotations

import json
import subprocess
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "exploration" / "PART_CCCXXVII_MASS_MIXING_CLOSURE_SURFACE.py"
RESULTS = ROOT / "PART_CCCXXVII_mass_mixing_closure_surface_results.json"


@lru_cache(maxsize=1)
def run_surface() -> dict:
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
    return json.loads(RESULTS.read_text(encoding="utf-8"))


def test_mass_mixing_surface_generates_verified_artifact():
    data = run_surface()
    assert data["part"] == "CCCXXVII"
    assert data["all_within_2sigma"] is True
    assert data["all_internal_identities_pass"] is True
    assert data["degrees_of_freedom"] == 6
    assert data["reduced_chi2"] < 0.34
    assert data["max_abs_z"] <= 1.0 + 1e-12


def test_mass_mixing_surface_uses_correct_w33_atoms_and_identities():
    data = run_surface()
    assert data["atoms"] == {
        "q": 3,
        "lambda": 2,
        "mu": 4,
        "k": 12,
        "v": 40,
        "Phi3": 13,
        "Phi4": 10,
        "Phi6": 7,
    }
    identities = data["internal_identities"]
    assert identities["q_factorial_seed"] is True
    assert identities["srg_vertex_formula"] is True
    assert identities["srg_valency_formula"] is True
    assert identities["higgs_denominator_is_phi4_squared"] is True
    assert identities["ckm_lambda_denominator_is_vertex_count"] is True


def test_mass_mixing_surface_observables_are_the_expected_sheet():
    data = run_surface()
    observables = {entry["name"]: entry for entry in data["observables"]}
    assert set(observables) == {
        "lambda_H_MSbar_MZ",
        "wolf_lambda",
        "wolf_A",
        "wolf_rhobar",
        "wolf_etabar",
        "top_yukawa_pole",
    }
    assert observables["lambda_H_MSbar_MZ"]["formula"] == "Phi_3/Phi_4^2 = 13/100"
    assert observables["wolf_lambda"]["formula"] == "q^2/v = 9/40"
    assert observables["wolf_A"]["formula"] == "q^4/Phi_4^2 = 81/100"
    assert observables["wolf_etabar"]["formula"] == "(Phi_6/Phi_4)^3 = 343/1000"
    assert observables["top_yukawa_pole"]["formula"] == "(v/(v+1))^(1/3)"
    assert all(abs(entry["z"]) <= 1.0 + 1e-12 for entry in observables.values())
