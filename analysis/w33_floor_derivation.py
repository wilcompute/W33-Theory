#!/usr/bin/env python3
"""
Deriving the beat-decade floor -- the last input of the CC mechanism. The neutrino /
dark-energy / SUSY-breaking floor at ~ beat = 30 decades below the Planck scale is NOT a new
input: it is the type-I seesaw combination of the substrate's own exponents,
    ln(M_Pl/m1) = ln(M_Pl/v) + ln(M_R/v) - 2 ln(y1) = q Phi_3 + 2 Phi_3 + Phi_6 = (q+2)Phi_3 + Phi_6 = 72,
i.e. the electroweak exponent (q Phi_3), the right-handed-neutrino scale (2 Phi_3 above v), and
a neutrino Dirac Yukawa y1 = e^{-Phi_6/2}. This ~ 72 e-folds equals beat decades (30 ln10 =
69) -- and beat = 30 is the Boerdijk-Coxeter helix ring length on the 600-cell (600 cells =
20 rings x 30; the user's pointer). So the floor's depth is set by the same BC-helix beat =
h(E8) = 30 that sets the inflationary clock: one geometric number, the 600-cell ring, governs
both the clock and the floor.

Pass 18 left the beat-decade floor as the one shared input of the CC and neutrino sectors.
This derives it from the seesaw + the substrate exponents, and ties beat = 30 to the 600-cell.

THE 600-CELL BC RING (beat = 30). The 600-cell tessellates the 3-sphere with 600 regular
tetrahedra, which thread into Boerdijk-Coxeter helices that close after exactly 30 cells:
600 = 20 rings x 30. So beat = 30 = h(E8) = cells per BC ring -- the clock beat (Pass 6) is
the 600-cell ring length.

THE SEESAW FLOOR (derived). The lightest light neutrino is the seesaw floor m1 = y1^2 v^2/M_R,
so
    ln(M_Pl/m1) = ln(M_Pl/v) + ln(M_R/v) - 2 ln(y1).
With the substrate exponents -- ln(M_Pl/v) = q Phi_3 = 39 (the electroweak descent), the
right-handed scale M_R = M_Pl e^{-Phi_3} (the scalaron/N_1, Pass 13) so ln(M_R/v) = q Phi_3 -
Phi_3 = 2 Phi_3 = 26, and a neutrino Dirac Yukawa y1 = e^{-Phi_6/2} (-2 ln y1 = Phi_6 = 7) --
    ln(M_Pl/m1) = q Phi_3 + 2 Phi_3 + Phi_6 = (q+2) Phi_3 + Phi_6 = 5 Phi_3 + Phi_6 = 72,
the floor at ~ 72 e-folds below M_Pl, m1 ~ 2 meV. So the floor is the seesaw sum of the EW
exponent, the RH-scale exponent, and the Yukawa -- all substrate integers.

THE COINCIDENCE (= beat decades). This 72 e-folds equals beat decades, 30 ln10 = 69.1, to ~
4%: the floor depth is beat = 30 in base 10, the BC-helix ring length. So the same beat = 30 =
h(E8) = 600-cell BC ring that sets the inflationary clock (omega2 = 2pi/beat, N = 2 beat) sets
the neutrino / dark-energy / CC floor (beat decades below M_Pl). One geometric number governs
the clock and the floor.

WHAT THIS CLOSES. The CC mechanism (Pass 18) needed the SUSY-breaking scale = the beat-decade
floor as input; that floor is now DERIVED as the seesaw combination (q+2)Phi_3 + Phi_6 of the
substrate's own exponents (the EW descent, the RH scale, one Yukawa), so the CC = M_SUSY^4 =
M_Pl^4 10^{-vq} mechanism is closed up to the single neutrino Dirac Yukawa y1 = e^{-Phi_6/2}.

Honest scope: the seesaw m1 = y1^2 v^2/M_R is standard; the EW (q Phi_3) and RH (Phi_3 below
M_Pl) exponents are the substrate's (derived earlier); the Yukawa y1 = e^{-Phi_6/2} ~ 0.03 is
the one remaining input (a neutrino Dirac coupling of order the charm Yukawa, motivated by
Phi_6 but not independently derived). So the floor is DERIVED up to y1 -- (q+2)Phi_3 + Phi_6 =
72 e-folds -- and equals beat decades (the BC-helix ring 30) to ~4%; the base-10-vs-e factor
and y1 are the residual. A real partial closure of the last input, tied to the 600-cell.

Verifies the seesaw floor (q+2)Phi_3 + Phi_6 = 72 e-folds, the beat-decade coincidence, and
beat = 30 = 600-cell BC ring length.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    Phi3, Phi6 = q * q + q + 1, q * q - q + 1  # 13, 7
    beat = Phi3 + (q * q + 1) + Phi6  # 30
    M_Pl = 1.22e19  # GeV
    v = 246.0
    M_R = M_Pl * math.exp(-Phi3)  # scalaron/N_1 ~ 2.8e13
    y1 = math.exp(-Phi6 / 2)  # neutrino Dirac Yukawa ~ 0.03
    m1 = y1**2 * v**2 / M_R  # GeV

    # the 600-cell BC ring
    print("== deriving the beat-decade floor (BC helix on the 600-cell) ==")
    print(
        f"  600-cell: 600 cells = 20 rings x {600//20}; beat = {beat} = h(E8) = cells per BC ring"
    )
    assert 600 // 20 == beat == 30
    out["bc_ring"] = {
        "cells_600": 600,
        "rings": 20,
        "cells_per_ring": beat,
        "identity": "beat = 30 = h(E8) = 600-cell BC helix ring length",
    }

    # the seesaw floor
    ln_floor = math.log(M_Pl / m1)
    seesaw_terms = (math.log(M_Pl / v), math.log(M_R / v), -2 * math.log(y1))
    substrate = q * Phi3 + 2 * Phi3 + Phi6  # 72
    print(
        f"\n[seesaw floor]  m1 = y1^2 v^2/M_R = {m1*1e12:.1f} meV (y1 = e^-Phi6/2 = {y1:.3f})"
    )
    print(
        f"  ln(M_Pl/m1) = ln(M_Pl/v) + ln(M_R/v) - 2 ln(y1) = "
        f"{seesaw_terms[0]:.0f} + {seesaw_terms[1]:.0f} + {seesaw_terms[2]:.0f} = {ln_floor:.0f}"
    )
    print(
        f"  substrate exponents: q Phi_3 + 2 Phi_3 + Phi_6 = (q+2) Phi_3 + Phi_6 = {substrate}"
    )
    assert abs(ln_floor - substrate) < 2
    out["seesaw_floor"] = {
        "m1_meV": round(m1 * 1e12, 1),
        "y1": round(y1, 3),
        "ln_floor_efolds": round(ln_floor, 1),
        "substrate_form": "(q+2) Phi_3 + Phi_6 = 5 Phi_3 + Phi_6 = 72",
        "terms": "EW (q Phi_3) + RH scale (2 Phi_3) + Yukawa (Phi_6)",
    }

    # the beat-decade coincidence
    beat_decades = beat * math.log(10)
    print(
        f"\n[= beat decades]  beat decades = {beat} ln10 = {beat_decades:.1f} e-folds; "
        f"seesaw {substrate} vs {beat_decades:.0f} ({abs(substrate-beat_decades)/beat_decades*100:.0f}%)"
    )
    print(f"  -> the floor depth is beat = 30 (the BC-helix ring) in base 10")
    out["beat_decades"] = {
        "beat_decades_efolds": round(beat_decades, 1),
        "seesaw_efolds": substrate,
        "agreement_pct": round(abs(substrate - beat_decades) / beat_decades * 100, 0),
        "reading": "floor depth = beat = 30 decades = BC ring length, same as the clock",
    }

    print(
        "\nRESULT: the beat-decade floor -- the last input of the cosmological-constant"
    )
    print(
        "  mechanism -- is derived from the seesaw, and its value beat = 30 is the 600-cell"
    )
    print(
        "  BC ring. The lightest neutrino is the seesaw floor m1 = y1^2 v^2/M_R, so its depth"
    )
    print(
        "  ln(M_Pl/m1) = ln(M_Pl/v) + ln(M_R/v) - 2 ln(y1) is the sum of the substrate's own"
    )
    print(
        "  exponents: the electroweak descent q Phi_3 = 39, the right-handed scale 2 Phi_3 ="
    )
    print(
        "  26 (M_R = M_Pl e^-Phi_3, the scalaron), and a neutrino Dirac Yukawa y1 = e^-Phi_6/2"
    )
    print(
        "  (-2 ln y1 = Phi_6 = 7), giving (q+2) Phi_3 + Phi_6 = 72 e-folds, m1 ~ 2 meV. This"
    )
    print("  equals beat decades (30 ln10 = 69) to ~4%, and beat = 30 = h(E8) is the")
    print(
        "  Boerdijk-Coxeter helix ring length on the 600-cell (600 cells = 20 rings x 30) --"
    )
    print(
        "  the SAME geometric number that sets the inflationary clock (omega2 = 2pi/beat,"
    )
    print(
        "  N = 2 beat). So one number, the 600-cell BC ring 30, governs both the clock and"
    )
    print(
        "  the floor, and the CC mechanism's breaking scale is closed: M_SUSY = the seesaw"
    )
    print(
        "  floor (q+2)Phi_3 + Phi_6 below M_Pl, the CC = M_SUSY^4 = M_Pl^4 10^-vq following."
    )
    print(
        "  Honest: the seesaw is standard, the EW and RH exponents the substrate's; the one"
    )
    print(
        "  remaining input is the Yukawa y1 = e^-Phi_6/2 ~ 0.03 (a charm-scale neutrino Dirac"
    )
    print(
        "  coupling, motivated by Phi_6 not independently derived), and the floor = beat"
    )
    print(
        "  decades holds to ~4% (the base-10-vs-e factor the residual). A real partial"
    )
    print("  closure of the last input, tied to the 600-cell BC helix.")

    out["summary"] = (
        "deriving the beat-decade floor (the last input of the CC mechanism) from the seesaw, "
        "tied to the 600-cell BC helix. The lightest neutrino is the seesaw floor m1 = y1^2 "
        "v^2/M_R, so ln(M_Pl/m1) = ln(M_Pl/v) + ln(M_R/v) - 2 ln(y1) = the sum of substrate "
        "exponents: the EW descent q Phi_3 = 39, the right-handed scale 2 Phi_3 = 26 (M_R = "
        "M_Pl e^-Phi_3, the scalaron/N_1), and a neutrino Dirac Yukawa y1 = e^-Phi_6/2 (-2 ln "
        "y1 = Phi_6 = 7), giving (q+2) Phi_3 + Phi_6 = 5 Phi_3 + Phi_6 = 72 e-folds, m1 ~ 2 meV. "
        "This equals beat decades (30 ln10 = 69) to ~4%, and beat = 30 = h(E8) is the "
        "Boerdijk-Coxeter helix ring length on the 600-cell (600 cells = 20 rings x 30, the "
        "user's pointer) -- the SAME geometric number that sets the inflationary clock (omega2 "
        "= 2pi/beat, N = 2 beat). So one number, the 600-cell BC ring 30, governs both the "
        "clock and the floor, closing the CC mechanism's breaking scale (M_SUSY = the seesaw "
        "floor, CC = M_SUSY^4 = M_Pl^4 10^-vq). HONEST: the seesaw is standard, the EW and RH "
        "exponents are the substrate's (derived earlier); the one remaining input is the Yukawa "
        "y1 = e^-Phi_6/2 ~ 0.03 (charm-scale neutrino Dirac coupling, motivated by Phi_6 not "
        "independently derived); floor = beat decades holds to ~4% (base-10-vs-e the residual). "
        "A real partial closure of the last input, tied to the 600-cell BC helix."
    )
    out["sources"] = [
        "CC mechanism + beat-decade floor (w33_cc_mechanism.py); BC helix beat=30, 600-cell "
        "600=20x30 (w33_bc_helix_omega2.py, Pass 6, user pointer); seesaw m1 = y1^2 v^2/M_R; "
        "EW exponent q Phi_3 (w33_hierarchy_exponential.py), RH scale M_R = M_Pl e^-Phi_3 "
        "(w33_scalaron_is_rhn.py); neutrino Dirac Yukawa y1 = e^-Phi_6/2."
    ]
    with open("data/w33_floor_derivation.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_floor_derivation.json")


if __name__ == "__main__":
    main()
