#!/usr/bin/env python3
"""Pass 4203 -- generators outside the pool, and whether the law is general.

Pass 4202 exhausted the ten natural generators at sizes 4-8: no regular presentation
generates ASp(4,3).  Two questions immediately follow and both are cheap.

(a) A GENERATOR OUTSIDE THE POOL.  The parallel track's Pass 3005 routes addresses with
    rank-one symplectic TRANSVECTIONS, which are not in this project's opcode pool at all.
    Forty of them exist.  If some transvection set is regular and universal, Pass 4202's
    conclusion is scoped to the pool rather than to the machine.

(b) IS THE LAW GENERAL?  "Non-abelian forces irregular" would stop being about W(3,3) and
    become a statement about instruction sets.  It is easy to refute if false: any small
    non-abelian group with a regular Cayley graph on a transitive action does it.

    py -3 analysis/w33_pass4203_transvections_and_the_general_law.py
"""

from __future__ import annotations

import json
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
FULL = 81 * 51840


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def transvections():
    """T_a(x) = x + <x, a> a, one per projective point: forty rank-one symplectic maps."""
    seen, out = set(), []
    for a in TV:
        if a == (0, 0, 0, 0):
            continue
        key = min(tuple((c * x) % 3 for x in a) for c in (1, 2))
        if key in seen:
            continue
        seen.add(key)
        rows = []
        for i in range(4):
            e = tuple(1 if j == i else 0 for j in range(4))
            s = sum(e[p] * J[p][q] * a[q] for p in range(4) for q in range(4)) % 3
            rows.append(tuple((e[j] + s * a[j]) % 3 for j in range(4)))
        M = tuple(tuple(rows[j][i] for j in range(4)) for i in range(4))
        out.append((key, M))
    return out


def graph(gens):
    A = np.zeros((81, 81))
    for M, t in gens:
        for i, x in enumerate(TV):
            j = TI[tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def connected(A):
    seen, fr = {0}, [0]
    while fr:
        v = fr.pop()
        for u in np.flatnonzero(A[v]):
            if int(u) not in seen:
                seen.add(int(u))
                fr.append(int(u))
    return len(seen) == A.shape[0]


def order(gens, cap=FULL):
    idt = (ID4, (0, 0, 0, 0))
    seen, fr = {idt}, [idt]
    while fr:
        nxt = []
        for M, t in fr:
            for A, a in gens:
                P = (mm(A, M), tuple((mv(A, t)[i] + a[i]) % 3 for i in range(4)))
                if P not in seen:
                    seen.add(P)
                    nxt.append(P)
                    if len(seen) > cap:
                        return len(seen)
        fr = nxt
    return len(seen)


def main() -> int:
    print("=" * 78)
    print("Pass 4203(a) -- transvections: a generator family outside the pool")
    print("=" * 78)
    T = transvections()
    print(f"  rank-one symplectic transvections: {len(T)}")
    RNG = np.random.default_rng(4203)
    trans = [(ID4, tuple(1 if j == i else 0 for j in range(4))) for i in range(4)]

    best = None
    tested = 0
    # transvection subsets alone, and transvections plus translations
    for size in (2, 3, 4):
        for _ in range(400):
            pick = RNG.choice(len(T), size=size, replace=False)
            gens = [(T[int(i)][1], (0, 0, 0, 0)) for i in pick]
            for extra, label in ((gens, "T only"), (gens + trans, "T + translations")):
                tested += 1
                A = graph(extra)
                d = A.sum(axis=1)
                if int(d.min()) != int(d.max()) or not connected(A):
                    continue
                o = order(extra)
                k = int(d[0])
                ev = np.linalg.eigvalsh(A)
                lam2 = max(abs(l) for l in ev if abs(abs(l) - k) > 1e-9)
                ram = 2 * sqrt(k - 1)
                rec = {"label": label, "size": size, "degree": k, "order": o,
                       "universal": o >= FULL, "lambda2": float(lam2),
                       "ramanujan": bool(lam2 <= ram + 1e-9)}
                if best is None or (rec["universal"] and not best["universal"]):
                    best = rec
                if rec["universal"]:
                    break
            if best and best.get("universal"):
                break
        if best and best.get("universal"):
            break

    print(f"  candidate sets tested: {tested}")
    if best and best["universal"]:
        print(f"  REGULAR AND UNIVERSAL FOUND: {best}")
        print("""
  Pass 4202's conclusion is SCOPED TO ITS POOL, not to the machine.  A generator family the
  project does not use gives a regular universal presentation, so the Ramanujan question is
  well posed after all -- just not for the opcodes actually implemented.""")
    elif best:
        print(f"  best regular set found: {best} (not universal)")
        print("""
  No regular AND universal set among the sampled transvection families either.  That is a
  second, structurally different generator pool giving the same answer, which strengthens
  Pass 4202 without proving it.""")
    else:
        print("""
  No regular connected set found among the sampled transvection families at all.  The
  transvections collide even more than the opcodes do, which is consistent with Pass
  4202 and adds nothing beyond it.""")

    print()
    print("=" * 78)
    print("Pass 4203(b) -- is 'non-abelian forces irregular' a general law?")
    print("=" * 78)
    print("""  Refuting it needs one non-abelian group with a regular Cayley graph.  S_3 acting on
  itself by left multiplication, generated by a transposition and a 3-cycle:""")
    # S_3 as permutations of (0,1,2)
    import itertools as it
    els = list(it.permutations(range(3)))
    idx = {e: i for i, e in enumerate(els)}

    def comp(p, q):
        return tuple(p[q[i]] for i in range(3))

    gens3 = [(1, 0, 2), (1, 2, 0)]                       # a transposition and a 3-cycle
    A = np.zeros((6, 6))
    for g in gens3:
        for e in els:
            A[idx[e], idx[comp(g, e)]] = 1
            A[idx[comp(g, e)], idx[e]] = 1
    np.fill_diagonal(A, 0)
    d = A.sum(axis=1)
    reg = int(d.min()) == int(d.max())
    print(f"  S_3 Cayley graph degrees: {sorted(set(d.tolist()))}  regular: {reg}")
    print(f"  the group is non-abelian: {comp(gens3[0], gens3[1]) != comp(gens3[1], gens3[0])}")
    print(f"""
  So NO -- non-abelian does not force irregular in general.  A non-abelian group with a
  regular Cayley graph exists at order six.

  Pass 4202's tension is therefore NOT a general law about instruction sets.  It is a fact
  about THIS group with THESE generators: the collisions that destroy regularity come from
  distinct opcodes sending some frame to the same frame, which is a property of the ACTION
  on 81 points, not of non-commutativity as such.  The Cayley graph of a group on ITSELF is
  always regular; the graph on a smaller transitive set need not be.

  That distinction is the whole thing, and it was worth checking rather than assuming: the
  81-frame graph is not a Cayley graph of ASp(4,3) at all -- it is a SCHREIER graph on a
  coset space, and Schreier graphs collide.""")

    out = {"transvections": len(T), "sets_tested": tested, "best": best,
           "s3_regular": bool(reg),
           "general_law": False,
           "correct_framing": "the 81-frame graph is a Schreier graph on a coset space, "
                              "not a Cayley graph of ASp(4,3); Schreier graphs collide"}
    path = ROOT / "data" / "PART_W33_PASS4203_TRANSVECTIONS_GENERAL_LAW.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
