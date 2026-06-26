#!/usr/bin/env python3
"""
The exponential the hierarchy needs is a substrate integer: ln(M_Pl/M_EW) = q*Phi_3 = 39.
Pass 7 left an honest negative -- the power-law kissing ladder gives only ~3x10^4, while
the Planck/electroweak ratio is ~10^17, and the gap needs ~39 e-folds of EXPONENTIAL
separation. The substrate supplies exactly that integer: q*Phi_3 = 3*13 = 39, so
M_Pl/M_EW = e^(q Phi_3) = e^39 ~ 8.7x10^16, putting the electroweak scale at M_Pl e^-39 ~
141 GeV -- squarely in the electroweak window -- and it splits the inflationary
N = 60 = q(Phi_3 + Phi_6) cleanly into Planck->EW (q Phi_3 = 39) and EW->end (q Phi_6 = 21).

w33_gravity_hierarchy.py identified the missing mechanism as an exponential e^N with N ~ 39.
Here we find that 39 is not arbitrary: it is q Phi_3, a substrate integer, and it slots
into the e-fold budget.

THE EXPONENTIAL HIERARCHY. The dimensionful Planck/electroweak ratio is, in the
substrate's e-fold currency,
    ln(M_Pl / M_EW) = q * Phi_3 = 3 * 13 = 39,
so M_Pl / M_EW = e^39 = 8.66x10^16 and the dimensionless gravitational strength at the EW
scale is (M_EW/M_Pl)^2 = e^(-2 q Phi_3) = e^-78. Inverting, the predicted electroweak
scale is M_EW = M_Pl e^(-39) = 1.22x10^19 GeV * e^-39 = 141 GeV -- between the W (80),
Z (91), Higgs (125) and top (173) masses, i.e. THE electroweak scale.

THE e-FOLD BUDGET CLOSES. Inflation runs N = 60 = 2*beat = 2(Phi_3+Phi_4+Phi_6) e-folds,
which also equals q(Phi_3 + Phi_6) = 3*20 = 60 (the 20 = 600/30 BC rings of the 600-cell).
This splits the inflationary window exactly:
    Planck -> EW :  q Phi_3 = 39 e-folds   (the gravity-to-electroweak descent),
    EW -> end    :  q Phi_6 = 21 e-folds,
    total        :  q(Phi_3 + Phi_6) = 60 = N.
So the electroweak scale sits q Phi_3 = 39 e-folds below the Planck scale, with q Phi_6 =
21 e-folds of inflation remaining -- the hierarchy is the gravity-shell descent measured
in the same e-fold clock as the CMB tilt.

Honest scope: this is an integer-level MATCH, not a forced derivation -- q Phi_3 = 39
reproduces the observed ln(M_Pl/M_EW) (which ranges 38.4 for M_EW = v=246 GeV to 39.3 for
M_EW ~ 100 GeV) to ~1-2%, and equivalently predicts M_EW ~ 141 GeV, but the substrate
does not independently derive WHY the EW scale sits exactly q Phi_3 e-folds down. What is
genuinely new and non-trivial: the missing exponent is a clean substrate integer q Phi_3,
it lands the EW scale in the right window, and it splits N = 60 = q Phi_3 + q Phi_6 into
two substrate integers. This converts Pass 7's open edge into a sharp, suggestive
identification (a postdiction), flagged as such.

Verifies q Phi_3 = 39, the predicted M_EW from e^-39, the ranges of ln(M_Pl/M_EW) over EW
scale choices, and the N = 60 = q Phi_3 + q Phi_6 e-fold split.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    Phi3, Phi4, Phi6 = q * q + q + 1, q * q + 1, q * q - q + 1  # 13,10,7
    beat = Phi3 + Phi4 + Phi6  # 30
    N = 2 * beat  # 60

    dN = q * Phi3  # 39 = the gravity->EW exponent
    print("== the exponential hierarchy: ln(M_Pl/M_EW) = q*Phi_3 = 39 ==")
    print(f"  q*Phi_3 = {q}*{Phi3} = {dN}")
    assert dN == 39

    M_Pl = 1.22e19  # GeV (full/Newtonian Planck mass; G = 1/M_Pl^2)
    ratio = math.exp(dN)
    M_EW_pred = M_Pl / ratio
    print(f"  M_Pl/M_EW = e^{dN} = {ratio:.3e}")
    print(
        f"  predicted M_EW = M_Pl e^-{dN} = {M_EW_pred:.0f} GeV  "
        f"(between W=80, Z=91, Higgs=125, top=173)"
    )
    out["exponent"] = {
        "dN": dN,
        "form": "q*Phi_3 = 3*13",
        "MPl_over_MEW": float(f"{ratio:.3e}"),
        "M_Pl_GeV": M_Pl,
        "M_EW_predicted_GeV": round(M_EW_pred, 0),
    }
    # the dimensionless gravitational strength at EW
    print(
        f"  dimensionless (M_EW/M_Pl)^2 = e^(-2 q Phi_3) = e^-{2*dN} = {math.exp(-2*dN):.2e}"
    )
    out["dimensionless_gravity_strength_EW"] = "e^(-2 q Phi_3) = e^-78"

    # check against observed ln(M_Pl/M_EW) for various EW scale choices
    print(f"\n[observed ln(M_Pl/M_EW) across EW scale choices vs q*Phi_3 = {dN}]")
    choices = {
        "Higgs vev v=246": 246.0,
        "top=173": 173.0,
        "Higgs=125": 125.0,
        "~100 GeV": 100.0,
        "Z=91": 91.2,
        "W=80": 80.4,
    }
    rows = []
    for name, mew in choices.items():
        ln_ratio = math.log(M_Pl / mew)
        rows.append(
            {
                "EW_scale": name,
                "ln_ratio": round(ln_ratio, 2),
                "delta_from_39": round(ln_ratio - dN, 2),
            }
        )
        print(
            f"  M_EW = {name:16s}: ln = {ln_ratio:5.2f}  (q Phi_3 - ln = {dN-ln_ratio:+.2f})"
        )
    out["observed_ln_ratios"] = rows
    # 39 sits within the spread of EW-scale definitions
    lns = [r["ln_ratio"] for r in rows]
    assert min(lns) - 1 <= dN <= max(lns) + 1

    # the e-fold budget closes: N = 60 = q Phi_3 + q Phi_6
    planck_to_ew = q * Phi3  # 39
    ew_to_end = q * Phi6  # 21
    print(
        f"\n[e-fold budget]  N = {N} = 2*beat = 2(Phi3+Phi4+Phi6); also = q(Phi3+Phi6) = {q*(Phi3+Phi6)}"
    )
    print(f"  Planck->EW : q Phi_3 = {planck_to_ew} e-folds")
    print(f"  EW->end    : q Phi_6 = {ew_to_end} e-folds")
    print(f"  total      : {planck_to_ew + ew_to_end} = N = {N}")
    assert planck_to_ew + ew_to_end == N == q * (Phi3 + Phi6) == 60
    assert (
        q * (Phi3 + Phi6) == 3 * 20 and 20 == 600 // beat
    )  # 20 = BC rings of 600-cell
    out["efold_budget"] = {
        "N": N,
        "N_as_2beat": 2 * beat,
        "N_as_q(Phi3+Phi6)": q * (Phi3 + Phi6),
        "planck_to_EW": planck_to_ew,
        "EW_to_end": ew_to_end,
        "rings_20": "Phi3+Phi6 = 20 = 600/30 BC rings",
    }

    print(
        "\nRESULT: the exponential the hierarchy needs is a substrate integer. Pass 7's"
    )
    print(
        "  open edge -- the ~13-order gap between the power-law tower (3x10^4) and the"
    )
    print("  Planck/electroweak 10^17 -- is filled by an EXPONENTIAL whose exponent is")
    print(
        "  q Phi_3 = 39: ln(M_Pl/M_EW) = q Phi_3, so M_Pl/M_EW = e^39 ~ 8.7x10^16 and the"
    )
    print(
        "  electroweak scale sits at M_Pl e^-39 ~ 141 GeV -- right among W, Z, Higgs, top."
    )
    print(
        "  And it closes the e-fold budget: inflation's N = 60 = q(Phi_3 + Phi_6) splits"
    )
    print(
        "  into the Planck->EW descent q Phi_3 = 39 and the remaining q Phi_6 = 21 e-folds,"
    )
    print("  both substrate integers. So the gravity-to-electroweak hierarchy is the")
    print(
        "  gravity-shell descent measured in the same e-fold clock as the CMB tilt -- 39"
    )
    print(
        "  e-folds down. Honest: an integer-level MATCH/postdiction (q Phi_3 reproduces"
    )
    print(
        "  the observed ln to ~1-2% and predicts M_EW ~ 141 GeV), not a derivation of why"
    )
    print(
        "  the EW scale sits there -- but the exponent is a clean substrate integer that"
    )
    print(
        "  slots exactly into the e-fold budget, turning the open edge into a sharp clue."
    )

    out["summary"] = (
        "the exponential the hierarchy needs is a substrate integer: ln(M_Pl/M_EW) = "
        "q*Phi_3 = 3*13 = 39. Pass 7's open edge (power-law tower 3x10^4 vs observed 10^17) "
        "is filled by an exponential with exponent q Phi_3 = 39: M_Pl/M_EW = e^39 ~ "
        "8.7x10^16, predicting M_EW = M_Pl e^-39 ~ 141 GeV (between W=80, Z=91, Higgs=125, "
        "top=173 -- THE electroweak scale), and (M_EW/M_Pl)^2 = e^-78 = e^(-2 q Phi_3). It "
        "closes the e-fold budget: inflation N = 60 = 2 beat = q(Phi_3+Phi_6) splits into "
        "Planck->EW = q Phi_3 = 39 and EW->end = q Phi_6 = 21 e-folds (with Phi_3+Phi_6 = 20 "
        "= 600/30 BC rings). So the gravity-to-electroweak hierarchy is the gravity-shell "
        "descent measured in the same e-fold clock as the CMB tilt, 39 e-folds down. "
        "HONEST: an integer-level MATCH/postdiction -- q Phi_3 = 39 reproduces the observed "
        "ln(M_Pl/M_EW) (38.4 at v=246 to 39.3 at ~100 GeV) to ~1-2% and predicts M_EW ~ 141 "
        "GeV, but does not independently derive why the EW scale sits exactly q Phi_3 "
        "e-folds down. New: the missing exponent is a clean substrate integer that slots "
        "exactly into N = 60 = q Phi_3 + q Phi_6 -- the open edge becomes a sharp clue."
    )
    out["sources"] = [
        "Pass 7 open edge (w33_gravity_hierarchy.py); N=60=2 beat, beat=30 (w33_efold_tick.py); "
        "q Phi_3 = 39, q Phi_6 = 21, q(Phi3+Phi6)=60; M_Pl=1.22e19 GeV; electroweak scale "
        "~100-246 GeV (PDG); inflation e-fold budget."
    ]
    with open("data/w33_hierarchy_exponential.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_hierarchy_exponential.json")


if __name__ == "__main__":
    main()
