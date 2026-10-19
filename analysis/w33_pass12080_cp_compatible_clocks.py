"""Pass 12080: time reversals inside E8 -- Kramers observers square to -1, flavour CP squares to +1, and each CP picks
one clock at each event it fixes (Claude track; 12059, 12069, 12079).

Construction. Write the Coxeter element C of the 12052 model in bipartite form by conjugation (cyclic shifts and
commutations of simple reflections), C = h^-1 (c1 c2) h; then w = h^-1 c1 h is an involution in W(E8) with
w C w^-1 = C^-1, so w inverts the Eisenstein unit omega = C^10, preserves the forty fibres and acts on W(3,3)
anti-symplectically. The anti-symplectic elements of W(E8) normalising the fibration are the coset w * (3 x Sp(4,3)).
Exact results (all 51840 elements w g, g in Sp(4,3)):
  1. Those inducing an involution of the forty events are exactly
       72 with NO fixed event and e^2 = -1 in W(E8)   -- the Kramers reversals (observers, 12059), and
       1080 with 8 fixed events and e^2 = +1           -- the bosonic CPs (12069: pairs of disjoint contexts).
     The fermionic/bosonic dichotomy J^2 = -+1 on F_3^4 is literally e^2 = -+1 in W(E8).
  2. Clocks. The Eisenstein unit omega keeps every clock at its event and 3-cycles the three clocks there: the clock
     choice at an event is a choice of cube root of unity. A Kramers reversal preserves no clock. Every bosonic CP
     preserves exactly 8 clocks, exactly ONE at each of its 8 fixed events (the CP-compatible clocks).
  3. The four CP-compatible clocks on one of its contexts L leave su(2)^8 on exactly the CP's own fixed set L u L'
     (12079), for all 1080 CPs.
Reading. Observers' time reversals and flavour CP are the two square classes (-1, +1) of antilinear Weyl elements of
E8. A flavour CP singles out one clock at each event it fixes, and on its fixed contexts those clocks leave the
Hamming-code su(2)^8. Scope: W(E8)-level statements in the 12052 model.
"""

import itertools
import json
import sys
from collections import Counter, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402

OUT = ROOT / "data" / "w33_pass12080_cp_compatible_clocks.json"
SIMPLE = ([0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
          [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0])


def inverting_involution(C, refl):
    simple = [np.array(v, float) for v in SIMPLE]
    S = [refl(a) for a in simple]
    Cm = np.round(np.array([[a @ b for b in simple] for a in simple])).astype(int)
    col = {0: 0}
    st = [0]
    while st:
        i = st.pop()
        for j in range(8):
            if j != i and Cm[i, j] != 0 and j not in col:
                col[j] = 1 - col[i]
                st.append(j)
    start = tuple(range(8))
    prev, dq, end = {start: None}, deque([start]), None
    while dq:
        o = dq.popleft()
        if all(col[o[k]] <= col[o[k + 1]] for k in range(7)):
            end = o
            break
        nb = [(o[:k] + (o[k + 1], o[k]) + o[k + 2:], None) for k in range(7) if Cm[o[k], o[k + 1]] == 0]
        nb.append((o[1:] + (o[0],), o[0]))
        for n, s in nb:
            if n not in prev:
                prev[n] = (o, s)
                dq.append(n)
    seq, o = [], end
    while prev[o] is not None:
        po, s = prev[o]
        if s is not None:
            seq.append(s)
        o = po
    h = np.eye(8)
    for s in seq[::-1]:
        h = S[s] @ h
    first = [i for i in end if col[i] == col[end[0]]]
    c1 = np.linalg.multi_dot([S[i] for i in first]) if len(first) > 1 else S[first[0]]
    return np.linalg.inv(h) @ c1 @ h


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    G = sp43_from_ticks(tick)
    wm = inverting_involution(C, refl)
    checks["w in W(E8): involution with w C w^-1 = C^-1 (inverts omega = C^10)"] = bool(
        np.allclose(wm @ wm, np.eye(8)) and np.allclose(wm @ C @ np.linalg.inv(wm), np.linalg.inv(C)))
    w = perm(wm)
    Wp = perm(np.linalg.matrix_power(C, 10))
    neg = perm(-np.eye(8))
    ptof = np.empty(240, int)
    for x in range(40):
        for i in fib[x]:
            ptof[i] = x
    clocks = [s for k, s in invs if k == "clock"]
    Pc = np.array(clocks)
    cpt = np.array([next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == {y for y in range(40) if not s[fib[y]].any()}) for s in clocks])
    checks["w preserves the forty fibres"] = all(len({ptof[w[i]] for i in fib[x]}) == 1 for x in range(40))
    om_ok = all(not np.array_equal(Pc[i][Wp], Pc[i]) and any(np.array_equal(Pc[i][Wp], Pc[j]) and cpt[j] == cpt[i] for j in range(120))
                and np.array_equal(Pc[i][Wp][Wp][Wp], Pc[i]) for i in range(120))
    checks["omega keeps each clock at its event and 3-cycles the three clocks there"] = bool(om_ok)
    idn = np.arange(240)
    stats, link_ok, ncp = Counter(), True, 0
    for g in G:
        e = w[g]
        pp = np.array([ptof[e[fib[x][0]]] for x in range(40)])
        if not np.array_equal(pp[pp], np.arange(40)):
            continue
        fixed = sorted(np.where(pp == np.arange(40))[0].tolist())
        sq = e[e]
        sqt = "+1" if np.array_equal(sq, idn) else ("-1" if np.array_equal(sq, neg) else "other")
        keep = [i for i in range(120) if np.array_equal(Pc[i][e], Pc[i])]
        perfix = Counter(int(np.sum(cpt[keep] == x)) for x in fixed)
        stats[(len(fixed), sqt, len(keep), tuple(sorted(perfix.items())))] += 1
        if len(fixed) == 8:
            ncp += 1
            L = next(list(c) for c in itertools.combinations(fixed, 4) if all(Adj[a, b] for a in c for b in c if a != b))
            cl4 = [i for i in keep if cpt[i] in L]
            even = np.ones(240, bool)
            for i in cl4:
                even &= ~Pc[i]
            link_ok &= len(cl4) == 4 and int(even.sum()) == 16 and {ptof[i] for i in np.nonzero(even)[0]} == set(fixed)
    res["involutions_on_events"] = {str(k): v for k, v in stats.items()}
    checks["the coset w Sp(4,3) contains exactly 72 (0 fixed events, e^2 = -1) + 1080 (8 fixed events, e^2 = +1) event involutions"] = (
        stats == Counter({(0, "-1", 0, ()): 72, (8, "+1", 8, ((1, 8),)): 1080}))
    checks["Kramers reversals preserve no clock; each bosonic CP preserves exactly one clock at each of its 8 fixed events"] = (
        stats[(0, "-1", 0, ())] == 72 and stats[(8, "+1", 8, ((1, 8),))] == 1080)
    checks["for all 1080 CPs, the CP-compatible clocks on L leave su(2)^8 on exactly the CP fixed set L u L'"] = bool(link_ok and ncp == 1080)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
