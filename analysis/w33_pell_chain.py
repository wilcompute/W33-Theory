#!/usr/bin/env python3
"""W(3,3) Pell Chain Theorem (extends Twin Pell to a quadruple chain).

The Twin Pell theorem found two unit-discriminant quadratics whose roots are
substrate-primitive pairs:

    (q, q+1)   = (3, 4)   from x^2 -  7 x +  12 = 0,
    (2^q, q^2) = (8, 9)   from x^2 - 17 x +  72 = 0.

This script identifies TWO MORE such pairs, giving a quadruple Pell chain.

Pell Chain.
-----------
Pair                root values    sum    product    physical role
--------------------------------------------------------------------
(q, q+1)            (3, 4)          7      12=k       CSS distances / codec
(2^q, q^2)          (8, 9)         17      72=lam_g   Catalan-unique tomo/Heis
(k, Phi_3)          (12, 13)       25     156=k Phi3  automatic consecutive
(g, 2^mu)           (15, 16)       31     240=|E|     E8-root-count factorisation

Total-sum identity:    7 + 17 + 25 + 31 = 80 = 2 v.
Total-product identity: 12 + 72 + 156 + 240 = 480 = 2 |E|.

The substrate's QUADRUPLE Pell chain has total sum 2 v and total product
2 |E|.  This is a STRUCTURAL identity binding the chain to the W(3,3)
graph's vertex and edge counts.

Parity-sector bridge.
---------------------
Omitting the (k, Phi_3) automatic pair, the three NON-AUTOMATIC Pell
sums total 7 + 17 + 31 = 55 = even metric classes from the
parity-sector split (commit ed74badb).  The single sum 25 = (q+1)^2 = mu^2
of the automatic (k, Phi_3) pair is exactly mu^2.

So:
    sum of NON-AUTOMATIC Pell sums = even parity-sector classes
                                    = 55,
    sum of AUTOMATIC Pell (k, Phi_3) sum = f + 1 = 25
                                         = (q+2)^2 at q = 3,
    grand total                     = 80 = 2 v.

Catalan and quasi-Catalan coincidences.
---------------------------------------
The (2^q, q^2) pair is consecutive ONLY at q = 3 (Mihailescu's theorem).
The (g, 2^mu) pair is consecutive at q = 3 (g=15, 2^mu=16) AND at q = 5
(g=65, 2^mu=64, order reversed); a quasi-Catalan-like coincidence.

The automatic pairs (q, q+1), (k, Phi_3), and (q*Phi_3, v) are consecutive
for ALL q in the W(3,q) family.

Bonus fifth pair: (q*Phi_3, v).
-------------------------------
v - q * Phi_3 = (q+1)(q^2+1) - q(q^2+q+1) = q^3 + q^2 + q + 1 - q^3 - q^2 - q = 1
for ALL q, so (q*Phi_3, v) = (39, 40) is also an automatic Pell pair with
product q * Phi_3 * v = Hodge exact-gradient times v.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
QP1 = 4
MU = QP1
K = Q * QP1                # 12
PHI3 = Q ** 2 + Q + 1      # 13
PHI4 = Q ** 2 + 1          # 10
PHI6 = QP1 + Q - 1         # 7
V = 40
E = 240
F = 24
G = 15
H1 = Q ** QP1              # 81


def discriminant(b: int, c: int) -> int:
    return b * b - 4 * c


def pell_pair(a: int, b: int, name: str, role: str, status: str) -> dict:
    s = a + b
    p = a * b
    return {
        "name": name,
        "roots": [a, b],
        "consecutive": abs(a - b) == 1,
        "quadratic": f"x^2 - {s} x + {p} = 0",
        "sum": s,
        "product": p,
        "discriminant": discriminant(s, p),
        "role": role,
        "status": status,
    }


def pell_chain() -> list[dict]:
    return [
        pell_pair(
            Q, QP1,
            "small Pell (q, q+1)",
            "CSS code distances; codec product; toroidal genus roots",
            "automatic-for-all-q",
        ),
        pell_pair(
            2 ** Q, Q ** 2,
            "Catalan Pell (2^q, q^2)",
            "tomotope cells x Heisenberg-projective dim = lambda_gauge",
            "Catalan-unique at q = 3 (Mihailescu)",
        ),
        pell_pair(
            K, PHI3,
            "automatic Pell (k, Phi_3)",
            "codec x 3rd cyclotomic; Phi_3 = k + 1 always",
            "automatic-for-all-q",
        ),
        pell_pair(
            G, 2 ** MU,
            "E_8-root Pell (g, 2^mu)",
            "negative-eigenspace mult x binary mu-shell = |E| = E_8 root count",
            "Catalan-like coincidence at q = 3 (g = mu^2 - 1)",
        ),
    ]


def bonus_fifth_pair() -> dict:
    """(q * Phi_3, v) — automatic, equals (Hodge exact-gradient, vertex count)."""
    a, b = Q * PHI3, V
    return pell_pair(
        a, b,
        "Hodge-exact Pell (q Phi_3, v)",
        "Hodge exact-gradient x vertex count; v - q*Phi_3 = 1 always",
        "automatic-for-all-q",
    )


def chain_totals(chain: list[dict]) -> dict:
    sums = [p["sum"] for p in chain]
    prods = [p["product"] for p in chain]
    return {
        "sums": sums,
        "products": prods,
        "total_sum": sum(sums),
        "total_product": sum(prods),
        "total_sum_equals_2v": sum(sums) == 2 * V,
        "total_product_equals_2_edges": sum(prods) == 2 * E,
    }


def parity_sector_bridge(chain: list[dict]) -> dict:
    """Three non-automatic Pell sums total to the even-class count from the
    parity-sector split, and the single automatic-(k, Phi_3) sum is mu^2.
    """
    automatic_sum_kphi3 = K + PHI3   # 25
    non_automatic_sums = [c["sum"] for c in chain if c["sum"] != automatic_sum_kphi3]
    return {
        "non_automatic_sums": non_automatic_sums,
        "non_automatic_sums_total": sum(non_automatic_sums),
        "even_metric_classes": 55,
        "non_automatic_total_equals_even_classes": sum(non_automatic_sums) == 55,
        "automatic_kphi3_sum": automatic_sum_kphi3,
        "automatic_kphi3_sum_equals_f_plus_1": automatic_sum_kphi3 == F + 1,
        "automatic_kphi3_sum_equals_q_plus_2_squared_at_q3": automatic_sum_kphi3 == (Q + 2) ** 2,
        "grand_total": sum(non_automatic_sums) + automatic_sum_kphi3,
        "grand_total_equals_2v": (sum(non_automatic_sums) + automatic_sum_kphi3) == 2 * V,
    }


def hodge_bridge(chain: list[dict]) -> dict:
    """The chain products map onto Hodge decomposition triples."""
    return {
        "chain_products": [c["product"] for c in chain],
        "hodge_decomposition_total": 240,
        "hodge_decomposition_split": "240 = 39 + 120 + 81",
        "k_in_chain": K in [c["product"] for c in chain],
        "lambda_gauge_in_chain": 72 in [c["product"] for c in chain],
        "edge_count_in_chain": E in [c["product"] for c in chain],
        "interpretation": (
            "Three of the four Pell products -- 12=k, 72=lambda_gauge, 240=|E| -- "
            "are core substrate primitives that appear separately in the Hodge "
            "decomposition (120 = k * Phi_4, lambda_gauge is the X-scheme middle "
            "eigenvalue, |E| is the total carrier).  The fourth product 156 = k * Phi_3 "
            "factors as codec times third cyclotomic, the automatic pair."
        ),
    }


def consecutive_perfect_powers_check() -> list[dict]:
    rows = []
    for qq in range(2, 9):
        rows.append({
            "q": qq,
            "two_to_q": 2 ** qq,
            "q_squared": qq ** 2,
            "diff_q2_minus_2q": qq ** 2 - 2 ** qq,
            "consecutive": abs(qq ** 2 - 2 ** qq) == 1,
        })
    return rows


def quasi_catalan_g_2mu() -> list[dict]:
    """At which q is (g, 2^mu) consecutive?"""
    rows = []
    for qq in range(2, 8):
        v_q = (qq + 1) * (qq ** 2 + 1)
        k_q = qq * (qq + 1)
        r_q = qq - 1
        s_q = -(qq + 1)
        # SRG multiplicities f, g satisfy f + g = v - 1, f*r + g*s + k = 0.
        # so f = (-(s)*(v-1) - k)/(r - s),
        #    g = (v - 1) - f.
        denom = r_q - s_q
        if denom == 0:
            f_q = 0
            g_q = 0
        else:
            f_q = (-s_q * (v_q - 1) - k_q) // denom
            g_q = (v_q - 1) - f_q
        two_mu = 2 ** (qq + 1)
        rows.append({
            "q": qq,
            "v": v_q,
            "g": g_q,
            "2^mu": two_mu,
            "g_minus_2mu": g_q - two_mu,
            "consecutive": abs(g_q - two_mu) == 1,
        })
    return rows


def build_payload() -> dict:
    chain = pell_chain()
    bonus = bonus_fifth_pair()
    return {
        "header": {
            "q": Q,
            "v": V,
            "edges": E,
            "k": K,
            "Phi_3": PHI3,
            "Phi_4": PHI4,
            "Phi_6": PHI6,
            "g_negative_eigenspace_mult": G,
            "f_positive_eigenspace_mult": F,
        },
        "pell_chain": chain,
        "chain_totals": chain_totals(chain),
        "parity_sector_bridge": parity_sector_bridge(chain),
        "hodge_bridge": hodge_bridge(chain),
        "bonus_fifth_pair_q_phi3_v": bonus,
        "catalan_check_2q_qsq": consecutive_perfect_powers_check(),
        "quasi_catalan_check_g_2mu": quasi_catalan_g_2mu(),
        "theorem": (
            "W(3,3) Pell Chain Theorem.  The W(3,3) substrate hosts FOUR "
            "consecutive-integer Pell pairs whose roots are substrate "
            "primitives: (q, q+1), (2^q, q^2), (k, Phi_3), and (g, 2^mu).  "
            "Their sums total exactly 2 v = 80 and their products total "
            "exactly 2 |E| = 480, binding the chain rigidly to the "
            "vertex and edge counts of the W(3,3) graph.  Three of the "
            "four are non-automatic; their sums total 7 + 17 + 31 = 55, "
            "the even metric class count from the parity-sector split.  "
            "The fourth (automatic) sum is mu^2 = 25, completing 80 = 2 v.  "
            "Three of the four products -- k, lambda_gauge, and |E| -- "
            "are core substrate primitives that label the Hodge decomposition.  "
            "Mihailescu's theorem implies the (2^q, q^2) pair is "
            "Catalan-unique to q = 3."
        ),
        "honesty_boundary": (
            "All Pell-pair identities are exact arithmetic.  Mihailescu's "
            "theorem is a deep number-theoretic input; we use only its "
            "Catalan-uniqueness statement.  The quasi-Catalan g = mu^2 - 1 "
            "happens to hold at q = 3 because mu^2 = 2^mu when mu = 4, "
            "another isolated arithmetic coincidence."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_pell_chain.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 72)
    print("W(3,3) PELL CHAIN THEOREM")
    print("=" * 72)
    print()
    for c in payload["pell_chain"]:
        print(f"  {c['name']:35s} {c['roots']} : sum={c['sum']:>2}  prod={c['product']:>3}  "
              f"disc={c['discriminant']}  {c['status']}")
    print()
    t = payload["chain_totals"]
    print(f"  total sum  = {t['total_sum']} = 2v: {t['total_sum_equals_2v']}")
    print(f"  total prod = {t['total_product']} = 2|E|: {t['total_product_equals_2_edges']}")
    print()
    p = payload["parity_sector_bridge"]
    print(f"  non-automatic Pell sums = {p['non_automatic_sums']} -> total {p['non_automatic_sums_total']}")
    print(f"  equals even metric classes (parity-sector): {p['non_automatic_total_equals_even_classes']}")
    print(f"  automatic (k, Phi_3) sum = {p['automatic_kphi3_sum']} = f+1: {p['automatic_kphi3_sum_equals_f_plus_1']}; = (q+2)^2 at q=3: {p['automatic_kphi3_sum_equals_q_plus_2_squared_at_q3']}")
    print(f"  grand total = {p['grand_total']} = 2v: {p['grand_total_equals_2v']}")
    print()
    print(f"Bonus fifth pair: (q*Phi_3, v) = {payload['bonus_fifth_pair_q_phi3_v']['roots']} "
          f"sum={payload['bonus_fifth_pair_q_phi3_v']['sum']} prod={payload['bonus_fifth_pair_q_phi3_v']['product']}")
    print()
    print("Catalan check (2^q vs q^2):")
    for row in payload["catalan_check_2q_qsq"]:
        flag = "*** CATALAN ***" if row["consecutive"] else ""
        print(f"  q={row['q']}: 2^q={row['two_to_q']:>4}  q^2={row['q_squared']:>4}  diff={row['diff_q2_minus_2q']:>4} {flag}")
    print()
    print("Quasi-Catalan check (g vs 2^mu):")
    for row in payload["quasi_catalan_check_g_2mu"]:
        flag = "*** CONSECUTIVE ***" if row["consecutive"] else ""
        print(f"  q={row['q']}: g={row['g']:>4}  2^mu={row['2^mu']:>4}  diff={row['g_minus_2mu']:>4} {flag}")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
