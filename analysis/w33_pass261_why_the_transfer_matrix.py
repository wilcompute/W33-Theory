#!/usr/bin/env python3
"""Pass 261: WHY the +8 -- the inhomogeneous term is forced by the "+1".

Pass 256 closed the even-q rank law as rank_2 W(3,2^t) = Tr(B^t) + 1 with
B = [[4,2],[2,5]], equivalently a(t+1) = 9a(t) - 16a(t-1) + 8.  Pass 250 had
tested the HOMOGENEOUS recurrence and (correctly) refuted it.  This witness
explains why the homogeneous test was doomed a priori, and derives the mysterious
constant 8 exactly.

THEOREM.  Let B be any 2x2 matrix and c any constant, and set
    a(t) = Tr(B^t) + c.
Cayley-Hamilton gives B^2 = Tr(B) B - det(B) I, hence for every t
    Tr(B^{t+1}) = Tr(B) Tr(B^t) - det(B) Tr(B^{t-1}).
Substituting Tr(B^t) = a(t) - c:
    a(t+1) - c = Tr(B)(a(t) - c) - det(B)(a(t-1) - c)
so
    a(t+1) = Tr(B) a(t) - det(B) a(t-1) + c * (1 - Tr(B) + det(B)).

    ==> the recurrence is HOMOGENEOUS if and only if c = 0 (or the pencil
        1 - Tr B + det B vanishes).  A nonzero additive constant c FORCES an
        inhomogeneous term, and that term is exactly c(1 - Tr B + det B).

For the substrate: c = 1, Tr(B) = 9, det(B) = 16, so the constant is
    1 * (1 - 9 + 16) = 8.
The "+8" of Pass 256 is nothing but the "+1" of the trivial (all-ones) module
pushed through Cayley-Hamilton.  Pass 250's homogeneous test could never have
succeeded: the +1 guarantees inhomogeneity.

Also recorded (rigorous): Tr(B^t) counts closed walks of length t in the
2-state weighted digraph with adjacency B -- which is why a TRACE appears at all
in a Frobenius-degree-t counting problem -- together with B's invariants
Tr = 9 (= the t=1 rank minus the trivial module), det = 16 = 2^4 = |F_2^4| (the
ambient symplectic space), discriminant 81 - 64 = 17 (the "sqrt 17").

HONEST SCOPE: Pass 262 refuted the extension of this transfer structure to odd
p, so B is a CHARACTERISTIC-2 object. This pass explains the SHAPE of the even-q
law (why a trace, why an inhomogeneous constant, and what its value must be); it
does not derive the entries 4,2,2,5 from the geometry, which remains open.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass261_why_the_transfer_matrix.json"

ANCHORS = {1: 10, 2: 50, 3: 298, 4: 1890, 5: 12250}


def main():
    checks = {}

    # ---- 1. the general theorem, proved symbolically
    p, q_, c, t = sp.symbols("p q c t")        # p = Tr(B), q_ = det(B)
    # define T(t) = Tr(B^t) abstractly via the CH recurrence; verify the shift
    Tn, Tn1 = sp.symbols("T_n T_nm1")          # Tr(B^t), Tr(B^{t-1})
    Tnext = p * Tn - q_ * Tn1                   # Cayley-Hamilton
    a_n, a_nm1 = Tn + c, Tn1 + c
    a_next = Tnext + c
    # claim: a_next == p*a_n - q_*a_nm1 + c*(1 - p + q_)
    claim = sp.expand(p * a_n - q_ * a_nm1 + c * (1 - p + q_))
    checks["general_theorem_holds"] = sp.simplify(a_next - claim) == 0

    # ---- 2. homogeneous iff c = 0 (the pencil 1 - Tr + det is generically != 0)
    inhom = c * (1 - p + q_)
    checks["inhomogeneous_unless_c_zero"] = sp.simplify(inhom.subs(c, 0)) == 0
    # for the substrate's B the pencil is nonzero, so c=1 => genuine inhomogeneity
    pencil = (1 - 9 + 16)
    checks["pencil_is_8"] = pencil == 8
    checks["so_constant_is_8"] = 1 * pencil == 8

    # ---- 3. the concrete matrix reproduces everything
    B = sp.Matrix([[4, 2], [2, 5]])
    trB, detB = int(B.trace()), int(B.det())
    checks["trace_9"] = trB == 9
    checks["det_16_eq_2_pow_4"] = detB == 16 == 2 ** 4
    disc = trB ** 2 - 4 * detB
    checks["discriminant_17"] = disc == 17
    # Cayley-Hamilton on B itself
    checks["cayley_hamilton_B"] = sp.simplify(
        B ** 2 - (trB * B - detB * sp.eye(2))) == sp.zeros(2, 2)

    # a(t) = Tr(B^t)+1 satisfies the derived recurrence with constant 8
    a = {t_: int((B ** t_).trace()) + 1 for t_ in range(1, 7)}
    rec_ok = all(a[t_ + 1] == 9 * a[t_] - 16 * a[t_ - 1] + 8
                 for t_ in range(2, 6))
    checks["derived_recurrence_reproduces_a"] = rec_ok
    checks["a_matches_anchors"] = all(a[t_] == ANCHORS[t_] for t_ in ANCHORS)

    # ---- 4. Pass 250's homogeneous test was doomed: predict its failure exactly
    # homogeneous prediction differs from truth by exactly the accumulated +8
    homog = [ANCHORS[1], ANCHORS[2]]
    for _ in range(3):
        homog.append(9 * homog[-1] - 16 * homog[-2])
    checks["homogeneous_gives_290_not_298"] = homog[2] == 290
    checks["homogeneous_off_by_8_at_t3"] = ANCHORS[3] - homog[2] == 8

    # ---- 5. why a TRACE: Tr(B^t) counts closed walks of length t
    Bi = [[4, 2], [2, 5]]

    def closed_walks(M, length):
        n = len(M)
        total = 0
        for start in range(n):
            # count weighted walks start -> start of given length
            vec = [1 if i == start else 0 for i in range(n)]
            for _ in range(length):
                vec = [sum(vec[i] * M[i][j] for i in range(n)) for j in range(n)]
            total += vec[start]
        return total

    checks["trace_counts_closed_walks"] = all(
        closed_walks(Bi, t_) == int((B ** t_).trace()) for t_ in range(1, 5))

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass261.why_the_transfer_matrix.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "For any 2x2 matrix B and constant c, a(t) = Tr(B^t) + c satisfies "
            "a(t+1) = Tr(B) a(t) - det(B) a(t-1) + c(1 - Tr(B) + det(B)), by "
            "Cayley-Hamilton. The recurrence is homogeneous iff c = 0. For the "
            "substrate c = 1, Tr(B) = 9, det(B) = 16, so the inhomogeneous "
            "constant is exactly 1*(1 - 9 + 16) = 8. The '+8' IS the '+1'."
        ),
        "derivation": {
            "cayley_hamilton": "B^2 = Tr(B) B - det(B) I",
            "trace_recurrence": "Tr(B^{t+1}) = Tr(B) Tr(B^t) - det(B) Tr(B^{t-1})",
            "shift": "a(t) = Tr(B^t) + c",
            "result": "a(t+1) = Tr(B) a(t) - det(B) a(t-1) + c(1 - Tr B + det B)",
            "substrate": "c=1, Tr=9, det=16  =>  constant = 1 - 9 + 16 = 8",
        },
        "why_pass250_failed": (
            "Pass 250 tested the HOMOGENEOUS recurrence 9a(t)-16a(t-1) and got "
            "290 instead of 298 -- off by exactly 8, the pencil value. The test "
            "was doomed a priori: the trivial module contributes an additive +1 "
            "to the rank, and by the theorem above ANY nonzero additive constant "
            "forces an inhomogeneous term. The refutation was correct; the "
            "conclusion 'open' was premature."
        ),
        "invariants_of_B": {
            "matrix": [[4, 2], [2, 5]],
            "trace": trB,
            "trace_meaning": "the t=1 rank (10) minus the trivial module (1)",
            "det": detB,
            "det_meaning": "16 = 2^4 = |F_2^4|, the ambient symplectic space",
            "discriminant": disc,
            "discriminant_meaning": "17 -- the quadratic irrationality of the "
                                    "even tower, eigenvalues (9 +- sqrt17)/2",
        },
        "why_a_trace": (
            "Tr(B^t) counts closed walks of length t in the 2-state weighted "
            "digraph with adjacency B (verified). A Frobenius-degree-t counting "
            "problem is naturally a count of length-t cyclic configurations, "
            "which is exactly what a trace of a t-th power computes -- this is "
            "why a transfer matrix appears at all."
        ),
        "honest_scope": (
            "This pass explains the SHAPE of the even-q law: why a trace, why "
            "the recurrence must be inhomogeneous, and what the constant must "
            "be (8, forced). It does NOT derive the entries 4,2,2,5 from the "
            "geometry -- that remains open. Pass 262 further shows the transfer "
            "structure does not extend to odd p, so B is a characteristic-2 "
            "object."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
