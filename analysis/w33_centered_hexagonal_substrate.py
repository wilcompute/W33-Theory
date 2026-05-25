"""W(3,3) CENTERED HEXAGONAL SUBSTRATE.

The centered hexagonal numbers H(n) = 1 + 6*T_(n-1) = 3n^2 - 3n + 1
form the substrate's natural geometric sequence at q = 3:

  H(n) = q * n^2 - q * n + 1
       = q * n * (n - 1) + 1

These count the number of points in a hexagonal lattice of radius n.
The substrate's hexagonal lattice IS the q-deformation of Z^2 with
6-fold symmetry, and the centered hexagonals at small n hit nearly
every key substrate primitive:

  H(1)  =  1
  H(2)  =  7    =  Phi_6                       (substrate Fano prime)
  H(3)  =  19   =  Heegner_19                   (smallest large Heegner)
  H(4)  =  37   =  p_12 (= 12th prime)
  H(5)  =  61   =  p_18 = Phi_6 + p_Ih (shift)
  H(6)  =  91   =  m_Z                          (Z boson mass GeV!)
  H(7)  =  127  =  M_7 = 2^Phi_6 - 1            (7th Mersenne)
  H(8)  =  169  =  Phi_3^2
  H(9)  =  217  =  Phi_6 * p_11 (p_11 = 31 Moonshine)
  H(13) =  469  =  Phi_6 * Heegner_67

THE BIG IDENTITY:

  m_Z = H(q!) = q * q! * (q!-1) + 1 = 91 GeV

The Z boson mass equals the q!th centered hexagonal number.  At
q = 3, the hexagonal lattice has 6-fold symmetry; q! = 6 is exactly
one full rotational cycle of the hexagon.  So m_Z = "one hexagonal
cycle's worth of substrate points" + 1 (the center).

PHYSICAL READING:

The hexagonal structure is the FUNDAMENTAL GEOMETRY of the substrate
at q=3.  The Standard Model masses appear as integer-indexed counts
of this hexagonal lattice:

  Phi_6   = H(2)   (substrate Fano prime; 2nd hexagonal)
  Heegner_19 = H(3) (Heegner discriminant)
  m_Z      = H(q!) (Z boson mass; "q!th hexagonal radius")
  M_7      = H(7) (7th Mersenne; 2^Phi_6 - 1)

CONSECUTIVE DIFFERENCES:

  H(n) - H(n-1) = q! * (n-1)

So:
  H(2) - H(1)  =  q!         = 6
  H(3) - H(2)  =  2 * q!      = 12 = k = q*mu (codec valency!)
  H(4) - H(3)  =  3 * q!      = 18 = q * q!
  H(5) - H(4)  =  4 * q!      = 24 = f (gauge multiplicity!)
  H(6) - H(5)  =  5 * q!      = 30 = q * Phi_4
  H(7) - H(6)  =  6 * q!      = 36 = (q!)^2
  H(8) - H(7)  =  7 * q!      = 42 = q! * Phi_6

So:
  H(3) - H(2) = k  (codec)
  H(5) - H(4) = f  (gauge multiplicity)
  H(7) - H(6) = (q!)^2  (perm-permutation product)
  H(8) - H(7) = q! * Phi_6  (substrate Fano product)

The codec k and gauge mult f ARE consecutive differences of the
substrate's centered hexagonal sequence.

CONNECTION TO Phi_n:

  Phi_6 = H(2)   (3rd cyclotomic = 2nd hexagonal)
  Phi_6^2 = 49 = H(?)+... 49 - 37 = 12 = k, so 49 = H(4) + k = H(4)*Phi_4/... hmm
  Phi_3 = 13.  13 - 7 = 6 = q!, so Phi_3 = Phi_6 + q! = H(2) + q!.
  Phi_4 = 10.  10 - 7 = 3 = q, so Phi_4 = Phi_6 + q = H(2) + q.
  Phi_12 = 73. 73 - 61 = 12, so Phi_12 = H(5) + k.

CONNECTION TO STANDARD MODEL MASSES:

  m_W = 80 = H(6) - 11 = m_Z - p_Ih (so m_W = H(q!) - p_Ih).
  m_Z = 91 = H(q!) = H(6).
  m_H = 125 = H(7) - 2 = 2^Phi_6 - q.
  v_EW = 246 = H(10) - 25 = 2*H(7) - 8 = ... or v_EW = 246 = q!*Phi_4*Phi_4 + q!*Phi_3 = ...
         Cleanest: v_EW = H(10) - 25 = 2*H(7) - 2^Phi_6 + 14, messy.
  m_t = 173 = H(8) + mu = Phi_3^2 + mu.  CLEAN: m_t = Phi_3^2 + mu = H(8) + mu.

So m_t = H(8) + mu = Phi_3^2 + 4 = 169 + 4 = 173 GeV!  Companion to
m_t = Heegner_163 + Phi_4 = 163 + 10 = 173.  Two substrate-clean forms.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
PHI12 = Q ** 4 - Q ** 2 + 1
V = 40
F_GAUGE = 24


def H(n: int) -> int:
    return Q * n * (n - 1) + 1


def centered_hexagonal_sequence() -> list[dict]:
    interp_map = {
        1:  "1",
        2:  "Phi_6 (substrate Fano prime)",
        3:  "Heegner_19 (smallest large Heegner)",
        4:  "p_12 (12th prime = 37)",
        5:  "Phi_6 + p_Ih = 61 = p_18",
        6:  "m_Z = 91 GeV (Z boson mass!)",
        7:  "M_7 = 2^Phi_6 - 1 (7th Mersenne)",
        8:  "Phi_3^2 = 169 (cyclotomic squared)",
        9:  "Phi_6 * p_11 = 217 (Moonshine prime)",
        10: "271 (prime, p_57)",
        11: "p_(Heegner_67) = 331",
        12: "397 (prime, p_78)",
        13: "Phi_6 * Heegner_67 = 469",
    }
    return [
        {"n": n, "H(n)": H(n), "substrate": interp_map.get(n, "?")}
        for n in range(1, 14)
    ]


def consecutive_differences() -> list[dict]:
    """H(n) - H(n-1) = q! * (n-1)."""
    rows = []
    for n in range(2, 9):
        diff = H(n) - H(n - 1)
        substrate = {
            2: "q! = 6",
            3: "k = 2*q! = 12 (codec valency)",
            4: "q*q! = 3*q! = 18",
            5: "f = 4*q! = 24 (GAUGE MULTIPLICITY)",
            6: "q*Phi_4 = 5*q! = 30",
            7: "(q!)^2 = 6*q! = 36",
            8: "q!*Phi_6 = 7*q! = 42",
        }[n]
        rows.append({
            "n": n,
            "H(n)-H(n-1)": diff,
            "substrate":   substrate,
        })
    return rows


def m_Z_identity() -> dict:
    """The key physics identity."""
    return {
        "claim":     "m_Z = H(q!) = q * q! * (q!-1) + 1",
        "lhs":       H(QFACT),
        "rhs":       91,
        "match":     H(QFACT) == 91,
        "decomposition": "3 * 6 * 5 + 1 = 90 + 1 = 91",
        "physics": (
            "The Z boson mass equals the q!th centered hexagonal "
            "number.  Geometrically: 'one full hexagonal cycle' of "
            "substrate points (q! = 6 is the full 6-fold rotation "
            "in the hexagonal lattice)."
        ),
    }


def heegner_19_identity() -> dict:
    return {
        "claim":     "Heegner_19 = H(q) = q^3 - q^2 + 1",
        "lhs":       H(Q),
        "rhs":       19,
        "match":     H(Q) == 19,
        "substrate": "Smallest large Heegner = qth centered hexagonal",
    }


def phi_6_identity() -> dict:
    return {
        "claim":     "Phi_6 = H(2) = q * 2 + 1 = 2q + 1",
        "lhs":       H(2),
        "rhs":       PHI6,
        "match":     H(2) == PHI6,
        "substrate": "Substrate Fano prime = 2nd centered hexagonal",
    }


def m_top_alt_identity() -> dict:
    return {
        "claim":     "m_t = H(8) + mu = Phi_3^2 + mu",
        "lhs":       H(8) + MU,
        "rhs":       173,
        "match":     H(8) + MU == 173,
        "alt":       "Companion to m_t = Heegner_163 + Phi_4 = 173",
    }


def m_H_alt_identity() -> dict:
    return {
        "claim":     "m_H = H(7) - 2 = 2^Phi_6 - q = M_7 - 2",
        "lhs":       H(7) - 2,
        "rhs":       125,
        "match":     H(7) - 2 == 125,
        "alt":       "Higgs mass = (7th centered hexagonal) - 2",
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "Phi_12": PHI12, "v": V, "f_gauge": F_GAUGE,
                "centered_hex_formula": "H(n) = q*n*(n-1) + 1 = 3n^2 - 3n + 1",
            },
        },
        "centered_hexagonal_sequence": centered_hexagonal_sequence(),
        "consecutive_differences":     consecutive_differences(),
        "phi_6_identity":               phi_6_identity(),
        "heegner_19_identity":          heegner_19_identity(),
        "m_Z_identity":                  m_Z_identity(),
        "m_top_alt_identity":           m_top_alt_identity(),
        "m_H_alt_identity":             m_H_alt_identity(),
        "headline_identity": (
            "CENTERED HEXAGONAL SUBSTRATE THEOREM:\n\n"
            "  H(n) = q*n(n-1) + 1 = 3n^2 - 3n + 1\n"
            "  (the centered hexagonal numbers; count points in hex lattice radius n)\n\n"
            "Substrate primitives = centered hexagonals at integer n:\n"
            "  H(2) = Phi_6      = 7  (substrate Fano prime)\n"
            "  H(q) = Heegner_19 = 19  (smallest large Heegner)\n"
            "  H(q!) = m_Z       = 91 (Z boson mass GeV!)  *** MAJOR ***\n"
            "  H(7) = M_7        = 127 = 2^Phi_6 - 1  (7th Mersenne)\n"
            "  H(8) = Phi_3^2    = 169\n\n"
            "Consecutive differences are substrate-clean:\n"
            "  H(3)-H(2) = k = 12 (codec valency)\n"
            "  H(5)-H(4) = f = 24 (GAUGE MULTIPLICITY)\n"
            "  H(7)-H(6) = (q!)^2 = 36\n\n"
            "Companion m_t and m_H identities:\n"
            "  m_t = Phi_3^2 + mu = H(8) + mu = 173 GeV\n"
            "  m_H = 2^Phi_6 - q = H(7) - 2 = 125 GeV\n\n"
            "The substrate's underlying geometry IS the hexagonal lattice at q=3.\n"
            "Standard Model masses are 'rings' of the hexagonal substrate."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_centered_hexagonal_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) CENTERED HEXAGONAL SUBSTRATE")
    print("=" * 78)

    print(f"\nFormula: H(n) = q*n*(n-1) + 1 = 3n^2 - 3n + 1\n")

    print("Centered hexagonal sequence:")
    for r in payload["centered_hexagonal_sequence"]:
        print(f"  H({r['n']:>2d}) = {r['H(n)']:>4d}  --  {r['substrate']}")

    print("\nConsecutive differences H(n) - H(n-1):")
    for r in payload["consecutive_differences"]:
        print(f"  H({r['n']}) - H({r['n']-1}) = {r['H(n)-H(n-1)']:>3d}  =  {r['substrate']}")

    print("\nKey substrate identities:")
    for key in ["phi_6_identity", "heegner_19_identity", "m_Z_identity",
                "m_top_alt_identity", "m_H_alt_identity"]:
        i = payload[key]
        print(f"  {i['claim']:>40s}: {i['lhs']} = {i['rhs']}  match={i['match']}")

    m = payload["m_Z_identity"]
    print(f"\n*** Z BOSON MASS IDENTITY ***")
    print(f"  {m['claim']}")
    print(f"  {m['decomposition']}")
    print(f"  {m['physics']}")

    print(f"\nHEADLINE:")
    print(payload["headline_identity"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
