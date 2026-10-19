"""Pass 12066: time turns triality (Claude track; continues 12064).

Two clocks at non-collinear events p, q split one generation of E6(p) matter as 27 = 1+1+1 + 8_v + 8_s + 8_c, with the
D4 given by the fibres of the four common neighbours {p,q}^perp (12064). Exact results in the 12052 root model:
  1. The symmetries fixing both events, Stab(p) n Stab(q) (48), act on {8_v, 8_s, 8_c} as the CYCLIC group Z3 (never
     a transposition); the kernel is the two-clock group H_p n Stab(q) = Stab(p) n H_q = C2 x Q8 (16). The Z3 is the
     clock-choice rotation: its elements move the clock real form at p (and at q).
  2. The generators are ticks: for each of the four common neighbours r (the events simultaneous with both clocks,
     whose fibres form the D4), t_r fixes p and q and the monomial, and cycles 8_v -> 8_s -> 8_c (t_r^2 reverses).
     Ticks at p, q and at the other two events of their hyperbolic line do not fix the pair.
Reading. A tick at an event simultaneous with both clocks is a triality rotation of the matter octets, and it is the
same operation as re-choosing the clocks. Only the cyclic half of triality (Z3, not S3) is realised -- time has an
orientation. Whether the three octets can be read as three families is not established here.
Scope: Weyl-level action on weights in the 12052 model.
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

OUT = ROOT / "data" / "w33_pass12066_time_turns_triality.json"


def model():
    R, C, fib, refl, perm = build()
    Adj, invs, tick, _ = setup()
    G = sp43_from_ticks(tick)
    cp = {}
    for k, s in invs:
        if k == "clock":
            ev = {x for x in range(40) if not s[fib[x]].any()}
            cp.setdefault(next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == ev), []).append(s)
    p = 0
    nb = [int(x) for x in np.nonzero(Adj[p])[0]]
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
    idx = {tuple(np.round(w * 6).astype(int)): k for k, w in enumerate(L27)}
    w27 = lambda v: idx.get(tuple(np.round(v * 6).astype(int)), idx.get(tuple(np.round(-v * 6).astype(int))))  # noqa: E731
    rep = {}
    for i in matter:
        if col3(i):
            rep.setdefault(w27(Pe @ R[i]), i)
    M = dict(R=R, fib=fib, Adj=Adj, tick=tick, G=G, cp=cp, p=p, nb=nb, far=far, Pe=Pe, col3=col3, L27=L27, w27=w27)
    M["act27"] = lambda g: tuple(w27(Pe @ R[g[rep[k]]]) for k in range(27))
    M["H"] = lambda x: np.all(cp[x][0][G] == cp[x][0][None, :], axis=1)
    M["S"] = lambda x: np.array([set(g[fib[x]]) == set(fib[x]) for g in G])
    M["mono"] = lambda x: tuple(sorted(w27(Pe @ R[i]) for i in fib[x] if col3(i)))
    M["trip"] = sorted(t for t in itertools.combinations(range(27), 3) if np.allclose(L27[list(t)].sum(0), 0))
    return M


def orbits(perms, n):
    seen, out = set(), []
    for k in range(n):
        if k not in seen:
            o = frozenset(int(a[k]) for a in perms)
            seen |= o
            out.append(o)
    return out


def main():
    checks, res = {}, {}
    M = model()
    G, p, nb, far, Adj, tick, fib = M["G"], M["p"], M["nb"], M["far"], M["Adj"], M["tick"], M["fib"]
    q = far[0]
    K = M["H"](p) & M["H"](q)
    orb = orbits([M["act27"](g) for g in G[K]], 27)
    eights = [o for o in orb if len(o) == 8]
    mono = sorted(k for o in orb if len(o) == 1 for k in o)
    checks["far clock pair: 27 = 1+1+1+8+8+8, singlets = the monomial of q (12064)"] = len(eights) == 3 and tuple(mono) == M["mono"](q)

    def on_octets(g):
        a = M["act27"](g)
        return tuple(eights.index(frozenset(a[k] for k in e)) if frozenset(a[k] for k in e) in eights else -1 for e in eights)
    S2 = M["S"](p) & M["S"](q)
    pat = Counter(on_octets(g) for g in G[S2])
    res["Stab_p_n_Stab_q_on_octets"] = {str(k): v for k, v in pat.items()}
    checks["Stab(p) n Stab(q) (48) acts on the octets as cyclic Z3 (16 each of id, (012), (021)); no transposition"] = (
        int(S2.sum()) == 48 and pat == Counter({(0, 1, 2): 16, (1, 2, 0): 16, (2, 0, 1): 16}))
    ker = M["H"](p) & M["S"](q)
    checks["kernel = H_p n Stab(q) = Stab(p) n H_q = C2 x Q8 (16), trivial on the octets"] = bool(
        int(ker.sum()) == 16 and np.array_equal(ker, M["S"](p) & M["H"](q)) and np.array_equal(ker, K)
        and all(on_octets(g) == (0, 1, 2) for g in G[ker]))
    common = [x for x in nb if Adj[q, x]]
    hyp = [x for x in range(40) if x not in (p, q) and all(Adj[x, y] for y in common)]
    ok = len(common) == 4 and len(hyp) == 2
    cyc = set()
    for r in common:
        t = tick[r]
        for g, want in ((t, None), (t[t], None)):
            fixes = set(g[fib[p]]) == set(fib[p]) and set(g[fib[q]]) == set(fib[q])
            a = M["act27"](g)
            ok &= fixes and sorted(a[k] for k in mono) == mono
            cyc.add(on_octets(g))
    checks["ticks at the 4 common neighbours fix p, q and the monomial and 3-cycle the octets"] = bool(ok and cyc == {(1, 2, 0), (2, 0, 1)})
    checks["ticks at p, q and the other two hyperbolic-line events do not fix the pair"] = all(
        not (set(tick[r][fib[p]]) == set(fib[p]) and set(tick[r][fib[q]]) == set(fib[q])) for r in [p, q] + hyp)
    moved = all(not np.array_equal(M["cp"][p][0][tick[r]], M["cp"][p][0]) for r in common)
    checks["the triality ticks move the clock real form at p (they lie outside H_p)"] = bool(moved)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
