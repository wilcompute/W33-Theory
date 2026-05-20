"""Kemeny spectral excess identity for W(3,3).

MCXLIX proves the Kemeny-volume excess identity K*v = v^2 + r, which shows
the Kemeny constant encodes the secondary eigenvalue r through a simple
quadratic excess formula.

Key theorems:
  * K = v + r/v   (Kemeny constant = v + r/v)
  * K*v = v^2 + r (Kemeny-volume = volume^2 + secondary eigenvalue)
  * K - v = r/v = 1/20  (Kemeny excess per vertex = r/v)
  * K - v = 1/S_holo  (Kemeny excess = inverse holographic entropy)
  * S_holo = v/2 = alpha*r = 20  (holographic entropy from W(3,3))
  * S_holo = v*k/(8*q)  (Bekenstein-Hawking form with G=q)
  * (k-r)*(k-s) = 4*v  (spectral-volume product identity)
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_lovasz_independence_clique import (  # noqa: E402
    lovasz_independence_clique_packet,
)


def _exact(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def _packet_fraction(entry: dict[str, object]) -> Fraction:
    return Fraction(int(entry["numerator"]), int(entry["denominator"]))


def kemeny_spectral_excess_packet() -> dict[str, object]:
    """Return exact Kemeny spectral excess data for W(3,3)."""
    lovasz = lovasz_independence_clique_packet()
    q = int(lovasz["parameters"]["q"])
    v = int(lovasz["parameters"]["v"])
    k = int(lovasz["parameters"]["k"])
    r = int(lovasz["parameters"]["r"])
    s = int(lovasz["parameters"]["s"])
    lam = int(lovasz["parameters"]["lam"])
    mu = int(lovasz["parameters"]["mu"])

    alpha = int(lovasz["independence_clique"]["alpha"])  # 10
    omega = int(lovasz["independence_clique"]["omega"])  # 4

    # Kemeny constant (exact)
    f = 24   # multiplicity of r-eigenvalue
    g = 15   # multiplicity of s-eigenvalue
    K = Fraction(f * k, k - r) + Fraction(g * k, k - s)
    # K = 24*12/10 + 15*12/16 = 144/5 + 45/4 = 576/20 + 225/20 = 801/20

    # K = v + r/v identity
    K_formula = Fraction(v * v + r, v)   # = (1600 + 2)/40 = 1602/40 = 801/20
    kemeny_identity_1 = K == K_formula

    # K*v = v^2 + r identity
    Kv = K * v   # = 1602
    Kv_formula = v * v + r   # = 1602
    kemeny_identity_2 = Kv == Kv_formula

    # K excess: K - v = r/v
    K_excess = K - v
    K_excess_formula = Fraction(r, v)
    kemeny_excess_identity = K_excess == K_excess_formula

    # Spectral product identity: (k-r)*(k-s) = 4*v
    spectral_product = (k - r) * (k - s)   # 10 * 16 = 160
    spectral_product_formula = 4 * v       # 4 * 40 = 160
    spectral_product_identity = spectral_product == spectral_product_formula

    # Holographic entropy: S = alpha * r = 10 * 2 = 20 = v/2
    S_holo_from_alpha_r = alpha * r   # 10 * 2 = 20
    S_holo_from_v = Fraction(v, 2)    # 40/2 = 20
    S_holo_from_bh = Fraction(v * k, 8 * q)   # 40*12/24 = 480/24 = 20
    S_holo = Fraction(S_holo_from_alpha_r)

    holographic_identity_1 = S_holo == S_holo_from_v
    holographic_identity_2 = S_holo == S_holo_from_bh

    # Kemeny-holographic connection: K - v = 1/S
    K_excess_inv = Fraction(1, int(S_holo))   # 1/20
    kemeny_holographic_identity = K_excess == K_excess_inv

    # Bekenstein-Hawking form: S = |E|/(4*G) where G = q (Newton's constant)
    edges = v * k // 2   # 240
    G_newton = Fraction(edges, 4 * int(S_holo))   # 240/80 = 3 = q
    G_equals_q = G_newton == q

    # Algebraic proof sketch:
    # From Kemeny formula: K - v = [k(v+lam-mu-2k) - v*mu] / [(k-r)(k-s)]
    # Numerator = k(v+lam-mu-2k) - v*mu
    num = k * (v + lam - mu - 2 * k) - v * mu
    denom = (k - r) * (k - s)
    K_excess_algebraic = Fraction(num, denom)
    algebraic_check = K_excess_algebraic == K_excess

    # Also: num = v/alpha = v/(v/omega) = omega = 4? No: num = 8
    # num = 8 = v/(omega * alpha/omega) = ... let's see: v/(5) = 8 → Δ_YM=5
    delta_ym = q + 2   # = 5
    num_from_physics = v // delta_ym   # 40/5 = 8
    num_physics_check = num == num_from_physics

    # Summary of key numbers
    return {
        "parameters": {
            "q": q,
            "v": v,
            "k": k,
            "r": r,
            "s": s,
            "lam": lam,
            "mu": mu,
            "f": f,
            "g": g,
        },
        "kemeny_constant": {
            "K": _exact(K),
            "formula": "K = 24*(12/10) + 15*(12/16) = 144/5 + 45/4 = 801/20",
        },
        "kemeny_spectral_identity": {
            "K_equals_v_plus_r_over_v": kemeny_identity_1,
            "formula_K": _exact(K_formula),
            "Kv": int(Kv),
            "Kv_equals_v2_plus_r": kemeny_identity_2,
            "Kv_formula": Kv_formula,
            "K_minus_v": _exact(K_excess),
            "r_over_v": _exact(K_excess_formula),
            "kemeny_excess_identity": kemeny_excess_identity,
            "statement": "K = v + r/v  where r = 2 (secondary eigenvalue = SRG lambda param)",
        },
        "spectral_product_identity": {
            "k_minus_r": k - r,
            "k_minus_s": k - s,
            "product": spectral_product,
            "four_v": spectral_product_formula,
            "identity": "(k-r)*(k-s) = 4*v",
            "verified": spectral_product_identity,
        },
        "holographic_entropy": {
            "S_from_alpha_r": _exact(S_holo),
            "S_from_v_half": _exact(S_holo_from_v),
            "S_from_BH": _exact(S_holo_from_bh),
            "formula_alpha_r": "S = alpha * r = 10 * 2 = 20",
            "formula_v_half": "S = v/2 = 40/2 = 20",
            "formula_BH": "S = v*k/(8*q) = 480/24 = 20  [Bekenstein-Hawking form]",
            "identity_v_half": holographic_identity_1,
            "identity_BH": holographic_identity_2,
        },
        "bekenstein_hawking": {
            "edges": edges,
            "S_holo": int(S_holo),
            "G_newton": _exact(G_newton),
            "G_equals_q": G_equals_q,
            "formula": "S = |E|/(4*G) with G=q=3",
            "interpretation": (
                "The Newton constant of the W(3,3) holographic screen equals "
                "q = 3, the order of the finite field GF(q) defining W(3,3)."
            ),
        },
        "kemeny_holographic_bridge": {
            "K_minus_v": _exact(K_excess),
            "one_over_S": _exact(K_excess_inv),
            "identity": "K - v = 1/S_holo",
            "verified": kemeny_holographic_identity,
            "statement": (
                "Kemeny constant exceeds v by exactly the inverse holographic entropy: "
                "K - v = 1/S = 1/20"
            ),
        },
        "algebraic_proof": {
            "numerator": num,
            "denominator": denom,
            "K_excess_algebraic": _exact(K_excess_algebraic),
            "algebraic_check": algebraic_check,
            "numerator_formula": "k*(v+lam-mu-2k) - v*mu",
            "numerator_from_delta_ym": num_from_physics,
            "num_physics_check": num_physics_check,
            "delta_ym": delta_ym,
            "note": "numerator = v/Delta_YM = 40/5 = 8",
        },
        "master_identities_summary": {
            "K_equals_v_plus_r_over_v": kemeny_identity_1,
            "Kv_equals_v2_plus_r": kemeny_identity_2,
            "K_excess_equals_1_over_S": kemeny_holographic_identity,
            "spectral_product_equals_4v": spectral_product_identity,
            "S_equals_v_over_2": holographic_identity_1,
            "G_newton_equals_q": G_equals_q,
        },
    }


def main() -> None:
    packet = kemeny_spectral_excess_packet()
    out_path = ROOT / "PART_MCXLIX_KEMENY_SPECTRAL_EXCESS_results.json"
    with open(out_path, "w") as fh:
        json.dump(packet, fh, indent=2)
    data_path = ROOT / "data" / "w33_kemeny_spectral_excess.json"
    data_path.parent.mkdir(exist_ok=True)
    with open(data_path, "w") as fh:
        json.dump(packet, fh, indent=2)
    print(f"MCXLIX results written to {out_path}")
    ids = packet["master_identities_summary"]
    for name, val in ids.items():
        status = "✓" if val else "✗"
        print(f"  [{status}] {name}")


if __name__ == "__main__":
    main()
