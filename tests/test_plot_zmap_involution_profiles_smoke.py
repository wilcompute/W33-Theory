from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


def test_plot_zmap_involution_profiles_smoke(tmp_path: Path) -> None:
    input_json = (
        Path("artifacts/min_cert_census_medium_2026_02_10")
        / "e6_f3_trilinear_reduced_orbit_closed_form_equiv_hessian_exact_full.json"
    )
    if not input_json.exists():
        pytest.skip(f"Missing optional z-map census input {input_json}")

    out = subprocess.run(
        [sys.executable, "tools/plot_zmap_involution_profiles.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    fig_dir = Path("artifacts/min_cert_census_medium_2026_02_10/figures")
    img1 = fig_dir / "zmap_hist_hessian.png"
    img2 = fig_dir / "match_count_hist_hessian.png"
    assert img1.exists(), f"Missing zmap histogram PNG: {img1}"
    assert img2.exists(), f"Missing match count histogram PNG: {img2}"
