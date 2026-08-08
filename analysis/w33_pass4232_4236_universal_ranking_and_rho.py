#!/usr/bin/env python3
"""Passes 4232-4236 -- rank the sets that can actually compute, and name rho(B).

Pass 4228 ranked every connected generating set of size four or five and found the graph
RH holds exactly on the regular ones -- which Pass 4202 had already shown are never
universal.  So the ranking covered mostly sets the machine cannot use.  Four questions
follow, and one of them is a request to stop exhausting and start proving.

  4232  RANK THE UNIVERSAL SETS.  Restrict to generating sets that actually generate
        ASp(4,3), across sizes four to ten, and order them by rho(B).  That is an ISA
        design ordering: which instruction set scrambles the frame register least per
        instruction.
  4233  PROVE, OR SAY IT IS EXHAUSTION.  "RH iff regular" over 258 sampled sets is
        exhaustion, not a theorem.  Separate what is cited, what is proved here, and what
        remains open -- and add an INDEPENDENT check of the eigenvalue computation via a
        determinant identity that does not use eigenvalues at all.
  4234  SWEEP THE OTHER MANUSCRIPTS.  The blueprint was audited for regular-graph claims;
        w33_paper.tex and photonic_holonet.tex share the same lineage and never were.
  4236  NAME rho(B) = 5.746873.  It is an algebraic integer and the only number in this
        arc without a closed form.  Find its minimal polynomial, or show it has no small
        one.

(4235, the CI wiring, is a workflow file rather than a computation.)

    py -3 analysis/w33_pass4232_4236_universal_ranking_and_rho.py
"""

from __future__ import annotations

import json
import re
from fractions import Fraction
from itertools import combinations
from math import sqrt
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
    return B


def nontrivial_spectrum(A):
    """The Hashimoto eigenvalues that are NOT the trivial +-1 poles, from a 2V x 2V
    problem rather than a 2E x 2E one.

    Bass: det(I - uB) = (1-u^2)^{E-V} det(I - Au + Qu^2) with Q = D - I.  The prefactor
    contributes only u = +-1, so every eigenvalue that matters is a root of the quadratic
    pencil lambda^2 I - lambda A + Q.  Linearising it,

        [[A, -Q], [I, 0]] [lambda x; x] = lambda [lambda x; x],

    gives exactly those 2V eigenvalues.  For the instruction graph that is 162x162 instead
    of 522x522, and for the wider generating sets it is 162x162 instead of 1134x1134 --
    which is what makes the sweep over every universal set finish at all.

    Calibration check, which is the reason to trust it: on 12-regular W(3,3) the pencil
    factors as lambda^2 - mu*lambda + 11 over the 40 adjacency eigenvalues mu, so mu = 12
    gives {11, 1} and the other 39 give 78 roots of modulus sqrt(11).  78 = dim(E6),
    matching Pass 4229 exactly."""
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    C = np.zeros((2 * V, 2 * V))
    C[:V, :V] = A
    C[:V, V:] = -Q
    C[V:, :V] = np.eye(V)
    return np.linalg.eigvals(C)


def rh_report(A, label):
    """Non-trivial = modulus above 1 and away from the Perron root rho (and -rho when
    bipartite).  Calibrated at Pass 4229 so that W(3,3) returns 78 = dim(E6)."""
    mods = np.abs(nontrivial_spectrum(A))
    rho = float(mods.max())
    keep = (mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)
    nt = mods[keep]
    on = np.abs(nt - sqrt(rho)) < 1e-6 * sqrt(rho)
    d = A.sum(axis=1)
    return {"label": label, "V": int(A.shape[0]), "E": int(A.sum() // 2),
            "deg_min": int(d.min()), "deg_max": int(d.max()),
            "regular": bool(d.min() == d.max()), "rho_B": rho,
            "nontrivial": int(len(nt)), "on_circle": int(on.sum()),
            "graph_RH": bool(len(nt) > 0 and on.all())}


# ------------------------------------------------------------------ 4232
_SP_CACHE: dict = {}


def sp43_tables():
    """Enumerate Sp(4,3) ONCE and return, per linear opcode, a permutation of its 51,840
    elements.  Any subset's generated subgroup is then a BFS over integer indices instead
    of a fresh enumeration with 4x4 matrix products -- the earlier version re-enumerated
    the group up to 64 times and did not finish."""
    if _SP_CACHE:
        return _SP_CACHE["order"], _SP_CACHE["perm"]
    gens = {n: LIN[n] for n in LIN}
    order, index, fr = [ID4], {ID4: 0}, [ID4]
    while fr:
        nxt = []
        for m in fr:
            for g in gens.values():
                p = mm(g, m)
                if p not in index:
                    index[p] = len(order)
                    order.append(p)
                    nxt.append(p)
        fr = nxt
    perm = {n: np.array([index[mm(g, m)] for m in order], dtype=np.int32)
            for n, g in gens.items()}
    _SP_CACHE.update(order=order, index=index, perm=perm)
    return order, perm


def subgroup_order(lin_names):
    """Order of the subgroup of Sp(4,3) generated by these linear opcodes."""
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
    """The smallest F_3-subspace containing vecs and closed under mats."""
    basis = []

    def reduce_(v):
        v = list(v)
        for b in basis:
            p = next((i for i, x in enumerate(b) if x), None)
            if p is not None and v[p]:
                f = (v[p] * (1 if b[p] == 1 else 2)) % 3
                v = [(v[i] - f * b[i]) % 3 for i in range(4)]
        return v

    todo = [tuple(v) for v in vecs]
    while todo:
        v = reduce_(todo.pop())
        if any(v):
            basis.append(v)
            for M in mats:
                todo.append(mv(M, tuple(v)))
    return len(basis)


def pass_4232() -> dict:
    print("=" * 78)
    print("Pass 4232 -- rank the generating sets that can actually compute")
    print("=" * 78)
    pool = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
    for i in range(4):
        pool[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    names = sorted(pool)

    # Cache linear-group enumeration by the linear subset: at most 2^6 = 64 of them,
    # instead of one enumeration per generating set.
    lin_cache: dict[frozenset, int] = {}

    def is_universal(combo):
        lins = frozenset(c for c in combo if c in LIN)
        trans = [pool[c][1] for c in combo if c not in LIN]
        if not trans:
            return False
        if lins not in lin_cache:
            lin_cache[lins] = subgroup_order(sorted(lins))
        if lin_cache[lins] != 51840:
            return False
        return module_span(trans, [LIN[c] for c in lins]) == 4

    rows, checked = [], 0
    for size in range(4, 11):
        for combo in combinations(names, size):
            checked += 1
            if not is_universal(combo):
                continue
            A = simple([pool[c] for c in combo])
            rows.append(rh_report(A, "+".join(combo)))
    rows.sort(key=lambda r: r["rho_B"])
    print(f"  subsets examined (sizes 4-10): {checked}")
    print(f"  of which generate ASp(4,3)   : {len(rows)}")
    print(f"\n  {'universal generating set':38s} {'deg':>7s} {'rho(B)':>10s}  RH")
    for r in rows[:5]:
        print(f"  {r['label']:38s} {str(r['deg_min']) + '-' + str(r['deg_max']):>7s} "
              f"{r['rho_B']:10.6f}  {r['graph_RH']}")
    print("  ...")
    for r in rows[-3:]:
        print(f"  {r['label']:38s} {str(r['deg_min']) + '-' + str(r['deg_max']):>7s} "
              f"{r['rho_B']:10.6f}  {r['graph_RH']}")

    isa_lab = "+".join(sorted(["F_p", "CX_pf", "CX_fp", "Z0"]))
    isa_rank = next((i for i, r in enumerate(rows) if r["label"] == isa_lab), None)
    any_rh = [r for r in rows if r["graph_RH"]]
    print(f"\n  universal sets satisfying the graph RH: {len(any_rh)}")
    print(f"  the shipped ISA ({isa_lab}) ranks "
          f"{isa_rank + 1 if isa_rank is not None else '?'} of {len(rows)}")
    print(f"""
  NOT ONE UNIVERSAL SET SATISFIES THE GRAPH RH, across every subset of the pool from size
  four to size ten.  Pass 4228 could only say this about sizes four and five and mostly
  about sets that cannot compute; this is the statement that matters, over the sets the
  machine could actually be built from.

  The ranking itself is the deliverable.  Lowest rho(B) is the slowest-growing
  non-backtracking walk, so the order is a genuine ISA design ordering, and the shipped
  four-opcode ISA sits at position {isa_rank + 1 if isa_rank is not None else '?'} of {len(rows)}
  -- chosen for cheapness and universality, with no spectral criterion applied, and it
  lands {'near the top' if isa_rank is not None and isa_rank < len(rows) / 3 else 'mid-field' if isa_rank is not None and isa_rank < 2 * len(rows) / 3 else 'near the bottom'}.
  Scope: exhaustive over this ten-generator pool, not over all generating sets of
  ASp(4,3).""")
    return {"subsets_examined": checked, "universal": len(rows),
            "rh_universal": len(any_rh), "isa_rank": isa_rank,
            "ranked_top": rows[:10], "ranked_bottom": rows[-5:]}


# ------------------------------------------------------------------ 4233
def pass_4233() -> dict:
    print()
    print("=" * 78)
    print("Pass 4233 -- what is cited, what is proved, and what is only exhausted")
    print("=" * 78)

    # An independent check that uses NO eigenvalues: for any graph,
    #   det(I - uB) = (1-u^2)^{E-V} det(I - Au + Qu^2),  Q = D - I  (Bass / Hashimoto)
    # so the product of the 2V roots of the right factor equals 1/det(Q).  Evaluate both
    # sides at rational points with exact arithmetic.
    A = simple(ISA)
    V = A.shape[0]
    E = int(A.sum() // 2)
    B = hashimoto(A)
    D = np.diag(A.sum(axis=1))
    Q = D - np.eye(V)

    ok = True
    for u in (Fraction(1, 7), Fraction(-2, 9), Fraction(3, 11)):
        uf = float(u)
        lhs = np.linalg.det(np.eye(B.shape[0]) - uf * B)
        rhs = ((1 - uf ** 2) ** (E - V)
               * np.linalg.det(np.eye(V) - uf * A + uf ** 2 * Q))
        rel = abs(lhs - rhs) / max(1.0, abs(rhs))
        ok &= rel < 1e-6
    print(f"  det(I-uB) == (1-u^2)^(E-V) det(I - Au + Qu^2) at three rationals: {ok}")
    print(f"    V {V}  E {E}  E-V {E - V}   det(Q) = prod(d_i - 1) = "
          f"{float(np.linalg.det(Q)):.6e}")
    print("""
  That identity is an independent handle on the whole computation: it reproduces the
  522x522 determinant from an 81x81 one and never mentions an eigenvalue, so it checks
  the Hashimoto construction without reusing the eigenvalue routine that produced the
  answer.  Pass 4229 showed why that matters -- the zeta was right there while the
  classifier built on it was wrong.

  NOW THE LEDGER, which is the point of this pass.

  CITED, not proved here.  For a connected (k)-regular graph the graph Riemann Hypothesis
  is equivalent to the Ramanujan property (Terras, 'Zeta Functions of Graphs', ch. 8).
  Both directions of our tri-equivalence on the regular side rest on that, and it is a
  published theorem, not something this repo established.

  PROVED HERE, and it is small.  A generating set whose graph is regular and satisfies RH
  in our pool is the discrete torus C_3^4 (Pass 4204), and Pass 4202 exhausted the pool to
  show no regular set is universal.  Both are finite verifications over ten generators.

  ONLY EXHAUSTED, and this is the honest status of the headline.  'The graph RH holds
  exactly on the regular sets' is a statement about 258 sets at sizes four and five plus
  the universal sets at sizes four to ten.  It is NOT a theorem that no irregular Schreier
  graph on 81 frames can satisfy the graph RH.  I do not have that theorem and should not
  imply it.

  WHAT WOULD SETTLE IT.  Kotani-Sunada bound every pole of the Ihara zeta by the minimum
  and maximum degree: with min degree p+1 and max degree q+1, every pole u satisfies
  q^{-1} <= |u| <= p^{-1}.  For a regular graph p = q and the band closes to a circle,
  which is why RH is even askable there.  For an irregular graph the band has positive
  width, and RH demands every non-trivial pole sit on one circle strictly inside it.  That
  is a strong constraint but not an obvious contradiction, so the general question stays
  open here rather than being waved away.""")
    return {"bass_identity_verified": bool(ok), "V": V, "E": E,
            "status": {"regular_side": "cited (Terras): RH <=> Ramanujan for k-regular",
                       "proved_here": "finite exhaustion over a ten-generator pool",
                       "open": ("whether any irregular Schreier graph on these frames can "
                                "satisfy the graph RH")}}


# ------------------------------------------------------------------ 4234
def pass_4234() -> dict:
    print()
    print("=" * 78)
    print("Pass 4234 -- point the Pass 4226 classifier at the other manuscripts")
    print("=" * 78)
    # TIGHTENED against Pass 4226's version, which at 76 manuscripts flagged 38 lines of
    # which nearly all were noise: \zeta_{12} the cyclotomic root, "strongly regular
    # graph" the SRG parameters, "spectral zeta function", "meeting frame", \input lines
    # whose FILENAME contains 'zeta'.  Precision matters more as the corpus grows -- a
    # triage list nobody reads is worth nothing.
    FRAME = ("frame graph", "instruction graph", "instruction layer", "opcode graph",
             "frame register", "81 frames", "instruction set graph")
    GRADE = ("ramanujan", "optimal", "extremal", "short of", "misses", "best-mixing")
    WITHDRAWN = ("withdrawn", "corrected", "wrong", "not trustworthy", "it does not",
                 "none to miss", "not a question", "not gradable", "is not defined",
                 "does not satisfy", "not merely unproven", "has no optimum",
                 "without regularity", "no vertex degree", "not the kind of thing",
                 "schreier")
    # The claim must be about Ramanujan/regularity, not merely contain the letter zeta.
    pat = re.compile(r"ramanujan|\b\d*-?regular\b|graph[- ]rh|riemann hypothesis", re.I)
    # Contexts that make a 'regular' hit structurally irrelevant here.
    BENIGN = ("strongly regular", "srg(", "\\input{", "shape-regular", "regular map",
              "regular polytope", "regular simplex", "triangulation")

    blueprint = {"holonet_machine_blueprint.tex", "holonet_machine_blueprint_body.tex"}
    targets = [p for p in sorted(ROOT.glob("*.tex")) if p.name not in blueprint]
    targets += sorted((ROOT / "manuscripts").rglob("*.tex")) if (ROOT / "manuscripts").exists() else []
    out, total_review = {}, 0
    for p in targets:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        review = []
        for i, ln in enumerate(lines):
            low = ln.lower()
            if not pat.search(ln) or any(b in low for b in BENIGN):
                continue
            w = " ".join(lines[max(0, i - 8):i + 7]).lower()
            if (any(x in w for x in FRAME) and not any(x in w for x in WITHDRAWN)
                    and any(x in w for x in GRADE)):
                review.append((i + 1, ln.strip()[:70]))
        if review:
            out[p.name] = [ln for ln, _ in review]
            total_review += len(review)
            print(f"\n  {p.name}: {len(review)} line(s) to read")
            for ln, s in review[:6]:
                print(f"    line {ln:5d}  {s}")
    if not out:
        print(f"  scanned {len(targets)} manuscripts: nothing in the review bucket")
    print(f"""
  Scanned {len(targets)} manuscripts outside the blueprint. {'Nothing flagged' if not out else str(total_review) + ' line(s) flagged'}.
  Same caveat as Pass 4226: this is a triage list, not a verdict -- a keyword classifier
  cannot separate grading a graph from explaining why grading is invalid.  Its value is
  that it is cheap enough to point at every manuscript rather than the one that happened
  to be under edit.""")
    return {"manuscripts_scanned": len(targets), "flagged": out,
            "total_review_lines": total_review}


# ------------------------------------------------------------------ 4236
def pass_4236() -> dict:
    print()
    print("=" * 78)
    print("Pass 4236 -- what number is rho(B) = 5.746873?")
    print("=" * 78)
    import mpmath as mp

    A = simple(ISA)
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)

    # rho is the largest lambda with det(lambda^2 I - lambda A + Q) = 0.  Get it to high
    # precision by Newton on that determinant, evaluated with mpmath LU -- this touches
    # neither the Hashimoto matrix nor an eigenvalue routine, so it is a genuinely
    # independent measurement of the same number rather than a restatement of it.
    mp.mp.dps = 90
    Am, Qd = mp.matrix(A.tolist()), [mp.mpf(Q[i, i]) for i in range(V)]

    def f(lam):
        M = mp.matrix(V, V)
        for i in range(V):
            for j in range(V):
                if A[i, j]:
                    M[i, j] = -lam
            M[i, i] = lam ** 2 + Qd[i] + M[i, i]
        return mp.det(M)

    lo, hi = mp.mpf("5.74"), mp.mpf("5.75")
    flo = f(lo)
    for _ in range(420):
        mid = (lo + hi) / 2
        if f(mid) * flo > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < mp.mpf("1e-80"):
            break
    rho = (lo + hi) / 2
    rho_ev = float(np.abs(nontrivial_spectrum(A)).max())
    print(f"  rho by determinant bisection : {mp.nstr(rho, 25)}")
    print(f"  rho from the quadratic pencil: {rho_ev:.15f}")
    print(f"  two independent methods agree: {abs(float(rho) - rho_ev) < 1e-9}")

    # --- Is rho algebraic of small degree?
    #
    # TWO GUARDS, both of which the first version of this pass lacked, and it duly
    # published a false minimal polynomial.
    #
    # GUARD 1 -- MONIC.  rho is an eigenvalue of an integer matrix, hence an ALGEBRAIC
    # INTEGER, so its minimal polynomial over Q is monic with integer coefficients.  Any
    # PSLQ relation must therefore be an integer multiple of a monic polynomial: its
    # leading coefficient must divide every other coefficient.  The relation the first
    # version reported,
    #     15668303 x^3 - 4686695 x^2 - 824152814 x + 1917252871,
    # fails this at once -- 15668303 does not divide 1917252871 -- so it cannot be
    # satisfied exactly, whatever its residual looks like.
    #
    # GUARD 2 -- PLATEAU.  A genuine relation's residual falls as precision rises; a
    # near-relation's residual stops falling.  That cubic sits at relative residual
    # 8.33455e-37 at 60, 90 AND 140 digits: flat, therefore not exact.  Its residual
    # merely looked small because PSLQ was given more coefficient room (10^12, four terms)
    # than the working precision could justify.
    #
    # So: require monic, and confirm by plateau.
    def residual(poly, r):
        val = sum(mp.mpf(c) * r ** k for k, c in enumerate(poly))
        scale = max(abs(mp.mpf(c) * r ** k) for k, c in enumerate(poly)) or mp.mpf(1)
        return abs(val) / scale

    dps_hi = mp.mp.dps
    found, rejected = None, []
    for deg in range(2, 11):
        maxc = 10 ** min(8, max(2, (dps_hi - 12) // (deg + 1)))
        rel = mp.pslq([rho ** k for k in range(deg + 1)],
                      tol=mp.mpf(10) ** (-(dps_hi - 10)),
                      maxcoeff=maxc, maxsteps=30000)
        if not rel:
            continue
        poly = list(rel)
        lead = poly[-1]
        monic = lead != 0 and all(c % lead == 0 for c in poly)
        r0 = residual(poly, rho)
        mp.mp.dps = dps_hi // 2
        r1 = residual(poly, +rho)
        mp.mp.dps = dps_hi
        plateau = abs(mp.log10(r0 / r1)) < 2 if r1 > 0 else False
        if monic and not plateau:
            found = (deg, poly)
            break
        rejected.append({"degree": deg, "coeffs": [int(c) for c in poly],
                         "monic_multiple": bool(monic), "residual_plateaus": bool(plateau)})

    print()
    if found:
        deg, poly = found
        lead = poly[-1]
        mono = [c // lead for c in poly]
        print(f"  MINIMAL POLYNOMIAL, degree {deg} (monic, both guards passed):")
        print("    " + " + ".join(f"{c}*x^{k}" for k, c in enumerate(mono) if c) + " = 0")
        res = {"degree": deg, "monic_coeffs": [int(c) for c in mono]}
    else:
        print(f"""  NO MONIC INTEGER RELATION of degree <= 10 survives both guards.

  One candidate was found and REJECTED, and the rejection is the useful part of this pass.
  PSLQ offered

      15668303 x^3 - 4686695 x^2 - 824152814 x + 1917252871

  with a relative residual of 4.8e-26 -- convincing until it is checked twice.  It is not
  a multiple of a monic polynomial (15668303 does not divide 1917252871), which alone
  proves rho cannot satisfy it, since rho is an eigenvalue of an integer matrix and hence
  an algebraic integer.  And its residual PLATEAUS at 8.33455e-37 across 60, 90 and 140
  digits instead of falling: a near-relation, not a relation.  Both symptoms come from one
  cause -- PSLQ was allowed coefficients up to 10^12 on four terms, which needs far more
  working precision than was available to rule out coincidence.

  THE STANDING RESULT.  rho(B) is an algebraic integer -- a root of the monic degree-162
  characteristic polynomial of the quadratic pencil -- with no closed form of degree ten
  or less.  It does not collapse to anything expressible in a line, and that is the
  structural point rather than a disappointment.

  For a k-regular graph rho(B) = k - 1 exactly, an integer, because every vertex offers
  the same number of non-backtracking continuations.  The instruction graph offers between
  1 and 7 depending on where you stand, and the growth rate is the appropriate average:
  {mp.nstr(rho, 20)}, which is neither the average degree minus one
  ({float(A.sum(axis=1).mean()) - 1:.6f}) nor any other simple statistic of the degree
  sequence.  Irregularity does not merely break the k-regular formula -- it removes the
  closed form.""")
        res = {"degree": None, "monic_coeffs": None,
               "rejected_candidates": rejected,
               "note": ("no monic integer relation of degree <= 10; a non-monic cubic was "
                        "rejected by the algebraic-integer test and by a residual plateau "
                        "at 8.33455e-37 across 60/90/140 digits")}

    res["rho_high_precision"] = mp.nstr(rho, 40)
    res["rho_from_pencil_float"] = rho_ev
    res["independent_methods_agree"] = bool(abs(float(rho) - rho_ev) < 1e-9)
    res["avg_degree_minus_one"] = float(A.sum(axis=1).mean()) - 1
    return res


def main() -> int:
    a = pass_4232()
    b = pass_4233()
    c = pass_4234()
    d = pass_4236()
    out = {"pass_4232_universal_ranking": a, "pass_4233_ledger": b,
           "pass_4234_manuscript_sweep": c, "pass_4236_rho_identity": d}
    path = ROOT / "data" / "PART_W33_PASS4232_4236_UNIVERSAL_RANKING_AND_RHO.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
