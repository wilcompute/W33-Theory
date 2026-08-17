"""Regression lock for Passes 5675-5682."""
from __future__ import annotations

import collections
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS5675_5682_CODE_KNOWS_THE_BLOCK_SYSTEM.json"
BT1413 = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"
PARTITION = [[0, 5, 8, 11], [1, 4, 7, 9], [2, 3, 6, 10]]


def kern2(A):
    A = np.array(A, dtype=int) % 2
    m, n = A.shape
    piv, r = [], 0
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c]), None)
        if p is None:
            continue
        A[[r, p]] = A[[p, r]]
        for i in range(m):
            if i != r and A[i][c]:
                A[i] = (A[i] + A[r]) % 2
        piv.append(c)
        r += 1
    B = []
    for f in [c for c in range(n) if c not in piv]:
        v = np.zeros(n, dtype=int)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = A[i][f] % 2
        B.append(v % 2)
    return np.array(B)


@pytest.fixture(scope="module")
def M():
    if not BT1413.is_file():
        pytest.skip("bt1413 absent")
    d = json.loads(BT1413.read_text(encoding="utf-8", errors="replace"))
    inc = collections.defaultdict(set)
    for r in d["flag_rows"]:
        inc[r["tomotope_face_label_from_q4_edge_pair"]].add(
            r["tomotope_edge_label_from_q4_face_pair"])
    fs = sorted(inc)
    es = sorted({e for v in inc.values() for e in v})
    out = np.zeros((16, 12), dtype=int)
    for i, f in enumerate(fs):
        for e in inc[f]:
            out[i][es.index(e)] = 1
    return out


def test_weight8_complements_are_the_partition(M):
    """The headline, recomputed from the raw certificate."""
    K = kern2(M)
    words = []
    for bits in itertools.product([0, 1], repeat=K.shape[0]):
        v = np.zeros(12, dtype=int)
        for b, row in zip(bits, K):
            if b:
                v = (v + row) % 2
        words.append(v)
    w8 = [w for w in words if w.sum() == 8]
    assert len(w8) == 3
    comps = sorted(sorted(int(i) for i, x in enumerate(w) if x == 0) for w in w8)
    assert comps == sorted(PARTITION), "the unique T12_165 block system"
    flat = sorted(x for c in comps for x in c)
    assert flat == list(range(12)), "a genuine partition"


def test_eight_relations_among_the_sixteen_outputs(M):
    """What yosys did not find."""
    L = kern2(M.T)
    assert L.shape[0] == 8
    assert not (M[[0, 1, 2, 3]].sum(0) % 2).any(), "s0^s1^s2^s3 == 0 identically"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_block_system_is_unique():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5675"]
    assert d["block_representatives"] == 1, "uniqueness is what rules out coincidence"
    assert d["is_the_code_partition"] is True
    assert d["primitive"] is False
    assert d["transitive_id"] == 165


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_yosys_found_none():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5680_5681"]
    assert d["found_relations"] == 0
    assert d["existing_relations"] == 8
    assert d["cells"] == d["naive"], "no reduction at all"


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_csaszar_answer_preserves_the_retraction():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5677_5678"]
    assert "retraction stands" in d["csaszar_answer"]
    assert d["largest"]["excess"] == 9


@pytest.mark.skipif(not CERT.is_file(), reason="certificate not built")
def test_literature_recorded_as_not_found():
    d = json.loads(CERT.read_text(encoding="utf-8"))["pass_5682"]
    assert d["result"] == "NOT FOUND"
    assert "weak evidence" in d["caveat"], "must not be read as novelty"
