#!/usr/bin/env python3
"""
The three forces meet -- at M_Pl e^{-Phi_6}, with alpha_GUT^{-1} = f = 24. Pass 26 fixed the weak
angle as a 27-trace; the deeper test of grand unification is whether the THREE running gauge
couplings actually converge to a single value at a single scale. This witness runs the one-loop
renormalization group from M_Z upward and finds: with the plain Standard-Model content the three
couplings do NOT unify (the pairwise crossings are spread over 10^13-10^17 GeV, the famous
near-miss), but with the substrate's structural-supersymmetric content -- the SUSY-like spectrum
implied by the exact boson-fermion balance f Phi_4 = g mu^2 = 240 -- all three converge to a single
point at M_GUT ~ 2x10^16 GeV ~ M_Pl e^{-Phi_6}, with the unified coupling alpha_GUT^{-1} ~ 24 = f =
dim SU(5). So the unification scale is the substrate's mass-ladder rung M_Pl e^{-Phi_6} (the
grand-unification e-fold, Phi_6 = q^2-q+1 = 7), and the unified coupling's inverse is the gauge
mode count f = 24 = the dimension of the unified group SU(5) -- the strength at which the forces
merge is the number of gauge bosons. The structural SUSY that cancels the leading cosmological
constant (f Phi_4 = g mu^2) is the SAME content that makes the couplings unify: one spectrum does
both.

This turns the assumed unification into a computed one: the substrate's boson-fermion balance
supplies the SUSY-like content, and the couplings then meet at M_Pl e^{-Phi_6} with
alpha_GUT^{-1} = f.

THE INPUTS (at M_Z, SU(5) normalization).
    alpha_1^{-1} = (3/5) cos^2 th_W / alpha_em = 59.0   (alpha_1 = 5/3 alpha_Y)
    alpha_2^{-1} = sin^2 th_W / alpha_em       = 29.6
    alpha_3^{-1} = 1 / alpha_s                  = 8.5
THE RUNNING.  alpha_i^{-1}(mu) = alpha_i^{-1}(M_Z) - (b_i/2pi) ln(mu/M_Z), one loop.
    Standard Model: (b_1,b_2,b_3) = (41/10, -19/6, -7)  -> NO single meeting point.
    Structural SUSY: (b_1,b_2,b_3) = (33/5, 1, -3)       -> single meeting point.

THE RESULT (structural-SUSY content).
    M_GUT ~ 2x10^16 GeV ~ M_Pl e^{-Phi_6} (the GUT rung of the mass ladder, Phi_6 = 7).
    alpha_GUT^{-1} ~ 24 = f = dim SU(5) (the gauge mode count = the unified group's dimension).
    The three pairwise crossings coincide to within ~1% in ln(mu) -- genuine unification.

THE STRUCTURAL-SUSY LINK.  The content that unifies the couplings is the SUSY-like spectrum, and
the substrate already carries a structural supersymmetry: the Hodge boson and fermion sectors
balance, f Phi_4 = g mu^2 = 24*10 = 15*16 = 240 = |roots(E8)| (the cancellation behind the
cosmological constant, Pass 18). So the SAME boson-fermion balance that cancels the leading vacuum
energy supplies the content that unifies the gauge couplings -- one spectrum, two consequences.

Honest scope: one-loop running with the structural-SUSY (MSSM-like) beta functions is STANDARD,
and that the MSSM unifies near 2x10^16 with alpha_GUT^{-1} ~ 24-25 is the textbook result. The
substrate content is (i) that the unification scale is the mass-ladder rung M_Pl e^{-Phi_6} (the
running 2x10^16 vs M_Pl e^{-Phi_6} ~ 1.1x10^16 agree to a factor ~2 / the exponent 6.4 vs 7 to
~10%, within one-loop + threshold uncertainty), (ii) that alpha_GUT^{-1} ~ 24 = f = dim SU(5) is the
gauge mode count, and (iii) that the unifying SUSY-like content is the SAME boson-fermion balance
f Phi_4 = g mu^2 that cancels the leading CC. The exact M_GUT and alpha_GUT depend on the (assumed
SUSY-like) spectrum and thresholds, not derived in detail here; plain SM does NOT unify. So: a
computed unification at the substrate scale with alpha_GUT^{-1} = f, given the structural-SUSY
content the substrate's balance implies.

Verifies that the SM content fails to unify (spread crossings) while the structural-SUSY content
unifies at ~2x10^16 ~ M_Pl e^{-Phi_6} with alpha_GUT^{-1} ~ 24 = f.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, f = 3, 24
    Phi6 = 7
    M_Z = 91.1876
    M_Pl = 1.22e19
    ainv_em, s2w, alpha_s = 127.95, 0.23122, 0.1181

    a2 = s2w * ainv_em
    aY = (1 - s2w) * ainv_em
    a1 = 0.6 * aY  # SU(5) normalization alpha_1 = 5/3 alpha_Y
    a3 = 1 / alpha_s
    ainv = [a1, a2, a3]
    print("== the three forces meet: gauge-coupling unification ==")
    print(f"  at M_Z: a1^-1={a1:.2f}, a2^-1={a2:.2f}, a3^-1={a3:.2f}  (SU(5) norm)")
    out["inputs"] = {
        "a1inv_MZ": round(a1, 2),
        "a2inv_MZ": round(a2, 2),
        "a3inv_MZ": round(a3, 2),
    }

    def crossings(b):
        # t where a_i^-1 = a_j^-1 : (ai-aj)/((bi-bj)/2pi)
        res = {}
        for i, j, lbl in [(0, 1, "a1=a2"), (0, 2, "a1=a3"), (1, 2, "a2=a3")]:
            t = (ainv[i] - ainv[j]) / ((b[i] - b[j]) / (2 * math.pi))
            mu = M_Z * math.exp(t)
            aG = ainv[1] - b[1] / (2 * math.pi) * t
            res[lbl] = {"t": t, "mu": mu, "aGUT_inv": aG}
        return res

    scenarios = {
        "Standard Model": (41 / 10, -19 / 6, -7),
        "structural SUSY": (33 / 5, 1.0, -3.0),
    }
    out["scenarios"] = {}
    for name, b in scenarios.items():
        cr = crossings(b)
        mus = [cr[k]["mu"] for k in cr]
        spread = max(mus) / min(mus)
        unifies = spread < 2.0  # all three within a factor 2 in scale
        print(f"\n  [{name}]  betas = ({b[0]:.2f},{b[1]:.2f},{b[2]:.2f})")
        for lbl, d in cr.items():
            print(f"    {lbl}: mu={d['mu']:.2e} GeV, aGUT^-1={d['aGUT_inv']:.1f}")
        print(f"    -> scale spread = {spread:.1f}x; UNIFIES (single point): {unifies}")
        out["scenarios"][name] = {
            "betas": [round(x, 3) for x in b],
            "crossings": {
                k: {"mu_GeV": f"{v['mu']:.2e}", "aGUT_inv": round(v["aGUT_inv"], 1)}
                for k, v in cr.items()
            },
            "scale_spread": round(spread, 1),
            "unifies": unifies,
        }

    # the structural-SUSY unification point
    cr = crossings(scenarios["structural SUSY"])
    M_GUT = sum(cr[k]["mu"] for k in cr) / 3
    aGUT_inv = sum(cr[k]["aGUT_inv"] for k in cr) / 3
    M_Pl_e_Phi6 = M_Pl * math.exp(-Phi6)
    print(f"\n[the unification point (structural SUSY)]")
    print(
        f"  M_GUT ~ {M_GUT:.2e} GeV;  M_Pl e^-Phi6 = {M_Pl_e_Phi6:.2e} GeV "
        f"(factor {M_GUT/M_Pl_e_Phi6:.1f})"
    )
    print(f"  exponent ln(M_Pl/M_GUT) = {math.log(M_Pl/M_GUT):.1f} vs Phi6 = {Phi6}")
    print(f"  alpha_GUT^-1 ~ {aGUT_inv:.1f} = f = {f} = dim SU(5)")
    assert 22 < aGUT_inv < 27 and 5e15 < M_GUT < 5e16
    out["unification"] = {
        "M_GUT_GeV": f"{M_GUT:.2e}",
        "M_Pl_e_minus_Phi6": f"{M_Pl_e_Phi6:.2e}",
        "exponent_vs_Phi6": [round(math.log(M_Pl / M_GUT), 1), Phi6],
        "aGUT_inv": round(aGUT_inv, 1),
        "aGUT_inv_is_f": round(aGUT_inv) == f,
        "f_is_dim_SU5": f == 5**2 - 1,
    }

    # the structural-SUSY link to the CC balance
    print(
        f"\n[structural-SUSY link]  the unifying content is the boson-fermion balance"
    )
    print(
        f"  f Phi_4 = g mu^2 = 24*10 = 15*16 = 240 = |roots(E8)| (the CC cancellation)"
    )
    print(
        f"  the SAME balance that cancels the leading vacuum energy supplies the SUSY-like"
    )
    print(
        f"  content that unifies the gauge couplings -- one spectrum, two consequences"
    )
    assert 24 * 10 == 15 * 16 == 240
    out["structural_susy"] = {
        "balance": "f Phi_4 = g mu^2 = 240 = |roots(E8)|",
        "reading": "the boson-fermion balance (CC cancellation) is the content that unifies the couplings",
    }

    print(
        "\nRESULT: the three forces meet -- at the substrate scale, with the substrate coupling."
    )
    print(
        "  Running the one-loop renormalization group from M_Z, the plain Standard-Model content"
    )
    print(
        "  does NOT unify: the three pairwise crossings are spread over 10^13-10^17 GeV (the famous"
    )
    print(
        "  near-miss). But with the substrate's structural-supersymmetric content -- the SUSY-like"
    )
    print(
        "  spectrum implied by the exact boson-fermion balance f Phi_4 = g mu^2 = 240 -- all three"
    )
    print(
        f"  converge to a single point at M_GUT ~ 2x10^16 GeV ~ M_Pl e^-Phi_6 (the grand-unification"
    )
    print(
        "  rung of the mass ladder, Phi_6 = q^2-q+1 = 7), with the unified coupling alpha_GUT^-1 ~"
    )
    print(
        "  24 = f = dim SU(5). So the scale at which the forces merge is the substrate's mass-ladder"
    )
    print(
        "  rung M_Pl e^-Phi_6, and the strength at which they merge is the gauge mode count f = 24 ="
    )
    print(
        "  the dimension of the unified group. And the content that does the unifying is the SAME"
    )
    print(
        "  boson-fermion balance that cancels the leading cosmological constant -- one spectrum, two"
    )
    print(
        "  consequences. Honest: one-loop MSSM-like running unifying near 2x10^16 with alpha_GUT^-1"
    )
    print(
        "  ~ 24-25 is textbook; the substrate content is that M_GUT is the ladder rung M_Pl e^-Phi_6"
    )
    print(
        "  (to ~10% in the exponent), that alpha_GUT^-1 = f = dim SU(5), and that the unifying"
    )
    print(
        "  SUSY-like content is the boson-fermion balance f Phi_4 = g mu^2; plain SM does not unify."
    )

    out["summary"] = (
        "the three forces meet -- at M_Pl e^-Phi6, with alpha_GUT^-1 = f = 24. One-loop RG from "
        "M_Z (SU(5) norm): plain Standard-Model content does NOT unify (pairwise crossings spread "
        "over 10^13-10^17 GeV, the near-miss); the substrate's structural-SUSY content (the SUSY-"
        "like spectrum implied by the boson-fermion balance f Phi4 = g mu^2 = 240) converges to a "
        "single point at M_GUT ~ 2x10^16 GeV ~ M_Pl e^-Phi6 (GUT rung, Phi6 = q^2-q+1 = 7), with "
        "alpha_GUT^-1 ~ 24 = f = dim SU(5). So the unification scale is the mass-ladder rung M_Pl "
        "e^-Phi6 and the unified coupling inverse is the gauge mode count f = 24 = dim of the "
        "unified group; the SAME boson-fermion balance that cancels the leading CC supplies the "
        "content that unifies the couplings (one spectrum, two consequences). HONEST: one-loop "
        "MSSM-like unification near 2x10^16 with alpha_GUT^-1 ~ 24-25 is textbook; the substrate "
        "content is M_GUT = the ladder rung M_Pl e^-Phi6 (exponent 6.4 vs 7, ~10%), alpha_GUT^-1 = "
        "f = dim SU(5), and the unifying content = the balance f Phi4 = g mu^2; the exact M_GUT/"
        "alpha_GUT depend on the assumed SUSY-like spectrum and thresholds, not derived in detail; "
        "plain SM does NOT unify."
    )
    out["sources"] = [
        "M_Z, sin^2 th_W, alpha_s, alpha_em (PDG); one-loop SM/MSSM beta functions (standard); "
        "M_GUT = M_Pl e^-Phi6 (mass ladder, w33_everything.tex / w33_floor_derivation.py); f=24, "
        "g=15, balance f Phi4 = g mu^2 = 240 (w33_cc_mechanism.py, w33_e6_27_standard_model.py)."
    ]
    with open("data/w33_gauge_unification.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_gauge_unification.json")


if __name__ == "__main__":
    main()
