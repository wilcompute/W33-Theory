"""Regression gate for the three-copy symmetric exhaustion certificate."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))

import w33_pass20260906_three_copy_symmetric_exhaustion as ex  # noqa: E402

_PAYLOAD = None


def payload():
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = ex.verify()
    return _PAYLOAD


def test_certificate_passes_and_matches_frozen_artifact() -> None:
    p = payload()
    assert p["status"] == "PASS"
    assert all(p["checks"].values())
    frozen_path = os.path.join(ROOT, "data", "PART_W33_PASS20260906_THREE_COPY_SYMMETRIC_EXHAUSTION.json")
    with open(frozen_path, encoding="utf-8") as fh:
        frozen = json.load(fh)
    assert frozen["certificate_sha256"] == p["certificate_sha256"]


def test_symmetric_family_sizes_are_exact() -> None:
    groups = ex.enumerate_groups()
    assert len(groups) == 961
    assert sum(2 ** len(b) for b, _ in groups) == 27391


def test_witnesses_exist_and_are_independently_confirmed() -> None:
    p = payload()
    assert p["result"]["total_witnesses_all_rays"] > 0
    for row in p["result"]["per_ray"].values():
        if row["witnesses"]:
            assert row["independently_confirmed_dense"] == min(row["witnesses"], 4)


def test_all_rays_have_trivial_local_pauli_stabiliser() -> None:
    p = payload()
    assert p["local_stabiliser"]["rays_with_only_identity"] == 36
    assert p["local_stabiliser"]["nontrivial_rays"] == {}
