"""Pass 12064: a second clock is a Yukawa monomial, and two clocks split matter by triality (Claude track; 12056, 12060).

Setting (12052, 12056). In the root model, a point p has the A2(p) fibre, E6(p) = the 12 neighbour fibres, and the
162 matter roots (27,3) + (27bar,3bar) in the 27 far fibres. The clock group H_p (432) preserves E6(p).
Exact results:
  1. Each far fibre carries one E6 cubic monomial. Its three colour-3 roots project to three weights of the 27 of E6(p)
     that sum to zero (a tritangent: Gram 4/3 on the diagonal, -2/3 off it). The zero sum is automatic, r + w r + w^2 r =
     0 for the Eisenstein fibre; the 270 lifted triples are corpus (2026-09-21 matter81). The 27 far points give 9
     tritangents, 3 points each, and these PARTITION the 27 weights -- one of the nine-tritangent covers of PASS5010.
  2. Vacuum symmetry on matter, modulo -1 (which only exchanges 27 and 27bar):
       one clock (H_p, 432):                      transitive on the 27;
       two collinear clocks (+-1 x S3, 12):       27 = 3 + 3 + 3 + 6 + 6 + 6;
       two non-collinear clocks (C2 x Q8, 16):    27 = 1 + 1 + 1 + 8 + 8 + 8.
  3. TRIALITY. For the non-collinear pair, the three fixed weights are exactly the monomial of the second clock's
     fibre. The E6 roots orthogonal to it form D4, and they are exactly the fibres of the four common neighbours
     {p, q}^perp (the D4 of 12056). Each 8-orbit is a minuscule weight system of that D4 (norm 1, four antipodal pairs,
     <w, alpha> in {0, +-1}), and the three are distinct. So the two-clock vacuum splits one generation of E6 matter
     as 27 = 1 + 1 + 1 + 8_v + 8_s + 8_c, the Spin(8) triality decomposition, with the three singlets = the Yukawa
     monomial carried by the second clock.
Reading. Relative to a clock at p, every non-collinear event q is a Yukawa coupling 27^3 of E6(p) matter. Putting a
second clock there leaves the spin group C2 x Q8 (12060) and splits matter into the three Spin(8) octets permuted by
triality plus the three monomial singlets. The E6 > D4 x U(1)^2 branching is classical; new is that the two-clock
vacuum realises it with the singlets on the second clock.
Scope: weight-level (Weyl-group) statements in the 12052 root model; no Yukawa magnitude or vacuum energy is computed.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402

OUT = ROOT / "data" / "w33_pass12064_a_second_clock_is_a_yukawa_monomial.json"


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    G = sp43_from_ticks(tick)
    cp = {}
    for k, s in invs:
        if k == "clock":
            ev = {x for x in range(40) if not s[fib[x]].any()}
            cp.setdefault(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev), s)
    Hmask = lambda x: np.all(cp[x][G] == cp[x][None, :], axis=1)  # noqa: E731
    p = 0
    nb = list(np.nonzero(Adj[p])[0])
    far = [x for x in range(40) if x != p and not Adj[p, x]]
    A2 = R[fib[p]]
    Pa = A2.T @ np.linalg.pinv(A2.T)
    Pe = np.eye(8) - Pa
    matter = sum((fib[x] for x in far), [])
    ms = sorted({tuple(np.round(Pa @ R[i] * 6).astype(int)) for i in matter})
    m0 = np.array(ms[0]) / 6
    three = [np.array(m) / 6 for m in ms if np.allclose(np.array(m) / 6, m0) or any(np.allclose(np.array(m) / 6 - m0, a) for a in A2)]
    col3 = lambda i: any(np.allclose(Pa @ R[i], m) for m in three)  # noqa: E731
    L27 = np.array(sorted({tuple(np.round(Pe @ R[i] * 6).astype(int)) for i in matter if col3(i)})) / 6
    idx27 = {tuple(np.round(w * 6).astype(int)): k for k, w in enumerate(L27)}
    w27 = lambda v: idx27.get(tuple(np.round(v * 6).astype(int)), idx27.get(tuple(np.round(-v * 6).astype(int))))  # noqa: E731
    gram = np.round(L27 @ L27.T * 3).astype(int)
    checks["27 weights of E6(p): norms 4/3, others 1/3 (x16) and -2/3 (x10)"] = bool(
        len(L27) == 27 and all(Counter(gram[i].tolist()) == Counter({4: 1, 1: 16, -2: 10}) for i in range(27)))
    trip = {t for t in itertools.combinations(range(27), 3) if np.allclose(L27[list(t)].sum(0), 0)}
    mono = {}
    for x in far:
        mono[x] = tuple(sorted(w27(Pe @ R[i]) for i in fib[x] if col3(i)))
    checks["each far fibre carries one tritangent (E6 cubic monomial); 45 tritangents in all"] = len(trip) == 45 and all(
        len(m) == 3 and m in trip for m in mono.values())
    cover = Counter(mono.values())
    checks["the 27 far points give 9 tritangents, 3 points each, partitioning the 27 weights"] = bool(
        len(cover) == 9 and set(cover.values()) == {3} and sorted(sum(cover.keys(), ())) == list(range(27)))

    def orbits27(mask):
        els = G[mask]
        rep = {}
        for i in matter:
            if col3(i):
                rep.setdefault(w27(Pe @ R[i]), i)
        perm27 = np.array([[w27(Pe @ R[g[rep[k]]]) for k in range(27)] for g in els])
        seen, out = set(), []
        for k in range(27):
            if k not in seen:
                o = set(perm27[:, k].tolist())
                seen |= o
                out.append(sorted(o))
        return out
    Hp = Hmask(p)
    o1 = orbits27(Hp)
    q_col, q_far = nb[0], far[0]
    oc = orbits27(Hp & Hmask(q_col))
    of = orbits27(Hp & Hmask(q_far))
    res["orbit_sizes"] = dict(one_clock=sorted(map(len, o1)), collinear_pair=sorted(map(len, oc)), far_pair=sorted(map(len, of)))
    checks["orbits on the 27 (mod -1): one clock 27; collinear pair 3,3,3,6,6,6; far pair 1,1,1,8,8,8"] = res["orbit_sizes"] == dict(
        one_clock=[27], collinear_pair=[3, 3, 3, 6, 6, 6], far_pair=[1, 1, 1, 8, 8, 8])
    fixed = sorted(o[0] for o in of if len(o) == 1)
    checks["far pair: the 3 fixed weights are exactly the second clock's monomial"] = tuple(fixed) == mono[q_far]
    E6r = R[sum((fib[x] for x in nb), [])]
    D4 = [i for x in nb for i in fib[x] if np.allclose(L27[fixed] @ R[i], 0)]
    common = [x for x in nb if Adj[q_far, x]]
    checks["E6 roots orthogonal to the monomial: 24, rank 4 (D4) = the fibres of the 4 common neighbours {p,q}^perp"] = bool(
        len(D4) == 24 and np.linalg.matrix_rank(R[D4]) == 4 and sorted(D4) == sorted(sum((fib[x] for x in common), []))
        and len(common) == 4 and len(E6r) == 72)
    B = np.linalg.svd(R[D4])[2][:4]
    mins = []
    for o in of:
        if len(o) != 8:
            continue
        P = L27[o] @ B.T
        g = np.round(P @ P.T * 4).astype(int)
        ips = np.round(P @ (R[D4] @ B.T).T * 2).astype(int)
        anti = sum(1 for i in range(8) for j in range(i + 1, 8) if np.allclose(P[i], -P[j]))
        mins.append((set(np.diag(g).tolist()) == {4} and anti == 4 and set(ips.ravel().tolist()) <= {-2, 0, 2},
                     frozenset(map(tuple, np.round(P * 6).astype(int)))))
    checks["triality: the three 8-orbits are minuscule D4 weight systems, pairwise distinct (8_v, 8_s, 8_c)"] = bool(
        len(mins) == 3 and all(m[0] for m in mins) and len({m[1] for m in mins}) == 3)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
