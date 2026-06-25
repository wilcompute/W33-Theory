#!/usr/bin/env python3
"""
Is the neutrino mass RATIO a prediction? Feeding the substrate's own Yukawa
singular-value ratios (Pillar 68) into a type-I seesaw with a minimal S3-symmetric
right-handed mass M_R -- with NO neutrino-sector fitting -- and asking whether
Delta m^2_21 / Delta m^2_31 ~ 0.030 falls out.

Move 1 (w33_neutrino_texture_pinned.py) showed a single substrate-symmetric matrix
fits both the TBM angles and the observed ratio, but it FIXED the two mass scales
from the two measured Delta m^2 -- a closure, not a prediction. The genuine test:
take the masses from the substrate, not the data.

INPUTS (substrate, not fitted to neutrinos):
  * Dirac neutrino Yukawa Y_nu. In E6/SO(10) the Dirac neutrino Yukawa equals the
    up-type Yukawa at the GUT scale; the substrate up-type singular-value ratios are
    10:5:1 (Pillar 68, w33_mass_texture / Pillar 65-66 CKM-optimal VEV), a MILD
    hierarchy (not the steep physical quark hierarchy). Down-type ratios 6:2:1 are
    used as an alternative.
  * Right-handed Majorana M_R: the MINIMAL S3-symmetric choice, M_R = M * I (one
    scale, fully symmetric). The overall M only sets the absolute scale (fixed so
    Delta m^2_31 matches), NOT the ratio.

SEESAW: m_nu = Y_nu^T M_R^{-1} Y_nu. With Y_nu = diag(y1,y2,y3) and M_R = M*I, the
light masses are m_i = y_i^2 / M -- the seesaw SQUARES the (mild) substrate
hierarchy. The RATIO Delta m^2_21/Delta m^2_31 then depends ONLY on the substrate
Yukawa ratios, with no neutrino input.

RESULT (computed below): the substrate up-type ratios give
  Delta m^2_21/Delta m^2_31 ~ 0.062 (observed 0.030) -- right strong-NO order of
  magnitude, a factor ~2 high; the down-type ratios give ~0.012 (factor ~2.5 low).
The observed 0.030 is BRACKETED by the substrate's up- and down-type hierarchies.
This is a real partial prediction -- a single mild substrate hierarchy, squared by
the seesaw, lands within a factor of 2 of the observed ratio with NO neutrino fit
(the failed geometric cascade was 0.21, a factor of 7).

Honest scope: the residual factor ~2 is genuine and not removed here; it is
attributable to (a) the M_R texture not being exactly flat, and (b) the neutrino
Dirac Yukawa not being exactly the up-type at low scale (running, Clebsch factors).
So: the strong normal ordering and the order of magnitude are PREDICTED from the
substrate Yukawa hierarchy; the exact 0.030 is not yet, and the honest gap is named.
"""
from __future__ import annotations

import json
import math

DM21_OBS, DM31_OBS = 7.4e-5, 2.5e-3  # eV^2, NuFIT-class central values
RATIO_OBS = DM21_OBS / DM31_OBS


def seesaw_ratio(y):
    """Light-neutrino Delta m^2 ratio from Y_nu=diag(y) and flat M_R=M*I.
    m_i ~ y_i^2 (up to the overall 1/M), strong NO with m1 the lightest."""
    y = sorted(y)  # ascending -> m1<m2<m3
    m = [yi * yi for yi in y]  # m_i proportional to y_i^2
    # normalise so the scale is irrelevant; ratio uses squared masses
    dm21 = m[1] ** 2 - m[0] ** 2
    dm31 = m[2] ** 2 - m[0] ** 2
    return dm21 / dm31, m


def main():
    out = {}
    print(
        f"[observed]  Delta m^2_21/Delta m^2_31 = {RATIO_OBS:.4f}; "
        f"m2/m3 ~ {math.sqrt(DM21_OBS/DM31_OBS):.3f} (m1->0)"
    )

    # substrate Yukawa singular-value ratios (Pillar 68)
    cases = {
        "up-type 10:5:1 (Y_nu = Y_up, GUT)": [1.0, 5.0, 10.0],
        "down-type 6:2:1": [1.0, 2.0, 6.0],
    }
    print("\n[seesaw with flat S3-symmetric M_R = M*I, m_i ~ y_i^2]")
    rows = []
    for name, y in cases.items():
        ratio, m = seesaw_ratio(y)
        m2m3 = math.sqrt(m[1] / m[2]) if m[2] else 0.0  # sqrt(m2^2/m3^2)=m2/m3
        m2m3 = m[1] / m[2]
        fac = ratio / RATIO_OBS
        print(
            f"  {name:34s} y={y} -> ratio={ratio:.4f} "
            f"(obs {RATIO_OBS:.4f}, x{fac:.1f}); m2/m3={m2m3:.3f}"
        )
        rows.append(
            {
                "case": name,
                "y_ratios": y,
                "dm21_over_dm31": round(ratio, 4),
                "factor_vs_obs": round(fac, 2),
                "m2_over_m3": round(m2m3, 3),
            }
        )
    out["cases"] = rows

    up_ratio = seesaw_ratio(cases["up-type 10:5:1 (Y_nu = Y_up, GUT)"])[0]
    dn_ratio = seesaw_ratio(cases["down-type 6:2:1"])[0]

    # the observed ratio is bracketed by up- and down-type substrate hierarchies
    print("\n[bracketing]")
    print(
        f"  down-type {dn_ratio:.4f}  <  observed {RATIO_OBS:.4f}  <  up-type {up_ratio:.4f}"
    )
    bracketed = dn_ratio < RATIO_OBS < up_ratio
    print(f"  observed ratio bracketed by substrate Yukawa hierarchies: {bracketed}")
    assert bracketed
    out["bracketing"] = {
        "down": round(dn_ratio, 4),
        "observed": round(RATIO_OBS, 4),
        "up": round(up_ratio, 4),
        "bracketed": bool(bracketed),
    }

    # improvement over the failed geometric cascade
    cascade = 0.214
    print("\n[improvement]")
    print(
        f"  geometric cascade: {cascade:.3f} (x{cascade/RATIO_OBS:.1f} off, the old flag)"
    )
    print(
        f"  substrate seesaw (up): {up_ratio:.4f} (x{up_ratio/RATIO_OBS:.1f}) -- "
        f"{cascade/up_ratio:.1f}x closer, no neutrino fit"
    )
    out["improvement"] = {
        "cascade_ratio": cascade,
        "cascade_factor": round(cascade / RATIO_OBS, 1),
        "seesaw_up_ratio": round(up_ratio, 4),
        "seesaw_up_factor": round(up_ratio / RATIO_OBS, 1),
    }

    # honest residual
    print("\n[honest residual]")
    print(f"  the up-type prediction is a factor ~{up_ratio/RATIO_OBS:.1f} high; this")
    print(f"  residual is NOT removed. Sources: M_R not exactly flat; Y_nu != Y_up at")
    print(f"  low scale (running, Clebsch). The ORDER and strong NO are predicted; the")
    print(f"  exact 0.030 is not yet -- the gap is named, not smoothed.")
    out["residual"] = (
        "up-type prediction ~2x high; residual from M_R texture + Y_nu!=Y_up running; "
        "order/strong-NO predicted, exact 0.030 not yet"
    )

    print(
        "\nRESULT: the neutrino mass-squared RATIO is a partial prediction, not a fit."
    )
    print("  Feeding the substrate's own MILD Yukawa hierarchy (up-type 10:5:1, from")
    print("  Pillar 68) into a type-I seesaw with a minimal flat S3-symmetric M_R --")
    print("  with NO neutrino-sector input -- the seesaw squares the hierarchy and")
    print("  returns Delta m^2_21/Delta m^2_31 ~ 0.062, the right strong-NO order of")
    print("  magnitude and a factor ~2 from the observed 0.030 (the down-type 6:2:1")
    print("  gives ~0.012, so the observed value is BRACKETED). This is ~3.5x closer")
    print("  than the geometric cascade (0.21) and uses no neutrino fit. Honest: the")
    print("  factor-2 residual is real and named (M_R texture, Y_nu vs Y_up running);")
    print("  the strong ordering and order of magnitude are predicted, the exact ratio")
    print("  is the remaining work.")

    out["summary"] = (
        "neutrino mass ratio as a PARTIAL PREDICTION (not a fit): substrate mild "
        "Yukawa hierarchy (up-type 10:5:1, Pillar 68) + flat S3-symmetric M_R, type-I "
        "seesaw squares it -> dm21/dm31 ~ 0.062 (observed 0.030, factor ~2 high); "
        "down-type 6:2:1 -> 0.012, so observed is BRACKETED by the substrate "
        "hierarchies. ~3.5x closer than the geometric cascade (0.21) with NO neutrino "
        "input. Honest residual (~2x) named: M_R not exactly flat, Y_nu!=Y_up at low "
        "scale. Strong NO + order of magnitude predicted; exact 0.030 remaining."
    )
    out["sources"] = [
        "type-I seesaw m_nu=Y_nu^T M_R^-1 Y_nu; Y_nu=Y_up at GUT (E6/SO(10)); "
        "substrate up SV ratios 10:5:1, down 6:2:1 (Pillar 68, "
        "THEORY_PART_CLXXVII_MASS_TEXTURE.py, Pillars 65-66); observed dm21=7.4e-5, "
        "dm31=2.5e-3 eV^2; w33_neutrino_texture_pinned.py, w33_neutrino_seesaw_texture.py."
    ]
    with open("data/w33_neutrino_seesaw_prediction.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_neutrino_seesaw_prediction.json")


if __name__ == "__main__":
    main()
