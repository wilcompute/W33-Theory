from pathlib import Path

import pytest

from src.finite_geometry.veldmap import summarize_veldkamp


def test_veldkamp_summary_exists_and_sane():
    base = Path("bundles") / "v23_toe_finish" / "v23"
    csv = base / "Q_triangles_with_centers_Z2_S3_fiber6.csv"
    if not csv.exists():
        pytest.skip(f"v23 CSV not generated yet: {csv}")
    s = summarize_veldkamp(csv)
    # basic structural checks
    assert s["n_points"] >= 40 and s["n_points"] <= 60  # expect ~45
    assert s["n_triangles"] > 1000
    assert s["n_generators"] >= s["n_points"]
    # GF(2) invariants present and consistent
    assert "gf2_rank" in s and s["gf2_rank"] > 0
    assert s["expected_n_veldkamp"] == (1 << s["gf2_rank"])  # 2^rank
    assert s["n_veldkamp"] == s["expected_n_veldkamp"]
    assert isinstance(s["veldkamp_enumerated"], bool)
    # veldkamp reasonably large (not trivial)
    assert s["n_veldkamp"] > s["n_generators"]
    # generator sizes (neighborhoods) should be >1
    assert max(s["generator_size_hist"].keys()) > 1
    # degree histogram non-empty
    assert len(s["degree_hist"]) > 0
