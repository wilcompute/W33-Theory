"""Test BT982 explicit integral E8 basis construction."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest


def e8_cartan():
    G = np.zeros((8, 8), dtype=np.int64)
    edges = [(0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
    for a, b in edges:
        G[a, b] = G[b, a] = -1
    np.fill_diagonal(G, 2)
    return G


def test_bt982_json_exists_and_claims():
    path = Path("data/bt982_explicit_integral_e8_basis.json")
    assert path.exists(), "BT982 output JSON missing"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["theorem"] == "BT982 explicit integral E8 basis"
    assert data["winner_minimizer"] == 2
    assert data["matches_standard_e8_cartan"] is True
    checks = data["checks"]
    assert checks["T2_M_unimodular"] is True
    assert checks["T3_T_unimodular"] is True
    assert checks["T4_final_gram_is_e8_cartan"] is True


def test_bt982_final_gram_is_e8():
    data = json.loads(Path("data/bt982_explicit_integral_e8_basis.json").read_text(encoding="utf-8"))
    G = np.array(data["final_gram_Bt_G_vertex_B"], dtype=np.int64)
    assert np.array_equal(G, e8_cartan())
    det = round(np.linalg.det(G))
    assert abs(det) == 1
    eig = np.linalg.eigvalsh(G.astype(float))
    assert eig.min() > 1e-9
    assert np.all(np.diag(G) % 2 == 0)


def test_bt982_both_gauges_agree():
    bt954 = json.loads(
        Path("data/bt954_metric_selector_among_support60.json").read_text(encoding="utf-8")
    )
    bt956 = json.loads(
        Path("data/bt956_tetracode_metric_selector_matrix.json").read_text(encoding="utf-8")
    )
    bt982 = json.loads(Path("data/bt982_explicit_integral_e8_basis.json").read_text(encoding="utf-8"))
    assert bt954["metric_winner"] == bt956["metric_winner"] == bt982["winner_minimizer"]
