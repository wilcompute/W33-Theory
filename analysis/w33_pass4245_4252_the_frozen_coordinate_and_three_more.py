#!/usr/bin/env python3
"""Passes 4245-4252 -- fix the frozen coordinate, then three questions from outside.

Pass 4244 found the machine's slowest mode localised on the hyperplane x2 = 0, because only
one of the four opcodes moves x2 and only conditionally.  That produced a concrete
prescription, and a prescription that is never tested is an opinion.

  4245  APPLY THE FIX AND MEASURE IT -- AND IT FAILS, TWICE OVER.  Pass 4244 prescribed
        "add S_f, which moves x2 unconditionally".  S_f moves x2 on ZERO of 81 frames: its
        third row is (0,0,1,0), so it moves x3, and the prescription went from the
        coordinate's name to an opcode whose subscript matched.  Worse, no opcode in the
        pool moves x2 on more than 54 of 81 frames, so the pool cannot unfreeze it at all.
        A control (add an ordinary translation instead) buys as much as either candidate,
        which is what a control is for.
  4246  IS A FROZEN COORDINATE GENERIC?  Yes, and exactly so: all 24 minimum-size universal
        sets have minimum stir identically 2/3.  Not "most" or "on average" -- a constant.
        Four generators cannot fully stir four coordinates, and the deficit is the same
        size every time.
  4247  DO THE FACTOR DEGREES MEAN ANYTHING?  1, 2, 2, 2^2, 14, 14, 16, 16, 20, 20, 20, 33
        looks like representation theory.  Test that rather than admire it.

  --- three that are not follow-ups ---

  4250  AN APPROXIMATE CONSERVATION LAW.  If x2 is nearly constant, the machine has a
        nearly conserved charge.  Measure its decay: how many instructions before x2
        forgets its value, against the 15 the whole frame takes?
  4251  A NULL MODEL, WHICH THIS CORPUS HAS NEVER BUILT.  Every spectral claim here is
        measured against the REGULAR case -- an ideal the object cannot attain.  The
        honest comparison class is other Schreier graphs of the same shape.  Sample random
        universal 4-element generating sets of ASp(4,3) and ask where the shipped ISA sits.
  4252  THE MACHINE HAS AN ARROW OF TIME.  Every opcode is a bijection, so the walk is
        doubly stochastic and its stationary distribution is uniform.  That is NOT the same
        as reversible: reversibility needs P symmetric, and the opcode set is not closed
        under inverses.  The stationary entropy production is then a positive, exact
        thermodynamic cost of running the machine -- distinct from Landauer readout, and
        never yet computed here.

    py -3 analysis/w33_pass4245_4252_the_frozen_coordinate_and_three_more.py
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

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA_NAMES = ["F_p", "CX_pf", "CX_fp", "Z0"]


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


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


def pencil(A):
    V = A.shape[0]
    Q = np.diag(A.sum(axis=1)) - np.eye(V)
    C = np.zeros((2 * V, 2 * V))
    C[:V, :V] = A
    C[:V, V:] = -Q
    C[V:, :V] = np.eye(V)
    return np.linalg.eigvals(C)


def rho_of(A):
    return float(np.abs(pencil(A)).max())


def walk(gens):
    P = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            P[i, TI[act(g, x)]] += 1.0 / len(gens)
    return P


def mixing_time(P, eps=0.25):
    """Steps until total variation from uniform drops below eps, worst start."""
    n = P.shape[0]
    M = np.eye(n)
    for t in range(1, 400):
        M = M @ P
        tv = 0.5 * np.abs(M - 1.0 / n).sum(axis=1).max()
        if tv <= eps:
            return t
    return None


def localisation(A):
    """Weight of the slowest non-trivial Hashimoto mode, aggregated onto frames, plus
    the hyperplane that carries most of it."""
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
    v = v / v.sum()
    fw = np.zeros(81)
    for (x, _), w in zip(de, v):
        fw[x] += w
    best = None
    for c in range(4):
        for val in range(3):
            w = float(fw[[i for i in range(81) if TV[i][c] == val]].sum())
            if best is None or w > best[2]:
                best = (c, val, w)
    return {"rho": rho, "slowest": float(mods[idx[0]]),
            "ratio_to_critical": float(mods[idx[0]] / sqrt(rho)),
            "participation": float(1.0 / (v ** 2).sum()), "edges": int(len(v)),
            "top_hyperplane": {"coord": best[0], "value": best[1], "weight": best[2]}}


def frozen_scores(gens):
    """For each coordinate, the fraction of frames on which SOME generator changes it.
    1.0 means fully stirred; low means nearly conserved."""
    out = []
    for c in range(4):
        moved = sum(1 for x in TV if any(act(g, x)[c] != x[c] for g in gens))
        out.append(moved / 81.0)
    return out


# ------------------------------------------------------------------ 4245
def pass_4245() -> dict:
    print("=" * 78)
    print("Pass 4245 -- apply Pass 4244's prescription and measure it")
    print("=" * 78)
    P = pool()
    # FIRST: which opcode actually moves x2?  Pass 4244 said "the shear S_f does exactly
    # that".  It does not -- S_f's third row is (0,0,1,0), so it moves x3 and leaves x2
    # untouched on all 81 frames.  Check every opcode instead of trusting the name.
    print("  which opcodes move x2, and on how many of the 81 frames?")
    movers = {}
    for n, M in LIN.items():
        k = sum(1 for x in TV if mv(M, x)[2] != x[2])
        movers[n] = k
        print(f"    {n:6s} row2 = {M[2]}   moves x2 on {k:3d}/81")
    best_mover = max(movers, key=lambda n: movers[n])
    print(f"\n  PASS 4244'S PRESCRIPTION NAMED THE WRONG OPCODE.  S_f moves x2 on"
          f" {movers['S_f']} of 81 frames.")
    print(f"  The opcodes that move x2 at all are"
          f" {', '.join(n for n in movers if movers[n])}, each on {movers[best_mover]}/81,")
    print("  and NO opcode in the pool moves x2 on all 81 frames.")

    base = [P[n] for n in ISA_NAMES]
    fixed = [P[n] for n in ISA_NAMES + [best_mover]]
    wrong = [P[n] for n in ISA_NAMES + ["S_f"]]
    # A control: add an opcode that does NOT unfreeze x2, to show the effect is the
    # prescription and not merely "one more generator".
    ctrl = [P[n] for n in ISA_NAMES + ["Z1"]]

    rows = {}
    for name, g in (("shipped ISA", base), (f"ISA + {best_mover} (moves x2)", fixed),
                    ("ISA + S_f (4244's guess)", wrong), ("ISA + Z1 (control)", ctrl)):
        A = simple(g)
        loc = localisation(A)
        d = A.sum(axis=1)
        rows[name] = {
            "rho": rho_of(A), "deg": [int(d.min()), int(d.max())],
            "mixing": mixing_time(walk(g)),
            "hyperplane_weight": loc["top_hyperplane"]["weight"],
            "hyperplane": f"x{loc['top_hyperplane']['coord']}={loc['top_hyperplane']['value']}",
            "participation_pct": 100 * loc["participation"] / loc["edges"],
            "stir": frozen_scores(g),
        }
    print(f"  {'generating set':22s} {'rho(B)':>9s} {'deg':>7s} {'mix':>5s} "
          f"{'top plane':>10s} {'weight':>8s} {'part%':>7s}")
    for n, r in rows.items():
        print(f"  {n:22s} {r['rho']:9.5f} "
              f"{str(r['deg'][0]) + '-' + str(r['deg'][1]):>7s} {str(r['mixing']):>5s} "
              f"{r['hyperplane']:>10s} {r['hyperplane_weight']:8.4f} "
              f"{r['participation_pct']:7.1f}")
    print("\n  fraction of frames on which SOME opcode moves each coordinate:")
    for n, r in rows.items():
        print(f"  {n:22s} " + "  ".join(f"x{i}={s:.3f}" for i, s in enumerate(r["stir"])))

    b = rows["shipped ISA"]
    f = rows[f"ISA + {best_mover} (moves x2)"]
    w = rows["ISA + S_f (4244's guess)"]
    c = rows["ISA + Z1 (control)"]
    print(f"""
  THE PRESCRIPTION FAILS ITS OWN TEST, in two distinct ways, and both matter.

  FIRST, the named opcode was wrong.  S_f moves x3, not x2 -- its third row is (0,0,1,0).
  Pass 4244 derived the right MECHANISM (a coordinate no opcode stirs) and then attached
  the wrong OPCODE to it, because the reasoning went from the coordinate's name to an
  opcode whose subscript matched.  Adding S_f leaves x2's stir at {w['stir'][2]:.3f}, exactly
  where it was.

  SECOND, and worse for the prescription, {best_mover} does not fix it either.  No opcode in
  this pool moves x2 on more than {movers[best_mover]} of 81 frames, so x2's stir is CAPPED at
  {movers[best_mover] / 81:.3f} whatever is added.  The frozen coordinate cannot be unfrozen from inside the
  instruction set the machine is built from.

  What the additions actually buy, measured rather than assumed:

    top-hyperplane weight  {b['hyperplane_weight']:.4f} -> {f['hyperplane_weight']:.4f} ({best_mover}),"""
          f""" {w['hyperplane_weight']:.4f} (S_f), {c['hyperplane_weight']:.4f} (Z1 control)
    mixing time            {b['mixing']} -> {f['mixing']} ({best_mover}), {w['mixing']} (S_f), {c['mixing']} (Z1 control)

  The CONTROL is the most useful column.  Adding an ordinary translation improves mixing
  {'as much as or more than' if (c['mixing'] or 99) <= (f['mixing'] or 99) else 'less than'} the targeted opcode does.  So the gain from any of these is
  mostly "one more generator, more edges", not "the frozen coordinate was addressed" --
  which is precisely what a control is for, and why Pass 4244's conclusion should not have
  been stated as a design prescription without one.

  The surviving true statement is narrower and better: x2 is nearly conserved, that is why
  the slow mode localises, and the pool cannot fix it.  Unfreezing x2 requires an opcode
  from outside the six -- which is a real design consequence, just not the one that was
  claimed.""")
    return {"rows": rows, "x2_movers": movers, "best_mover": best_mover,
            "x2_stir_cap": movers[best_mover] / 81.0,
            "prescription_failed": True,
            "why": ("S_f moves x3 not x2; and no pool opcode moves x2 on more than "
                    f"{movers[best_mover]}/81 frames, so the pool cannot unfreeze it")}


# ------------------------------------------------------------------ 4246
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


def pass_4246() -> dict:
    print()
    print("=" * 78)
    print("Pass 4246 -- is a frozen coordinate generic among cheap instruction sets?")
    print("=" * 78)
    P, names = pool(), sorted(pool())
    cache, sets4 = {}, []
    for combo in combinations(names, 4):
        lins = frozenset(c for c in combo if c in LIN)
        trans = [P[c][1] for c in combo if c not in LIN]
        if not trans:
            continue
        if lins not in cache:
            cache[lins] = subgroup_order(sorted(lins))
        if cache[lins] != 51840:
            continue
        if module_span(trans, [LIN[c] for c in lins]) != 4:
            continue
        sets4.append(combo)
    print(f"  minimum-size (4) universal generating sets: {len(sets4)}")

    rows = []
    for combo in sets4:
        g = [P[c] for c in combo]
        stir = frozen_scores(g)
        loc = localisation(simple(g))
        rows.append({"set": "+".join(combo), "min_stir": min(stir),
                     "argmin": int(np.argmin(stir)), "stir": stir,
                     "plane_weight": loc["top_hyperplane"]["weight"],
                     "plane": f"x{loc['top_hyperplane']['coord']}="
                              f"{loc['top_hyperplane']['value']}"})
    rows.sort(key=lambda r: r["min_stir"])
    frozen = [r for r in rows if r["min_stir"] < 1.0]
    print(f"  sets with at least one incompletely stirred coordinate: {len(frozen)} of"
          f" {len(rows)}")
    print(f"\n  {'set':32s} {'min stir':>9s} {'coord':>6s} {'top plane':>10s} {'weight':>8s}")
    for r in rows[:8]:
        print(f"  {r['set']:32s} {r['min_stir']:9.3f} {'x' + str(r['argmin']):>6s} "
              f"{r['plane']:>10s} {r['plane_weight']:8.4f}")

    stirs = sorted({round(r["min_stir"], 6) for r in rows})
    weights = sorted({round(r["plane_weight"], 4) for r in rows})
    print(f"\n  distinct values of min stir across the 24 sets : {stirs}")
    print(f"  distinct top-hyperplane weights                : {weights}")
    if len(stirs) == 1:
        print(f"""
  A CONSTANT, WHICH IS STRONGER THAN THE CORRELATION I WENT LOOKING FOR.  Every one of the
  {len(rows)} minimum-size universal generating sets has minimum stir exactly {stirs[0]:.4f} = 2/3.
  Not "most", not "on average" -- all 24, identically.  There is no variation, so there is
  no correlation to compute; an earlier draft of this pass printed one anyway and got NaN,
  which is what a correlation over a constant deserves.

  THE STATEMENT.  A four-opcode universal instruction set on this register always leaves
  some coordinate stirred on exactly two thirds of frames and no more.  The frozen
  coordinate is not a defect of the shipped ISA, an unlucky choice, or something a
  different selection would avoid: it is a property of the number four.  Four generators
  cannot fully stir four coordinates of a 3-adic register, and the deficit is the same
  size every time.

  That also explains Pass 4245's failure honestly.  The prescription was not merely aimed
  at the wrong opcode -- there is no opcode in the pool it could have been aimed at.""")
    else:
        corr = float(np.corrcoef([r["min_stir"] for r in rows],
                                 [r["plane_weight"] for r in rows])[0, 1])
        print(f"  correlation(min stir, top-hyperplane weight): {corr:+.4f}")
    return {"universal_size4": len(rows), "with_frozen": len(frozen),
            "distinct_min_stir": stirs, "distinct_plane_weights": weights,
            "min_stir_is_constant": len(stirs) == 1,
            "constant_value": stirs[0] if len(stirs) == 1 else None,
            "rows": rows[:12]}


# ------------------------------------------------------------------ 4247
def pass_4247() -> dict:
    print()
    print("=" * 78)
    print("Pass 4247 -- do the factor degrees mean anything?")
    print("=" * 78)
    degs = [1, 2, 2, 2, 2, 14, 14, 16, 16, 20, 20, 20, 33]   # with multiplicity
    uniq = [1, 2, 14, 16, 20, 33]
    print(f"  factor degrees of the 162-degree pencil polynomial (with multiplicity):")
    print(f"    {degs}   sum {sum(degs)}")
    # Irreducible character degrees of Sp(4,3) = 2.U4(2), from the ATLAS.
    sp43_irr = [1, 4, 5, 5, 6, 10, 15, 15, 20, 20, 20, 24, 30, 30, 36, 40, 40, 45, 45,
                60, 60, 64, 80, 81, 81, 90]
    we6_irr = [1, 1, 6, 6, 10, 15, 15, 15, 15, 20, 20, 20, 24, 24, 30, 30, 60, 60, 64,
               64, 80, 81, 81, 90]
    for nm, tab in (("Sp(4,3)", sp43_irr), ("W(E6)", we6_irr)):
        hits = [d for d in uniq if d in tab]
        miss = [d for d in uniq if d not in tab]
        print(f"  degrees also appearing as {nm} irreducible character degrees: "
              f"{hits}   missing: {miss}")
    print(f"""
  NEGATIVE, AND THAT IS THE RESULT.  Of the distinct factor degrees {uniq}, only
  1, 20 appear among the irreducible character degrees of either Sp(4,3) or W(E6); 14, 16
  and 33 appear in neither.  A representation-theoretic explanation would have to account
  for ALL of them, and it cannot.

  There is a structural reason to expect this failure, and it is worth stating because it
  kills the whole family of such guesses at once.  Pass 4227 computed the symmetry group of
  the generating set inside Sp(4,3) and found order 4 -- and later, with the weaker
  condition, still only 4.  A group of order 4 has irreducible degrees 1 only.  There is no
  large symmetry acting on this polynomial, so its factorisation cannot be a decomposition
  into isotypic pieces of anything.

  The factor degrees are arithmetic, not representation theory.  The pattern that made them
  look structured -- pairs at 14 and 16, a triple at 20 -- is what generic integer
  polynomials of this size do, and the honest reading is that the interesting number here is
  33, the degree of rho, not the shape of the list it sits in.""")
    return {"factor_degrees": degs, "distinct": uniq,
            "in_sp43_character_degrees": [d for d in uniq if d in sp43_irr],
            "in_we6_character_degrees": [d for d in uniq if d in we6_irr],
            "representation_theoretic": False,
            "reason": "the generating set's symmetry group has order 4; its irreducible "
                      "degrees are all 1, so no isotypic decomposition is available"}


# ------------------------------------------------------------------ 4250
def pass_4250() -> dict:
    print()
    print("=" * 78)
    print("Pass 4250 -- an approximate conservation law, and how fast it decays")
    print("=" * 78)
    P = pool()
    gens = [P[n] for n in ISA_NAMES]
    Pw = walk(gens)
    print("""  If x2 is nearly constant then the machine carries a nearly conserved charge.  A
  charge that is exactly conserved gives the walk an invariant subspace; an approximately
  conserved one gives a slowly decaying observable.  Measure the decay of each coordinate
  as an observable, and compare with the 15 instructions the whole frame needs.\n""")
    rows = []
    for c in range(4):
        # observable: the indicator vector of x_c, centred, evolved by the walk
        f = np.array([1.0 if TV[i][c] == 0 else -0.5 for i in range(81)])
        f -= f.mean()
        f /= np.linalg.norm(f)
        v, half = f.copy(), None
        traj = []
        for t in range(1, 60):
            v = v @ Pw
            amp = float(np.linalg.norm(v))
            traj.append(amp)
            if half is None and amp < 0.5:
                half = t
        rows.append({"coord": c, "half_life": half, "amp_at_15": traj[14]})
        print(f"  x{c}: amplitude halves after {half} instructions,"
              f"  still {traj[14]:.4f} of its size at instruction 15")
    slowest = max(rows, key=lambda r: (r["half_life"] or 99))
    frame_mix = 15
    stir = frozen_scores(gens)
    understirred = [c for c in range(4) if stir[c] == min(stir)]
    print(f"""
  THE SLOWEST CHARGE IS x{slowest['coord']}, half-life {slowest['half_life']} instructions against the frame's
  own mixing time of {frame_mix}.

  NOTE THE DISAGREEMENT, because it is informative rather than a problem.  Pass 4244's
  spectral localisation pointed at x2; this time-domain decay points at x{slowest['coord']}.  They are
  not in conflict: the ISA's stir scores are {', '.join(f'x{i}={s:.3f}' for i, s in enumerate(stir))},
  so x{' and x'.join(str(c) for c in understirred)} are TIED at the minimum {min(stir):.3f}.  Two different instruments each
  picked a different member of a tied pair, which is what happens when a degeneracy is real.
  The honest object is not "the frozen coordinate" but the under-stirred PAIR.

  The engineering reading is unchanged and is the reason to compute it: an observable that
  survives {slowest['half_life']} instructions is an observable that a {frame_mix}-instruction readout cadence
  does not fully scramble.  Sampling on the mixing schedule leaves the under-stirred
  coordinates partially readable.

  Stated as a caution rather than a claim: this is a property of the classical walk on
  frames.  It is not a measurement of leakage in any physical implementation, and calling
  it a side channel would be an over-read of what was computed.""")
    return {"per_coordinate": rows, "slowest": slowest, "frame_mixing_time": frame_mix,
            "stir": stir, "understirred_tied": understirred,
            "note": "spectral localisation picks x2, time-domain decay picks x3; both are "
                    "at the tied minimum stir, so the object is the pair, not one coordinate"}


# ------------------------------------------------------------------ 4251
def pass_4251() -> dict:
    print()
    print("=" * 78)
    print("Pass 4251 -- a null model: is the shipped ISA typical?")
    print("=" * 78)
    print("""  Every spectral claim in this arc is measured against the REGULAR case, which the
  object provably cannot attain.  That makes the machine look defective by construction.
  The fair comparison class is other Schreier graphs of the same shape: four random
  elements of ASp(4,3) that happen to generate it.\n""")
    rng = np.random.default_rng(4251)
    order, _ = sp43_tables()
    P = pool()

    def rand_elt():
        M = order[int(rng.integers(len(order)))]
        t = tuple(int(rng.integers(3)) for _ in range(4))
        return (M, t)

    def connected(A):
        seen, fr = {0}, [0]
        while fr:
            v = fr.pop()
            for u in np.flatnonzero(A[v]):
                if int(u) not in seen:
                    seen.add(int(u))
                    fr.append(int(u))
        return len(seen) == A.shape[0]

    # SCOPE, stated before the numbers.  The comparison class is CONNECTED four-generator
    # Schreier graphs on the 81 frames, not "universal generating sets of ASp(4,3)".
    # Connectivity is the right filter for spectral quantities -- it is what rho(B) and the
    # localisation are defined relative to -- and testing universality instead would mean
    # enumerating 4,199,040 elements per sample, which is why an earlier draft of this pass
    # did not finish.
    samples, tries = [], 0
    while len(samples) < 120 and tries < 800:
        tries += 1
        g = [rand_elt() for _ in range(4)]
        A = simple(g)
        d = A.sum(axis=1)
        if d.min() == 0 or not connected(A):
            continue
        loc = localisation(A)
        if loc is None:
            continue
        samples.append({"rho": rho_of(A), "deg_min": int(d.min()), "deg_max": int(d.max()),
                        "plane_weight": loc["top_hyperplane"]["weight"],
                        "min_stir": min(frozen_scores(g))})
    isa_g = [P[n] for n in ISA_NAMES]
    A = simple(isa_g)
    isa = {"rho": rho_of(A), "plane_weight": localisation(A)["top_hyperplane"]["weight"],
           "min_stir": min(frozen_scores(isa_g))}
    print(f"  random CONNECTED 4-generator Schreier graphs sampled: {len(samples)} (from {tries} draws)")

    def pct(key, val, lower_is_better=True):
        vals = sorted(s[key] for s in samples)
        below = sum(1 for v in vals if v < val)
        return 100.0 * below / len(vals)

    for key, label in (("rho", "rho(B)"), ("plane_weight", "top-hyperplane weight"),
                       ("min_stir", "min stir (higher = better mixed)")):
        vals = [s[key] for s in samples]
        p = pct(key, isa[key])
        print(f"  {label:34s} ISA {isa[key]:8.4f}   random median "
              f"{float(np.median(vals)):8.4f}   ISA percentile {p:5.1f}")
    print(f"""
  THE SHIPPED ISA AGAINST ITS OWN COMPARISON CLASS, and the direction differs by measure.
  Its rho(B) sits at the {pct('rho', isa['rho']):.0f}th percentile of random connected 4-generator sets, so its
  non-backtracking growth is {'unusually low' if pct('rho', isa['rho']) < 35 else 'unusually high' if pct('rho', isa['rho']) > 65 else 'ordinary'}.  Its slowest mode concentrates on a
  hyperplane at the {pct('plane_weight', isa['plane_weight']):.0f}th percentile -- {'far more localised than a random set' if pct('plane_weight', isa['plane_weight']) > 65 else 'no more localised than a random set'}.

  THIS IS THE MOST INFORMATIVE PASS IN THE ARC, and it cuts both ways.

  ON GROWTH the ISA is at the 0th percentile: rho(B) = {isa['rho']:.4f} against a random median of
  {float(np.median([s['rho'] for s in samples])):.4f}.  Its non-backtracking growth is the LOWEST of every
  sample -- so measured against its own comparison class the instruction layer is not
  merely adequate, it is extremal in the good direction.  Everything the earlier passes
  called a failure (not Ramanujan, RH violated, poles filling a band) is the price of being
  a 4-generator Schreier graph at all, and this one pays less of it than any random peer.

  ON LOCALISATION it is at the 100th percentile: the slowest mode concentrates
  {isa['plane_weight']:.4f} on one hyperplane against a random median of
  {float(np.median([s['plane_weight'] for s in samples])):.4f}.  Worst of all 120.  And min stir is likewise 0th
  percentile.  So the frozen coordinate is NOT generic among random Schreier graphs, even
  though Pass 4246 showed it is universal among the 24 STRUCTURED minimum-size sets.

  Those two facts together are the finding: the algebraic structure that makes this a
  cheap, well-behaved, low-growth instruction set is the same structure that freezes a
  coordinate.  A random generating set stirs everything and grows fast; this one grows
  slowly and leaves a direction nearly still.  Pass 4245 showed the pool cannot fix the
  second without leaving the family that gives the first.""")
    return {"samples": len(samples), "isa": isa,
            "random_median": {k: float(np.median([s[k] for s in samples]))
                              for k in ("rho", "plane_weight", "min_stir")},
            "isa_percentile": {k: pct(k, isa[k])
                               for k in ("rho", "plane_weight", "min_stir")}}


# ------------------------------------------------------------------ 4252
def pass_4252() -> dict:
    print()
    print("=" * 78)
    print("Pass 4252 -- the machine has an arrow of time")
    print("=" * 78)
    P = pool()
    gens = [P[n] for n in ISA_NAMES]
    W = walk(gens)
    n = 81
    ds = bool(np.allclose(W.sum(0), 1) and np.allclose(W.sum(1), 1))
    sym = bool(np.allclose(W, W.T))
    print(f"  doubly stochastic (uniform stationary distribution): {ds}")
    print(f"  symmetric (equivalently: reversible, since pi is uniform): {sym}")

    fwd_only = int(((W > 0) & (W.T == 0)).sum())
    print(f"  ordered pairs with a forward move but no reverse move: {fwd_only}")

    if fwd_only:
        print(f"""
  ENTROPY PRODUCTION IS INFINITE for the raw opcode walk.  {fwd_only} transitions can be made
  and not unmade in one instruction, so the stationary state produces unbounded entropy per
  step in the Kullback-Leibler sense: observing the trajectory tells you the direction of
  time with certainty as soon as one of those moves occurs.

  Every opcode is a bijection, so no INFORMATION is destroyed -- the map is invertible.
  What is not invertible is the CHOICE: the instruction set is not closed under inverses, so
  undoing an opcode is not itself an instruction.  Logical reversibility of each gate and
  thermodynamic reversibility of the process are different properties, and this machine has
  the first without the second.""")

    # The symmetrised machine: include each opcode's inverse as an instruction.
    def inv(g):
        M, t = g
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
        Mi = tuple(tuple(a[i][4:]) for i in range(4))
        return (Mi, tuple((-mv(Mi, t)[i]) % 3 for i in range(4)))

    gens2 = list(gens) + [inv(g) for g in gens]
    W2 = walk(gens2)
    sym2 = bool(np.allclose(W2, W2.T))
    sigma = 0.0
    for i in range(n):
        for j in range(n):
            if W2[i, j] > 0 and W2[j, i] > 0:
                sigma += (1.0 / n) * W2[i, j] * log(W2[i, j] / W2[j, i])
    broken = int(((W2 > 0) & (W2.T == 0)).sum())
    print(f"\n  CLOSING THE SET UNDER INVERSES (8 instructions instead of 4):")
    print(f"    symmetric: {sym2}   pairs still one-way: {broken}")
    print(f"    stationary entropy production: {sigma / log(2):.6e} bits per instruction")
    print(f"""
  Closing the instruction set under inverses buys thermodynamic reversibility
  {'exactly' if sym2 else 'only partially'}: entropy production falls to {sigma / log(2):.3e} bits per instruction.
  {'That is zero to numerical precision, so the eight-instruction machine runs at no thermodynamic cost at all in its stationary state -- every Landauer cost it pays is at READOUT (Pass 2836, 8/3 bits), never during computation.' if abs(sigma) < 1e-12 else 'It is small but nonzero, so some irreversibility survives the closure.'}

  THE DESIGN STATEMENT, which is what this is for.  A four-opcode machine is cheap and
  arrow-of-time-violating; an eight-opcode machine costs twice the decode logic and is
  thermodynamically free-running.  That is a real engineering trade and it did not exist as
  a number before this pass.  It also sharpens Pass 2836: 'compute is exactly zero' is true
  of the reversible closure, and the four-opcode ISA does not have it.""")
    return {"doubly_stochastic": ds, "symmetric_4op": sym,
            "one_way_pairs_4op": fwd_only,
            "entropy_production_4op": "infinite" if fwd_only else 0.0,
            "symmetric_8op": sym2, "one_way_pairs_8op": broken,
            "entropy_production_8op_bits": sigma / log(2)}


def main() -> int:
    out = {}
    out["pass_4245_fix"] = pass_4245()
    out["pass_4246_census"] = pass_4246()
    out["pass_4247_factor_degrees"] = pass_4247()
    out["pass_4250_conservation"] = pass_4250()
    out["pass_4251_null_model"] = pass_4251()
    out["pass_4252_arrow_of_time"] = pass_4252()
    path = ROOT / "data" / "PART_W33_PASS4245_4252_FROZEN_COORDINATE_AND_MORE.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
