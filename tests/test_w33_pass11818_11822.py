"""Regression tests for Passes 11818-11822 (corrected R rule, Z6-II textures, hidden confinement, SU(9) theorems, Lean)."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11818_11821_su9_flavour_and_corrected_textures as S  # noqa: E402

DATA = ROOT / "data"


def test_su9_theorems():
    r = S.p11821()
    assert r["a"]["per_copy_net_tens"] == 3 and r["a"]["per_copy_net_fivebars"] == 3
    assert r["b"]["cubic_alternating"] and r["b"]["degenerate_pair_and_zero"]
    assert not r["c"]["cubic_84_9bar_9bar_allowed"] and r["c"]["quartic_84_9bar3_allowed"]


def test_certificate():
    c = json.load(open(DATA / "w33_pass11818_11821_su9_flavour_and_corrected_textures.json"))
    p = c["p11818"]
    assert p["no_neutral_pure_monomial"] == 10 and p["down_zero_all_orders_pure"] == 22
    bench = [v for k, v in c["p11819"].items() if "1558" in k][0]
    assert bench["up_zero_degree_entries"] == 1 and bench["down_pure_gauge_only_entries"] > 0
    flag = c["p11820"]["flagship"]
    assert flag[0]["group"] == "su5" and flag[0]["b"] == 8.0 and flag[0]["Lambda_over_Ms"] < 1e-8
    assert abs(c["p11820"]["vev_needed_for_mb_over_mt_1_40_at_degree_12"] - 0.7354) < 1e-3


def test_lean_module():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11822SU9Flavour" in root
    src = (ROOT / "formal" / "W33" / "Pass11822SU9Flavour.lean").read_text(encoding="utf-8")
    for name in ("skew_transpose", "skew_mulVec_self", "skew_det", "skew_mul_transpose", "centre_rule", "family_counts"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
