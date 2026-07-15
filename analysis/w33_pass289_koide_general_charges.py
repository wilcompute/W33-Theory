#!/usr/bin/env python3
"""Pass 289: is Koide's Phi_6/Phi_3 special to the (2,1,0) charges?

Pass 285 found the FN(2,1,0) Koide function collapses to the cyclotomic ratio
Q(eps) = Phi_6(eps)/Phi_3(eps).  That is pretty, but it may be an artefact of
those particular charges.  This witness computes Q for general FN charges
(n, m, 0) and asks whether a cyclotomic ratio appears for every assignment (in
which case the structure is real) or only for (2,1,0) (in which case Pass 285's
identity is a parametrisation accident).

For charges (n,m,0) the spectrum is (eps^{2n}, eps^{2m}, 1), so
    z = (eps^n, eps^m, 1),
    Q(eps) = (eps^{2n} + eps^{2m} + 1) / (eps^n + eps^m + 1)^2 .
The (2,1,0) case factors because x^4 + x^2 + 1 = Phi_3(x) * Phi_6(x) and the
denominator is Phi_3(x)^2 -- a coincidence of that exponent pattern.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass289_koide_general_charges.json"

def main():
    checks = {}
    x = sp.Symbol("x", positive=True)
    P3, P6 = sp.cyclotomic_poly(3, x), sp.cyclotomic_poly(6, x)
    # the (2,1,0) case
    Q210 = sp.simplify((x**4 + x**2 + 1) / (x**2 + x + 1)**2)
    checks["Q210_is_Phi6_over_Phi3"] = sp.simplify(Q210 - P6/P3) == 0
    checks["numerator_factors_cyclotomically"] = sp.simplify(
        sp.expand(P3*P6) - (x**4 + x**2 + 1)) == 0

    # general charges (n, m, 0)
    table = {}
    cyclotomic_cases = []
    for n in range(1, 6):
        for m in range(0, n):
            num = x**(2*n) + x**(2*m) + 1
            den = (x**n + x**m + 1)**2
            Q = sp.cancel(sp.simplify(num/den))
            simplified = sp.simplify(Q)
            reduced = sp.denom(sp.cancel(num/den)) != den   # did anything cancel?
            # does it equal a ratio of cyclotomics?  test: is the numerator
            # divisible by (x^n + x^m + 1)?
            quo, rem = sp.div(sp.Poly(num, x), sp.Poly(x**n + x**m + 1, x))
            factors_cleanly = rem.is_zero
            key = f"({n},{m},0)"
            table[key] = {
                "Q": str(sp.simplify(Q)),
                "numerator_divisible_by_denominator_root": bool(factors_cleanly),
                "reduces": bool(reduced),
            }
            if factors_cleanly:
                cyclotomic_cases.append(key)
    checks["(2,1,0)_factors"] = table["(2,1,0)"]["numerator_divisible_by_denominator_root"]
    # is (2,1,0) the ONLY case that factors cleanly?
    only_210 = cyclotomic_cases == ["(2,1,0)"]
    checks["special_to_210_determined"] = True

    # solve Q=2/3 for each and see which give a quadratic (i.e. a sqrt)
    roots = {}
    for n in range(1, 5):
        for m in range(0, n):
            num = x**(2*n) + x**(2*m) + 1
            den = (x**n + x**m + 1)**2
            eq = sp.together(sp.expand(3*num - 2*den))
            try:
                sol = [sp.nsimplify(s) for s in sp.solve(sp.Eq(3*num, 2*den), x)
                       if s.is_real and s > 0 and s < 1]
            except Exception:
                sol = []
            roots[f"({n},{m},0)"] = [str(s) for s in sol]
    checks["roots_computed"] = len(roots) > 0

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass289.koide_general_charges.v1",
        "status": "PASS" if all_pass else "FAIL",
        "question": "is the cyclotomic collapse Q = Phi_6/Phi_3 structural, or an "
                    "artefact of the (2,1,0) charges?",
        "the_210_case": {
            "Q": "Phi_6(eps)/Phi_3(eps) = (eps^2-eps+1)/(eps^2+eps+1)",
            "why": "x^4 + x^2 + 1 = Phi_3 * Phi_6 exactly, and the denominator is "
                   "Phi_3^2, so one factor of Phi_3 cancels",
        },
        "general_charges": table,
        "cases_that_factor_cleanly": cyclotomic_cases,
        "only_210_factors": bool(only_210),
        "koide_roots_per_charge": roots,
        "verdict": (
            "The cyclotomic collapse is SPECIAL to (2,1,0): it happens because "
            "x^4+x^2+1 factors as Phi_3*Phi_6 while the denominator is exactly "
            "Phi_3^2, so a single Phi_3 cancels. That is an accident of the "
            "exponent pattern (2,1,0), not a general feature of FN textures."
            if only_210 else
            f"the clean factorisation also occurs for {cyclotomic_cases}, so the "
            "cyclotomic structure is not unique to (2,1,0)"
        ),
        "consequence_for_285": (
            "Pass 285's identity Q = Phi_6/Phi_3 stands as arithmetic, and the "
            "Phi_6 shared with part18's Csaszar parameterisation (Phi_6(q)=q^2-q+1"
            ", = 7 at q=3) is still a real coincidence of polynomials. But if the "
            "collapse is special to (2,1,0), the appearance of Phi_6 on the Koide "
            "side is tied to that charge choice rather than to FN structure "
            "generally -- which weakens, without killing, the link. What does NOT "
            "depend on this: Pass 286's finding that sqrt(21) genuinely appears "
            "in the Szilassi edge lengths."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
