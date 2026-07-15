#!/usr/bin/env python3
"""Pass 312: formalise the rank law's LAST GAP -- det(B_p) -- in Lean.

Pass 284 formalised the even-q recurrence and the Cayley-Hamilton derivation of
the +8. Since then the picture sharpened: Pass 270 identified Tr B as the doily's
rank minus the trivial module; Pass 287 showed the "trace law" is a tautology;
Pass 281 REFUTED the det = |ambient| conjecture (det(B_3) = 76, not 81). So det
is the only unexplained quantity left, and it is now small enough to state in
Lean as data plus the one-line refutation.

Added to formal/W33/RankLaw.lean:
    det_B2                      : (9^2 - 49)/2 = 16
    det_B3                      : (24^2 - 424)/2 = 76
    det_is_not_p_pow_four       : (76 : Z) != 3^4        -- Pass 281 in one line
    det_B2_coincides_with_ambient : (16 : Z) = 2^4       -- the coincidence that misled 275

Same honest scope as Pass 284: there is no Lean toolchain here, so this is a
STRUCTURAL certification plus an independent Python re-verification of every
arithmetic claim. It is NOT a kernel check.
"""
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "W33" / "RankLaw.lean"
OUT = ROOT / "data" / "w33_pass312_lean_det_gap.json"

def main():
    checks = {}
    src = LEAN.read_text(encoding="utf-8")
    body = re.sub(r"/-.*?-/", "", src, flags=re.S)
    checks["file_exists"] = LEAN.exists()
    checks["no_sorry"] = "sorry" not in body
    for name in ("det_B2", "det_B3", "det_is_not_p_pow_four",
                 "det_B2_coincides_with_ambient"):
        checks[f"states_{name}"] = f"theorem {name}" in body
    # the earlier Pass 284 content is still there
    for name in ("a_three", "shifted_recurrence", "constant_is_eight"):
        checks[f"pass284_{name}_retained"] = f"theorem {name}" in body

    # independent Python re-verification
    checks["py_det_B2_is_16"] = (9 ** 2 - 49) // 2 == 16
    checks["py_det_B3_is_76"] = (24 ** 2 - 424) // 2 == 76
    checks["py_76_is_not_81"] = 76 != 3 ** 4
    checks["py_16_is_2_pow_4"] = 16 == 2 ** 4
    # and the traces they come from
    checks["py_Tr_B2_from_rank"] = 10 - 1 == 9
    checks["py_Tr_B3_from_rank"] = 25 - 1 == 24
    checks["py_TrB2sq_from_rank"] = 50 - 1 == 49
    checks["py_TrB3sq_from_rank"] = 425 - 1 == 424

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass312.lean_det_gap.v1",
        "status": "PASS" if all_pass else "FAIL",
        "file": "formal/W33/RankLaw.lean",
        "the_last_gap": (
            "det(B_p) is the only unexplained quantity in the rank story. "
            "Tr(B_p) is a tautology (Pass 287); the +8 is forced by "
            "Cayley-Hamilton (Pass 261); the '+1' is the all-ones module (Pass "
            "270); and det = |ambient| is REFUTED (Pass 281: det(B_3) = 76, not "
            "3^4 = 81). Only the values 16 and 76 remain, with no closed form."
        ),
        "added_theorems": {
            "det_B2": "(9^2 - 49)/2 = 16, from rank_2 W(3,2)=10 and W(3,4)=50",
            "det_B3": "(24^2 - 424)/2 = 76, from rank_3 W(3,3)=25 and W(3,9)=425",
            "det_is_not_p_pow_four": "(76 : Z) != 3^4 -- Pass 281's refutation in one line",
            "det_B2_coincides_with_ambient": "(16 : Z) = 2^4 -- the p=2 coincidence that misled Pass 275",
        },
        "honest_scope": (
            "NOT kernel-checked: no Lean toolchain here, so this is a STRUCTURAL "
            "certification (parses as expected, states the claimed theorems, no "
            "sorry) plus an INDEPENDENT Python re-verification of every "
            "arithmetic claim. Same caveat as Passes 207 and 284."
        ),
        "why_formalisable": (
            "After 261/265/270/275/281/287 the entire even-q law is arithmetic "
            "about a 2x2 integer matrix -- no geometry, no F2 rank, no incidence "
            "structure. Even the refutation is one line. That is Mathlib-sized."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
