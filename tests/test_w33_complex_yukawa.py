"""Tests for scripts/w33_complex_yukawa.py.

Verifies:
  1. The script runs and produces data/w33_complex_yukawa.json
  2. The Z3 complex profiles are correctly complex (psi_1 is complex)
  3. CKM error < real-profile baseline (complex profiles improve on real)
  4. Mean-profile Jarlskog remains zero at the exact layer
  5. CKM matrix is diagonal-dominant
  6. PMNS error < 0.20 (large-angle lepton mixing reproduced)
  7. PMNS matrix is approximately bi-large (first two columns mixed)
"""

import json
import math
import os
import subprocess
import sys

import numpy as np
import pytest


@pytest.fixture(scope="module")
def results():
    """Run the script once and return the parsed JSON output."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    res = subprocess.run(
        [sys.executable, "scripts/w33_complex_yukawa.py"],
        env=env,
        capture_output=True,
        text=True,
        cwd=os.path.abspath("."),
    )
    assert res.returncode == 0, f"script failed:\n{res.stderr}\n{res.stdout}"
    assert os.path.exists("data/w33_complex_yukawa.json"), "JSON output not written"
    with open("data/w33_complex_yukawa.json") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# basic sanity
# ---------------------------------------------------------------------------


def test_script_runs(results):
    assert results is not None


def test_json_has_expected_keys(results):
    for key in [
        "complex_best_ckm",
        "complex_best_pmns",
        "real_baseline_ckm_error",
        "identity_ckm_baseline",
    ]:
        assert key in results, f"Missing key: {key}"


def test_complex_best_ckm_exists(results):
    assert results["complex_best_ckm"] is not None
    assert "ckm_error" in results["complex_best_ckm"]
    assert "Jarlskog" in results["complex_best_ckm"]
    assert "V_CKM" in results["complex_best_ckm"]


def test_complex_best_pmns_exists(results):
    assert results["complex_best_pmns"] is not None
    assert "pmns_error" in results["complex_best_pmns"]
    assert "V_PMNS" in results["complex_best_pmns"]


# ---------------------------------------------------------------------------
# CKM tests
# ---------------------------------------------------------------------------


def test_complex_ckm_improves_over_real_baseline(results):
    """Complex Z3 profiles should reduce CKM error below the real-profile baseline."""
    real_err = results["real_baseline_ckm_error"]
    complex_err = results["complex_best_ckm"]["ckm_error"]
    assert complex_err < real_err, (
        f"Complex CKM error {complex_err:.4f} is not better than "
        f"real baseline {real_err:.4f}"
    )


def test_complex_ckm_below_identity(results):
    """Best complex CKM error should be below the trivial identity baseline."""
    err = results["complex_best_ckm"]["ckm_error"]
    baseline = results["identity_ckm_baseline"]
    assert (
        err < baseline
    ), f"CKM error {err:.4f} not better than identity baseline {baseline:.4f}"


def test_complex_ckm_error_finite(results):
    err = results["complex_best_ckm"]["ckm_error"]
    assert math.isfinite(err) and err > 0


def test_mean_profile_jarlskog_cp_conserving(results):
    """The exact mean-profile complex scan is CP-conserving at this layer."""
    J = results["complex_best_ckm"]["Jarlskog"]
    assert abs(J) < 1e-12


def test_ckm_diagonal_dominant(results):
    """The predicted CKM matrix should be diagonal-dominant."""
    V = np.array(results["complex_best_ckm"]["V_CKM"])
    for i in range(3):
        assert V[i, i] == max(V[i]), f"Row {i} of CKM not diagonal-dominant: {V[i]}"


def test_vud_close(results):
    """V_ud should be close to 1 (>0.85)."""
    V = np.array(results["complex_best_ckm"]["V_CKM"])
    assert V[0, 0] > 0.85, f"|V_ud| = {V[0,0]:.4f}, expected > 0.85"


def test_vtb_close(results):
    """V_tb should be close to 1 (>0.85)."""
    V = np.array(results["complex_best_ckm"]["V_CKM"])
    assert V[2, 2] > 0.85, f"|V_tb| = {V[2,2]:.4f}, expected > 0.85"


def test_vub_suppressed(results):
    """V_ub should be small (<0.10 -- suppressed compared to V_us)."""
    V = np.array(results["complex_best_ckm"]["V_CKM"])
    assert V[0, 2] < 0.10, f"|V_ub| = {V[0,2]:.4f} should be suppressed (<0.10)"


# ---------------------------------------------------------------------------
# PMNS tests
# ---------------------------------------------------------------------------


def test_pmns_error_below_threshold(results):
    """PMNS error should be well below the identity baseline (~1.2)."""
    err = results["complex_best_pmns"]["pmns_error"]
    assert err < 0.20, (
        f"PMNS error {err:.4f} is too large; "
        "W33 should predict large neutrino mixing"
    )


def test_pmns_finite(results):
    err = results["complex_best_pmns"]["pmns_error"]
    assert math.isfinite(err) and err > 0


def test_pmns_large_theta12(results):
    """Solar mixing angle theta_12 should be large: sin^2(theta_12) > 0.2."""
    V = np.array(results["complex_best_pmns"]["V_PMNS"])
    # |V_e2|^2 = sin^2(theta_12) * cos^2(theta_13)
    # Just check V[0,1] > 0.45 (sin(33 deg) = 0.55)
    assert (
        V[0, 1] > 0.45
    ), f"|V_e2| = {V[0,1]:.4f}, expected > 0.45 (large solar mixing)"


def test_pmns_large_theta23(results):
    """Atmospheric mixing angle theta_23 should be large: |V_mu3| > 0.55."""
    V = np.array(results["complex_best_pmns"]["V_PMNS"])
    assert (
        V[1, 2] > 0.55
    ), f"|V_mu3| = {V[1,2]:.4f}, expected > 0.55 (large atmospheric mixing)"


def test_pmns_first_row_structure(results):
    """First row of PMNS should have V_e1 > V_e2 > V_e3 (observed hierarchy)."""
    V = np.array(results["complex_best_pmns"]["V_PMNS"])
    assert (
        V[0, 0] > V[0, 1] > V[0, 2]
    ), f"PMNS first row {V[0]} should satisfy V_e1 > V_e2 > V_e3"


# ---------------------------------------------------------------------------
# Dominant eigenvector profile tests
# ---------------------------------------------------------------------------


def test_dominant_best_ckm_exists(results):
    """dominant_best_ckm key must exist with required sub-keys."""
    assert "dominant_best_ckm" in results, "Missing key: dominant_best_ckm"
    r = results["dominant_best_ckm"]
    for key in ["ckm_error", "Jarlskog", "V_CKM"]:
        assert key in r, f"dominant_best_ckm missing sub-key: {key}"


def test_dominant_best_pmns_exists(results):
    """dominant_best_pmns key must exist with required sub-keys."""
    assert "dominant_best_pmns" in results, "Missing key: dominant_best_pmns"
    r = results["dominant_best_pmns"]
    for key in ["pmns_error", "Jarlskog", "V_PMNS"]:
        assert key in r, f"dominant_best_pmns missing sub-key: {key}"


def test_dominant_ckm_error_small(results):
    """Dominant-profile CKM error should be < 0.10 (well below mean-profile 0.235)."""
    err = results["dominant_best_ckm"]["ckm_error"]
    assert err < 0.10, (
        f"Dominant CKM error {err:.4f} should be < 0.10; "
        "dominant eigenvector profiles should give near-experimental CKM"
    )


def test_dominant_ckm_beats_mean_profile(results):
    """Dominant-profile CKM error must be strictly better than mean-profile error."""
    err_dom = results["dominant_best_ckm"]["ckm_error"]
    err_mean = results["complex_best_ckm"]["ckm_error"]
    assert (
        err_dom < err_mean
    ), f"Dominant CKM error {err_dom:.4f} should beat mean-profile {err_mean:.4f}"


def test_dominant_ckm_vus_accurate(results):
    """V_us (Cabibbo angle) should be in experimental range [0.18, 0.27]."""
    V = np.array(results["dominant_best_ckm"]["V_CKM"])
    Vus = V[0, 1]
    assert (
        0.18 < Vus < 0.27
    ), f"|V_us| = {Vus:.4f}, expected in [0.18, 0.27] (experimental: 0.2243)"


def test_dominant_ckm_vud_close(results):
    """V_ud from dominant profiles should be > 0.93."""
    V = np.array(results["dominant_best_ckm"]["V_CKM"])
    assert V[0, 0] > 0.93, f"|V_ud| = {V[0,0]:.4f}, expected > 0.93"


def test_dominant_ckm_vtb_close(results):
    """V_tb from dominant profiles should be > 0.95."""
    V = np.array(results["dominant_best_ckm"]["V_CKM"])
    assert V[2, 2] > 0.95, f"|V_tb| = {V[2,2]:.4f}, expected > 0.95"


def test_dominant_pmns_error_small(results):
    """Dominant-profile PMNS error remains in the large-mixing window."""
    err = results["dominant_best_pmns"]["pmns_error"]
    assert err < 0.12, (
        f"Dominant PMNS error {err:.4f} should be < 0.12; "
        "dominant profiles should still give viable neutrino mixing"
    )


def test_dominant_pmns_ve3_accurate(results):
    """|V_e3| = sin(theta_13) should be in experimental range [0.10, 0.20]."""
    V = np.array(results["dominant_best_pmns"]["V_PMNS"])
    Ve3 = V[0, 2]
    assert (
        0.10 < Ve3 < 0.20
    ), f"|V_e3| = {Ve3:.4f}, expected in [0.10, 0.20] (experimental: 0.149)"


def test_mean_profile_pmns_beats_dominant_profile(results):
    """Mean-profile PMNS remains the sharper lepton-mixing packet."""
    err_dom = results["dominant_best_pmns"]["pmns_error"]
    err_mean = results["complex_best_pmns"]["pmns_error"]
    assert (
        err_mean < err_dom
    ), f"Mean-profile PMNS error {err_mean:.4f} should beat dominant-profile {err_dom:.4f}"
