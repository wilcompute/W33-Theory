"""Regression gate for Pass 11963: the Weber law at neutrino-sized epsilon."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

import w33_pass11963_weber_law_at_neutrino_epsilon as mod  # noqa: E402

_CACHE: dict = {}


def payload() -> dict:
    if "p" not in _CACHE:
        _CACHE["p"] = mod.verify()
    return _CACHE["p"]


def test_certificate_passes_and_matches_frozen_artifact() -> None:
    p = payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())
    with open(os.path.join(ROOT, "data", "w33_pass11963_weber_law_at_neutrino_epsilon.json"), encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["semantic_sha256"] == p["semantic_sha256"]


def test_independent_law_is_exact_only_at_small_epsilon() -> None:
    p = payload()
    assert p["independent_law_check"]["max_rel_err_at_eps_1e-4"] < 1e-5
    lo, hi = p["bands_fixed_R_MZ"]["ratio"]
    assert lo < 0.5 < 0.58 < hi


def test_headline_scale_survives_but_phase_is_free() -> None:
    p = payload()
    m1 = p["bands_fixed_R_MZ"]["m1_meV"]
    assert 0.6 < m1[0] and m1[1] < 1.1
    assert p["phase_spread_of_m1_at_fixed_tau"] > 1.2
    s = p["bands_fixed_R_MZ"]["sigma_meV"]
    assert 59.0 < s[0] and s[1] < 60.5


def test_level_curve_is_absent_near_re_tau_zero() -> None:
    p = payload()
    assert all(v > mod.R_MZ for v in p["weber_ratio_minimum_over_im_tau"].values())
