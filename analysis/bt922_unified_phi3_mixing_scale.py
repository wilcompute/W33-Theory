#!/usr/bin/env python3
"""
BT922 - The unified Phi3 mixing scale: both quark and lepton mixing
        are governed by Phi3 = q^2+q+1 = 13 (hard open #1, unification).

BT920: the PMNS (lepton) angles are tribimaximal deformed by 1/Phi3.
BT922: the CKM (quark) Cabibbo angle is the q/Phi3 rotation -

  tan theta_C = q/Phi3 = 3/13       (sin theta_C = q/sqrt(Phi3^2+q^2))

so the entire fermion-mixing sector is set by the single scale
Phi3 = q^2+q+1 = 13 (the third cyclotomic; the number of points in
PG(2,3); the Singer C13 clock, BT807):

  QUARK  (CKM):  tan theta_C = q/Phi3 = 3/13          (a rotation)
  LEPTON (PMNS): TBM deformed by 1/Phi3
                 (solar (1/3)(1-1/Phi3), atmos (1/2)(1+1/Phi3))

Quark mixing is a small q/Phi3 rotation off the identity; lepton
mixing is a 1/Phi3 deformation off tribimaximal.  Same scale Phi3,
two regimes (rotation vs democratic deformation) - the quark/lepton
mixing dichotomy is the CKM-near-identity vs PMNS-near-TBM split, both
controlled by Phi3.
"""
from __future__ import annotations

from fractions import Fraction as F
import json
import math


def main():
    q, lam, mu, Phi3, Phi6 = 3, 2, 4, 13, 7

    # CKM: Cabibbo as the q/Phi3 rotation
    tanC = F(q, Phi3)
    sinC = q/math.sqrt(Phi3**2 + q**2)
    obs_tanC = 0.2243/0.97373    # |Vus|/|Vud|
    print(f"QUARK (CKM): tan theta_C = q/Phi3 = {tanC} = {float(tanC):.5f}")
    print(f"   observed |Vus|/|Vud| = {obs_tanC:.5f} "
          f"(dev {abs(float(tanC)-obs_tanC)/obs_tanC*100:.2f}%)")
    print(f"   sin theta_C = q/sqrt(Phi3^2+q^2) = {sinC:.5f}")
    assert abs(float(tanC) - obs_tanC)/obs_tanC < 0.01

    # LEPTON: PMNS = TBM deformed by 1/Phi3 (BT920)
    eps = F(1, Phi3)
    s12 = F(1, 3)*(1 - eps)
    s23 = F(1, 2)*(1 + eps)
    s13 = F(lam, Phi6*Phi3)
    assert s12 == F(4, 13) and s23 == F(7, 13) and s13 == F(2, 91)
    print(f"LEPTON (PMNS): TBM deformed by 1/Phi3 = {eps}:")
    print(f"   sin2_th12 = (1/3)(1-1/Phi3) = {s12}")
    print(f"   sin2_th23 = (1/2)(1+1/Phi3) = {s23}")
    print(f"   sin2_th13 = lambda/(Phi6 Phi3) = {s13}")

    # the unified scale
    print(f"\nUNIFIED: both mixing sectors set by Phi3 = q^2+q+1 = "
          f"{q**2+q+1} = 13")
    print(f"   = #points in PG(2,3) = the Singer C13 clock (BT807)")
    print(f"   quark = q/Phi3 rotation (off identity);")
    print(f"   lepton = 1/Phi3 deformation (off tribimaximal).")
    assert q**2 + q + 1 == Phi3

    out = {
        "theorem": "BT922 unified Phi3 mixing scale",
        "quark_CKM": {"tan_thetaC": "q/Phi3 = 3/13",
                      "sin_thetaC": "q/sqrt(Phi3^2+q^2) = 3/sqrt(178)"},
        "lepton_PMNS": {"deformation": "1/Phi3 off tribimaximal",
                        "s12": "(1/3)(1-1/Phi3)=4/13",
                        "s23": "(1/2)(1+1/Phi3)=7/13",
                        "s13": "lambda/(Phi6 Phi3)=2/91"},
        "scale": "Phi3 = q^2+q+1 = 13 (PG(2,3) / Singer C13)",
        "dichotomy": "quark = rotation off identity; "
                     "lepton = deformation off TBM",
    }
    with open("data/bt922_unified_phi3_mixing_scale.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt922_unified_phi3_mixing_scale.json")


if __name__ == "__main__":
    main()
