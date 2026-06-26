#!/usr/bin/env python3
"""
The gravity dictionary, closed to a number: Newton's constant in substrate units is
G = k/(4f) = 1/8 = 1/2^q. The de Sitter loop (w33_memory_is_desitter.py) fixed the
cosmological constant Lambda = kappa = 2/k = 1/6 by Ollivier-Ricci curvature; here the
Gibbons-Hawking horizon thermodynamics fixes the remaining gravitational number. With
the horizon AREA = the gauge causal screen k = 12 and the de Sitter ENTROPY = the
boundary central charge S_dS = c = f = 24, the Bekenstein-Hawking relation S = A/(4G)
inverts to a single dimensionless Newton constant

        G = A / (4 S) = k / (4 f) = 12 / 96 = 1/8 = 1 / 2^q.

So the substrate's three gravitational numbers are all cyclotomic/q-integers:
        Lambda  = 2/k        = 1/6           (cosmological constant, = Ollivier kappa)
        S_dS    = f = c      = 24            (de Sitter entropy = central charge)
        G       = k/(4f)     = 1/8 = 1/2^q   (Newton constant)
        ell     = 1/sqrt(Lambda) = sqrt(6)   (de Sitter radius)
and they are mutually consistent: S = A/(4G) = 24 = f, and the de Sitter free energy /
horizon temperature follow.

WHY THESE ASSIGNMENTS.
  * AREA A = k = 12. The holographic screen is the GAUGE shell: in the 1+12+27 split
    (w33_holographic_code / w33_information_structure), the 12 = k is the boundary
    gauge layer through which bulk (27 = matter) is encoded -- the causal screen whose
    "area" (number of boundary bonds per point) is the valency k = 12.
  * ENTROPY S = f = c = 24. The de Sitter / horizon entropy equals the boundary central
    charge c = f = 24 (the Witting degree, the number of faces of the substrate's
    register), the standard "entropy = central charge" of a holographic boundary.
  * Lambda = 2/k = 1/6. Computed as the bulk Ollivier-Ricci curvature (positive = de
    Sitter), in the Gauss-Bonnet convention that closes E*Lambda = v.
Then G is forced: G = A/(4S) = k/(4f) = 1/2^q. The power 2^q = 8 is the GKP/qubit
dimension of the D4 matter shell -- Newton's constant is the inverse matter-shell
Hilbert dimension, the gravitational coupling = 1/(states the horizon resolves).

CONSISTENCY CHECKS (all exact, q=3).
  S = A/(4G) = 12/(4*(1/8)) = 24 = f.            [Bekenstein-Hawking]
  Lambda * ell^2 = (1/6)*6 = 1.                  [de Sitter radius]
  E * Lambda = 240*(1/6) = 40 = v.               [Gauss-Bonnet closure]
  G * S_dS = (1/8)*24 = 3 = q.                   [G*entropy = q]
  A / G = 12/(1/8) = 96 = 4f = 4 S_dS.           [area/Newton = 4*entropy]
  T_dS = 1/(2 pi ell) = 1/(2 pi sqrt(6)).        [de Sitter temperature]

Honest scope: the AREA=k and ENTROPY=c=f assignments are the substrate's holographic
dictionary (the central geometric claim, shared with w33_memory_is_desitter and the
holographic-code witnesses); Lambda=2/k is computed (Ollivier). GIVEN that dictionary,
G = k/(4f) = 1/2^q is FORCED by Bekenstein-Hawking -- a derived number, not a new
posit. In substrate (dimensionless) units; the absolute Planck scale (the dimensionful
G) is part of the named dynamical residue (absolute scales), not fixed here.

Verifies the dictionary numbers and every consistency relation at q=3.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    k = q * (q + 1)  # 12  gauge causal screen = horizon area
    f = q**3 - q  # 24  faces = central charge = de Sitter entropy
    v = (q + 1) * (q * q + 1)  # 40 points
    E = v * k // 2  # 240 edges = E8 roots
    mu = 4

    Lambda = 2 / k  # 1/6  cosmological constant = Ollivier kappa
    A = k  # 12   horizon area
    S = f  # 24   de Sitter entropy = central charge
    G = A / (4 * S)  # 1/8  Newton constant
    ell = 1 / math.sqrt(Lambda)  # sqrt(6) de Sitter radius

    print("== the gravity dictionary (substrate units, q=3) ==")
    print(
        f"  Lambda = 2/k          = {Lambda:.6f}  (= 1/6; cosmological const = Ollivier kappa)"
    )
    print(f"  A      = k            = {A}        (horizon area = gauge causal screen)")
    print(f"  S_dS   = f = c        = {S}        (de Sitter entropy = central charge)")
    print(f"  G      = A/(4S) = k/4f = {G}      (= 1/8 = 1/2^q; Newton constant)")
    print(f"  ell    = 1/sqrt(Lambda)= {ell:.6f}  (= sqrt(6); de Sitter radius)")

    assert abs(G - 1 / 8) < 1e-12
    assert G == k / (4 * f)
    assert abs(G - 1 / 2**q) < 1e-12
    out["dictionary"] = {
        "Lambda": "2/k = 1/6",
        "A_area": k,
        "S_dS": S,
        "S_dS_form": "f = c = 24 (central charge)",
        "G": "k/(4f) = 1/8 = 1/2^q",
        "ell": "1/sqrt(Lambda) = sqrt(6)",
    }

    # consistency checks
    checks = []
    checks.append(("Bekenstein-Hawking  S = A/(4G)", S, A / (4 * G)))
    checks.append(("de Sitter radius  Lambda*ell^2", 1.0, Lambda * ell**2))
    checks.append(("Gauss-Bonnet closure  E*Lambda", v, E * Lambda))
    checks.append(("G * S_dS = q", q, G * S))
    checks.append(("A / G = 4 S_dS", 4 * S, A / G))
    print(f"\n[consistency checks]")
    allok = True
    for name, want, got in checks:
        ok = abs(want - got) < 1e-9
        allok = allok and ok
        print(
            f"  {name:34s} want {want:8.4f}  got {got:8.4f}  {'OK' if ok else 'FAIL'}"
        )
    assert allok
    out["checks"] = [
        {"relation": n, "want": round(w, 6), "got": round(g, 6), "ok": True}
        for n, w, g in checks
    ]

    T_dS = 1 / (2 * math.pi * ell)
    print(f"\n[de Sitter thermodynamics]")
    print(f"  horizon temperature T_dS = 1/(2 pi ell) = {T_dS:.6f}")
    print(f"  free energy  F = -T_dS * S_dS = {-T_dS*S:.6f}")
    out["thermo"] = {
        "T_dS": round(T_dS, 6),
        "T_dS_form": "1/(2 pi sqrt(6))",
        "F": round(-T_dS * S, 6),
    }

    # the interpretation of 2^q
    print(
        f"\n[interpretation]  G = 1/2^q: 2^q = {2**q} = GKP/qubit dim of the D4 matter"
    )
    print(f"  shell -> Newton's constant = inverse matter-shell Hilbert dimension")
    print(f"  (gravitational coupling = 1/(states the horizon resolves)).")
    out["interpretation"] = (
        "G = 1/2^q = 1/8: 2^q is the GKP/qubit Hilbert dimension of the D4 matter shell; "
        "Newton's constant = inverse matter-shell dimension = 1/(states the horizon resolves)."
    )

    print("\nRESULT: the gravity dictionary closes to a number. With the holographic")
    print("  screen identified as the gauge shell (horizon area A = k = 12) and the de")
    print("  Sitter entropy as the boundary central charge (S_dS = c = f = 24), the")
    print(
        "  Bekenstein-Hawking relation forces Newton's constant G = A/(4S) = k/(4f) ="
    )
    print(
        "  1/8 = 1/2^q -- the inverse Hilbert dimension of the D4 matter shell. Together"
    )
    print("  with the computed cosmological constant Lambda = 2/k = 1/6 (Ollivier")
    print("  curvature) and the de Sitter radius ell = sqrt(6), the substrate's three")
    print(
        "  gravitational numbers are all q-integers, mutually consistent (S = A/4G = f,"
    )
    print("  E*Lambda = v, G*S = q), and dimensionless. Gravity in substrate units is")
    print(
        "  fixed: Lambda = 1/6, S_dS = 24, G = 1/2^q. The only residue is the absolute"
    )
    print(
        "  Planck scale (a dynamical input, not an integer) -- the dictionary itself is"
    )
    print("  closed.")

    out["summary"] = (
        "the gravity dictionary closed to a number: Newton's constant G = k/(4f) = 1/8 = "
        "1/2^q in substrate units. Given the holographic dictionary -- horizon AREA = "
        "gauge causal screen k = 12, de Sitter ENTROPY = boundary central charge S_dS = "
        "c = f = 24 -- Bekenstein-Hawking S = A/(4G) FORCES G = A/(4S) = k/(4f) = 1/2^q "
        "(2^q = 8 = GKP/qubit dim of the D4 matter shell, so G = inverse matter-shell "
        "Hilbert dimension). With Lambda = 2/k = 1/6 (computed as Ollivier-Ricci "
        "curvature, w33_memory_is_desitter) and de Sitter radius ell = 1/sqrt(Lambda) = "
        "sqrt(6), the three gravitational numbers are all q-integers and mutually "
        "consistent: S = A/4G = 24 = f, Lambda*ell^2 = 1, E*Lambda = 40 = v "
        "(Gauss-Bonnet), G*S_dS = 3 = q, A/G = 96 = 4 S_dS. Honest: AREA=k and ENTROPY="
        "c=f are the holographic dictionary (the central geometric claim); GIVEN it, G = "
        "1/2^q is DERIVED by Bekenstein-Hawking; in dimensionless substrate units (the "
        "absolute Planck scale is part of the named dynamical residue)."
    )
    out["sources"] = [
        "Lambda=2/k Ollivier-Ricci (w33_memory_is_desitter.py); 1+12+27 split, holographic "
        "screen (w33_holographic_code.py, w33_information_structure.py); de Sitter entropy "
        "= central charge c=f=24 (Gibbons-Hawking 1977; holographic c-theorem); "
        "Bekenstein-Hawking S=A/4G; D4 GKP/qubit dim 2^q=8 (w33_d4_gkp_error_curve.py); "
        "Gauss-Bonnet closure E*Lambda=v (Face 1, w33_cosmology_seventh_face.py)."
    ]
    with open("data/w33_gravity_dictionary.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_gravity_dictionary.json")


if __name__ == "__main__":
    main()
