"""Regression checks for the corrected MCLII spectral-action script."""

import subprocess
import sys


def test_mclii_spectral_action_script_runs_with_corrected_spectrum():
    result = subprocess.run(
        [sys.executable, "analysis/w33_spectral_action_moduli_integral.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "lambda = ±sqrt(5/6): mult 48 each" in result.stdout
    assert "lambda = ±sqrt(4/3): mult 30 each" in result.stdout
    assert "Total Dirac modes = 4v - 2 = 158" in result.stdout
    assert "Boundary: the exact finite coefficient scaffold" in result.stdout
