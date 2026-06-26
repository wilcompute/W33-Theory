#!/usr/bin/env python3
"""
Testing the G-running against a real datum -- the hierarchy -- with an exact positive and
an honest negative. The Newton-constant ladder G_s = k/(4 kissing_s) has step factors
that are ALL substrate constants (x mu, x Phi_4, x q^2 Phi_3 Phi_6), so the geometric
gravity hierarchy over the tower is exact and cyclotomic: G(A2)/G(E8) = mu Phi_4 = 40 = v,
and G(A2)/G(Leech) = mu q^2 Phi_3 Phi_4 Phi_6 = 32760 = kissing(Leech)/kissing(A2). But
these are 10^1-10^4 factors: the discrete tower does NOT by itself reach the Planck/
electroweak 10^17. Reaching 10^17 needs either the dynamical absolute scale (the named
residue) or the exponential e-fold mechanism (e^N) -- and neither lands precisely. The
honest verdict: the substrate fixes the gravity hierarchy at the tower level (v=40, exact)
but not the full 10^17 (a genuine open edge).

w33_newton_running.py gave G_s = q/(h_s rank_s) on the root-lattice rungs A2<D4<E8. This
extends the ladder to the Leech (the moonshine ceiling) and confronts the result with the
observed hierarchy.

THE STEP FACTORS ARE SUBSTRATE CONSTANTS (exact). With G_s = k/(4 kissing_s),
    kissing:   A2=6, D4=24, E8=240, Leech=196560,
the ratios between consecutive rungs are
    G(A2)/G(D4) = 24/6     = 4    = mu,
    G(D4)/G(E8) = 240/24   = 10   = Phi_4,
    G(E8)/G(Leech) = 196560/240 = 819 = q^2 Phi_3 Phi_6 = 9*13*7,
each a substrate constant. The cumulative spans are therefore cyclotomic:
    G(A2)/G(E8)    = mu Phi_4              = 40    = v               (the tower hierarchy),
    G(A2)/G(Leech) = mu q^2 Phi_3 Phi_4 Phi_6 = 32760 = kissing(Leech)/kissing(A2),
and Leech's kissing 196560 = 6 mu q^2 Phi_3 Phi_4 Phi_6 ties back to the alpha closure.
So the substrate's GEOMETRIC gravity hierarchy -- UV (A2) to IR (Leech, the c=24 ceiling)
-- is the exact integer 32760, with the gravity-to-gauge step to E8 being exactly v=40.

THE HONEST NEGATIVE (the 10^17 test). The observed Planck/electroweak ratio is
M_Pl/M_EW ~ 10^17 (and M_Pl^2/M_EW^2, the dimensionless gravity strength at the EW scale,
~ 10^34). The tower's largest gravity ratio is 32760 ~ 3x10^4 -- about 13 orders of
magnitude short. So the discrete kissing ladder does NOT produce the electroweak
hierarchy; it produces a geometric hierarchy of v=40 (to E8) / 32760 (to Leech). The
missing orders must come from either (a) the dynamical absolute scale (the residue we
have always named -- a dimensionful input, not an integer), or (b) an EXPONENTIAL
mechanism: de Sitter expansion gives e^N with N=60 e-folds -> e^60 ~ 1.1x10^26, while
M_Pl/M_EW ~ 10^17 needs only N ~ 39 e-folds of separation. Neither the power-law tower
(3x10^4) nor the full inflationary e^60 (10^26) lands on 10^17 without tuning. We report
this as an OPEN edge, not a closure.

Honest scope: the step factors and the cumulative v=40 / 32760 are EXACT arithmetic on
the established kissing numbers (the positive result). The confrontation with 10^17 is a
genuine NEGATIVE: the substrate fixes the tower-level (geometric) gravity hierarchy but
not the absolute Planck/EW hierarchy, which stays in the dynamical residue. Stated
plainly, not smoothed.

Verifies the substrate-constant step factors, the cumulative v=40 and 32760 spans, the
Leech kissing factorisation, and the ~13-order shortfall to 10^17.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction


def main():
    out = {}
    q = 3
    k = q * (q + 1)  # 12
    mu = 4
    Phi3, Phi4, Phi6 = q * q + q + 1, q * q + 1, q * q - q + 1  # 13,10,7

    rungs = {
        "A2": {"rank": 2, "kissing": 6},
        "D4": {"rank": 4, "kissing": 24},
        "E8": {"rank": 8, "kissing": 240},
        "Leech": {
            "rank": 24,
            "kissing": 196560,
        },  # moonshine ceiling (c = rank = 24 = f)
    }
    G = {n: Fraction(k, 4 * d["kissing"]) for n, d in rungs.items()}
    print("== the gravity hierarchy over the tower A2 < D4 < E8 < Leech ==")
    for n in rungs:
        print(
            f"  G({n:5s}) = k/(4*{rungs[n]['kissing']:6d}) = {str(G[n]):>10s} "
            f"= {float(G[n]):.3e}"
        )
    out["G"] = {n: {"kissing": rungs[n]["kissing"], "G": str(G[n])} for n in rungs}

    # step factors = substrate constants
    s1 = G["A2"] / G["D4"]
    s2 = G["D4"] / G["E8"]
    s3 = G["E8"] / G["Leech"]
    print(f"\n[step factors, all substrate constants]")
    print(f"  A2->D4   : {s1} = mu = {mu}")
    print(f"  D4->E8   : {s2} = Phi_4 = {Phi4}")
    print(
        f"  E8->Leech: {s3} = q^2 Phi_3 Phi_6 = {q*q}*{Phi3}*{Phi6} = {q*q*Phi3*Phi6}"
    )
    assert s1 == mu and s2 == Phi4 and s3 == q * q * Phi3 * Phi6 == 819
    out["steps"] = {
        "A2_to_D4": {"factor": int(s1), "is": "mu = 4"},
        "D4_to_E8": {"factor": int(s2), "is": "Phi_4 = 10"},
        "E8_to_Leech": {"factor": int(s3), "is": "q^2 Phi_3 Phi_6 = 819"},
    }

    # cumulative spans, cyclotomic
    span_E8 = G["A2"] / G["E8"]
    span_Leech = G["A2"] / G["Leech"]
    v = (q + 1) * Phi4
    print(f"\n[cumulative spans, cyclotomic]")
    print(f"  G(A2)/G(E8)    = mu*Phi_4 = {span_E8} = v = {v}   (gravity->gauge tower)")
    print(
        f"  G(A2)/G(Leech) = mu*q^2*Phi_3*Phi_4*Phi_6 = {span_Leech} "
        f"= kissing(Leech)/kissing(A2)"
    )
    assert span_E8 == v == 40
    assert span_Leech == mu * q * q * Phi3 * Phi4 * Phi6 == 32760
    assert (
        196560 == 6 * mu * q * q * Phi3 * Phi4 * Phi6
    )  # Leech factorisation (alpha closure)
    out["spans"] = {
        "A2_to_E8": {"value": int(span_E8), "form": "mu*Phi_4 = v = 40"},
        "A2_to_Leech": {
            "value": int(span_Leech),
            "form": "mu*q^2*Phi_3*Phi_4*Phi_6 = 32760",
        },
        "leech_kissing": "196560 = 6*mu*q^2*Phi_3*Phi_4*Phi_6 (alpha closure)",
    }

    # the honest 10^17 test
    M_Pl_over_M_EW = 1e17
    tower_max = float(span_Leech)
    shortfall_orders = math.log10(M_Pl_over_M_EW / tower_max)
    N_needed = math.log(M_Pl_over_M_EW)  # e-folds to give 10^17 exponentially
    N_inflation = 60
    e60 = math.exp(N_inflation)
    print(f"\n[the 10^17 test -- honest negative]")
    print(f"  observed M_Pl/M_EW ~ 1e17; tower max G ratio = {tower_max:.3e} (= 32760)")
    print(
        f"  shortfall = {shortfall_orders:.1f} orders of magnitude (tower is power-law)"
    )
    print(f"  exponential option: e^N, N=60 -> e^60 = {e60:.2e} (overshoots 1e17);")
    print(
        f"  1e17 needs only N ~ {N_needed:.0f} e-folds of separation -> neither lands."
    )
    out["hierarchy_test"] = {
        "observed_MPl_over_MEW": "~1e17",
        "tower_max_ratio": 32760,
        "shortfall_orders": round(shortfall_orders, 1),
        "exponential_e60": float(f"{e60:.3e}"),
        "N_for_1e17": round(N_needed, 1),
        "verdict": "OPEN: tower gives geometric hierarchy v=40 / 32760, not the absolute 1e17",
    }

    print(
        "\nRESULT: an exact positive and an honest negative. The Newton-constant ladder's"
    )
    print(
        "  step factors are all substrate constants -- x mu, x Phi_4, x q^2 Phi_3 Phi_6"
    )
    print(
        "  (= 4, 10, 819) along A2->D4->E8->Leech -- so the geometric gravity hierarchy"
    )
    print(
        "  is cyclotomic and exact: G(A2)/G(E8) = mu Phi_4 = 40 = v (the gravity-to-gauge"
    )
    print("  span), and the full UV->IR span to the Leech ceiling is G(A2)/G(Leech) =")
    print(
        "  mu q^2 Phi_3 Phi_4 Phi_6 = 32760 = kissing(Leech)/kissing(A2), tying back to"
    )
    print("  the Leech factorisation 196560 = 6 mu q^2 Phi_3 Phi_4 Phi_6 of the alpha")
    print(
        "  closure. But this is ~3x10^4, about 13 orders short of the Planck/electroweak"
    )
    print(
        "  10^17: the discrete tower fixes the TOWER-LEVEL gravity hierarchy (v=40), not"
    )
    print("  the absolute one. The missing orders need the dynamical scale (the named")
    print(
        "  residue) or an exponential (e^N, N=60 -> 10^26, overshooting); neither lands"
    )
    print("  on 10^17 without tuning. So the substrate explains the geometric gravity")
    print(
        "  hierarchy exactly and leaves the absolute Planck/EW hierarchy open -- reported"
    )
    print("  plainly, an exact result and a real edge.")

    out["summary"] = (
        "G-running vs the hierarchy: an exact positive and an honest negative. The Newton "
        "ladder G_s = k/(4 kissing_s) has step factors that are ALL substrate constants -- "
        "A2->D4 x mu=4, D4->E8 x Phi_4=10, E8->Leech x q^2 Phi_3 Phi_6 = 819 -- so the "
        "geometric gravity hierarchy is cyclotomic and exact: G(A2)/G(E8) = mu Phi_4 = 40 "
        "= v (gravity->gauge), and the full span to the Leech ceiling G(A2)/G(Leech) = "
        "mu q^2 Phi_3 Phi_4 Phi_6 = 32760 = kissing(Leech)/kissing(A2), consistent with "
        "the alpha-closure factorisation 196560 = 6 mu q^2 Phi_3 Phi_4 Phi_6. HONEST "
        "NEGATIVE: 32760 ~ 3e4 is ~13 orders short of the Planck/electroweak ~1e17; the "
        "discrete tower fixes the tower-level (geometric) gravity hierarchy v=40 but NOT "
        "the absolute 1e17. The missing orders need the dynamical absolute scale (named "
        "residue) or an exponential (e^N, N=60 -> 1e26, overshooting; 1e17 needs N~39) -- "
        "neither lands without tuning. So the substrate explains the geometric gravity "
        "hierarchy exactly and leaves the absolute Planck/EW hierarchy OPEN. Stated "
        "plainly: exact step factors + cumulative v=40/32760 (positive), 1e17 not "
        "reproduced (negative)."
    )
    out["sources"] = [
        "G-running G_s=k/(4 kissing_s) (w33_newton_running.py); kissing numbers A2=6, "
        "D4=24, E8=240, Leech=196560; Leech factorisation 196560=6 mu q^2 Phi_3 Phi_4 "
        "Phi_6 (w33_alpha_closure.py); moonshine ceiling = Leech c=rank=24=f; observed "
        "M_Pl/M_EW ~ 1e17; inflation N=60 (w33_efold_tick.py)."
    ]
    with open("data/w33_gravity_hierarchy.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_gravity_hierarchy.json")


if __name__ == "__main__":
    main()
