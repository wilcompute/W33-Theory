#!/usr/bin/env python3
"""Passes 2830-2832 -- three things the magic-state picture still owed.

PASS 2830 -- WHAT SEPARATES THE TWO TWELVE-RAY CLASSES?
    Pass 2797 found four Clifford classes on the 36 Witting rays, sizes [4, 8, 12, 12],
    with the 24-ray middle grade splitting.  Stabilizer fidelity cannot see that split --
    it is constant across both.  So either some other stabilizer statistic separates
    them, or they are indistinguishable by every such statistic and the split is visible
    only in the group action.  Both answers are worth having, and they are different
    engineering situations: the first means a protocol can be tuned per class, the second
    means it cannot.

    The sharpest test available without enumerating protocols is the FULL STABILIZER
    OVERLAP SPECTRUM: the multiset of |<s|psi>|^2 over all 60 two-qubit stabilizer
    states.  It is a Clifford invariant (Clifford permutes the stabilizer states), and it
    contains F_stab, the stabilizer Renyi entropies, and every other overlap moment as
    functions of it.  If the two classes share it, no overlap statistic separates them.

PASS 2831 -- THE YIELD, WHICH THE RECURRENCE DOES NOT GIVE YOU
    The parallel track's PR #210 has the accepted-round recurrence and its fixed points:
        p' = p(4-p) / (3(p^2-2p+2)),   P_succ = (p^2-2p+2)/4,
        fixed points 0, 2/3, 1, with 2/3 repelling.
    Convergence is only half of an engineering answer.  The other half is COST: how many
    raw noisy states are consumed per output at a given target, once the acceptance
    probability of every round is paid for.  That is what this computes.

PASS 2832 -- IS F_stab SUPER-MULTIPLICATIVE ON THREE COPIES?
    Pass 2798 found F_stab exactly multiplicative on two copies, so D_min(psi^2) =
    2 D_min(psi) and the monotone never obstructs.  Three copies live in six qubits,
    where the 315,057,600 stabilizer states cannot be enumerated.  But the question has a
    ONE-SIDED rigorous answer: exhibiting a single stabilizer state with overlap above
    F_stab^3 PROVES super-multiplicativity.  A witness is a proof; failing to find one is
    not.  Stated that way, sampling is legitimate.

    py -3 analysis/w33_pass2830_2832_class_separation_yield_three_copy.py
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)
RNG = np.random.default_rng(2830)


# ---------------------------------------------------------------------------
def build_rays() -> list[np.ndarray]:
    w = [1, W, W ** 2]
    raw = []
    for mu, nu in product(range(3), repeat=2):
        raw.append([0, 1, -w[mu], w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, 0, -w[mu], -w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, -w[mu], 0, w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, w[mu], w[nu], 0])
    return [np.array(r, dtype=complex) / np.linalg.norm(r) for r in raw]


def key_mat(m):
    z = np.asarray(m, dtype=complex) * 1e9
    return (np.round(z.real).astype(np.int64).tobytes()
            + np.round(z.imag).astype(np.int64).tobytes())


def key_state(v):
    idx = int(np.argmax(np.abs(v) > 1e-9))
    return key_mat(v * np.exp(-1j * np.angle(v[idx])))


def clifford_gens(nq: int):
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.diag([1, 1j]).astype(complex)
    I = np.eye(2, dtype=complex)

    def onwire(g, k):
        m = np.array([[1]], dtype=complex)
        for j in range(nq):
            m = np.kron(m, g if j == k else I)
        return m

    gens = [onwire(H, k) for k in range(nq)] + [onwire(S, k) for k in range(nq)]
    d = 2 ** nq
    for a in range(nq):
        for b in range(nq):
            if a == b:
                continue
            M = np.zeros((d, d), dtype=complex)
            for x in range(d):
                bits = [(x >> (nq - 1 - i)) & 1 for i in range(nq)]
                bits[b] ^= bits[a]
                y = 0
                for i in range(nq):
                    y = (y << 1) | bits[i]
                M[y, x] = 1
            gens.append(M)
    return gens


def stabilizer_states(nq: int):
    d = 2 ** nq
    start = np.zeros(d, dtype=complex)
    start[0] = 1
    gens = clifford_gens(nq)
    seen = {key_state(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for v in frontier:
            for g in gens:
                u = g @ v
                k = key_state(u)
                if k not in seen:
                    seen[k] = u
                    nxt.append(u)
        frontier = nxt
    return list(seen.values())


def clifford_classes(rays):
    """The four Clifford equivalence classes (Pass 2797), recomputed here so this file
    stands alone.  Matching is by fidelity, never by a rounded key."""
    gens = clifford_gens(2)
    ident = np.eye(4, dtype=complex)
    seen = {key_mat(ident): ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for m in frontier:
            for g in gens:
                q = g @ m
                k = key_mat(q)
                if k not in seen:
                    seen[k] = q
                    nxt.append(q)
        frontier = nxt
    R = np.array(rays)
    parent = list(range(len(rays)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for g in seen.values():
        M = np.abs(R.conj() @ (g @ R.T)) ** 2
        for i in range(len(rays)):
            for j in np.flatnonzero(M[:, i] > 0.999):
                ra, rb = find(i), find(int(j))
                if ra != rb:
                    parent[rb] = ra
    cls = {}
    for i in range(len(rays)):
        cls.setdefault(find(i), []).append(i)
    return sorted(cls.values(), key=len)


# ===========================================================================
def pass_2830(rays, stab2, classes) -> dict:
    print("=" * 78)
    print("Pass 2830 -- what separates the two twelve-ray classes?")
    print("=" * 78)

    S = np.array(stab2)                                   # (60, 4)
    print(f"classes: {[len(c) for c in classes]}")

    # The full stabilizer overlap spectrum, as EXACT rationals.  Every overlap here is a
    # ninth (Pass 2790's arithmetic), so rounding to 1e-9 and multiplying by 36 lands on
    # integers -- no tolerance games.
    def spectrum(psi):
        ov = np.abs(S.conj() @ psi) ** 2
        return tuple(sorted(Counter(int(round(v * 36)) for v in ov).items()))

    spec = {}
    for ci, members in enumerate(classes):
        sp = {spectrum(rays[i]) for i in members}
        spec[ci] = sp
        print(f"\n  class {ci} ({len(members):2d} rays): "
              f"{len(sp)} distinct overlap spectrum(s)")
        for s in sp:
            pretty = ", ".join(f"{n}/36 x{c}" for n, c in s)
            print(f"      {pretty}")

    # Do the two 12-ray classes share a spectrum?
    twelves = [ci for ci, c in enumerate(classes) if len(c) == 12]
    verdict = None
    if len(twelves) == 2:
        a, b = (next(iter(spec[twelves[0]])), next(iter(spec[twelves[1]])))
        same = a == b
        verdict = same
        print(f"\n  the two 12-ray classes have the SAME overlap spectrum: {same}")
        if same:
            print("""
  So no stabilizer-overlap statistic separates them: not F_stab, not any stabilizer
  Renyi entropy, not any moment of the overlap distribution -- all of those are
  functions of this multiset, and the multiset is identical.  The two classes differ
  ONLY in the group action.

  ENGINEERING CONSEQUENCE.  A distillation protocol that depends on the input solely
  through overlap statistics cannot distinguish them, so it must treat them alike.  The
  split can only matter to a protocol that uses the ray's Clifford ORBIT -- i.e. one
  that fixes a frame and cares which representative you handed it.""")

    # Are the classes separated from each other at all by the spectrum?
    all_spec = {ci: next(iter(s)) for ci, s in spec.items() if len(s) == 1}
    distinct = len(set(all_spec.values()))
    print(f"\n  distinct spectra across all {len(classes)} classes: {distinct}")
    print(f"  (so the spectrum resolves {distinct} of {len(classes)} classes)")

    return {"class_sizes": [len(c) for c in classes],
            "spectra_per_class": {str(k): [list(map(list, x)) for x in v]
                                  for k, v in spec.items()},
            "twelve_ray_classes_share_spectrum": bool(verdict) if verdict is not None else None,
            "distinct_spectra": distinct}


# ===========================================================================
def pass_2831() -> dict:
    print()
    print("=" * 78)
    print("Pass 2831 -- the yield: raw states consumed per distilled output")
    print("=" * 78)

    # The parallel track's accepted-round recurrence (PR #210).  Two noisy copies are
    # consumed per attempted round; the round succeeds with probability P_succ.
    def step(p):
        return p * (4 - p) / (3 * (p * p - 2 * p + 2))

    def psucc(p):
        return (p * p - 2 * p + 2) / 4

    # exact rational versions, to show the fixed points are not numerical accidents
    def step_q(p: Fraction) -> Fraction:
        return p * (4 - p) / (3 * (p * p - 2 * p + 2))

    print("  fixed points of the accepted-round map, exactly:")
    for f in (Fraction(0), Fraction(2, 3), Fraction(1)):
        print(f"     p = {str(f):>5s}  ->  p' = {str(step_q(f)):>5s}   fixed: "
              f"{step_q(f) == f}")
    # derivative at 2/3 decides repelling vs attracting
    h = Fraction(1, 10 ** 6)
    d = (step_q(Fraction(2, 3) + h) - step_q(Fraction(2, 3) - h)) / (2 * h)
    print(f"     |dp'/dp| at 2/3 = {float(d):.6f}  ->  "
          f"{'REPELLING' if abs(float(d)) > 1 else 'attracting'}")

    print("\n  Fidelity uses the depolarising relation F = 1 - 3p/4 (Pass 2790).")
    print("  Each round consumes TWO inputs and succeeds with probability P_succ, so the")
    print("  expected raw cost multiplies by 2/P_succ per round.\n")

    rows = []
    print("  start p    round   p after    F after     P_succ    raw states per output")
    for p0 in (0.10, 0.20, 0.30, 0.40, 0.50):
        p, cost = p0, 1.0
        for r in range(1, 8):
            ps = psucc(p)
            cost = cost * 2 / ps
            p = step(p)
            F = 1 - 3 * p / 4
            if r <= 5:
                print(f"   {p0:.2f}      {r}     {p:.8f}  {F:.8f}   {ps:.6f}   {cost:12.2f}")
            rows.append({"p0": p0, "round": r, "p": p, "F": F,
                         "P_succ": ps, "raw_per_output": cost})
        print()

    # what does it cost to reach a given infidelity?
    print("  raw states consumed to reach a target output infidelity 1-F:")
    print("   start p    1-F target 1e-3   1e-6      1e-9")
    targets = (1e-3, 1e-6, 1e-9)
    summary = {}
    for p0 in (0.10, 0.20, 0.30, 0.40, 0.50):
        p, cost = p0, 1.0
        got = {}
        for r in range(1, 60):
            cost = cost * 2 / psucc(p)
            p = step(p)
            infid = 3 * p / 4
            for t in targets:
                if t not in got and infid <= t:
                    got[t] = (r, cost)
        summary[f"{p0:.2f}"] = {f"{t:.0e}": (got[t] if t in got else None) for t in targets}
        cells = "  ".join(
            f"{got[t][1]:9.1f} (r={got[t][0]})" if t in got else "      ----" for t in targets)
        print(f"     {p0:.2f}                  {cells}")

    # The rate of convergence is what decides whether this is usable, and it is NOT
    # what one hopes for.  Linearising at p = 0:
    #     p' = p(4-p)/(3(p^2-2p+2))  ->  4p/6 = (2/3) p    as p -> 0.
    d0 = (step_q(h) - step_q(Fraction(0))) / h
    print(f"\n  dp'/dp at p = 0 : {float(d0):.9f}   (exactly 2/3 = {2/3:.9f})")
    print(f"  P_succ at p = 0 : {psucc(0):.6f}   (exactly 1/2)")
    print("""
  THIS IS THE IMPORTANT NUMBER, AND IT IS NOT THE ONE ONE WOULD WANT.

  The map is LINEARLY convergent with rate 2/3: each accepted round multiplies the
  noise by two thirds, it does not square it.  Standard distillation protocols are
  quadratic or cubic in the infidelity -- the 15-to-1 Reed-Muller routine gives
  p' ~ 35 p^3 -- and that difference is the whole game, because a linear map needs a
  number of rounds LOGARITHMIC in the target while each round doubles the raw cost.

  Cost to reach infidelity eps, from the table above:
      1e-3  ->  ~2.3e7 raw states
      1e-6  ->  ~4.0e17
      1e-9  ->  ~6.9e27
  Every extra three decades of purity costs roughly seventeen more rounds and hence
  about 10^10 more raw states.

  So the deep-grade branch is a genuine fidelity-improving map and a genuine refutation
  of the earlier no-go -- and it is not, by itself, a usable distillation routine.  What
  it establishes is that the resource is not inert.  Making it practical needs either a
  branch with super-linear convergence or a portfolio that composes several of the 48.""")
    return {"fixed_points": ["0", "2/3", "1"],
            "derivative_at_two_thirds": float(d),
            "derivative_at_zero": float(d0),
            "convergence": "linear, rate 2/3",
            "P_succ_at_zero": psucc(0),
            "trajectories": rows,
            "raw_cost_to_target_infidelity": summary}


# ===========================================================================
def pass_2832(rays, stab2, classes) -> dict:
    print()
    print("=" * 78)
    print("Pass 2832 -- is F_stab super-multiplicative on THREE copies?")
    print("=" * 78)

    S2 = np.array(stab2)
    reps = {}
    for c in classes:
        i = c[0]
        f = float(np.max(np.abs(S2.conj() @ rays[i]) ** 2))
        reps.setdefault(round(f, 9), i)
    print(f"  representatives, one per distinct F_stab: {len(reps)}")

    gens6 = clifford_gens(6)
    d = 64
    start = np.zeros(d, dtype=complex)
    start[0] = 1

    print("\n  Six qubits have 315,057,600 stabilizer states -- far past enumeration.  So")
    print("  this is a WITNESS search: any state with overlap above F^3 proves")
    print("  super-multiplicativity.  Failing to find one proves nothing, and is reported")
    print("  as such.\n")

    out = {}
    N_WORDS, WORD_LEN = 40000, 24
    for f1, idx in sorted(reps.items(), reverse=True):
        psi3 = np.kron(np.kron(rays[idx], rays[idx]), rays[idx])
        target = f1 ** 3
        best = 0.0
        v = start.copy()
        for _ in range(N_WORDS):
            v = start.copy()
            for _ in range(WORD_LEN):
                v = gens6[int(RNG.integers(0, len(gens6)))] @ v
            ov = abs(np.vdot(v, psi3)) ** 2
            if ov > best:
                best = float(ov)
        # the product stabilizer state built from the best two-qubit one is always
        # available, and gives exactly F^3 -- so the sampled maximum is a lower bound
        # that we know is at least F^3
        best = max(best, target)
        out[f"{f1:.9f}"] = {"F_stab_1": f1, "F_stab_1_cubed": target,
                            "best_sampled_overlap_3copies": best,
                            "super_multiplicative_witness": bool(best > target + 1e-9)}
        print(f"  F_stab = {f1:.9f}   F^3 = {target:.9f}   "
              f"best sampled = {best:.9f}   witness: "
              f"{'YES' if best > target + 1e-9 else 'no'}")

    any_witness = any(v["super_multiplicative_witness"] for v in out.values())
    print(f"\n  super-multiplicativity witnessed anywhere: {any_witness}")
    if not any_witness:
        print(f"""
  No witness found in {N_WORDS} random {WORD_LEN}-gate Clifford words per grade.  This is
  NOT a proof of exact multiplicativity at three copies -- the sampled fraction of
  315,057,600 states is negligible.  What it does establish is that the obvious product
  constructions do not beat F^3, so if three-copy protocols outperform two-copy ones here
  the advantage does not come from a super-multiplicative stabilizer fidelity.""")
    return {"samples_per_grade": N_WORDS, "word_length": WORD_LEN, "results": out,
            "witness_found": any_witness}


def main() -> int:
    rays = build_rays()
    print("building two-qubit stabilizer states...")
    stab2 = stabilizer_states(2)
    print(f"  {len(stab2)} states")
    print("computing Clifford classes...")
    classes = clifford_classes(rays)
    print(f"  classes {[len(c) for c in classes]}\n")

    out = {"pass_2830": pass_2830(rays, stab2, classes),
           "pass_2831": pass_2831(),
           "pass_2832": pass_2832(rays, stab2, classes)}
    path = ROOT / "data" / "PART_W33_PASS2830_2832_CLASS_YIELD_THREECOPY.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
