"""Regression gate for Pass 11962: the 40-line module versus the Steinberg St_81."""
from __future__ import annotations

import json
import os
import shutil
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

import w33_pass11962_line_module_steinberg_hom as mod  # noqa: E402

HAVE_GAP = bool(shutil.which("gap") or shutil.which("wsl.exe"))
_CACHE: dict = {}


def payload() -> dict:
    if "p" not in _CACHE:
        _CACHE["p"] = mod.verify()
    return _CACHE["p"]


def test_independent_python_spectrum_is_1_24_15() -> None:
    spec = mod.independent_spectrum_check()
    assert spec["line_graph_valency"] == 12
    assert spec["spectrum"] == {-4: 15, 2: 24, 12: 1}


@pytest.mark.skipif(not HAVE_GAP, reason="GAP is required to replay the character computation")
def test_certificate_passes_and_matches_frozen_artifact() -> None:
    p = payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())
    with open(os.path.join(ROOT, "data", "w33_pass11962_line_module_steinberg_hom.json"), encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["semantic_sha256"] == p["semantic_sha256"]


@pytest.mark.skipif(not HAVE_GAP, reason="GAP is required to replay the character computation")
def test_headline_counts() -> None:
    r = payload()["results"]
    assert r["HOM_FULL"] == "0"
    assert r["HOM_SYLOW3"] == "40"
    assert r["N_CLASSES"] == "116"
    assert r["N_HOM_NONZERO"] == "115"
    assert r["N_EMBED"] == "36"
    assert r["MAX_ORDER_EMBED"] == "24"
    assert r["MIN_ORDER_NOEMBED"] == "8"
    assert r["N_NOEMBED_EXPLAINED_BY_ORBITS"] == "79"


def test_frozen_certificate_records_the_scope_boundary() -> None:
    with open(os.path.join(ROOT, "data", "w33_pass11962_line_module_steinberg_hom.json"), encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert "non-equivariant storage" in frozen["boundary"]
    assert frozen["status"] == "PASS"
