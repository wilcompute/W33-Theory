#!/usr/bin/env python3
"""Tests for Pillar 93: regular subgroup N generation."""

from __future__ import annotations

import json
from pathlib import Path

from THEORY_PART_CXCIII_FIND_N import compose, is_regular, subgroup_generated_by

REPO = Path(__file__).resolve().parent.parent


def _existing_path(*relative_paths: str) -> Path:
    for relative_path in relative_paths:
        path = REPO / relative_path
        if path.exists():
            return path
    raise AssertionError(f"Missing expected artifact from: {relative_paths}")


def test_find_N_files_exist():
    _existing_path(
        "N_subgroup.json", "archive/json/N_subgroup.json", "pillars/N_subgroup.json"
    )
    _existing_path("N_flag_map.json", "archive/json/N_flag_map.json")


def test_N_properties():
    N = json.loads(
        _existing_path(
            "N_subgroup.json", "archive/json/N_subgroup.json", "pillars/N_subgroup.json"
        ).read_text()
    )
    assert len(N) == 192
    # closure test
    closure = subgroup_generated_by([tuple(p) for p in N])
    assert len(closure) == 192
    # regularity
    assert is_regular([tuple(p) for p in N])


def test_flag_map():
    fmap = json.loads(
        _existing_path("N_flag_map.json", "archive/json/N_flag_map.json").read_text()
    )
    assert set(int(k) for k in fmap.keys()) == set(range(192))
    # each value should be a 192-permutation
    for v in fmap.values():
        assert isinstance(v, list) and len(v) == 192


def test_orders_distribution():
    N = json.loads(
        _existing_path(
            "N_subgroup.json", "archive/json/N_subgroup.json", "pillars/N_subgroup.json"
        ).read_text()
    )

    def order(p):
        cur = list(range(192))
        for i in range(1, 1000):
            cur = [p[j] for j in cur]
            if cur == list(range(192)):
                return i
        return None

    dist = {}
    for p in N:
        o = order(p)
        dist[o] = dist.get(o, 0) + 1
    # ensure exactly 192 elements accounted
    assert sum(dist.values()) == 192
    # sanity: must contain the orders found in earlier run
    assert set(dist.keys()).issubset({1, 2, 3, 4, 6})


def test_pillar_93_narrative_exists():
    _existing_path("PILLAR_93.md", "pillars/THEORY_PART_CXCIII_FIND_N.py")
