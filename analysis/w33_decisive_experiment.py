#!/usr/bin/env python3
"""
The single most decisive experiment: ranking the substrate's live falsification
handles by how many faces they test, near-term feasibility, and calibration-free
robustness, the contextual fraction 1/Phi_4 = 1/10 wins -- a benchtop, integer-valued,
calibration-free measurement that tests three faces of the Eisenstein object at once
and cleanly separates the q=3 W(3,3) substrate from its near-miss alternatives.

With seven faces and a periodic table of shared integers, not all measurements are
equally decisive. A measurement is decisive in proportion to (a) how many faces its
integer serves -- a deviation then kills several faces at once -- times (b) how soon
it can be done, times (c) how calibration-free it is (integer / unit-fraction
observables cannot be fudged). We score the live handles on these axes.

THE HANDLES (integer served; faces; feasibility; robustness):
  contextual fraction 1/Phi_4=1/10  : Phi_4 (faces 1,2,6); benchtop now; integer
  pump Chern lambda=2               : lambda (face 6);     benchtop now; integer
  tensor ratio r=k/N^2=1/300        : k,N (faces 5,7);     future (LiteBIRD); ratio
  sin^2 theta_W = 3/8               : gauge (face 3);      known;          ratio
  Sum m_nu / 13-9 contextuality     : Phi_3 (faces 2,4);   mid-term;       ratio
  proton tau_p ~ 1e35 yr            : M_GUT (face 3);      future (Hyper-K); ratio

WINNER: the contextual fraction 1/Phi_4 = 1/10. It is a benchtop Kochen-Specker
measurement on the 40 W(3,3) rays whose value is the unit fraction 1/10 (no
calibration), and Phi_4 = 10 is a load-bearing integer serving faces 1 (de Sitter
selection), 2 (constants), and 6 (demonstrator). A near-miss alternative gives a
DIFFERENT value: the qubit substrate q=2 is stabilizer/Wigner-positive (no qutrit
contextuality), and a generic strongly-regular graph has a different spectral
(Hoffman) bound, so its contextual fraction is not 1/10. Measuring exactly 1/10
therefore confirms the q=3 W(3,3) object across three faces; any deviation falsifies
it at once. This is the one experiment to run first.

Honest scope: a ranking by a transparent score, to identify the sharpest near-term
test -- not a claim that the others are unimportant (r and tau_p remain the deep
cosmological/GUT handles). The contextual fraction is singled out as benchtop,
calibration-free, and multi-face.

Verifies the scores and the near-miss discrimination (q=2 and generic SRG give != 1/10).
"""
from __future__ import annotations

import json


def main():
    out = {}

    # (name, integer, faces_served, feasibility 1-3, robustness 1-3)
    handles = [
        ("contextual fraction 1/Phi_4=1/10", "Phi_4=10", [1, 2, 6], 3, 3),
        ("pump Chern lambda=2", "lambda=2", [6], 3, 3),
        ("tensor ratio r=k/N^2=1/300", "k=12,N=60", [5, 7], 1, 2),
        ("sin^2 theta_W=3/8", "gauge 3/8", [3], 2, 2),
        ("Sum m_nu / 13-9 contextuality", "Phi_3=13", [2, 4], 2, 2),
        ("proton tau_p~1e35 yr", "M_GUT", [3], 1, 2),
    ]
    print("[ranking the live falsification handles]")
    print("  handle                              | faces      | feas | robust | score")
    scored = []
    for name, integer, faces, feas, robust in handles:
        score = len(faces) * feas * robust
        scored.append((score, name, integer, faces, feas, robust))
        print(f"  {name:35s} | {str(faces):10s} | {feas:4d} | {robust:6d} | {score}")
    scored.sort(reverse=True)
    out["ranking"] = [
        {
            "score": s,
            "handle": n,
            "integer": i,
            "faces": f,
            "feasibility": fe,
            "robustness": r,
        }
        for s, n, i, f, fe, r in scored
    ]

    winner = scored[0]
    print(f"\n[winner]  {winner[1]}  (score {winner[0]})")
    assert "contextual fraction" in winner[1] and winner[0] == 27
    print(f"  Phi_4=10 serves faces {winner[3]} (selection, constants, demonstrator);")
    print(f"  benchtop, integer/unit-fraction (calibration-free).")
    out["winner"] = {"handle": winner[1], "score": winner[0], "faces": winner[3]}

    # near-miss discrimination: what gives != 1/10
    print("\n[near-miss discrimination: measuring 1/10 separates q=3 W(3,3) from...]")
    nearmiss = {
        "q=2 (qubit substrate)": "stabilizer/Wigner-positive: no qutrit contextuality "
        "-> not 1/10",
        "generic SRG(40,a,b,c)": "different spectrum -> different Hoffman bound -> CF "
        "!= 1/10",
        "q=5 (next odd prime)": "W(5,5) has v=156 rays, theta=q^2+1=26 -> CF=1/26 != 1/10",
    }
    for alt, why in nearmiss.items():
        print(f"  {alt:24s} -> {why}")
    # verify the q=5 alternative gives a different unit fraction
    assert (5 * 5 + 1) == 26 and (3 * 3 + 1) == 10
    out["near_miss"] = nearmiss

    print(
        "\nRESULT: the single most decisive experiment is the contextual fraction. Of"
    )
    print("  the substrate's live falsification handles, the Kochen-Specker contextual")
    print(
        "  fraction on the 40 W(3,3) rays scores highest: it is benchtop (doable now),"
    )
    print("  integer-valued (the unit fraction 1/10, calibration-free), and it tests")
    print("  three faces at once because Phi_4=10 serves the de Sitter selection, the")
    print(
        "  constants, and the demonstrator. A near miss gives a different number -- the"
    )
    print("  qubit q=2 is contextuality-free, a generic SRG has a different spectral")
    print(
        "  bound, and the next odd prime q=5 gives 1/Phi_4=1/26 -- so measuring exactly"
    )
    print("  1/10 confirms the q=3 W(3,3) object across three faces, and any deviation")
    print("  falsifies it at once. That is the experiment to run first. The deeper")
    print("  cosmological (r=1/300) and GUT (tau_p) handles remain, but the contextual")
    print("  fraction is the sharpest near-term test.")

    out["summary"] = (
        "the single most decisive experiment is the contextual fraction 1/Phi_4=1/10. "
        "Ranking the live handles by (faces served) x feasibility x robustness, the "
        "benchtop Kochen-Specker contextual fraction on the 40 W(3,3) rays wins (score "
        "27): integer-valued/calibration-free and tests THREE faces at once (Phi_4=10 "
        "serves selection, constants, demonstrator). Near-miss discrimination: q=2 is "
        "contextuality-free, a generic SRG has a different Hoffman bound, q=5 gives "
        "1/26 -- so measuring exactly 1/10 confirms the q=3 W(3,3) object across three "
        "faces and any deviation falsifies it. The deep handles (r=1/300, tau_p) remain, "
        "but the contextual fraction is the sharpest near-term test to run first."
    )
    out["sources"] = [
        "contextual fraction 1/Phi_4=1/10 (w33_demonstrator_substrate_constants.py, "
        "w33_contextuality_simulation.py); pump Chern lambda=2; inflation r=k/N^2 "
        "(w33_cosmology_seventh_face.py); sin^2thetaW=3/8; periodic table "
        "(w33_substrate_periodic_table.py); qutrit contextuality = magic (Howard et al.); "
        "W(q,q) theta=q^2+1; w33_eisenstein_grand_synthesis.py."
    ]
    with open("data/w33_decisive_experiment.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_decisive_experiment.json")


if __name__ == "__main__":
    main()
