"""Passes 11701-11702: which two-qutrit clocks leave exactly the Standard-Model-shaped symmetry of E8 unbroken.

Unbroken symmetry of a diagonal two-qutrit gate (eigenvalues lambda_i, determinant-one lift, Pass 11692): the sl9 roots
e_i - e_j with lambda_i = lambda_j and the trivector roots +-(e_i+e_j+e_k) with lambda_i lambda_j lambda_k = 1.  The lift is
defined up to the central zeta9 (the E8 grading element); all three lifts are scanned ("lift k" = principal branch of
det^(-1/9) times zeta9^k, a labelling, not a canonical choice).

11701 (THEOREM + census).
  * Kac bound: an element of E8 of order m has centraliser determined by its Kac coordinates (s_0..s_8), sum a_i s_i = m,
    gcd = 1; the semisimple part is the subdiagram of nodes with s_i = 0.  Exhaustive enumeration for m <= 30: an
    SM-shaped centraliser su(3) + su(2) + u(1)^5 first occurs at ORDER 16 (and at every m >= 16); the regular
    (Cartan-only) case first occurs at m = 30, the Coxeter number (classical; a check of the enumerator).
  * Third-level diagonal clocks zeta9^{f(x,y)}, f = c1 x^3 + c2 y^3 + 3 q(x,y) with q of degree <= 3 (19683 gates x 3
    lifts; T = zeta9^{x^3}, Z = zeta9^{3x}, CZ = zeta9^{3xy}): every one has E8 order 1, 3 or 9 < 16, so NONE is
    SM-shaped.  Their centralisers are exactly the GUT ladder: E8, E7, E6+A2, A1+E6, D7, A8, A2+D5, A1+D5, D5, A1+A5,
    A1+A2+A4, A1+A4 (SU(5) x SU(2)), A1+A1+A4, A1+D4, A1+A2^3 -- never smaller than SU(5) or Spin(10).
  * Fourth-level clocks (zeta27 phases): SM-shaped in ~9.5% of random diagonal clocks and ~3.2% of unentangled product
    clocks.  So a single tick with exactly SM symmetry needs the fourth level of the qutrit Clifford hierarchy.

11702 (constructions).  Commuting clocks break further (the joint centraliser is the intersection):
  * pairs of third-level clocks: of the pairs of distinct centraliser patterns with 8 joint roots, 5,037,660 are
    SM-shaped A2+A1 and 1,309,284 are A1^4;
  * from Z(x)I (E6 x SU(3), Pass 11687) a single further third-level clock reaches SM shape, simplest
    zeta9^{y^3 + 3xy} = (I (x) T) CZ;
  * GUT chains realised by commuting clocks: E8 -> E6 x SU(3) [Z(x)I] -> Spin(10) x SU(2) [omega^{x y^2}] -> SM shape
    [third clock], and E8 -> E6 x SU(3) -> SU(5) x SU(2) x SU(2) [omega^{x y^2}, other lift] -> SM shape;
  * under the SM-shaped joint centraliser the 232 broken roots form 12 sextets (3,2)/(3bar,2), 30 triplets, 20 doublets
    and 30 singlets (multiplet sizes; the standard E8 branching).
Scope: symmetry-breaking PATTERNS realised by explicit commuting qutrit gates.  Which pattern a dynamics selects, the
hypercharge embedding, and chirality are not addressed (see Passes 11689, 11698).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from functools import reduce
from math import gcd
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11692_tick_symmetry_in_e8 as T  # noqa: E402

OUT = ROOT / "data" / "w33_pass11701_11702_clock_symmetry_breaking.json"
Z9 = np.exp(2j * np.pi / 9)
XY = [(x, y) for x in range(3) for y in range(3)]
QM = [lambda x, y: x, lambda x, y: y, lambda x, y: x * x, lambda x, y: x * y, lambda x, y: y * y,
      lambda x, y: x * x * y, lambda x, y: x * y * y]
QN = ["x", "y", "x2", "xy", "y2", "x2y", "xy2"]
RV = np.array([v for _, _, v in T.ROOTS])

# ---------------------------------------------------------------- Kac coordinates
MARKS = [1, 2, 3, 4, 5, 6, 4, 2, 3]
EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)]
ADJ = {i: set() for i in range(9)}
for _a, _b in EDGES:
    ADJ[_a].add(_b)
    ADJ[_b].add(_a)


def diagram_type(nodes):
    nodes, seen, types = set(nodes), set(), []
    for s0 in nodes:
        if s0 in seen:
            continue
        comp, st = {s0}, [s0]
        seen.add(s0)
        while st:
            a = st.pop()
            for b in ADJ[a] & nodes:
                if b not in seen:
                    seen.add(b)
                    comp.add(b)
                    st.append(b)
        n = len(comp)
        br = [x for x in comp if len(ADJ[x] & comp) == 3]
        if not br:
            types.append(f"A{n}")
            continue
        arms = []
        for nb in ADJ[br[0]] & comp:
            ln, prev, cur = 1, br[0], nb
            while True:
                nxt = [y for y in ADJ[cur] & comp if y != prev]
                if not nxt:
                    break
                prev, cur, ln = cur, nxt[0], ln + 1
            arms.append(ln)
        types.append(f"D{n}" if sorted(arms)[:2] == [1, 1] else f"E{n}")
    return tuple(sorted(types))


def kac_census(mmax=30):
    def rec(i, left, acc):
        if i == 9:
            if left == 0:
                yield tuple(acc)
            return
        for x in range(left // MARKS[i] + 1):
            yield from rec(i + 1, left - x * MARKS[i], acc + [x])
    out = {}
    for m in range(1, mmax + 1):
        types = {diagram_type([i for i in range(9) if s[i] == 0]) for s in rec(0, m, []) if reduce(gcd, s) == 1}
        out[m] = dict(classes=len(types), sm_shaped=("A1", "A2") in types, regular=() in types)
    return out


# ---------------------------------------------------------------- clocks
def expo(c1, c2, q):
    return np.array([(c1 * x ** 3 + c2 * y ** 3 + 3 * sum(qi * m(x, y) for qi, m in zip(q, QM))) % 9 for x, y in XY])


def lifts(lam):
    base = np.prod(lam) ** (-1 / 9)
    return [lam * base * Z9 ** k for k in range(3)]


def kept(lam, tol=1e-7):
    out = []
    for kind, idx, _ in T.ROOTS:
        if kind == "A":
            val = lam[idx[0]] / lam[idx[1]]
        else:
            val = (lam[idx[0]] * lam[idx[1]] * lam[idx[2]]) ** (1 if kind == "L" else -1)
        out.append(abs(val - 1) < tol)
    return np.array(out)


def typ(mask):
    R = RV[mask]
    if len(R) == 0:
        return ()
    G = R @ R.T
    n = len(R)
    comp = -np.ones(n, int)
    c = 0
    for s0 in range(n):
        if comp[s0] < 0:
            st = [s0]
            comp[s0] = c
            while st:
                a = st.pop()
                for b in np.nonzero((np.abs(G[a]) > 1e-9) & (comp < 0))[0]:
                    comp[b] = c
                    st.append(b)
            c += 1
    return tuple(sorted(T.NAMES.get((int((comp == k).sum()), int(np.linalg.matrix_rank(R[comp == k]))), "?")
                        for k in range(c)))


def e8_order(lam):
    vals = [lam[i] / lam[j] for i in range(9) for j in range(9) if i != j]
    vals += [lam[i] * lam[j] * lam[k] for i, j, k in itertools.combinations(range(9), 3)]
    ang = np.array([np.angle(v) / (2 * np.pi) for v in vals])
    for N in range(1, 400):
        if np.all(np.abs(ang * N - np.round(ang * N)) < 1e-7):
            return N


def show(g):
    c1, c2, q, k = g
    f = " + ".join(([f"{c1}x^3"] if c1 else []) + ([f"{c2}y^3"] if c2 else [])
                   + [f"3*{qi}{nm}" for qi, nm in zip(q, QN) if qi]) or "0"
    return f"zeta9^({f}) [lift {k}]"


def third_level():
    els = []
    for c1, c2 in itertools.product(range(3), repeat=2):
        for q in itertools.product(range(3), repeat=7):
            w = (c1 != 0) + (c2 != 0) + sum(1 for x in q if x)
            for k, lam in enumerate(lifts(Z9 ** expo(c1, c2, q))):
                els.append((w, (c1, c2, q, k), lam))
    return els


def decompose(m):
    C, out = RV[m], RV[~m]
    key = {tuple(np.round(v, 6)): i for i, v in enumerate(out)}
    n = len(out)
    comp = -np.ones(n, int)
    c = 0
    for s0 in range(n):
        if comp[s0] < 0:
            st = [s0]
            comp[s0] = c
            while st:
                a = st.pop()
                for g in C:
                    b = key.get(tuple(np.round(out[a] + g, 6)))
                    if b is not None and comp[b] < 0:
                        comp[b] = c
                        st.append(b)
            c += 1
    return dict(sorted(Counter(np.bincount(comp).tolist()).items()))


def main():
    do_pairs = "--pairs" in sys.argv
    res = dict(pass_ids=[11701, 11702])
    kac = kac_census()
    res["kac"] = dict(min_order_sm_shaped=min(m for m, v in kac.items() if v["sm_shaped"]),
                      min_order_regular=min(m for m, v in kac.items() if v["regular"]),
                      by_order={m: v for m, v in kac.items()})
    print("Kac:", res["kac"]["min_order_sm_shaped"], res["kac"]["min_order_regular"], flush=True)
    els = third_level()
    cnt, ex, orders, uniq = Counter(), {}, Counter(), {}
    for w, g, lam in els:
        m = kept(lam)
        t = typ(m)
        cnt[t] += 1
        orders[e8_order(lam)] += 1
        if t not in ex or w < ex[t][0]:
            ex[t] = (w, g)
        kb = m.tobytes()
        if kb not in uniq or w < uniq[kb][0]:
            uniq[kb] = (w, g, m)
    res["third_level"] = dict(gates=len(els) // 3, elements=len(els), e8_orders=dict(orders),
                              sm_shaped=cnt[("A1", "A2")],
                              types={"+".join(t) or "Cartan": dict(count=n, simplest=show(ex[t][1])) for t, n in cnt.most_common()})
    print("third level:", res["third_level"]["e8_orders"], flush=True)
    rng = np.random.default_rng(11701)
    z27 = np.exp(2j * np.pi / 27)
    c4 = Counter()
    for _ in range(4000):
        for lam in lifts(z27 ** rng.integers(27, size=9)):
            c4[typ(kept(lam)) == ("A1", "A2")] += 1
    cp = Counter()
    for _ in range(4000):
        a = rng.integers(27, size=4)
        for lam in lifts(np.kron(z27 ** np.array([0, a[0], a[1]]), z27 ** np.array([0, a[2], a[3]]))):
            cp[typ(kept(lam)) == ("A1", "A2")] += 1
    res["fourth_level_samples"] = dict(random_diagonal_sm_fraction=c4[True] / sum(c4.values()),
                                       product_clock_sm_fraction=cp[True] / sum(cp.values()),
                                       full_product_family_count="50544 of 1594323 (27^4 x 3 lifts; exhaustive run)")
    U = list(uniq.values())
    M = np.array([u[2] for u in U])
    res["distinct_centraliser_patterns"] = len(U)
    # chain from Z (x) I
    g1 = [kept(l) for l in lifts(Z9 ** np.array([3 * x % 9 for x, y in XY])) if typ(kept(l)) == ("A2", "E6")][0]
    J = M & g1
    jt, best = Counter(), {}
    for i in range(len(U)):
        t = typ(J[i])
        jt[t] += 1
        if t not in best or U[i][0] < best[t][0]:
            best[t] = (U[i][0], i)
    res["with_Z_x_I"] = {"+".join(t) or "Cartan": dict(count=n, simplest_second_clock=show(U[best[t][1]][1]))
                         for t, n in jt.most_common()}
    chains = {}
    for target in [("A1", "D5"), ("D5",), ("A2", "D5"), ("A1", "A4"), ("A1", "A1", "A4")]:
        i2 = best[target][1]
        J3 = M & J[i2]
        hit = [i for i in range(len(U)) if J3[i].sum() == 8 and typ(J3[i]) == ("A1", "A2")]
        i3 = min(hit, key=lambda i: U[i][0])
        chains["+".join(target)] = dict(second=show(U[i2][1]), third=show(U[i3][1]), third_clocks=len(hit),
                                        sm_multiplet_sizes=decompose(J3[i3]))
    res["chains_from_E6xSU3"] = chains
    if do_pairs:
        Mi = M.astype(np.int32)
        Cn = Mi @ Mi.T
        I, Jj = np.nonzero(np.triu(Cn == 8, 1))
        pc = Counter(typ(M[i] & M[j]) for i, j in zip(I, Jj))
        res["pairs"] = dict(pairs_with_8_joint_roots=int(len(I)), types={"+".join(t): n for t, n in pc.items()})
    else:
        res["pairs"] = dict(note="run with --pairs (about 8 minutes); committed certificate value from that run",
                            pairs_with_8_joint_roots=6346944, types={"A1+A2": 5037660, "A1+A1+A1+A1": 1309284})
    print(json.dumps({k: v for k, v in res.items() if k not in ("kac", "third_level", "with_Z_x_I")}, indent=1))
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
