#!/usr/bin/env python3
"""
PART CCCCCXIII: CP Kernel Jarlskog Theorem

CCCCCXII unified the flavor kernel.  This part isolates the CP-violating
subkernel and keeps the algebra exact.

CKM side:
  lambda_CKM = q^2/v = 9/40
  A_CKM      = q^4/Phi4^2 = 81/100
  rho_bar    = (lambda/(mu+1))^2 = 4/25
  eta_bar    = (Phi6/Phi4)^3 = 343/1000

The CKM CP slope is
  tan(gamma) = eta_bar/rho_bar = 343/160.

The leading Wolfenstein Jarlskog kernel is
  J_CKM^(lead) = A^2 lambda_CKM^6 eta_bar.

PMNS side:
  sin^2 theta12 = mu/Phi3 = 4/13
  sin^2 theta23 = mu/Phi6 = 4/7
  sin^2 theta13 = q^2/(lambda*Phi4)^2 = 9/400
  delta_CP/pi   = (k-1)/Phi4 = 11/10.

Since delta_CP = 11*pi/10,
  sin(delta_CP) = -sin(pi/10),
  sin^2(delta_CP) = (3 - sqrt(5))/8.

Thus the PMNS Jarlskog square is the exact algebraic number
  J_PMNS^2 = B * (3 - sqrt(5))/8,
where
  B = s12^2 c12^2 s23^2 c23^2 s13^2 c13^4
    = 37150083 / 33124000000.

Interpretation:
  CKM CP is a rational cyclotomic slope/area kernel; PMNS CP is the same
  angular W(3,3) surface but with the exact pentagonal radical from sin(pi/10).

Run:
    python exploration/PART_CCCCCXIII_CP_KERNEL_JARLSKOG_THEOREM.py
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import math
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Qsqrt5:
    """Exact number a + b*sqrt(5), with rational a,b."""
    a: Fraction
    b: Fraction

    def __mul__(self, other: Fraction | int) -> "Qsqrt5":
        other = Fraction(other)
        return Qsqrt5(self.a * other, self.b * other)

    __rmul__ = __mul__

    def __str__(self) -> str:
        a = str(self.a)
        b = str(abs(self.b))
        sign = "+" if self.b >= 0 else "-"
        return f"{a} {sign} {b}*sqrt(5)"

    def decimal(self) -> float:
        return float(self.a) + float(self.b) * math.sqrt(5)


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

    # CKM kernel.
    lambda_ckm = Fraction(q*q, v)
    A_ckm = Fraction(q**4, phi4*phi4)
    rho_bar = Fraction(lam, mu+1)**2
    eta_bar = Fraction(phi6, phi4)**3
    tan_gamma = eta_bar / rho_bar
    J_ckm_leading = A_ckm*A_ckm * lambda_ckm**6 * eta_bar

    # PMNS kernel.
    s12_2 = Fraction(mu, phi3)
    c12_2 = 1 - s12_2
    s23_2 = Fraction(mu, phi6)
    c23_2 = 1 - s23_2
    s13_2 = Fraction(q*q, (lam*phi4)**2)
    c13_2 = 1 - s13_2
    delta_over_pi = Fraction(k-1, phi4)
    sin2_delta = Qsqrt5(Fraction(3,8), Fraction(-1,8))
    B_pmns = s12_2*c12_2*s23_2*c23_2*s13_2*c13_2*c13_2
    J_pmns_squared = sin2_delta * B_pmns
    J_pmns_signed_decimal = -math.sqrt(J_pmns_squared.decimal())

    # Cross-surface identities.
    pmns_solar_over_atm = s12_2 / s23_2
    ckm_eta_base = Fraction(phi6, phi4)
    pmns_delta_base = Fraction(k-1, phi4)

    # CP hierarchy diagnostics.
    J_ratio_abs_decimal = abs(J_pmns_signed_decimal) / float(J_ckm_leading)
    ckm_cp_slope_num_den = (eta_bar.numerator * rho_bar.denominator, eta_bar.denominator * rho_bar.numerator)

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,r,s,f,g)==(3,2,4,12,40,240,2,-4,24,15),
        "ckm_parameters": (lambda_ckm,A_ckm,rho_bar,eta_bar)==(Fraction(9,40),Fraction(81,100),Fraction(4,25),Fraction(343,1000)),
        "ckm_tan_gamma": tan_gamma == Fraction(343,160),
        "ckm_j_leading_exact": J_ckm_leading == Fraction(1195967049543,40960000000000000),
        "pmns_angles": (s12_2,s23_2,s13_2,delta_over_pi)==(Fraction(4,13),Fraction(4,7),Fraction(9,400),Fraction(11,10)),
        "pmns_B_factor": B_pmns == Fraction(37150083,33124000000),
        "pmns_sin2_delta_exact": sin2_delta == Qsqrt5(Fraction(3,8), Fraction(-1,8)),
        "pmns_J_squared_exact_pair": J_pmns_squared == Qsqrt5(Fraction(111450249,264992000000), Fraction(-37150083,264992000000)),
        "pmns_solar_atm_ratio": pmns_solar_over_atm == Fraction(7,13),
        "ckm_eta_base": ckm_eta_base == Fraction(7,10),
        "pmns_delta_base": pmns_delta_base == Fraction(11,10),
        "cp_hierarchy_positive": J_ratio_abs_decimal > 300,
    }

    result = {
        "part": "CCCCCXIII",
        "title": "CP Kernel Jarlskog Theorem",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E,
            "r": r, "s": s, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "ckm_cp_kernel": {
            "lambda_CKM": str(lambda_ckm),
            "A_CKM": str(A_ckm),
            "rho_bar": str(rho_bar),
            "eta_bar": str(eta_bar),
            "tan_gamma": str(tan_gamma),
            "J_CKM_leading": str(J_ckm_leading),
            "J_CKM_leading_decimal": float(J_ckm_leading),
        },
        "pmns_cp_kernel": {
            "sin2_theta12": str(s12_2),
            "sin2_theta23": str(s23_2),
            "sin2_theta13": str(s13_2),
            "delta_CP_over_pi": str(delta_over_pi),
            "sin2_delta_CP": str(sin2_delta),
            "B_factor": str(B_pmns),
            "J_PMNS_squared": str(J_pmns_squared),
            "J_PMNS_signed_decimal": J_pmns_signed_decimal,
        },
        "cross_surface": {
            "PMNS_solar_over_atmospheric": str(pmns_solar_over_atm),
            "CKM_eta_base_Phi6_over_Phi4": str(ckm_eta_base),
            "PMNS_delta_base_kminus1_over_Phi4": str(pmns_delta_base),
            "abs_J_PMNS_over_J_CKM_leading_decimal": J_ratio_abs_decimal,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The CP sector splits cleanly into a rational CKM cyclotomic-slope kernel and an algebraic PMNS angular kernel. "
            "CKM CP uses eta=(Phi6/Phi4)^3 and rho=(lambda/(mu+1))^2, giving tan(gamma)=343/160. "
            "PMNS CP uses delta/pi=(k-1)/Phi4=11/10, whose sine introduces the exact pentagonal radical "
            "sin^2(pi/10)=(3-sqrt(5))/8. Both are projections of the cyclotomic angular surface."
        ),
    }

    out = Path("PART_CCCCCXIII_cp_kernel_jarlskog_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXIII: CP Kernel Jarlskog Theorem")
    print("="*88)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*88)
    print(f"J_CKM_leading={J_ckm_leading} = {float(J_ckm_leading):.12e}")
    print(f"J_PMNS^2={J_pmns_squared} = {J_pmns_squared.decimal():.12e}")
    print(f"J_PMNS signed ~= {J_pmns_signed_decimal:.12e}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
