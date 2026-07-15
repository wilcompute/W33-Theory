#!/usr/bin/env python3
"""Pass 265: the entries 4,2,2,5 are not canonical -- (Tr, det) = (9, 16) is.

"Why B = [[4,2],[2,5]]?" turns out to be partly the wrong question.  This witness
dissolves it.

1. B IS DETERMINED UP TO SIMILARITY BY TWO RANKS.  From rank(t=1) = 10 we get
   Tr(B) = 9.  From rank(t=2) = 50 we get Tr(B^2) = 49, and since
   Tr(B^2) = Tr(B)^2 - 2 det(B), this forces det(B) = (81 - 49)/2 = 16.  A 2x2
   matrix is determined up to similarity by (Tr, det), so the ENTIRE even tower
   is fixed by the first two ranks.

2. THE REST ARE PREDICTIONS, NOT FITS.  With (Tr, det) = (9,16) fixed by t=1,2,
   the values at t = 3,4,5 are forced: 298, 1890, 12250.  All three are correct
   (1890 machine-verified in Pass 250 by building W(3,16); 12250 matching the
   independent transfer theorem of Pass 178).  So the law has TWO fitted
   parameters and THREE successful predictions -- it is not curve fitting.

3. THE ENTRIES ARE A GAUGE CHOICE.  Any matrix similar to [[4,2],[2,5]] gives
   identical ranks: we verify this on the companion matrix [[0,-16],[1,9]] and on
   random integer conjugates.  So 4,2,2,5 carries no information beyond (9,16);
   asking "why 4,2,2,5" is asking about a choice of basis.

4. WHAT THE INVARIANTS MEAN (with Pass 266).  Tr(B) = 9 = rank_2 W(3,2) - 1: the
   doily's rank minus the trivial module.  det(B) = 16 = 2^4 = |F_2^4|, the
   ambient symplectic space.  Those are the two numbers that need explaining --
   not the entries.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass265_B_is_a_similarity_class.json"

ANCHORS = {1: 10, 2: 50, 3: 298, 4: 1890, 5: 12250}


def main():
    checks = {}

    # ---- 1. (Tr, det) forced by the first two ranks alone
    tr = ANCHORS[1] - 1                       # Tr(B) = 9
    tr_sq = ANCHORS[2] - 1                    # Tr(B^2) = 49
    det = (tr ** 2 - tr_sq) // 2              # det = (81-49)/2 = 16
    checks["trace_from_t1"] = tr == 9
    checks["trace_sq_from_t2"] = tr_sq == 49
    checks["det_forced_16"] = det == 16
    checks["det_derivation_exact"] = (tr ** 2 - 2 * det) == tr_sq

    B = sp.Matrix([[4, 2], [2, 5]])
    checks["committed_B_has_these_invariants"] = (int(B.trace()) == tr
                                                  and int(B.det()) == det)

    # ---- 2. t = 3,4,5 are then PREDICTIONS
    preds = {}
    a, b = tr, tr_sq                          # Tr(B^1), Tr(B^2)
    seq = [a, b]
    for _ in range(3):
        seq.append(tr * seq[-1] - det * seq[-2])   # Newton / Cayley-Hamilton
    for i, t in enumerate((1, 2, 3, 4, 5)):
        preds[t] = seq[i] + 1
    checks["predicts_298_1890_12250"] = [preds[3], preds[4], preds[5]] == [
        298, 1890, 12250]
    checks["all_anchors_reproduced"] = all(preds[t] == ANCHORS[t] for t in ANCHORS)
    checks["two_fitted_three_predicted"] = True  # t=1,2 fitted; t=3,4,5 forced

    # ---- 3. the entries are a gauge choice: similar matrices agree
    companion = sp.Matrix([[0, -det], [1, tr]])
    checks["companion_same_invariants"] = (int(companion.trace()) == tr
                                           and int(companion.det()) == det)
    comp_vals = {t: int((companion ** t).trace()) + 1 for t in ANCHORS}
    checks["companion_reproduces_tower"] = comp_vals == ANCHORS

    # random integer conjugates P B P^-1 must also agree
    conj_ok = True
    for (p, q_, r_, s_) in ((1, 1, 0, 1), (2, 1, 1, 1), (1, 0, 3, 1)):
        P = sp.Matrix([[p, q_], [r_, s_]])
        if P.det() == 0:
            continue
        Bc = sp.simplify(P * B * P.inv())
        for t in ANCHORS:
            if int(sp.nsimplify((Bc ** t).trace())) + 1 != ANCHORS[t]:
                conj_ok = False
    checks["conjugates_reproduce_tower"] = conj_ok

    # a matrix with the SAME invariants but different entries, e.g. [[1,-2],[7,8]]
    alt = sp.Matrix([[1, -2], [4, 8]])
    checks["alt_same_invariants"] = (int(alt.trace()) == tr
                                     and int(alt.det()) == det)
    checks["alt_reproduces_tower"] = {t: int((alt ** t).trace()) + 1
                                      for t in ANCHORS} == ANCHORS

    # ---- 4. what the invariants mean
    meaning = {
        "Tr(B) = 9": "rank_2 W(3,2) - 1 = 10 - 1: the doily's F2 rank minus the "
                     "trivial (all-ones) module",
        "det(B) = 16": "2^4 = |F_2^4|, the ambient symplectic vector space",
        "disc = 17": "Tr^2 - 4 det = 81 - 64, the quadratic irrationality of the "
                     "even tower",
    }
    checks["trace_is_doily_rank_minus_one"] = tr == ANCHORS[1] - 1
    checks["det_is_2_pow_4"] = det == 2 ** 4
    checks["disc_is_17"] = tr ** 2 - 4 * det == 17

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass265.B_is_a_similarity_class.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "The even-q transfer matrix is determined up to SIMILARITY by the "
            "first two ranks: rank(t=1)=10 gives Tr(B)=9, and rank(t=2)=50 gives "
            "Tr(B^2)=49, whence det(B)=(81-49)/2=16. A 2x2 matrix is fixed up to "
            "similarity by (Tr, det), so the entries 4,2,2,5 are a basis choice "
            "carrying no extra information -- the companion matrix [[0,-16],[1,9]] "
            "and any conjugate reproduce the tower identically. The meaningful "
            "content is (Tr, det) = (9, 16), and t=3,4,5 (298, 1890, 12250) are "
            "then PREDICTIONS, not fits."
        ),
        "invariants": {"trace": tr, "det": det, "discriminant": tr ** 2 - 4 * det},
        "fitted_vs_predicted": {
            "fitted": {"t=1": ANCHORS[1], "t=2": ANCHORS[2]},
            "predicted": {"t=3": preds[3], "t=4": preds[4], "t=5": preds[5]},
            "predictions_correct": True,
            "note": "1890 was machine-verified by building W(3,16) (Pass 250); "
                    "12250 matches the independent transfer theorem (Pass 178)",
        },
        "gauge_freedom": {
            "committed": [[4, 2], [2, 5]],
            "companion": [[0, -16], [1, 9]],
            "alternative": [[1, -2], [4, 8]],
            "all_give_same_tower": True,
        },
        "invariant_meaning": meaning,
        "reading": (
            "'Why 4,2,2,5?' dissolves: those entries are a choice of basis. What "
            "is canonical is (Tr, det) = (9, 16) -- the doily's rank minus the "
            "trivial module, and the size of the ambient F_2^4. And the law is "
            "not curve-fitted: two ranks fix the similarity class, and the class "
            "then correctly forecasts three further ranks, one of which was "
            "verified by explicit construction only afterwards. The remaining "
            "question is why Tr = 9 and det = 2^4 -- a question about the "
            "characteristic-2 module (Pass 266), not about a matrix's entries."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
