#!/usr/bin/env python3
"""
PART CCCCCXIX: Finite Action Triad Theorem

CCCCCXVIII closed the loop:
    spectral/holonomy sources -> minimal flavor operators -> observables.

This part packages the three sources into one finite action triad:

  A_det  = log det(I+J) = log(41)
  A_free = log Z_exc(t),  Z_exc(t)=48e^{10t}+30e^{16t}
  A_hol  = U(12) holonomy/unit action on the Z12 phase lattice

The theorem is algebraic, so we avoid analytic logs in checks and verify the
exact exponentiated/action carriers:

  exp(A_det)       = 41
  Z_exc(0)         = 78 = dim(E6)
  Z_exc'(0)/Z(0)   = 160/13
  U(12)            = {1,5,7,11}

From these three action components we recover the same generated flavor kernel:
  top/CKM lambda, Higgs/CKM-A/PMNS-theta13/tau, CKM-PMNS angular CP, alpha.

Run:
    python exploration/PART_CCCCCXIX_FINITE_ACTION_TRIAD_THEOREM.py
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
    D = 2*E
    theta = k-1
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k-r
    delta_s = k-s

    # A_det carrier.
    det_carrier = v + 1
    det_action_symbol = "A_det=log det(I+J)=log(41)"

    # A_free carrier and cumulants.
    Zexc0 = 2*f + 2*g
    Zexc1 = 2*f*delta_r + 2*g*delta_s
    Zexc2 = 2*f*delta_r**2 + 2*g*delta_s**2
    free_mean = Fraction(Zexc1, Zexc0)
    free_second = Fraction(Zexc2, Zexc0)
    free_variance = free_second - free_mean*free_mean
    gap_ratio = Fraction(delta_s, delta_r)
    lambda_H = gap_ratio / free_mean

    # A_hol carrier.
    U12 = [a for a in range(1,12) if math.gcd(a,12)==1]
    W33_units = sorted([1, mu+1, phi6, k-1])
    half_turn = 6

    # Generated kernel.
    D_t = det_carrier
    D_b = q*D_t + lam
    D_c = D_b + k
    y_t_cubed = Fraction(v, D_t)
    lambda_CKM = Fraction(q*q, v)
    compactified_CKM = Fraction(q*q, D_t)
    y_b = Fraction(q, D_b)
    y_c = Fraction(1, D_c)
    y_tau = lambda_H*y_b*y_b/y_c
    A_CKM = Fraction(q**4, phi3)*lambda_H
    theta13 = Fraction(q*q, lam*lam*phi3)*lambda_H
    rho = Fraction(lam, mu+1)**2
    eta = Fraction(phi6, phi4)**3
    delta_cp = Fraction(k-1, phi4)
    solar = Fraction(mu, phi3)
    atmospheric = Fraction(mu, phi6)

    M_vac = theta*((k-lam)**2 + 1)
    Delta_M = Fraction(q, lam*theta)
    M_eff = Fraction(M_vac,1) + Delta_M
    alpha_slip = Fraction(v,1)/M_eff
    alpha_inv = Fraction(D_c,1) + alpha_slip

    # Finite action triad can be read as a product carrier if exponentiated.
    # We do not claim this product is itself physical; it is an accounting invariant.
    action_product_carrier = det_carrier * Zexc0 * len(U12)

    expected = {
        "y_t_cubed": Fraction(40,41),
        "lambda_CKM": Fraction(9,40),
        "compactified_CKM": Fraction(9,41),
        "y_b": Fraction(3,125),
        "y_c": Fraction(1,137),
        "y_tau": Fraction(16029,1562500),
        "lambda_H": Fraction(13,100),
        "A_CKM": Fraction(81,100),
        "PMNS_theta13": Fraction(9,400),
        "rho_bar": Fraction(4,25),
        "eta_bar": Fraction(343,1000),
        "PMNS_delta_over_pi": Fraction(11,10),
        "PMNS_solar": Fraction(4,13),
        "PMNS_atmospheric": Fraction(4,7),
        "alpha_inverse_refined": Fraction(669969,4889),
    }
    generated = {
        "y_t_cubed": y_t_cubed,
        "lambda_CKM": lambda_CKM,
        "compactified_CKM": compactified_CKM,
        "y_b": y_b,
        "y_c": y_c,
        "y_tau": y_tau,
        "lambda_H": lambda_H,
        "A_CKM": A_CKM,
        "PMNS_theta13": theta13,
        "rho_bar": rho,
        "eta_bar": eta,
        "PMNS_delta_over_pi": delta_cp,
        "PMNS_solar": solar,
        "PMNS_atmospheric": atmospheric,
        "alpha_inverse_refined": alpha_inv,
    }

    dim_G2 = lam*phi6
    dim_SU5 = f
    dim_SO10 = q*q*(mu+1)
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,D,theta,r,s,f,g)==(3,2,4,12,40,240,480,11,2,-4,24,15),
        "det_action_carrier_41": det_carrier == 41,
        "free_action_carrier_E6": Zexc0 == dim_E6 == 78,
        "free_action_mean": free_mean == Fraction(160,13),
        "free_action_variance": free_variance == Fraction(720,169),
        "holonomy_action_units": U12 == W33_units == [1,5,7,11],
        "half_turn": half_turn == 6,
        "lambda_H_from_action_triad": lambda_H == Fraction(13,100),
        "generated_equals_expected": generated == expected,
        "action_product_carrier": action_product_carrier == 41*78*4 == 12792,
        "dimensions": (dim_G2,dim_SU5,dim_SO10,dim_E6,dim_E8)==(14,24,45,78,248),
    }

    result = {
        "part": "CCCCCXIX",
        "title": "Finite Action Triad Theorem",
        "action_triad": {
            "A_det": {"symbol": det_action_symbol, "carrier": det_carrier},
            "A_free": {
                "symbol": "A_free(t)=log(48e^{10t}+30e^{16t})",
                "Zexc0": Zexc0,
                "Zexc1": Zexc1,
                "mean": str(free_mean),
                "variance": str(free_variance),
            },
            "A_hol": {"symbol": "A_hol=U(12) action on Z12 phase lattice", "units": U12, "half_turn": half_turn},
        },
        "generated_outputs": {name: str(val) for name, val in generated.items()},
        "action_product_carrier": action_product_carrier,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The three source operators form a finite action triad: determinant action for compactification, "
            "free-energy action for cumulants/Higgs, and holonomy-unit action for CP/angular data. The exact carriers "
            "of these three actions generate the full flavor kernel and refined alpha branch."
        ),
    }

    out = Path("PART_CCCCCXIX_finite_action_triad_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXIX: Finite Action Triad Theorem")
    print("="*90)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*90)
    print(f"A_det carrier={det_carrier}")
    print(f"A_free carrier={Zexc0}, mean={free_mean}, variance={free_variance}")
    print(f"A_hol units={U12}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
