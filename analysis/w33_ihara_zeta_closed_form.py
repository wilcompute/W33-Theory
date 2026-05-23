"""W(3,3) IHARA ZETA FUNCTION IN CLOSED SUBSTRATE-PRIMITIVE FORM.

Direct successor to the Hashimoto sector-projected spectrum theorem
(commit 88899d6b).  The Ihara--Bass identity combined with the W(3,3)
adjacency spectrum {12, +2, -4} immediately yields the FULL Ihara zeta
function of W(3,3) as an explicit polynomial in substrate primitives.

THE CLOSED FORM.
================

For W(3,3): valency k+1 = 12, k-1 = p_Ih = 11, n = v = 40,
m = |E| = 240, m - n = 200.

    zeta_{W33}^{-1}(u)
      = (1 - u^2)^{m-n}  *  prod over A-eigenvalues lambda
                            (1 - lambda u + (k-1) u^2)^{mult(lambda)}
      = (1 - u^2)^{200}
        * (1 - u)(1 - 11 u)               (Perron factor)
        * (1 - 2 u + 11 u^2)^{24}         (gauge factor, mult f)
        * (1 + 4 u + 11 u^2)^{15}         (chiral factor, mult g).

Total degree: 2*200 + 2 + 2*24 + 2*15 = 480 = 2 |E|.  (Verified.)

SUBSTRATE-PRIMITIVE DISCRIMINANTS.
==================================

Each quadratic factor has a discriminant lambda^2 - 4(k-1):

    Perron  (1 - 12 u + 11 u^2):  disc = 144 - 44 = +100 = Phi_4^2 = 10^2
    Gauge   (1 - 2 u + 11 u^2):   disc =   4 - 44 = -40  = -v  (vertex count)
    Chiral  (1 + 4 u + 11 u^2):   disc =  16 - 44 = -28  = -mu Phi_6
                                                          = -n_even (Klein bitangents)

So the discriminants of the three (Perron, gauge, chiral) Ihara zeta
factors are EXACTLY (Phi_4^2, -v, -n_even) -- three core substrate
primitives.  The negative gauge and chiral discriminants confirm both
factors are irreducible over R, forcing the corresponding complex
Hashimoto eigenvalues.

IHARA-RAMANUJAN STATEMENT (Graph Riemann Hypothesis for W(3,3)).
================================================================

The non-trivial zeros of zeta_{W33}^{-1}(u) -- i.e., the zeros of the
gauge and chiral quadratic factors -- all lie on

    |u| = 1 / sqrt(k - 1) = 1 / sqrt(11) = 1 / sqrt(p_Ih).

W(3,3) therefore satisfies the graph Riemann hypothesis (Ihara--Ramanujan)
in the strongest possible sense: both non-trivial sectors saturate the
bound, with complex zeros on the same circle of radius 1/sqrt(11).

NON-BACKTRACKING CLOSED-WALK COUNT (graph prime number theorem).
================================================================

Writing N_n = #{ length-n non-backtracking closed walks } = tr(B^n) =
sum over Hashimoto eigenvalues u_i with multiplicities:

    N_1 = 0                                   (no length-1 NB closed walks)
    N_2 = 0                                   (no length-2 NB closed walks)
    N_3 = 960  = mu * |E|                     (triangle contribution)
                = 6 * (number of triangles)
                = 160 * 6 = #triangles times q!
    N_4 = 13920
    N_5 = 181440 = |E| * q^q * n_even
                 = 240 * 27 * 28
    N_6 = 1818240, approx p_Ih^6 = 11^6 = 1771561.

For large n: N_n approx p_Ih^n = 11^n, the Perron-dominated growth.
This is the graph prime number theorem for W(3,3): the number of
length-n non-backtracking closed walks grows exponentially with base
exactly the Ihara prime p_Ih = 11.

SPECIAL VALUES OF zeta^{-1}(u).
================================

    zeta^{-1}(0) = 1 (trivial)
    zeta^{-1}(1) = 0 (Perron pole of zeta)
    zeta^{-1}(-1) = 0 (anti-Perron pole of zeta)
    zeta^{-1}(1/11) = 0 (Perron pair zero)

The zeros of zeta_{W33}^{-1} therefore distribute as:
    * 200 doubled trivial zeros at u = +/-1 (backtrack stabiliser),
    * 2 Perron-pair zeros at u = 1 and u = 1/11,
    * 24 complex-conjugate gauge zeros on |u| = 1/sqrt(11),
    * 15 complex-conjugate chiral zeros on |u| = 1/sqrt(11).

LOG-DERIVATIVE.
================

d/du log zeta_{W33}(u) = sum_p sum_{j>=1} deg(p) * u^{j deg(p) - 1}

where the outer sum is over PRIME (= primitive, NB, equivalence class
of) closed walks.  Substituting the closed form gives an explicit
power series whose coefficients are the closed-walk counts above.
"""
from __future__ import annotations

import cmath
import json
import math
from pathlib import Path


# Substrate constants
Q = 3
QP1 = 4
MU = QP1
LAM_SRG = Q - 1
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
V = 40
EDGES = 240
F = 24
G_NEG = 15
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
CSASZAR_COUNT = Q + 2
N_EVEN = 28  # Klein bitangents


def zeta_factor_data() -> list[dict]:
    """Three irreducible factor families of zeta_{W33}^{-1}(u)."""
    return [
        {
            "name": "Perron",
            "polynomial": "1 - 12 u + 11 u^2 = (1 - u)(1 - 11 u)",
            "lambda_A": 12,
            "multiplicity_in_zeta_inverse": 1,
            "discriminant": 144 - 44,
            "discriminant_substrate": "Phi_4^2 = 10^2 = 100",
            "factors_over_Q": True,
            "real_zeros": [1.0, 1.0 / 11.0],
        },
        {
            "name": "gauge",
            "polynomial": "1 - 2 u + 11 u^2",
            "lambda_A": 2,
            "multiplicity_in_zeta_inverse": F,
            "discriminant": 4 - 44,
            "discriminant_substrate": "-v (vertex count)",
            "factors_over_Q": False,
            "complex_zeros": ["(1 +/- i sqrt(10))/11"],
            "modulus_of_zeros": 1.0 / math.sqrt(P_IH),
        },
        {
            "name": "chiral",
            "polynomial": "1 + 4 u + 11 u^2",
            "lambda_A": -4,
            "multiplicity_in_zeta_inverse": G_NEG,
            "discriminant": 16 - 44,
            "discriminant_substrate": "-mu Phi_6 = -n_even (Klein bitangent count)",
            "factors_over_Q": False,
            "complex_zeros": ["(-2 +/- i sqrt(7))/11"],
            "modulus_of_zeros": 1.0 / math.sqrt(P_IH),
        },
    ]


def closed_walk_counts(N_max: int = 8) -> list[dict]:
    """N_n = tr(B^n) computed from sector eigenvalues."""
    eigvals = [
        (11.0, 1), (1.0, 1),                          # Perron pair
        (complex(1.0, math.sqrt(10.0)), F),           # gauge complex
        (complex(1.0, -math.sqrt(10.0)), F),
        (complex(-2.0, math.sqrt(7.0)), G_NEG),       # chiral complex
        (complex(-2.0, -math.sqrt(7.0)), G_NEG),
        (1.0, EDGES - V), (-1.0, EDGES - V),          # backtrack stabilisers
    ]
    rows = []
    for n in range(1, N_max + 1):
        total = sum(m * (u ** n) for u, m in eigvals)
        val = int(round(total.real if isinstance(total, complex) else total))
        rows.append({"n": n, "N_n": val})
    return rows


def substrate_factorisations_of_N3_N5() -> dict:
    return {
        "N_3": {
            "value": 960,
            "factorisations": [
                "mu * |E| = 4 * 240",
                "q! * #triangles = 6 * 160",
                "(q+1) * E_8 root count",
            ],
            "interpretation": "Each of 160 triangles yields 6 NB closed walks (3 starts * 2 directions).",
        },
        "N_5": {
            "value": 181440,
            "factorisations": [
                "|E| * q^q * n_even = 240 * 27 * 28",
                "240 * 756",
            ],
            "interpretation": "Substrate factor n_even = Klein bitangents in length-5 NB walk count.",
        },
    }


def ihara_ramanujan_summary() -> dict:
    return {
        "ramanujan_radius_squared": 1.0 / P_IH,
        "ramanujan_radius": 1.0 / math.sqrt(P_IH),
        "substrate_form": "|u| = 1 / sqrt(p_Ih) = 1/sqrt(11)",
        "complex_zeros_per_sector": {"gauge": 2 * F, "chiral": 2 * G_NEG},
        "all_complex_zeros_on_ramanujan_circle": True,
        "graph_riemann_hypothesis": (
            "All non-trivial zeros of zeta_{W33}^{-1}(u) lie on the circle "
            "|u| = 1/sqrt(p_Ih), with W(3,3) saturating the Ihara-Ramanujan bound."
        ),
    }


def total_degree_check() -> dict:
    deg = 2 * (EDGES - V) + 2 + 2 * F + 2 * G_NEG
    return {
        "total_degree": deg,
        "should_equal_2E": 2 * EDGES,
        "match": deg == 2 * EDGES,
    }


def special_values_zeta_inverse() -> dict:
    return {
        "zeta_inv_at_0": 1,
        "zeta_inv_at_plus_1": "0 (anti-Perron via (1-u^2)^200)",
        "zeta_inv_at_minus_1": "0 (anti-Perron via (1-u^2)^200)",
        "zeta_inv_at_1_over_11": "0 (Perron pair zero)",
    }


def build_payload() -> dict:
    factors = zeta_factor_data()
    walks = closed_walk_counts(8)
    return {
        "header": {
            "k_minus_1": P_IH, "vertices": V, "edges": EDGES,
            "f_mult": F, "g_neg_mult": G_NEG,
        },
        "closed_form": {
            "zeta_inverse_factorization": (
                "zeta_{W33}^{-1}(u) = (1-u^2)^{200} * (1-u)(1-11u) "
                "* (1-2u+11u^2)^{24} * (1+4u+11u^2)^{15}"
            ),
            "total_degree": 2 * EDGES,
        },
        "zeta_factors": factors,
        "non_backtracking_closed_walk_counts": walks,
        "substrate_factorisations": substrate_factorisations_of_N3_N5(),
        "ihara_ramanujan_summary": ihara_ramanujan_summary(),
        "total_degree_check": total_degree_check(),
        "special_values": special_values_zeta_inverse(),
        "theorem": (
            "W(3,3) Ihara Zeta Closed-Form Theorem.  The reciprocal Ihara "
            "zeta function of W(3,3) factors over Z[u] as "
            "zeta^{-1}(u) = (1-u^2)^{200} (1-u)(1-11u) (1-2u+11u^2)^{24} "
            "(1+4u+11u^2)^{15}.  The three Ihara quadratic factors have "
            "discriminants exactly (Phi_4^2, -v, -mu Phi_6) = "
            "(100, -40, -28) -- pure substrate primitives.  All complex "
            "zeros lie on |u| = 1/sqrt(p_Ih) = 1/sqrt(11), so W(3,3) "
            "saturates the Ihara-Ramanujan (graph Riemann hypothesis) "
            "bound.  The non-backtracking closed-walk counts N_n = tr(B^n) "
            "begin 0, 0, mu*|E|, ... and grow asymptotically as p_Ih^n -- "
            "the graph prime number theorem for W(3,3)."
        ),
        "honesty_boundary": (
            "The Ihara-Bass identity is a classical theorem (Ihara 1966; "
            "Bass 1992).  The substrate-primitive identification of the "
            "discriminants (Phi_4^2, -v, -mu Phi_6) and the walk-count "
            "factorisations (mu |E|, |E| q^q n_even) are exact arithmetic "
            "consequences.  The closed form here is therefore a "
            "rigorously substantiated, NOT a conjectured, identity."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_ihara_zeta_closed_form.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) IHARA ZETA CLOSED FORM (SUBSTRATE-PRIMITIVE)")
    print("=" * 78)
    print(f"\n{payload['closed_form']['zeta_inverse_factorization']}")
    print(f"total degree = {payload['closed_form']['total_degree']} = 2|E|")
    print("\nQuadratic factor discriminants (substrate identification):")
    for fac in payload["zeta_factors"]:
        print(f"  {fac['name']:>7s}: {fac['polynomial']:>30s}   "
              f"disc = {fac['discriminant']:>4d} = {fac['discriminant_substrate']}")
    print("\nIhara-Ramanujan: all complex zeros on |u| = 1/sqrt(11):")
    print(f"  ramanujan radius = 1/sqrt(p_Ih) = {payload['ihara_ramanujan_summary']['ramanujan_radius']:.6f}")
    print("\nNon-backtracking closed-walk counts:")
    for w in payload["non_backtracking_closed_walk_counts"]:
        print(f"  N_{w['n']} = {w['N_n']:>10d}")
    print("\nSubstrate factorisations:")
    for k, v in payload["substrate_factorisations"].items():
        print(f"  {k} = {v['value']} = {v['factorisations'][0]}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
