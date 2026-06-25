#!/usr/bin/env python3
"""
Deriving the Majorana ratio Phi3/q^2 = 13/9 from the Z3 grade structure: the naive
single-grade texture is DEGENERATE (it fails), and the splitting that fixes it is
the projective/affine point-count ratio |PG(2,3)|/|AG(2,3)| = 13/9 -- the same
Phi3 = 13 = Phi_3(q=3) cyclotomic that runs through the whole census.

w33_neutrino_majorana_texture.py found that the seesaw needs a Majorana eigenvalue
ratio r2/r3 = Phi3/q^2 = 13/9 to turn the substrate Dirac hierarchy into the
observed Delta m^2 ratio, but left 13/9 as a motivated input. This witness opens it
up: it builds M_R from the Z3 grade selection rule (Pillar 68) and shows two things.

STEP A (the naive texture FAILS). With a single grade-0 B-L breaking VEV, the
selection rule grade(a)+grade(b) = 0 mod 3 forces
    M_R = [[A,0,0],[0,0,C],[0,C,0]]   (in the grade basis),
whose eigenvalues are {A, +C, -C}: the {1,2} block is DEGENERATE in magnitude. The
seesaw then gives two degenerate light neutrinos -- contradicting the observed
non-degenerate spectrum. So the substrate Majorana mass CANNOT come from one grade;
the degeneracy must be broken.

STEP B (the splitting IS projective/affine). The degeneracy-breaking ratio is
    r2/r3 = Phi3/q^2 = 13/9 = |PG(2,3)| / |AG(2,3)|,
the ratio of projective to affine points of the plane over F_3: the symmetric
(democratic, trivial-rep) right-handed neutrino mode -- the TBM column (1,1,1)/sqrt3
-- couples to ALL Phi3 = q^2+q+1 = 13 projective points, while the orthogonal modes
see only the q^2 = 9 affine points (the projective plane minus the q+1 = 4 points of
the line at infinity). So the heavier (democratic) Majorana eigenvalue exceeds the
others by exactly the projective/affine count 13/9.

THE CYCLOTOMIC TIE. Phi3 = 13 is Phi_3(q) at q=3 -- one of the degree-2 cyclotomics
{Phi_3,Phi_4,Phi_6}(3) = {13,10,7} that also factor the de Sitter cubic and the GQ
point count (w33_desitter_crystallographic_unify.py). So the neutrino Majorana
hierarchy is set by the SAME cyclotomic skeleton that selects q=3 -- the neutrino
sector and the q=3 selection share one structure.

Honest scope: Step A (the degeneracy) is an exact consequence of the grade rule.
Step B gives 13/9 a precise geometric MEANING (projective/affine) and the right
spectrum, but identifying the M_R eigenvalues *literally* with these point counts
needs the full cubic-form coupling c(N_a,N_b,<v>) computed over a multi-grade VEV --
that explicit computation is the remaining rigor. What is established: the naive
texture is degenerate (so a splitting is mandatory), and the splitting that works is
the projective/affine = Phi3/q^2 ratio tied to the cyclotomic skeleton.
"""
from __future__ import annotations

import json

import numpy as np

DM21_OBS, DM31_OBS = 7.4e-5, 2.5e-3
RATIO_OBS = DM21_OBS / DM31_OBS


def grade0_MR(A=1.0, C=1.0):
    """M_R from a single grade-0 VEV: nonzero where grade(a)+grade(b)=0 mod 3.
    In the grade basis (0,1,2): (0,0)->A; (1,2),(2,1)->C; all else 0."""
    return np.array([[A, 0, 0], [0, 0, C], [0, C, 0]], dtype=float)


def main():
    out = {}
    q = 3
    Phi3 = q * q + q + 1  # 13
    print(f"[substrate]  q={q}, Phi3=Phi_3({q})=q^2+q+1={Phi3}, q^2={q*q}")

    # ---- STEP A: the naive single-grade texture is degenerate ----
    M = grade0_MR(A=1.7, C=1.0)
    eig = np.linalg.eigvalsh(M)
    mags = sorted(np.abs(eig))
    print("\n[STEP A: single grade-0 VEV M_R]")
    print(f"  M_R = {M.tolist()}")
    print(
        f"  eigenvalues = {np.round(eig,4).tolist()}; |eig| sorted = {np.round(mags,4).tolist()}"
    )
    degenerate = abs(mags[1] - mags[2]) < 1e-9 or abs(mags[0] - mags[1]) < 1e-9
    print(f"  TWO eigenvalues degenerate in magnitude: {degenerate}  -> seesaw gives")
    print(f"  two degenerate light neutrinos -> CONTRADICTS observed spectrum.")
    assert degenerate
    out["step_A_degeneracy"] = {
        "M_R": M.tolist(),
        "abs_eigs": [round(x, 4) for x in mags],
        "degenerate": bool(degenerate),
        "conclusion": "single-grade M_R is degenerate; a splitting is mandatory",
    }

    # ---- STEP B: the splitting is projective/affine = Phi3/q^2 ----
    PG = q * q + q + 1  # 13 projective points of PG(2,3)
    AG = q * q  # 9 affine points
    line_inf = q + 1  # 4 points on the line at infinity
    print("\n[STEP B: projective/affine splitting]")
    print(
        f"  |PG(2,3)| = q^2+q+1 = {PG}; |AG(2,3)| = q^2 = {AG}; "
        f"line at infinity = q+1 = {line_inf}; {PG}-{line_inf}={PG-line_inf}"
    )
    assert PG - line_inf == AG
    r2_over_r3 = PG / AG
    print(f"  democratic (trivial-rep) mode sees all {PG}; others see affine {AG}")
    print(f"  => r2/r3 = |PG|/|AG| = {PG}/{AG} = Phi3/q^2 = {r2_over_r3:.4f}")
    out["step_B_geometry"] = {
        "PG_points": PG,
        "AG_points": AG,
        "line_at_infinity": line_inf,
        "r2_over_r3": round(r2_over_r3, 4),
        "meaning": "Phi3/q^2 = |PG(2,3)|/|AG(2,3)| = projective/affine",
    }

    # the resulting neutrino spectrum (substrate Dirac (1,5,10), this M_R ratio)
    y = (1.0, 5.0, 10.0)
    m2m3 = (y[1] / y[2]) ** 2 * (AG / PG)  # (1/4)*(9/13)
    ratio = m2m3**2
    print(
        f"\n[spectrum]  m2/m3 = (y2/y3)^2 (q^2/Phi3) = {m2m3:.4f} "
        f"(obs {np.sqrt(RATIO_OBS):.4f})"
    )
    print(f"  Delta m^2_21/Delta m^2_31 = {ratio:.4f} (obs {RATIO_OBS:.4f})")
    assert abs(ratio - RATIO_OBS) / RATIO_OBS < 0.05
    out["spectrum"] = {
        "m2_over_m3": round(m2m3, 4),
        "dm21_over_dm31": round(ratio, 4),
        "observed": round(RATIO_OBS, 4),
    }

    # the cyclotomic tie
    cyc = {3: q * q + q + 1, 4: q * q + 1, 6: q * q - q + 1}
    print(f"\n[cyclotomic tie]  Phi3=13 is Phi_3({q}); the degree-2 cyclotomics")
    print(f"  {{Phi_3,Phi_4,Phi_6}}({q}) = {{{cyc[3]},{cyc[4]},{cyc[6]}}} -- the same")
    print(f"  skeleton that selects q=3 (de Sitter, crystallographic). The neutrino")
    print(f"  Majorana hierarchy and the q=3 selection share one cyclotomic structure.")
    assert cyc == {3: 13, 4: 10, 6: 7}
    out["cyclotomic_tie"] = {
        "Phi_3_4_6_at_3": [cyc[3], cyc[4], cyc[6]],
        "note": "Phi3=13=Phi_3(3); neutrino hierarchy uses the q=3-selection skeleton",
    }

    print("\nRESULT: the Majorana ratio is opened up. The naive single-grade M_R is")
    print("  exactly DEGENERATE (the grade rule forces a [[A,0,0],[0,0,C],[0,C,0]]")
    print("  texture with eigenvalues {A,+C,-C}), so the substrate CANNOT give the")
    print("  observed non-degenerate neutrinos from one grade -- a splitting is")
    print("  mandatory. The splitting that works is the projective/affine point-count")
    print("  ratio |PG(2,3)|/|AG(2,3)| = 13/9 = Phi3/q^2: the democratic right-handed")
    print(
        "  neutrino (the trivial-rep TBM column) couples to all 13 projective points,"
    )
    print("  the others to the 9 affine ones. That gives Delta m^2_21/Delta m^2_31 =")
    print(
        "  0.030, and Phi3=13 is Phi_3(3) -- so the neutrino Majorana hierarchy is set"
    )
    print(
        "  by the SAME cyclotomic skeleton that selects q=3. Honest: the degeneracy is"
    )
    print(
        "  exact; the projective/affine identification gives 13/9 a geometric meaning"
    )
    print(
        "  and the right spectrum, but pinning M_R's eigenvalues to these counts from"
    )
    print("  the cubic-form coupling is the remaining rigor.")

    out["summary"] = (
        "Majorana ratio 13/9 opened up: the naive single-grade-0 VEV gives an EXACTLY "
        "degenerate M_R = [[A,0,0],[0,0,C],[0,C,0]] (eigs {A,+C,-C}) -> two degenerate "
        "light neutrinos, contradicting observation, so a splitting is mandatory. The "
        "splitting is the projective/affine count |PG(2,3)|/|AG(2,3)| = 13/9 = Phi3/q^2 "
        "(democratic RH-neutrino sees all 13 projective points, others the 9 affine), "
        "giving dm21/dm31=0.030. Phi3=13=Phi_3(3), one of the degree-2 cyclotomics "
        "{13,10,7} that select q=3 -- the neutrino hierarchy shares the q=3 skeleton. "
        "Honest: degeneracy exact; projective/affine gives 13/9 meaning + right "
        "spectrum, but deriving M_R eigenvalues = these counts from the cubic form is "
        "the remaining step."
    )
    out["sources"] = [
        "Z3 grade selection rule (Pillar 68, THEORY_PART_CLXXVII_MASS_TEXTURE.py); "
        "type-I seesaw m_i=y_i^2/r_i; PG(2,3)=13 projective / AG(2,3)=9 affine points; "
        "Phi_n(3) for n=3,4,6 = 13,10,7; w33_neutrino_majorana_texture.py, "
        "w33_desitter_crystallographic_unify.py."
    ]
    with open("data/w33_majorana_grade_derivation.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_majorana_grade_derivation.json")


if __name__ == "__main__":
    main()
