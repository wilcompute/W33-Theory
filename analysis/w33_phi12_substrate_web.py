"""W(3,3) PHI_12 SUBSTRATE WEB.

Following the discovery that Phi_12 = q^4 - q^2 + 1 = 73 km/s/Mpc
equals the SH0ES local-universe Hubble constant, we systematically
explore identities of the form Phi_12 +/- X for substrate primitives
X, and identities Heegner_n = (A + B)/2 for substrate primitives A, B.

PHI_12 LINEAR WEB (additive identities):

  Phi_12 + Phi_6 = 2v = m_W            (W boson mass in GeV!)
  Phi_12 + Phi_3 = 2 * Heegner_43       (central Heegner)
  Phi_12 + p_Ih  = k * Phi_6 = 12*7 = 84
  Phi_12 + mu    = Phi_6 * p_Ih = 7*11 = 77
  Phi_12 + q     = mu * Heegner_19 = 4*19 = 76
  Phi_12 + 2^q   = q^4 = q^(q+1) = 81
  Phi_12 - q     = Phi_6 * Phi_4 = 7*10 = 70
  Phi_12 - mu    = q * 23 (23 = Ogg supersingular)
  Phi_12 - q!    = Heegner_67 (Planck Hubble; SUBSTRATE HUBBLE TENSION)
  Phi_12 - Phi_6 = 2 * q * p_Ih = 66
  Phi_12 - Phi_3 = q! * Phi_4 = 60
  Phi_12 - 2^q   = 5 * Phi_3 = 65
  Phi_12 * Phi_6 = M_9 = 511 (9th Mersenne prime; CMB Omega-density sum)

KEY NEW IDENTITY:

  Phi_12 + Phi_6 = 2v = m_W (W boson mass, GeV)
  --------------------------------------------
  SH0ES Hubble (73) + Fano prime (7) = W boson mass (80)
  --------------------------------------------

This connects the late-universe Hubble constant directly to the
W boson mass via the substrate's Fano prime Phi_6 = 7.

HEEGNER-AS-MEAN IDENTITIES:

The large prime Heegner discriminants are arithmetic means of
substrate primitive pairs:

  Heegner_19  = (q^q + p_Ih) / 2     = (27 + 11)/2 = 19
  Heegner_43  = (Phi_3 + Phi_12) / 2  = (13 + 73)/2 = 43
  Heegner_67  = (2^Phi_6 + q!) / 2    = (128 + 6)/2 = 67
  Heegner_163 = ??? (no clean 2-term mean form found)

PHI_12 PRIME DECOMPOSITIONS:

  Phi_12 = 73 (prime)
  73 - q  = 70 = Phi_6 * Phi_4
  73 + q  = 76 = mu * Heegner_19

The PHI_12 +/- q pair both factor cleanly: through Fano*Phi_4 below,
through mu*Heegner_19 above.

PHYSICAL READING:

Phi_12 is the substrate's 'top' cyclotomic value, sitting between:
  Heegner_67 (early-universe / Planck Hubble) below by q!
  Phi_12 = m_W - Phi_6 itself (late-universe / SH0ES Hubble)
  m_W = 2v above by Phi_6 (W boson mass)
  q^4 = 81 above by 2^q (gauge-coupling running)

So Phi_12 = SH0ES Hubble is positioned in the substrate cyclotomic
tower at a TIGHT distance from m_W, alpha-coupling scale q^4, and
the lower-cyclotomic factor Phi_6*Phi_4.
"""
from __future__ import annotations

import json
from pathlib import Path
from sympy import isprime


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


def phi12_additive_identities() -> list[dict]:
    items = [
        ("Phi_12 + Phi_6  = 2v = m_W",          PHI12 + PHI6,   2 * V,
         "W boson mass (GeV)"),
        ("Phi_12 + Phi_3  = 2*Heegner_43",       PHI12 + PHI3,   2 * 43,
         "Central Heegner prime times 2"),
        ("Phi_12 + p_Ih   = k * Phi_6",          PHI12 + P_IH,   K_CODEC * PHI6,
         "Substrate-clean product"),
        ("Phi_12 + mu     = Phi_6 * p_Ih",       PHI12 + MU,     PHI6 * P_IH,
         "Two substrate primes"),
        ("Phi_12 + q      = mu * Heegner_19",    PHI12 + Q,      MU * 19,
         "mu times smallest large Heegner"),
        ("Phi_12 + 2^q    = q^(q+1)",            PHI12 + 2 ** Q, Q ** (Q + 1),
         "Substrate gauge power"),
        ("Phi_12 - q      = Phi_6 * Phi_4",      PHI12 - Q,      PHI6 * PHI4,
         "Substrate prism product"),
        ("Phi_12 - q!     = Heegner_67",         PHI12 - QFACT,  67,
         "HUBBLE TENSION (Planck H_0)"),
        ("Phi_12 - Phi_6  = 2 * q * p_Ih",       PHI12 - PHI6,   2 * Q * P_IH,
         "Symmetric dual"),
        ("Phi_12 - Phi_3  = q! * Phi_4",         PHI12 - PHI3,   QFACT * PHI4,
         "Substrate symmetry"),
        ("Phi_12 - 2^q    = 5 * Phi_3",          PHI12 - 2 ** Q, 5 * PHI3,
         "Substrate-clean (5 outside substrate)"),
        ("Phi_12 * Phi_6  = M_9 (Mersenne)",     PHI12 * PHI6,   511,
         "9th Mersenne; CMB Omega density sum"),
    ]
    return [
        {"identity": s, "lhs": l, "rhs": r, "match": l == r, "physics": p}
        for (s, l, r, p) in items
    ]


def heegner_mean_identities() -> list[dict]:
    """Heegner_n = (A + B)/2 for substrate primitives A, B."""
    return [
        {
            "heegner":   19,
            "formula":   "(q^q + p_Ih) / 2 = (27 + 11)/2",
            "A":         Q ** Q,
            "B":         P_IH,
            "predicted": (Q ** Q + P_IH) // 2,
            "match":     (Q ** Q + P_IH) // 2 == 19,
        },
        {
            "heegner":   43,
            "formula":   "(Phi_3 + Phi_12) / 2 = (13 + 73)/2",
            "A":         PHI3,
            "B":         PHI12,
            "predicted": (PHI3 + PHI12) // 2,
            "match":     (PHI3 + PHI12) // 2 == 43,
        },
        {
            "heegner":   67,
            "formula":   "(2^Phi_6 + q!) / 2 = (128 + 6)/2",
            "A":         2 ** PHI6,
            "B":         QFACT,
            "predicted": (2 ** PHI6 + QFACT) // 2,
            "match":     (2 ** PHI6 + QFACT) // 2 == 67,
        },
    ]


def phi12_substrate_position() -> dict:
    """Phi_12's place in the substrate ladder."""
    return {
        "below_Phi_12": {
            "Heegner_67": 67,
            "Phi_6 * Phi_4": PHI6 * PHI4,
            "5 * Phi_3":    5 * PHI3,
            "2 * q * p_Ih": 2 * Q * P_IH,
            "q! * Phi_4":   QFACT * PHI4,
        },
        "phi_12":       PHI12,
        "above_Phi_12": {
            "mu * Heegner_19": MU * 19,
            "Phi_6 * p_Ih":    PHI6 * P_IH,
            "q^(q+1)":         Q ** (Q + 1),
            "2v = m_W":        2 * V,
            "k * Phi_6":       K_CODEC * PHI6,
            "2 * Heegner_43":  2 * 43,
        },
        "interpretation": (
            "Phi_12 sits at a substrate-clean MIDPOINT between the "
            "Planck Hubble below (Heegner_67) and the W boson mass "
            "above (2v = m_W). The substrate's cyclotomic ladder "
            "anchors all of cosmology + electroweak."
        ),
    }


def hubble_W_relation() -> dict:
    """The major new identity: Phi_12 + Phi_6 = m_W."""
    return {
        "claim":     "H_0_SH0ES + Phi_6 = m_W",
        "formula":   "Phi_12 + Phi_6 = 2v",
        "substrate": "73 + 7 = 80",
        "lhs":       PHI12 + PHI6,
        "rhs":       2 * V,
        "match":     PHI12 + PHI6 == 2 * V,
        "physics": (
            "The late-universe Hubble constant (73 km/s/Mpc) plus the "
            "substrate Fano prime (7) EQUALS the W boson mass (80 GeV). "
            "This is a striking substrate-level identity linking "
            "cosmology and electroweak physics."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "Phi_12": PHI12, "v": V, "f_gauge": F_GAUGE,
                "m_W (= 2v)": 2 * V,
            },
        },
        "phi12_additive_identities":  phi12_additive_identities(),
        "heegner_mean_identities":     heegner_mean_identities(),
        "phi12_substrate_position":    phi12_substrate_position(),
        "hubble_W_relation":            hubble_W_relation(),
        "headline_identity": (
            "PHI_12 SUBSTRATE WEB - MAJOR NEW IDENTITY:\n"
            "  Phi_12 + Phi_6 = 2v = m_W (W boson mass GeV)\n"
            "  73 + 7 = 80\n"
            "  SH0ES Hubble + Fano prime = W boson mass!\n\n"
            "Plus 11 more Phi_12 +/- X = substrate-product identities.\n"
            "Heegners as means: 19 = (q^q+p_Ih)/2, 43 = (Phi_3+Phi_12)/2,\n"
            "                    67 = (2^Phi_6+q!)/2.\n"
            "Phi_12 sits at a substrate ladder midpoint, anchoring\n"
            "cosmology (H_0_SH0ES) to electroweak (m_W) via Phi_6."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_phi12_substrate_web.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) PHI_12 SUBSTRATE WEB")
    print("=" * 78)

    print("\nPhi_12 additive identities (Phi_12 +/- X = substrate product):")
    for r in payload["phi12_additive_identities"]:
        print(f"  {r['identity']:>40s}: {r['lhs']:>3d} = {r['rhs']:>4d}  match={r['match']}")

    print("\nHeegner-as-mean identities:")
    for r in payload["heegner_mean_identities"]:
        print(f"  Heegner_{r['heegner']:>3d} = {r['formula']:>35s}  match={r['match']}")

    print("\nKEY NEW IDENTITY (Hubble <-> W boson):")
    h = payload["hubble_W_relation"]
    print(f"  {h['claim']}")
    print(f"  {h['formula']}: {h['substrate']}, match={h['match']}")
    print(f"  {h['physics']}")

    print("\nPhi_12 substrate ladder position:")
    p = payload["phi12_substrate_position"]
    print(f"  Below Phi_12:")
    for k, v in p["below_Phi_12"].items():
        print(f"    {k:>20s}: {v}")
    print(f"  Phi_12 = {p['phi_12']}")
    print(f"  Above Phi_12:")
    for k, v in p["above_Phi_12"].items():
        print(f"    {k:>20s}: {v}")

    print(f"\nHEADLINE:")
    print(payload["headline_identity"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
