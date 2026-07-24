from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _check(script: str) -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "analysis" / script), "--check"],
        cwd=ROOT,
        check=True,
        timeout=1800,
    )


def test_pass801_global_h2_stable_elements() -> None:
    _check("w33_pass801_global_h2_stable_elements.py")


def test_pass802_gluing66_extension_geometry() -> None:
    _check("w33_pass802_gluing66_extension_geometry.py")


def test_pass803_oddq_cut_lattice_companion() -> None:
    _check("w33_pass803_oddq_cut_lattice_companion.py")


def test_pass804_adversarial_calibration_failclosed() -> None:
    _check("w33_pass804_adversarial_calibration_failclosed.py")


def test_pass805_continuous_minplus_circuit() -> None:
    _check("w33_pass805_continuous_minplus_circuit.py")
