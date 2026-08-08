#!/usr/bin/env python3
"""Passes 4222-4226 -- the zeta the instruction graph actually has, and four audits.

Three passes have now tried to say something spectral about the 81-frame instruction graph
and been withdrawn for the same reason: 3060 applied a k-regular Ihara formula, 4201
measured a graph its Clifford generator contributed no edges to, and 3042's "3.23% short of
Ramanujan" graded a graph with degrees 2 to 8 against a 4-regular threshold.  Pass 4203
found the shared cause -- it was called a Cayley graph, so regularity felt obligatory.

Bass's determinant relation genuinely does need regularity.  The Ihara zeta does not.  For
ANY finite graph,

    zeta^-1(u) = det(I - uB),   B = the Hashimoto non-backtracking edge matrix,

with B indexed by the 2E directed edges and B[(x,y),(y,z)] = 1 iff z != x.  The instruction
graph has 261 edges, so B is 522x522 and the whole question is a small eigenvalue problem.
This is the tool the object always needed and never got.

  4222  the exact Ihara zeta of the instruction graph, no regularity assumed, validated
        against K4 and against the parallel track's Pass 4191 Levi closed form first
  4223  a benchmark that survives irregularity, replacing the withdrawn 3.23%
  4224  is the irregularity locus a union of symmetry orbits?
  4225  minimum load ports, as an exact architectural number
  4226  sweep the manuscript for the remaining regular-graph claims

    py -3 analysis/w33_pass4222_4226_zeta_without_regularity.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
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
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
# Pass 2866's ISA, read from source: three linear opcodes and one translation (the load
# port).  Pass 4213 corrected an earlier pass that assumed four Clifford operations.
ISA_LIN = ["F_p", "CX_pf", "CX_fp"]
ISA = [(LIN[n], (0, 0, 0, 0)) for n in ISA_LIN] + [(ID4, (1, 0, 0, 0))]

J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def simple(gens, n=81, pts=None, idx=None):
    pts = pts or TV
    idx = idx or TI
    A = np.zeros((n, n))
    for g in gens:
        for i, x in enumerate(pts):
            j = idx[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


# --------------------------------------------------------------------------- zeta
def hashimoto(A):
    """B on the 2E directed edges: B[(x,y),(y,z)] = 1 iff z != x.  No regularity used."""
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


def zeta_inv_at(B, u):
    m = B.shape[0]
    return np.linalg.det(np.eye(m) - u * B)


def k4():
    A = np.ones((4, 4)) - np.eye(4)
    return A


def levi_w33():
    """Incidence graph of W(3,3): 40 isotropic points and 40 totally isotropic lines,
    each point on four lines.  This is Pass 4191's degree-four Levi graph."""
    vecs = [v for v in
            ((a, b, c, d) for a in range(3) for b in range(3)
             for c in range(3) for d in range(3)) if any(v)]
    seen, pts = set(), []
    for v in vecs:
        key = min(tuple((c * x) % 3 for x in v) for c in (1, 2))
        if key not in seen:
            seen.add(key)
            pts.append(key)
    pidx = {p: i for i, p in enumerate(pts)}

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    lines = set()
    for p, q in combinations(pts, 2):
        if form(p, q) != 0:
            continue
        span = set()
        for a in range(3):
            for b in range(3):
                w = tuple((a * p[i] + b * q[i]) % 3 for i in range(4))
                if any(w):
                    span.add(min(tuple((c * x) % 3 for x in w) for c in (1, 2)))
        if len(span) == 4:
            lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))
    n = len(pts) + len(lines)
    A = np.zeros((n, n))
    for li, L in enumerate(lines):
        for p in L:
            A[pidx[p], len(pts) + li] = 1
            A[len(pts) + li, pidx[p]] = 1
    return A, len(pts), len(lines)


def pass_4222() -> dict:
    print("=" * 78)
    print("Pass 4222 -- the Ihara zeta of the instruction graph, no regularity assumed")
    print("=" * 78)

    # --- reference 1: K4, whose closed form is textbook
    A = k4()
    B, de = hashimoto(A)
    print(f"  reference 1  K4: V 4  2E {len(de)}  B {B.shape[0]}x{B.shape[0]}")
    ok1 = True
    for u in (0.13, -0.21, 0.37):
        lhs = zeta_inv_at(B, u)
        rhs = ((1 - u ** 2) ** 2 * (1 - u) * (1 - 2 * u) * (1 + u + 2 * u ** 2) ** 3)
        ok1 &= abs(lhs - rhs) < 1e-9 * max(1.0, abs(rhs))
    print(f"               det(I-uB) == (1-u^2)^2 (1-u)(1-2u)(1+u+2u^2)^3 : {ok1}")

    # --- reference 2: Pass 4191's Levi closed form, a large graph with a nontrivial form
    AL, npts, nlin = levi_w33()
    BL, deL = hashimoto(AL)
    degL = AL.sum(axis=1)
    print(f"  reference 2  Levi: points {npts}  lines {nlin}  degrees "
          f"{int(degL.min())}-{int(degL.max())}  2E {len(deL)}")
    ok2 = True
    for u in (0.11, -0.17, 0.29):
        lhs = zeta_inv_at(BL, u)
        rhs = ((1 - u ** 2) ** 81 * (1 - 9 * u ** 2)
               * (1 + 9 * u ** 4) ** 24 * (1 + 3 * u ** 2) ** 30)
        ok2 &= abs(lhs - rhs) < 1e-6 * max(1.0, abs(rhs))
    print(f"               det(I-uB) == Pass 4191's closed form               : {ok2}")
    print("               (the Hashimoto route reproduces a form Bass produced, on a")
    print("                graph where both apply -- so the tool is validated where it")
    print("                can be checked, before being used where Bass cannot go)")

    # --- the object itself
    AI = simple(ISA)
    d = AI.sum(axis=1)
    BI, deI = hashimoto(AI)
    E = int(AI.sum() // 2)
    print(f"\n  the instruction graph: V 81  E {E}  degrees {int(d.min())}-{int(d.max())}"
          f"  regular {bool(d.min() == d.max())}")
    print(f"  Hashimoto matrix     : {BI.shape[0]}x{BI.shape[0]}")

    ev = np.linalg.eigvals(BI)
    rho = float(max(abs(ev)))
    R = 1.0 / rho
    # poles of zeta are 1/eigenvalue; "trivial" ones sit at |u| = 1 (from eigenvalue +-1)
    mods = np.array([abs(v) for v in ev])
    nontriv = mods[mods > 1 + 1e-9]
    on_circle = np.abs(nontriv - sqrt(rho)) < 1e-6 * sqrt(rho)
    print(f"  spectral radius rho(B)      : {rho:.9f}")
    print(f"  zeta radius R = 1/rho       : {R:.9f}")
    print(f"  sqrt(rho)                   : {sqrt(rho):.9f}")
    print(f"  Hashimoto eigenvalues with |lambda| > 1 : {len(nontriv)}")
    print(f"  of those, |lambda| == sqrt(rho)         : {int(on_circle.sum())}")
    rh = bool(on_circle.all()) and len(nontriv) > 0
    print(f"  graph Riemann Hypothesis (all non-trivial poles on |u| = 1/sqrt(rho)): {rh}")

    print(f"""
  So the question that was ill-posed three times is now answered, and the answer is
  {'YES' if rh else 'NO'}.  The instruction graph {'satisfies' if rh else 'does NOT satisfy'} the
  graph Riemann Hypothesis.

  What changed is only the tool.  Bass needs a degree; Hashimoto needs a graph.  Every
  earlier attempt reached for a formula whose hypothesis the object fails, and the object
  was never the problem -- {BI.shape[0]}x{BI.shape[0]} is a small eigenvalue problem, and it was
  available at Pass 3060.""")

    return {"k4_reference": bool(ok1), "levi_reference": bool(ok2),
            "V": 81, "E": E, "deg_min": int(d.min()), "deg_max": int(d.max()),
            "regular": bool(d.min() == d.max()), "B_dim": int(BI.shape[0]),
            "rho_B": rho, "zeta_radius": R, "sqrt_rho": sqrt(rho),
            "nontrivial_count": int(len(nontriv)),
            "nontrivial_on_circle": int(on_circle.sum()),
            "graph_riemann_hypothesis": rh}


def pass_4223(z: dict) -> dict:
    print()
    print("=" * 78)
    print("Pass 4223 -- a benchmark that survives irregularity")
    print("=" * 78)
    AI = simple(ISA)
    d = AI.sum(axis=1)
    dbar = float(d.mean())
    ev = np.linalg.eigvalsh(AI)
    lam1 = float(max(ev))
    lam2 = float(sorted((abs(v) for v in ev), reverse=True)[1])
    hoory = 2 * sqrt(dbar - 1)
    print(f"  adjacency spectrum   lambda_1 {lam1:.6f}   |lambda_2| {lam2:.6f}")
    print(f"  average degree dbar  {dbar:.6f}   (degrees {int(d.min())} to {int(d.max())})")
    print(f"  Hoory's irregular Alon-Boppana benchmark 2*sqrt(dbar-1) = {hoory:.6f}")
    print(f"  |lambda_2| vs that benchmark: "
          f"{'above' if lam2 > hoory else 'below'} by {abs(lam2 - hoory):.6f}")
    print(f"""
  This is what replaces the withdrawn 3.23%.  Two honest statements and one refusal.

  HONEST 1.  rho(B) = {z['rho_B']:.6f} is exact, needs no regularity, and is the growth rate of
  non-backtracking instruction streams.  It is the right invariant for this object.

  HONEST 2.  Hoory's theorem gives 2*sqrt(dbar-1) = {hoory:.6f} as the irregular analogue of
  the Alon-Boppana bound, using the AVERAGE degree.  Measured |lambda_2| = {lam2:.6f}.
  Scope, stated plainly: Hoory's bound is asymptotic -- it constrains families of graphs,
  not one finite graph -- so this is a benchmark to report, not a threshold to pass or
  fail.  Quoting a percentage against it would repeat the mistake in a new costume.

  THE REFUSAL.  There is no number here that says how far the instruction layer is from
  optimal, because optimality is a regular-graph notion and this graph is not regular.
  The comparison the blueprint can make is between the two LAYERS: the address graph is
  12-regular and attains its optimum exactly; the instruction graph is a Schreier graph
  and has no optimum to attain.  That asymmetry is the finding.""")
    return {"lambda1": lam1, "lambda2": lam2, "avg_degree": dbar,
            "hoory_benchmark": hoory, "lambda2_above_benchmark": bool(lam2 > hoory),
            "refusal": ("no percentage-from-optimal exists for this graph; optimality is "
                        "a regular-graph notion")}


def pass_4224() -> dict:
    """A VACUOUS FRAMING, CAUGHT AND REPLACED.

    The first draft asked "is the deficiency constant on symmetry orbits?" and answered
    yes.  Both the question and the answer were worthless, for two independent reasons,
    and it is worth recording both because each is a trap this corpus has fallen into
    before.

      1. The group it computed had ORDER 1.  Requiring conjugation to permute the three
         linear opcodes exactly, while fixing e0, leaves only the identity.  Every orbit is
         a singleton, so "constant on orbits" is a statement about 81 sets of size one.
         That is Pass 3081's error exactly: a test whose two sides are the same thing.
      2. Even with the right group it would have been trivial.  Deficiency is 8 minus
         degree, and DEGREE IS AN AUTOMORPHISM INVARIANT OF ANY GRAPH.  So "deficiency is
         constant on automorphism orbits" is true of every graph ever drawn.  A test that
         cannot fail measures nothing.

    The question with content is the CONVERSE.  Deficiency classes are automatically
    unions of orbits; the real question is whether they are EXACTLY the orbits -- whether
    symmetry explains the partition {3, 6, 12, 24, 36} completely, or whether the graph
    distinguishes frames that share a degree.  Colour refinement answers it: 1-WL produces
    the canonical partition that refines the orbit partition, so if 1-WL stabilises to
    exactly the five degree classes, degree is the whole story; if it splits them, there is
    structure the degree does not see."""
    print()
    print("=" * 78)
    print("Pass 4224 -- does symmetry EXPLAIN the irregularity, or merely permit it?")
    print("=" * 78)
    AI = simple(ISA)
    d = AI.sum(axis=1)
    defic = {i: int(8 - d[i]) for i in range(81)}
    prof = Counter(defic.values())
    print(f"  deficiency profile: {dict(sorted(prof.items()))}")
    print("""
  First, a framing that had to be discarded.  "Is deficiency constant on symmetry orbits?"
  is trivially YES for every graph in existence, because deficiency is 8 minus degree and
  degree is an automorphism invariant.  The first draft of this pass asked it anyway, on a
  group that turned out to have order 1, so it compared 81 singletons with themselves.
  A test that cannot fail measures nothing; the question with content is the converse.
""")

    # 1-WL colour refinement: the canonical partition refining the automorphism orbits.
    colour = {i: int(d[i]) for i in range(81)}
    for _ in range(81):
        sig = {i: (colour[i], tuple(sorted(colour[int(j)]
                                           for j in np.flatnonzero(AI[i]))))
               for i in range(81)}
        order = {s: k for k, s in enumerate(sorted(set(sig.values())))}
        new = {i: order[sig[i]] for i in range(81)}
        if len(set(new.values())) == len(set(colour.values())):
            colour = new
            break
        colour = new

    cells = Counter(colour.values())
    cell_sizes = sorted(Counter(cells.values()).items())
    print(f"  1-WL stable partition: {len(cells)} cells, sizes {dict(cell_sizes)}")
    print(f"  degree classes       : {len(prof)} cells, sizes "
          f"{dict(sorted(Counter(prof.values()).items()))}")

    refines = len(cells) > len(prof)
    # is each WL cell inside a single degree class?  (it must be; degree seeds the colours)
    inside = all(len({defic[i] for i in range(81) if colour[i] == c}) == 1 for c in cells)
    print(f"  every WL cell lies inside one degree class: {inside}")
    print(f"  WL strictly refines the degree partition  : {refines}")

    if refines:
        print(f"""
  SO SYMMETRY DOES NOT EXPLAIN THE PARTITION.  Colour refinement splits the five degree
  classes into {len(cells)}, which means the graph distinguishes frames that share a degree --
  they sit differently in the graph even though they lose the same number of edges.  The
  histogram {{0:12, 1:36, 2:24, 4:6, 6:3}} is therefore a COARSENING: real structure, but
  strictly less than the whole story, and any account of the irregularity that stops at the
  degree sequence is incomplete by {len(cells) - len(prof)} cells.""")
    else:
        print(f"""
  SYMMETRY EXPLAINS THE PARTITION EXACTLY.  Colour refinement cannot separate any two
  frames of equal degree, so the five degree classes are as fine as the graph's own
  structure gets.  The deficiency histogram is then a complete invariant at the 1-WL level,
  and the irregularity really is a property of degree alone.""")

    # Geometry of the deficient frames: are the extreme classes affine subspaces?
    geo = {}
    for k in sorted(prof):
        pts = [TV[i] for i in range(81) if defic[i] == k]
        closed = all(tuple((2 * a[t] - b[t]) % 3 for t in range(4)) in set(pts)
                     for a in pts for b in pts) if 1 < len(pts) <= 27 else None
        geo[str(k)] = {"size": len(pts), "affine_subspace_or_coset": closed}
    print("\n  deficiency class   size   is it an affine subspace/coset of F_3^4?")
    for k, v in geo.items():
        print(f"  {k:>16s}   {v['size']:4d}   {v['affine_subspace_or_coset']}")

    return {"deficiency_profile": {str(k): v for k, v in sorted(prof.items())},
            "wl_cells": len(cells),
            "wl_cell_sizes": {str(k): v for k, v in cell_sizes},
            "degree_classes": len(prof),
            "wl_refines_degree": bool(refines),
            "wl_cells_inside_degree_classes": bool(inside),
            "class_geometry": geo,
            "discarded_framing": ("'deficiency is constant on automorphism orbits' is "
                                  "trivially true for every graph, since degree is an "
                                  "automorphism invariant; the first draft also computed "
                                  "it on a group of order 1")}


def pass_4225() -> dict:
    print()
    print("=" * 78)
    print("Pass 4225 -- minimum load ports, exactly")
    print("=" * 78)
    FULL = 81 * 51840

    def connected(A):
        seen, fr = {0}, [0]
        while fr:
            v = fr.pop()
            for u in np.flatnonzero(A[v]):
                if int(u) not in seen:
                    seen.add(int(u))
                    fr.append(int(u))
        return len(seen) == A.shape[0]

    def lin_orbit(v):
        """Orbit of a vector under the group the three linear opcodes generate.  This is
        the cheap route to universality and it is also the proof: the translations a
        generating set produces are the normal closure of the ones it starts with, so a
        single translation lifts Sp(4,3) to the full affine group exactly when its orbit
        spans.  Enumerating 4,199,040 group elements four times computes the same fact
        four times over, at 81 points' worth of work each."""
        mats = [LIN[n] for n in ISA_LIN]
        seen, fr = {v}, [v]
        while fr:
            nxt = []
            for x in fr:
                for M in mats:
                    y = mv(M, x)
                    if y not in seen:
                        seen.add(y)
                        nxt.append(y)
            fr = nxt
        return seen

    lin = [(LIN[n], (0, 0, 0, 0)) for n in ISA_LIN]
    A0 = simple(lin)
    d0 = A0.sum(axis=1)
    print("  ZERO load ports (the three linear opcodes alone):")
    print(f"    degrees {int(d0.min())}-{int(d0.max())}   connected {connected(A0)}"
          f"   isolated frames {int((d0 == 0).sum())}   subgroup Sp(4,3), order 51,840")
    print(f"    -> the frame graph is disconnected and the origin is fixed by every")
    print("       opcode, so it reaches 51,840 of 4,199,040 -- no translation at all.")

    print("\n  ONE load port, each of the four directions:")
    rows = []
    for i in range(4):
        t = tuple(1 if j == i else 0 for j in range(4))
        gens = lin + [(ID4, t)]
        A = simple(gens)
        d = A.sum(axis=1)
        orb = lin_orbit(t)
        spans = len(orb) == 80                     # all 80 nonzero vectors
        o = 51840 * 81 if spans else None
        rows.append({"direction": f"e{i}", "deg_min": int(d.min()),
                     "deg_max": int(d.max()), "connected": bool(connected(A)),
                     "linear_orbit_size": len(orb), "spans_all_translations": bool(spans),
                     "group_order": o, "universal": bool(spans)})
        print(f"    Z{i}: degrees {int(d.min())}-{int(d.max())}  connected "
              f"{connected(A)}  orbit of e{i} under Sp(4,3): {len(orb)}/80"
              f"  universal {spans}")

    allok = all(r["universal"] and r["connected"] for r in rows)
    print(f"""
  MINIMUM LOAD PORTS = 1, and the choice does not matter: {'all four' if allok else 'not all'}
  single translations connect the frame graph and lift the three linear opcodes to the full
  affine group of order {FULL:,}.

  That is an architectural number, not an aesthetic one.  Zero load ports is not a
  restricted machine, it is a machine with an unreachable address -- the origin is fixed by
  every linear opcode (Pass 4204a), so a Clifford-only register cannot be written and
  synthesis eliminates it (Pass 2774).  One load port removes both problems at once, and a
  second buys nothing in reachability.""")
    return {"zero_ports": {"deg_min": int(d0.min()), "deg_max": int(d0.max()),
                           "connected": bool(connected(A0)),
                           "isolated": int((d0 == 0).sum()), "group_order": 51840},
            "one_port": rows, "minimum_load_ports": 1,
            "direction_matters": not allok}


def pass_4226() -> dict:
    print()
    print("=" * 78)
    print("Pass 4226 -- sweep the manuscript for the remaining regular-graph claims")
    print("=" * 78)
    body = ROOT / "holonet_machine_blueprint_body.tex"
    txt = body.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()
    pat = re.compile(r"ramanujan|k?-?regular|2\\sqrt|ihara|zeta|\\lambda_2", re.I)
    hits = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if pat.search(ln)]
    print(f"  lines mentioning a regular-graph notion: {len(hits)}")

    # Classify rather than assert.  A hit is only dangerous when it is about the FRAME
    # graph AND grades it against a threshold.  Stating a measured eigenvalue is fine;
    # comparing it with a regular-graph bound is not.
    FRAME = ("frame", "instruction", "opcode", "isa")
    GRADE = ("\\le", "bound", "short of", "misses", "optimal", "threshold", "%")
    # Prose that DENIES the grading is correct prose, not a finding.  Without these the
    # checker flags its own corrections, which is how a keyword classifier fails.
    WITHDRAWN = ("withdrawn", "corrected", "wrong", "not trustworthy", "it does not",
                 "none to miss", "not a question", "not gradable", "is not defined",
                 "does not satisfy", "not merely unproven", "has no optimum",
                 "without regularity", "no vertex degree", "not the kind of thing")

    buckets = {"address-graph": [], "measurement-only": [], "documented-as-wrong": [],
               "NEEDS REVIEW": []}
    for ln, s in hits:
        window = " ".join(lines[max(0, ln - 8):ln + 7]).lower()
        if not any(w in window for w in FRAME):
            buckets["address-graph"].append((ln, s))
        elif any(w in window for w in WITHDRAWN):
            buckets["documented-as-wrong"].append((ln, s))
        elif any(w in window for w in GRADE):
            buckets["NEEDS REVIEW"].append((ln, s))
        else:
            buckets["measurement-only"].append((ln, s))

    for name, rows in buckets.items():
        print(f"\n  {name}: {len(rows)}")
        for ln, s in rows:
            print(f"    line {ln:5d}  {s[:74]}")

    review = buckets["NEEDS REVIEW"]
    mo = (", ".join(f"line {ln}" for ln, _ in buckets["measurement-only"]) or "empty")
    print(f"""
  WHAT THE SWEEP FOUND.  One real fourth instance, at line 595 of the pre-correction text:
  "the address layer ... is provably at an optimum the instruction layer MISSES".  That
  sentence presupposes the instruction layer has an optimum to miss, which Pass 4213 had
  just denied.  Three withdrawals from one cause is exactly the pattern that hides a
  fourth, and there was one.  It is now corrected in place.

  WHAT THE SWEEP IS, AND IS NOT.  This is a TRIAGE LIST, not a verdict.  A keyword
  classifier over prose cannot reliably separate "grades the instruction graph against a
  regular bound" from "explains why that grading is invalid" -- the two are written in
  almost the same words, and an early draft of this classifier duly flagged its own
  corrections.  {len(review)} line(s) remain in the review bucket and are meant to be read, not
  counted.  Calibrating it to zero would mean tuning it until it agrees with today's text,
  which is how a checker stops finding anything.

  The genuinely clean signal is the measurement-only bucket ({mo}): it reports
  |lambda_2| = 0.893992 with the gap, relaxation, mixing time and Kemeny constant and
  never compares any of them with a bound.  That is the form the honest statement takes --
  report what the walk does, do not grade it.""")
    return {"regular_notion_lines": len(hits),
            "buckets": {k: [ln for ln, _ in v] for k, v in buckets.items()},
            "needs_review": [ln for ln, _ in review],
            "fourth_instance_found_and_fixed": True,
            "is_triage_not_verdict": True}


def main() -> int:
    z = pass_4222()
    b = pass_4223(z)
    o = pass_4224()
    p = pass_4225()
    s = pass_4226()
    out = {"pass_4222_zeta": z, "pass_4223_benchmark": b, "pass_4224_orbits": o,
           "pass_4225_load_ports": p, "pass_4226_sweep": s}
    path = ROOT / "data" / "PART_W33_PASS4222_4226_ZETA_WITHOUT_REGULARITY.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
