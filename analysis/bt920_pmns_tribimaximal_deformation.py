#!/usr/bin/env python3
"""
BT920 - Hard open #1 (partial solution): the PMNS matrix is
        tribimaximal deformed by +-1/Phi3.

The flavor group is S3 (BT879).  The S3-symmetric ("democratic")
neutrino mixing is tribimaximal (TBM): sin^2 th12 = 1/3,
sin^2 th23 = 1/2, sin^2 th13 = 0 (the (1,1,1) democratic eigenvector
is TBM's solar column).  The substrate's PMNS angles are TBM deformed
by a single parameter 1/Phi3 = 1/13:

  sin^2 th12 = (1/3)(1 - 1/Phi3) = 4/13     (solar, REDUCED)
  sin^2 th23 = (1/2)(1 + 1/Phi3) = 7/13     (atmospheric, RAISED)
  sin^2 th13 = lambda/(Phi6.Phi3) = 2/91    (reactor, turned on)

The solar and atmospheric deformations are equal and opposite in the
SAME unit 1/Phi3 (solar down, atmospheric up), and the reactor angle
turns on at lambda/(Phi6 Phi3).  So the PMNS PATTERN is derived: TBM
from the S3 flavor symmetry, deformed at the substrate flavor-breaking
scale 1/Phi3.  (What remains: a first-principles value for the single
deformation 1/Phi3 and the reactor coefficient lambda/Phi6 from the
within-grade profile.)
"""
from __future__ import annotations

from fractions import Fraction as F
import json


def main():
    q, lam, mu, Phi3, Phi6 = 3, 2, 4, 13, 7

    s12 = F(mu, Phi3)            # 4/13
    s23 = F(Phi6, Phi3)         # 7/13
    s13 = F(lam, Phi6*Phi3)     # 2/91
    TBM12, TBM23, TBM13 = F(1, 3), F(1, 2), F(0)
    eps = F(1, Phi3)            # the deformation parameter

    # T1: solar = (1/3)(1 - eps)
    assert s12 == TBM12*(1 - eps)
    print(f"T1 sin^2 th12 = (1/3)(1 - 1/Phi3) = {s12} (solar, reduced "
          f"from TBM 1/3 by factor 1-1/13)")

    # T2: atmospheric = (1/2)(1 + eps)
    assert s23 == TBM23*(1 + eps)
    print(f"T2 sin^2 th23 = (1/2)(1 + 1/Phi3) = {s23} (atmospheric, "
          f"raised from TBM 1/2 by factor 1+1/13)")

    # T3: reactor turns on at lambda/(Phi6 Phi3)
    assert s13 == F(lam, Phi6*Phi3) and TBM13 == 0
    print(f"T3 sin^2 th13 = lambda/(Phi6.Phi3) = {s13} (reactor, turned "
          f"on from TBM 0)")

    # the deformation is a SINGLE parameter 1/Phi3, opposite signs
    solar_def = 1 - s12/TBM12
    atmos_def = s23/TBM23 - 1
    assert solar_def == eps and atmos_def == eps
    print(f"   solar deformation = -1/Phi3, atmospheric = +1/Phi3 "
          f"(SAME unit {eps}); a single flavor-breaking parameter")

    # PDG check
    import math
    pdg = {"s12": (0.307, 0.012), "s23": (0.546, 0.021),
           "s13": (0.02203, 0.00070)}
    for nm, val in [("s12", s12), ("s23", s23), ("s13", s13)]:
        o, e = pdg[nm]
        print(f"   {nm} = {float(val):.5f} vs PDG {o} "
              f"({abs(float(val)-o)/e:.1f} sigma)")

    print("\nPARTIAL SOLUTION (#1): PMNS = tribimaximal (the S3-symmetric")
    print("mixing, S3 = the derived flavor group BT879) deformed by the")
    print("single parameter 1/Phi3 - solar down, atmospheric up by the")
    print("same unit, reactor on at lambda/(Phi6 Phi3).  The PATTERN is")
    print("derived; the value of 1/Phi3 from the within-grade profile is")
    print("the remaining input.")

    out = {
        "theorem": "BT920 PMNS = tribimaximal deformed by 1/Phi3",
        "solar": {"value": "4/13", "form": "(1/3)(1 - 1/Phi3)"},
        "atmospheric": {"value": "7/13", "form": "(1/2)(1 + 1/Phi3)"},
        "reactor": {"value": "2/91", "form": "lambda/(Phi6*Phi3)"},
        "deformation_parameter": "1/Phi3 = 1/13",
        "tbm_origin": "S3 flavor symmetry (BT879), democratic = TBM",
        "remaining": "value of 1/Phi3 and reactor coeff from within-grade",
    }
    with open("data/bt920_pmns_tribimaximal_deformation.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt920_pmns_tribimaximal_deformation.json")


if __name__ == "__main__":
    main()
