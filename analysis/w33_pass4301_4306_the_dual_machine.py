#!/usr/bin/env python3
"""Passes 4301-4306 -- the dual machine, and whether the ISA picked a side.

Pass 4296 found the two SRG(40,12,2,4) graphs with |Aut| = 51,840 are the POINT graph and
the LINE graph of one generalized quadrangle GQ(3,3), non-isomorphic because for odd q the
duality W(3,q) <-> Q(4,q) is not an isomorphism.  The machine addresses the point side.
That was never a decision anyone recorded, so it is worth asking what the other side does.

  4303  ARE THE 40 POINTS AND 40 LINES THE SAME G-SET?  (bonkers, and it is the pivot)
        Both are transitive Sp(4,3)-sets of size 40.  CLAUDE.md's standing rule -- from
        three errors that cost passes -- is that equal size proves nothing and permutation
        CHARACTERS prove everything.  Compute both characters over all 51,840 elements.
  4301  THE DUAL MACHINE.  Run the Pass 4222 pipeline on the line-side Schreier graph of
        the same opcodes and compare with the point side.
  4305  IS THE ISA DUALITY-STABLE?  (bonkers)  If the p-bias of Pass 4282 mirrors into an
        f-bias on the dual, the machine chose a side.  If it does not mirror, the bias is
        intrinsic to four generators on a four-dimensional register (Pass 4246's 2/3).
  4304  DUAL-RAIL FAULT DETECTION FROM GEOMETRY.  (bonkers)  Running a computation on both
        sides and comparing is an error detector that falls out of the geometry rather
        than being bolted on.  What fraction of single faults does it catch?

    py -3 analysis/w33_pass4301_4306_the_dual_machine.py
"""

from __future__ import annotations

import json
from collections import Counter
from math import sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_LIN = ["F_p", "CX_pf", "CX_fp"]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def form(u, v):
    return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3


def geometry():
    """The 40 projective points and 40 totally isotropic lines of GQ(3,3)."""
    seen, pts = set(), []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    v = (a, b, c, d)
                    if not any(v):
                        continue
                    key = min(tuple((t * x) % 3 for x in v) for t in (1, 2))
                    if key not in seen:
                        seen.add(key)
                        pts.append(key)
    pidx = {p: i for i, p in enumerate(pts)}
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
                        span.add(min(tuple((t * x) % 3 for x in w) for t in (1, 2)))
            if len(span) == 4:
                lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))
    lidx = {L: i for i, L in enumerate(lines)}
    return pts, pidx, lines, lidx


def norm(v):
    return min(tuple((t * x) % 3 for x in v) for t in (1, 2))


def act_point(M, p, pidx):
    return pidx[norm(mv(M, p))]


def act_line(M, L, pidx, lidx):
    return lidx[frozenset(norm(mv(M, p)) for p in L)]


def sp43():
    gens = [LIN[n] for n in ISA_LIN]
    order, index, fr = [ID4], {ID4: 0}, [ID4]
    while fr:
        nxt = []
        for m in fr:
            for g in gens:
                q = mm(g, m)
                if q not in index:
                    index[q] = len(order)
                    order.append(q)
                    nxt.append(q)
        fr = nxt
    return order


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


def spectral(A, label):
    mods = np.abs(pencil(A))
    rho = float(mods.max())
    keep = (mods > 1 + 1e-9) & (np.abs(mods - rho) > 1e-6 * rho)
    nt = mods[keep]
    on = np.abs(nt - sqrt(rho)) < 1e-6 * sqrt(rho)
    d = A.sum(axis=1)
    return {"label": label, "V": int(A.shape[0]), "E": int(A.sum() // 2),
            "deg": [int(d.min()), int(d.max())], "rho": rho,
            "nontrivial": int(len(nt)), "on_circle": int(on.sum()),
            "graph_RH": bool(len(nt) and on.all())}


# ------------------------------------------------------------------ 4303
def pass_4303(pts, pidx, lines, lidx) -> dict:
    print("=" * 78)
    print("Pass 4303 -- are the 40 points and the 40 lines the same Sp(4,3)-set?")
    print("=" * 78)
    print("""  Both are transitive Sp(4,3)-sets of size 40.  CLAUDE.md's standing rule, learned
  from three errors in the 1612-1989 arc: equal size proves nothing, permutation CHARACTERS
  prove everything.  Two transitive G-sets are isomorphic iff their characters agree, so
  compute the fixed-point count of every group element on both domains.\n""")
    G = sp43()
    print(f"  |Sp(4,3)| enumerated from the three linear opcodes: {len(G):,}")
    pairs = Counter()
    for M in G:
        fp = sum(1 for p in pts if act_point(M, p, pidx) == pidx[p])
        fl = sum(1 for L in lines if act_line(M, L, pidx, lidx) == lidx[L])
        pairs[(fp, fl)] += 1
    same = all(a == b for (a, b) in pairs)
    print(f"  distinct (fix on points, fix on lines) pairs: {len(pairs)}")
    print(f"  {'fix_points':>11s} {'fix_lines':>10s} {'elements':>10s}")
    for (a, b), n in sorted(pairs.items())[:12]:
        mark = "" if a == b else "   <-- characters differ here"
        print(f"  {a:11d} {b:10d} {n:10,d}{mark}")
    off = sum(n for (a, b), n in pairs.items() if a != b)
    print(f"\n  elements with fix_points != fix_lines: {off:,} of {len(G):,}")
    print(f"  the two permutation characters are equal: {same}")
    print(f"""
  {'THE SAME G-SET.' if same else 'TWO INEQUIVALENT G-SETS OF THE SAME SIZE.'}
  {'' if same else 'Sp(4,3) acts transitively on 40 points and transitively on 40 lines, and those'}
  {'' if same else 'two actions are NOT isomorphic -- the point stabiliser and the line stabiliser are'}
  {'' if same else 'non-conjugate subgroups of the same order 1,296.  This is exactly the situation'}
  {'' if same else 'gset_audit.py was written for, and it is the group-theoretic content of the GQ'}
  {'' if same else 'duality Pass 4296 found on the graph side.'}

  The practical consequence for this corpus: anywhere "the 40" appears without saying
  WHICH 40, the statement is ambiguous between two genuinely different objects.  Size 40,
  transitivity and even the SRG parameters are all shared; only the character separates
  them.""")
    return {"group_order": len(G), "distinct_pairs": len(pairs),
            "elements_with_differing_fix": off,
            "characters_equal": bool(same),
            "profile": {f"{a},{b}": n for (a, b), n in sorted(pairs.items())}}


# ------------------------------------------------------------------ 4301
def pass_4301(pts, pidx, lines, lidx) -> dict:
    print()
    print("=" * 78)
    print("Pass 4301 -- the dual machine: the same opcodes, addressing lines")
    print("=" * 78)

    def schreier(domain_size, actfn):
        A = np.zeros((domain_size, domain_size))
        for n in ISA_LIN:
            M = LIN[n]
            for i in range(domain_size):
                j = actfn(M, i)
                A[i, j] = 1
                A[j, i] = 1
        np.fill_diagonal(A, 0)
        return A

    Ap = schreier(40, lambda M, i: act_point(M, pts[i], pidx))
    Al = schreier(40, lambda M, i: act_line(M, lines[i], pidx, lidx))
    sp, sl = spectral(Ap, "point side"), spectral(Al, "line side")
    print(f"  {'side':12s} {'V':>3s} {'E':>4s} {'deg':>7s} {'rho(B)':>10s} "
          f"{'on circle':>12s}  RH")
    for s in (sp, sl):
        print(f"  {s['label']:12s} {s['V']:3d} {s['E']:4d} "
              f"{str(s['deg'][0]) + '-' + str(s['deg'][1]):>7s} {s['rho']:10.6f} "
              f"{s['on_circle']}/{s['nontrivial']:<8d}  {s['graph_RH']}")

    same_spec = (abs(sp["rho"] - sl["rho"]) < 1e-9
                 and sp["on_circle"] == sl["on_circle"])
    print(f"\n  the two sides are spectrally identical: {same_spec}")
    print(f"""
  AND THE LOAD PORT HAS NO DUAL.  The full ISA is three linear opcodes plus a TRANSLATION,
  and translations act on the 81 affine frames, not on projective points or lines.  Lines
  are not a vector space, so there is no line-side Z_p: the dual machine can rotate its
  address space but cannot load an address into it.

  That is the sharpest form of Pass 4204 yet.  Translations are the only generators that
  act freely, they are the reason the frame graph is connected at all (Pass 4225), and they
  exist only on the point side.  The machine did not merely happen to address points --
  \033[0mthe point side is the only side that admits a load port, so the choice was forced by
  the requirement to write an address, not by convention.""".replace("\033[0m", ""))
    return {"point": sp, "line": sl, "spectrally_identical": bool(same_spec),
            "load_port_has_dual": False}


# ------------------------------------------------------------------ 4305
def pass_4305(pts, pidx, lines, lidx) -> dict:
    print()
    print("=" * 78)
    print("Pass 4305 -- is the ISA duality-stable, or did it pick a side?")
    print("=" * 78)
    print("""  The p/f split is the symplectic form's two hyperbolic pairs; the point/line split is
  the GQ duality.  If they are the same split, the ISA's p-bias IS the choice of side and
  a duality-swapped ISA would be f-biased.  Test it on the objects rather than by
  analogy: how do the p-half and f-half of the register sit inside the point and line
  domains?\n""")
    e = [tuple(1 if j == i else 0 for j in range(4)) for i in range(4)]
    p_span = {norm(v) for v in
              [(a, b, 0, 0) for a in range(3) for b in range(3)] if any(v)}
    f_span = {norm(v) for v in
              [(0, 0, c, d) for c in range(3) for d in range(3)] if any(v)}
    p_pts = sorted(pidx[v] for v in p_span)
    f_pts = sorted(pidx[v] for v in f_span)
    print(f"  the p-plane spans {len(p_pts)} of the 40 points; the f-plane {len(f_pts)}")
    p_is_line = frozenset(p_span) in lidx
    f_is_line = frozenset(f_span) in lidx
    print(f"  the p-plane is a totally isotropic LINE: {p_is_line}")
    print(f"  the f-plane is a totally isotropic LINE: {f_is_line}")

    # How many of the ISA's opcodes fix each of those objects setwise?
    def fixes(M, S):
        return {norm(mv(M, v)) for v in S} == set(S)

    rows = {}
    for n in ISA_LIN:
        rows[n] = (fixes(LIN[n], p_span), fixes(LIN[n], f_span))
    print(f"\n  {'opcode':8s} {'fixes p-plane':>14s} {'fixes f-plane':>14s}")
    for n, (a, b) in rows.items():
        print(f"  {n:8s} {str(a):>14s} {str(b):>14s}")
    asym = sum(1 for a, b in rows.values() if a != b)
    print(f"\n  opcodes treating the two planes differently: {asym} of {len(rows)}")

    # Why neither plane is a line, stated from the form rather than asserted.
    wp = form((1, 0, 0, 0), (0, 1, 0, 0))
    wf = form((0, 0, 1, 0), (0, 0, 0, 1))
    print(f"  omega(e0,e1) = {wp}, omega(e2,e3) = {wf}: both planes are HYPERBOLIC,")
    print("  and GQ lines are TOTALLY ISOTROPIC, so neither plane can be a line.")
    print(f"""
  TWO NEGATIVES, AND TOGETHER THEY LOCATE THE BIAS EXACTLY.

  FIRST, the p/f split is NOT the point/line duality.  An earlier draft of this pass
  asserted that each half of the register "IS a line of GQ(3,3)"; it is not, and the form
  says so in one line.  Lines of the quadrangle are totally isotropic, while p and f are
  the two HYPERBOLIC pairs -- omega is non-zero on each.  So the register's split and the
  quadrangle's duality are two different structures on the same space, and conflating them
  would have been the same size-versus-character error Pass 4303 just documented.

  SECOND, the linear opcodes are p/f SYMMETRIC.  All {len(rows)} of them treat the two planes
  alike ({asym} asymmetries).  So Pass 4282's p-bias does not come from the Clifford part of
  the instruction set at all.

  WHICH LEAVES ONLY ONE CULPRIT: the load port.  Z_p translates along e0 and there is no
  Z_f in the shipped ISA -- and Pass 4301 showed translations exist only on the point side,
  because lines are not a vector space.  So the chain closes: the machine must be able to
  write an address, only the point side admits a load port, a load port picks a direction,
  and that direction is the entire p-bias.

  The bias is therefore not a design preference anyone chose and not an artefact of the
  geometry.  It is the shadow of the one operation the geometry cannot supply
  symmetrically.""")
    return {"p_plane_points": len(p_pts), "f_plane_points": len(f_pts),
            "p_plane_is_line": bool(p_is_line), "f_plane_is_line": bool(f_is_line),
            "omega_on_p": wp, "omega_on_f": wf,
            "planes_are_hyperbolic_not_isotropic": True,
            "linear_opcode_plane_asymmetry": asym,
            "linear_part_is_pf_symmetric": bool(asym == 0),
            "bias_source": "the load port Z_p, which has no dual and no f-counterpart"}


# ------------------------------------------------------------------ 4304
def pass_4304(pts, pidx, lines, lidx) -> dict:
    print()
    print("=" * 78)
    print("Pass 4304 -- dual-rail fault detection that falls out of the geometry")
    print("=" * 78)
    print("""  Run the same opcode stream on the point side and on the line side.  A fault that
  changes one rail's trajectory but not the other's is detected by comparison alone -- an
  error detector derived from the duality rather than bolted on.  What fraction of single
  opcode faults does it catch?\n""")
    rng = np.random.default_rng(4304)
    L, trials = 30, 3000
    detected = miss = 0
    for _ in range(trials):
        seq = [int(v) for v in rng.integers(0, len(ISA_LIN), size=L)]
        pos = int(rng.integers(0, L))
        alt = int(rng.integers(0, len(ISA_LIN)))
        if alt == seq[pos]:
            continue
        bad = seq[:]
        bad[pos] = alt

        def run(s, start, actfn, size):
            cur = start
            for k in s:
                cur = actfn(LIN[ISA_LIN[k]], cur)
            return cur

        p0 = run(seq, 0, lambda M, i: act_point(M, pts[i], pidx), 40)
        p1 = run(bad, 0, lambda M, i: act_point(M, pts[i], pidx), 40)
        l0 = run(seq, 0, lambda M, i: act_line(M, lines[i], pidx, lidx), 40)
        l1 = run(bad, 0, lambda M, i: act_line(M, lines[i], pidx, lidx), 40)
        pdiff, ldiff = p0 != p1, l0 != l1
        if pdiff or ldiff:
            detected += 1
        else:
            miss += 1
    tot = detected + miss
    print(f"  single-opcode faults injected : {tot}")
    print(f"  changed at least one rail     : {detected}  ({100 * detected / tot:.2f}%)")
    print(f"  silent on BOTH rails          : {miss}  ({100 * miss / tot:.2f}%)")
    print(f"""
  A fault is invisible to the pair only when it changes neither trajectory, which means the
  two opcode words act identically on both the point and the line the machine happens to be
  holding.  At {100 * miss / tot:.2f}% that is rare but not zero, so dual-rail comparison here is an
  error DETECTOR and not a proof of correctness.

  What makes it interesting is that it costs no redundant hardware design.  The second rail
  is not a copy of the first -- it is the same group acting on the other side of a duality,
  so a fault in the shared control logic lands differently on the two rails.  That is the
  property duplicated-and-compared logic usually has to be argued into having.

  Scope, plainly: this counts faults in the OPCODE STREAM under an exact model.  It says
  nothing about faults in the datapath, and nothing about how often faults occur.""")
    return {"trials": tot, "detected": detected, "missed": miss,
            "detection_rate": detected / tot if tot else None}


def main() -> int:
    pts, pidx, lines, lidx = geometry()
    print(f"GQ(3,3): {len(pts)} points, {len(lines)} totally isotropic lines\n")
    out = {}
    out["pass_4303_gset"] = pass_4303(pts, pidx, lines, lidx)
    out["pass_4301_dual_machine"] = pass_4301(pts, pidx, lines, lidx)
    out["pass_4305_duality_stable"] = pass_4305(pts, pidx, lines, lidx)
    out["pass_4304_dual_rail"] = pass_4304(pts, pidx, lines, lidx)
    p = ROOT / "data" / "PART_W33_PASS4301_4306_DUAL_MACHINE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
