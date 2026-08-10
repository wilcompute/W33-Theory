#!/usr/bin/env python3
"""Pass 4691 -- I checked the premise Pass 4688 refused to assume, and it fails. So does my
own denominator.

Pass 4688 computed that the three-copy distillation search collapses from 315,057,600 to 26
IF the condition is invariant under the full local Clifford group, and explicitly refused to
assert that branch: "the difference is decided by one reading of the protocol, not by more
computation."  This is that reading, and it goes the unfavourable way twice.

TWO CORRECTIONS, THE FIRST TO MY OWN WORK.

1. THE DENOMINATOR WAS WRONG, AND WRONG IN THE DIRECTION THAT FLATTERED THE SEARCH.
   Pass 4680 priced the null against 315,057,600 = the number of MAXIMAL stabilizer groups
   on six qubits.  But Pass 2881 does not sample maximal groups.  It samples SYNDROME
   PROJECTORS built from k in {1,2,3,4} commuting generators with independent signs -- a
   different and much larger space, because a k-generator group with k < 6 is not maximal
   and the sign choice multiplies it again.  Counting isotropic k-subspaces of the symplectic
   F_2^12 and their sign assignments gives the real figure below.  The power of the 30,000-
   sample null is therefore LOWER than Pass 4680 said, not higher.

2. THE LOCAL-CLIFFORD REDUCTION DOES NOT APPLY.
   The clean input is |m>^{tensor 3} for a FIXED ray m in C^4 with cube-root-of-unity
   amplitudes -- a magic state, not a stabilizer state.  The nine "single-error" vectors are
   an orthonormal complement basis, so the space they span is (m^perp ox m ox m) + (m ox
   m^perp ox m) + (m ox m ox m^perp), which depends only on the RAY [m].  A local Clifford U
   maps this instance to a valid instance if and only if U fixes that ray.  The symmetry
   group is therefore the local-Clifford stabiliser of [m], NOT the full local Clifford
   group -- and that stabiliser is computed here by exhaustion over all 576 local Cliffords
   per copy.

    py -3 analysis/w33_pass4691_the_premise_is_false_and_my_denominator_was_wrong.py
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

W = np.exp(2j * np.pi / 3)


def isotropic_subspaces(n: int, k: int) -> int:
    """Number of k-dimensional isotropic subspaces of the symplectic space F_2^{2n}."""
    if k == 0:
        return 1
    ordered = 1
    for j in range(1, k + 1):
        ordered *= (2 ** (2 * n - j + 1) - 2 ** (j - 1))
    glk = 1
    for i in range(k):
        glk *= (2 ** k - 2 ** i)
    return ordered // glk


def single_qubit_cliffords():
    """The 24 single-qubit Clifford operations, as matrices modulo global phase."""
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.array([[1, 0], [0, 1j]], dtype=complex)
    I = np.eye(2, dtype=complex)

    def key(M):
        # canonical form modulo global phase: divide by first nonzero entry's phase
        f = M.flatten()
        i = int(np.argmax(np.abs(f) > 1e-9))
        M = M * np.exp(-1j * np.angle(f[i]))
        return tuple(np.round(M.flatten(), 6))

    seen, out, frontier = {key(I)}, [I], [I]
    while frontier:
        M = frontier.pop()
        for G in (H, S):
            N = G @ M
            k = key(N)
            if k not in seen:
                seen.add(k)
                out.append(N)
                frontier.append(N)
    return out


def build_ray():
    v = np.array([0, 1, -1, 1], dtype=complex) * np.array([1, 1, W, W], dtype=complex)
    v = np.array([0, 1, -W, W], dtype=complex)
    return v / np.linalg.norm(v)


def main() -> int:
    print("=" * 78)
    print("Pass 4691 -- the premise, read rather than assumed")
    print("=" * 78)

    # ---- correction 1: the real size of the searched space ----------------
    print("\n  CORRECTION 1 -- what Pass 2881 actually samples\n")
    print(f"  {'k gens':>7s} {'isotropic k-subspaces':>23s} {'x 2^k signs':>18s}")
    total = 0
    rows = []
    for k in (1, 2, 3, 4):
        s = isotropic_subspaces(6, k)
        p = s * 2 ** k
        total += p
        rows.append({"k": k, "subspaces": s, "projectors": p})
        print(f"  {k:7d} {s:23,d} {p:18,d}")
    print(f"  {'TOTAL':>7s} {'':>23s} {total:18,d}")

    MAXIMAL = 315_057_600
    SAMPLES = 30_000
    print(f"""
    PASS 4680 USED {MAXIMAL:,} -- THE NUMBER OF MAXIMAL STABILIZER GROUPS. The search does
    not sample those. It samples syndrome projectors from 1 to 4 commuting generators with
    independent signs, and there are {total:,} of them: {total/MAXIMAL:.1f}x more.

    So the coverage was not 0.0095% but {100*SAMPLES/total:.6f}%, and every power figure in
    Pass 4680 was optimistic by a factor of {total/MAXIMAL:.1f}. Against a hundred-witness set the
    power was not 0.95% but {100*(1-(1-100/total)**SAMPLES):.3f}%. The null is weaker evidence than the pass
    that criticised it for being weak evidence said it was.""")

    # ---- correction 2: the symmetry group -------------------------------
    print("\n  CORRECTION 2 -- is the condition local-Clifford invariant?\n")
    m = build_ray()
    C1 = single_qubit_cliffords()
    print(f"    single-qubit Cliffords (mod phase) : {len(C1)}")
    print(f"    local Cliffords per 2-qubit copy   : {len(C1)**2}")

    fix = 0
    for A, B in itertools.product(C1, repeat=2):
        v = np.kron(A, B) @ m
        # does it fix the RAY [m]?
        if abs(abs(np.vdot(m, v)) - 1.0) < 1e-9:
            fix += 1
    print(f"    of those, fixing the ray [m]       : {fix}")

    copies = math.factorial(3)
    group = fix ** 3 * copies
    print(f"    symmetry group of the instance     : {fix}^3 x 3! = {group:,}")

    print(f"""
    THE CLEAN INPUT IS A MAGIC STATE, WHICH IS WHY THIS FAILS. |m> has cube-root-of-unity
    amplitudes and is not a stabilizer state, so almost no local Clifford fixes its ray --
    {fix} of {len(C1)**2} per copy. The nine error vectors span a space determined by [m] alone, so an
    element fixing the ray fixes the whole instance and nothing else does.

    THE REDUCTION IS {group:,}x, NOT 12,117,600x. That takes the search from {total:,}
    to about {total//group:,} orbit representatives -- still far beyond enumeration, and
    {(total//group)/26:,.0f} times the 26 classes Pass 4688 computed under the favourable branch.

    PASS 4688'S NUMBER WAS NOT WRONG; IT WAS ANSWERING A DIFFERENT QUESTION. 26 is the count
    of local-Clifford classes of stabilizer STATES, and it would be the right count if the
    instance were LC-invariant. The instance is not, because a magic state has almost no
    local-Clifford symmetry -- which is very close to what makes it magic in the first place.
    That is the whole content of the premise Pass 4688 declined to assume, and declining was
    correct: asserting it would have claimed a nine-order-of-magnitude reduction that does
    not exist.""")

    out = {
        "boundary": ("both corrections are exact counts. The isotropic-subspace formula is "
                     "standard and the ray-stabiliser is found by exhaustion over all 576 "
                     "local Cliffords per copy, modulo global phase. This pass does NOT run "
                     "the distillation search, does not settle whether a witness exists, and "
                     "does not claim the 3!-copy-permutation factor is the full non-local "
                     "symmetry -- only that the LOCAL Clifford part is 3 per copy"),
        "correction_1_denominator": {
            "pass_4680_used": MAXIMAL,
            "actual_projector_space": total,
            "understatement_factor": total / MAXIMAL,
            "per_k": rows,
            "true_coverage_fraction": SAMPLES / total,
            "true_power_vs_100_witnesses": 1 - (1 - 100 / total) ** SAMPLES,
            "note": ("Pass 2881 samples syndrome projectors from k<=4 commuting generators "
                     "with signs, not maximal stabilizer groups; 4680's power figures were "
                     "optimistic by this factor")},
        "correction_2_symmetry": {
            "single_qubit_cliffords": len(C1),
            "local_cliffords_per_copy": len(C1) ** 2,
            "fixing_the_ray": fix,
            "copy_permutations": copies,
            "instance_symmetry_group": group,
            "orbit_representatives": total // group,
            "lc_invariance_holds": False,
            "reason": ("the clean input is a magic state with cube-root-of-unity amplitudes, "
                       "so its local-Clifford ray stabiliser is tiny; Pass 4688's 26 classes "
                       "count LC-classes of stabilizer states and answer a different "
                       "question")},
        "conclusion": (
            "the favourable branch of Pass 4688 is FALSE: the reduction is a few hundred, "
            "not twelve million, because a magic state has almost no local-Clifford "
            "symmetry. Separately, Pass 4680's denominator was 12.2x too small, so the "
            "30,000-sample null has even less power than that pass reported"),
    }
    p = ROOT / "data" / "PART_W33_PASS4691_PREMISE_FALSE_DENOMINATOR_WRONG.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
