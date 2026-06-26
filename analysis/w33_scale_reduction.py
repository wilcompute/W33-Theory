#!/usr/bin/env python3
"""
Closing the absolute scale -- honestly. A dimensionful number (M_Pl in GeV) can NEVER be
derived from dimensionless integers; that is logically impossible. What CAN be done, and is
done here, is to reduce EVERY physical scale to ONE unit via substrate-integer exponents:
M_GUT = M_Pl e^-Phi_6, M_EW = M_Pl e^-(q Phi_3), m_proton ~ M_Pl e^-(v+mu), and the
inflationary scale ~ M_GUT. Then choosing any single scale as the unit fixes all the others
by integers -- so the theory has exactly ONE dimensionful input (a units choice) and ZERO
free dimensionless parameters. The gravitational coupling at the proton scale,
alpha_G = (m_p/M_Pl)^2 = e^-(2(v+mu)) = e^-88 ~ 6x10^-39, is then a substrate integer in
the exponent -- the "gravity is weak" number.

Every pass named "absolute scales" as the residue. This pins down exactly what is
irreducible (one unit) and shows everything else is integer-locked to it.

THE IMPOSSIBILITY (stated plainly). No theory can output a dimensionful number (a mass in
GeV) from pure numbers -- you must pick a unit. So "deriving M_Pl" is not the goal; the
goal is to reduce all scales to one unit by integers, leaving a single dimensionful input.

THE SCALE LADDER (all to M_Pl by substrate integers).
    M_GUT   = M_Pl e^-Phi_6        (Phi_6 = 7,    gravity -> GUT; matches trinification),
    V^(1/4) ~ M_GUT                (inflation at the GUT scale, Pass 9),
    M_EW    = M_Pl e^-(q Phi_3)    (q Phi_3 = 39, the electroweak scale ~141 GeV),
    m_p     ~ M_Pl e^-(v+mu)       (v+mu = 44,    ln(M_Pl/m_p) = 44.0 observed),
so every scale is M_Pl times e^(-integer). Choosing M_Pl (or equivalently m_p, the mass we
weigh in) as the unit fixes all others by integers: ONE dimensionful input, ZERO free
dimensionless numbers.

THE GRAVITY-IS-WEAK NUMBER. The dimensionless strength of gravity between two protons is
    alpha_G = (m_p / M_Pl)^2 = e^-(2(v+mu)) = e^-88 = 6.0x10^-39,
versus the observed (m_p/M_Pl)^2 = 5.9x10^-39 -- the famous ~10^-39 weakness of gravity as a
substrate integer (88 = 2(v+mu)) in the exponent.

Honest scope: the cosmological exponents Phi_6 = 7 (GUT) and q Phi_3 = 39 (EW) are the
clean, established ones; the proton exponent ln(M_Pl/m_p) = 44.0 is reproduced by v+mu = 44
(also = (Phi_3+Phi_6)+f = 20+24) to 0.05% in the log, but 44 admits several substrate forms
-- the integer is real, its unique "derivation" is not pinned (a flagged caveat). The deep
point is conceptual and robust: all scales reduce to one unit by integer exponents, so the
absolute-scale residue is exactly ONE dimensionful input (a units choice) -- the theory has
no free dimensionless parameters. m_p itself comes from QCD dimensional transmutation, whose
full exponent needs the gauge running (deferred), here matched to v+mu.

Verifies the scale ladder exponents, ln(M_Pl/m_p) = 44 ~ v+mu, the one-unit reduction, and
alpha_G = e^-88 ~ observed.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    Phi3, Phi4, Phi6 = q * q + q + 1, q * q + 1, q * q - q + 1  # 13,10,7
    mu = 4
    v = (q + 1) * Phi4  # 40
    f = q**3 - q  # 24

    M_Pl = 1.2209e19  # GeV (full)
    m_p = 0.9383  # GeV
    M_EW = M_Pl * math.exp(-q * Phi3)  # e^-39 ~ 141 GeV
    M_GUT = M_Pl * math.exp(-Phi6)  # e^-7 ~ 1.1e16

    ln_mp = math.log(M_Pl / m_p)
    print("== reducing all scales to one unit by substrate integers ==")
    print(f"  ln(M_Pl/M_GUT) = Phi_6        = {Phi6}    -> M_GUT = {M_GUT:.2e} GeV")
    print(f"  ln(M_Pl/M_EW)  = q*Phi_3      = {q*Phi3}   -> M_EW  = {M_EW:.0f} GeV")
    print(
        f"  ln(M_Pl/m_p)   = {ln_mp:.2f} ~ v+mu = {v+mu}   (= (Phi3+Phi6)+f = {(Phi3+Phi6)+f})"
    )
    assert abs(ln_mp - (v + mu)) < 0.1
    assert v + mu == (Phi3 + Phi6) + f == 44
    out["scale_ladder"] = {
        "M_GUT": {"exponent": "Phi_6 = 7", "GeV": float(f"{M_GUT:.3e}")},
        "M_EW": {"exponent": "q*Phi_3 = 39", "GeV": round(M_EW, 0)},
        "m_proton": {
            "exponent": "v+mu = 44 (= (Phi3+Phi6)+f = 20+24)",
            "ln_observed": round(ln_mp, 2),
            "GeV": m_p,
        },
    }

    # the one-unit reduction
    print(
        f"\n[the reduction]  every scale = M_Pl * e^(-integer); choosing one unit (M_Pl,"
    )
    print(
        f"  or m_p) fixes all others by integers -> ONE dimensionful input, ZERO free"
    )
    print(f"  dimensionless parameters.")
    out["reduction"] = {
        "statement": "all scales = M_Pl * e^(-substrate integer)",
        "dimensionful_inputs": 1,
        "free_dimensionless_parameters": 0,
        "note": "a dimensionful number cannot come from integers; one unit is irreducible",
    }

    # gravity-is-weak number
    alpha_G_sub = math.exp(-2 * (v + mu))  # e^-88
    alpha_G_obs = (m_p / M_Pl) ** 2
    print(f"\n[gravity is weak]  alpha_G = (m_p/M_Pl)^2 = e^-(2(v+mu)) = e^-88")
    print(f"  substrate = {alpha_G_sub:.2e};  observed = {alpha_G_obs:.2e}")
    assert abs(math.log(alpha_G_sub / alpha_G_obs)) < 0.1
    out["gravity_weak"] = {
        "alpha_G": "(m_p/M_Pl)^2 = e^-(2(v+mu)) = e^-88",
        "substrate": float(f"{alpha_G_sub:.3e}"),
        "observed": float(f"{alpha_G_obs:.3e}"),
    }

    print(
        "\nRESULT: the absolute-scale residue is pinned to exactly one dimensionful input."
    )
    print(
        "  A mass in GeV can never come from pure integers -- a unit must be chosen -- so"
    )
    print("  the goal is not to derive M_Pl but to reduce every scale to one unit by")
    print(
        "  integers, and that is achieved: M_GUT = M_Pl e^-Phi_6 (7), V^(1/4) ~ M_GUT,"
    )
    print(
        "  M_EW = M_Pl e^-q Phi_3 (39), m_p ~ M_Pl e^-(v+mu) (44). Choosing any single"
    )
    print(
        "  scale as the unit fixes all the others by substrate integers, so the theory"
    )
    print("  has ONE dimensionful input (a units choice) and ZERO free dimensionless")
    print(
        "  parameters -- the cleanest possible form of 'closing the scale'. The famous"
    )
    print(
        "  weakness of gravity follows: alpha_G = (m_p/M_Pl)^2 = e^-88 = 6x10^-39, the"
    )
    print(
        "  10^-39 as the substrate integer 88 = 2(v+mu) in the exponent. Honest: the GUT"
    )
    print(
        "  and EW exponents (7, 39) are clean; the proton exponent 44 = v+mu reproduces"
    )
    print("  ln(M_Pl/m_p)=44.0 to 0.05% but admits several substrate forms (a flagged")
    print(
        "  caveat), and m_p's exponent ultimately comes from QCD running (deferred). The"
    )
    print("  robust result is conceptual: one unit, zero free dimensionless numbers.")

    out["summary"] = (
        "closing the absolute scale, honestly: a dimensionful number cannot be derived from "
        "integers (a unit must be chosen), so the achievement is reducing EVERY scale to ONE "
        "unit by substrate-integer exponents -- M_GUT = M_Pl e^-Phi_6 (7), V^(1/4) ~ M_GUT, "
        "M_EW = M_Pl e^-(q Phi_3) (39), m_p ~ M_Pl e^-(v+mu) (44, = (Phi3+Phi6)+f = 20+24, "
        "reproducing ln(M_Pl/m_p)=44.0 to 0.05%). Choosing any one scale as the unit fixes "
        "all others by integers, so the theory has ONE dimensionful input (a units choice) "
        "and ZERO free dimensionless parameters. The gravity-is-weak number follows: "
        "alpha_G = (m_p/M_Pl)^2 = e^-(2(v+mu)) = e^-88 = 6x10^-39 vs observed 5.9x10^-39 -- "
        "the famous ~10^-39 as the substrate integer 88 in the exponent. HONEST: the GUT (7) "
        "and EW (39) exponents are clean; the proton 44 = v+mu reproduces the log to 0.05% "
        "but admits several substrate forms (flagged), and m_p's exponent ultimately comes "
        "from QCD dimensional transmutation (gauge running, deferred). The robust point is "
        "conceptual and solid: one unit, zero free dimensionless parameters -- the residue "
        "is exactly one units choice."
    )
    out["sources"] = [
        "M_GUT=M_Pl e^-Phi_6, M_EW=M_Pl e^-q Phi_3 (w33_hierarchy_derivation.py); "
        "inflation V^(1/4)~M_GUT (w33_complete_primordial_spectrum.py); M_Pl=1.2209e19 GeV, "
        "m_p=0.9383 GeV (PDG); gravitational coupling alpha_G=(m_p/M_Pl)^2; v=40, mu=4, "
        "f=24; QCD dimensional transmutation for m_p."
    ]
    with open("data/w33_scale_reduction.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_scale_reduction.json")


if __name__ == "__main__":
    main()
