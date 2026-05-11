#!/usr/bin/env python3
"""
PART CCCCCXII: Unified Flavor Kernel Theorem

This theorem consolidates the recent channel/cumulant work into one flavor
architecture.  The point is not to add a new empirical closure; it is to sort
existing CKM, PMNS, Higgs, alpha/charm, and heavy-Yukawa formulas by the exact
W(3,3) operation that generates them.

Kernel operations:
  1. Perron determinant / compactification
       det(I+J)=v+1=41
       y_t^3=v/(v+1), lambda_CKM=q^2/v, lambda_CKM*y_t^3=q^2/(v+1)

  2. q-dressed Perron + valency/Gaussian core ladder
       D_b=q(v+1)+lambda=125, D_c=D_b+k=137
       y_b=q/D_b, y_c=1/D_c, alpha_core=D_c

  3. E6 excited cumulant + restricted gap ratio
       mu_exc=160/13, Delta_s/Delta_r=8/5
       lambda_H=(Delta_s/Delta_r)/mu_exc=13/100
       A_CKM=(q^4/Phi3)lambda_H, theta13=(q^2/(lambda^2 Phi3))lambda_H
       y_tau=lambda_H*y_b^2/y_c

  4. Cyclotomic angular surface
       PMNS solar=mu/Phi3, PMNS atmospheric=mu/Phi6,
       PMNS CP/pi=(k-1)/Phi4, CKM eta=(Phi6/Phi4)^3,
       CKM rho=(lambda/(mu+1))^2.

Run:
    python exploration/PART_CCCCCXII_UNIFIED_FLAVOR_KERNEL_THEOREM.py
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
    directed_edges = 2*E
    r = lam
    s = -mu
    f = 24
    g = 15
    phi3 = q*q + q + 1
    phi4 = q*q + 1
    phi6 = q*q - q + 1
    delta_r = k-r
    delta_s = k-s

    # 1. Perron determinant / compactification.
    det_I_plus_J = v + 1
    y_t_cubed = Fraction(v, det_I_plus_J)
    lambda_ckm = Fraction(q*q, v)
    compactified_ckm_density = lambda_ckm * y_t_cubed

    # 2. Heavy Yukawa ladder / Gaussian core.
    D_t = det_I_plus_J
    D_b = q*D_t + lam
    D_c = D_b + k
    D_c_gaussian = (k-1)**2 + mu**2
    D_c_cyclotomic = phi3*phi4 + phi6
    y_b = Fraction(q, D_b)
    y_c = Fraction(1, D_c)

    # 3. Cumulant/gap Higgs surface.
    excited_total = 2*f + 2*g
    excited_first_moment = 2*f*delta_r + 2*g*delta_s
    excited_mean = Fraction(excited_first_moment, excited_total)
    gap_ratio = Fraction(delta_s, delta_r)
    lambda_H = gap_ratio / excited_mean
    A_ckm = Fraction(q**4, phi3) * lambda_H
    theta13_pmns = Fraction(q*q, lam*lam*phi3) * lambda_H
    y_tau = lambda_H * y_b*y_b / y_c
    yukawa_higgs_ratio = y_tau*y_c/(y_b*y_b)

    # 4. Cyclotomic/angular surface.
    pmns_solar = Fraction(mu, phi3)
    pmns_atmospheric = Fraction(mu, phi6)
    pmns_cp_over_pi = Fraction(k-1, phi4)
    ckm_eta = Fraction(phi6, phi4)**3
    ckm_rho = Fraction(lam, mu+1)**2

    # CKM A/lambda etc.
    ckm_A_over_lambdaH = A_ckm / lambda_H
    pmns_solar_over_atm = pmns_solar / pmns_atmospheric

    # Alpha core and slip from Perron Green residue for inclusion.
    alpha_core = D_c
    M_vac = (k-1)*((k-lam)**2 + 1)
    Delta_M = Fraction(q, lam*(k-1))
    M_eff = Fraction(M_vac, 1) + Delta_M
    alpha_slip = Fraction(v, 1)/M_eff
    alpha_inv = Fraction(alpha_core, 1) + alpha_slip

    # Structural dimensions.
    dim_G2 = lam*phi6
    dim_SU5 = f
    dim_SO10 = q*q*(mu+1)
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q,lam,mu,k,v,E,directed_edges,r,s,f,g)==(3,2,4,12,40,240,480,2,-4,24,15),
        "perron_det_41": det_I_plus_J == 41,
        "top_cube_40_over_41": y_t_cubed == Fraction(40,41),
        "lambda_ckm_9_over_40": lambda_ckm == Fraction(9,40),
        "compactified_ckm_density_9_over_41": compactified_ckm_density == Fraction(9,41),
        "bottom_ladder_denominator_125": D_b == 125 == (mu+1)**3,
        "charm_ladder_denominator_137": D_c == 137 == D_c_gaussian == D_c_cyclotomic,
        "yb_yc": (y_b, y_c) == (Fraction(3,125), Fraction(1,137)),
        "excited_E6_mean": excited_total == dim_E6 == 78 and excited_mean == Fraction(160,13),
        "gap_ratio": gap_ratio == Fraction(8,5),
        "lambda_H_13_over_100": lambda_H == Fraction(13,100),
        "A_CKM_81_over_100": A_ckm == Fraction(81,100),
        "PMNS_theta13_9_over_400": theta13_pmns == Fraction(9,400),
        "y_tau_forced": y_tau == Fraction(16029,1562500),
        "yukawa_higgs_ratio": yukawa_higgs_ratio == lambda_H,
        "pmns_solar_4_over_13": pmns_solar == Fraction(4,13),
        "pmns_atmospheric_4_over_7": pmns_atmospheric == Fraction(4,7),
        "pmns_cp_11_over_10": pmns_cp_over_pi == Fraction(11,10),
        "ckm_eta_343_over_1000": ckm_eta == Fraction(343,1000),
        "ckm_rho_4_over_25": ckm_rho == Fraction(4,25),
        "A_over_lambdaH_81_over_13": ckm_A_over_lambdaH == Fraction(81,13),
        "pmns_solar_atm_ratio_7_over_13": pmns_solar_over_atm == Fraction(7,13),
        "alpha_core_and_refined": alpha_core == 137 and alpha_inv == Fraction(669969,4889),
        "structural_dimensions": (dim_G2,dim_SU5,dim_SO10,dim_E6,dim_E8)==(14,24,45,78,248),
    }

    result = {
        "part": "CCCCCXII",
        "title": "Unified Flavor Kernel Theorem",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E, "directed_edges": directed_edges,
            "r": r, "s": s, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "kernel_operations": {
            "perron_determinant_compactification": {
                "det_I_plus_J": det_I_plus_J,
                "y_t_cubed": str(y_t_cubed),
                "lambda_CKM": str(lambda_ckm),
                "lambda_CKM_times_y_t_cubed": str(compactified_ckm_density),
            },
            "heavy_yukawa_gaussian_ladder": {
                "D_t": D_t,
                "D_b": D_b,
                "D_c": D_c,
                "y_b": str(y_b),
                "y_c": str(y_c),
                "alpha_core": alpha_core,
                "alpha_inverse_refined": str(alpha_inv),
            },
            "cumulant_gap_higgs_surface": {
                "excited_mean": str(excited_mean),
                "gap_ratio": str(gap_ratio),
                "lambda_H": str(lambda_H),
                "A_CKM": str(A_ckm),
                "PMNS_theta13": str(theta13_pmns),
                "y_tau": str(y_tau),
            },
            "cyclotomic_angular_surface": {
                "PMNS_solar": str(pmns_solar),
                "PMNS_atmospheric": str(pmns_atmospheric),
                "PMNS_CP_over_pi": str(pmns_cp_over_pi),
                "CKM_eta": str(ckm_eta),
                "CKM_rho": str(ckm_rho),
            },
        },
        "cross_identities": {
            "A_CKM_over_lambda_H": str(ckm_A_over_lambdaH),
            "PMNS_solar_over_atmospheric": str(pmns_solar_over_atm),
            "y_tau_yc_over_yb_squared": str(yukawa_higgs_ratio),
            "alpha_slip": str(alpha_slip),
        },
        "structural_dimensions": {"G2": dim_G2, "SU5": dim_SU5, "SO10": dim_SO10, "E6": dim_E6, "E8": dim_E8},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The flavor sector is organized by four W(3,3) operations: Perron determinant compactification; "
            "q-dressed/Gaussian heavy-Yukawa ladder; E6 excited cumulant plus restricted gap ratio; and the "
            "cyclotomic angular surface. CKM, PMNS, Higgs, alpha/charm, and third-generation Yukawas are therefore "
            "not separate tables but projections of one finite flavor kernel."
        ),
    }

    out = Path("PART_CCCCCXII_unified_flavor_kernel_theorem_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCXII: Unified Flavor Kernel Theorem")
    print("="*88)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*88)
    print(f"lambda_H={lambda_H}, A={A_ckm}, theta13={theta13_pmns}")
    print(f"CKM lambda={lambda_ckm}, top^3={y_t_cubed}, product={compactified_ckm_density}")
    print(f"PMNS solar={pmns_solar}, atmospheric={pmns_atmospheric}, CP/pi={pmns_cp_over_pi}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
