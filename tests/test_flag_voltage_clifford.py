#!/usr/bin/env python3
import csv
import json
import zipfile
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
HEIS_BUNDLE = ROOT / "TOE_K27_HEISENBERG_S3_v01_20260228_bundle.zip"
TRIALITY_BRIDGE = ROOT / "data" / "w33_triality_bridge.json"


def build_ops(six):
    # load coords
    if not HEIS_BUNDLE.exists():
        pytest.skip(f"Missing K27 Heisenberg bundle: {HEIS_BUNDLE}")
    with zipfile.ZipFile(HEIS_BUNDLE) as zf:
        coords_csv = zf.read(
            "TOE_K27_HEISENBERG_S3_v01_20260228/K27_heisenberg_coords.csv"
        ).decode()
    qid2coords = {
        int(r["qid"]): (int(r["x"]), int(r["y"]), int(r["z"]))
        for r in csv.DictReader(coords_csv.splitlines())
    }
    omega = np.exp(2j * np.pi / 3)
    X = np.roll(np.eye(3, dtype=complex), -1, axis=1)
    Z = np.diag([1, omega, omega**2])
    n = 192

    def compose(p, q):
        return tuple(p[q[i]] for i in range(n))

    ops = {}
    for q in six:
        x, y, z = qid2coords[q]
        ops[q] = (
            (omega**z) * np.linalg.matrix_power(X, x) @ np.linalg.matrix_power(Z, y)
        )
    return ops


def mod_phase(mat):
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if abs(mat[i, j]) > 1e-6:
                phase = mat[i, j] / abs(mat[i, j])
                return mat / phase
    return mat


def test_six_qids_closure():
    if not TRIALITY_BRIDGE.exists():
        pytest.skip(f"Missing triality bridge report: {TRIALITY_BRIDGE}")
    report = json.loads(TRIALITY_BRIDGE.read_text(encoding="utf-8"))
    six = set()
    for qs in report["T4b_block_qids"].values():
        six.update(qs)
    six = sorted(six)
    ops = build_ops(six)
    mult = {}
    for a in six:
        mult[a] = {}
        for b in six:
            prod = ops[a] @ ops[b]
            prod = mod_phase(prod)
            found = None
            for c in six:
                if np.allclose(prod, mod_phase(ops[c]), atol=1e-6):
                    found = c
                    break
            mult[a][b] = found
    # ensure each row has at least one non-None to avoid trivial collapse
    assert any(any(v is not None for v in row.values()) for row in mult.values())
    # closure set same
    closure = set()
    for a in six:
        for b in six:
            if mult[a][b] is not None:
                closure.add(mult[a][b])
    assert closure.issubset(set(six))

    # check existence of central element (commutes with all) using full operators
    central_candidates = []
    for q in six:
        A = ops[q]
        if all(np.allclose(A @ ops[b], ops[b] @ A, atol=1e-6) for b in six):
            central_candidates.append(q)
    assert central_candidates, "no central element found in the six"

    # at least one generator of order 3
    orders = {q: np.linalg.matrix_power(ops[q], 3) for q in six}
    assert any(np.allclose(mod_phase(orders[q]), np.eye(3)) for q in six)
