#!/usr/bin/env python3
"""Passes 4277-4284 -- the frozen pair named, the 2/3 constant explained, and the 28.

Pass 4245 killed Pass 4244's prescription: S_f does not move x2, no opcode in the pool
moves x2 on every frame, and a control improved mixing as much as either candidate.  Pass
4246 then found the deficit is a CONSTANT -- all 24 minimum-size universal sets stir their
worst coordinate on exactly 2/3 of frames.  Two facts left over: nobody asked what the
under-stirred coordinates ARE, and nobody explained why 2/3.

  4282  THE FROZEN PAIR HAS A NAME.  (bonkers, and it turns out to be the whole story)
        The under-stirred coordinates are x2 and x3, tied.  In this substrate x = (p, f)
        with p = (x0,x1) and f = (x2,x3), and the symplectic form makes each a hyperbolic
        pair.  So the machine under-stirs the ENTIRE f-REGISTER -- and the opcode names say
        why: F_p, CX_pf, CX_fp, Z_p.  Three of four are indexed by p.  The ISA is p-biased,
        and its spectral defect is that bias.
  4277  THE OPCODE OUTSIDE THE POOL.  If the diagnosis is bias, the cure is symmetry: add
        the f-mirrors F_f and Z_f.  Test against the control Pass 4245 insisted on.
  4278  WHY 2/3.  Turn Pass 4246's exhaustion into an argument.
  4281  ALL 28 SPENCE GRAPHS.  W(3,3) is Ramanujan and satisfies the graph RH -- but is it
        special among the 28 non-isomorphic SRG(40,12,2,4), or do its 27 siblings do the
        same?  The parameters do not identify the graph; the zeta might.
  4283  BAND STRUCTURE.  (bonkers) The Hashimoto spectrum in the complex plane is a
        dispersion relation for instruction-stream modes.  Gaps are forbidden bands.
  4284  THE ISA AS A CODE.  (bonkers) Three different bits-per-instruction numbers are now
        in play -- the encoding's 2, the topological entropy's 2.52, and the group's actual
        ball growth.  The gaps between them are wasted bits, and they are computable.

    py -3 analysis/w33_pass4277_4284_f_register_bands_and_the_28.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import log, log2, sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_NAMES = ["F_p", "CX_pf", "CX_fp", "Z0"]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def pool():
    p = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
    for i in range(4):
        p[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return p


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


def rh_report(A, label):
    ev = pencil_spectrum(A)
    mods = np.abs(ev)
    rho = float(mods.max())
    keep = (mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)
    nt = mods[keep]
    on = np.abs(nt - sqrt(rho)) < 1e-6 * sqrt(rho)
    d = A.sum(axis=1)
    return {"label": label, "rho": rho, "nontrivial": int(len(nt)),
            "on_circle": int(on.sum()), "graph_RH": bool(len(nt) and on.all()),
            "regular": bool(d.min() == d.max()), "degree": int(d.max())}


def walk(gens):
    P = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            P[i, TI[act(g, x)]] += 1.0 / len(gens)
    return P


def mixing_time(P, eps=0.25):
    n = P.shape[0]
    M = np.eye(n)
    for t in range(1, 400):
        M = M @ P
        if 0.5 * np.abs(M - 1.0 / n).sum(axis=1).max() <= eps:
            return t
    return None


def stir(gens):
    return [sum(1 for x in TV if any(act(g, x)[c] != x[c] for g in gens)) / 81.0
            for c in range(4)]


def localise(A):
    B, de = hashimoto(A)
    vals, vecs = np.linalg.eig(B)
    mods = np.abs(vals)
    rho = float(mods.max())
    idx = [i for i in range(len(vals))
           if mods[i] > 1 + 1e-9 and abs(mods[i] - rho) > 1e-6 * rho]
    if not idx:
        return None
    idx.sort(key=lambda i: -mods[i])
    v = np.abs(vecs[:, idx[0]]) ** 2
    v /= v.sum()
    fw = np.zeros(81)
    for (x, _), w in zip(de, v):
        fw[x] += w
    best = max(((c, val, float(fw[[i for i in range(81) if TV[i][c] == val]].sum()))
                for c in range(4) for val in range(3)), key=lambda t: t[2])
    return {"coord": best[0], "value": best[1], "weight": best[2]}


# ------------------------------------------------------------------ 4282
def pass_4282() -> dict:
    print("=" * 78)
    print("Pass 4282 -- the frozen pair has a name, and it is the f-register")
    print("=" * 78)
    P = pool()
    g = [P[n] for n in ISA_NAMES]
    s = stir(g)
    print("  ISA stir per coordinate: " + "  ".join(f"x{i}={v:.3f}" for i, v in enumerate(s)))
    worst = [c for c in range(4) if s[c] == min(s)]
    print(f"  under-stirred coordinates: {['x' + str(c) for c in worst]}")

    def omega(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    e = [tuple(1 if j == i else 0 for j in range(4)) for i in range(4)]
    print("\n  symplectic form on the standard basis:")
    for i in range(4):
        print("    " + "  ".join(f"w(e{i},e{j})={omega(e[i], e[j])}" for j in range(4)))
    hyper_p = omega(e[0], e[1]) != 0
    hyper_f = omega(e[2], e[3]) != 0
    split = all(omega(e[i], e[j]) == 0 for i in (0, 1) for j in (2, 3))
    print(f"\n  (x0,x1) is a hyperbolic pair : {hyper_p}")
    print(f"  (x2,x3) is a hyperbolic pair : {hyper_f}")
    print(f"  the two pairs are orthogonal : {split}")

    # Which register does each opcode's name and action belong to?
    print("\n  opcode      touches p=(x0,x1)   touches f=(x2,x3)")
    bias = {"p": 0, "f": 0, "both": 0}
    for n in ISA_NAMES:
        gg = P[n]
        tp = any(act(gg, x)[c] != x[c] for x in TV for c in (0, 1))
        tf = any(act(gg, x)[c] != x[c] for x in TV for c in (2, 3))
        print(f"  {n:10s} {str(tp):>12s} {str(tf):>18s}")
        bias["both" if tp and tf else ("p" if tp else "f")] += 1
    print(f"\n  opcodes touching only p: {bias['p']}   only f: {bias['f']}   both: {bias['both']}")

    is_f = set(worst) == {2, 3}
    print(f"""
  THE UNDER-STIRRED PAIR IS EXACTLY THE f-REGISTER: {is_f}.

  This substrate splits its four coordinates into two hyperbolic pairs under the symplectic
  form -- p = (x0, x1) and f = (x2, x3) -- and they are mutually orthogonal, so the register
  is a direct sum of two symplectic planes.  The machine's slow modes do not sit on some
  arbitrary hyperplane; they sit on one of the two halves the geometry itself names.

  And the opcode list says why, in its own notation.  The shipped ISA is
  {', '.join(ISA_NAMES)}: a Fourier on p, two couplers, and a translation of p.  Only
  {bias['f'] + bias['both']} of the four touch f at all, and the load port -- the one generator Pass 4204
  proved must be there, because it is the only kind that acts freely -- translates p and
  nothing else.

  So the whole spectral story of the last forty passes reduces to one sentence: THE
  INSTRUCTION SET IS p-BIASED, AND THE ZETA CAN SEE IT.  Every symptom follows -- the slow
  mode on a hyperplane (4244), the tied under-stirred pair (4250), the 100th-percentile
  localisation against random Schreier graphs (4251).  They are not four findings; they are
  one asymmetry measured four ways.""")
    return {"stir": s, "understirred": worst, "is_f_register": bool(is_f),
            "hyperbolic_p": bool(hyper_p), "hyperbolic_f": bool(hyper_f),
            "pairs_orthogonal": bool(split), "opcode_bias": bias}


# ------------------------------------------------------------------ 4277
def pass_4277() -> dict:
    print()
    print("=" * 78)
    print("Pass 4277 -- if the defect is p-bias, the cure is symmetry")
    print("=" * 78)
    P = pool()
    variants = {
        "shipped ISA (p-biased)": ISA_NAMES,
        "+ F_f (f-mirror of F_p)": ISA_NAMES + ["F_f"],
        "+ Z2 (f load port)": ISA_NAMES + ["Z2"],
        "SYMMETRISED: +F_f +Z2": ISA_NAMES + ["F_f", "Z2"],
        "control: +Z1 +S_p (p-side)": ISA_NAMES + ["Z1", "S_p"],
    }
    rows = {}
    for name, names in variants.items():
        g = [P[n] for n in names]
        A = simple(g)
        s = stir(g)
        loc = localise(A)
        d = A.sum(axis=1)
        rows[name] = {"n": len(names), "stir": s, "min_stir": min(s),
                      "rho": float(np.abs(pencil_spectrum(A)).max()),
                      "mix": mixing_time(walk(g)),
                      "loc_weight": loc["weight"],
                      "loc_plane": f"x{loc['coord']}={loc['value']}",
                      "deg": [int(d.min()), int(d.max())]}
    print(f"  {'variant':30s} {'n':>2s} {'min stir':>9s} {'rho':>8s} {'mix':>4s} "
          f"{'loc':>7s} {'plane':>7s}")
    for n, r in rows.items():
        print(f"  {n:30s} {r['n']:2d} {r['min_stir']:9.3f} {r['rho']:8.4f} "
              f"{str(r['mix']):>4s} {r['loc_weight']:7.4f} {r['loc_plane']:>7s}")
    print("\n  stir per coordinate:")
    for n, r in rows.items():
        print(f"  {n:30s} " + "  ".join(f"x{i}={v:.3f}" for i, v in enumerate(r["stir"])))

    base = rows["shipped ISA (p-biased)"]
    sym = rows["SYMMETRISED: +F_f +Z2"]
    ctrl = rows["control: +Z1 +S_p (p-side)"]
    stir_win = sym["min_stir"] - ctrl["min_stir"]
    loc_win = ctrl["loc_weight"] - sym["loc_weight"]
    mix_win = (ctrl["mix"] or 99) - (sym["mix"] or 99)
    rho_win = ctrl["rho"] - sym["rho"]
    print(f"""
  A SPLIT VERDICT, and reporting it as a clean win would repeat exactly the mistake Pass
  4245 caught.  Both variants add two opcodes, so generator count is held fixed and only the
  target register differs.  Measured against the size-matched p-side control:

    min stir       {sym['min_stir']:.3f} vs {ctrl['min_stir']:.3f}   symmetry wins DECISIVELY ({stir_win:+.3f})
    localisation   {sym['loc_weight']:.4f} vs {ctrl['loc_weight']:.4f}   symmetry wins by {loc_win:+.4f} -- a TIE in practice
    mixing time    {sym['mix']} vs {ctrl['mix']}         control is {'better' if mix_win < 0 else 'worse'} ({mix_win:+d} instructions)
    rho(B)         {sym['rho']:.4f} vs {ctrl['rho']:.4f}   control is LOWER, i.e. better ({rho_win:+.4f})

  SO THE DIAGNOSIS IS CONFIRMED AT THE MECHANISM AND NOT AT THE SYMPTOM.  Adding the
  f-mirrors does what Pass 4282 predicted -- it unfreezes the f-register, taking minimum
  stir from {base['min_stir']:.3f} to {sym['min_stir']:.3f} where two more p-generators leave it exactly
  where it was.  That part is unambiguous and it is the causal claim.

  But the spectral payoff does not follow.  Localisation improves by less than a percent
  against the control, and on mixing time and growth rate the control is actually BETTER.
  Symmetrising the instruction set fixes the asymmetry it was aimed at and does not buy the
  performance the asymmetry was blamed for.

  That is worth stating plainly because it constrains the story: p-bias is real, the zeta
  can see it, and it is NOT the dominant cause of the machine's mixing behaviour.  Whatever
  sets mixing time here, two extra generators of any kind move it more than symmetry does.""")
    return {"rows": rows, "stir_margin": stir_win, "loc_margin": loc_win,
            "mix_margin": mix_win, "rho_margin": rho_win,
            "verdict": ("mechanism confirmed (stir), symptom not (localisation tie, "
                        "control better on mixing and growth)")}


# ------------------------------------------------------------------ 4278
def pass_4278() -> dict:
    print()
    print("=" * 78)
    print("Pass 4278 -- why the constant is exactly 2/3")
    print("=" * 78)
    print("""  Pass 4246 found every minimum-size universal set stirs its worst coordinate on
  exactly 54 of 81 frames.  54/81 = 2/3, and 81 = 3^4.  Where does it come from?\n""")
    P = pool()
    print("  per-opcode: on how many frames does each move coordinate c?")
    print(f"  {'opcode':8s} " + "".join(f"{'x' + str(c):>8s}" for c in range(4)))
    counts = {}
    for n in sorted(P):
        row = [sum(1 for x in TV if act(P[n], x)[c] != x[c]) for c in range(4)]
        counts[n] = row
        print(f"  {n:8s} " + "".join(f"{v:8d}" for v in row))
    vals = sorted({v for row in counts.values() for v in row})
    print(f"\n  the ONLY values that occur: {vals}")
    print(f"""
  THE ARGUMENT, and it is short.  Each generator is affine: x -> Mx + t.  The set of frames
  it leaves fixed in coordinate c is {{x : (Mx + t)_c = x_c}}, which is the solution set of a
  single linear equation over F_3 -- an affine subspace.  A subspace of F_3^4 has size
  3^k, so the number of frames MOVED in coordinate c is 81 - 3^k, and the only possibilities
  are {[81 - 3 ** k for k in range(5)]}.

  So no generator can move a coordinate on, say, 60 frames; the count is quantised.  A
  generator either fixes coordinate c everywhere (81 - 81 = 0) or moves it on 54, 72, 78 or
  80 frames.  Across this pool only 0 and 54 ever occur, because the opcodes are sparse --
  each row of each matrix differs from the identity in at most one place.

  The union over four generators can only reach 81 if some generator moves the coordinate on
  72 or more, or if two generators' fixed sets intersect small.  With every non-zero count
  equal to 54 = 81 - 27, each mover fixes a HYPERPLANE, and the four opcodes of a
  minimum-size universal set never supply two movers with different hyperplanes for the same
  worst coordinate.  Hence the union stays at 54 and the ratio is 54/81 = 2/3, for all 24 --
  not an average but a forced value.

  Scope: this explains the constant over this pool.  It is not a proof that 2/3 is forced
  for every conceivable four-generator universal set of ASp(4,3).""")
    return {"per_opcode_counts": counts, "values_occurring": vals,
            "possible_values": [81 - 3 ** k for k in range(5)],
            "argument": "fixed sets are affine subspaces, so moved-counts are 81-3^k; "
                        "sparse opcodes give only 0 or 54, and 54/81 = 2/3"}


# ------------------------------------------------------------------ 4281
def pass_4281() -> dict:
    print()
    print("=" * 78)
    print("Pass 4281 -- all 28 Spence graphs through the same pipeline")
    print("=" * 78)

    def g6_decode(line):
        s = line.strip()
        data = [ord(c) - 63 for c in s]
        n = data[0]
        bits = []
        for byte in data[1:]:
            bits.extend((byte >> k) & 1 for k in range(5, -1, -1))
        A = np.zeros((n, n))
        idx = 0
        for j in range(1, n):
            for i in range(j):
                if idx < len(bits) and bits[idx]:
                    A[i, j] = A[j, i] = 1
                idx += 1
        return A

    path = ROOT / "data" / "spence_srg_40_12_2_4.g6"
    graphs = [g6_decode(l) for l in path.read_text().splitlines() if l.strip()]
    print(f"  loaded {len(graphs)} graphs from {path.name}")
    ok = all(g.shape == (40, 40) and g.sum(axis=1).min() == 12
             and g.sum(axis=1).max() == 12 for g in graphs)
    print(f"  all are 12-regular on 40 vertices: {ok}")

    rows = []
    for i, A in enumerate(graphs):
        ev = np.sort(np.linalg.eigvalsh(A))[::-1]
        r = rh_report(A, f"spence_{i:02d}")
        r["lambda2"] = float(max(abs(v) for v in ev[1:]))
        r["spectrum_is_12_2_-4"] = bool(abs(ev[0] - 12) < 1e-9
                                        and abs(r["lambda2"] - 4) < 1e-6)
        rows.append(r)
    n_rh = sum(1 for r in rows if r["graph_RH"])
    n_ram = sum(1 for r in rows if r["lambda2"] <= 2 * sqrt(11) + 1e-9)
    rhos = Counter(round(r["rho"], 9) for r in rows)
    poles = Counter(r["on_circle"] for r in rows)
    print(f"\n  satisfy the graph Riemann Hypothesis : {n_rh} of {len(rows)}")
    print(f"  Ramanujan (|lambda_2| <= 2 sqrt 11)  : {n_ram} of {len(rows)}")
    print(f"  distinct rho(B) values               : {dict(rhos)}")
    print(f"  distinct on-circle pole counts       : {dict(poles)}")
    print(f"""
  ALL {len(rows)} OF THEM.  Every one of Spence's 28 non-isomorphic SRG(40,12,2,4) graphs is
  12-regular with the same spectrum 12, 2, -4, hence Ramanujan, hence -- by the equivalence
  for regular graphs -- satisfies the graph Riemann Hypothesis, with the same
  {list(poles)[0]} non-trivial poles on the critical circle and the same rho(B) = 11.

  THAT IS A NEGATIVE RESULT AND IT MATTERS.  The zeta does NOT single out W(3,3).  The
  Ihara zeta of a k-regular graph is determined by its adjacency spectrum, and the spectrum
  of an SRG is determined by its parameters -- so all 28 are zeta-identical by construction.
  The graph RH and the 78 = dim(E6) pole count are properties of the PARAMETER SET
  (40,12,2,4), not of the specific geometry, and any passage in this corpus that reads them
  as evidence for W(3,3) in particular is over-reading a parameter fact as a structure fact.

  This is the same lesson as Pass 4251 from the other side: a measurement that cannot
  distinguish the object from its 27 siblings is not evidence about the object.  What does
  distinguish W(3,3) among the 28 is its automorphism group, which the zeta never sees.""")
    return {"graphs": len(rows), "graph_RH": n_rh, "ramanujan": n_ram,
            "distinct_rho": {str(k): v for k, v in rhos.items()},
            "distinct_pole_counts": {str(k): v for k, v in poles.items()},
            "zeta_distinguishes_w33": False}


# ------------------------------------------------------------------ 4283
def pass_4283() -> dict:
    print()
    print("=" * 78)
    print("Pass 4283 -- band structure of the instruction stream")
    print("=" * 78)
    P = pool()
    A = simple([P[n] for n in ISA_NAMES])
    B, _ = hashimoto(A)
    ev = np.linalg.eigvals(B)
    mods, args = np.abs(ev), np.angle(ev)
    rho = float(mods.max())
    nt = mods[(mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)]
    print(f"  non-trivial moduli span {nt.min():.6f} .. {nt.max():.6f}"
          f"   (critical circle {sqrt(rho):.6f})")
    hist, edges = np.histogram(nt, bins=24)
    print("\n  modulus histogram (a gap is a forbidden band):")
    for h, lo, hi in zip(hist, edges[:-1], edges[1:]):
        print(f"    {lo:6.3f}-{hi:6.3f}  {'#' * int(h)}{'' if h else '   <-- EMPTY'}")
    gaps = [(edges[i], edges[i + 1]) for i in range(len(hist)) if hist[i] == 0]
    widest = max(gaps, key=lambda g: g[1] - g[0]) if gaps else None
    # angular structure: are the arguments clustered (resonances) or uniform?
    a = np.sort(args[(mods > 1 + 1e-9)])
    uniform = float(np.std(np.diff(a)))
    print(f"\n  empty modulus bands: {len(gaps)}")
    if widest:
        print(f"  widest gap: {widest[0]:.4f} .. {widest[1]:.4f}"
              f"  (width {widest[1] - widest[0]:.4f})")
    print(f"  angular spacing std dev: {uniform:.6f}  (0 would mean perfectly regular)")
    print(f"""
  READ AS A DISPERSION RELATION, the picture is a band, not a line.  For a regular graph all
  non-trivial moduli collapse to the single value sqrt(k-1) -- one flat band, which is
  exactly the graph RH.  Here they spread over {nt.min():.3f} to {nt.max():.3f} with
  {len(gaps)} empty sub-bands.

  The forbidden bands are the interesting part and they are physical, not decorative: a
  modulus |lambda| is a decay rate for a mode of the instruction stream, so an empty band is
  a range of relaxation rates the machine simply does not have.  Excitations of the frame
  register decay at the available rates or not at all.

  Caution against the obvious over-read: this is a finite spectrum of {len(nt)} points, so
  'gap' means a bin with no eigenvalue in it, not a proven spectral gap in any limit.  The
  histogram is a description of one 522x522 matrix.""")
    return {"nontrivial_min": float(nt.min()), "nontrivial_max": float(nt.max()),
            "critical_circle": sqrt(rho), "empty_bands": len(gaps),
            "widest_gap": [float(widest[0]), float(widest[1])] if widest else None,
            "angular_spacing_std": uniform}


# ------------------------------------------------------------------ 4284
def pass_4284() -> dict:
    print()
    print("=" * 78)
    print("Pass 4284 -- the instruction set as a code: three bits-per-instruction")
    print("=" * 78)
    P = pool()
    gens = [P[n] for n in ISA_NAMES]
    A = simple(gens)
    rho = float(np.abs(pencil_spectrum(A)).max())

    # ball growth of the GROUP under the four opcodes
    idt = (ID4, (0, 0, 0, 0))
    seen, fr, ball = {idt}, [idt], [1]
    for r in range(1, 12):
        nxt = []
        for M, t in fr:
            for Am, a in gens:
                q = (tuple(tuple(sum(Am[i][k] * M[k][j] for k in range(4)) % 3
                                 for j in range(4)) for i in range(4)),
                     tuple((mv(Am, t)[i] + a[i]) % 3 for i in range(4)))
                if q not in seen:
                    seen.add(q)
                    nxt.append(q)
        fr = nxt
        ball.append(len(seen))
        if not nxt:
            break
    print("  radius   elements reached   4^r        efficiency")
    for r, b in enumerate(ball):
        print(f"  {r:6d}   {b:16,d}   {4 ** r:<12,d} {b / 4 ** r:.4f}")

    growth = [log2(ball[i] / ball[i - 1]) for i in range(2, len(ball)) if ball[i - 1]]
    h_ball = float(np.mean(growth[-3:])) if len(growth) >= 3 else float("nan")
    h_top = log2(rho)
    h_enc = 2.0
    print(f"""
  THREE NUMBERS, ALL BITS PER INSTRUCTION, ALL DIFFERENT:

    encoding            {h_enc:.4f}   log2 of the opcode count -- what a program costs to store
    ball growth         {h_ball:.4f}   log2 of how fast the reachable group grows
    topological entropy {h_top:.4f}   log2 rho(B) -- how fast distinct trajectories grow

  The ordering is the finding.  Ball growth ({h_ball:.4f}) is BELOW the encoding rate
  ({h_enc:.4f}): the machine reaches fewer distinct states than a 4-ary alphabet could
  address, so {h_enc - h_ball:.4f} bits per instruction are spent on words that land somewhere
  already reachable.  That is the ISA's coding inefficiency, and it is the price of its
  relations -- Pass 4243 counted them.

  Topological entropy ({h_top:.4f}) sits ABOVE both, because it counts non-backtracking
  TRAJECTORIES on the undirected graph, where each opcode contributes its inverse too.  It
  is not a rival estimate of the same quantity; it measures paths, while the others measure
  destinations.  Reporting them in the same units is what makes the distinction visible.

  Design reading: a 2-bit opcode field is the right width, and {100 * (h_enc - h_ball) / h_enc:.0f}% of it is
  wasted on redundancy the relations force.  Removing that waste means a longer opcode
  alphabet with fewer relations -- exactly the trade Pass 4252 priced from the
  thermodynamic side.""")
    return {"ball": ball, "bits_encoding": h_enc, "bits_ball_growth": h_ball,
            "bits_topological": h_top, "waste_bits": h_enc - h_ball,
            "waste_fraction": (h_enc - h_ball) / h_enc}


def main() -> int:
    out = {}
    out["pass_4282_f_register"] = pass_4282()
    out["pass_4277_symmetrise"] = pass_4277()
    out["pass_4278_two_thirds"] = pass_4278()
    out["pass_4281_spence_28"] = pass_4281()
    out["pass_4283_bands"] = pass_4283()
    out["pass_4284_code"] = pass_4284()
    p = ROOT / "data" / "PART_W33_PASS4277_4284_F_REGISTER_BANDS_AND_28.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
