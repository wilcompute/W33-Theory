"""Regression lock for Passes 5667-5674."""

from __future__ import annotations

import collections
import json
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5667_5674_STRATIFIED_BY_CHARACTERISTIC.json"
BT1413 = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"


def rank_p(A, p):
    A = np.array(A, dtype=int) % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] % p), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r][c]), p - 2, p)) % p
        for i in range(m):
            if i != r and A[i][c] % p:
                A[i] = (A[i] - A[i][c] * A[r]) % p
        r += 1
    return r


@pytest.fixture(scope="module")
def M():
    if not BT1413.is_file():
        pytest.skip("bt1413 absent")
    d = json.loads(BT1413.read_text(encoding="utf-8", errors="replace"))
    inc = collections.defaultdict(set)
    for r in d["flag_rows"]:
        inc[r["tomotope_face_label_from_q4_edge_pair"]].add(
            r["tomotope_edge_label_from_q4_face_pair"])
    faces = sorted(inc)
    edges = sorted({e for v in inc.values() for e in v})
    out = np.zeros((16, 12), dtype=int)
    for i, f in enumerate(faces):
        for e in inc[f]:
            out[i][edges.index(e)] = 1
    return out


def test_reye_collapses_only_at_two(M):
    assert int(np.linalg.matrix_rank(M.astype(float))) == 10
    assert rank_p(M, 2) == 8, "the characteristic-2 collapse"
    for p in (3, 5, 7, 13):
        assert rank_p(M, p) == 10, f"no collapse at {p}"


def test_griesmer_equality():
    """[12,4,6] meets the Griesmer bound, so it is length-optimal."""
    assert sum(math.ceil(6 / 2 ** i) for i in range(4)) == 12


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_the_failed_hypothesis_is_recorded():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5671"]
    assert p["result"].startswith("FAILED")
    assert p["distance_8_graph"]["srg"] == [16, 3, 2, 0]
    assert "unexplained" in p["leaves_open"] or "S4 wr S2" in p["leaves_open"]


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_the_retraction_is_recorded():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    rows = {r["object"]: r for r in d["pass_5672"]["table"]}
    assert rows["Csaszar vertex-face"]["excess"] == 0, "artefact, not a connection"
    assert rows["Csaszar vertex-edge"]["excess"] == 0
    assert rows["Q4 face-edge"]["excess"] == 4
    assert rows["Reye 12_4 16_3"]["excess"] == 1
    assert "NOT" in d["pass_5672"]["retraction"]


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_coincidence_eleven_killed():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    p = d["pass_5667_5668"]
    assert p["coincidence_number"] == 11
    assert p["sm_pattern"] == [1, 3, 8]
    assert p["patterns_on_12"] > 1, "1+3+8 must not be the only pattern"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_yosys_reported_absent_not_run():
    d = json.loads(CERT.read_text(encoding="utf-8"))
    assert d["pass_5674"]["yosys_present"] is False
    assert "no synthesis" in d["pass_5674"]["status"]
