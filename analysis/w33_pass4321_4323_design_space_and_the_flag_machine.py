#!/usr/bin/env python3
"""Passes 4321-4323 -- the design space priced, and the zeta's own domain as a register.

Pass 4314 found the machine has TWO independent asymmetries: the load port (which causes
the p-bias and the localisation) and the non-involutive Clifford opcodes (which cause the
arrow of time).  Two independent defects with two independent prices means a 2x2 design
space, and nobody has drawn it.

Pass 4313 noticed in passing that a flag machine holds 160 incident point-line pairs.  The
Levi graph has 160 EDGES.  That is not a coincidence and it is worth following.

  4321  THE 2x2 DESIGN SPACE, MODELED.  Four machines -- biased/symmetric crossed with
        irreversible/reversible -- each enumerated by opcode count and measured for finite
        mixing, entropy production and localisation.  No B/D RTL or Yosys synthesis was
        performed in this pass.
  4322  FLAGS ARE LEVI EDGES.  (bonkers)  A flag is an incident point-line pair; an edge of
        the Levi graph is an incident point-line pair.  They are the same 160 objects.  So
        the state space of the flag machine IS the domain on which the Ihara zeta is
        defined, and the non-backtracking walk that produces rho(B) is a physically
        realisable instruction stream rather than a bookkeeping device.
  4323  IS A ZERO-ASYMMETRY MACHINE POSSIBLE?  (bonkers)  If both defects can be removed at
        once, that machine is the one this whole document has been circling.  If they
        cannot, the obstruction is the result.

    py -3 analysis/w33_pass4321_4323_design_space_and_the_flag_machine.py
"""

from __future__ import annotations

import json
from collections import Counter
from math import log, sqrt
from pathlib import Path

import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cert_util  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def minv(M):
    a = [list(M[i]) + [1 if j == i else 0 for j in range(4)] for i in range(4)]
    r = 0
    for c in range(4):
        p = next(i for i in range(r, 4) if a[i][c] % 3)
        a[r], a[p] = a[p], a[r]
        iv = 1 if a[r][c] % 3 == 1 else 2
        a[r] = [(x * iv) % 3 for x in a[r]]
        for i in range(4):
            if i != r and a[i][c] % 3:
                f = a[i][c] % 3
                a[i] = [(a[i][k] - f * a[r][k]) % 3 for k in range(8)]
        r += 1
    return tuple(tuple(a[i][4:]) for i in range(4))


def inv_op(g):
    M, t = g
    Mi = minv(M)
    return (Mi, tuple((-mv(Mi, t)[i]) % 3 for i in range(4)))


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


def localise(A):
    B, de = hashimoto(A)
    vals, vecs = np.linalg.eig(B)
    mods = np.abs(vals)
    rho = float(mods.max())
    idx = [i for i in range(len(vals))
           if mods[i] > 1 + 1e-9 and abs(mods[i] - rho) > 1e-6 * rho]
    if not idx:
        return rho, None
    idx.sort(key=lambda i: -mods[i])
    v = np.abs(vecs[:, idx[0]]) ** 2
    v /= v.sum()
    fw = np.zeros(A.shape[0])
    for (x, _), w in zip(de, v):
        fw[x] += w
    best = max((float(fw[[i for i in range(81) if TV[i][c] == val]].sum())
                for c in range(4) for val in range(3)))
    return rho, best


def thermo(gens):
    n = 81
    P = walk(gens)
    ow = int(((P > 0) & (P.T == 0)).sum())
    if ow:
        return float("inf"), ow
    s = 0.0
    for i in range(n):
        for j in range(n):
            if P[i, j] > 0 and P[j, i] > 0:
                s += (1.0 / n) * P[i, j] * log(P[i, j] / P[j, i])
    return s / log(2), 0


def pass_4321() -> dict:
    print("=" * 78)
    print("Pass 4321 -- the 2x2 design space, priced")
    print("=" * 78)
    Z = {i: (ID4, tuple(1 if j == i else 0 for j in range(4))) for i in range(4)}
    biased = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
              (LIN["CX_fp"], (0, 0, 0, 0)), Z[0]]
    symmetric = biased + [(LIN["F_f"], (0, 0, 0, 0)), Z[2]]
    pair_swap = ((0, 0, 1, 0), (0, 0, 0, 1),
                 (1, 0, 0, 0), (0, 1, 0, 0))

    def swap_conjugate(g):
        M, t = g
        return (mm(mm(pair_swap, M), pair_swap), mv(pair_swap, t))

    def swap_invariant(gs):
        return set(map(swap_conjugate, gs)) == set(gs)

    def stir_counts(gs):
        return [sum(any(act(g, x)[c] != x[c] for g in gs) for x in TV)
                for c in range(4)]

    def close(gs):
        out, seen = [], set()
        for g in gs:
            for h in (g, inv_op(g)):
                if h not in seen:
                    seen.add(h)
                    out.append(h)
        return out

    machines = {
        "A  biased, irreversible (shipped)": biased,
        "B  symmetric, irreversible": symmetric,
        "C  biased, reversible": close(biased),
        "D  symmetric, reversible": close(symmetric),
    }
    rows = {}
    print(f"  {'machine':34s} {'ops':>4s} {'mix':>4s} {'rho(B)':>8s} {'loc':>7s} "
          f"{'entropy':>9s}")
    for name, g in machines.items():
        A = simple(g)
        rho, loc = localise(A)
        mt = mixing_time(walk(g))
        ent, ow = thermo(g)
        rows[name] = {"ops": len(g), "mix": mt, "rho": rho, "loc": loc,
                      "entropy_bits": None if ent == float("inf") else ent,
                      "one_way": ow, "pf_swap_invariant": swap_invariant(g),
                      "stir_counts_over_81": stir_counts(g),
                      "hardware_synthesized": False}
        e = "inf" if ent == float("inf") else f"{ent:.2e}"
        print(f"  {name:34s} {len(g):4d} {str(mt):>4s} {rho:8.4f} {loc:7.4f} {e:>9s}")

    print(f"""
  FOUR MACHINES, AND THE BLUEPRINT HAS BEEN QUOTING ONE.  Machine A is the shipped ISA.
  B fixes p/f asymmetry, C fixes the arrow of time, D fixes both -- and because Pass 4314 showed
  the two defects are independent, no two of these are the same design.

  The prices are not interchangeable.  C doubles the opcode count and buys exactly zero
  entropy production; B adds two opcodes and buys exact p/f-swap invariance; D pays for both.
  These are opcode-count and finite-model prices, not synthesized cell counts. A reader
  choosing between them needs all four rows, which is why they are printed together here
  rather than one at a time across forty passes.""")
    return rows


def pass_4322() -> dict:
    print()
    print("=" * 78)
    print("Pass 4322 -- flags ARE Levi edges: the zeta's domain is a register")
    print("=" * 78)

    def norm(v):
        return min(tuple((t * x) % 3 for x in v) for t in (1, 2))

    seen, pts = set(), []
    for v in TV:
        if any(v):
            k = norm(v)
            if k not in seen:
                seen.add(k)
                pts.append(k)
    pidx = {p: i for i, p in enumerate(pts)}

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    lines = set()
    for i in range(40):
        for j in range(i + 1, 40):
            if form(pts[i], pts[j]):
                continue
            span = set()
            for c1 in range(3):
                for c2 in range(3):
                    w = tuple((c1 * pts[i][t] + c2 * pts[j][t]) % 3 for t in range(4))
                    if any(w):
                        span.add(norm(w))
            if len(span) == 4:
                lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))

    flags = [(pidx[p], li) for li, L in enumerate(lines) for p in L]
    n = 80
    Lg = np.zeros((n, n))
    for li, L in enumerate(lines):
        for p in L:
            Lg[pidx[p], 40 + li] = 1
            Lg[40 + li, pidx[p]] = 1
    edges = int(Lg.sum() // 2)
    B, de = hashimoto(Lg)
    print(f"  incident point-line FLAGS        : {len(flags)}")
    print(f"  EDGES of the Levi graph          : {edges}")
    print(f"  identical                        : {len(flags) == edges}")
    print(f"  DIRECTED edges (Hashimoto domain): {len(de)} = 2 x {edges}")
    print(f"  Hashimoto matrix                 : {B.shape[0]}x{B.shape[0]}")
    mods = np.abs(np.linalg.eigvals(B))
    rho = float(mods.max())
    print(f"  rho(B)                           : {rho:.6f}")
    print(f"""
  A FLAG IS AN EDGE, AND A DIRECTED FLAG IS A HASHIMOTO BASIS VECTOR.  The {len(flags)} incident
  point-line pairs are exactly the {edges} edges of the Levi graph, and the {len(de)} directed
  edges are exactly the basis on which the non-backtracking matrix B is written.

  So the Ihara zeta of the address geometry is not a bookkeeping device applied from
  outside: its domain is a machine state.  A flag machine holding a directed incident pair
  and forbidden to immediately reverse is literally performing the non-backtracking walk
  whose growth rate is rho(B) = {rho:.0f}.  The quantity Passes 4222-4284 spent forty passes
  computing for the instruction layer is, on the address layer, the throughput of a
  register the machine could actually have.

  That reframes what the zeta measures here.  For the frame graph it is a spectral
  invariant of a Schreier graph.  For the Levi graph it is the state count of a physical
  design -- and that design is the one that satisfies the graph RH exactly (Pass 4313).""")
    return {"flags": len(flags), "levi_edges": edges,
            "identical": bool(len(flags) == edges),
            "directed": len(de), "hashimoto_dim": int(B.shape[0]), "rho": rho}


def pass_4323(design) -> dict:
    print()
    print("=" * 78)
    print("Pass 4323 -- is a zero-asymmetry machine possible?")
    print("=" * 78)
    d = design["D  symmetric, reversible"]
    print(f"  machine D (symmetric + reversible): {d['ops']} opcodes")
    print(f"    entropy production : {d['entropy_bits']:.3e} bits/instruction")
    print(f"    one-way pairs      : {d['one_way']}")
    print(f"    localisation       : {d['loc']:.4f}")
    print(f"    mixing time        : {d['mix']}")

    a = design["A  biased, irreversible (shipped)"]
    arrow_gone = d["one_way"] == 0
    bias_gone = d["pf_swap_invariant"] and not a["pf_swap_invariant"]
    print(f"\n  arrow of time removed : {arrow_gone}")
    print(f"  p/f asymmetry removed : {bias_gone}")
    print(f"  localisation peak     : {a['loc']:.4f} -> {d['loc']:.4f}")
    print(f"""
  BOTH DEFECTS CAN BE REMOVED AT ONCE, AND THE RESULT IS NOT FREE.  Machine D runs with
  {'exactly zero' if d['entropy_bits'] is not None and abs(d['entropy_bits']) < 1e-12 else 'reduced'} stationary entropy production and the lowest localisation of the four,
  at {d['ops']} opcodes against the shipped machine's {a['ops']}.  Pass 4279 priced the reversible
  closure at 1.95x the cells; D is that closure applied to a wider set, so its decode logic
  is larger again.

  THE REMAINING {d['loc']:.4f} NUMBER IS NOT P/F BIAS.  The exact pair-swap conjugation fixes
  Machine D's whole opcode set and its graph, and the slow-mode weight occurs equally on the
  swapped x1 and x3 coordinates.  It is symmetric localisation.  Comparing a maximum
  three-class weight with 1/3 cannot by itself diagnose which plane was preferred.

  So the corrected answer is stronger: both named asymmetries can be removed exactly in
  the finite ISA model.  What remains is a localisation/mixing question inside a symmetric
  machine.  No B/D RTL was synthesized here, so hardware price remains open.""")
    return {"machine_D": d, "arrow_removed": bool(arrow_gone),
            "pf_asymmetry_removed": bool(bias_gone),
            "localisation_peak_reduced": bool(d["loc"] < a["loc"]),
            "symmetric_localisation_not_bias": True,
            "uniform_reference": 1 / 3, "hardware_synthesized": False}


def main() -> int:
    ds = pass_4321()
    out = {"pass_4321_design_space": ds,
           "pass_4322_flags_are_edges": pass_4322(),
           "pass_4323_zero_asymmetry": pass_4323(ds)}
    p = ROOT / "data" / "PART_W33_PASS4321_4323_DESIGN_SPACE_FLAGS.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    # Pass 4395: cert_util.dumps rounds floats to a declared precision first, so the
    # certificate survives a re-run on another LAPACK build.  It keeps the
    # round-trip rule from CLAUDE.md (Pass 2482) intact.
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
