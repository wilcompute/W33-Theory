#!/usr/bin/env python3
"""
BT918 - Falsifiability cross-check: the BT898 mixing-angle ratios vs PDG.

BT898 expressed the fermion mixing angles as graph-parameter ratios in
the within-grade ("profile") coordinate system (q=3, lambda=2, mu=4,
Phi3=13, Phi6=7).  Those ratios were flagged as profile constraints,
not yet derived from the 9.2 within-grade layer.  BT918 does the honest
falsifiability evaluation: compares them to current PDG/NuFIT central
values.

  sin^2 th12 (solar)   = mu/Phi3            = 4/13
  sin^2 th23 (atmos)   = Phi6/Phi3          = 7/13
  sin^2 th13 (reactor) = lambda/(Phi6.Phi3) = 2/91
  sin th_C (Cabibbo)   = q/sqrt(Phi3^2+q^2) = 3/sqrt(178)

Result: all four land within 1 sigma of PDG (deviations 0.06-1.4%).
Structural notes: the two large PMNS angles sum to 4/13+7/13 = 11/13
(numerator 11 = k-1 = the Ihara prime); the reactor denominator is
Phi6.Phi3 = 91; the Cabibbo radicand is Phi3^2+q^2 = 178.

Honest boundary: this confirms the BT898 ratios are empirically
excellent; the first-principles DERIVATION of these specific ratios
from the within-grade (q^2=9) profile remains open (BT894/897/898).
"""
from __future__ import annotations

import json
import math


def main():
    q, lam, mu, Phi3, Phi6 = 3, 2, 4, 13, 7
    rows = [
        ("sin2_theta12_solar", "mu/Phi3", mu/Phi3, 0.307, 0.012),
        ("sin2_theta23_atmos", "Phi6/Phi3", Phi6/Phi3, 0.546, 0.022),
        ("sin2_theta13_reactor", "lambda/(Phi6*Phi3)",
         lam/(Phi6*Phi3), 0.02203, 0.00070),
        ("sin_thetaC_Cabibbo", "q/sqrt(Phi3^2+q^2)",
         q/math.sqrt(Phi3**2 + q**2), 0.22500, 0.00070),
    ]
    print(f"{'quantity':24s} {'substrate':20s} {'value':>9s} "
          f"{'PDG':>9s} {'dev%':>6s} {'sigma':>6s}")
    out = []
    allok = True
    for name, form, val, obs, err in rows:
        dev = abs(val-obs)/obs*100
        sig = abs(val-obs)/err
        print(f"{name:24s} {form:20s} {val:9.5f} {obs:9.5f} "
              f"{dev:6.2f} {sig:6.1f}")
        out.append({"quantity": name, "substrate_form": form,
                    "value": val, "pdg": obs, "dev_pct": dev,
                    "sigma": sig})
        if sig > 1.0:
            allok = False

    # structural identities
    assert mu/Phi3 + Phi6/Phi3 == 11/13   # large angles sum to (k-1)/Phi3
    assert Phi3**2 + q**2 == 178
    print(f"\nstructural: sin2_th12 + sin2_th23 = 4/13 + 7/13 = 11/13 "
          f"(11 = k-1 = Ihara prime); Cabibbo radicand Phi3^2+q^2 = 178")
    print(f"all four within 1 sigma of PDG: {allok}")
    assert allok
    print("\nFALSIFIABILITY: the four mixing angles, as substrate graph-")
    print("parameter ratios (BT898 within-grade coordinates), match the")
    print("observed PMNS + Cabibbo angles to 0.06-1.4% (all <1 sigma).")
    print("Derivation of these ratios from the q^2=9 profile is open.")

    res = {
        "theorem": "BT918 mixing-angle falsifiability cross-check",
        "angles": out,
        "all_within_1sigma": allok,
        "structural": {"th12+th23": "11/13 (11=k-1 Ihara)",
                       "cabibbo_radicand": 178},
        "boundary": "ratios empirically excellent; first-principles "
                    "derivation from within-grade q^2=9 profile open",
    }
    with open("data/bt918_mixing_angle_falsifiability.json", "w") as fj:
        json.dump(res, fj, indent=2)
    print("\nwrote data/bt918_mixing_angle_falsifiability.json")


if __name__ == "__main__":
    main()
