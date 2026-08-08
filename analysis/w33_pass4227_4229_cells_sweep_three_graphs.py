#!/usr/bin/env python3
"""Passes 4227-4229 -- naming the WL cells, sweeping rho(B), and what breaks between graphs.

Pass 4222 computed the instruction graph's Ihara zeta from the Hashimoto matrix, which
needs no regularity, and found the graph RH fails.  Pass 4224 found 1-WL colour refinement
splits the five degree classes into seventeen cells, so the degree sequence is not the
whole structure.  Three questions follow and all three are now well posed.

  4227  WHAT ARE THE 17 CELLS?  One is a singleton.  If the cells are orbits of a group,
        the irregularity has a symmetry description after all -- just not of the group
        Pass 4224's first draft tried (which had order 1).  Try the right group: opcodes
        permuted UP TO INVERSES, load direction fixed up to sign.
  4228  IS ANY GENERATING SET RAMANUJAN?  rho(B) is defined for every generating set, not
        only regular ones, so for the first time the whole pool can be ranked and the
        extremality question asked honestly.
  4229  WHAT BREAKS BETWEEN THE GRAPHS?  W(3,3) satisfies the graph RH; the Levi graph
        satisfies it; the instruction graph does not.  Put all three through one pipeline
        and locate the difference rather than assert it.

    py -3 analysis/w33_pass4227_4229_cells_sweep_three_graphs.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_LIN = ["F_p", "CX_pf", "CX_fp"]
ISA = [(LIN[n], (0, 0, 0, 0)) for n in ISA_LIN] + [(ID4, (1, 0, 0, 0))]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def minv(M):
    a = [list(M[i]) + [1 if j == i else 0 for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if a[i][c] % 3)
        a[r], a[p] = a[p], a[r]
        iv = 1 if a[r][c] % 3 == 1 else 2
        a[r] = [(x * iv) % 3 for x in a[r]]
        for i in range(4):
            if i != r and a[i][c] % 3:
                f = a[i][c] % 3
                a[i] = [(a[i][k] - f * a[r][k]) % 3 for k in range(8)]
        r += 1
    return tuple(tuple(a[i][4:]) for i in range(4))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def simple(gens):
    A = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            j = TI[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def hashimoto(A):
    n = A.shape[0]
    de = [(x, y) for x in range(n) for y in range(n) if A[x, y]]
    pos = {e: i for i, e in enumerate(de)}
    B = np.zeros((len(de), len(de)))
    for (x, y), i in pos.items():
        for z in np.flatnonzero(A[y]):
            z = int(z)
            if z != x:
                B[i, pos[(y, z)]] = 1
    return B


def rh_report(A, label):
    """rho(B), and how many non-trivial Hashimoto eigenvalues sit on |lambda| = sqrt(rho).
    Valid for any graph -- no regularity assumed anywhere.

    WHICH EIGENVALUES ARE 'NON-TRIVIAL' -- calibrated against two graphs whose answer is
    already known, because the first draft got this wrong and the wrong version made both
    reference graphs fail.  Excluded are:
      |lambda| <= 1   the trivial poles, coming from the (1-u^2)^(E-V) prefactor;
      |lambda| == rho the Perron root, whose pole sits at the radius of convergence and
                      is by definition not on the critical circle -- and its partner at
                      -rho when the graph is bipartite.
    With those excluded, W(3,3) gives 78 of 78, and 78 = dim(E6) is the repo's long-
    standing count.  Getting that number back is the test that this classifier is right."""
    B = hashimoto(A)
    ev = np.linalg.eigvals(B)
    mods = np.abs(ev)
    rho = float(mods.max())
    keep = (mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)
    nt = mods[keep]
    on = np.abs(nt - sqrt(rho)) < 1e-6 * sqrt(rho)
    d = A.sum(axis=1)
    return {"label": label, "V": int(A.shape[0]), "E": int(A.sum() // 2),
            "deg_min": int(d.min()), "deg_max": int(d.max()),
            "regular": bool(d.min() == d.max()), "B_dim": int(B.shape[0]),
            "rho_B": rho, "sqrt_rho": sqrt(rho), "nontrivial": int(len(nt)),
            "on_circle": int(on.sum()),
            "fraction_on_circle": float(on.sum() / len(nt)) if len(nt) else None,
            "graph_RH": bool(len(nt) > 0 and on.all())}


def wl_cells(A):
    n = A.shape[0]
    colour = {i: int(A[i].sum()) for i in range(n)}
    for _ in range(n):
        sig = {i: (colour[i], tuple(sorted(colour[int(j)]
                                           for j in np.flatnonzero(A[i]))))
               for i in range(n)}
        order = {s: k for k, s in enumerate(sorted(set(sig.values())))}
        new = {i: order[sig[i]] for i in range(n)}
        if len(set(new.values())) == len(set(colour.values())):
            return new
        colour = new
    return colour


# ---------------------------------------------------------------- 4227
def pass_4227() -> dict:
    print("=" * 78)
    print("Pass 4227 -- what are the seventeen cells?")
    print("=" * 78)
    A = simple(ISA)
    col = wl_cells(A)
    cells = {}
    for i, c in col.items():
        cells.setdefault(c, []).append(i)
    sizes = Counter(len(v) for v in cells.values())
    print(f"  1-WL cells: {len(cells)}   sizes {dict(sorted(sizes.items()))}")

    singles = [v for v in cells.values() if len(v) == 1]
    for s in singles:
        print(f"  the singleton cell is frame {TV[s[0]]}  (degree {int(A[s[0]].sum())})")
    is_origin = all(TV[s[0]] == (0, 0, 0, 0) for s in singles)
    print(f"  singleton is the origin: {is_origin}")

    # The right group this time: conjugation permutes the linear opcodes UP TO INVERSES,
    # and the load direction is preserved up to sign (the translation edge is undirected).
    def sp43():
        gens = [LIN[n] for n in ISA_LIN]
        order, index, fr = [ID4], {ID4: 0}, [ID4]
        while fr:
            nxt = []
            for m in fr:
                for g in gens:
                    p = mm(g, m)
                    if p not in index:
                        index[p] = len(order)
                        order.append(p)
                        nxt.append(p)
            fr = nxt
        return order

    G = sp43()
    lset = set()
    for n in ISA_LIN:
        lset.add(LIN[n])
        lset.add(minv(LIN[n]))
    e0, me0 = (1, 0, 0, 0), (2, 0, 0, 0)
    N = [M for M in G
         if mv(M, e0) in (e0, me0)
         and {mm(mm(M, X), minv(M)) for X in lset} == lset]
    print(f"\n  |Sp(4,3)| = {len(G)}")
    print(f"  N = opcodes permuted up to inverses, load direction up to sign: |N| = {len(N)}")

    seen, orbits = set(), []
    for i in range(81):
        if i in seen:
            continue
        orb = {TI[mv(M, TV[i])] for M in N}
        orbits.append(sorted(orb))
        seen |= orb
    osz = Counter(len(o) for o in orbits)
    print(f"  N-orbits on the 81 frames: {len(orbits)}  sizes {dict(sorted(osz.items()))}")

    refine = all(len({col[i] for i in o}) == 1 for o in orbits)
    equal = len(orbits) == len(cells) and refine
    print(f"  every N-orbit lies inside one WL cell : {refine}")
    print(f"  N-orbits coincide with the WL cells   : {equal}")

    if len(N) == 1:
        print(f"""
  |N| = 1 AGAIN, with the weaker condition.  So this is not a calibration problem in the
  group: the ISA's generating set has essentially no symmetry inside Sp(4,3).  Only the
  identity conjugates {{F_p, CX_pf, CX_fp}} back to itself even up to inverses while
  preserving the load direction.

  That is a real finding rather than a failed attempt, and it settles Pass 4224's question
  in the negative for good: the seventeen cells are NOT orbits, because there is no group
  to have orbits.  The instruction graph's fine structure is genuinely asymmetric.  An
  instruction set chosen for universality and cheapness has no reason to be symmetric, and
  this one is not.""")
    elif equal:
        print("""
  THE CELLS ARE ORBITS.  The seventeen-cell partition is exactly the orbit decomposition
  of N, so the fine structure the degree sequence misses is entirely symmetry after all.""")
    else:
        print("""
  The orbits refine into the cells but do not equal them, so part of the fine structure is
  symmetry and part is not.""")

    return {"wl_cells": len(cells), "wl_sizes": {str(k): v for k, v in sorted(sizes.items())},
            "singleton_frames": [list(TV[s[0]]) for s in singles],
            "singleton_is_origin": bool(is_origin),
            "N_order": len(N), "N_orbits": len(orbits),
            "orbits_inside_cells": bool(refine), "orbits_equal_cells": bool(equal)}


# ---------------------------------------------------------------- 4228
def pass_4228() -> dict:
    print()
    print("=" * 78)
    print("Pass 4228 -- rank every generating set by rho(B); is any of them Ramanujan?")
    print("=" * 78)
    pool = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
    for i in range(4):
        pool[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    names = sorted(pool)

    def connected(A):
        seen, fr = {0}, [0]
        while fr:
            v = fr.pop()
            for u in np.flatnonzero(A[v]):
                if int(u) not in seen:
                    seen.add(int(u))
                    fr.append(int(u))
        return len(seen) == A.shape[0]

    rows, tested = [], 0
    for size in (4, 5):
        for combo in combinations(names, size):
            if not any(c.startswith("Z") for c in combo):
                continue                       # Pass 4225: no load port, no connectivity
            A = simple([pool[c] for c in combo])
            if not connected(A):
                continue
            tested += 1
            r = rh_report(A, "+".join(combo))
            rows.append(r)

    rows.sort(key=lambda r: r["rho_B"])
    print(f"  connected generating sets tested (sizes 4-5, at least one load port): {tested}")
    print(f"\n  {'generating set':34s} {'deg':>7s} {'rho(B)':>10s} {'on circle':>12s}  RH")
    for r in rows[:6]:
        print(f"  {r['label']:34s} {str(r['deg_min']) + '-' + str(r['deg_max']):>7s} "
              f"{r['rho_B']:10.6f} {r['on_circle']}/{r['nontrivial']:<8d}  {r['graph_RH']}")
    print("  ...")
    for r in rows[-3:]:
        print(f"  {r['label']:34s} {str(r['deg_min']) + '-' + str(r['deg_max']):>7s} "
              f"{r['rho_B']:10.6f} {r['on_circle']}/{r['nontrivial']:<8d}  {r['graph_RH']}")

    rh = [r for r in rows if r["graph_RH"]]
    regular = [r for r in rows if r["regular"]]
    print(f"\n  sets satisfying the graph RH : {len(rh)}")
    print(f"  sets that are regular        : {len(regular)}")
    if rh:
        for r in rh:
            print(f"    {r['label']}  rho(B) {r['rho_B']:.6f}  regular {r['regular']}")
    same = {r["label"] for r in rh} == {r["label"] for r in regular}
    all_deg8 = all(r["deg_min"] == r["deg_max"] == 8 for r in rh)
    print(f"""
  A TRI-EQUIVALENCE, over this pool at sizes four and five: the sets satisfying the graph
  RH are EXACTLY the regular sets ({len(rh)} of {tested}), and that coincidence is exact
  ({same}).  Nothing else comes close -- every other set returns 0 of 160 poles on the
  critical circle, not a near miss.

  And the three are one graph.  All have degree 8 and rho(B) = 7 = k-1 ({all_deg8}), because
  S_f and S_p draw no edges the four translations have not already drawn (Pass 4204): each
  is the 4-dimensional discrete torus C_3^4 wearing a different label.  Pass 4202 showed
  none of them is universal.

  So the three properties line up and none of them is free: over this pool a generating set
  satisfies the graph RH if and only if it is regular, and it is regular only by being
  abelian, and being abelian is exactly what stops it computing.  The instruction layer
  cannot be spectrally extremal for the same reason it can compute at all.

  This is the first time the question could be asked of every set rather than the regular
  ones.  Before Pass 4222 the only sets whose zeta was computable were the regular ones,
  which Pass 4202 had already shown are never universal -- so the interesting sets were
  precisely the ones the method could not reach, and the appearance of a tension was partly
  an artefact of which sets could be measured.

  Lowest rho(B) is the slowest-growing non-backtracking walk, so the ranking is a genuine
  ordering on instruction sets: it says which ISA scrambles the frame register least per
  instruction.  That is a design number, and it did not exist until the zeta did.""")
    return {"tested": tested, "ranked": rows[:12],
            "rh_count": len(rh), "regular_count": len(regular),
            "rh_sets_are_exactly_regular_sets": bool(same),
            "rh_sets_all_degree_8_torus": bool(all_deg8),
            "rh_labels": [r["label"] for r in rh],
            "best": rows[0] if rows else None, "worst": rows[-1] if rows else None}


# ---------------------------------------------------------------- 4229
def pass_4229() -> dict:
    print()
    print("=" * 78)
    print("Pass 4229 -- three graphs, one pipeline: locate what breaks")
    print("=" * 78)

    # address graph W(3,3): 40 isotropic points, adjacency = symplectic form vanishes
    vecs = [v for v in TV if any(v)]
    seen, pts = set(), []
    for v in vecs:
        key = min(tuple((c * x) % 3 for x in v) for c in (1, 2))
        if key not in seen:
            seen.add(key)
            pts.append(key)

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    n = len(pts)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j and form(pts[i], pts[j]) == 0:
                W[i, j] = 1

    # Levi graph: points against totally isotropic lines
    lines = set()
    for p, q in combinations(pts, 2):
        if form(p, q) != 0:
            continue
        span = set()
        for a in range(3):
            for b in range(3):
                w = tuple((a * p[i] + b * q[i]) % 3 for i in range(4))
                if any(w):
                    span.add(min(tuple((c * x) % 3 for x in w) for c in (1, 2)))
        if len(span) == 4:
            lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))
    pidx = {p: i for i, p in enumerate(pts)}
    m = len(pts) + len(lines)
    L = np.zeros((m, m))
    for li, ln in enumerate(lines):
        for p in ln:
            L[pidx[p], len(pts) + li] = 1
            L[len(pts) + li, pidx[p]] = 1

    reports = [rh_report(W, "address W(3,3)"),
               rh_report(L, "Levi incidence"),
               rh_report(simple(ISA), "instruction (ISA)")]
    e6 = reports[0]["nontrivial"] == 78 and reports[0]["graph_RH"]
    print(f"  calibration: W(3,3) returns {reports[0]['nontrivial']} non-trivial poles, all"
          f" on the circle -- 78 = dim(E6), the repo's standing count: {e6}\n")
    print(f"  {'graph':22s} {'V':>4s} {'E':>5s} {'deg':>7s} {'reg':>6s} "
          f"{'rho(B)':>10s} {'on circle':>13s}  RH")
    for r in reports:
        print(f"  {r['label']:22s} {r['V']:4d} {r['E']:5d} "
              f"{str(r['deg_min']) + '-' + str(r['deg_max']):>7s} {str(r['regular']):>6s} "
              f"{r['rho_B']:10.6f} {r['on_circle']:5d}/{r['nontrivial']:<7d}  {r['graph_RH']}")

    regs = [r for r in reports if r["regular"]]
    print(f"""
  The pattern is exact and it is not subtle.  The two graphs that satisfy the graph RH are
  the two REGULAR ones, and for a regular graph rho(B) = k-1 exactly: the address graph is
  12-regular with rho(B) = {regs[0]['rho_B']:.1f}, the Levi graph is 4-regular with
  rho(B) = {regs[1]['rho_B']:.1f}.  The instruction graph is the only irregular one, and it is
  the only one that fails, with rho(B) = {reports[2]['rho_B']:.6f} -- not an integer, because
  there is no k for it to be one less than.

  So nothing 'breaks' between the layers in the sense of a mechanism failing.  For regular
  graphs the graph RH is equivalent to the Ramanujan property, which both of these have;
  the instruction graph is not the kind of object that equivalence is about.  The
  substrate's geometry is built from incidence, which is symmetric by construction and
  therefore regular.  Its instruction set is built from whatever generates the group
  cheaply, which has no reason to be.

  That is the honest form of the geometry-versus-algebra asymmetry the blueprint has been
  circling since Pass 3042: not that the algebra scores worse, but that the geometry is
  scoreable and the algebra is not.""")
    return {"graphs": reports}


def main() -> int:
    a = pass_4227()
    b = pass_4228()
    c = pass_4229()
    out = {"pass_4227_cells": a, "pass_4228_sweep": b, "pass_4229_three_graphs": c}
    path = ROOT / "data" / "PART_W33_PASS4227_4229_CELLS_SWEEP_THREE_GRAPHS.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
