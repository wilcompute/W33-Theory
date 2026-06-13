#!/usr/bin/env python3
"""
BT919 - The complete quark+lepton mixing+CP falsifiability scorecard.

Consolidates the W(3,3) graph-parameter predictions for the entire
flavor-mixing sector (CKM elements, PMNS angles, CP phase, Jarlskog,
Wolfenstein A) into one audit against current PDG/NuFIT central values
with sigma levels.  Extends BT918 (PMNS+Cabibbo) to the full sector.

All quantities are rational functions of {q=3, lambda=2, mu=4,
Phi3=13, Phi6=7, Theta=10, v=40}.  Result: 8 of 9 within 1 sigma; the
only outlier is the Wolfenstein A = mu/(q+lambda) = 4/5 at 1.7 sigma.

Honest framing: the discrete STRUCTURE under these ratios is derived
(BT858-892, the long-root transvection geometry); the mixing/CP
RATIOS themselves are validated phenomenology (w33_paper), with the
first-principles derivation from the within-grade q^2=9 profile
(BT894/897/898) still open.  This packet is the falsifiability audit,
not a derivation.
"""
from __future__ import annotations

import json


def main():
    q, lam, mu, Phi3, Phi6, Theta, v = 3, 2, 4, 13, 7, 10, 40
    rows = [
        ("|V_us| Cabibbo", "(lam+Phi6)/v", (lam+Phi6)/v, 0.22501, 0.00068),
        ("|V_cb|", "mu/Theta^2", mu/Theta**2, 0.04053, 0.00072),
        ("|V_ub|", "lam/(v*Phi3)", lam/(v*Phi3), 0.00382, 0.00020),
        ("sin2_th12 solar", "mu/Phi3", mu/Phi3, 0.307, 0.012),
        ("sin2_th23 atmos", "Phi6/Phi3", Phi6/Phi3, 0.546, 0.021),
        ("sin2_th13 reactor", "lam/(Phi6*Phi3)", lam/(Phi6*Phi3),
         0.02203, 0.00070),
        ("sin delta_CP", "(mu^2-1)/(mu^2+1)", (mu**2-1)/(mu**2+1),
         0.911, 0.030),
        ("J_CKM Jarlskog", "27/884000", 27/884000, 3.08e-5, 0.13e-5),
        ("A Wolfenstein", "mu/(q+lam)", mu/(q+lam), 0.826, 0.015),
    ]
    print(f"{'quantity':20s} {'substrate':18s} {'value':>11s} "
          f"{'PDG':>10s} {'dev%':>6s} {'sig':>5s}")
    out = []
    within = 0
    for nm, f, val, obs, err in rows:
        dev = abs(val-obs)/obs*100
        sig = abs(val-obs)/err
        if sig <= 1.0:
            within += 1
        print(f"{nm:20s} {f:18s} {val:11.5g} {obs:10.5g} {dev:6.2f} "
              f"{sig:5.1f}")
        out.append({"quantity": nm, "form": f, "value": val,
                    "pdg": obs, "err": err, "dev_pct": dev, "sigma": sig})
    print(f"\nwithin 1 sigma: {within}/{len(rows)} "
          f"(outlier: A = mu/(q+lam) = 4/5 at 1.7 sigma)")
    assert within == 8
    # the two large PMNS angles + Ihara identity (BT918)
    assert mu/Phi3 + Phi6/Phi3 == 11/13
    print("structural: sin2_th12+sin2_th23 = 11/13 (11=k-1 Ihara); "
          "all denominators built from Phi3=13, Phi6=7, Theta=10, v=40")

    res = {
        "theorem": "BT919 mixing+CP falsifiability scorecard",
        "predictions": out,
        "within_1sigma": within, "total": len(rows),
        "outlier": "A = mu/(q+lambda) = 4/5 at 1.7 sigma",
        "boundary": "structure derived (BT858-892); mixing/CP ratios "
                    "validated phenomenology, within-grade derivation open",
    }
    with open("data/bt919_mixing_cp_scorecard.json", "w") as fj:
        json.dump(res, fj, indent=2)
    print("\nwrote data/bt919_mixing_cp_scorecard.json")


if __name__ == "__main__":
    main()
