#!/usr/bin/env python3
"""Pass 4504 -- explicit minimal natural gauge section after the order-648 no-go.

Pass 4503 corrects the old Pass-4493 claim: neither order-648 point nor line
stabilizer admits an equivariant section.  The canonical incident-flag
stabilizer H, |H|=162, does split the apartment extension.  Its affine family
has dimension six, so there are exactly 64 H-equivariant sections.

This pass enumerates all 64 exactly.  In the canonical quotient coordinates used
by Passes 4488/4493, the lexicographic optimum

    (total minimal ambient Hamming weight,
     maximum column weight,
     union-of-lines support)

is

    (42, 9, 13),

with column weights

    1,1,1,1,5,5,5,5,9,9.

The ambient representatives are minimized modulo J=<all-ones>, because E=M/J.
This is a finite-module gauge compiler, not a physical measurement schedule.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from w33_pass4493_symmetry_breaking_section_threshold import (
    actions_from_line_gens,
    build_geometry,
    build_line_perm,
    line_perm_from_point_perm,
    perm_group,
    point_perm_from_matrix,
    quotient_model,
    rank2,
    small_generating_set,
    transvection_matrix,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json"


def rref_solve(A, b):
    A = np.asarray(A, dtype=np.uint8).copy()
    b = np.asarray(b, dtype=np.uint8).reshape(-1, 1)
    M = np.hstack((A, b))
    m, n = A.shape
    pivots = []
    r = 0
    for c in range(n):
        rows = np.flatnonzero(M[r:, c])
        if not len(rows):
            continue
        rr = r + int(rows[0])
        if rr != r:
            M[[r, rr]] = M[[rr, r]]
        for i in range(m):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        pivots.append(c)
        r += 1
    for i in range(r, m):
        if not M[i, :n].any() and M[i, n]:
            raise ValueError("inconsistent GF(2) system")
    x = np.zeros(n, dtype=np.uint8)
    for i, c in reversed(list(enumerate(pivots))):
        x[c] = int(M[i, n] ^ (np.dot(M[i, :n], x) % 2))
    free = [c for c in range(n) if c not in pivots]
    null = []
    for f in free:
        z = np.zeros(n, dtype=np.uint8)
        z[f] = 1
        for i, c in reversed(list(enumerate(pivots))):
            z[c] = int(np.dot(M[i, :n], z) % 2)
        null.append(z)
    return x, np.asarray(null, dtype=np.uint8)


def section_system(Pi, GE, GV):
    I10 = np.eye(10, dtype=np.uint8)
    I39 = np.eye(39, dtype=np.uint8)
    blocks = [np.kron(I10, Pi).astype(np.uint8)]
    rhs = [I10.reshape(-1, order="F")]
    for e, v in zip(GE, GV):
        blocks.append((np.kron(I10, e) ^ np.kron(v.T, I39)).astype(np.uint8))
        rhs.append(np.zeros(390, dtype=np.uint8))
    return np.vstack(blocks), np.concatenate(rhs)


def main() -> int:
    pts, pidx, lines, lidx, _, Astar, *_ = build_geometry()
    _, Ereps, Vreps, coordE, coordV, Pi = quotient_model(np.asarray(Astar, dtype=np.uint8))

    matrices = [transvection_matrix(v) for v in pts]
    point_trans = [point_perm_from_matrix(M, pts, pidx) for M in matrices]
    line_trans = [build_line_perm(M, pts, pidx, lines, lidx) for M in matrices]
    selected = []
    full_line = {tuple(range(40))}
    for i, lp in enumerate(line_trans):
        trial = perm_group([line_trans[j] for j in selected] + [lp], 40)
        if len(trial) > len(full_line):
            selected.append(i)
            full_line = trial
        if len(full_line) == 25920:
            break
    full_point = perm_group([point_trans[i] for i in selected], 40)
    assert len(full_line) == len(full_point) == 25920

    fp, fl = min((p, li) for li, line in enumerate(lines) for p in line)
    flag_point = {
        g for g in full_point
        if g[fp] == fp and line_perm_from_point_perm(g, lines, lidx)[fl] == fl
    }
    flag = {line_perm_from_point_perm(g, lines, lidx) for g in flag_point}
    assert len(flag) == 162
    gens = small_generating_set(flag, 40)
    GE, GV = actions_from_line_gens(gens, Ereps, Vreps, coordE, coordV)
    A, b = section_system(Pi, GE, GV)
    assert rank2(A) == rank2(np.column_stack((A, b))) == 384

    x0, null = rref_solve(A, b)
    assert len(null) == 6

    J = np.ones(40, dtype=np.uint8)
    Ereps = np.asarray(Ereps, dtype=np.uint8)

    def score(x):
        S = x.reshape((39, 10), order="F")
        assert np.array_equal((Pi @ S) % 2, np.eye(10, dtype=np.uint8))
        for e, v in zip(GE, GV):
            assert np.array_equal((e @ S) % 2, (S @ v) % 2)
        supports = []
        weights = []
        for j in range(10):
            ambient = (S[:, j] @ Ereps) % 2
            alt = ambient ^ J
            if int(alt.sum()) < int(ambient.sum()):
                ambient = alt
            supp = tuple(int(i) for i in np.flatnonzero(ambient))
            supports.append(supp)
            weights.append(len(supp))
        union = sorted(set().union(*(set(s) for s in supports)))
        return (sum(weights), max(weights), len(union)), weights, supports, S

    candidates = []
    for mask in range(1 << 6):
        x = x0.copy()
        for i in range(6):
            if (mask >> i) & 1:
                x ^= null[i]
        sc, weights, supports, S = score(x)
        candidates.append((sc, mask, weights, supports, S))
    candidates.sort(key=lambda z: (z[0], z[1]))
    best = candidates[0]
    sc, mask, weights, supports, S = best
    assert sc == (42, 9, 13), sc
    assert sorted(weights) == [1, 1, 1, 1, 5, 5, 5, 5, 9, 9]

    # Reconfirm the corrected order-648 no-go in the same coordinate model.
    line_stab = {g for g in full_line if g[0] == 0}
    point_stab_point = {g for g in full_point if g[0] == 0}
    point_stab = {line_perm_from_point_perm(g, lines, lidx) for g in point_stab_point}
    no_go = {}
    for name, group, expected in (
        ("line", line_stab, (386, 387)),
        ("point", point_stab, (387, 388)),
    ):
        gg = small_generating_set(group, 40)
        ee, vv = actions_from_line_gens(gg, Ereps, Vreps, coordE, coordV)
        AA, bb = section_system(Pi, ee, vv)
        got = (rank2(AA), rank2(np.column_stack((AA, bb))))
        assert got == expected and got[0] != got[1]
        no_go[name] = {"order": 648, "rank_coefficient": got[0], "rank_augmented": got[1], "split": False}

    out = {
        "pass": 4504,
        "theorem": "order-648 no-go plus exhaustive optimal order-162 flag-equivariant section",
        "flag": {"point": fp, "line": fl, "order": 162, "section_family_dimension": 6, "sections_exhausted": 64},
        "order648_no_go": no_go,
        "optimization_basis": "canonical Pass-4493 quotient coordinates",
        "objective": ["total_minimal_ambient_Hamming_weight", "maximum_column_weight", "union_line_support"],
        "optimum": {"score": list(sc), "affine_mask": mask, "column_weights": weights, "ambient_line_supports": [list(s) for s in supports], "union": sorted(set().union(*(set(s) for s in supports)))},
        "boundary": "The 13-line/weight-42 optimum is coordinate-basis dependent software gauge synthesis in E=M/J. It is not a physical measurement optimum, decoder threshold, or optical layout claim.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
