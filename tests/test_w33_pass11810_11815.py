"""Regression tests for Passes 11810-11815 (all-order Yukawa textures, fractional-class group, Lean module)."""

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass11810_11813_yukawa_textures as Y  # noqa: E402

DATA = ROOT / "data"


def _flagship_text():
    with gzip.open(DATA / "w33_pass11810_probe_fields.json.gz", "rt") as g:
        models = json.load(g)["models"]
    return [m["text"] for m in models.values() if m["label"] == "SM_20260917_3"][0]


def test_flagship_up_locked_and_down_lepton_zero():
    fields = Y.parse_text(_flagship_text())
    fr = Y.frame(fields)
    q = sorted(n for n in fields if n.startswith("q_"))
    bu = sorted(n for n in fields if n.startswith("bu_"))
    M = Y.matrix(fields, fr, q, bu, fr["pure_singlets"], fr["pure_doublets"])
    assert Y.classify_up(M) == "locked g*epsilon"
    assert set(Y.finite(M)) == {"q_2.bu_3", "q_3.bu_2"}
    bd = sorted(n for n in fields if n.startswith("bd_"))
    D = Y.matrix(fields, fr, q, bd, fr["pure_singlets"], fr["doublets"], use_r=False)
    assert not Y.finite(D)


def test_certificate_summary():
    c = json.load(open(DATA / "w33_pass11810_11813_yukawa_textures.json"))["summary"]
    assert c["models"] == 33
    assert c["up_pure_class_by_variant"]["both"].get("locked g*epsilon") == c["locked_models_without_R_charged_neutral_monomial"] == 10
    assert c["down_lepton_zero_all_orders_pure_gauge_only"] >= 22
    assert min(c["down_composite_min_degree"]) >= 15 and min(c["up_composite_min_split_degree"]) >= 6


def test_lean_module_registered():
    root = (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")
    assert "import W33.Pass11815LevelCharges" in root
    src = (ROOT / "formal" / "W33" / "Pass11815LevelCharges.lean").read_text(encoding="utf-8")
    for name in ("charge_integral_of_colour_neutral", "charge_not_integral_of_colour_charged", "weinberg_level_trace",
                 "nine_level_partitions", "su9_anomaly_balance"):
        assert f"theorem {name}" in src
    assert "sorry" not in src
