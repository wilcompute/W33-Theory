#!/usr/bin/env python3
"""
Is y1 actually free? Pinning the Dirac top to the atmospheric scale gives y1 ~ 0.017, a factor
~2 from e^{-Phi_6/2}. Pass 20 left the lightest neutrino's Dirac Yukawa y1 = e^{-Phi_6/2} = 0.030
as the tower's one free input. This witness tests whether it is really free, by a SECOND,
data-anchored route: fix the Dirac texture ratio (up-type-like 9:2:1, the Pillar-65/68 SVD), pin
the HEAVIEST Dirac eigenvalue y3 by matching the atmospheric neutrino mass m_nu3 = sqrt(Dm^2_31)
to the type-I seesaw m_nu3 = y3^2 v^2/M_R with the substrate scale M_R = M_Pl e^{-Phi_3} (the
scalaron/N_1, Pass 13), and read off y1 = y3/9 from the texture. The result: y1 ~ 0.017,
m1 = m_nu3/81 ~ 0.6 meV -- and this AGREES with the a priori half-GUT-exponent value
e^{-Phi_6/2} = 0.030 to a factor ~2. So y1 is NOT an independent free parameter: two routes (the
half-GUT-exponent guess, and atmospheric-pinning + the substrate M_R + the texture ratio) land
on the same coupling within a factor ~2, trading the free input for the measured Dm^2_31. The
honest limitation: a SINGLE M_R over-predicts the neutrino hierarchy (81:4:1 from the 9:2:1
Dirac texture, vs the observed mild ~6:1), so the full spectrum needs the Majorana M_R texture
(the Pillar-68/69 cubic form) -- the residual freedom moves there, it is not eliminated. So this
is a PARTIAL closure: y1 is pinned (to a factor ~2) by data + structure, but the spectrum's
detail still rests on the Majorana texture.

This tests the Pass-20 residual: not "derive y1 from nothing" but "is y1 free, or fixed by the
texture + a measured scale?" -- and finds it fixed to a factor ~2, with the residual moving to
the Majorana sector.

THE TWO ROUTES TO y1.
  Route A (a priori, Pass 20): y1 = e^{-Phi_6/2} = 0.0302 (half the GUT exponent).
  Route B (data-anchored, here): the texture ratio 9:2:1 fixes y1 = y3/9; y3 is pinned by
    m_nu3 = sqrt(Dm^2_31) = 0.050 eV = y3^2 v^2/M_R with M_R = M_Pl e^{-Phi_3}; so
    y3 = sqrt(m_nu3 M_R)/v ~ 0.15, y1 = y3/9 ~ 0.017, m1 = y1^2 v^2/M_R = m_nu3/81 ~ 0.6 meV.
  They agree to a factor ~1.8 -- y1 is not independently free.

THE INVERSE CHECK. What M_R makes Route B give exactly y1 = e^{-Phi_6/2}? M_R = (9 y1)^2 v^2/
m_nu3 ~ 9e13 GeV, within a factor ~3 of M_Pl e^{-Phi_3} = 2.8e13 GeV. So the substrate scalaron
scale and the half-GUT-exponent Yukawa are mutually consistent to a factor ~3 -- the two
substrate inputs (M_R = M_Pl e^{-Phi_3}, y1 = e^{-Phi_6/2}) reproduce the atmospheric scale.

THE HONEST LIMITATION (the spectrum needs Majorana texture). A single M_R with the 9:2:1 Dirac
texture predicts the LIGHT spectrum m3:m2:m1 = y3^2:y2^2:y1^2 = 81:4:1, i.e. m3/m2 ~ 20, but the
observed ratio sqrt(Dm^2_31/Dm^2_21) = sqrt(33) ~ 5.7. So the simple seesaw over-hierarchises by
~3.5x; the observed mild hierarchy and large mixing require the Majorana M_R to be NON-degenerate
(the Pillar-68/69 cubic-form M_R, grade-0 degenerate + grade-1 lift). The residual freedom is
therefore the M_R texture, not y1 -- y1 is pinned, the spectrum detail is in the Majorana sector.

Honest scope: Route B uses a MEASURED input (Dm^2_31) and assumes the neutrino Dirac texture =
up-type 9:2:1 and a single M_R; under those, y1 ~ 0.017 agrees with e^{-Phi_6/2} = 0.030 to a
factor ~2 and m1 ~ 0.6-2 meV sits at the dark-energy floor. This does NOT achieve "zero residual
free numbers": the single-M_R spectrum fails the observed hierarchy, so the Majorana texture is
needed and carries the residual. The real content: y1 is fixed to a factor ~2 by data + the
substrate M_R + the texture ratio (two independent routes agree), and the leftover freedom is
the Majorana M_R texture the substrate supplies but this witness does not fully derive.

Verifies Route B y1 = y3/9 ~ 0.017 and its factor-~2 agreement with e^{-Phi_6/2}, m1 = m_nu3/81
~ 0.6 meV, the inverse-check M_R ~ 9e13 within ~3x of M_Pl e^{-Phi_3}, and the single-M_R
hierarchy failure (81:4:1 vs observed sqrt(33)) that forces the Majorana texture.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    Phi3, Phi6 = q * q + q + 1, q * q - q + 1  # 13, 7
    M_Pl = 1.22e19  # GeV
    v = 246.0  # GeV
    M_R = M_Pl * math.exp(-Phi3)  # scalaron/N_1 ~ 2.8e13 GeV
    ratio = (9.0, 2.0, 1.0)  # up-type-like Dirac texture (Pillar 65/68 SVD)

    # neutrino scales (measured)
    Dm2_31 = 2.5e-3  # eV^2 (atmospheric)
    Dm2_21 = 7.5e-5  # eV^2 (solar)
    m_nu3 = math.sqrt(Dm2_31) * 1e-9  # GeV (0.050 eV)
    print("== is y1 free? a second, data-anchored route ==")

    # Route A: a priori
    y1_A = math.exp(-Phi6 / 2)
    print(
        f"  Route A (a priori):   y1 = e^-Phi6/2 = {y1_A:.4f}  (half the GUT exponent)"
    )

    # Route B: atmospheric pinning
    y3 = math.sqrt(m_nu3 * M_R) / v
    y1_B = y3 / ratio[0]
    m1_B = y1_B**2 * v**2 / M_R * 1e12  # meV
    print(
        f"  Route B (atm-pinned): y3 = sqrt(m_nu3 M_R)/v = {y3:.3f} (M_R = M_Pl e^-Phi3 = {M_R:.1e} GeV)"
    )
    print(
        f"                        y1 = y3/9 = {y1_B:.4f};  m1 = m_nu3/81 = {m1_B:.2f} meV"
    )
    agree = max(y1_A, y1_B) / min(y1_A, y1_B)
    print(
        f"  -> the two routes agree to a factor {agree:.2f} -- y1 is NOT independently free"
    )
    out["two_routes"] = {
        "y1_a_priori": round(y1_A, 4),
        "y1_atm_pinned": round(y1_B, 4),
        "y3": round(y3, 3),
        "M_R_GeV": f"{M_R:.2e}",
        "m1_meV": round(m1_B, 2),
        "agreement_factor": round(agree, 2),
    }
    assert agree < 2.5  # within a factor ~2

    # inverse check: what M_R gives exactly y1 = e^-Phi6/2?
    M_R_needed = (ratio[0] * y1_A) ** 2 * v**2 / m_nu3
    fac = M_R_needed / M_R
    print(
        f"\n[inverse check]  M_R for y1 = e^-Phi6/2 exactly: {M_R_needed:.1e} GeV "
        f"= {fac:.1f}x M_Pl e^-Phi3"
    )
    print(
        "  -> the scalaron scale M_R = M_Pl e^-Phi3 and y1 = e^-Phi6/2 reproduce the "
        "atmospheric scale to a factor ~3"
    )
    out["inverse_check"] = {
        "M_R_needed_GeV": f"{M_R_needed:.2e}",
        "factor_vs_scalaron": round(fac, 1),
        "reading": "M_R = M_Pl e^-Phi3 and y1 = e^-Phi6/2 are mutually consistent to ~3x",
    }

    # the honest limitation: single-M_R over-hierarchises
    spectrum = tuple(rr**2 for rr in ratio)  # 81:4:1
    obs_ratio = math.sqrt(Dm2_31 / Dm2_21)
    pred_ratio = spectrum[0] / spectrum[1]
    print(f"\n[honest limitation -- single M_R over-hierarchises]")
    print(
        f"  9:2:1 Dirac + single M_R -> light spectrum m3:m2:m1 = {spectrum[0]:.0f}:{spectrum[1]:.0f}:{spectrum[2]:.0f}"
    )
    print(
        f"  predicted m3/m2 = {pred_ratio:.0f} vs observed sqrt(Dm31/Dm21) = {obs_ratio:.1f} "
        f"({pred_ratio/obs_ratio:.1f}x too hierarchical)"
    )
    print(
        "  -> the observed mild hierarchy + large mixing need the Majorana M_R texture"
    )
    print(
        "     (Pillar 68/69 cubic form); the residual freedom moves to the Majorana sector"
    )
    out["limitation"] = {
        "single_MR_spectrum": "81:4:1",
        "pred_m3_over_m2": round(pred_ratio, 0),
        "obs_m3_over_m2": round(obs_ratio, 1),
        "over_hierarchy_factor": round(pred_ratio / obs_ratio, 1),
        "conclusion": "single M_R fails the spectrum; Majorana M_R texture needed (residual moves there)",
    }

    print(
        "\nRESULT: y1 is not independently free -- two routes pin it to a factor ~2. Pass 20"
    )
    print(
        "  left the lightest neutrino's Dirac Yukawa y1 = e^-Phi_6/2 = 0.030 as the tower's one"
    )
    print(
        "  free input. A second, DATA-ANCHORED route fixes it: take the Dirac texture ratio"
    )
    print(
        "  9:2:1 (the Pillar-65/68 SVD), pin the heaviest Dirac eigenvalue y3 by matching the"
    )
    print(
        "  atmospheric mass m_nu3 = sqrt(Dm^2_31) = 0.050 eV to the type-I seesaw y3^2 v^2/M_R"
    )
    print(
        "  with the substrate scale M_R = M_Pl e^-Phi_3 (the scalaron), and read y1 = y3/9 ="
    )
    print(
        "  0.017, m1 = m_nu3/81 = 0.6 meV. This agrees with the a priori half-GUT-exponent"
    )
    print(
        "  value e^-Phi_6/2 = 0.030 to a factor ~1.8 -- two independent routes (a half of the"
    )
    print(
        "  GUT exponent; atmospheric-pinning + the substrate M_R + the texture ratio) on the"
    )
    print(
        "  same coupling. So y1 is fixed to a factor ~2 by data + structure, trading the free"
    )
    print(
        "  input for the measured Dm^2_31; equivalently M_R = M_Pl e^-Phi_3 and y1 = e^-Phi_6/2"
    )
    print(
        "  reproduce the atmospheric scale to ~3x. HONEST: this is a PARTIAL closure, not zero"
    )
    print(
        "  residual -- a single M_R with the 9:2:1 Dirac texture predicts m3:m2:m1 = 81:4:1"
    )
    print(
        "  (m3/m2 ~ 20) vs the observed mild sqrt(33) ~ 5.7, so the spectrum needs the Majorana"
    )
    print(
        "  M_R texture (the Pillar-68/69 cubic form) and the residual freedom moves to the"
    )
    print(
        "  Majorana sector. The content: y1 is pinned to a factor ~2 by two routes; the leftover"
    )
    print(
        "  freedom is the Majorana texture the substrate supplies but this does not derive."
    )

    out["summary"] = (
        "is y1 free? a second, data-anchored route pins it to a factor ~2. Pass 20 left the "
        "lightest neutrino Dirac Yukawa y1 = e^-Phi6/2 = 0.030 as the tower's one free input. "
        "Route B: take the Dirac texture ratio 9:2:1 (Pillar 65/68 SVD), pin the heaviest "
        "eigenvalue y3 by matching m_nu3 = sqrt(Dm^2_31) = 0.050 eV to the seesaw y3^2 v^2/M_R "
        "with M_R = M_Pl e^-Phi3 (scalaron), read y1 = y3/9 = 0.017, m1 = m_nu3/81 = 0.6 meV. "
        "This agrees with the a priori e^-Phi6/2 = 0.030 to a factor ~1.8 -- two independent "
        "routes on the same coupling, so y1 is NOT independently free; it trades for the "
        "measured Dm^2_31. Inverse: M_R = M_Pl e^-Phi3 and y1 = e^-Phi6/2 reproduce the "
        "atmospheric scale to ~3x. HONEST: PARTIAL closure -- a single M_R + 9:2:1 Dirac gives "
        "light spectrum 81:4:1 (m3/m2 ~ 20) vs observed sqrt(33) ~ 5.7, so the Majorana M_R "
        "texture (Pillar 68/69 cubic form) is needed and the residual freedom moves there. y1 "
        "is pinned to a factor ~2 by data + the substrate M_R + texture; the leftover is the "
        "Majorana texture, not eliminated."
    )
    out["sources"] = [
        "Pass-20 residual y1 = e^-Phi6/2 (w33_neutrino_dirac_yukawa.py); Dirac texture 9:2:1 "
        "(Pillar 65/68, w33_yukawa_optimization.py / w33_mass_texture.py); M_R = M_Pl e^-Phi3 "
        "(w33_scalaron_is_rhn.py); cubic-form M_R (Pillar 68/69, w33_majorana_cubic_form.py); "
        "Dm^2_31 = 2.5e-3 eV^2, Dm^2_21 = 7.5e-5 eV^2 (global fits)."
    ]
    with open("data/w33_yukawa_closure.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_yukawa_closure.json")


if __name__ == "__main__":
    main()
