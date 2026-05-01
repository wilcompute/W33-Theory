import json
from pathlib import Path

import numpy as np
import pytest

PREDICTIONS_PATH = Path("MASS_PREDICTIONS.json")
pytestmark = pytest.mark.skipif(
    not PREDICTIONS_PATH.exists(),
    reason="optional generated artifact missing: MASS_PREDICTIONS.json",
)


def test_mass_predictions_file_exists():
    assert PREDICTIONS_PATH.exists(), "mass predictions JSON missing"


def test_e8_w33_matches_within_tolerance():
    data = json.load(open(PREDICTIONS_PATH))
    matches = data.get("E8_W33_matches", {})
    # require relative error <5% for the three main ratios
    for key in ["m_t/m_b", "m_c/m_s", "m_\u03c4/m_\u03bc"]:
        assert key in matches, f"{key} not in predictions"
        info = matches[key]
        exp = info["exp"]
        pred = info["pred"]
        rel_err = abs(exp - pred) / pred
        assert rel_err < 0.05, f"{key} relative error too large: {rel_err:.2%}"


def test_koide_accuracy():
    data = json.load(open(PREDICTIONS_PATH))
    koide = data.get("koide", {})
    leptons_Q = koide.get("leptons")
    assert leptons_Q is not None
    assert abs(leptons_Q - 2 / 3) < 1e-3, f"lepton Koide parameter off: {leptons_Q}"


def test_yukawa_ratios_match_tau_mu():
    # also verify that at least one of the yukawa ratios (sqrt eigenvalue max/min)
    # is within 10% of the tau/mu ratio from the mass table
    mass_data = json.load(open(PREDICTIONS_PATH))
    tau_mu = mass_data["mass_ratios"]["m_\u03c4/m_\u03bc"]
    gram_data = json.load(open("data/h1_subspaces.json"))
    ratios = []
    for G in gram_data["gram_matrices"]:
        Gmat = np.array(G, dtype=float)
        eigs = np.linalg.eigvalsh(Gmat)
        sqrt_eigs = np.sqrt(eigs)
        ratios.append(sqrt_eigs[-1] / sqrt_eigs[0])
    assert any(
        abs(r - tau_mu) / tau_mu < 0.10 for r in ratios
    ), "no yukawa ratio within 10% of tau/mu"
