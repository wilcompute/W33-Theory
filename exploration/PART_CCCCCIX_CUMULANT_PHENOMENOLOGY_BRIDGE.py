#!/usr/bin/env python3
"""
PART CCCCCIX: Cumulant Phenomenology Bridge

CCCCCVIII turned the finite spectral action into a free-energy/cumulant kernel:

    Z(t)=82+320 e^{4t}+48 e^{10t}+30 e^{16t},   F(t)=log Z(t).

This part tests whether the cumulant invariants are merely internal statistics
or whether they reconstruct empirical closure surfaces.

Main findings:

1. Full mean is the G2 dimension per q:
       kappa_1 = 14/3 = dim(G2)/q = (lambda*Phi6)/q.

2. Full variance is the E8+SU5 dimension per q^2:
       kappa_2 = 272/9 = (dim(E8)+dim(SU5))/q^2.

3. Excited-sector mean reconstructs the Higgs quartic after correcting by the
   restricted gap ratio:
       mu_exc = 160/13,
       Delta_s/Delta_r = 8/5,
       (Delta_s/Delta_r)/mu_exc = 13/100 = lambda_H.

4. The same lambda_H then generates CKM A and PMNS theta13:
       A_CKM = (q^4/Phi3) lambda_H = 81/100,
       sin^2(theta13) = (q^2/(lambda^2 Phi3)) lambda_H = 9/400.

This shows the free-energy fluctuations are not decorative; they feed directly
into the scalar/flavor surface.

Run:
    python exploration/PART_CCCCCIX_CUMULANT_PHENOMENOLOGY_BRIDGE.py
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

    # Dirac/free-energy sectors.
    sectors = {
        "ground": (0, 2*q**4 + 1),
        "gauge": (mu, lam**3 * v),
        "r_gap": (delta_r, 2*f),
        "s_gap": (delta_s, 2*g),
    }
    total = sum(mult for _eig, mult in sectors.values())
    M1 = sum(mult*eig for eig, mult in sectors.values())
    M2 = sum(mult*eig*eig for eig, mult in sectors.values())
    mean = Fraction(M1, total)
    second = Fraction(M2, total)
    variance = second - mean*mean

    # Excited restricted sector.
    excited_total = sectors["r_gap"][1] + sectors["s_gap"][1]
    excited_M1 = sectors["r_gap"][0]*sectors["r_gap"][1] + sectors["s_gap"][0]*sectors["s_gap"][1]
    excited_mean = Fraction(excited_M1, excited_total)
    gap_ratio = Fraction(delta_s, delta_r)

    # Phenomenology reconstruction from cumulants/gaps.
    lambda_H_from_excited_mean = gap_ratio / excited_mean
    A_ckm_from_lambda_H = Fraction(q**4, phi3) * lambda_H_from_excited_mean
    pmns_theta13_from_lambda_H = Fraction(q*q, lam*lam*phi3) * lambda_H_from_excited_mean

    # Existing direct forms.
    lambda_H_direct = Fraction(phi3, phi4*phi4)
    A_ckm_direct = Fraction(q**4, phi4*phi4)
    pmns_theta13_direct = Fraction(q*q, (lam*phi4)**2)

    # Group dimensions from cumulants.
    dim_G2 = lam*phi6
    dim_SU5 = f
    dim_SO10 = q*q*(mu+1)
    dim_E6 = lam*q*phi3
    dim_E8 = E + lam**3

    # Additional fluctuation bridge.
    coefficient_variation_sq = variance / (mean*mean)
    ckm_A_minus_higgs_numerator = phi3 + mu  # 17
    cv2_structural = Fraction(lam*lam * ckm_A_minus_higgs_numerator, phi6*phi6)

    checks = {
        "true_master_equation": math.factorial(q) == 2*q,
        "w33_atoms": (q, lam, mu, k, v, E, D) == (3,2,4,12,40,240,480),
        "mean_is_G2_dim_over_q": mean == Fraction(dim_G2, q) == Fraction(14,3),
        "variance_is_E8_plus_SU5_over_q2": variance == Fraction(dim_E8 + dim_SU5, q*q) == Fraction(272,9),
        "coefficient_variation_sq_is_68_over_49": coefficient_variation_sq == Fraction(68,49),
        "cv2_structural_form": coefficient_variation_sq == cv2_structural,
        "excited_total_E6": excited_total == dim_E6 == 78,
        "excited_mean_160_over_13": excited_mean == Fraction(160,13),
        "gap_ratio_8_over_5": gap_ratio == Fraction(8,5),
        "lambda_H_from_excited_mean": lambda_H_from_excited_mean == lambda_H_direct == Fraction(13,100),
        "A_ckm_from_lambda_H": A_ckm_from_lambda_H == A_ckm_direct == Fraction(81,100),
        "pmns_theta13_from_lambda_H": pmns_theta13_from_lambda_H == pmns_theta13_direct == Fraction(9,400),
        "dimensions": (dim_G2, dim_SU5, dim_SO10, dim_E6, dim_E8) == (14,24,45,78,248),
    }

    result = {
        "part": "CCCCCIX",
        "title": "Cumulant Phenomenology Bridge",
        "atoms": {
            "q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "E": E, "directed_edges": D,
            "r": r, "s": s, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6,
        },
        "free_energy_cumulants": {
            "mean_kappa1": str(mean),
            "variance_kappa2": str(variance),
            "coefficient_variation_squared": str(coefficient_variation_sq),
            "mean_as_G2_over_q": f"{dim_G2}/{q}",
            "variance_as_E8_plus_SU5_over_q2": f"({dim_E8}+{dim_SU5})/{q*q}",
        },
        "excited_sector_bridge": {
            "excited_total": excited_total,
            "E6_dim": dim_E6,
            "excited_mean": str(excited_mean),
            "gap_ratio_Delta_s_over_Delta_r": str(gap_ratio),
            "lambda_H_from_gap_ratio_over_excited_mean": str(lambda_H_from_excited_mean),
        },
        "phenomenology_reconstruction": {
            "lambda_H": str(lambda_H_from_excited_mean),
            "A_CKM_from_lambda_H": str(A_ckm_from_lambda_H),
            "PMNS_theta13_from_lambda_H": str(pmns_theta13_from_lambda_H),
            "A_over_lambda_H": str(A_ckm_from_lambda_H / lambda_H_from_excited_mean),
        },
        "fluctuation_bridge": {
            "CV_squared": str(coefficient_variation_sq),
            "CV_squared_structural": "lambda^2*(Phi3+mu)/Phi6^2",
            "Phi3_plus_mu": ckm_A_minus_higgs_numerator,
        },
        "structural_dimensions": {"G2": dim_G2, "SU5": dim_SU5, "SO10": dim_SO10, "E6": dim_E6, "E8": dim_E8},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": (
            "The free-energy cumulants reconstruct phenomenology. The full mean is dim(G2)/q, the variance is "
            "(dim(E8)+dim(SU5))/q^2, and the excited E6 mean combined with the restricted gap ratio gives "
            "lambda_H=13/100. That Higgs value then generates CKM A and PMNS theta13 by existing gap-square projections."
        ),
    }

    out = Path("PART_CCCCCIX_cumulant_phenomenology_bridge_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCCIX: Cumulant Phenomenology Bridge")
    print("="*86)
    for key, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'} {key}")
    print("-"*86)
    print(f"mean={mean}, variance={variance}, CV^2={coefficient_variation_sq}")
    print(f"excited_mean={excited_mean}, gap_ratio={gap_ratio}")
    print(f"lambda_H={lambda_H_from_excited_mean}, A={A_ckm_from_lambda_H}, theta13={pmns_theta13_from_lambda_H}")
    print(f"all_checks_pass={result['all_checks_pass']}")
    print(f"wrote {out}")

    assert result["all_checks_pass"]


if __name__ == "__main__":
    main()
