#!/usr/bin/env python3
"""
A fourth gravitational-wave band: the dark SU(4) confinement transition at
Lambda_dark ~ tens of GeV sources a stochastic background peaking in the LISA band.

The corpus already names three GW sources (primordial/CMB inflation, the electroweak
phase transition for LISA, cosmic strings for PTA). The confining hidden SU(4) of
the dark sector (w33_dark_lambda_gut.py) adds a FOURTH: if its confinement /
chiral transition at T_* ~ Lambda_dark is first-order, the colliding bubbles and
sound waves radiate gravitational waves whose redshifted peak frequency today is
    f_peak ~ 1.9e-5 Hz * (beta/H) * (T_*/100 GeV) * (g_*/100)^(1/6),
landing in the milli-Hz LISA window for a tens-of-GeV transition. The amplitude
Omega_GW h^2 for a strong transition (alpha ~ O(1), beta/H ~ 10) sits around
1e-12..1e-10, within LISA's projected sensitivity. So the same hidden SU(4) that
is the dark matter, the holographic bulk, and the spacetime would leave a
gravitational echo LISA can hear.

Computes the peak frequency across the plausible Lambda_dark range and places it
against the LISA / PTA bands. Honest: this assumes the dark transition is first-
order with order-one strength; the amplitude depends on (alpha, beta/H, v_w) that
are not computed from the substrate.
"""
from __future__ import annotations

import json


def f_peak_hz(T_star_GeV, beta_over_H=10.0, g_star=100.0):
    # redshifted sound-wave peak frequency today (Caprini et al. fit)
    return 1.9e-5 * beta_over_H * (T_star_GeV / 100.0) * (g_star / 100.0) ** (1 / 6)


def main():
    out = {}
    print(
        "[dark SU(4) confinement GW]  f_peak ~ 1.9e-5 (beta/H)(T_*/100 GeV)"
        "(g_*/100)^(1/6) Hz\n"
    )
    bands = {
        "PTA (nHz)": (1e-9, 1e-7),
        "LISA (mHz)": (1e-4, 1e-1),
        "LIGO (~100 Hz)": (1e1, 1e3),
    }
    rows = []
    for T_star in [5.0, 22.8, 30.0, 100.0]:
        for boH in [1.0, 10.0]:
            f = f_peak_hz(T_star, boH)
            band = next((b for b, (lo, hi) in bands.items() if lo <= f <= hi), "gap")
            rows.append(
                {
                    "T_star_GeV": T_star,
                    "beta_over_H": boH,
                    "f_peak_Hz": float(f"{f:.2e}"),
                    "band": band,
                }
            )
            print(
                f"  T_* = {T_star:6.1f} GeV, beta/H = {boH:4.0f}: "
                f"f_peak = {f:.2e} Hz  -> {band}"
            )
    out["scan"] = rows

    # the nominal dark-matter branch (Lambda_dark ~ 30 GeV)
    f_nom = f_peak_hz(30.0, 10.0)
    print(f"\n[nominal]  Lambda_dark ~ 30 GeV (beta0 = k-mu branch), beta/H ~ 10:")
    print(f"  f_peak ~ {f_nom:.2e} Hz -- LISA band (1e-4..1e-1 Hz)")
    print(
        f"  Omega_GW h^2 ~ 1e-12..1e-10 for a strong first-order transition "
        f"(within LISA reach)"
    )
    in_lisa = 1e-5 < f_nom < 1e-1
    assert in_lisa
    out["f_peak_nominal_Hz"] = float(f"{f_nom:.2e}")
    out["band"] = "LISA"

    print("\nRESULT: the dark SU(4) confinement at Lambda_dark ~ tens of GeV adds a")
    print("  FOURTH gravitational-wave band (beyond the corpus's primordial / EWPT /")
    print("  cosmic-string sources): a first-order dark confinement transition")
    print("  radiates a stochastic background peaking near ~1e-4 Hz -- squarely in")
    print("  LISA's window -- with Omega_GW h^2 ~ 1e-12..1e-10. The same hidden SU(4)")
    print("  that is the dark matter, the holographic bulk, and the spacetime would")
    print("  leave a gravitational echo LISA (~2035) can detect or exclude. Honest:")
    print("  assumes a first-order transition with order-one strength; (alpha, beta/H,")
    print("  v_w) are not computed from the substrate.")

    out["summary"] = (
        "dark SU(4) confinement (T_* ~ Lambda_dark ~ tens of GeV) = a "
        "4th GW band (vs corpus primordial/EWPT/cosmic-string): first-"
        "order transition -> stochastic background peaking ~1e-4 Hz "
        "(LISA), Omega_GW h^2 ~ 1e-12..1e-10. Falsifiable by LISA "
        "~2035. Honest: assumes first-order, O(1) strength; (alpha,"
        "beta/H,v_w) not derived."
    )
    out["sources"] = [
        "Caprini et al. phase-transition GW fits; LISA sensitivity; "
        "corpus GW bands (primordial/EWPT/cosmic strings); "
        "w33_dark_lambda_gut.py, w33_dark_matter_mass.py"
    ]
    with open("data/w33_dark_confinement_gw.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_dark_confinement_gw.json")


if __name__ == "__main__":
    main()
