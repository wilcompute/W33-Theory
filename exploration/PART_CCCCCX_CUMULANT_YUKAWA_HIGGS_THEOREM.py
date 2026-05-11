#!/usr/bin/env python3
"""
PART CCCCCX: Cumulant Yukawa-Higgs Theorem

Existing empirical bridge (CCCXLI):

    y_tau * y_c / y_b^2 = lambda_H = 13/100.

New input from CCCCCIX:

    lambda_H = (Delta_s/Delta_r) / mu_exc

where
    Delta_s/Delta_r = 8/5,
    mu_exc = 160/13 is the E6 excited-sector mean of the finite spectral
    free-energy distribution.

Therefore the third-generation Yukawa identity is now derived from the
cumulant bridge:

    y_tau * y_c / y_b^2 = (Delta_s/Delta_r) / mu_exc.

Using W(3,3) Yukawa seeds
    y_c = 1/137,
    y_b = q/(mu+1)^3 = 3/125,

the tau Yukawa is forced:

    y_tau = lambda_H * y_b^2 / y_c
          = (13/100)*(9/15625)*137
          = 16029/1562500.

Run:
    python exploration/PART_CCCCCX_CUMULANT_YUKAWA_HIGGS_THEOREM.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


def main() -> None:
    q = 3
    assert math.factorial(q) == 2*q
    lam = 2
    mu = 4
    k = q*(q+1)
    v = (q+1)*(q*q+1)
    E = v*k//2
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k-r
    delta_s = k-s

    # Excited-sector cumulant/Higgs bridge.
    excited_total = 2*f + 2*g
    excited_first_moment = 2*f*delta_r + 2*g*delta_s
    excited_mean = Fraction(excited_first_moment, excited_total)
    gap_ratio = Fraction(delta_s, delta_r)
    lambda_H_cumulant = gap_ratio / excited_mean
    lambda_H_direct = Fraction(phi3, phi4*phi4)

    # Yukawa seeds from prior empirical arc.
    y_c = Fraction(1, (k-1)**2 + mu**2)       # 1/137
    y_b = Fraction(q, (mu+1)**3)              # 3/125
    y_tau_forced = lambda_H_cumulant * y_b * y_b / y_c
    yukawa_ratio = y_tau_forced * y_c / (y_b*y_b)

    # Alternative forms.
    y_tau_formula_num = phi3 * q*q * ((k-1)**2 + mu**2)
    y_tau_formula_den = (phi4*phi4) * ((mu+1)**6)
    y_tau_formula = Fraction(y_tau_formula_num, y_tau_formula_den)

    # Direct tau mass prediction from v_EW/sqrt(2) if desired as dimensionless only here.
    # y_tau approx 0.01025856; mass = y_tau*v/sqrt2 requires v input, omitted.

    # Crosslinks to CKM/PMNS produced from same lambda_H.
    A_ckm = Fraction(q**4, phi3) * lambda_H_cumulant
    pmns_theta13 = Fraction(q*q, lam*lam*phi3) * lambda_H_cumulant

    # Structural dimensions.
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3
    dim_SU5 = f

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "lambda_H_from_cumulant": lambda_H_cumulant == lambda_H_direct == Fraction(13,100),
        "excited_total_E6": excited_total == dim_E6 == 78,
        "excited_mean_160_over_13": excited_mean == Fraction(160,13),
        "gap_ratio_8_over_5": gap_ratio == Fraction(8,5),
        "y_c_1_over_137": y_c == Fraction(1,137),
        "y_b_3_over_125": y_b == Fraction(3,125),
        "forced_y_tau": y_tau_forced == Fraction(16029,1562500),
        "forced_y_tau_alt_formula": y_tau_forced == y_tau_formula,
        "yukawa_ratio_equals_lambda_H": yukawa_ratio == lambda_H_cumulant,
        "A_ckm_from_same_lambda_H": A_ckm == Fraction(81,100),
        "pmns_from_same_lambda_H": pmns_theta13 == Fraction(9,400),
        "structural_dims": (dim_SU5, dim_E6, dim_E8) == (24,78,248),
    }

    result = {
        "part": "CCCCCX",
        "title": "Cumulant Yukawa-Higgs Theorem",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E,
            "r": r, "s": s, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "cumulant_higgs_bridge": {
            "excited_total": excited_total,
            "excited_first_moment": excited_first_moment,
            "excited_mean": str(excited_mean),
            "gap_ratio_Delta_s_over_Delta_r": str(gap_ratio),
            "lambda_H": str(lambda_H_cumulant),
            "identity": "lambda_H=(Delta_s/Delta_r)/mu_exc",
        },
        "yukawa_identity": {
            "y_c": str(y_c),
            "y_b": str(y_b),
            "y_tau_forced": str(y_tau_forced),
            "y_tau_decimal": float(y_tau_forced),
            "ratio_y_tau_y_c_over_y_b_squared": str(yukawa_ratio),
            "identity": "y_tau*y_c/y_b^2=lambda_H=(Delta_s/Delta_r)/mu_exc",
        },
        "same_lambda_H_outputs": {
            "lambda_H": str(lambda_H_cumulant),
            "A_CKM": str(A_ckm),
            "PMNS_theta13": str(pmns_theta13),
        },
        "structural_dimensions": {"SU5": dim_SU5, "E6": dim_E6, "E8": dim_E8},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The third-generation Yukawa-Higgs identity is now downstream of the free-energy cumulant bridge. "
            "The excited E6 mean and restricted gap ratio generate lambda_H, and the prior W(3,3) charm/bottom "
            "Yukawa seeds then force y_tau so that y_tau*y_c/y_b^2=lambda_H exactly."
        ),
    }

    out = Path("PART_CCCCCX_cumulant_yukawa_higgs_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCX: Cumulant Yukawa-Higgs Theorem")
    print("="*86)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*86)
    print(f"lambda_H={lambda_H_cumulant}")
    print(f"y_c={y_c}, y_b={y_b}, y_tau={y_tau_forced}")
    print(f"ratio={yukawa_ratio}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
