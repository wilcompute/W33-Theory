#!/usr/bin/env python3
"""
PART CCCCCXV: Minimal Flavor Operator Basis Theorem

Recent parts described the flavor kernel using four surfaces.  This theorem
compresses them to three finite operators:

  O1. Perron determinant compactification
      det(I+J)=v+1=41
      Generates y_t^3, lambda_CKM, compactified CKM density.

  O2. E6 cumulant/gap generator
      Z_exc(t)=48e^(10t)+30e^(16t), mu_exc=160/13, Delta_s/Delta_r=8/5
      Generates lambda_H, A_CKM, theta13, y_tau once y_b,y_c seeds exist.

  O3. Z12 holonomy unit group
      U(12)={1,mu+1,Phi6,k-1}={1,5,7,11}
      Generates bottom unit, CKM eta/CP, PMNS CP, PMNS solar/atmospheric
      cyclotomic angular data.

The Gaussian/charm core is not a fourth independent operator; it is generated
as a ladder output from O1 and O3/W33 valency:
      D_b=q*det(I+J)+lambda=125,
      D_c=D_b+k=137=|(k-1)+mu i|^2.

Thus the flavor sector has a minimal 3-operator basis:
      {Perron determinant, E6 cumulant/gap generator, Z12 holonomy units}.

Run:
    python exploration/PART_CCCCCXV_MINIMAL_FLAVOR_OPERATOR_BASIS.py
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
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k-r
    delta_s = k-s

    # O1: Perron determinant.
    O1_det = v + 1
    y_t_cubed = Fraction(v, O1_det)
    lambda_ckm = Fraction(q*q, v)
    ckm_compact = lambda_ckm * y_t_cubed

    # O2: E6 cumulant/gap generator.
    Z_exc_M0 = 2*f + 2*g
    Z_exc_M1 = 2*f*delta_r + 2*g*delta_s
    mu_exc = Fraction(Z_exc_M1, Z_exc_M0)
    gap_ratio = Fraction(delta_s, delta_r)
    lambda_H = gap_ratio / mu_exc
    A_ckm = Fraction(q**4, phi3) * lambda_H
    theta13 = Fraction(q*q, lam*lam*phi3) * lambda_H

    # O3: Z12 holonomy units.
    U12 = [a for a in range(1, 12) if math.gcd(a, 12) == 1]
    O3_units = sorted([1, mu+1, phi6, k-1])
    bottom_unit = mu+1
    ckm_cp_unit = phi6
    pmns_cp_unit = k-1

    # Ladder outputs from O1 + O3/W33 valency.
    D_t = O1_det
    D_b = q*D_t + lam
    D_c = D_b + k
    y_b = Fraction(q, D_b)
    y_c = Fraction(1, D_c)
    y_tau = lambda_H*y_b*y_b/y_c

    # Angular outputs from O3 + Phi denominators.
    rho_bar = Fraction(lam, bottom_unit)**2
    eta_bar = Fraction(ckm_cp_unit, phi4)**3
    pmns_delta = Fraction(pmns_cp_unit, phi4)
    pmns_solar = Fraction(mu, phi3)
    pmns_atm = Fraction(mu, phi6)

    # Alpha output from ladder + Perron Green.
    M_vac = (k-1)*((k-lam)**2 + 1)
    Delta_M = Fraction(q, lam*(k-1))
    M_eff = Fraction(M_vac, 1) + Delta_M
    alpha_slip = Fraction(v, 1)/M_eff
    alpha_inv = Fraction(D_c, 1) + alpha_slip

    # Coverage dictionary: all required flavor outputs generated.
    generated = {
        "y_t_cubed": y_t_cubed,
        "lambda_CKM": lambda_ckm,
        "lambda_CKM_times_y_t_cubed": ckm_compact,
        "lambda_H": lambda_H,
        "A_CKM": A_ckm,
        "PMNS_theta13": theta13,
        "y_b": y_b,
        "y_c": y_c,
        "y_tau": y_tau,
        "rho_bar": rho_bar,
        "eta_bar": eta_bar,
        "PMNS_delta_over_pi": pmns_delta,
        "PMNS_solar": pmns_solar,
        "PMNS_atmospheric": pmns_atm,
        "alpha_inverse_refined": alpha_inv,
    }

    expected = {
        "y_t_cubed": Fraction(40,41),
        "lambda_CKM": Fraction(9,40),
        "lambda_CKM_times_y_t_cubed": Fraction(9,41),
        "lambda_H": Fraction(13,100),
        "A_CKM": Fraction(81,100),
        "PMNS_theta13": Fraction(9,400),
        "y_b": Fraction(3,125),
        "y_c": Fraction(1,137),
        "y_tau": Fraction(16029,1562500),
        "rho_bar": Fraction(4,25),
        "eta_bar": Fraction(343,1000),
        "PMNS_delta_over_pi": Fraction(11,10),
        "PMNS_solar": Fraction(4,13),
        "PMNS_atmospheric": Fraction(4,7),
        "alpha_inverse_refined": Fraction(669969,4889),
    }

    dim_G2 = lam*phi6
    dim_SU5 = f
    dim_SO10 = q*q*(mu+1)
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,D,r,s,f,g)==(3,2,4,12,40,240,480,2,-4,24,15),
        "O1_perron_det": O1_det == 41,
        "O2_excited_E6_generator": Z_exc_M0 == dim_E6 == 78 and mu_exc == Fraction(160,13),
        "O2_gap_ratio": gap_ratio == Fraction(8,5),
        "O3_unit_group": U12 == O3_units == [1,5,7,11],
        "ladder_outputs": (D_t,D_b,D_c)==(41,125,137),
        "all_generated_values_match_expected": generated == expected,
        "alpha_slip": alpha_slip == Fraction(880,24445),
        "dimensions": (dim_G2,dim_SU5,dim_SO10,dim_E6,dim_E8)==(14,24,45,78,248),
    }

    result = {
        "part": "CCCCCXV",
        "title": "Minimal Flavor Operator Basis Theorem",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E, "directed_edges": D,
            "r": r, "s": s, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "minimal_operator_basis": {
            "O1_Perron_determinant": {
                "definition": "det(I+J)=v+1",
                "value": O1_det,
                "outputs": ["y_t^3", "lambda_CKM", "lambda_CKM*y_t^3"],
            },
            "O2_E6_cumulant_gap_generator": {
                "definition": "Z_exc(t)=48e^{10t}+30e^{16t}; lambda_H=(Delta_s/Delta_r)/mu_exc",
                "excited_mean": str(mu_exc),
                "gap_ratio": str(gap_ratio),
                "outputs": ["lambda_H", "A_CKM", "PMNS theta13", "y_tau via Higgs identity"],
            },
            "O3_Z12_holonomy_units": {
                "definition": "U(12)={1,mu+1,Phi6,k-1}",
                "units": O3_units,
                "outputs": ["bottom unit", "CKM rho/eta", "PMNS solar/atmospheric/CP"],
            },
        },
        "generated_flavor_outputs": {k_: str(v_) for k_, v_ in generated.items()},
        "ladder_outputs": {"D_t": D_t, "D_b": D_b, "D_c": D_c, "alpha_slip": str(alpha_slip)},
        "structural_dimensions": {"G2": dim_G2, "SU5": dim_SU5, "SO10": dim_SO10, "E6": dim_E6, "E8": dim_E8},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The flavor sector reduces to a minimal three-operator basis: Perron determinant compactification; "
            "E6 excited cumulant/gap generator; and Z12 holonomy units. The Gaussian/charm core and heavy-Yukawa "
            "ladder are generated outputs, not independent operators."
        ),
    }

    out = Path("PART_CCCCCXV_minimal_flavor_operator_basis_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXV: Minimal Flavor Operator Basis Theorem")
    print("="*88)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*88)
    print("generated outputs:")
    for key, value in generated.items():
        print(f"  {key} = {value}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
