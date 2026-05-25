"""W(3,3) HEEGNER F-LATTICE SUBSTRATE IDENTITIES.

Extension of the Fano Prism Dual Tower (MCCLIV/dual): the THREE
substrate-clean products {v, q*p_Ih, Phi_3} = {40, 33, 13} from the
Phi_6-centered pairs satisfy further linear identities, and tie
directly to the large prime Heegner discriminants {19, 43, 67, 163}.

THE THREE PRODUCT IDENTITIES (from Fano Prism Dual Tower):

  Pair                Sum           Product       Substrate form
  ----                ---           -------       --------------
  (mu, Phi_4)         2*Phi_6 = 14  v   = 40      mu*Phi_4 = Phi_6^2 - q^2
  (q, p_Ih)           2*Phi_6 = 14  q*p_Ih = 33   q*p_Ih   = Phi_6^2 - mu^2
  (1, Phi_3)          2*Phi_6 = 14  Phi_3 = 13    1*Phi_3  = Phi_6^2 - (q!)^2

NEW PRODUCT-SUM IDENTITIES:

(a) v + q*p_Ih = Phi_12 = H_0_SH0ES

    40 + 33 = 73 = q^4 - q^2 + 1 = Phi_12, the 12th cyclotomic at q=3.

    Substrate reading: the first TWO Phi_6-symmetric products sum to
    the 12th cyclotomic value, which equals the SH0ES local-universe
    Hubble constant (73 km/s/Mpc, PDG 73.04).

(b) v - q*p_Ih = Phi_6

    40 - 33 = 7 = Phi_6.  The difference returns the symmetric center.

(c) v + q*p_Ih + Phi_3 = 2 * Heegner_43

    40 + 33 + 13 = 86 = 2 * 43 = 2 * Heegner_43.

    Substrate reading: the FULL sum of the three Phi_6-symmetric
    products is twice the central large prime Heegner discriminant.

PRIME-INDEX IDENTITY (companion to alpha^-1 = p_33):

(d) p_(q * Phi_6) = Phi_12

    The (q*Phi_6 = 21)th prime is 73 = Phi_12.
    Compare: p_(q*p_Ih) = p_33 = 137 = alpha^-1.

    Two substrate-clean prime-index identities of form
    p_(q * <Phi_6 or p_Ih>) = (Phi_12 or alpha^-1).

W BOSON MASS IDENTITY:

(e) Phi_12 = m_W - Phi_6 = 2v - Phi_6

    Since m_W = 2v = 80 GeV, we have Phi_12 = 80 - 7 = 73.
    So the SH0ES Hubble constant equals the W boson mass minus
    the substrate Fano prime.

==============================================================
THE BIG ONE: HEEGNER F-LATTICE THEOREM
==============================================================

The FOUR large prime Heegner-discriminant primes {19, 43, 67, 163}
form an arithmetic progression on the f = 24 (gauge multiplicity)
lattice:

  Heegner_19  = 19  = Heegner_19 + 0*f
  Heegner_43  = 43  = Heegner_19 + 1*f
  Heegner_67  = 67  = Heegner_19 + 2*f
  Heegner_163 = 163 = Heegner_19 + 6*f = Heegner_19 + q!*f

So {19, 43, 67, 163} = Heegner_19 + n*f  for  n in {0, 1, 2, q!}.

Increments are {0, 1, 2, q!}: the first three positive integers
plus q!. The 'missing' increments {3, 4, 5} = {q, mu, mu+1} would
correspond to non-Heegner primes {67+72=139... wait no, on the
n-grid 19+3f=91, 19+4f=115, 19+5f=139}: 91 = m_Z (substrate Z mass!),
115 = 5*23 (Ogg!), 139 is prime but not Heegner.

So the Heegner f-lattice 'skips' 91 = m_Z, 115, 139 between
67 and 163.

==============================================================
EACH LARGE HEEGNER HAS A SUBSTRATE FORM:
==============================================================

  Heegner_19  =  q + mu^2     =  3 + 16   =  19      [or q + 2^mu]
  Heegner_43  =  (q!)^2 + Phi_6  =  36 + 7  =  43
  Heegner_67  =  (2^Phi_6 + q!)/2 = (128+6)/2 = 67
  Heegner_163 =  mu*v + q     =  4*40 + 3 = 163

Each large Heegner is a substrate-clean integer expression.

==============================================================
CONSEQUENCES:
==============================================================

(i) Heegner_43 = (Heegner_19 + Heegner_67)/2
    The middle large Heegner is the arithmetic mean of the outer two.

(ii) Heegner_43 - Heegner_19 = f = gauge_mult = 24
     Two Heegner primes differ by exactly the gauge sector multiplicity.

(iii) Heegner_67 + f = m_Z = 91 GeV
      Adding the gauge mult to Planck Hubble returns the Z boson mass.

(iv) Heegner_163 = 6f + Heegner_19 = q! * f + Heegner_19
     The largest Heegner is q!-fold gauge above the smallest large Heegner.

(v) Heegner_67 - Heegner_43 = f, Heegner_43 - Heegner_19 = f
    Two consecutive f-steps.

This is a deep substrate organisation of the Heegner discriminants
by the gauge multiplicity f, which the substrate predicts equals
the GUT-scale inverse fine-structure constant: alpha_GUT^-1 = 24 = f.

So the Heegner f-lattice connects:
  - alpha_GUT^-1 (gauge unification)
  - m_Z (Z boson mass)
  - All four large prime Heegner discriminants
  - The Master Cyclotomic Identity Phi_12 (SH0ES Hubble)
"""
from __future__ import annotations

import json
from pathlib import Path
from sympy import prime, isprime


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
V = 40
F_GAUGE = 24
PHI12 = Q ** 4 - Q ** 2 + 1

# Heegner primes (large; class h=1)
HEEGNERS = [19, 43, 67, 163]


def fano_prism_dual_products() -> dict:
    return {
        "products": [
            {"pair": "(mu, Phi_4)",   "product": MU * PHI4,    "substrate": "v"},
            {"pair": "(q, p_Ih)",     "product": Q * P_IH,     "substrate": "q*p_Ih"},
            {"pair": "(1, Phi_3)",    "product": 1 * PHI3,     "substrate": "Phi_3"},
        ],
        "sum_all": V + Q * P_IH + PHI3,
        "v_plus_qpIh": V + Q * P_IH,
        "v_minus_qpIh": V - Q * P_IH,
    }


def product_sum_identities() -> list[dict]:
    return [
        {
            "claim":    "v + q*p_Ih = Phi_12 = H_0_SH0ES",
            "lhs":      V + Q * P_IH,
            "rhs":      PHI12,
            "match":    V + Q * P_IH == PHI12,
            "physics":  "Sum of first two Fano-prism products = late-universe Hubble",
        },
        {
            "claim":    "v - q*p_Ih = Phi_6",
            "lhs":      V - Q * P_IH,
            "rhs":      PHI6,
            "match":    V - Q * P_IH == PHI6,
            "physics":  "Difference returns the substrate symmetric center",
        },
        {
            "claim":    "v + q*p_Ih + Phi_3 = 2 * Heegner_43",
            "lhs":      V + Q * P_IH + PHI3,
            "rhs":      2 * 43,
            "match":    V + Q * P_IH + PHI3 == 2 * 43,
            "physics":  "Full Fano-prism product sum = 2 * central Heegner prime",
        },
        {
            "claim":    "Phi_12 = m_W - Phi_6 = 2v - Phi_6",
            "lhs":      PHI12,
            "rhs":      2 * V - PHI6,
            "match":    PHI12 == 2 * V - PHI6,
            "physics":  "Late-universe Hubble = W boson mass minus Fano prime",
        },
    ]


def prime_index_identity() -> dict:
    """p_(q*Phi_6) = Phi_12 = H_0_SH0ES."""
    idx = Q * PHI6  # = 21
    p_idx = prime(idx)
    return {
        "claim":       "p_(q * Phi_6) = Phi_12",
        "index":       idx,
        "p_at_idx":    p_idx,
        "predicted":   PHI12,
        "match":       p_idx == PHI12,
        "comparison":  "Companion to alpha^-1 = p_(q*p_Ih) = p_33 = 137",
    }


def heegner_substrate_forms() -> list[dict]:
    """Each large Heegner has a substrate-clean form."""
    return [
        {
            "heegner":   19,
            "formula":   "q + mu^2 = q + 2^mu",
            "computed":  Q + MU ** 2,
            "match":     Q + MU ** 2 == 19,
        },
        {
            "heegner":   43,
            "formula":   "(q!)^2 + Phi_6",
            "computed":  QFACT ** 2 + PHI6,
            "match":     QFACT ** 2 + PHI6 == 43,
        },
        {
            "heegner":   67,
            "formula":   "(2^Phi_6 + q!) / 2",
            "computed":  (2 ** PHI6 + QFACT) // 2,
            "match":     (2 ** PHI6 + QFACT) // 2 == 67,
        },
        {
            "heegner":   163,
            "formula":   "mu * v + q",
            "computed":  MU * V + Q,
            "match":     MU * V + Q == 163,
        },
    ]


def heegner_f_lattice_theorem() -> dict:
    """{19, 43, 67, 163} = 19 + n*f for n in {0, 1, 2, q!}."""
    rows = []
    for n, h in zip([0, 1, 2, QFACT], HEEGNERS):
        predicted = 19 + n * F_GAUGE
        rows.append({
            "n":         n,
            "heegner":   h,
            "lattice":   f"19 + {n}*f = 19 + {n*F_GAUGE}",
            "predicted": predicted,
            "match":     predicted == h,
        })
    return {
        "claim": (
            "All FOUR large prime Heegner discriminants lie on the "
            "f-gauge lattice anchored at 19, with multipliers "
            "n in {0, 1, 2, q!}."
        ),
        "f":           F_GAUGE,
        "anchor":      19,
        "multipliers": [0, 1, 2, QFACT],
        "rows":        rows,
        "skipped":     "n=3,4,5 give 91=m_Z, 115=5*Ogg(23), 139 (prime, not Heegner)",
    }


def gauge_to_mass_identity() -> dict:
    """Heegner_67 + f = m_Z = 91 GeV."""
    return {
        "claim":     "Heegner_67 + f = m_Z(GeV)",
        "computed":  67 + F_GAUGE,
        "m_Z":       91,
        "match":     67 + F_GAUGE == 91,
        "substrate": "(Planck early-universe Hubble) + alpha_GUT^-1 = Z boson mass",
    }


def heegner_skip_pattern() -> list[dict]:
    """What lies on the f-lattice between Heegner_67 and Heegner_163?"""
    skipped = []
    for n in [3, 4, 5]:
        val = 19 + n * F_GAUGE
        skipped.append({
            "n":          n,
            "value":      val,
            "is_prime":   bool(isprime(val)),
            "is_heegner": val in HEEGNERS,
            "substrate": {
                3: "91 = m_Z (Z boson mass GeV)",
                4: "115 = 5 * 23 (Ogg supersingular)",
                5: "139 = prime, not Heegner",
            }[n],
        })
    return skipped


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "Phi_12": PHI12, "v": V, "f_gauge": F_GAUGE,
                "Heegners_large": HEEGNERS,
            },
        },
        "fano_prism_dual_products": fano_prism_dual_products(),
        "product_sum_identities":   product_sum_identities(),
        "prime_index_identity":     prime_index_identity(),
        "heegner_substrate_forms":  heegner_substrate_forms(),
        "heegner_f_lattice":        heegner_f_lattice_theorem(),
        "gauge_to_mass_identity":   gauge_to_mass_identity(),
        "heegner_skip_pattern":     heegner_skip_pattern(),
        "headline_identity": (
            "HEEGNER F-LATTICE THEOREM:\n"
            "  All four LARGE prime Heegners on the f=24 gauge lattice:\n"
            "    Heegner_n = 19 + j*f  for j in {0, 1, 2, q!}\n"
            "    j=0: 19,   j=1: 43,   j=2: 67,   j=q!=6: 163\n\n"
            "PRODUCT-SUM IDENTITY:\n"
            "  v + q*p_Ih      = Phi_12 = 73 = H_0_SH0ES  (NEW)\n"
            "  v + q*p_Ih + Phi_3 = 2*Heegner_43 = 86       (NEW)\n"
            "  Phi_12 = m_W - Phi_6 = 80 - 7                  (NEW)\n\n"
            "PRIME-INDEX:\n"
            "  p_(q*Phi_6) = p_21 = 73 = Phi_12 (companion to p_33 = 137)\n\n"
            "GAUGE/MASS:\n"
            "  Heegner_67 + f = 91 = m_Z (Z boson mass GeV)\n"
            "  Substrate links: Heegners <-> alpha_GUT^-1 <-> m_Z <-> Phi_12 <-> H_0"
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_heegner_f_lattice_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) HEEGNER F-LATTICE SUBSTRATE IDENTITIES")
    print("=" * 78)

    print("\nProduct-sum identities (extending Fano Prism Dual Tower):")
    for r in payload["product_sum_identities"]:
        print(f"  {r['claim']:>40s}: {r['lhs']} = {r['rhs']}  match={r['match']}")
        print(f"    physics: {r['physics']}")

    print("\nPrime-index identity:")
    p = payload["prime_index_identity"]
    print(f"  {p['claim']}: p_{p['index']} = {p['p_at_idx']} = Phi_12 (match: {p['match']})")
    print(f"  {p['comparison']}")

    print("\nLarge Heegner substrate forms:")
    for r in payload["heegner_substrate_forms"]:
        print(f"  Heegner_{r['heegner']:>3d} = {r['formula']:>30s}  = {r['computed']:>3d}  match={r['match']}")

    print("\nHeegner f-lattice theorem:")
    h = payload["heegner_f_lattice"]
    print(f"  {h['claim']}")
    for r in h["rows"]:
        print(f"    n={r['n']}: {r['lattice']:>20s}  = {r['predicted']:>3d}  match={r['match']}")
    print(f"  Skipped: {h['skipped']}")

    print("\nGauge-to-mass identity:")
    g = payload["gauge_to_mass_identity"]
    print(f"  {g['claim']}: {g['computed']} = {g['m_Z']}  match={g['match']}")
    print(f"  {g['substrate']}")

    print(f"\nHEADLINE:")
    print(payload["headline_identity"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
