"""Pass 12053: time is the centre of the clock's symmetry group. The compatible dynamics of each real form of E8
(Claude track; continues Pass 12052).

Ticks are determinant-one transvections t_p = r_v w^2 centred at points p of W(3,3) (12052); the 40 ticks generate
Sp(4,3) (51840, checked by closure). A dynamics is compatible with a real form iff it fixes the form's involution.
1. Gate sets (exact). One tick: 3 clock involutions, 0 split. Any two ticks with different centres -- even commuting
   ones at collinear centres -- admit NO non-compact real form. The same holds for the ticks of an isotropic line, of
   p-perp, of one hyperbolic line, and of a whole factorisation (which generate the local Clifford group
   SL2(3) x SL2(3)), and for all ticks. The hypothesis "local dynamics selects the split form" is therefore FALSE:
   the local Clifford group fixes no split involution either.
2. The full compatible groups (exact, from the closure):
   * clock involution at p: stabiliser of order 432, with centre EXACTLY <-1> x <t_p> = Z6, derived subgroup 54,
     abelianisation 8. It contains exactly two ticks, t_p^{+-1}.
   * split involution: stabiliser of order 384, centre {+-1}, derived subgroup 192, abelianisation 2. It contains
     NO tick.
Reading. The time generator of the clock real form is central in that form's entire symmetry group: every dynamics
compatible with the one-time real form commutes with the tick. That is the finite analogue of a Hamiltonian that
commutes with every conserved symmetry. The split real form admits no tick at all. So "one time" is not just
selected by a tick (12052): the tick is the centre of everything compatible with it.
Scope: compatibility = fixed involution (equivalently, commuting with the real structure, since Sp(4,3) sits in the
compact form); inner involutions; finite group statements.
Not new: transvection groups of Sp(4,3) and parabolic subgroups (classical); 12052 (classification).
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402

OUT = ROOT / "data" / "w33_pass12053_gate_sets_and_real_forms.json"


def setup():
    R, C, fib, refl, perm = build()
    W3 = np.linalg.matrix_power(C, 10)
    IP = R @ R.T
    Adj = np.array([[int(p != q and np.all(np.abs(IP[np.ix_(fib[p], fib[q])]) < 1e-9)) for q in range(40)] for p in range(40)])
    inv = {}
    for h in list(R) + [R[i] + R[j] for i in range(240) for j in range(i + 1, 240) if abs(IP[i, j]) < 1e-9]:
        inv.setdefault(tuple(((np.round(R @ h).astype(int)) % 2).tolist()), h)
    invs = []
    for sig in inv:
        s = np.array(sig, bool)
        invs.append(("clock" if 8 + 240 - s.sum() == 136 else "split", s))
    tick = {}
    for p in range(40):
        a = R[fib[p][0]]
        r = refl(a) @ refl(W3 @ a)
        if not np.allclose(np.linalg.matrix_power(r, 3), np.eye(8)):
            r = refl(a) @ refl(W3 @ W3 @ a)
        tick[p] = perm(r @ W3 @ W3)
    return Adj, invs, tick, fib


def compatible(points, invs, tick):
    out = {"clock": 0, "split": 0}
    for kind, s in invs:
        if all(np.all(s[tick[p]] == s) for p in points):
            out[kind] += 1
    return out


def main():
    Adj, invs, tick, fib = setup()
    res, checks = {}, {}
    p = 0
    nb = list(np.nonzero(Adj[p])[0])
    far = [q for q in range(40) if q != p and not Adj[p, q]]
    q_col, q_non = nb[0], far[0]
    # an isotropic line through p: p, q_col and the two common neighbours forming a triangle with them
    common = [r for r in nb if Adj[q_col, r]]
    line = [p, q_col] + common
    perp = [p] + nb
    # a factorisation: two orthogonal hyperbolic lines = the even set of a split involution
    split_sets = []
    for kind, s in invs:
        if kind == "split":
            S = frozenset(x for x in range(40) if not s[fib[x]].any())
            if S not in split_sets:
                split_sets.append(S)
    F = sorted(split_sets[0])
    # H1, H2: the two K4 halves -- points of F with no edge between them inside a half
    sub = Adj[np.ix_(F, F)]
    H1 = [F[0]] + [F[j] for j in range(1, 8) if not sub[0, j]]
    H2 = [x for x in F if x not in H1]
    gate_sets = {
        "one tick": [p],
        "two ticks, collinear centres": [p, q_col],
        "two ticks, non-collinear centres": [p, q_non],
        "ticks on an isotropic line (4)": line,
        "ticks on p-perp (13)": perp,
        "ticks on one hyperbolic line H1 (4): SL2(3) on one qutrit": H1,
        "ticks on a factorisation H1+H2 (8): local Clifford group": H1 + H2,
        "all 40 ticks: Sp(4,3)": list(range(40)),
    }
    table = {k: compatible(v, invs, tick) for k, v in gate_sets.items()}
    res["table"] = table
    res["line_ok"] = bool(len(line) == 4 and all(Adj[a, b] for a, b in itertools.combinations(line, 2)))
    res["H1_H2"] = [list(map(int, H1)), list(map(int, H2))]
    for k, v in table.items():
        print("%-62s clock %3d  split %3d" % (k, v["clock"], v["split"]))
    checks["one tick: exactly 3 clock, 0 split (12052)"] = table["one tick"] == {"clock": 3, "split": 0}
    checks["two ticks with different centres admit no non-compact real form"] = (
        table["two ticks, collinear centres"] == {"clock": 0, "split": 0} and table["two ticks, non-collinear centres"] == {"clock": 0, "split": 0})
    checks["refuted hypothesis recorded: the local Clifford group of a tensor split fixes no split involution either"] = (
        table["ticks on a factorisation H1+H2 (8): local Clifford group"] == {"clock": 0, "split": 0})
    checks["all ticks admit none (only the compact form)"] = table["all 40 ticks: Sp(4,3)"] == {"clock": 0, "split": 0}
    checks["sanity: the isotropic line is a 4-clique and H1, H2 are the two halves of K44"] = bool(
        res["line_ok"] and len(H1) == 4 and len(H2) == 4 and not any(Adj[a, b] for a in H1 for b in H1 if a != b)
        and all(Adj[a, b] for a in H1 for b in H2))
    nG, rc, rs = stabilisers()
    res["sp43_order_from_ticks"] = nG
    res["clock_stabiliser"] = rc
    res["split_stabiliser"] = rs
    checks["the 40 ticks generate Sp(4,3) (order 51840)"] = nG == 51840
    checks["clock stabiliser: order 432, centre exactly <-1> x <t_p> = Z6, derived 54, contains only the two ticks at p"] = (
        rc["order"] == 432 and rc["centre"] == 6 and rc.get("centre_is_minus1_times_tick") and rc["derived"] == 54 and rc["ticks_in"] == 2)
    checks["split stabiliser: order 384, centre {+-1}, derived 192, contains no tick"] = (
        rs["order"] == 384 and rs["centre"] == 2 and rs["derived"] == 192 and rs["ticks_in"] == 0)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res



def sp43_from_ticks(tick):
    """BFS closure of the 40 determinant-one ticks: the group Sp(4,3) as root permutations (expect 51840)."""
    gens = [tick[p].astype(np.int16) for p in range(40)]
    start = np.arange(240, dtype=np.int16)
    seen = {start.tobytes(): start}
    frontier = [start]
    while frontier:
        nxt = []
        for g in frontier:
            for t in gens:
                h = t[g]
                k = h.tobytes()
                if k not in seen:
                    seen[k] = h
                    nxt.append(h)
        frontier = nxt
    return np.array(list(seen.values()))


def closure(gens):
    idn = np.arange(240, dtype=np.int16)
    seen = {idn.tobytes(): idn}
    frontier = [idn]
    while frontier:
        nxt = []
        for g in frontier:
            for t in gens:
                h = t[g]
                if h.tobytes() not in seen:
                    seen[h.tobytes()] = h
                    nxt.append(h)
        frontier = nxt
    return list(seen.values())


def stabiliser_report(G, s, tick, centre_point=None):
    H = G[np.all(s[G] == s[None, :], axis=1)]
    Hl = [h.astype(np.int64) for h in H]
    cen = [h for h in Hl if all(np.array_equal(h[g], g[h]) for g in Hl)]
    inv = lambda p: np.argsort(p)  # noqa: E731
    comms = {}
    for a in Hl:
        for b in Hl[::7]:
            c = a[b[inv(a)[inv(b)]]]
            comms[c.astype(np.int16).tobytes()] = c.astype(np.int16)
    D = closure(list(comms.values()))
    ticks_in = [p for p in range(40) for t in (tick[p], tick[p][tick[p]]) if np.all(s[t] == s)]
    rep = dict(order=len(H), centre=len(cen), derived=len(D), abelianisation=len(H) // len(D), ticks_in=len(ticks_in),
               tick_centres=sorted(set(ticks_in)))
    if centre_point is not None:
        tp = tick[centre_point].astype(np.int64)
        minus = None
        for h in cen:
            if not np.array_equal(h, np.arange(240)) and np.array_equal(h[h], np.arange(240)):
                minus = h
        gen_c = {np.arange(240).tobytes()}
        for a in ([tp, tp[tp]] + ([minus] if minus is not None else [])):
            pass
        cand = closure([tp.astype(np.int16)] + ([minus.astype(np.int16)] if minus is not None else []))
        rep["centre_is_minus1_times_tick"] = bool(len(cand) == len(cen) and {c.tobytes() for c in cand} == {c.astype(np.int16).tobytes() for c in cen})
    return rep


def stabilisers():
    Adj, invs, tick, fib = setup()
    G = sp43_from_ticks(tick)
    cl = next(s for k, s in invs if k == "clock")
    sp = next(s for k, s in invs if k == "split")
    even = [x for x in range(40) if not cl[fib[x]].any()]
    centre = next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(even))
    return len(G), stabiliser_report(G, cl, tick, centre), stabiliser_report(G, sp, tick)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stab":
        print(stabilisers())
    else:
        main()
