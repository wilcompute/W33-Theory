#!/usr/bin/env python3
"""Tests for Pillar 93: regular subgroup N generation."""

from __future__ import annotations

import json
from pathlib import Path

from THEORY_PART_CXCIII_FIND_N import subgroup_generated_by, is_regular, compose


def test_find_N_files_exist():
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "N_subgroup.json").exists()
    assert (repo / "N_flag_map.json").exists()


def test_N_properties():
    repo = Path(__file__).resolve().parent.parent
    N = json.loads((repo / "N_subgroup.json").read_text(encoding="utf-8"))
    assert len(N) == 192
    # closure test
    closure = subgroup_generated_by([tuple(p) for p in N])
    assert len(closure) == 192
    # regularity
    assert is_regular([tuple(p) for p in N])


def test_flag_map():
    repo = Path(__file__).resolve().parent.parent
    fmap = json.loads((repo / "N_flag_map.json").read_text(encoding="utf-8"))
    assert set(int(k) for k in fmap.keys()) == set(range(192))
    # each value should be a 192-permutation
    for v in fmap.values():
        assert isinstance(v, list) and len(v) == 192


def test_orders_distribution():
    repo = Path(__file__).resolve().parent.parent
    N = json.loads((repo / "N_subgroup.json").read_text(encoding="utf-8"))
    def order(p):
        cur = list(range(192))
        for i in range(1,1000):
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
    assert set(dist.keys()).issubset({1,2,3,4,6})


def test_pillar_93_narrative_exists():
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "PILLAR_93.md").exists()
