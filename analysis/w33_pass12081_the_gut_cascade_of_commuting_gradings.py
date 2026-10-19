"""Pass 12081: the GUT cascade of commuting clock and split gradings -- every elementary abelian 2-subgroup of the E8
torus, its fixed algebra, and the first appearance of su(3) + su(2) (Claude track; 12071, 12077-12078).

The 255 inner involutions of E8 in one torus are the non-zero vectors of E8/2E8 = F_2^8: 120 clocks and 135 splits.
Commuting sets generate subspaces V; the fixed algebra of V is h + span(roots even under V). Each root alpha has a
class [alpha/2] (always a clock, 2 roots per clock), and alpha is even under V iff [alpha/2] lies in the orthogonal
complement V^perp for B(x,y) = 4<x,y> mod 2 -- verified directly. Exact classification (all subspaces):
  dim 1 (255):    e7+a1 (clock, 120), d8 (split, 135)
  dim 2 (10795):  e6 (1120, all 3 elements clocks), d6+2a1 (3780), a7 (4320), 2d4 (1575)
  dim 3 (97155):  d5 (7560, 6 clocks), a5+a1 (40320), d4+4a1 (9450), 2a3 (37800), 8a1 (2025)
  dim 4 (200787): d4 (3150), a4 (24192, 10 clocks), a3+2a1 (75600), 8a1 (2025), 2a2 (67200), 4a1 (28350), torus (270)
  dim 5 (97155):  a3 (7560), a2+a1 (40320, 16 clocks), 4a1 (9450), 2a1 (37800), torus (2025)
  dim 6 (10795):  a2 (1120), 2a1 (3780), a1 (4320), torus (1575);   dim 7: a1 (120), torus (135)
  The Standard-Model pair su(3) + su(2) (with u(1)^5) appears first and only at dimension 5, in 40320 subspaces.
  Every sampled SM subspace (40 of 40) contains a full flag of subspaces with fixed algebras
      e7+a1  >  e6  >  so(10)  >  su(5)  >  su(3)+su(2):
  the textbook grand-unified chain is a flag of commuting clock/split gradings of E8.
Reading. The maximal-symmetry branch (the largest fixed algebra at each dimension, which bosonic loops prefer, 12077-12078)
runs e7+a1 > e6 > so(10) and then turns to d4 and a3; su(5) and the Standard Model are the next-to-maximal choices at
dimensions 4 and 5. So the chain to the Standard Model exists inside the clock/split grading structure, but the simplest
dynamics does not single it out beyond SO(10). Scope: elementary abelian 2-groups of the torus (Wilson-line / grading
breaking); no continuous Higgs breaking.
"""

import json
import random
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12081_the_gut_cascade_of_commuting_gradings.json"
NAMES = {(2, 1): "A1", (6, 2): "A2", (12, 3): "A3", (20, 4): "A4", (30, 5): "A5", (42, 6): "A6", (56, 7): "A7", (72, 8): "A8",
         (24, 4): "D4", (40, 5): "D5", (60, 6): "D6", (84, 7): "D7", (112, 8): "D8", (72, 6): "E6", (126, 7): "E7", (240, 8): "E8"}


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    vecs = [s for k, s in invs]
    kinds = [k for k, s in invs]
    key = {s.tobytes(): i for i, s in enumerate(vecs)}
    n = len(vecs)
    IP = np.round(R @ R.T).astype(int)
    cache = {}

    def rootsys(mask):
        k = mask.tobytes()
        if k not in cache:
            idx = np.nonzero(mask)[0]
            sub = IP[np.ix_(idx, idx)] != 0
            seen, out = np.zeros(len(idx), bool), []
            for i in range(len(idx)):
                if seen[i]:
                    continue
                comp, st = {i}, [i]
                while st:
                    a = st.pop()
                    for b in np.nonzero(sub[a])[0]:
                        if b not in comp:
                            comp.add(int(b))
                            st.append(int(b))
                seen[list(comp)] = True
                c = sorted(comp)
                out.append(NAMES.get((len(c), int(np.linalg.matrix_rank(R[idx[c]]))), "?"))
            cache[k] = tuple(sorted(out))
        return cache[k]
    checks["255 non-zero classes: 120 clocks + 135 splits"] = n == 255 and kinds.count("clock") == 120
    level = {1: {frozenset([i]) for i in range(n)}}
    for d in (2, 3, 4):
        nxt = set()
        for S in level[d - 1]:
            for v in range(n):
                if v not in S:
                    nxt.add(frozenset(S | {key[(vecs[v] ^ vecs[u]).tobytes()] for u in S} | {v}))
        level[d] = nxt
    checks["subspace counts 255, 10795, 97155, 200787 (Gaussian binomials of F_2^8)"] = [len(level[d]) for d in (1, 2, 3, 4)] == [255, 10795, 97155, 200787]
    table = {}
    for d in (1, 2, 3, 4):
        c = Counter()
        for S in level[d]:
            m = np.ones(240, bool)
            for v in S:
                m &= ~vecs[v]
            c[(8 + int(m.sum()), rootsys(m), sum(1 for v in S if kinds[v] == "clock"))] += 1
        table[d] = c
    rootcls = np.array([key[(np.round(R @ R[a]).astype(int) % 2 == 1).tobytes()] for a in range(240)])
    checks["each root class [alpha/2] is a clock, two roots per clock"] = all(kinds[c] == "clock" for c in rootcls) and set(Counter(rootcls).values()) == {2}
    for k in (3, 2, 1):
        c = Counter()
        for U in level[k]:
            m = np.isin(rootcls, list(U))
            c[(8 + int(m.sum()), rootsys(m), None)] += 1
        table[8 - k] = c
    res["cascade"] = {str(d): {str(k[:2]) + (" clocks=%s" % k[2] if k[2] is not None else ""): v for k, v in c.items()} for d, c in table.items()}
    exp = {1: {(136, ("A1", "E7")): 120, (120, ("D8",)): 135},
           2: {(80, ("E6",)): 1120, (72, ("A1", "A1", "D6")): 3780, (64, ("A7",)): 4320, (56, ("D4", "D4")): 1575},
           3: {(48, ("D5",)): 7560, (40, ("A1", "A5")): 40320, (40, ("A1",) * 4 + ("D4",)): 9450, (32, ("A3", "A3")): 37800, (24, ("A1",) * 8): 2025},
           4: {(32, ("D4",)): 3150, (28, ("A4",)): 24192, (24, ("A1", "A1", "A3")): 75600, (24, ("A1",) * 8): 2025, (20, ("A2", "A2")): 67200,
               (16, ("A1",) * 4): 28350, (8, ()): 270},
           5: {(20, ("A3",)): 7560, (16, ("A1", "A2")): 40320, (16, ("A1",) * 4): 9450, (12, ("A1", "A1")): 37800, (8, ()): 2025},
           6: {(14, ("A2",)): 1120, (12, ("A1", "A1")): 3780, (10, ("A1",)): 4320, (8, ()): 1575},
           7: {(10, ("A1",)): 120, (8, ()): 135}}
    agg = {d: Counter() for d in table}
    for d, c in table.items():
        for k, v in c.items():
            agg[d][k[:2]] += v
    checks["fixed algebras of all subspaces, dimensions 1-7, as tabulated"] = all(dict(agg[d]) == exp[d] for d in exp)
    sm = sorted({d for d in agg for k in agg[d] if "A2" in k[1] and "A1" in k[1]})
    checks["su(3)+su(2) appears first and only at dimension 5 (40320 subspaces)"] = sm == [5]
    random.seed(2)
    V3 = [U for U in level[3] if rootsys(np.isin(rootcls, list(U))) == ("A1", "A2")]
    target = [("A1", "E7"), ("E6",), ("D5",), ("A4",), ("A1", "A2")]

    def fixed_rs(S):
        m = np.ones(240, bool)
        for h in S:
            m &= ~vecs[h]
        return rootsys(m)

    def span_of(els):
        cur = [np.zeros(240, bool)]
        for h in els:
            cur = cur + [c ^ vecs[h] for c in cur]
        return frozenset(key[c.tobytes()] for c in cur if c.any())
    dual_ok, flags, clk = True, 0, Counter()
    for U in random.sample(V3, 40):
        m = np.isin(rootcls, list(U))
        V = [h for h in range(n) if not np.any(vecs[h][m])]
        fx = np.ones(240, bool)
        for h in V:
            fx &= ~vecs[h]
        dual_ok &= len(V) == 31 and np.array_equal(fx, m)
        clk[sum(1 for h in V if kinds[h] == "clock")] += 1

        def dfs(gens, depth):
            if depth == 5:
                return True
            S = span_of(gens) if gens else frozenset()
            for h in V:
                if h in S:
                    continue
                if fixed_rs(span_of(gens + [h])) == target[depth] and dfs(gens + [h], depth + 1):
                    return True
            return False
        flags += int(dfs([], 0))
    checks["duality verified: each SM subspace V (31 elements) fixes exactly the roots whose class lies in V^perp"] = bool(dual_ok)
    checks["SM subspaces have 16 clocks + 15 splits"] = clk == Counter({16: 40})
    checks["every sampled SM subspace (40/40) contains a flag e7+a1 > e6 > so(10) > su(5) > su(3)+su(2)"] = flags == 40
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
