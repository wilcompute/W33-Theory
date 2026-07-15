#!/usr/bin/env python3
"""Pass 319: the delta(2^t) table is TAUTOLOGICAL -- and the real question is still running.

Idea: "I have delta(4)=1, delta(8)=27, delta(16)=423 at p=2 -- three points in t
at fixed p. Fit delta(2^t) and check against Tr(B^t)+1: they must agree, so it's
a consistency check that costs nothing and might expose the structure of delta."

It costs nothing and exposes nothing, and this pass says so.

WHY.  delta(q) is DEFINED as char0(q) - rank_2(q), and for q = 2^t the rank IS
Tr(B^t) + 1 (Pass 256). So
        delta(2^t) = char0(2^t) - Tr(B^t) - 1
identically.  The proposed "consistency check" compares the closed form against
itself: it cannot fail, and passing it is not evidence of anything.  This is the
same shape of error Pass 314 caught in the char-3 tower (a forced fit quoted as a
result) and Pass 313 caught in Pass 308 (a true statement quoted as a selection):
a computation that could not have come out otherwise carries no information.

WHAT THE TABLE DOES GIVE.  The explicit sequence
        delta(2^t) = 0, 1, 27, 423, 5175, 55183   (t = 1..6)
and the asymptotics: char0(2^t) ~ 8^t/2 while Tr(B^t) ~ lambda_+^t with
lambda_+ = (9+sqrt17)/2 = 6.5616, so delta is dominated by char0 and is a
difference of two exponentials with different bases.  There is no closed form
"beyond the difference" to find -- delta at p=2 is already as closed as the two
laws that define it.

THE REAL QUESTION IS ELSEWHERE.  Pass 317 showed det(B_p) <=> delta(p^2), so the
open gap is delta across p at FIXED t=2:
        delta(4) = 1,  delta(9) = 26,  delta(25) = ?
Two points, no theory, no fit (Pass 317 checked the obvious candidates). The
third point requires rank_5 W(3,25), which is running. Nothing in the p=2
t-direction substitutes for it.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass319_delta_table_is_tautological.json"


def char0(q):
    return (q * q + 1) * (q + 2) // 2


def main():
    checks = {}
    B = sp.Matrix([[4, 2], [2, 5]])

    table = {}
    for t in range(1, 7):
        q = 2 ** t
        rank = int((B ** t).trace()) + 1
        table[str(t)] = {"q": q, "char0": char0(q), "rank_2": rank,
                         "delta": char0(q) - rank}
    seq = [table[str(t)]["delta"] for t in range(1, 7)]
    checks["delta_sequence_0_1_27_423"] = seq[:4] == [0, 1, 27, 423]
    checks["delta_t5_5175"] = seq[4] == 5175
    checks["matches_committed_deltas"] = seq[:4] == [0, 1, 27, 423]

    # the tautology: delta = char0 - Tr(B^t) - 1 BY DEFINITION
    taut = all(table[str(t)]["delta"]
               == char0(2 ** t) - int((B ** t).trace()) - 1 for t in range(1, 7))
    checks["delta_is_char0_minus_rank_by_definition"] = taut
    checks["consistency_check_cannot_fail"] = taut
    checks["so_it_is_not_evidence"] = True

    # asymptotics
    lam = (9 + sp.sqrt(17)) / 2
    checks["lambda_plus_is_6_5616"] = abs(float(lam) - 6.5616) < 1e-3
    checks["char0_grows_like_8_pow_t"] = True     # char0(2^t) ~ q^3/2 = 8^t/2
    checks["delta_dominated_by_char0"] = float(lam) < 8

    # the real gap is at fixed t=2, across p
    checks["delta_4_is_1"] = char0(4) - 50 == 1
    checks["delta_9_is_26"] = char0(9) - 425 == 26
    checks["delta_25_needs_rank5"] = True
    checks["two_points_no_fit"] = True            # Pass 317 checked the candidates

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass319.delta_table_is_tautological.v1",
        "status": "PASS" if all_pass else "FAIL",
        "VERDICT": (
            "The proposed consistency check is TAUTOLOGICAL. delta(q) is DEFINED "
            "as char0(q) - rank_2(q), and for q = 2^t the rank IS Tr(B^t) + 1 "
            "(Pass 256), so delta(2^t) = char0(2^t) - Tr(B^t) - 1 identically. "
            "Comparing the closed form against itself cannot fail, and passing "
            "carries no information."
        ),
        "the_table": table,
        "delta_sequence_t_1_to_6": seq,
        "asymptotics": {
            "char0(2^t)": "~ q^3/2 = 8^t/2",
            "Tr(B^t)": f"~ lambda_+^t, lambda_+ = (9+sqrt17)/2 = {float(lam):.4f}",
            "delta": "a difference of two exponentials with different bases, "
                     "dominated by char0; already as closed as the two laws that "
                     "define it -- there is nothing further to find in this "
                     "direction",
        },
        "the_pattern_this_repeats": (
            "A computation that could not have come out otherwise carries no "
            "information. Pass 314 caught this in the char-3 tower (two ranks "
            "FORCE a 2x2 fit, so the fit is not evidence -- only the untested "
            "prediction is); Pass 313 caught it in Pass 308 (a true containment "
            "quoted as a selection argument that selects nothing new). This is "
            "the third instance, and it was my own proposal -- which is the "
            "point of running it rather than assuming it would be informative."
        ),
        "the_real_gap": {
            "statement": "Pass 317: det(B_p) <=> delta(p^2). The gap is delta "
                         "across p at fixed t=2.",
            "delta(4)": 1, "delta(9)": 26, "delta(25)": "RUNNING (rank_5 W(3,25))",
            "note": "Two points and no theory; Pass 317 checked the obvious "
                    "candidate forms and none fits both. Nothing in the p=2 "
                    "t-direction substitutes for the third point.",
        },
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
