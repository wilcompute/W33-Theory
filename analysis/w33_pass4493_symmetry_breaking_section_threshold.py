#!/usr/bin/env python3
"""Pass 4493 -- natural geometric symmetry-breaking threshold for apartment sections.

Passes 4488/4490 prove that the exact sequence

    0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0

has no PSp(4,3)-equivariant section.  This pass asks when a section first
appears after restricting to natural geometric stabilizers.

Exact computation gives:

  full PSp(4,3), order 25920:
      rank(A)=389, rank([A|b])=390 -> no section.

  one-line stabilizer, order 648 (index 40):
      rank(A)=rank([A|b])=370 -> sections exist,
      affine section-family dimension 20.

  one-point stabilizer, order 648 (index 40):
      same 370/370 and dimension 20.

  incident point-line flag stabilizer, order 162 (index 160):
      rank 338/338, family dimension 52.

  one apartment setwise stabilizer, order 16 (index 1620):
      rank 308/308, family dimension 82.

Thus, among these tested canonical geometric stabilizers, fixing ONE point or
ONE line is already sufficient to choose an equivariant protected complement.
This is the clean symmetry-breaking boundary:

    full W33 symmetry -> protected sector only as a quotient,
    point/line gauge   -> an equivariant 10D section can be selected.

Boundary: this is NOT a classification of every subgroup of PSp(4,3).  It does
not prove that no larger non-geometric subgroup splits the extension.  Nor is a
linear section automatically a physical decoder or a hardware gauge choice.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry,
    build_line_perm,
    transvection_matrix,
)
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT = Path(__file__).resolve().parents[1]


def rank2(M: np.ndarray) -> int:
    return len(rref_rows(np.asarray(M, dtype=np.uint8)))


def inv2(M: np.ndarray) -> np.ndarray:
    M = np.asarray(M, dtype=np.uint8)
    n = M.shape[0]
    A = np.hstack((M.copy(), np.eye(n, dtype=np.uint8)))
    for c in range(n):
        r = next(i for i in range(c, n) if A[i, c])
        if r != c:
            A[[c, r]] = A[[r, c]]
        for i in range(n):
            if i != c and A[i, c]:
                A[i] ^= A[c]
    return A[:, n:]


def extend(subspace: np.ndarray) -> np.ndarray:
    current = rref_rows(subspace)
    reps = []
    r = len(current)
    for e in np.eye(40, dtype=np.uint8):
        trial = rref_rows(np.vstack((current, e)))
        if len(trial) > r:
            reps.append(e.copy())
            current = trial
            r += 1
        if r == 40:
            break
    return np.asarray(reps, dtype=np.uint8)


def normalize_projective(v) -> tuple[int, ...]:
    w = [int(x) % 3 for x in v]
    for x in w:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in w)
    raise ValueError("zero projective vector")


def point_perm_from_matrix(M: np.ndarray, pts, pidx) -> tuple[int, ...]:
    out = []
    for x in pts:
        y = (M @ np.asarray(x, dtype=int)) % 3
        out.append(pidx[normalize_projective(y)])
    return tuple(out)


def compose(p, q):
    """Permutation product p o q."""
    return tuple(p[q[i]] for i in range(len(p)))


def perm_group(gens, n: int):
    identity = tuple(range(n))
    group = {identity}
    frontier = [identity]
    while frontier:
        g = frontier.pop()
        for h in gens:
            for x in (compose(g, h), compose(h, g)):
                if x not in group:
                    group.add(x)
                    frontier.append(x)
    return group


def small_generating_set(group, n: int):
    identity = tuple(range(n))
    target = len(group)
    gens = []
    current = {identity}
    for g in sorted(group):
        if g in current:
            continue
        trial = perm_group(gens + [g], n)
        if len(trial) > len(current):
            gens.append(g)
            current = trial
        if len(current) == target:
            break
    if len(current) != target:
        raise AssertionError("failed to generate subgroup")
    # Greedy redundancy removal.
    changed = True
    while changed:
        changed = False
        for i in range(len(gens)):
            trial_gens = gens[:i] + gens[i + 1 :]
            if len(perm_group(trial_gens, n)) == target:
                gens = trial_gens
                changed = True
                break
    return gens


def line_perm_from_point_perm(p, lines, lidx):
    return tuple(lidx[frozenset(p[x] for x in L)] for L in lines)


def perm_matrix(p):
    n = len(p)
    P = np.zeros((n, n), dtype=np.uint8)
    for i, j in enumerate(p):
        P[j, i] = 1
    return P


def quotient_model(Astar: np.ndarray):
    J = np.ones((1, 40), dtype=np.uint8)
    K = rref_rows(nullspace_mod2(Astar))
    Ereps = extend(J)
    Vreps = extend(K)
    BE = np.vstack((J, Ereps))
    BV = np.vstack((K, Vreps))
    BEi = inv2(BE)
    BVi = inv2(BV)

    def coordE(v):
        return ((v @ BEi) % 2)[1:]

    def coordV(v):
        return ((v @ BVi) % 2)[30:]

    Pi = np.column_stack([coordV(e) for e in Ereps]).astype(np.uint8)
    return K, Ereps, Vreps, coordE, coordV, Pi


def actions_from_line_gens(line_gens, Ereps, Vreps, coordE, coordV):
    GE, GV = [], []
    for p in line_gens:
        P = perm_matrix(p)
        GE.append(np.column_stack([coordE(P @ e) for e in Ereps]).astype(np.uint8))
        GV.append(np.column_stack([coordV(P @ v) for v in Vreps]).astype(np.uint8))
    return GE, GV


def section_system(Pi, GE, GV):
    I10 = np.eye(10, dtype=np.uint8)
    I39 = np.eye(39, dtype=np.uint8)
    blocks = [np.kron(I10, Pi).astype(np.uint8)]
    rhs = [I10.reshape(-1, order="F")]
    for e, v in zip(GE, GV):
        blocks.append((np.kron(I10, e) ^ np.kron(v.T, I39)).astype(np.uint8))
        rhs.append(np.zeros(390, dtype=np.uint8))
    A = np.vstack(blocks)
    b = np.concatenate(rhs)
    rA = rank2(A)
    rAug = rank2(np.column_stack((A, b)))
    return {
        "rank_coefficient": rA,
        "rank_augmented": rAug,
        "consistent": rA == rAug,
        "affine_dimension": (390 - rA) if rA == rAug else None,
        "equations": int(A.shape[0]),
        "unknowns": 390,
    }


def fixed_dimension(actions, n):
    if not actions:
        return n
    stacked = np.vstack([g ^ np.eye(n, dtype=np.uint8) for g in actions])
    return n - rank2(stacked)


def first_apartment(Astar):
    for C in itertools.combinations(range(40), 4):
        deg = [sum(int(Astar[x, y]) for y in C if y != x) for x in C]
        if deg == [2, 2, 2, 2]:
            return frozenset(C)
    raise AssertionError("no dual quadrangle found")


def main() -> int:
    pts, pidx, lines, lidx, _, Astar, *_ = build_geometry()
    Astar = np.asarray(Astar, dtype=np.uint8)
    K, Ereps, Vreps, coordE, coordV, Pi = quotient_model(Astar)

    matrices = [transvection_matrix(v) for v in pts]
    point_trans = [point_perm_from_matrix(M, pts, pidx) for M in matrices]
    line_trans = [build_line_perm(M, pts, pidx, lines, lidx) for M in matrices]

    # Greedily generate the full PSp action using matched point/line transvections.
    selected = []
    full_line = {tuple(range(40))}
    for i, lp in enumerate(line_trans):
        trial = perm_group([line_trans[j] for j in selected] + [lp], 40)
        if len(trial) > len(full_line):
            selected.append(i)
            full_line = trial
        if len(full_line) == 25920:
            break
    if len(full_line) != 25920:
        raise AssertionError("failed to generate full PSp line action")
    full_point = perm_group([point_trans[i] for i in selected], 40)
    if len(full_point) != 25920:
        raise AssertionError("failed to generate matched PSp point action")

    # For point-defined subgroups convert each point permutation to its line action.
    point_stab_point = {p for p in full_point if p[0] == 0}
    point_stab_line = {line_perm_from_point_perm(p, lines, lidx) for p in point_stab_point}
    line_stab = {g for g in full_line if g[0] == 0}

    # Canonical incident flag using the lexicographically first incident pair.
    flag_pair = min((p, li) for li, L in enumerate(lines) for p in L)
    fp, fl = flag_pair
    flag_point_group = {
        p
        for p in full_point
        if p[fp] == fp and line_perm_from_point_perm(p, lines, lidx)[fl] == fl
    }
    flag_line_group = {line_perm_from_point_perm(p, lines, lidx) for p in flag_point_group}

    apartment = first_apartment(Astar)
    apartment_stab = {
        g for g in full_line if frozenset(g[x] for x in apartment) == apartment
    }

    subgroup_specs = {
        "full_PSp": full_line,
        "one_line_stabilizer": line_stab,
        "one_point_stabilizer": point_stab_line,
        "incident_flag_stabilizer": flag_line_group,
        "apartment_setwise_stabilizer": apartment_stab,
    }

    results = {}
    for name, subgroup in subgroup_specs.items():
        gens = small_generating_set(subgroup, 40)
        GE, GV = actions_from_line_gens(gens, Ereps, Vreps, coordE, coordV)
        sec = section_system(Pi, GE, GV)
        results[name] = {
            "order": len(subgroup),
            "index_in_PSp": 25920 // len(subgroup),
            "generators_used": len(gens),
            "fixed_dim_E39": fixed_dimension(GE, 39),
            "fixed_dim_V10": fixed_dimension(GV, 10),
            "section_system": sec,
        }

    checks = {
        "full_order_25920": results["full_PSp"]["order"] == 25920,
        "full_nonsplit_389_390": (
            results["full_PSp"]["section_system"]["rank_coefficient"] == 389
            and results["full_PSp"]["section_system"]["rank_augmented"] == 390
            and not results["full_PSp"]["section_system"]["consistent"]
        ),
        "line_stabilizer_order648": results["one_line_stabilizer"]["order"] == 648,
        "line_stabilizer_splits_370": (
            results["one_line_stabilizer"]["section_system"]["rank_coefficient"] == 370
            and results["one_line_stabilizer"]["section_system"]["rank_augmented"] == 370
            and results["one_line_stabilizer"]["section_system"]["affine_dimension"] == 20
        ),
        "point_stabilizer_order648": results["one_point_stabilizer"]["order"] == 648,
        "point_stabilizer_splits_370": (
            results["one_point_stabilizer"]["section_system"]["rank_coefficient"] == 370
            and results["one_point_stabilizer"]["section_system"]["rank_augmented"] == 370
            and results["one_point_stabilizer"]["section_system"]["affine_dimension"] == 20
        ),
        "flag_stabilizer_order162": results["incident_flag_stabilizer"]["order"] == 162,
        "flag_stabilizer_splits_338": (
            results["incident_flag_stabilizer"]["section_system"]["rank_coefficient"] == 338
            and results["incident_flag_stabilizer"]["section_system"]["rank_augmented"] == 338
            and results["incident_flag_stabilizer"]["section_system"]["affine_dimension"] == 52
        ),
        "apartment_stabilizer_order16": results["apartment_setwise_stabilizer"]["order"] == 16,
        "apartment_stabilizer_splits_308": (
            results["apartment_setwise_stabilizer"]["section_system"]["rank_coefficient"] == 308
            and results["apartment_setwise_stabilizer"]["section_system"]["rank_augmented"] == 308
            and results["apartment_setwise_stabilizer"]["section_system"]["affine_dimension"] == 82
        ),
        "point_line_are_index40": (
            results["one_line_stabilizer"]["index_in_PSp"] == 40
            and results["one_point_stabilizer"]["index_in_PSp"] == 40
        ),
        "natural_threshold_point_or_line": (
            not results["full_PSp"]["section_system"]["consistent"]
            and results["one_line_stabilizer"]["section_system"]["consistent"]
            and results["one_point_stabilizer"]["section_system"]["consistent"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    out = {
        "pass": 4493,
        "theorem": "W33 natural geometric symmetry-breaking section threshold theorem",
        "sequence": "0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0",
        "tested_subgroups": results,
        "canonical_flag": {"point": fp, "line": fl},
        "canonical_apartment_lines": sorted(apartment),
        "conclusion": (
            "Among the tested canonical geometric stabilizers, full PSp(4,3) is nonsplit, "
            "while fixing one point or one line (order 648, index 40) already permits an "
            "equivariant 10-dimensional section; finer flag/apartment stabilizers admit larger families."
        ),
        "boundary": (
            "This is not a classification of every subgroup of PSp(4,3), and does not prove that no larger "
            "non-geometric subgroup splits the extension.  A linear section is a symmetry-breaking gauge choice, "
            "not automatically a physical decoder or hardware implementation."
        ),
        "checks": {"passed": sum(checks.values()), "total": len(checks)},
    }
    path = ROOT / "data/PART_W33_PASS4493_SYMMETRY_BREAKING_SECTION_THRESHOLD.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
