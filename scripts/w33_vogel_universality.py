#!/usr/bin/env python3
"""
Vogel universality (universal Lie algebra) checks and W(3,3) numerology.

This script is *not* part of the canonical pillar test suite; it is a compact,
computational companion to the recent literature on Vogel's universal Lie
algebra formalism and the classification of Jacobi identities.

Key references (open access / arXiv):
  - A. Morozov, A. Sleptsov, "Vogel’s universality and the classification
    problem for Jacobi identities", Eur. Phys. J. C 85, 1233 (2025).
    DOI: 10.1140/epjc/s10052-025-14943-y
    See eqs. (27)–(29) for χ(x1), χ(x3), χ(x5) and the (α,β,γ)↔(t,σ,ω) map.
  - A. Isaev et al., "Vogel universality and beyond", arXiv:2601.01612 (2026).
  - L. Bishler, A. Mironov, "Refined Vogel universality and Macdonald
    dimensions", arXiv:2504.13831 (2025).
  - L. Bishler, "Vogel universality and Macdonald dimensions",
    arXiv:2507.11414 (2025).
  - L. Bishler, A. Mironov, A. Morozov, "Macdonald deformation of the Vogel
    universality and hyperpolynomials", arXiv:2505.16569 (2025).

Run:
  python scripts/w33_vogel_universality.py
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

# Ensure we can import sibling modules from scripts/ when executed as a file.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from w33_homology import build_clique_complex, build_w33, compute_homology


def class_order_from_label(name: str) -> int:
    digits = ""
    for ch in name.strip():
        if ch.isdigit():
            digits += ch
        else:
            break
    return int(digits) if digits else 0


# ---------------------------------------------------------------------------
# Vogel / Dynkin locus polynomials (Morozov–Sleptsov 2025, eqs. (11)–(16))
# ---------------------------------------------------------------------------


def P_sl(alpha, beta, gamma):
    return (alpha + beta) * (beta + gamma) * (alpha + gamma)


def P_osp(alpha, beta, gamma):
    return (
        (alpha + 2 * beta)
        * (2 * alpha + beta)
        * (beta + 2 * gamma)
        * (2 * beta + gamma)
        * (alpha + 2 * gamma)
        * (2 * alpha + gamma)
    )


def P_exc(alpha, beta, gamma):
    return (
        (alpha - 2 * beta - 2 * gamma)
        * (beta - 2 * alpha - 2 * gamma)
        * (gamma - 2 * alpha - 2 * beta)
    )


def omega_factor(alpha, beta, gamma):
    # extra factor raising degrees to P_15 / P_22 (eq. (15))
    return (
        (alpha + beta + 2 * gamma)
        * (beta + gamma + 2 * alpha)
        * (gamma + alpha + 2 * beta)
    )


def P_Lie(alpha, beta, gamma):
    return (
        P_sl(alpha, beta, gamma) * P_osp(alpha, beta, gamma) * P_exc(alpha, beta, gamma)
    )


def P_G2(alpha, beta, gamma):
    t = alpha + beta + gamma
    return 18 * (alpha * alpha + beta * beta + gamma * gamma) - 25 * (t * t)


def P_F4(alpha, beta, gamma):
    t = alpha + beta + gamma
    return 81 * (alpha * alpha + beta * beta + gamma * gamma) - 65 * (t * t)


def P_E6(alpha, beta, gamma):
    t = alpha + beta + gamma
    return 18 * (alpha * alpha + beta * beta + gamma * gamma) - 13 * (t * t)


def P_E7(alpha, beta, gamma):
    t = alpha + beta + gamma
    return 81 * (alpha * alpha + beta * beta + gamma * gamma) - 53 * (t * t)


def P_E8(alpha, beta, gamma):
    t = alpha + beta + gamma
    return 225 * (alpha * alpha + beta * beta + gamma * gamma) - 137 * (t * t)


def P_Lie_refined(alpha, beta, gamma):
    # \mathcal{P}_{Lie} from eq. (14): replaces P_exc with algebra-specific loci.
    return (
        P_sl(alpha, beta, gamma)
        * P_osp(alpha, beta, gamma)
        * P_G2(alpha, beta, gamma)
        * P_F4(alpha, beta, gamma)
        * P_E6(alpha, beta, gamma)
        * P_E7(alpha, beta, gamma)
        * P_E8(alpha, beta, gamma)
    )


def dim_adj(alpha, beta, gamma):
    """Universal adjoint dimension formula (standard Vogel normalization)."""
    t = alpha + beta + gamma
    return (alpha - 2 * t) * (beta - 2 * t) * (gamma - 2 * t) / (alpha * beta * gamma)


def vogel_t_sigma_omega(alpha, beta, gamma):
    """Compute (t, σ, ω) in Isaev/Morozov notation from (α,β,γ).

    Using the relations (Morozov–Sleptsov 2025, EPJC, eq. (29)):
      t = α + β + γ
      αβ + βγ + γα = σ - 2 t^2
      αβγ = ω - t σ
    """
    a = Fraction(alpha)
    b = Fraction(beta)
    c = Fraction(gamma)
    t = a + b + c
    s2 = a * b + b * c + c * a
    s3 = a * b * c
    sigma = s2 + 2 * t * t
    omega = s3 + t * sigma
    return t, sigma, omega


def vogel_chi_x1(t):
    """Universal character χ(x1) for the split Casimir operator (Morozov–Sleptsov 2025, eq. (27))."""
    tt = Fraction(t)
    return 2 * tt


def vogel_chi_x3(t, omega):
    """Universal character χ(x3) for the split Casimir operator (Morozov–Sleptsov 2025, eq. (28))."""
    tt = Fraction(t)
    ww = Fraction(omega)
    return 4 * tt**3 - Fraction(3, 2) * ww


def vogel_chi_x5(t, sigma, omega):
    """Universal character χ(x5) for the split Casimir operator (Morozov–Sleptsov 2025, eq. (28))."""
    tt = Fraction(t)
    ss = Fraction(sigma)
    ww = Fraction(omega)
    return 12 * tt**5 - Fraction(17, 2) * tt**2 * ww + Fraction(3, 2) * ss * ww


def vogel_parameters() -> dict[str, tuple[object, object, object]]:
    """Minimal Vogel parameter table (common normalization)."""
    return {
        # exceptional (ordered as in many Vogel tables)
        "G2": (Fraction(-2), Fraction(10, 3), Fraction(8, 3)),
        "F4": (-2, 5, 6),
        "E6": (-2, 6, 8),
        "E7": (-2, 8, 12),
        "E8": (-2, 12, 20),
    }


def analyze_vogel_universality() -> dict[str, object]:
    params = vogel_parameters()

    dims_expected = {"G2": 14, "F4": 52, "E6": 78, "E7": 133, "E8": 248}
    dims = {}
    loci = {}
    refined = {}
    invariants = {}

    for name, (a, b, c) in params.items():
        dims[name] = float(dim_adj(a, b, c)) if name != "G2" else int(dim_adj(a, b, c))
        loci[name] = {
            "P_sl": P_sl(a, b, c),
            "P_osp": P_osp(a, b, c),
            "P_exc": P_exc(a, b, c),
            "P_Lie": P_Lie(a, b, c),
            "omega": omega_factor(a, b, c),
        }
        refined[name] = {
            "P_G2": P_G2(a, b, c),
            "P_F4": P_F4(a, b, c),
            "P_E6": P_E6(a, b, c),
            "P_E7": P_E7(a, b, c),
            "P_E8": P_E8(a, b, c),
            "P_Lie_refined": P_Lie_refined(a, b, c),
        }
        t, sigma, omega = vogel_t_sigma_omega(a, b, c)
        invariants[name] = {
            "t": t,
            "sigma": sigma,
            "omega": omega,
            "chi_x1": vogel_chi_x1(t),
            "chi_x3": vogel_chi_x3(t, omega),
            "chi_x5": vogel_chi_x5(t, sigma, omega),
        }

        # sanity: adjoint dims
        exp = dims_expected[name]
        got = dims[name]
        if isinstance(got, float):
            assert abs(got - exp) < 1e-9
        else:
            assert int(got) == exp

        # Dynkin locus should vanish
        assert loci[name]["P_Lie"] == 0
        # The algebra-specific polynomial should vanish at that algebra
        assert refined[name][f"P_{name}"] == 0

    # W33 invariants
    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    hom = compute_homology(simplices)
    b1 = int(hom["betti_numbers"][1])
    edge_count = int(len(edges))
    w33_gap = 4  # proven earlier: spectral gap Δ(L1)=4

    # "81" is a key coefficient in (13) for F4 and E7.
    vogel_coeff_81 = {"F4": 81, "E7": 81}

    # E8 dual Coxeter h^∨=t=30 ⇒ χ(x1)=2t=60 matches |E(W33)|/Δ = 240/4.
    e8_chi_x1 = int(invariants["E8"]["chi_x1"])
    assert edge_count == 240
    assert e8_chi_x1 == edge_count // w33_gap

    return {
        "vogel": {
            "params": {k: [str(x) for x in v] for k, v in params.items()},
            "dims": dims,
            "expected_dims": dims_expected,
            "loci": loci,
            "refined": refined,
            "invariants": {
                k: {kk: str(vv) for kk, vv in inv.items()}
                for k, inv in invariants.items()
            },
            "coeff_81_algebras": sorted(vogel_coeff_81.keys()),
        },
        "w33": {
            "n_vertices": n,
            "n_edges": edge_count,
            "b1": b1,
            "b1_equals_81": b1 == 81,
            "spectral_gap_L1": w33_gap,
            "bh_entropy_edges_over_gap": edge_count // w33_gap,
        },
    }


def main() -> dict[str, object]:
    out = analyze_vogel_universality()

    print("=" * 78)
    print("VOGEL UNIVERSALITY (2025+) — COMPUTATIONAL CHECKS")
    print("=" * 78)

    v = out["vogel"]
    w = out["w33"]

    print("\n§1. Universal adjoint dimensions")
    for name in ["G2", "F4", "E6", "E7", "E8"]:
        got = v["dims"][name]
        exp = v["expected_dims"][name]
        print(f"  {name:>2}: dim_adj = {got} (expected {exp})")

    print("\n§2. Dynkin locus polynomials (vanish on simple Lie algebras)")
    for name in ["G2", "F4", "E6", "E7", "E8"]:
        p = v["loci"][name]["P_Lie"]
        print(f"  {name:>2}: P_Lie = {p}")

    print("\n§3. Algebra-specific refined loci (eq. (13))")
    for name in ["G2", "F4", "E6", "E7", "E8"]:
        p = v["refined"][name][f"P_{name}"]
        print(f"  {name:>2}: P_{name} = {p}")

    print("\n§4. W(3,3) invariant touching Vogel coefficient 81")
    print(f"  b1(W33) = {w['b1']}  (expected 81)")
    print(f"  81 appears as coefficient in (13) for: {v['coeff_81_algebras']}")
    assert w["b1_equals_81"] is True

    inv = v.get("invariants", {})
    if isinstance(inv, dict) and "E8" in inv:
        e8 = inv["E8"]
        print("\n§5. Universal t,σ,ω invariants (split-Casimir characters)")
        print(
            "  E8: t=%s, σ=%s, ω=%s" % (e8.get("t"), e8.get("sigma"), e8.get("omega"))
        )
        print(
            "  χ(x1)=2t=%s  (matches |E(W33)|/Δ = %d/%d = %d)"
            % (
                e8.get("chi_x1"),
                w["n_edges"],
                w["spectral_gap_L1"],
                w["bh_entropy_edges_over_gap"],
            )
        )

    print("\nALL CHECKS PASSED ✓")
    return out


if __name__ == "__main__":
    main()
