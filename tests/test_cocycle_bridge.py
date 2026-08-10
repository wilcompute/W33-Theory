#!/usr/bin/env python3
"""Tests for the cocycle‑Heisenberg‑tomotope bridge bundle.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

repo = Path(__file__).resolve().parent.parent

L_CSV = repo / "K54_node_labels_L.csv"
EDGES_CSV = repo / "K54_edges_L_reconstruct.csv"
STAB_JSON = repo / "K27_stabilizer_C6.json"
T4_JSON = repo / "tomo_t4_cycle_structure.json"


@pytest.fixture(scope="module")
def load_data():
    assert L_CSV.exists() and EDGES_CSV.exists(), (
        "Run THEORY_PART_COCYCLE_HEISENBERG_TOMOTOPE_BRIDGE.py first."
    )
    L = []
    with open(L_CSV) as f:
        for r in csv.DictReader(f):
            L.append(int(r["L"]))
    edges = []
    with open(EDGES_CSV) as f:
        for r in csv.DictReader(f):
            r["u"] = int(r["u"])
            r["v"] = int(r["v"])
            r["cocycle_Z3_exp"] = int(r["cocycle_Z3_exp"])
            r["L_u"] = int(r["L_u"])
            r["L_v"] = int(r["L_v"])
            r["s_g"] = int(r["s_g"])
            r["predicted"] = int(r["predicted"])
            r["ok"] = int(r["ok"])
            edges.append(r)
    stab = json.loads(STAB_JSON.read_text(encoding="utf-8")) if STAB_JSON.exists() else {}
    t4 = json.loads(T4_JSON.read_text(encoding="utf-8")) if T4_JSON.exists() else {}
    return L, edges, stab, t4


def test_edge_reconstruction(load_data):
    _, edges, _, _ = load_data
    assert len(edges) == 270
    assert all(e["ok"] == 1 for e in edges)


def test_twin_phase_same(load_data):
    L, edges, _, _ = load_data
    # compute count by reading twin map
    twin_rows = []
    with open(repo / "pillar77_data" / "K54_to_K27_twin_map.csv") as f:
        for r in csv.DictReader(f):
            twin_rows.append(r)
    by_q = {}
    for r in twin_rows:
        q = int(r["qid"])
        pid = int(r["pocket_id"])
        by_q.setdefault(q, []).append(pid)
    same = sum(1 for pl in by_q.values() if L[pl[0]] == L[pl[1]])
    assert same == 9, "unexpected number of qids with equal phase twins"


def test_stabilizer_json(load_data):
    _, _, stab, _ = load_data
    assert stab, "stabilizer_C6.json missing"
    assert stab.get("size") == 6
    # ensure cycle distribution matches known values
    od = stab.get("order_distribution", {})
    assert od.get("1") == 1
    assert od.get("2") == 1
    assert od.get("3") == 2
    assert od.get("6") == 2


def test_t4_cycle_structure(load_data):
    _, _, _, t4 = load_data
    cs = t4.get("cycle_structure", {})
    assert cs.get("1") == 96
    assert cs.get("3") == 32
