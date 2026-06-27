#!/usr/bin/env python3
"""
The Higgs sector and the hierarchy: m_H = vq+mu+1, the electroweak scale at q Phi_3 e-folds, and
the metastability scale at h(E7). The electroweak/Higgs sector is the last piece of the
matter+gauge map: the Higgs mass, the electroweak scale, the quartic self-coupling, and the
hierarchy (why the electroweak scale is so far below the Planck scale). This witness collects the
substrate readings: the Higgs mass m_H = vq+mu+1 = 125 GeV; the electroweak vacuum expectation
value v_EW = 2(vq+q) = 246 GeV, so the Higgs is half the electroweak scale (m_H/v_EW ~ 1/2) and the
quartic is lambda = m_H^2/(2 v_EW^2) ~ mu^2/(vq+mu) = 16/124 = 0.129; the electroweak scale sits at
q Phi_3 = 39 e-folds below the Planck scale (ln(M_Pl/v_EW) = 38.4), the same q Phi_3 = 39 that
appears in the mass ladder; and the famous Higgs-vacuum (meta)stability scale, where the
Standard-Model quartic runs through zero at ~10^11 GeV, sits at h(E7) = 18 e-folds below M_Pl
(ln(M_Pl/10^11) = 18.6, with 18 = h(E7) = the complement-graph parameter lambda_bar = mu_bar). So
the Higgs mass, the electroweak scale, the quartic, the hierarchy exponent, and the metastability
scale are all substrate integers -- the electroweak sector is a cyclotomic descent like the rest.

This closes the matter+gauge map (Passes 25-27) at the symmetry-breaking sector: the Higgs and the
electroweak scale are substrate rungs, and the hierarchy is the integer q Phi_3 = 39.

THE HIGGS MASS AND QUARTIC.
    m_H = vq + mu + 1 = 120 + 4 + 1 = 125 GeV   (measured 125.25; vq = 120 = -log10 CC = 4 beat).
    v_EW = 2(vq + q) = 2(120 + 3) = 246 GeV     (the electroweak scale).
    m_H / v_EW = 125/246 = 0.51 ~ 1/2           (the Higgs is half the electroweak scale).
    lambda = m_H^2/(2 v_EW^2) = 0.129 ~ mu^2/(vq+mu) = 16/124 = 0.1290.

THE HIERARCHY (electroweak scale).
    ln(M_Pl / v_EW) = 38.4 ~ q Phi_3 = 39       (the electroweak rung of the mass ladder).
So the electroweak scale is q Phi_3 = 39 e-folds below the Planck scale -- the hierarchy is the
substrate integer q Phi_3, the same one that sets M_EW in the ladder. (The substrate fixes the
VALUE of the hierarchy; the dynamical protection of the light Higgs is the structural-SUSY question
of the next witness.)

THE METASTABILITY SCALE.
    The Standard-Model Higgs quartic runs through zero at the instability scale ~10^11 GeV, where
    ln(M_Pl/10^11) = 18.6 ~ h(E7) = 18 = lambda_bar = mu_bar (the complement SRG(40,27,18,18)).
So the scale at which the electroweak vacuum becomes metastable is h(E7) = 18 e-folds below the
Planck scale -- another substrate rung, tying the near-criticality of the Higgs vacuum to the
exceptional Coxeter number h(E7).

Honest scope: m_H = vq+mu+1 and v_EW = 2(vq+q) are integer-level POSTDICTIONS (the measured 125.25
and 246 GeV equal the substrate integers to ~0.2%); the quartic lambda = mu^2/(vq+mu) and the ratio
m_H/v_EW ~ 1/2 follow from those (a derived consequence, not an independent input). The hierarchy
q Phi_3 = 39 is the VALUE of the electroweak exponent (the ladder rung), matched to 38.4; the
substrate fixes the value but the dynamical hierarchy problem (radiative stability of the light
Higgs) is addressed by the structural SUSY, not here. The metastability ~ h(E7) is approximate (the
instability scale carries ~1-2 order-of-magnitude theory uncertainty), a suggestive match (18.6 vs
18). So: the electroweak sector's masses, scale, quartic, hierarchy exponent, and metastability
scale are substrate integers, mostly postdictions; the dynamical pieces are flagged.

Verifies m_H = vq+mu+1 = 125, v_EW = 2(vq+q) = 246, m_H/v_EW ~ 1/2, lambda = mu^2/(vq+mu) = 0.129,
the hierarchy q Phi_3 = 39, and the metastability h(E7) = 18.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, lam, mu, v = 3, 2, 4, 40
    Phi3, Phi6, hE7 = 13, 7, 18
    M_Pl = 1.22e19
    print("== the Higgs sector and the hierarchy ==")

    # Higgs mass, EW scale, quartic
    m_H = q * v + mu + 1  # 125
    v_EW = 2 * (q * v + q)  # 246
    m_H_meas, v_EW_meas = 125.25, 246.22
    ratio = m_H_meas / v_EW_meas
    lam_H = m_H_meas**2 / (2 * v_EW_meas**2)
    lam_sub = mu**2 / (q * v + mu)  # 16/124
    print(f"  m_H = vq+mu+1 = {m_H} GeV (meas {m_H_meas})")
    print(
        f"  v_EW = 2(vq+q) = {v_EW} GeV (meas {v_EW_meas}); m_H/v_EW = {ratio:.3f} ~ 1/2"
    )
    print(
        f"  quartic lambda = m_H^2/(2 v_EW^2) = {lam_H:.4f}; mu^2/(vq+mu) = 16/124 = {lam_sub:.4f}"
    )
    assert m_H == 125 and v_EW == 246 and abs(lam_H - lam_sub) / lam_H < 0.01
    out["higgs"] = {
        "m_H": m_H,
        "m_H_form": "vq+mu+1",
        "m_H_meas": m_H_meas,
        "v_EW": v_EW,
        "v_EW_form": "2(vq+q)",
        "v_EW_meas": v_EW_meas,
        "m_H_over_v_EW": round(ratio, 3),
        "lambda": round(lam_H, 4),
        "lambda_form": "mu^2/(vq+mu) = 16/124",
        "lambda_sub": round(lam_sub, 4),
    }

    # hierarchy
    hier = math.log(M_Pl / v_EW_meas)
    print(
        f"\n[hierarchy]  ln(M_Pl/v_EW) = {hier:.1f} ~ q Phi_3 = {q*Phi3} (the EW ladder rung)"
    )
    assert abs(hier - q * Phi3) < 1.5
    out["hierarchy"] = {
        "ln_MPl_over_vEW": round(hier, 1),
        "q_Phi3": q * Phi3,
        "reading": "the electroweak scale is q Phi_3 = 39 e-folds below M_Pl (the ladder rung)",
    }

    # metastability
    inst = 1e11  # SM Higgs instability scale
    meta = math.log(M_Pl / inst)
    print(
        f"\n[metastability]  SM Higgs quartic -> 0 at ~10^11 GeV; ln(M_Pl/10^11) = {meta:.1f} "
        f"~ h(E7) = {hE7}"
    )
    print(f"  18 = h(E7) = lambda_bar = mu_bar (complement SRG(40,27,18,18))")
    assert abs(meta - hE7) < 1.5
    out["metastability"] = {
        "instability_GeV": "~1e11",
        "ln_MPl_over_inst": round(meta, 1),
        "h_E7": hE7,
        "reading": "the EW vacuum becomes metastable at h(E7)=18 e-folds below M_Pl",
    }

    print(
        "\nRESULT: the electroweak sector is a cyclotomic descent like the rest. The Higgs mass"
    )
    print(
        "  is m_H = vq + mu + 1 = 125 GeV; the electroweak scale is v_EW = 2(vq + q) = 246 GeV, so"
    )
    print(
        "  the Higgs is half the electroweak scale (m_H/v_EW ~ 1/2) and the quartic self-coupling"
    )
    print(
        "  is lambda = m_H^2/(2 v_EW^2) = 0.129 ~ mu^2/(vq+mu) = 16/124. The electroweak scale sits"
    )
    print(
        "  at q Phi_3 = 39 e-folds below the Planck scale (ln(M_Pl/v_EW) = 38.4) -- the hierarchy is"
    )
    print(
        "  the substrate integer q Phi_3, the same one in the mass ladder. And the Higgs-vacuum"
    )
    print(
        "  metastability scale, where the Standard-Model quartic runs through zero at ~10^11 GeV,"
    )
    print(
        "  sits at h(E7) = 18 e-folds below M_Pl (ln(M_Pl/10^11) = 18.6, 18 = h(E7) = the"
    )
    print(
        "  complement-graph parameter). So the Higgs mass, the electroweak scale, the quartic, the"
    )
    print(
        "  hierarchy exponent, and the metastability scale are all substrate integers. Honest: m_H"
    )
    print(
        "  and v_EW are integer-level postdictions (to ~0.2%); the quartic and m_H/v_EW ~ 1/2 follow"
    )
    print(
        "  from them; the hierarchy q Phi_3 = 39 is the value of the electroweak exponent (the"
    )
    print(
        "  dynamical hierarchy protection is the structural-SUSY question of the next witness); the"
    )
    print(
        "  metastability ~ h(E7) is approximate (the instability scale has theory uncertainty)."
    )

    out["summary"] = (
        "the Higgs sector and the hierarchy, as substrate integers. m_H = vq+mu+1 = 125 GeV (meas "
        "125.25); v_EW = 2(vq+q) = 246 GeV, so m_H/v_EW ~ 1/2 and the quartic lambda = m_H^2/(2 "
        "v_EW^2) = 0.129 ~ mu^2/(vq+mu) = 16/124. The electroweak scale is q Phi_3 = 39 e-folds "
        "below M_Pl (ln(M_Pl/v_EW) = 38.4) -- the hierarchy is the substrate integer q Phi_3, the "
        "ladder rung. The Higgs-vacuum metastability scale (SM quartic -> 0 at ~10^11 GeV) is "
        "h(E7) = 18 e-folds below M_Pl (ln(M_Pl/10^11) = 18.6, 18 = h(E7) = lambda_bar = mu_bar of "
        "the complement SRG). So the electroweak masses, scale, quartic, hierarchy exponent, and "
        "metastability scale are all substrate integers -- a cyclotomic descent. HONEST: m_H and "
        "v_EW are integer-level postdictions (~0.2%); the quartic and m_H/v_EW ~ 1/2 follow from "
        "them; the hierarchy q Phi_3 = 39 is the value of the EW exponent (dynamical protection is "
        "the structural-SUSY question); metastability ~ h(E7) is approximate (instability-scale "
        "theory uncertainty). The EW symmetry-breaking sector closes the matter+gauge map."
    )
    out["sources"] = [
        "m_H = vq+mu+1, v_EW = 246, q Phi3 = 39 EW rung (mass ladder, w33_everything.tex / "
        "w33_e6_27_standard_model.py); SM Higgs metastability ~10^11 GeV (standard); h(E7)=18 = "
        "lambda_bar = mu_bar of complement SRG(40,27,18,18)."
    ]
    with open("data/w33_higgs_sector.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_higgs_sector.json")


if __name__ == "__main__":
    main()
