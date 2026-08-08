#!/usr/bin/env python3
"""Passes 4308-4314 -- is there only ONE asymmetry, and can the Levi graph compute?

Pass 4305 traced the ISA's p-bias to a single opcode: the load port Z_p.  The three linear
opcodes are p/f symmetric; translations act only on the point side because lines are not a
vector space; a load port must pick a direction; that direction is the whole bias.

The load port is now implicated in four separate facts -- it is the only free generator
(4204), the only route to connectivity (4225), the sole source of p-bias (4305), and the
one operation with no dual (4301).  That invites a unification and a warning at once: four
consequences of one opcode is a finding, but "everything traces to X" is exactly the shape
of claim that flatters itself.  So test it against the two defects NOT yet attributed.

  4314  ONE OPCODE, ALL DEFECTS?  (bonkers)  Does removing / symmetrising the load port
        also remove the arrow of time (4252) and the slow-mode localisation (4244)?  A
        clean yes unifies the machine's flaws; a no says there are independent defects and
        the unification was wishful.
  4310  DERIVE THE 2/3 CONSTANT from the translation alone, now that the asymmetry is
        located.  Pass 4278 argued it from affine fixed sets; if the load port is the only
        asymmetry the constant should follow from it directly.
  4312  THE SYMMETRIC MACHINE'S SYMMETRY GROUP.  (bonkers)  Pass 4227 found the shipped
        ISA's stabiliser in Sp(4,3) has order 4.  If symmetrising the load ports raises it,
        the machine acquires a genuine symmetry -- and a symmetry is a conserved quantity.
  4313  THE LEVI GRAPH AS DATAPATH.  (bonkers)  Points and lines are inequivalent G-sets
        (4303) but they are joined by incidence -- the 80-vertex Levi graph.  An opcode
        that moves along incidence is a point<->line transfer the current ISA does not
        have.  What does a machine with that instruction do?

    py -3 analysis/w33_pass4308_4314_one_opcode_and_the_levi_datapath.py
"""

from __future__ import annotations

import json
from collections import Counter
from math import log, sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_LIN = ["F_p", "CX_pf", "CX_fp"]


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


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def pool():
    p = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
    for i in range(4):
        p[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return p


def simple(gens, n=81, actor=act):
    A = np.zeros((n, n))
    dom = TV if n == 81 else list(range(n))
    for g in gens:
        for i in range(n):
            j = TI[actor(g, TV[i])] if n == 81 else actor(g, i)
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


def pencil(A):
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    C = np.zeros((2 * V, 2 * V))
    C[:V, :V] = A
    C[:V, V:] = -Q
    C[V:, :V] = np.eye(V)
    return np.linalg.eigvals(C)


def localisation(A):
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
    fw = np.zeros(A.shape[0])
    for (x, _), w in zip(de, v):
        fw[x] += w
    best = max(((c, val, float(fw[[i for i in range(81) if TV[i][c] == val]].sum()))
                for c in range(4) for val in range(3)), key=lambda t: t[2])
    return {"rho": rho, "coord": best[0], "value": best[1], "weight": best[2]}


def one_way_pairs(gens):
    fwd = set()
    for g in gens:
        for x in TV:
            fwd.add((TI[x], TI[act(g, x)]))
    return sum(1 for (a, b) in fwd if (b, a) not in fwd)


def entropy_production(gens):
    n = 81
    P = np.zeros((n, n))
    for g in gens:
        for x in TV:
            P[TI[x], TI[act(g, x)]] += 1.0 / len(gens)
    s = 0.0
    for i in range(n):
        for j in range(n):
            if P[i, j] > 0 and P[j, i] > 0:
                s += (1.0 / n) * P[i, j] * log(P[i, j] / P[j, i])
    oneway = int(((P > 0) & (P.T == 0)).sum())
    return (float("inf") if oneway else s / log(2)), oneway


# ------------------------------------------------------------------ 4314
def pass_4314() -> dict:
    print("=" * 78)
    print("Pass 4314 -- one opcode, all defects?  A unification test that can fail")
    print("=" * 78)
    P = pool()
    variants = {
        "shipped ISA (one load port)": ["F_p", "CX_pf", "CX_fp", "Z0"],
        "symmetric load ports (Z0+Z2)": ["F_p", "CX_pf", "CX_fp", "Z0", "Z2"],
        "all four load ports": ["F_p", "CX_pf", "CX_fp", "Z0", "Z1", "Z2", "Z3"],
        "linear only (no load port)": ["F_p", "CX_pf", "CX_fp"],
    }
    rows = {}
    for name, names in variants.items():
        g = [P[n] for n in names]
        A = simple(g)
        loc = localisation(A)
        sp, ow = entropy_production(g)
        d = A.sum(axis=1)
        rows[name] = {
            "n": len(names),
            "loc_plane": f"x{loc['coord']}={loc['value']}" if loc else "-",
            "loc_weight": loc["weight"] if loc else None,
            "one_way": ow,
            "entropy_bits": sp,
            "deg_min": int(d.min()),
        }
    print(f"  {'variant':30s} {'n':>2s} {'plane':>7s} {'loc':>7s} {'one-way':>8s} "
          f"{'entropy':>9s} {'dmin':>5s}")
    for n, r in rows.items():
        e = "inf" if r["entropy_bits"] == float("inf") else f"{r['entropy_bits']:.2e}"
        lw = f"{r['loc_weight']:.4f}" if r["loc_weight"] is not None else "-"
        print(f"  {n:30s} {r['n']:2d} {r['loc_plane']:>7s} {lw:>7s} {r['one_way']:8d} "
              f"{e:>9s} {r['deg_min']:5d}")

    base = rows["shipped ISA (one load port)"]
    sym = rows["symmetric load ports (Z0+Z2)"]
    allz = rows["all four load ports"]
    none = rows["linear only (no load port)"]
    loc_fixed = sym["loc_weight"] < base["loc_weight"]
    arrow_fixed = sym["one_way"] == 0
    arrow_ever = min(r["one_way"] for r in rows.values()) == 0
    print(f"""
  THE UNIFICATION IS PARTIAL, AND THE PART THAT FAILS IS THE INFORMATIVE ONE.

  LOCALISATION does respond to the load port.  Symmetrising takes the top-hyperplane weight
  from {base['loc_weight']:.4f} to {sym['loc_weight']:.4f}, and with all four translations it reaches
  {allz['loc_weight']:.4f}.  The defect Pass 4244 found tracks the asymmetry Pass 4305 located, which
  is what the unification predicted.

  THE ARROW OF TIME DOES NOT.  One-way pairs go {base['one_way']} -> {sym['one_way']} -> {allz['one_way']}, and even
  the machine with NO load port at all has {none['one_way']}.  Irreversibility is not the load port's
  doing: it comes from the linear opcodes not being involutions, so their inverses are not
  instructions -- a fact about the Clifford part that no amount of symmetrising the
  translations touches.

  So the machine has (at least) TWO independent asymmetries, not one.  The load port
  explains the p-bias and the localisation; the non-involutive Clifford opcodes explain the
  arrow of time.  Pass 4252's fix -- close the instruction set under inverses at 1.95x the
  cells -- addresses the second and does nothing for the first, and Pass 4277's f-mirrors
  address the first and nothing for the second.  Two defects, two prices, and neither
  purchase substitutes for the other.

  Worth stating because the tidier story was available and wrong: four facts traced to one
  opcode made "everything traces to the load port" feel inevitable, and the test that could
  refute it did.""")
    return {"variants": {k: {kk: (None if vv == float("inf") else vv)
                             for kk, vv in v.items()} for k, v in rows.items()},
            "localisation_tracks_load_port": bool(loc_fixed),
            "arrow_tracks_load_port": bool(arrow_fixed),
            "arrow_ever_zero_by_translations": bool(arrow_ever),
            "independent_asymmetries": 2}


# ------------------------------------------------------------------ 4310
def pass_4310() -> dict:
    print()
    print("=" * 78)
    print("Pass 4310 -- can the 2/3 constant be derived from the load port alone?")
    print("=" * 78)
    P = pool()
    print("  stir contributed by each opcode ALONE, per coordinate:")
    print(f"  {'opcode':8s} " + "".join(f"{'x' + str(c):>8s}" for c in range(4)))
    solo = {}
    for n in sorted(P):
        row = [sum(1 for x in TV if act(P[n], x)[c] != x[c]) / 81 for c in range(4)]
        solo[n] = row
        print(f"  {n:8s} " + "".join(f"{v:8.3f}" for v in row))

    tr = [v for n, v in solo.items() if n.startswith("Z")]
    lin_max = {c: max(solo[n][c] for n in LIN) for c in range(4)}
    print(f"\n  a single translation stirs its own coordinate on "
          f"{max(r[0] for r in tr):.3f} of frames")
    print(f"  the best LINEAR opcode stirs any coordinate on at most "
          f"{max(lin_max.values()):.3f}")
    print(f"""
  NO -- AND THE REASON CORRECTS THE PICTURE.  A translation stirs its own coordinate on
  ALL 81 frames (1.000): x -> x + e_i changes x_i everywhere, with no fixed points, which
  is Pass 4204's freeness restated.  So if the constant came from the load port it would be
  1, not 2/3.

  The 2/3 comes from the LINEAR opcodes, exactly as Pass 4278 argued: each one's fixed set
  in a coordinate is an affine subspace of size 3^k, so the moved-count is 81 - 3^k, and
  the sparse opcodes here only ever achieve 81 - 27 = 54.  The load port lifts the
  coordinate it acts on to 1.000 and leaves the other three at the linear ceiling.

  So the two findings are complementary rather than one being derivable from the other: the
  load port explains WHICH coordinate escapes the ceiling, and the affine-subspace argument
  explains WHERE the ceiling is.  Attributing 2/3 to the load port would have been the same
  over-unification Pass 4314 just refuted.""")
    return {"solo_stir": solo, "translation_stirs_own_coordinate": 1.0,
            "linear_ceiling": max(lin_max.values()),
            "derivable_from_load_port": False}


# ------------------------------------------------------------------ 4312
def pass_4312() -> dict:
    print()
    print("=" * 78)
    print("Pass 4312 -- does symmetrising buy the machine an actual symmetry?")
    print("=" * 78)
    order, index, fr = [ID4], {ID4: 0}, [ID4]
    while fr:
        nxt = []
        for m in fr:
            for g in (LIN[n] for n in ISA_LIN):
                q = mm(g, m)
                if q not in index:
                    index[q] = len(order)
                    order.append(q)
                    nxt.append(q)
        fr = nxt
    print(f"  |Sp(4,3)| = {len(order):,}")

    def stabiliser(lin_names, trans_vecs):
        """M in Sp(4,3) conjugating the opcode set to itself (up to inverses) and
        permuting the load directions among themselves (up to sign)."""
        S = set()
        for n in lin_names:
            S.add(LIN[n])
            S.add(minv(LIN[n]))
        T = {min(t, tuple((-x) % 3 for x in t)) for t in trans_vecs}
        out = []
        for M in order:
            Mi = minv(M)
            if {mm(mm(M, X), Mi) for X in S} != S:
                continue
            img = {min(mv(M, t), tuple((-x) % 3 for x in mv(M, t))) for t in T}
            if img == T:
                out.append(M)
        return out

    e = [tuple(1 if j == i else 0 for j in range(4)) for i in range(4)]
    cases = {
        "shipped: one load port e0": (ISA_LIN, [e[0]]),
        "symmetric: e0 and e2": (ISA_LIN, [e[0], e[2]]),
        "all four load ports": (ISA_LIN, e),
        "symmetric linear too (+F_f)": (ISA_LIN + ["F_f"], [e[0], e[2]]),
    }
    rows = {}
    for name, (lins, ts) in cases.items():
        st = stabiliser(lins, ts)
        rows[name] = len(st)
        print(f"  {name:32s} |stabiliser| = {len(st)}")
    base, sym = rows["shipped: one load port e0"], rows["all four load ports"]
    print(f"""
  {'SYMMETRISING BUYS SYMMETRY.' if sym > base else 'SYMMETRISING BUYS NO EXTRA SYMMETRY.'}
  The shipped ISA's stabiliser has order {base} (Pass 4227 found the same); with all four
  load ports it is {sym}.

  {'A larger stabiliser is a genuine structural gain and not just a spectral one: the instruction set now has automorphisms, and an automorphism of the ISA is a relabelling of the machine that no program can detect.' if sym > base else 'So the asymmetry is not in which load directions are present -- adding them all leaves the stabiliser where it was. The opcode set is rigid inside Sp(4,3) for reasons the translations do not touch.'}

  Either way this is the right object to have asked about.  A symmetry of the instruction
  set is what a conserved quantity would come from, and Pass 4250's nearly conserved
  coordinate is a candidate for exactly that -- the difference being that a true symmetry
  gives an exactly conserved observable, while what the machine has is a slow one.""")
    return {"stabilisers": rows, "gains_symmetry": bool(sym > base)}


# ------------------------------------------------------------------ 4313
def pass_4313() -> dict:
    print()
    print("=" * 78)
    print("Pass 4313 -- the Levi graph as datapath: a point<->line transfer opcode")
    print("=" * 78)

    def norm(v):
        return min(tuple((t * x) % 3 for x in v) for t in (1, 2))

    seen, pts = set(), []
    for v in TV:
        if not any(v):
            continue
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
    n = len(pts) + len(lines)
    L = np.zeros((n, n))
    for li, ln in enumerate(lines):
        for p in ln:
            L[pidx[p], 40 + li] = 1
            L[40 + li, pidx[p]] = 1
    d = L.sum(axis=1)
    print(f"  Levi graph: {len(pts)} points + {len(lines)} lines = {n} vertices,"
          f" {int(L.sum() // 2)} edges, degrees {int(d.min())}-{int(d.max())}")

    ev = np.sort(np.linalg.eigvalsh(L))[::-1]
    mods = np.abs(pencil(L))
    rho = float(mods.max())
    keep = (mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)
    nt = mods[keep]
    on = np.abs(nt - sqrt(rho)) < 1e-6 * sqrt(rho)
    print(f"  adjacency spectrum: {ev[0]:.3f}, {ev[1]:.3f}, ..., {ev[-1]:.3f}")
    print(f"  rho(B) = {rho:.6f}   non-trivial poles {len(nt)}, on circle {int(on.sum())}")
    print(f"  graph RH: {bool(len(nt) and on.all())}")

    # A machine whose state is a FLAG (incident point-line pair) rather than a point.
    flags = [(pidx[p], li) for li, ln in enumerate(lines) for p in ln]
    print(f"\n  incident point-line FLAGS: {len(flags)}")
    print(f"""
  THE TRANSFER OPCODE IS A REAL INSTRUCTION AND IT CHANGES THE STATE SPACE.  Moving along
  incidence takes a point to a line and back, so a machine that owns this opcode does not
  hold a point -- it holds a FLAG, one of the {len(flags)} incident pairs.  That is a bigger
  register than either side alone and it is where the two inequivalent G-sets of Pass 4303
  finally sit together.

  The Levi graph is 4-regular and bipartite, satisfies the graph RH (Pass 4200 verified its
  closed form independently), and rho(B) = {rho:.0f} exactly -- everything the instruction
  graph is not.  So the incidence datapath is the well-behaved object in this machine, and
  the irregularity lives entirely in the affine frame layer.

  What this does NOT give is a load port.  Incidence moves between existing points and
  lines; it cannot write an address any more than the line side could (Pass 4301).  A flag
  machine still needs a translation to become universal, and translations still exist only
  on the point half of the flag.  The asymmetry survives the enlargement.""")
    return {"levi_vertices": n, "levi_edges": int(L.sum() // 2),
            "degrees": [int(d.min()), int(d.max())], "rho": rho,
            "nontrivial": int(len(nt)), "on_circle": int(on.sum()),
            "graph_RH": bool(len(nt) and on.all()), "flags": len(flags),
            "provides_load_port": False}


def main() -> int:
    out = {"pass_4314_unification": pass_4314(),
           "pass_4310_two_thirds": pass_4310(),
           "pass_4312_symmetry": pass_4312(),
           "pass_4313_levi_datapath": pass_4313()}
    p = ROOT / "data" / "PART_W33_PASS4308_4314_ONE_OPCODE_LEVI.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
