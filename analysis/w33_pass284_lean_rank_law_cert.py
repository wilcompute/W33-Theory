#!/usr/bin/env python3
"""Pass 284: certify the Lean formalization of the even-q rank law.

The even-q law is now a statement about a 2x2 integer matrix and needs no
geometry, which makes it the first piece of this program small enough to
formalize. `formal/W33/RankLaw.lean` states:
  * the sequence a with a 1 = 10, a 2 = 50, a (t+1) = 9 a t - 16 a (t-1) + 8;
  * its anchors 298, 1890, 12250 (by decide);
  * the Cayley-Hamilton shift lemma (by ring) that FORCES the inhomogeneous
    constant c*(1 - Tr + det), hence 8 when c = 1;
  * det forced from the first two ranks, and the discriminant 17.

There is no Lean toolchain in this container, so -- exactly as in Pass 207 --
this witness certifies the file STRUCTURALLY (it parses as expected, states what
it claims, contains no `sorry`) and re-verifies every arithmetic claim
independently in Python. It is NOT a kernel check, and says so.
"""
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "W33" / "RankLaw.lean"
OUT = ROOT / "data" / "w33_pass284_lean_rank_law_cert.json"

def main():
    checks = {}
    src = LEAN.read_text(encoding="utf-8")
    body = re.sub(r"/-.*?-/", "", src, flags=re.S)      # strip block comments
    checks["file_exists"] = LEAN.exists()
    checks["no_sorry"] = "sorry" not in body
    checks["imports_mathlib"] = "import Mathlib" in src
    checks["declares_namespace"] = "namespace W33.RankLaw" in src
    for name in ("a_one", "a_two", "a_three", "a_four", "a_five",
                 "shifted_recurrence", "constant_is_eight",
                 "trace_from_doily_rank", "det_forced",
                 "discriminant_seventeen"):
        checks[f"states_{name}"] = f"theorem {name}" in body
    checks["in_root_import"] = "RankLaw" in (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8")

    # independently re-verify every arithmetic claim
    a = {1: 10, 2: 50}
    for t in range(3, 6):
        a[t] = 9 * a[t - 1] - 16 * a[t - 2] + 8
    checks["python_a3_298"] = a[3] == 298
    checks["python_a4_1890"] = a[4] == 1890
    checks["python_a5_12250"] = a[5] == 12250
    # the shift lemma, symbolically
    import sympy as sp
    p, q_, c, T, Tm = sp.symbols("p q c T Tm")
    lhs = (p * T - q_ * Tm) + c
    rhs = p * (T + c) - q_ * (Tm + c) + c * (1 - p + q_)
    checks["shift_lemma_is_an_identity"] = sp.simplify(lhs - rhs) == 0
    checks["python_constant_is_8"] = 1 * (1 - 9 + 16) == 8
    checks["python_det_forced_16"] = (9 ** 2 - 49) // 2 == 16
    checks["python_disc_17"] = 9 ** 2 - 4 * 16 == 17

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass284.lean_rank_law_cert.v1",
        "status": "PASS" if all_pass else "FAIL",
        "file": str(LEAN.relative_to(ROOT)),
        "formalized": [
            "the sequence a: a 1 = 10, a 2 = 50, a(t+1) = 9 a t - 16 a(t-1) + 8",
            "anchors a 3 = 298, a 4 = 1890, a 5 = 12250 (by decide)",
            "shifted_recurrence: the Cayley-Hamilton identity (by ring) forcing "
            "the inhomogeneous constant c*(1 - Tr + det)",
            "constant_is_eight: c=1, Tr=9, det=16 => the constant is exactly 8",
            "trace_from_doily_rank, det_forced, discriminant_seventeen",
        ],
        "honest_scope": (
            "NOT kernel-checked: there is no Lean toolchain in this container, so "
            "this is a STRUCTURAL certification (parses as expected, states the "
            "claimed theorems, contains no sorry) plus an INDEPENDENT Python "
            "re-verification of every arithmetic claim. A real `lake build` is "
            "still required before calling any of it machine-checked -- the same "
            "caveat carried by formal/W33/ShadowDichotomy.lean since Pass 207."
        ),
        "why_this_is_formalizable": (
            "After Passes 256/261/265/270/275 the even-q law is a statement about "
            "a 2x2 integer matrix -- no geometry, no F2 rank, no incidence "
            "structure. That is Mathlib-sized, which is why this is the first "
            "part of the rank story to reach Lean."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
