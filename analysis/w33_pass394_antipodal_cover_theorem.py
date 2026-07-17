#!/usr/bin/env python3
"""Pass 394: prove the W(3,q) bulk antipodal-cover law for every odd field.

Fix p_inf=(0,0,0,1). Every point opposite p_inf has the unique representative
(x,1,y,z). Two such points are collinear exactly when

    z' - z = y*x' - x*y'.

This gives an antipodal q-fold cover of K_{q^2} with intersection array
{q^2-1,q(q-1),1;1,q,q^2-1}. The proof applies to every odd prime power;
the executable checks instantiate q=3,5,7 in prime fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np


def vertices(q: int) -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in range(q) for y in range(q) for z in range(q)]


def build_adjacency(q: int) -> np.ndarray:
    verts = vertices(q)
    index = {v: i for i, v in enumerate(verts)}
    A = np.zeros((q**3, q**3), dtype=np.int8)
    for i, (x, y, z) in enumerate(verts):
        for xp in range(q):
            for yp in range(q):
                if (xp, yp) == (x, y):
                    continue
                zp = (z + y * xp - x * yp) % q
                A[i, index[(xp, yp, zp)]] = 1
    assert np.array_equal(A, A.T)
    return A


def all_distances(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    D = np.full((n, n), -1, dtype=np.int16)
    neighbors = [np.flatnonzero(A[i]).tolist() for i in range(n)]
    for source in range(n):
        D[source, source] = 0
        queue: deque[int] = deque([source])
        while queue:
            u = queue.popleft()
            for v in neighbors[u]:
                if D[source, v] < 0:
                    D[source, v] = D[source, u] + 1
                    queue.append(v)
    return D


def predicted(q: int) -> dict:
    return {
        "vertices": q**3,
        "fibres": q**2,
        "fibre_size": q,
        "degree": q*q - 1,
        "shells": {0: 1, 1: q*q-1, 2: (q*q-1)*(q-1), 3: q-1},
        "intersection": {
            1: (1, q-2, q*(q-1)),
            2: (q, q*q-q-2, 1),
            3: (q*q-1, 0, 0),
        },
        "spectrum": {
            str(q*q-1): 1,
            str(q-1): q*(q*q-1)//2,
            "-1": q*q-1,
            str(-(q+1)): q*(q-1)*(q-1)//2,
        },
    }


def verify_rung(q: int) -> dict:
    A = build_adjacency(q)
    D = all_distances(A)
    expected = predicted(q)
    checks: dict[str, bool] = {
        "vertex_count": A.shape == (q**3, q**3),
        "degree": set(A.sum(axis=1).tolist()) == {q*q-1},
        "diameter_three": int(D.max()) == 3,
        "shells": dict(Counter(int(x) for x in D[0])) == expected["shells"],
    }
    data: dict[int, tuple[int, int, int]] = {}
    neighbors = [np.flatnonzero(A[i]) for i in range(A.shape[0])]
    regular = True
    for source in range(A.shape[0]):
        for target in range(A.shape[0]):
            d = int(D[source, target])
            if d == 0:
                continue
            row = neighbors[target]
            triple = (
                int(np.count_nonzero(D[source, row] == d-1)),
                int(np.count_nonzero(D[source, row] == d)),
                int(np.count_nonzero(D[source, row] == d+1)),
            )
            if d in data and data[d] != triple:
                regular = False
            data.setdefault(d, triple)
    checks["distance_regular"] = regular
    checks["intersection_array"] = data == expected["intersection"]

    verts = vertices(q)
    index = {v: i for i, v in enumerate(verts)}
    fibres = [[index[(x, y, z)] for z in range(q)] for x in range(q) for y in range(q)]
    cover_ok = antipodal_ok = True
    for fibre in fibres:
        fibre_set = set(fibre)
        if np.any(A[np.ix_(fibre, fibre)]):
            cover_ok = False
        for u in fibre:
            if set(np.flatnonzero(D[u] == 3).tolist()) | {u} != fibre_set:
                antipodal_ok = False
        for other in fibres:
            if other is fibre:
                continue
            block = A[np.ix_(fibre, other)]
            if not (np.all(block.sum(0) == 1) and np.all(block.sum(1) == 1)):
                cover_ok = False
    checks["q_fold_cover_of_K_q2"] = cover_ok
    checks["distance_three_classes_are_phase_fibres"] = antipodal_ok
    observed = {str(k): int(v) for k, v in Counter(np.rint(np.linalg.eigvalsh(A)).astype(int)).items()}
    checks["spectrum"] = observed == expected["spectrum"]
    return {"q": q, "verified": all(checks.values()), "checks": checks, "spectrum": observed}


def stable_hash(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_certificate() -> dict:
    rungs = [verify_rung(q) for q in (3, 5, 7)]
    payload = {
        "pass": 394,
        "status": "PASS" if all(r["verified"] for r in rungs) else "FAIL",
        "theorem": "For every odd prime power q, the opposite-point graph of W(3,q) is an antipodal q-fold cover of K_{q^2} with array {q^2-1,q(q-1),1;1,q,q^2-1}; the antipodal classes are the central phase fibres.",
        "coordinate_proof": {
            "chart": "[x:1:y:z]",
            "adjacency": "z'-z=y*x'-x*y'",
            "common_neighbor_equation": "(y-y')r-(x-x')s=z'-z",
            "scope": "all odd prime powers; executable rungs q=3,5,7",
        },
        "rungs": rungs,
    }
    payload["certificate_sha256"] = stable_hash(payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/w33_pass394_antipodal_cover_theorem.json"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 394 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": payload["status"], "rungs": [3,5,7], "certificate_sha256": payload["certificate_sha256"]}))


if __name__ == "__main__":
    main()
