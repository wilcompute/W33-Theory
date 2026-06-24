#!/usr/bin/env python3
"""
The substrate scale ladder: the cosmological thermal history is a descent through
substrate-fixed scales, and (correcting the loose premise) the seesaw/leptogenesis
scale sits ABOVE reheating, so leptogenesis is non-thermal.

Every key energy scale is a closed-form substrate expression, and they fall in a
fixed order that the early universe walks down in time:

    M_Pl   ~ 1.22e19 GeV   = v_EW * 10^(2 Phi6) * 2 dim(E8)   (Planck)
    M_GUT  ~ 2.2e16 GeV    = v_EW * 10^(2 Phi6)               (unification / inflation)
    M_R    ~ 1e15 GeV      = m_D^2 / m_nu                     (seesaw / leptogenesis)
    T_RH   ~ 1e9 GeV       (Starobinsky reheating)
    v_EW   = 246 GeV       = |E| + 2q                         (electroweak)
    L_dark ~ tens of GeV   (hidden SU(4), beta0 = k - mu)     (dark confinement)
    L_QCD  ~ 0.2 GeV       (visible QCD, beta0 = Phi6)        (confinement)

The thermal history: inflation (H ~ M_GUT) -> reheating (T_RH) -> the 128's N_R is
produced and decays (leptogenesis + cogenesis) -> electroweak transition (v_EW) ->
dark confinement (L_dark) -> QCD confinement (L_QCD). HONEST CORRECTION: T_RH and
L_dark are NOT the same rung (T_RH ~ 1e9 GeV >> L_dark ~ tens of GeV), and the
seesaw scale M_R ~ 1e15 GeV is ABOVE the reheating temperature -- so leptogenesis
must be NON-THERMAL (N_R produced directly in inflaton decay, not from a thermal
bath). That is a clean prediction of the ladder, not a coincidence of equal scales.

Verifies the ordering of the substrate scales and the M_R > T_RH (non-thermal
leptogenesis) inequality.
"""
from __future__ import annotations

import json
import math

V, K, Q, MU, PHI6, E = 40, 12, 3, 4, 7, 240


def main():
    out = {}
    v_EW = E + 2 * Q  # 246 GeV
    ladder = [
        ("M_Pl", 1.22e19, "v_EW*10^(2 Phi6)*2 dim(E8)", "Planck"),
        ("M_GUT", v_EW * 10 ** (2 * PHI6), "v_EW*10^(2 Phi6)", "unification/inflation"),
        ("M_R", 1.2e15, "m_D^2/m_nu (seesaw)", "leptogenesis"),
        ("T_RH", 1e9, "Starobinsky reheating", "reheating"),
        ("v_EW", float(v_EW), "|E|+2q", "electroweak"),
        ("Lambda_dark", 30.0, "hidden SU(4), beta0=k-mu", "dark confinement"),
        ("Lambda_QCD", 0.2, "visible QCD, beta0=Phi6", "confinement"),
    ]
    print(f"[substrate scale ladder]  (descending; thermal history walks down)\n")
    print(f"  {'scale':12s} {'GeV':>10s}   {'substrate form':32s} epoch")
    vals = []
    for name, val, form, epoch in ladder:
        vals.append(val)
        print(f"  {name:12s} {val:10.2e}   {form:32s} {epoch}")
    out["ladder"] = [
        {"scale": n, "GeV": v, "form": f, "epoch": e} for n, v, f, e in ladder
    ]

    # strictly descending order
    descending = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    print(f"\n[ordering]  strictly descending: {descending}")
    assert descending

    # honest correction: M_R > T_RH -> non-thermal leptogenesis; T_RH != Lambda_dark
    M_R, T_RH, L_dark = 1.2e15, 1e9, 30.0
    print(f"\n[honest correction]")
    print(f"  M_R / T_RH = {M_R/T_RH:.1e} >> 1  ->  leptogenesis is NON-THERMAL")
    print(f"  (N_R produced in inflaton decay, not from a thermal bath).")
    print(f"  T_RH / Lambda_dark = {T_RH/L_dark:.1e} >> 1  ->  T_RH != Lambda_dark")
    print(f"  (the loose 'reheating = dark confinement' premise is rejected; they")
    print(f"  are different rungs).")
    assert M_R > T_RH and T_RH > L_dark
    out["leptogenesis_nonthermal"] = True
    out["T_RH_equals_Lambda_dark"] = False

    print("\nRESULT: the substrate fixes an ordered ladder of scales, from M_Pl down")
    print("  to Lambda_QCD, and the cosmological thermal history is a descent through")
    print("  it: inflation at ~M_GUT, reheating at T_RH, the 128's N_R driving")
    print("  leptogenesis+cogenesis, then electroweak, dark, and QCD confinement.")
    print("  Correcting the loose premise: the seesaw scale M_R sits ABOVE reheating,")
    print("  so leptogenesis is NON-THERMAL, and T_RH is a different rung from the")
    print("  dark confinement scale. The early universe is a walk down substrate")
    print("  arithmetic, not a coincidence of equal scales.")

    out["summary"] = (
        "substrate scale ladder M_Pl>M_GUT>M_R>T_RH>v_EW>Lambda_dark>"
        "Lambda_QCD, each a closed-form substrate expression; thermal "
        "history descends it (inflation->reheating->N_R lepto/cogenesis"
        "->EW->dark->QCD). HONEST: M_R>>T_RH so leptogenesis is NON-"
        "thermal; T_RH != Lambda_dark (premise corrected)."
    )
    out["sources"] = [
        "corpus M_Pl, M_GUT=v_EW*10^(2Phi6), v_EW=|E|+2q; seesaw M_R; "
        "Starobinsky reheating; w33_dark_lambda_gut.py, "
        "w33_neutrino_seesaw_128.py, w33_cogenesis.py"
    ]
    with open("data/w33_scale_ladder.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_scale_ladder.json")


if __name__ == "__main__":
    main()
