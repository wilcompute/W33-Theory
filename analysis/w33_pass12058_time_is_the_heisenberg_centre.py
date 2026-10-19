"""Pass 12058: time is the central charge of space translations. The symmetry group of the clock real form E8(-24)
at a point p is a finite spin-Galilei group: a Heisenberg group of translations whose centre is the tick, extended by
+-1 x Q8 (Claude track; continues 12052-12053).

H = stabiliser in Sp(4,3) of a clock involution at p (order 432, 12053). Exact results:
  1. U = the elements of 3-power order: 27 elements, normal, exponent 3, NONABELIAN, with Z(U) = [U,U] = <t_p>. U is a
     Heisenberg group 3^{1+2} whose centre is the tick group of p.
  2. Commutators. For translations T_u, T_v (u, v in U/Z = F_3^2): [T_u, T_v] = t_p^(c omega(u,v)), with omega the
     symplectic form and c a fixed unit. Two space translations commute only up to a tick of time, weighted by their
     symplectic area.
  3. H/U = 2 x Q8 (16 elements; orders 1:1, 2:3, 4:12), and H/Z(H) = 3^2 : Q8 (72 elements; orders 1:1, 2:9, 3:8,
     4:54; no order 8), Q8 acting freely on F_3^2. Choosing one of the three clock involutions at p (the three tick
     lines) breaks the point's SL(2,3) (binary tetrahedral) to Q8 (the quaternion units +-1, +-i, +-j, +-k).
  4. Orbits of H on the 40 points: 1 + 12 + 27 (the event p, its neighbours, the far points). U acts REGULARLY on the
     27 far points, so they form a Heisenberg torsor -- two space coordinates (F_3^2) and one time coordinate (F_3). U
     acts on the 12 neighbours in orbits of 3, one along each line through p.
Reading. In the one-time real form, the symmetry group is a finite analogue of the centrally extended (Bargmann)
Galilei group with spin. The central charge is not mass but TIME: the tick that chose the real form is the
commutator of space translations. Spin rotations are the quaternion group. The 27 events not collinear with p are
the Heisenberg spacetime of p.
Prior art (classical, cited): W(q) is an elation generalized quadrangle. Its elation group about a base point is the
Heisenberg group q^{1+2}; it acts regularly on the q^3 non-collinear points, and its centre is the group of symmetries
about the point (Payne-Thas, Finite Generalized Quadrangles, ch. 8; Kantor). The point stabiliser of Sp(4,q) is the
Jacobi group of a qudit. New here: through 12052-12053, the elation centre IS the tick that fixes the clock real form;
the real form's symmetry group is the elation group extended by +-1 x Q8; and the tick-line choice breaks SL(2,3) to Q8.
Scope: finite-group statements; the physical reading (Galilei, spacetime) is an interpretation, not a derivation of
continuum kinematics.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup, sp43_from_ticks  # noqa: E402

OUT = ROOT / "data" / "w33_pass12058_time_is_the_heisenberg_centre.json"


def main():
    checks, res = {}, {}
    Adj, invs, tick, fib = setup()
    G = sp43_from_ticks(tick)
    cl = next(s for k, s in invs if k == "clock")
    even = [x for x in range(40) if not cl[fib[x]].any()]
    p = next(x for x in range(40) if set(np.nonzero(Adj[x])[0]) == set(even))
    H = [h.astype(np.int64) for h in G[np.all(cl[G] == cl[None, :], axis=1)]]
    idn = np.arange(240)
    key = lambda g: g.astype(np.int16).tobytes()  # noqa: E731
    inv = lambda g: np.argsort(g)  # noqa: E731

    def order(h):
        g, n = h.copy(), 1
        while not np.array_equal(g, idn):
            g = g[h]
            n += 1
        return n

    def order_mod(h, S):
        g, n = h.copy(), 1
        while key(g) not in S:
            g = g[h]
            n += 1
        return n
    comm = lambda a, b: a[b[inv(a)[inv(b)]]]  # noqa: E731
    U = [h for h in H if order(h) in (1, 3, 9)]
    Uk = {key(u) for u in U}
    tp = tick[p].astype(np.int64)
    tps = {key(idn), key(tp), key(tp[tp])}
    ZU = {key(u) for u in U if all(np.array_equal(u[v], v[u]) for v in U)}
    commU = {key(comm(a, b)) for a in U for b in U}
    res["U"] = dict(order=len(U), orders=dict(Counter(order(u) for u in U)), centre_is_tick=ZU == tps, derived_is_tick=commU == tps)
    checks["U = 3-elements: 27, normal, exponent 3, nonabelian; Z(U) = [U,U] = <t_p> (Heisenberg, centre = tick)"] = bool(
        len(U) == 27 and all(key(a[b]) in Uk for a in U for b in U) and all(key(g[u[inv(g)]]) in Uk for g in H for u in U)
        and max(order(u) for u in U) == 3 and ZU == tps and commU == tps)

    reps = [u for u in U if key(u) not in tps]
    u1 = reps[0]
    u2 = next(u for u in reps if key(comm(u1, u)) != key(idn))

    def coords(u):
        for i in range(3):
            for j in range(3):
                g = idn.copy()
                for _ in range(i):
                    g = g[u1]
                for _ in range(j):
                    g = g[u2]
                for z in (idn, tp, tp[tp]):
                    if np.array_equal(g[z], u):
                        return i, j
        return None
    tpow = lambda c: 0 if key(c) == key(idn) else (1 if key(c) == key(tp) else 2)  # noqa: E731
    c12 = tpow(comm(u1, u2))
    ok = all(tpow(comm(a, b)) == (c12 * (coords(a)[0] * coords(b)[1] - coords(a)[1] * coords(b)[0])) % 3 for a in U for b in U)
    res["commutator_unit"] = c12
    checks["[T_u, T_v] = t_p^(c omega(u,v)) for all 27 x 27 pairs (time = symplectic area)"] = bool(ok and c12 in (1, 2))

    cosU, seen = [], set()
    for h in H:
        if key(h) in seen:
            continue
        cosU.append(h)
        seen |= {key(h[u]) for u in U}
    ordHU = dict(sorted(Counter(order_mod(h, Uk) for h in cosU).items()))
    cen = [h for h in H if all(np.array_equal(h[g], g[h]) for g in H)]
    Zk = {key(z) for z in cen}
    cosZ, seenZ = [], set()
    for h in H:
        if key(h) in seenZ:
            continue
        cosZ.append(h)
        seenZ |= {key(h[z]) for z in cen}
    ordHZ = dict(sorted(Counter(order_mod(h, Zk) for h in cosZ).items()))
    res["H_mod_U_orders"], res["H_mod_Z_orders"] = ordHU, ordHZ
    checks["H/U = 2 x Q8 (orders 1:1, 2:3, 4:12) and H/Z(H) = 3^2:Q8 (orders 1:1, 2:9, 3:8, 4:54)"] = bool(
        len(cosU) == 16 and ordHU == {1: 1, 2: 3, 4: 12} and len(cosZ) == 72 and ordHZ == {1: 1, 2: 9, 3: 8, 4: 54})

    pt_of = np.empty(240, int)
    for q, f in enumerate(fib):
        pt_of[f] = q
    on = lambda h: pt_of[h[[f[0] for f in fib]]]  # noqa: E731
    orbs, seen_p = [], set()
    for q in range(40):
        if q in seen_p:
            continue
        o = {int(on(h)[q]) for h in H}
        seen_p |= o
        orbs.append(len(o))
    far = [x for x in range(40) if x != p and not Adj[p, x]]
    regular = len({int(on(u)[far[0]]) for u in U}) == 27
    nb_orbits = sorted(Counter(len({int(on(u)[q]) for u in U}) for q in np.nonzero(Adj[p])[0]).items())
    res["orbits"] = dict(H=sorted(orbs), U_far_regular=regular, U_on_neighbours=nb_orbits)
    checks["H-orbits 1 + 12 + 27; U regular on the 27 far points (Heisenberg torsor); U-orbits of 3 on the neighbours"] = bool(
        sorted(orbs) == [1, 12, 27] and regular and nb_orbits == [(3, 12)])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
