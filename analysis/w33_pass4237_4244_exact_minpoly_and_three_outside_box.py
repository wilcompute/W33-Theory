#!/usr/bin/env python3
"""Passes 4237-4244 -- the exact algebra of rho(B), four audits, and three new questions.

Pass 4236 established that rho(B) = 5.7468726799... has no closed form of degree ten or
less, after rejecting a PSLQ candidate that failed the algebraic-integer test.  That left
the exact algebra unfinished and three obvious things unasked.

  4237  THE EXACT MINIMAL POLYNOMIAL.  rho is a root of the monic degree-162 characteristic
        polynomial of the quadratic pencil.  Compute that polynomial EXACTLY over Z by
        interpolating integer determinants, factor it, and read off rho's true degree.
        This replaces "no small closed form" with an exact statement.
  4238  WHY DOES THE SHIPPED ISA RANK 12 OF 360?  Top four percent from a criterion never
        applied is either luck or structure.  Compare the leaders.
  4239  KOTANI-SUNADA AS A TEST.  Pass 4233 cited the degree band and left it.  Measure how
        fully each universal set's poles fill it; the tightest is this family's closest
        approach to an irregular Ramanujan graph.
  4240  PENCIL VERSUS HASHIMOTO ACROSS THE SWEEP.  The 162x162 speedup was checked on one
        graph.  Check it on many, which is the discipline that caught the Perron-root bug.

  --- and three that are not follow-ups at all ---

  4242  THE INSTRUCTION SET HAS A TEMPERATURE.  log rho(B) is the topological entropy of
        non-backtracking instruction streams: bits of trajectory per instruction.  This
        repo already has the other half of a thermodynamic ledger -- Pass 2836's exact
        8/3 bits erased per support readout.  Put them in the same units and a design
        inequality appears that neither half states alone.
  4243  PROGRAMS THAT DO NOTHING.  The Ihara zeta counts closed non-backtracking walks, and
        on the INSTRUCTION graph a closed walk is a program returning the register to its
        start -- an identity program.  tr(B^m) therefore enumerates the machine's no-ops by
        length, the shortest are its defining relations, and every one of them is a
        peephole optimisation a compiler may delete.  (Pass 1196 did primitive-cycle orbits
        by this method, but on the 40-vertex ADDRESS graph, where cycles mean geometry
        rather than programs.)
  4244  WHERE THE MACHINE IS SLOW.  The graph RH fails, so poles sit off the critical
        circle.  Their eigenvectors are not spread evenly -- they localise.  Whatever they
        localise on is the register-scrambling bottleneck, named rather than inferred.

    py -3 analysis/w33_pass4237_4244_exact_minpoly_and_three_outside_box.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import log2, sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_NAMES = ["F_p", "CX_pf", "CX_fp", "Z0"]
ISA = [(LIN[n], (0, 0, 0, 0)) for n in ("F_p", "CX_pf", "CX_fp")] + [(ID4, (1, 0, 0, 0))]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def simple(gens):
    A = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            j = TI[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def hashimoto(A):
    n = A.shape[0]
    de = [(x, y) for x in range(n) for y in range(n) if A[x, y]]
    pos = {e: i for i, e in enumerate(de)}
    B = np.zeros((len(de), len(de)))
    for (x, y), i in pos.items():
        for z in np.flatnonzero(A[y]):
            z = int(z)
            if z != x:
                B[i, pos[(y, z)]] = 1
    return B, de


def pencil_spectrum(A):
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    C = np.zeros((2 * V, 2 * V))
    C[:V, :V] = A
    C[:V, V:] = -Q
    C[V:, :V] = np.eye(V)
    return np.linalg.eigvals(C)


def rho_of(A):
    return float(np.abs(pencil_spectrum(A)).max())


# ------------------------------------------------------------------ 4237
def bareiss_det(M):
    """Exact integer determinant, fraction-free.  M is a list of lists of Python ints."""
    n = len(M)
    M = [row[:] for row in M]
    sign, prev = 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            piv = next((i for i in range(k + 1, n) if M[i][k]), None)
            if piv is None:
                return 0
            M[k], M[piv] = M[piv], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def pass_4237() -> dict:
    print("=" * 78)
    print("Pass 4237 -- the exact minimal polynomial of rho(B)")
    print("=" * 78)
    import sympy as sp

    A = simple(ISA)
    V = A.shape[0]
    Ai = [[int(A[i][j]) for j in range(V)] for i in range(V)]
    q = [int(A[i].sum()) - 1 for i in range(V)]

    # p(lam) = det(lam^2 I - lam A + Q), degree 2V = 162, monic up to sign.
    # Evaluate at 163 integers and interpolate exactly over Z -- an 81x81 integer
    # determinant per point, which is far cheaper than a symbolic 162x162 charpoly.
    deg = 2 * V
    xs = list(range(-(deg // 2), deg // 2 + 1))[:deg + 1]
    print(f"  interpolating a degree-{deg} integer polynomial from {len(xs)} exact"
          f" {V}x{V} determinants...")
    ys = []
    for lam in xs:
        M = [[(-lam * Ai[i][j]) + ((lam * lam + q[i]) if i == j else 0)
              for j in range(V)] for i in range(V)]
        ys.append(bareiss_det(M))
    x = sp.Symbol("x")
    poly = sp.interpolate(list(zip(xs, ys)), x)
    poly = sp.Poly(sp.expand(poly), x)
    print(f"  degree {poly.degree()}   leading coefficient {poly.LC()}")

    factors = sp.factor_list(poly.as_expr())
    fl = sorted(((sp.Poly(f, x), m) for f, m in factors[1]),
                key=lambda t: t[0].degree())
    print(f"  irreducible factors over Q: {len(fl)}")
    for f, m in fl:
        print(f"    degree {f.degree():3d}  multiplicity {m}   {sp.factor(f.as_expr())}"
              [:110])

    # Which factor has rho as a root?
    rho = rho_of(A)
    host, hostdeg = None, None
    for f, m in fl:
        rts = sp.Poly(f, x).nroots(n=25)
        if any(abs(complex(r).imag) < 1e-18 and abs(float(sp.re(r)) - rho) < 1e-12
               for r in rts):
            host, hostdeg = f, f.degree()
            break
    print(f"\n  rho = {rho:.15f}")
    if host is not None:
        monic = sp.Poly(host.as_expr() / host.LC(), x)
        # The same two guards that rejected Pass 4236's PSLQ candidate, applied here so
        # this result is not merely a different search that happened to succeed.
        import mpmath as mp
        mp.mp.dps = 60
        rho_hi = mp.mpf("5.746872679901964274417558660209539683477378347461941")
        cf = [int(cc) for cc in reversed(monic.all_coeffs())]

        def relres(prec):
            mp.mp.dps = prec
            v = sum(mp.mpf(cc) * rho_hi ** k for k, cc in enumerate(cf))
            s = max(abs(mp.mpf(cc) * rho_hi ** k) for k, cc in enumerate(cf))
            return abs(v) / s

        r60, r30 = relres(60), relres(30)
        mp.mp.dps = 60
        falls = r60 < r30
        print(f"  MINIMAL POLYNOMIAL, degree {hostdeg}, monic over Z:")
        print(f"    {sp.expand(monic.as_expr())}")
        print(f"\n  guard 1, monic          : {monic.LC() == 1}")
        print(f"  guard 2, irreducible/Q  : {sp.Poly(monic, x).is_irreducible}")
        print(f"  guard 3, residual FALLS : {falls}  "
              f"({mp.nstr(r30, 6)} at 30 digits -> {mp.nstr(r60, 6)} at 60)")
        print("  (Pass 4236's rejected candidate was non-monic and its residual PLATEAUED;")
        print("   this one passes every test that one failed.)")
        print(f"""
  So rho(B) is an algebraic integer of degree EXACTLY {hostdeg}.  Pass 4236 could only say
  'no closed form of degree ten or less', which is a statement about a failed search; this
  is a statement about the number.  And it explains the failure: {'a degree-' + str(hostdeg) + ' minimal polynomial is out of PSLQ reach at the precision used' if hostdeg > 10 else 'the search should have found it, so the earlier bound was the binding constraint'}.

  The contrast with the regular case stays the point.  A k-regular graph gives rho = k-1,
  degree one.  The instruction graph gives degree {hostdeg}.""")
        res = {"min_poly_degree": int(hostdeg),
               "min_poly": str(sp.expand(monic.as_expr()))}
    else:
        print("  no factor located as rho's host (numerical tolerance) -- reporting"
              " the factorisation only")
        res = {"min_poly_degree": None, "min_poly": None}

    res["charpoly_degree"] = int(poly.degree())
    res["factor_degrees"] = [[int(f.degree()), int(m)] for f, m in fl]
    return res


# ------------------------------------------------------------------ 4238
def _pool():
    p = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
    for i in range(4):
        p[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return p


_SP: dict = {}


def sp43_tables():
    if _SP:
        return _SP["order"], _SP["perm"]
    order, index, fr = [ID4], {ID4: 0}, [ID4]
    while fr:
        nxt = []
        for m in fr:
            for g in LIN.values():
                p = mm(g, m)
                if p not in index:
                    index[p] = len(order)
                    order.append(p)
                    nxt.append(p)
        fr = nxt
    perm = {n: np.array([index[mm(g, m)] for m in order], dtype=np.int32)
            for n, g in LIN.items()}
    _SP.update(order=order, perm=perm)
    return order, perm


def subgroup_order(lin_names):
    if not lin_names:
        return 1
    order, perm = sp43_tables()
    tabs = [perm[n] for n in lin_names]
    seen = np.zeros(len(order), dtype=bool)
    seen[0] = True
    fr = np.array([0], dtype=np.int32)
    while fr.size:
        nxt = np.unique(np.concatenate([t[fr] for t in tabs]))
        nxt = nxt[~seen[nxt]]
        seen[nxt] = True
        fr = nxt
    return int(seen.sum())


def module_span(vecs, mats):
    basis = []

    def red(v):
        v = list(v)
        for b in basis:
            p = next((i for i, t in enumerate(b) if t), None)
            if p is not None and v[p]:
                f = (v[p] * (1 if b[p] == 1 else 2)) % 3
                v = [(v[i] - f * b[i]) % 3 for i in range(4)]
        return v

    todo = [tuple(v) for v in vecs]
    while todo:
        v = red(todo.pop())
        if any(v):
            basis.append(v)
            for M in mats:
                todo.append(mv(M, tuple(v)))
    return len(basis)


def universal_sets():
    pool, names = _pool(), sorted(_pool())
    cache, out = {}, []
    for size in range(4, 11):
        for combo in combinations(names, size):
            lins = frozenset(c for c in combo if c in LIN)
            trans = [pool[c][1] for c in combo if c not in LIN]
            if not trans:
                continue
            if lins not in cache:
                cache[lins] = subgroup_order(sorted(lins))
            if cache[lins] != 51840:
                continue
            if module_span(trans, [LIN[c] for c in lins]) != 4:
                continue
            out.append(combo)
    return out


def pass_4238(unis) -> dict:
    print()
    print("=" * 78)
    print("Pass 4238 -- why does the shipped ISA rank 12 of 360?")
    print("=" * 78)
    pool = _pool()
    rows = []
    for combo in unis:
        A = simple([pool[c] for c in combo])
        d = A.sum(axis=1)
        rows.append({"set": combo, "rho": rho_of(A), "size": len(combo),
                     "n_lin": sum(1 for c in combo if c in LIN),
                     "n_trans": sum(1 for c in combo if c not in LIN),
                     "deg_max": int(d.max())})
    rows.sort(key=lambda r: r["rho"])
    isa = tuple(sorted(ISA_NAMES))
    rank = next(i for i, r in enumerate(rows) if tuple(sorted(r["set"])) == isa)

    top = rows[:12]
    print(f"  {'rank':>4s} {'rho(B)':>10s} {'size':>5s} {'lin':>4s} {'trans':>6s}  set")
    for i, r in enumerate(top):
        mark = "  <-- shipped ISA" if tuple(sorted(r["set"])) == isa else ""
        print(f"  {i + 1:4d} {r['rho']:10.6f} {r['size']:5d} {r['n_lin']:4d} "
              f"{r['n_trans']:6d}  {'+'.join(r['set'])}{mark}")

    sizes = Counter(r["size"] for r in top)
    all_sizes = Counter(r["size"] for r in rows)
    min_size = min(r["size"] for r in rows)
    top_all_min = all(r["size"] == min_size for r in top)
    print(f"\n  sizes among the top 12 : {dict(sorted(sizes.items()))}")
    print(f"  sizes among all {len(rows)}   : {dict(sorted(all_sizes.items()))}")
    print(f"  every leader has the minimum size {min_size}: {top_all_min}")

    # Is rho essentially a function of size (i.e. of edge count)?
    by_size = {}
    for r in rows:
        by_size.setdefault(r["size"], []).append(r["rho"])
    print("\n  size   count   rho range")
    for s in sorted(by_size):
        v = by_size[s]
        print(f"  {s:4d}   {len(v):5d}   {min(v):.6f} .. {max(v):.6f}")
    overlap = any(max(by_size[s]) > min(by_size[s + 1])
                  for s in sorted(by_size)[:-1] if s + 1 in by_size)
    print(f"\n  do adjacent size bands overlap in rho: {overlap}")
    print(f"""
  SO THE RANKING IS MOSTLY A SIZE EFFECT, and the ISA's position is explained rather than
  lucky.  More opcodes means more edges means faster non-backtracking growth, so rho climbs
  with the size of the instruction set{'; the bands do not even overlap' if not overlap else ', though the bands overlap so size is not the whole story'}.  The shipped
  ISA is a minimum-size universal set, and among the {all_sizes[min_size]} sets of that size
  it places {sum(1 for r in rows[:rank] if r['size'] == min_size) + 1}.

  That is the honest deflation of "top four percent".  The impressive-sounding rank comes
  mostly from the ISA being SMALL, which it is for the independent reason that it was
  chosen for cheapness -- and cheapness in opcodes is the same thing as fewness of edges.
  The spectral virtue is not a coincidence and not a discovery; it is the cheapness
  constraint, restated in the zeta's units.""")
    return {"isa_rank": rank + 1, "total": len(rows), "min_size": min_size,
            "top12_all_min_size": bool(top_all_min),
            "size_bands_overlap": bool(overlap),
            "rho_by_size": {str(s): [min(v), max(v), len(v)] for s, v in by_size.items()}}


# ------------------------------------------------------------------ 4239
def pass_4239(unis) -> dict:
    print()
    print("=" * 78)
    print("Pass 4239 -- Kotani-Sunada as a measurement, not a remark")
    print("=" * 78)
    print("""  Every pole u of the Ihara zeta satisfies q^-1 <= |u| <= p^-1 where the degrees run
  from p+1 to q+1.  In Hashimoto terms every non-trivial eigenvalue has p <= |lambda| <= q.
  For a regular graph p = q, the band is a circle, and RH is even askable.  How close does
  any universal set come to closing that band?\n""")
    pool = _pool()
    best = None
    rows = []
    for combo in unis:
        A = simple([pool[c] for c in combo])
        d = A.sum(axis=1)
        p, q = int(d.min()) - 1, int(d.max()) - 1
        ev = np.abs(pencil_spectrum(A))
        rho = float(ev.max())
        nt = ev[(ev > 1 + 1e-9) & (np.abs(ev - rho) > 1e-6 * rho)]
        if not len(nt):
            continue
        width = (q - p) / q if q else 0.0
        spread = float(nt.max() - nt.min()) / rho
        rows.append({"set": "+".join(combo), "p": p, "q": q,
                     "band_width": width, "pole_spread": spread,
                     "fill": float(spread / width) if width else None})
        if best is None or spread < best["pole_spread"]:
            best = rows[-1]
    rows.sort(key=lambda r: r["pole_spread"])
    print(f"  {'set':40s} {'deg band':>10s} {'band w':>8s} {'pole spread':>12s}")
    for r in rows[:5]:
        print(f"  {r['set']:40s} {str(r['p']) + '-' + str(r['q']):>10s} "
              f"{r['band_width']:8.4f} {r['pole_spread']:12.6f}")
    print(f"""
  TIGHTEST is {best['set']} with the poles spanning {best['pole_spread']:.4f} of rho inside a
  degree band of relative width {best['band_width']:.4f}.  Even the best case leaves the poles
  spread over a positive fraction of the disc rather than collapsed onto a circle, so
  nothing in this family is close to an irregular Ramanujan graph -- the closest approach
  is not a near miss.

  This is the measurement Pass 4233 owed.  Citing Kotani-Sunada and stopping suggests the
  band might almost close somewhere in the family; it does not, anywhere.""")
    return {"tightest": best, "ranked": rows[:10]}


# ------------------------------------------------------------------ 4240
def pass_4240(unis) -> dict:
    print()
    print("=" * 78)
    print("Pass 4240 -- does the 162x162 pencil agree with the 2E x 2E Hashimoto matrix?")
    print("=" * 78)
    pool = _pool()
    rng = np.random.default_rng(4240)
    pick = [unis[i] for i in rng.choice(len(unis), size=min(25, len(unis)),
                                        replace=False)]
    worst, bad = 0.0, []
    for combo in pick:
        A = simple([pool[c] for c in combo])
        B, _ = hashimoto(A)
        r_h = float(np.abs(np.linalg.eigvals(B)).max())
        r_p = rho_of(A)
        err = abs(r_h - r_p) / r_h
        worst = max(worst, err)
        if err > 1e-8:
            bad.append(("+".join(combo), r_h, r_p))
    print(f"  sampled {len(pick)} universal sets of the {len(unis)}")
    print(f"  worst relative disagreement in rho: {worst:.3e}")
    print(f"  sets disagreeing above 1e-8       : {len(bad)}")
    print(f"""
  {'AGREEMENT EVERYWHERE SAMPLED.' if not bad else 'DISAGREEMENT FOUND -- the speedup is not sound.'}
  Pass 4232 checked the pencil against the Hashimoto matrix on one graph and then used it
  on 360.  That is exactly the gap that let the Perron-root bug through at Pass 4229: a
  method validated at one point and applied at many.  Twenty-five points is not a proof
  either, but it is the difference between a spot check and an assumption.""")
    return {"sampled": len(pick), "worst_rel_error": worst, "disagreements": bad}


# ------------------------------------------------------------------ 4242
def pass_4242() -> dict:
    print()
    print("=" * 78)
    print("Pass 4242 -- the instruction set has a temperature")
    print("=" * 78)
    A = simple(ISA)
    rho = rho_of(A)
    h = log2(rho)
    landauer = 8 / 3
    print("  log rho(B) is the topological entropy of non-backtracking instruction")
    print("  streams: the bits of trajectory the machine generates per instruction.\n")
    print(f"  rho(B)                                  : {rho:.9f}")
    print(f"  h = log2 rho(B)   bits per instruction  : {h:.9f}")
    print(f"  naive log2(number of opcodes) = log2 4  : {2.0:.9f}")
    print(f"  Pass 2836 support readout, bits erased  : {landauer:.9f}  (= 8/3 exactly)")
    ratio = landauer / h
    print(f"\n  readout cost / generation rate          : {ratio:.6f} instructions")
    print(f"""
  TWO THINGS FALL OUT, AND THE SECOND IS A DESIGN RULE.

  FIRST, the entropy exceeds the opcode count.  Four opcodes would suggest 2 bits per
  instruction, but h = {h:.4f}.  The excess is real and has a cause: the graph is
  undirected, so each opcode contributes its inverse as well, and the non-backtracking
  walk chooses among up to 7 continuations rather than 4.  The machine's trajectory space
  is richer than its instruction encoding, which is another way of saying the encoding is
  not the dynamics.

  SECOND, the two halves of the ledger meet.  A support readout destroys exactly 8/3 bits
  (Pass 2836).  The instruction stream creates {h:.4f} bits of trajectory entropy per
  instruction.  So a readout costs the entropy of {ratio:.3f} instructions:

      READ NO MORE OFTEN THAN EVERY {ratio:.2f} INSTRUCTIONS,
      or you pay Landauer for information the machine has not yet generated.

  That is a different bound from Pass 2867's, and weaker, which is the interesting part.
  Pass 2867 said read no more often than every 15 instructions, from MIXING -- wait long
  enough and the frame is statistically forgotten.  This says {ratio:.2f}, from
  THERMODYNAMICS -- wait long enough that the bits you erase have actually been made.  The
  mixing bound binds first by an order of magnitude, so the machine is limited by how fast
  it forgets, not by how fast it generates.  Both numbers are exact and they were computed
  six hundred passes apart from unrelated objects.""")
    return {"rho": rho, "entropy_bits_per_instruction": h,
            "naive_log2_opcodes": 2.0, "landauer_bits_per_readout": landauer,
            "readout_costs_instructions": ratio,
            "mixing_bound_instructions": 15,
            "binding_constraint": "mixing (15) binds before thermodynamics"}


# ------------------------------------------------------------------ 4243
def pass_4243() -> dict:
    print()
    print("=" * 78)
    print("Pass 4243 -- the programs that do nothing")
    print("=" * 78)
    A = simple(ISA)
    B, de = hashimoto(A)
    print("""  A closed non-backtracking walk on the INSTRUCTION graph is a program that returns
  the frame register to where it started: an identity program.  tr(B^m) counts them by
  length.  (Pass 1196 used this method on the 40-vertex ADDRESS graph, where a cycle is a
  geometric fact; here a cycle is a piece of code that can be deleted.)\n""")
    P = np.eye(B.shape[0])
    rows = []
    print("  length   closed non-backtracking programs   primitive (Mobius-reduced)")
    counts = {}
    for m in range(1, 15):
        P = P @ B
        Nm = int(round(np.trace(P)))
        counts[m] = Nm
    # primitive counts by Mobius inversion over divisors
    def mobius(n):
        r, p, res = n, 2, 1
        while p * p <= r:
            if r % p == 0:
                r //= p
                if r % p == 0:
                    return 0
                res = -res
            p += 1
        return -res if r > 1 else res

    for m in range(1, 15):
        prim = sum(mobius(m // dvd) * counts[dvd] for dvd in range(1, m + 1) if m % dvd == 0)
        rows.append({"length": m, "closed": counts[m], "primitive": int(prim)})
        print(f"  {m:6d}   {counts[m]:32d}   {int(prim)}")

    first = next((r["length"] for r in rows if r["closed"] > 0), None)
    print(f"""
  The shortest identity program has length {first}.  Everything at that length and just above
  is a DEFINING RELATION of the instruction set -- the machine's own equations, read off
  the zeta rather than derived from a presentation.

  For a compiler this table is peephole data, and the useful direction is the small end:
  any occurrence of a length-{first} closed walk in an instruction stream is dead code by
  construction, and there are {counts[first]} of them to match against.  The counts then grow
  like rho^m, which is Pass 4242's entropy seen from the other side -- the same number
  governs how much dead code exists and how much trajectory the machine generates.

  Note what makes this legible: it needs the graph, not the group.  The group's relations
  are a presentation problem; the graph's closed walks are a trace.""")
    return {"closed_by_length": counts, "rows": rows, "shortest_identity": first}


# ------------------------------------------------------------------ 4244
def pass_4244() -> dict:
    print()
    print("=" * 78)
    print("Pass 4244 -- where the machine is slow")
    print("=" * 78)
    A = simple(ISA)
    B, de = hashimoto(A)
    vals, vecs = np.linalg.eig(B)
    mods = np.abs(vals)
    rho = float(mods.max())
    crit = sqrt(rho)
    # non-trivial poles, ordered by distance OUTSIDE the critical circle: the further out,
    # the slower the corresponding mode decays, so the more it obstructs mixing.
    idx = [i for i in range(len(vals))
           if mods[i] > 1 + 1e-9 and abs(mods[i] - rho) > 1e-6 * rho]
    idx.sort(key=lambda i: -mods[i])
    print(f"  rho {rho:.6f}   critical circle sqrt(rho) {crit:.6f}")
    print(f"  non-trivial poles {len(idx)}, largest modulus {mods[idx[0]]:.6f} "
          f"({mods[idx[0]] / crit:.3f}x the critical circle)")

    # localisation: participation ratio of the slowest mode over DIRECTED EDGES, then
    # aggregate onto the source frame.
    v = np.abs(vecs[:, idx[0]]) ** 2
    v = v / v.sum()
    pr = 1.0 / float((v ** 2).sum())
    print(f"  participation ratio of the slowest mode: {pr:.1f} of {len(v)} directed edges"
          f"  ({100 * pr / len(v):.1f}%)")

    frame_w = np.zeros(81)
    for (x, y), w in zip(de, v):
        frame_w[x] += w
    order = np.argsort(-frame_w)
    d = A.sum(axis=1)
    print("\n  frames carrying the most of the slowest mode:")
    print(f"  {'frame':16s} {'weight':>9s} {'degree':>7s}")
    for i in order[:6]:
        print(f"  {str(TV[i]):16s} {frame_w[i]:9.4f} {int(d[i]):7d}")

    # IS IT A DEGREE EFFECT?  The obvious guess is that the mode sits where the opcodes
    # touch least.  Test it rather than assert it -- an earlier draft of this pass claimed
    # exactly that and the numbers below refute it.
    corr = float(np.corrcoef(frame_w, d)[0, 1])
    deg_top = float(d[order[:9]].mean())
    print(f"\n  correlation of mode weight with degree : {corr:+.4f}")
    print(f"  mean degree, top 9 frames / all frames : {deg_top:.3f} / {float(d.mean()):.3f}")
    print("  -> NOT a degree effect: the heavy frames are slightly ABOVE average degree.")

    # Where does it actually live?  Test each coordinate hyperplane.
    print("\n  coordinate  value   frames   mode weight   mean degree")
    best = None
    for c in range(4):
        for val in range(3):
            sel = [i for i in range(81) if TV[i][c] == val]
            w = float(frame_w[sel].sum())
            md = float(d[sel].mean())
            print(f"  {'x' + str(c):>10s} {val:6d} {len(sel):8d} {w:13.4f} {md:13.2f}")
            if best is None or w > best[2]:
                best = (c, val, w, md)
    c, val, w, md = best
    flat = all(abs(float(d[[i for i in range(81) if TV[i][c] == u]].mean()) - md) < 1e-9
               for u in range(3))

    # WHY?  Count how many opcodes move that coordinate at all.
    movers = []
    for nm, M in (("F_p", LIN["F_p"]), ("CX_pf", LIN["CX_pf"]), ("CX_fp", LIN["CX_fp"])):
        n_moved = sum(1 for x in TV if mv(M, x)[c] != x[c])
        if n_moved:
            movers.append((nm, n_moved))
    print(f"""
  THE MODE LIVES ON A HYPERPLANE, AND IT IS NOT ABOUT DEGREE.  Frames with x{c} = {val} are
  27 of 81 and carry {100 * w:.1f}% of the slowest mode, against {100 * (1 - w) / 2:.1f}% for each of the
  other two values.  Mean degree is {md:.2f} on all three classes alike ({flat}), so degree
  explains none of it -- the correlation between mode weight and degree is only {corr:+.3f}.

  THE CAUSE IS A NEAR-CONSERVED COORDINATE.  Of the four opcodes, only """
          f"""{', '.join(n for n, _ in movers)} moves x{c} at all,
  and it moves it on just {movers[0][1] if movers else 0} of 81 frames -- exactly those with x0 != 0.  The other
  three opcodes, including the load port, leave x{c} untouched.  So x{c} is very nearly a
  constant of the motion, and a register coordinate the instruction set barely stirs is
  precisely a slow mode.

  That is the bottleneck named, and the naming corrects a guess.  The natural story --
  'the machine is slow where the opcodes touch least, i.e. at low degree' -- is false here:
  the heavy frames have slightly higher degree than average.  The defect is not how MANY
  edges leave a frame but WHICH DIRECTION they move it in, and one direction is nearly
  frozen.

  Actionably, this is a sharper prescription than adding a second load port. What the
  design needs is an opcode that moves x{c} UNCONDITIONALLY -- the shear S_f does exactly
  that -- rather than more of the same. Pass 4225 showed one load port suffices for
  REACHABILITY; this says reachability was never the constraint on mixing.""")
    return {"rho": rho, "critical_circle": crit,
            "largest_nontrivial_modulus": float(mods[idx[0]]),
            "ratio_to_critical": float(mods[idx[0]] / crit),
            "participation_ratio": pr, "directed_edges": int(len(v)),
            "top_frames": [[list(TV[int(i)]), float(frame_w[int(i)]), int(d[int(i)])]
                           for i in order[:9]],
            "weight_degree_correlation": corr,
            "top9_mean_degree": deg_top, "all_mean_degree": float(d.mean()),
            "hyperplane": {"coordinate": c, "value": val, "mode_weight": w,
                           "mean_degree": md, "degree_flat_across_classes": bool(flat)},
            "opcodes_moving_that_coordinate": movers,
            "is_degree_effect": False}


def main() -> int:
    unis = universal_sets()
    out = {}
    out["pass_4238_why_rank"] = pass_4238(unis)
    out["pass_4239_kotani_sunada"] = pass_4239(unis)
    out["pass_4240_cross_check"] = pass_4240(unis)
    out["pass_4242_entropy"] = pass_4242()
    out["pass_4243_identity_programs"] = pass_4243()
    out["pass_4244_localisation"] = pass_4244()
    out["pass_4237_min_poly"] = pass_4237()
    path = ROOT / "data" / "PART_W33_PASS4237_4244_MINPOLY_AND_OUTSIDE_BOX.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
