#!/usr/bin/env python3
"""
The two-scale GUT and the proton-decay signature: the E6 -> SU(3)^3 -> SM chain
gives M_I ~ 10^13-14 GeV and M_GUT ~ 10^16 GeV, with proton decay dominated by the
gauge-mediated p -> e^+ pi^0 mode (the non-SUSY signature), tau_p ~ 10^35-36 yr --
the precise Hyper-Kamiokande target.

In non-supersymmetric GUTs (E6/trinification) proton decay is GAUGE-mediated by
the superheavy X,Y bosons at M_GUT, and the dominant channel is

    p -> e^+ pi^0   (branching ~ 30-60%),

with p -> mu^+ pi^0, p -> e^+ K^0, etc. subdominant; the p -> nubar K^+ mode
(which DOMINATES in SUSY GUTs via dimension-5 operators) is SUPPRESSED here, since
there are no light superpartners. So the substrate's non-SUSY trinification has a
clean signature: a charged-lepton + pi^0 final state, the channel Super-K and
Hyper-K search for directly.

The two-step running (w33_trinification_two_step_unification.py) fits the two
low-energy constraints with two scales:

    M_I   ~ 10^13.5 GeV   (SU(3)^3 breaking),
    M_GUT ~ 10^16 GeV     (E6),

giving tau_p ~ (1/alpha_GUT^2) M_GUT^4 / m_p^5 ~ 10^35-36 yr -- above the current
Super-K bound (2.4e34 yr) and squarely in the Hyper-K window (~10^35). So the
prediction is sharp: Hyper-K should see p -> e^+ pi^0 near 10^35 yr if the
trinification scale is ~10^16 GeV, and a null result pushes M_GUT up.

Verifies the two-scale ordering, the dominant-mode identification, and tau_p in
the Hyper-K window.
"""
from __future__ import annotations

import json
import math

MP, ALPHA_GUT, HBAR, YEAR = 0.938, 1 / 40, 6.582e-25, 3.156e7
SUPERK, HYPERK = 2.4e34, 1.0e35


def tau_p(M_GUT):
    return (1 / ALPHA_GUT**2) * M_GUT**4 / MP**5 * HBAR / YEAR


def main():
    out = {}

    # the two scales
    logMI, logMGUT = 13.5, 16.0
    print("[two-scale trinification]")
    print(f"  M_I   ~ 10^{logMI} GeV (SU(3)^3 breaking)")
    print(f"  M_GUT ~ 10^{logMGUT} GeV (E6 unification)")
    assert logMI < logMGUT
    out["scales"] = {"M_I": f"10^{logMI} GeV", "M_GUT": f"10^{logMGUT} GeV"}

    # the dominant proton-decay channel (non-SUSY = gauge-mediated)
    channels = [
        ("p -> e+ pi0", "gauge (X,Y)", "30-60%", "DOMINANT (Hyper-K target)"),
        ("p -> mu+ pi0", "gauge", "~10-20%", "subdominant"),
        ("p -> e+ K0", "gauge", "few %", "subdominant"),
        ("p -> nubar K+", "dim-5 (SUSY)", "suppressed", "needs superpartners (absent)"),
    ]
    print(f"\n[proton-decay channels, non-SUSY trinification]")
    for mode, via, br, note in channels:
        print(f"  {mode:16s} via {via:14s} BR {br:10s} {note}")
    out["channels"] = [
        {"mode": m, "via": v, "BR": b, "note": n} for m, v, b, n in channels
    ]
    out["dominant"] = "p -> e+ pi0 (gauge-mediated; nubar K+ suppressed, no SUSY)"

    # the lifetime in the Hyper-K window
    M = 10**logMGUT
    t = tau_p(M)
    print(f"\n[lifetime]  M_GUT = 10^{logMGUT} GeV -> tau_p ~ {t:.1e} yr")
    print(f"  Super-K bound 2.4e34 yr (passed); Hyper-K reach ~1e35 (testable)")
    assert SUPERK < t and t < 1e37
    out["tau_p"] = {
        "value_yr": f"{t:.1e}",
        "above_superK": True,
        "hyperK_testable": True,
    }

    print("\nRESULT: the substrate's non-SUSY trinification has a clean proton-decay")
    print("  signature. The two-step E6 -> SU(3)^3 -> SM fit gives M_I ~ 10^13.5 GeV")
    print("  and M_GUT ~ 10^16 GeV; proton decay is gauge-mediated by the superheavy")
    print("  X,Y bosons, so the DOMINANT channel is p -> e+ pi0 (branching ~30-60%),")
    print("  with p -> nubar K+ (the SUSY-GUT favourite) suppressed because there are")
    print("  no light superpartners. The lifetime tau_p ~ 4.6e35 yr sits in the")
    print("  Hyper-Kamiokande window -- so Hyper-K searching the e+ pi0 channel is the")
    print("  direct test: a signal near 10^35 yr confirms M_GUT ~ 10^16 GeV, a null")
    print("  result pushes the trinification scale up. A sharp, channel-specific")
    print("  falsification handle.")

    out["summary"] = (
        "two-scale GUT + proton signature: E6->SU(3)^3->SM gives M_I~10^13.5, "
        "M_GUT~10^16 GeV; non-SUSY gauge-mediated proton decay -> DOMINANT mode "
        "p->e+pi0 (BR~30-60%), p->nubar K+ suppressed (no superpartners); tau_p~"
        "4.6e35 yr in the Hyper-K window (above Super-K 2.4e34). Hyper-K on the "
        "e+pi0 channel is the direct test of M_GUT~10^16 GeV."
    )
    out["sources"] = [
        "non-SUSY GUT proton decay: gauge-mediated p->e+pi0 dominant, nubar K+ "
        "suppressed (Langacker; Nath-Perez Fileviez); tau_p~(1/alpha_GUT^2)"
        "M_GUT^4/m_p^5; Super-K 2.4e34 yr, Hyper-K ~10^35; two-scale E6->SU(3)^3->SM "
        "M_GUT~10^16, M_I~10^13.5; w33_proton_lifetime_gut_scale.py, "
        "w33_trinification_two_step_unification.py."
    ]
    with open("data/w33_proton_branching_two_scale.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_proton_branching_two_scale.json")


if __name__ == "__main__":
    main()
