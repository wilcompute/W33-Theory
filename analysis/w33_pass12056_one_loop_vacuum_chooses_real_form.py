"""Pass 12056: the one-loop vacuum chooses the real form. The vacua that the corpus's E8 Higgs computations select
(11884-11892) sit, at root level, inside the maximal compact subalgebra of exactly one real form: the trinification
point vacuum (bosonic loops) inside the clock form E8(-24) at that point, and the factorisation vacuum (periodic adjoint
fermions in the gauge-Higgs completion) inside the split form E8(8) (Claude track; continues 12052-12055).

Root model (12052). The fibre over a point p is an Eisenstein line {+-a, +-wa, +-w^2 a}, an A2 subsystem A2(p).
  * E6(p): the roots orthogonal to A2(p). They are exactly the fibres over the 12 points collinear with p (72 roots,
    checked to be an E6 system: closed, rank 6). So E8 > E6(p) x A2(p) at every point -- the corpus dictionary "a point
    of W(3,3) is E6 x SU(3)" (11887-11889; Pauli centraliser of a point).
  * D4(H): the fibres over the four points of a hyperbolic line H are a D4 system (24 roots, rank 4). A tensor
    factorisation H1 + H2 gives D4(H1) + D4(H2), the corpus's "factorisation -> D4 x D4" centraliser.
Theorem (exact). For an inner involution theta_h, the maximal compact subalgebra k contains the Cartan plus the even
roots.
  (a) Point vacuum. The trinification vev at the Witting ray p has centraliser e6(p) + h, with the family A2(p) broken to
      its Cartan (11887). Among the 255 involutions, the ones whose k contains e6(p) + h are EXACTLY the three clock
      involutions at p. Each also contains one su(2) in A2(p), one per tick line. No split involution does.
  (b) Factorisation vacuum. The ones whose k contains d4(H1) + d4(H2) + h are EXACTLY the three split involutions at
      that factorisation. No clock involution does.
Reading. The corpus vacuum phase diagram (11890-11892) says which vacuum the matter selects: bosonic Coleman-Weinberg
loops give a W(3,3) point (trinification), and periodic adjoint fermions in the Hosotani completion give a tensor
factorisation. By the theorem, these are the anchors of E8(-24) and E8(8). So the one-loop dynamics chooses the real
form: bosonic loops choose one time (the clock form, anchored at the selected point, where the tick of that point is
central -- 12053); periodic adjoint fermions choose the split form. This is the action behind 12054-12055's
condensate: the Coleman-Weinberg potential of the E8 Higgs.
Scope: root-level containment (k contains the vev centraliser's roots and Cartan) in the root model of 12052; the
identification of the corpus vacua with E6(p) x A2(p) and D4 x D4 is the corpus's dictionary (11887-11892), not
re-derived in the sl9 + Lambda^3 model here. Charged fermions are not included in the bosonic vacuum (as in 11884).
Not new: E8 > E6 x A2 and > D4 x D4 (Borel-de Siebenthal); real forms of E8; the corpus vacua and dictionary.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12052_real_forms_on_forty_points import build  # noqa: E402

OUT = ROOT / "data" / "w33_pass12056_one_loop_vacuum_chooses_real_form.json"


def root_system_rank_closed(roots):
    S = {tuple(np.round(r * 2).astype(int)) for r in roots}
    closed = all(tuple(np.round((a + b) * 2).astype(int)) in S for a in roots for b in roots
                 if abs(a @ b + 1) < 1e-9)       # a + b is a root of E8 iff <a,b> = -1; closure inside the subset
    return int(np.linalg.matrix_rank(np.array(roots))), bool(closed)


def main():
    checks, res = {}, {}
    R, C, fib, refl, perm = build()
    IP = R @ R.T
    Adj = np.array([[int(p != q and np.all(np.abs(IP[np.ix_(fib[p], fib[q])]) < 1e-9)) for q in range(40)] for p in range(40)])
    inv = {}
    for h in list(R) + [R[i] + R[j] for i in range(240) for j in range(i + 1, 240) if abs(IP[i, j]) < 1e-9]:
        inv.setdefault(tuple(((np.round(R @ h).astype(int)) % 2).tolist()), h)
    invs = []
    for sig in inv:
        s = np.array(sig, bool)
        even = ~s
        kind = "clock" if 8 + even.sum() == 136 else "split"
        n0 = frozenset(x for x in range(40) if even[fib[x]].all())
        invs.append((kind, even, n0))

    # E6(p) and A2(p)
    p = 0
    a2 = fib[p]
    perp_roots = [i for i in range(240) if all(abs(IP[i, j]) < 1e-9 for j in a2)]
    nb = list(np.nonzero(Adj[p])[0])
    nb_roots = sorted(i for q in nb for i in fib[q])
    rk, cl = root_system_rank_closed([R[i] for i in perp_roots])
    rk2, cl2 = root_system_rank_closed([R[i] for i in a2])
    res["E6p"] = dict(n_roots=len(perp_roots), rank=rk, closed=cl, equals_neighbour_fibres=sorted(perp_roots) == nb_roots)
    res["A2p"] = dict(n_roots=len(a2), rank=rk2, closed=cl2)
    checks["E6(p) = roots orthogonal to the fibre = the 12 neighbour fibres (72 roots, rank 6, closed); A2(p) = fibre"] = bool(
        len(perp_roots) == 72 and rk == 6 and cl and sorted(perp_roots) == nb_roots and len(a2) == 6 and rk2 == 2 and cl2)

    # D4(H1) + D4(H2) for a factorisation
    split_n0 = next(n0 for k, e, n0 in invs if k == "split")
    F = sorted(split_n0)
    sub = Adj[np.ix_(F, F)]
    H1 = [F[0]] + [F[j] for j in range(1, 8) if not sub[0, j]]
    H2 = [x for x in F if x not in H1]
    d1 = [R[i] for q in H1 for i in fib[q]]
    d2 = [R[i] for q in H2 for i in fib[q]]
    r1, c1 = root_system_rank_closed(d1)
    r2, c2 = root_system_rank_closed(d2)
    orth = all(abs(a @ b) < 1e-9 for a in d1 for b in d2)
    res["D4D4"] = dict(sizes=[len(d1), len(d2)], ranks=[r1, r2], closed=[c1, c2], mutually_orthogonal=orth)
    checks["factorisation fibres = D4(H1) + D4(H2): 24 + 24 roots, rank 4 each, closed, mutually orthogonal"] = bool(
        len(d1) == 24 and len(d2) == 24 and r1 == 4 and r2 == 4 and c1 and c2 and orth)

    # containment theorem, for every point and every factorisation
    pt_ok, fac_ok = True, True
    point_counts, fac_counts = [], []
    for q in range(40):
        e6 = [i for i in range(240) if all(abs(IP[i, j]) < 1e-9 for j in fib[q])]
        cont = [(k, n0) for k, e, n0 in invs if e[e6].all()]
        point_counts.append(Counter_kinds(cont))
        pt_ok &= sorted(k for k, _ in cont) == ["clock"] * 3 and all(n0 == frozenset(np.nonzero(Adj[q])[0]) for _, n0 in cont)
    facs = sorted({n0 for k, e, n0 in invs if k == "split"}, key=sorted)
    for Fs in facs:
        roots_F = [i for q in Fs for i in fib[q]]
        cont = [(k, n0) for k, e, n0 in invs if e[roots_F].all()]
        fac_counts.append(Counter_kinds(cont))
        fac_ok &= sorted(k for k, _ in cont) == ["split"] * 3 and all(n0 == Fs for _, n0 in cont)
    res["point_vacuum_containment"] = point_counts[0]
    res["factorisation_vacuum_containment"] = fac_counts[0]
    res["n_points_checked"], res["n_factorisations_checked"] = 40, len(facs)
    checks["(a) for all 40 points: k contains e6(p)+h for exactly the 3 clock involutions at p (no split one)"] = bool(pt_ok)
    checks["(b) for all 45 factorisations: k contains d4+d4+h for exactly the 3 split involutions there (no clock one)"] = bool(fac_ok and len(facs) == 45)
    # each clock involution at p contains exactly one root pair of A2(p): one su(2) per tick line
    pairs = []
    for k, e, n0 in invs:
        if k == "clock" and n0 == frozenset(nb):
            pairs.append(int(e[a2].sum()))
    res["A2p_even_roots_per_clock_involution"] = pairs
    checks["each clock involution at p keeps exactly one su(2) of the family A2(p) (2 even roots)"] = bool(pairs == [2, 2, 2])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


def Counter_kinds(cont):
    out = {"clock": 0, "split": 0}
    for k, _ in cont:
        out[k] += 1
    return out


if __name__ == "__main__":
    main()
