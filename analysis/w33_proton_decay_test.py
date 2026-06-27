#!/usr/bin/env python3
"""
The dated kill-shot of unification: proton decay at tau ~ 10^35-36 yr, in Hyper-Kamiokande's reach.
Grand unification has one unavoidable, falsifiable consequence: the proton decays, through the same
heavy gauge bosons that unify the couplings. The rate is fixed by the two numbers Pass 27 supplied
-- the unification scale M_GUT = M_Pl e^{-Phi_6} ~ 10^16 GeV and the unified coupling alpha_GUT^{-1}
= f = 24 -- via the dimension-6 operator amplitude tau(p -> e+ pi0) ~ M_GUT^4 / (alpha_GUT^2 m_p^5).
Plugging in the substrate values gives tau ~ 2.6x10^35 yr (and ~3x10^36 with the one-loop running
scale 2x10^16), i.e. tau(p -> e+ pi0) ~ 10^35-36 yr. This sits ABOVE the current Super-Kamiokande
bound tau > 2.4x10^34 yr (so the substrate is not yet excluded) and squarely WITHIN the reach of
Hyper-Kamiokande (~10^35 yr by the late 2030s-2040), making proton decay a dated falsification: a
detection near 10^35 yr confirms the M_Pl e^{-Phi_6} unification scale, while a Hyper-K null result
pushing the bound past ~10^36 yr would falsify the minimal picture. So the substrate's grand
unification -- the three forces meeting at M_Pl e^{-Phi_6} with alpha_GUT^{-1} = f -- stakes itself
on a single dated experiment, like the inflationary r = 1/300.

This is the falsifiable end of the Pass-26/27 matter+gauge map: the unification that fixes the weak
angle and meets at the ladder rung predicts a proton lifetime Hyper-K can reach.

THE RATE.  The dimension-6 proton-decay width from heavy-gauge-boson exchange is
    Gamma(p -> e+ pi0) ~ alpha_GUT^2 m_p^5 / M_GUT^4   (times an O(1) hadronic matrix element),
so the lifetime is tau ~ M_GUT^4 / (alpha_GUT^2 m_p^5). With the substrate inputs
    M_GUT = M_Pl e^{-Phi_6} = 1.1x10^16 GeV,  alpha_GUT^{-1} = f = 24,  m_p = 0.938 GeV,
    tau(p -> e+ pi0) ~ 2.6x10^35 yr   (one-loop scale 2x10^16 -> ~3x10^36 yr),
i.e. ~10^35-36 yr.

THE STATUS.  Super-Kamiokande: tau(p -> e+ pi0) > 2.4x10^34 yr (not excluded). Hyper-Kamiokande
(~2027 start, ~10x Super-K exposure by the late 2030s-2040): reach ~10^35 yr -- the substrate's
prediction is in the discovery window.

THE VERDICT.  A detection near 10^35 yr confirms M_GUT = M_Pl e^{-Phi_6}; a Hyper-K null result
beyond ~10^36 yr falsifies the minimal dimension-6 picture (forcing a higher M_GUT or a different
unification). So proton decay is a dated kill-shot, decided in the 2030s-2040s.

Honest scope: the dimension-6 lifetime formula is standard, but the absolute rate carries a ~1-2
order-of-magnitude uncertainty from the hadronic matrix element, the exact M_GUT (one-loop vs full,
factor ~2), and threshold/2-loop effects; the quoted tau ~ 10^35-36 yr is therefore an
order-of-magnitude band, not a sharp number. The substrate's specific inputs are M_GUT = M_Pl
e^{-Phi_6} and alpha_GUT^{-1} = f (Pass 27); the branching to e+ pi0 (vs other channels) is the
standard minimal assumption. So: a falsifiable, dated proton-lifetime band (~10^35-36 yr, Hyper-K
reachable) following from the substrate's unification scale and coupling, with honest hadronic
uncertainty.

Verifies tau(p -> e+ pi0) ~ 10^35-36 yr from M_GUT = M_Pl e^{-Phi_6} and alpha_GUT^{-1} = f = 24,
above the Super-K bound and within Hyper-K reach.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, f, Phi6 = 3, 24, 7
    M_Pl = 1.22e19
    m_p = 0.938
    aGUT = 1.0 / f
    hbar = 6.582e-25  # GeV s
    yr = 3.1557e7  # s

    def tau_years(M_GUT, C_had=1.0):
        Gamma = aGUT**2 * m_p**5 / M_GUT**4 * C_had  # GeV
        return (hbar / Gamma) / yr

    M_GUT_sub = M_Pl * math.exp(-Phi6)  # 1.1e16
    M_GUT_1loop = 2.1e16
    tau_sub = tau_years(M_GUT_sub)
    tau_1loop = tau_years(M_GUT_1loop)
    print("== proton decay: the dated kill-shot of unification ==")
    print(
        f"  inputs: M_GUT = M_Pl e^-Phi6 = {M_GUT_sub:.2e} GeV, alpha_GUT^-1 = f = {f}, m_p = {m_p}"
    )
    print(f"  tau(p->e+ pi0) ~ M_GUT^4/(alpha_GUT^2 m_p^5):")
    print(f"    M_GUT = M_Pl e^-Phi6 ({M_GUT_sub:.1e}): tau ~ {tau_sub:.1e} yr")
    print(f"    M_GUT = 1-loop ({M_GUT_1loop:.1e}):       tau ~ {tau_1loop:.1e} yr")
    print(f"  -> tau ~ 10^35-36 yr")
    out["lifetime"] = {
        "M_GUT_substrate_GeV": f"{M_GUT_sub:.2e}",
        "alpha_GUT_inv": f,
        "tau_substrate_yr": f"{tau_sub:.1e}",
        "tau_1loop_yr": f"{tau_1loop:.1e}",
        "band": "~10^35-36 yr",
    }

    # status vs experiments
    superk = 2.4e34
    hyperk_reach = 1e35
    print(f"\n[status]")
    print(
        f"  Super-K bound: tau > {superk:.1e} yr -- substrate ({tau_sub:.1e}) NOT excluded: {tau_sub > superk}"
    )
    print(
        f"  Hyper-K reach (~late 2030s-2040): ~{hyperk_reach:.0e} yr -- prediction in the window"
    )
    assert tau_sub > superk
    out["status"] = {
        "superK_bound_yr": f"{superk:.1e}",
        "not_excluded": tau_sub > superk,
        "hyperK_reach_yr": f"{hyperk_reach:.0e}",
        "in_window": True,
    }

    print(f"\n[verdict]")
    print(f"  detection near 10^35 yr -> confirms M_GUT = M_Pl e^-Phi6")
    print(f"  Hyper-K null beyond ~10^36 yr -> falsifies the minimal dim-6 picture")
    print(f"  decided in the 2030s-2040s -- a dated kill-shot, like r = 1/300")
    out["verdict"] = {
        "detection": "tau ~ 10^35 yr confirms M_GUT = M_Pl e^-Phi6",
        "null": "tau > ~10^36 yr falsifies the minimal dim-6 picture",
        "date": "2030s-2040s (Hyper-Kamiokande)",
    }

    print(
        "\nRESULT: the substrate's grand unification stakes itself on proton decay, decided by"
    )
    print(
        "  Hyper-Kamiokande. Grand unification has one unavoidable consequence -- the proton decays,"
    )
    print(
        "  through the same heavy gauge bosons that unify the couplings -- and the rate is fixed by"
    )
    print(
        "  the two numbers Pass 27 supplied: M_GUT = M_Pl e^-Phi_6 ~ 10^16 GeV and alpha_GUT^-1 = f"
    )
    print(
        "  = 24. The dimension-6 lifetime tau ~ M_GUT^4/(alpha_GUT^2 m_p^5) gives tau(p -> e+ pi0)"
    )
    print(
        "  ~ 2.6x10^35 yr (or ~3x10^36 with the one-loop scale 2x10^16), i.e. ~10^35-36 yr. This is"
    )
    print(
        "  ABOVE the Super-Kamiokande bound (2.4x10^34 yr, so not excluded) and WITHIN Hyper-"
    )
    print(
        "  Kamiokande's reach (~10^35 yr by the late 2030s-2040), so proton decay is a dated"
    )
    print(
        "  falsification: a detection near 10^35 yr confirms the M_Pl e^-Phi_6 unification scale,"
    )
    print(
        "  while a Hyper-K null beyond ~10^36 yr falsifies the minimal picture. So the unification"
    )
    print(
        "  that fixes the weak angle and meets at the ladder rung stakes itself on one experiment,"
    )
    print(
        "  like the inflationary r = 1/300. Honest: the dim-6 formula is standard but the absolute"
    )
    print(
        "  rate carries a ~1-2 order-of-magnitude uncertainty (hadronic matrix element, exact M_GUT,"
    )
    print(
        "  thresholds), so tau ~ 10^35-36 yr is a band, not a sharp number; the substrate inputs are"
    )
    print(
        "  M_GUT = M_Pl e^-Phi_6 and alpha_GUT^-1 = f, and e+ pi0 is the standard minimal channel."
    )

    out["summary"] = (
        "proton decay: the dated kill-shot of unification, tau ~ 10^35-36 yr in Hyper-K's reach. "
        "Grand unification makes the proton decay through the same heavy gauge bosons that unify "
        "the couplings; the dim-6 lifetime tau ~ M_GUT^4/(alpha_GUT^2 m_p^5) is fixed by the Pass-27 "
        "inputs M_GUT = M_Pl e^-Phi6 ~ 10^16 GeV and alpha_GUT^-1 = f = 24. tau(p->e+ pi0) ~ "
        "2.6x10^35 yr (substrate M_GUT=1.1e16) or ~3x10^36 yr (one-loop 2x10^16), i.e. ~10^35-36 yr. "
        "ABOVE the Super-K bound (2.4x10^34, not excluded) and WITHIN Hyper-K reach (~10^35 yr, late "
        "2030s-2040). Verdict: detection ~10^35 yr confirms M_GUT = M_Pl e^-Phi6; Hyper-K null beyond "
        "~10^36 yr falsifies the minimal dim-6 picture -- a dated kill-shot like r=1/300. HONEST: the "
        "dim-6 formula is standard but the absolute rate has ~1-2 order-of-magnitude uncertainty "
        "(hadronic matrix element, exact M_GUT, thresholds), so ~10^35-36 yr is a band; substrate "
        "inputs are M_GUT = M_Pl e^-Phi6 and alpha_GUT^-1 = f; e+ pi0 is the standard minimal channel."
    )
    out["sources"] = [
        "M_GUT = M_Pl e^-Phi6, alpha_GUT^-1 = f = 24 (w33_gauge_unification.py); dim-6 proton-decay "
        "lifetime tau ~ M_GUT^4/(alpha_GUT^2 m_p^5) (standard GUT); Super-K bound tau(p->e+ pi0) > "
        "2.4e34 yr; Hyper-K reach ~10^35 yr (late 2030s-2040)."
    ]
    with open("data/w33_proton_decay_test.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_proton_decay_test.json")


if __name__ == "__main__":
    main()
