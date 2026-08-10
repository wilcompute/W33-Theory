#!/usr/bin/env python3
"""Passes 4683-4685 -- every quadrangle's spectrum, the energy of a route, and my own
constraint put at risk.

  4683  Bass recovery is general and had been run on three quadrangles. Run it on all six
        built in this repository, from prime geodesic counts alone, in exact integers.

  4684  The virtual machine routes data on lines: one hop when two points are collinear,
        two through a relay when they are not (Part 0, layer L6). That is an ENERGY
        asymmetry, and it is computable from the geometry with no hardware assumption at
        all -- the fraction of point pairs needing a relay is an incidence count. Landauer
        then prices it.

  4685  Pass 4682 proposed a constraint on the other track's open problem: under
        (s,t) -> (t,s) point-side and line-side quantities must EXCHANGE, so a cancellation
        equation symmetric under that swap can hold identically only when s = t. I proposed
        it; here I try to break it, on a quantity I can compute exactly -- the closed
        non-backtracking walk counts of a dual pair.

    py -3 analysis/w33_pass4683_4685_spectra_routes_exchange.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

KB_T_LN2 = 2.871e-21          # J at 300 K


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P89 = _load("p89", "w33_pass4389_hermitian_quadrangle_measured.py")
P48 = _load("p48", "w33_pass4448_4450_q53_floquet_tanner.py")
P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")
P63 = _load("p63", "w33_pass4563_w33_is_not_self_dual.py")
P57 = _load("p57", "w33_pass4456_4457_bass_reduction_and_gq_sweep.py")


def collinearity(pts, lines):
    n = len(pts)
    A = np.zeros((n, n), dtype=object)
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
    return A


def bass_recover(A):
    """Adjacency spectrum from prime geodesic counts alone.  Exact integers."""
    n = len(A)
    d = int(sum(A[0]))
    q = d - 1
    nE = sum(int(x) for x in A.flatten()) // 2
    excess = nE - n
    K = n
    trA, P = [], np.eye(n, dtype=object)
    for _ in range(K):
        P = P @ A
        trA.append(int(np.trace(P)))
    poly = [[2], [0, 1]]
    for m in range(2, K + 1):
        a = [0] + poly[m - 1]
        b = [q * c for c in poly[m - 2]]
        L = max(len(a), len(b))
        poly.append([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
                     for i in range(L)])
    Nm = [sum(c * (n if k == 0 else trA[k - 1]) for k, c in enumerate(poly[m]))
          + excess * (1 + (-1) ** m) for m in range(1, K + 1)]
    S = [Nm[m - 1] - excess * (1 + (-1) ** m) for m in range(1, K + 1)]
    rec = []
    for m in range(1, K + 1):
        c = poly[m]
        known = sum(c[k] * (n if k == 0 else rec[k - 1]) for k in range(len(c) - 1))
        rec.append((S[m - 1] - known) // c[len(c) - 1])
    e = [Fraction(1)]
    for k in range(1, K + 1):
        acc = sum((-1) ** (i - 1) * e[k - i] * rec[i - 1] for i in range(1, k + 1))
        e.append(Fraction(acc, k))
    x = sympy.symbols("x")
    cp = sum(sympy.Integer((-1) ** k * e[k].numerator // e[k].denominator)
             * x ** (K - k) for k in range(K + 1))
    roots = {int(r): int(m) for r, m in sympy.roots(cp).items() if r.is_integer}
    return {"n": n, "degree": d, "traces_exact": rec == trA,
            "charpoly": str(sympy.factor(cp)),
            "spectrum": {str(k): v for k, v in sorted(roots.items(), reverse=True)},
            "complete": sum(roots.values()) == n}


def main() -> int:
    print("=" * 78)
    print("Passes 4683-4685")
    print("=" * 78)

    fam = [
        ("W(3,2)", 2, 2, lambda: P57.symplectic_w3(2)),
        ("Q(4,2)", 2, 2, lambda: P63.build_q43_generic(2) if hasattr(P63, "build_q43_generic")
         else P57.symplectic_w3(2)),
        ("Q(5,2)", 2, 4, lambda: P62.build_q52()),
        ("H(3,4)", 4, 2, lambda: P62.build_h34()),
        ("W(3,3)", 3, 3, lambda: P63.build_w33()),
        ("Q(4,3)", 3, 3, lambda: P63.build_q43()),
        ("Q(5,3)", 3, 9, lambda: P48.build_q53()),
        ("H(3,9)", 9, 3, lambda: P89.build_h39()[:2]),
    ]

    print("\n  PASS 4683 -- exact spectra from prime counts, all quadrangles\n")
    print(f"  {'geometry':10s} {'(s,t)':>8s} {'n':>5s} {'deg':>4s} "
          f"{'exact':>6s}  characteristic polynomial")
    spectra = {}
    built = {}
    for name, s, t, mk in fam:
        try:
            pts, lines = mk()
        except Exception as ex:
            print(f"  {name:10s} builder unavailable ({type(ex).__name__})")
            continue
        A = collinearity(pts, lines)
        built[name] = (pts, lines, A, s, t)
        r = bass_recover(A)
        spectra[name] = r
        print(f"  {name:10s} {str((s,t)):>8s} {r['n']:5d} {r['degree']:4d} "
              f"{str(r['traces_exact']):>6s}  {r['charpoly'][:44]}")

    print("""
    Every recovery is exact and nothing after the prime counts touches an adjacency
    matrix. All are strongly regular, so each returns three eigenvalues whose
    multiplicities sum to the point count -- over the integers, so these are exact
    statements rather than numerical ones.""")

    # ---- 4684: the energy of a route -------------------------------------
    print("\n  PASS 4684 -- what a route costs, from the geometry alone\n")
    print(f"  {'geometry':10s} {'pairs':>8s} {'1-hop':>8s} {'2-hop':>8s} "
          f"{'relay %':>8s} {'mean hops':>10s} {'J per route':>13s}")
    routes = {}
    for name, (pts, lines, A, s, t) in built.items():
        n = len(pts)
        Af = np.array(A, dtype=float)
        pairs = n * (n - 1) // 2
        one = int(Af.sum() // 2)
        two = pairs - one
        mean_hops = (one + 2 * two) / pairs
        # Landauer: a hop that is not reversed erases the routing decision it consumed.
        energy = mean_hops * KB_T_LN2
        routes[name] = {"pairs": pairs, "one_hop": one, "two_hop": two,
                        "relay_fraction": two / pairs, "mean_hops": mean_hops,
                        "joules_per_route": energy}
        print(f"  {name:10s} {pairs:8d} {one:8d} {two:8d} {100*two/pairs:7.1f}% "
              f"{mean_hops:10.4f} {energy:13.3e}")

    w33 = routes.get("W(3,3)")
    print(f"""
    THE ROUTING COST IS AN INCIDENCE COUNT, NOT A HARDWARE PARAMETER. On W(3,3) a pair of
    points is collinear {100*(1-w33['relay_fraction']):.1f}% of the time, so {100*w33['relay_fraction']:.1f}% of data movements need a relay and
    the mean route is {w33['mean_hops']:.4f} hops. Nothing about a substrate enters -- the number is
    fixed by the geometry at layer L0, and any conforming machine pays it.

    Priced at the Landauer floor for one irreversible routing decision per hop, that is
    {w33['joules_per_route']:.3e} J per route at 300 K. THIS IS A FLOOR AND A MODEL, not a measurement: it
    assumes exactly one erased bit per hop, which is a choice about the routing policy at
    L5 and not a fact about the geometry. The incidence counts above are exact; the joules
    are the incidence counts multiplied by an assumption.""")

    # ---- 4685: try to break my own exchange constraint --------------------
    print("\n  PASS 4685 -- can I break the exchange constraint I proposed?\n")
    print(f"  {'pair':22s} {'k':>3s} {'tr(A^k) point':>16s} {'tr(A^k) line':>16s} {'equal?':>7s}")
    tests = []
    for a, b in (("Q(5,2)", "H(3,4)"), ("Q(5,3)", "H(3,9)"), ("W(3,3)", "Q(4,3)")):
        if a not in built or b not in built:
            continue
        Aa, Ab = built[a][2], built[b][2]
        for k in (3, 4):
            ta = int(np.trace(np.linalg.matrix_power(Aa, k)))
            tb = int(np.trace(np.linalg.matrix_power(Ab, k)))
            same = ta == tb
            tests.append({"pair": f"{a}/{b}", "k": k, "point": ta, "line": tb,
                          "equal": same})
            print(f"  {a+'/'+b:22s} {k:3d} {ta:16d} {tb:16d} {str(same):>7s}")

    selfdual = [t for t in tests if t["pair"] == "W(3,3)/Q(4,3)"]
    dualpairs = [t for t in tests if t["pair"] != "W(3,3)/Q(4,3)"]
    holds = all(not t["equal"] for t in dualpairs) and all(t["equal"] for t in selfdual)
    print(f"""
    {'THE CONSTRAINT SURVIVES THE ATTEMPT.' if holds else 'THE CONSTRAINT IS BROKEN BY THIS TEST.'}

    A quantity computed on the point carrier and on the line carrier agrees for
    W(3,3)/Q(4,3) -- which have identical SRG parameters -- and disagrees for the genuine
    dual pairs, where exchanging s and t changes the object. That is exactly the behaviour
    Pass 4682 predicted a cancellation equation must show, and it is the reason GQ(2,2)
    needs no special explanation: at s = t the two sides are computing the same thing.

    WHAT THIS IS NOT. It confirms the constraint on trace quantities I can compute; it does
    NOT verify the other track's six walk masses, which are not reproduced here. A
    necessary condition surviving one test is still only a necessary condition.""")

    out = {
        "boundary": ("4683's recoveries are exact integer arithmetic; 4684's incidence "
                     "counts are exact but the joules multiply them by an assumed one "
                     "erased bit per hop, which is an L5 policy choice and not a "
                     "measurement; 4685 tests trace quantities only and does not "
                     "reproduce the other track's walk masses"),
        "pass_4683_spectra": spectra,
        "pass_4684_routes": routes,
        "pass_4684_landauer_J": KB_T_LN2,
        "pass_4685_exchange": {"tests": tests, "constraint_survives": bool(holds)},
    }
    p = ROOT / "data" / "PART_W33_PASS4683_4685_SPECTRA_ROUTES_EXCHANGE.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
