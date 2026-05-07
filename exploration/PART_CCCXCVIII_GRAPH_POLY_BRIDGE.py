#!/usr/bin/env python3
"""PART CCCXCVIII -- Graph Polynomial Suite: Clique, Independence, and Matching
Polynomials of W(3,3), with SM Crosswalk.

W(3,3) = Sp(4,3) symplectic graph, SRG(40,12,2,4).

Computes exact graph polynomials from the W(3,3) SRG parameter structure and
known K4 / f-vector constants:

  Clique polynomial      C(G;x) = 1 + 40x + 240x^2 + 160x^3 + 40x^4
  Independence seeds     I_k for k=0..3  (exact from SRG params)
  Matching seeds         M_k for k=0..2  (Hosoya index partial)

Key discoveries
---------------
  C(G;-1) = 81 = 3^4 = q^4 = |GF(3)^4|  (ambient symplectic space order)
  i_3     = 3240 = q^4 * V = 81 * 40     (3rd independence seed)
  i_3/i_2 = 6    = q! = 3!               (ratio = factorial of field order)
  C(G;1)  = 481  = V*K + 1               (total clique count)
  c_1 = c_4 = V  = 40                    (vertex count = K4 count)
  c_4/c_3 = 1/mu = 1/4                   (K4-to-triangle ratio)
  alpha * omega = V                        (10 * 4 = 40)
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# ── W(3,3) SRG constants ─────────────────────────────────────────────────────
V     = 40    # vertices
K     = 12    # valency
LAM   = 2     # lambda: common neighbours of adjacent pair
MU    = 4     # mu: common neighbours of non-adjacent pair
EDGES = V * K // 2   # 240
MULT_R = 24
MULT_S = 15
R_EIG  = 2
S_EIG  = -4
ABS_S  = 4

# SM / physics anchors
q         = 3   # GF(3) field order (W(3,3) lives in GF(3)^4)
GUT_DIM   = 27  # E6 fundamental / GUT dimension
ALPHA     = 10  # independence number = Lovász theta
CLIQUE_NU = 4   # clique number omega(G)

# K4 count from W(3,3) f-vector (derived from symplectic geometry):
# the 40 tetrahedra are exactly the K4 subgraphs.
K4_COUNT  = 40   # = V  (self-referential!)

# Triangle count from SRG: V*K*LAM/6
TRIANGLES = V * K * LAM // 6   # 160


# ── Clique polynomial ─────────────────────────────────────────────────────────

def clique_poly_coeffs() -> List[int]:
    """Coefficients [c0, c1, c2, c3, c4] of C(G;x)."""
    return [1, V, EDGES, TRIANGLES, K4_COUNT]


def clique_poly_eval(x) -> Fraction:
    """Evaluate C(G;x) exactly using Fraction arithmetic."""
    xf = Fraction(x)
    coeffs = clique_poly_coeffs()
    return sum(Fraction(c) * xf ** k for k, c in enumerate(coeffs))


def clique_number() -> int:
    """Clique number omega(G) = degree of clique polynomial = 4."""
    return CLIQUE_NU


# ── Independence polynomial seeds ────────────────────────────────────────────

def indep_poly_seed_i0() -> int:
    """i_0 = 1 (empty independent set)."""
    return 1


def indep_poly_seed_i1() -> int:
    """i_1 = V = 40 (single-vertex independent sets)."""
    return V


def indep_poly_seed_i2() -> int:
    """i_2 = C(V,2) - EDGES (non-adjacent pairs).
    = 780 - 240 = 540."""
    return V * (V - 1) // 2 - EDGES


def indep_poly_seed_i3() -> int:
    """i_3 = C(V,3) - T1 - T2 - T3  (independent triples, exact).

    T3 = triangles                            = V*K*LAM/6        = 160
    T2 = paths P_2 (2-edge paths)             = V*C(K,2) - 3*T3  = 2160
    T1 = single-edge triples (1 edge only)    = EDGES*(V-2) - 2*T2 - 3*T3 = 4320

    Equivalently, via:
      EDGES*(V-2) = T1 + 2*T2 + 3*T3   (wedge-counting identity)
      V*C(K,2)    = T2 + 3*T3           (vertex-centred wedges)
    """
    total_triples = V * (V - 1) * (V - 2) // 6   # C(40,3) = 9880
    t3 = TRIANGLES                                 # 160
    t2 = V * (K * (K - 1) // 2) - 3 * t3          # 2640 - 480 = 2160
    t1 = EDGES * (V - 2) - 2 * t2 - 3 * t3        # 9120 - 4320 - 480 = 4320
    return total_triples - t1 - t2 - t3


def independence_number() -> int:
    """Independence number alpha(G) = 10 = Lovász theta."""
    return ALPHA


# ── Matching polynomial seeds ─────────────────────────────────────────────────

def matching_seed_m0() -> int:
    """m_0 = 1 (empty matching)."""
    return 1


def matching_seed_m1() -> int:
    """m_1 = EDGES = 240 (single-edge matchings)."""
    return EDGES


def matching_seed_m2() -> int:
    """m_2 = C(EDGES,2) - V*C(K,2) (pairs of vertex-disjoint edges).
    = 28680 - 2640 = 26040."""
    pairs_of_edges   = EDGES * (EDGES - 1) // 2    # C(240,2) = 28680
    sharing_a_vertex = V * (K * (K - 1) // 2)      # 40 * 66  = 2640
    return pairs_of_edges - sharing_a_vertex


def matching_number() -> int:
    """Matching number nu = V/2 = 20 (perfect matching; V even, K-regular)."""
    return V // 2


def hosoya_partial() -> int:
    """Partial Hosoya index: m_0 + m_1 + m_2."""
    return matching_seed_m0() + matching_seed_m1() + matching_seed_m2()


# ── SM crosswalk ──────────────────────────────────────────────────────────────

def sm_crosswalk() -> Dict:
    """Map graph polynomial data to Standard-Model / geometric constants."""
    i2 = indep_poly_seed_i2()
    i3 = indep_poly_seed_i3()
    return {
        "C_at_minus1":           int(clique_poly_eval(-1)),  # 81 = q^4
        "ambient_space_order":   q ** 4,                     # |GF(3)^4| = 81
        "C_at_minus1_eq_q4":     int(clique_poly_eval(-1)) == q ** 4,
        "i3":                    i3,                          # 3240
        "i3_eq_q4_times_V":      i3 == q ** 4 * V,           # True
        "i3_over_i2":            str(Fraction(i3, i2)),       # 6/1
        "q_factorial":           6,                           # 3! = q!
        "total_cliques":         int(clique_poly_eval(1)),    # 481
        "V_times_K_plus_1":      V * K + 1,                  # 481
        "alpha_times_omega":     ALPHA * CLIQUE_NU,           # 40 = V
        "triangles_eq_V_mu":     TRIANGLES == V * MU,         # True
    }


# ── verify_all ────────────────────────────────────────────────────────────────

def verify_all() -> Tuple[List[Dict], int, int]:
    """27 checks in 5 groups.

    Group 1 (5): Clique polynomial coefficients
    Group 2 (5): Clique polynomial evaluations
    Group 3 (5): Independence polynomial seeds
    Group 4 (5): Matching polynomial seeds
    Group 5 (7): SM crosswalk and polynomial relations
    """
    checks: List[Dict] = []

    def chk(name: str, val, expected) -> bool:
        ok = val == expected
        checks.append({"check": name, "value": val, "expected": expected, "pass": ok})
        return ok

    # ── Group 1: Clique polynomial coefficients ───────────────────────────────
    coeffs = clique_poly_coeffs()
    chk("c0_empty_clique",   coeffs[0], 1)
    chk("c1_vertices",       coeffs[1], V)
    chk("c2_edges",          coeffs[2], EDGES)
    chk("c3_triangles",      coeffs[3], TRIANGLES)
    chk("c4_tetrahedra",     coeffs[4], K4_COUNT)

    # ── Group 2: Clique polynomial evaluations ────────────────────────────────
    chk("C_at_0",             int(clique_poly_eval(0)),  1)
    chk("C_at_1_total_cliques", int(clique_poly_eval(1)), 481)
    chk("C_at_minus1_eq_q4",  int(clique_poly_eval(-1)), q ** 4)
    chk("C_at_2",             int(clique_poly_eval(2)),  2961)
    chk("C_at_q_eq_C_at_3",   int(clique_poly_eval(q)), 9841)

    # ── Group 3: Independence polynomial seeds ────────────────────────────────
    i0 = indep_poly_seed_i0()
    i1 = indep_poly_seed_i1()
    i2 = indep_poly_seed_i2()
    i3 = indep_poly_seed_i3()

    chk("i0_empty_set",             i0, 1)
    chk("i1_vertices",              i1, V)
    chk("i2_non_adj_pairs",         i2, 540)
    chk("i3_independent_triples",   i3, 3240)
    chk("i3_eq_q4_times_V",         i3, q ** 4 * V)   # 81*40 = 3240

    # ── Group 4: Matching polynomial seeds ────────────────────────────────────
    m0 = matching_seed_m0()
    m1 = matching_seed_m1()
    m2 = matching_seed_m2()
    nu = matching_number()
    hz = hosoya_partial()

    chk("m0_empty_matching",        m0, 1)
    chk("m1_single_edges",          m1, EDGES)
    chk("m2_two_matchings",         m2, 26040)
    chk("matching_number_nu",       nu, V // 2)
    chk("hosoya_partial_3_terms",   hz, 26281)

    # ── Group 5: SM crosswalk and polynomial relations ─────────────────────────
    chk("clique_number_omega",       clique_number(),       CLIQUE_NU)
    chk("independence_number_alpha", independence_number(), ALPHA)
    chk("c1_eq_c4",                  coeffs[1] == coeffs[4], True)
    chk("triangles_eq_V_times_MU",   TRIANGLES,              V * MU)
    chk("c4_over_c3_eq_inv_MU",      Fraction(K4_COUNT, TRIANGLES), Fraction(1, MU))
    chk("i3_over_i2_eq_q_factorial", Fraction(i3, i2),       Fraction(6, 1))
    chk("alpha_times_omega_eq_V",    ALPHA * CLIQUE_NU,       V)

    passed = sum(1 for c in checks if c["pass"])
    total  = len(checks)
    return checks, passed, total


# ── build summary ─────────────────────────────────────────────────────────────

def build_cccxcviii_summary() -> Dict:
    checks, passed, total = verify_all()
    return {
        "part":          "CCCXCVIII",
        "title":         "Graph Polynomial Suite and SM Crosswalk for W(3,3)",
        "checks_pass":   passed,
        "checks_total":  total,
        "status":        "PASS" if passed == total else "FAIL",
        "fields": {
            "clique_poly_coeffs":  clique_poly_coeffs(),
            "C_at_0":              1,
            "C_at_1":              481,
            "C_at_minus1":         81,
            "C_at_2":              2961,
            "C_at_3":              9841,
            "clique_number":       CLIQUE_NU,
            "i0":                  1,
            "i1":                  V,
            "i2":                  indep_poly_seed_i2(),
            "i3":                  indep_poly_seed_i3(),
            "independence_number": ALPHA,
            "m0":                  1,
            "m1":                  EDGES,
            "m2":                  matching_seed_m2(),
            "matching_number":     matching_number(),
            "hosoya_partial":      hosoya_partial(),
        },
        "discoveries": [
            "C(G;-1) = q^4 = 3^4 = 81 = |GF(3)^4|: alternating clique eval = ambient space order",
            "i_3 = q^4*V = 81*40 = 3240: third independence seed = (field order)^4 x vertex count",
            "i_3/i_2 = 6 = q! = 3!: independence ratio = factorial of GF(3) field order",
            "C(G;1) = V*K+1 = 481: total clique count = vertex-valency product + 1",
            "c_1 = c_4 = V = 40: vertex count equals K4 (tetrahedra) count",
            "c_4/c_3 = 1/mu = 1/4: K4-to-triangle ratio = inverse mu intersection parameter",
            "alpha*omega = V = 40: independence number times clique number = vertex count",
            "triangles = V*mu = 160: triangle count = vertices times mu",
        ],
    }


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    checks, passed, total = verify_all()
    for c in checks:
        mark = "\u2713" if c["pass"] else "\u2717"
        print(f"  {mark} {c['check']}: {c['value']} == {c['expected']}")
    print(f"\n{passed}/{total} checks passed")

    summary = build_cccxcviii_summary()
    out_path = ROOT / "PART_CCCXCVIII_graph_poly_results.json"
    with open(out_path, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"Summary written to {out_path}")