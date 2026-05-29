"""Compute and return the canonical substrate primitives and a small set
of closed-form predictions used across the W33 project.

This module exposes compute_substrate_predictions() so tests can import
and assert exact rational identities.
"""
from fractions import Fraction


def compute_substrate_predictions():
    q = 3
    mu = q + 1
    q_fact = 6  # 3!
    k = mu * q
    Phi_3 = q * q + q + 1
    Phi_4 = q * q + 1
    Phi_6 = q * q - q + 1
    v = (q ** 4 - 1) // (q - 1)
    E_edges = v * k // 2

    # Exact rational formulas
    alpha_inv = Fraction(2 ** Phi_6 + q * q) + Fraction(1, mu * Phi_6)
    sin2_theta_w = Fraction(q, Phi_3)
    neutrino_wimp_exponent = v - q_fact

    denom_511 = 2 ** 9 - 1
    Omega_b = Fraction((mu + 1) ** 2, denom_511)
    Omega_DM = Fraction(q ** q * (mu + 1), denom_511)
    Omega_L = Fraction(Phi_3 * q ** q, denom_511)

    key_rate = Fraction(Phi_3, v)
    F3_visibility = Fraction(1, q)

    return {
        "q": q,
        "mu": mu,
        "q_fact": q_fact,
        "k": k,
        "Phi_3": Phi_3,
        "Phi_4": Phi_4,
        "Phi_6": Phi_6,
        "v": v,
        "E_edges": E_edges,
        "alpha_inv": alpha_inv,
        "sin2_theta_w": sin2_theta_w,
        "neutrino_wimp_exponent": neutrino_wimp_exponent,
        "Omega_b": Omega_b,
        "Omega_DM": Omega_DM,
        "Omega_L": Omega_L,
        "key_rate": key_rate,
        "F3_visibility": F3_visibility,
    }


def _format_fraction(frac: Fraction) -> str:
    return f"{frac} = {float(frac):.12f}"


def main():
    vals = compute_substrate_predictions()
    lines = [
        f"q = {vals['q']}",
        f"mu = {vals['mu']}",
        f"q! = {vals['q_fact']}",
        f"k = {vals['k']}",
        f"Phi_3 = {vals['Phi_3']}",
        f"Phi_4 = {vals['Phi_4']}",
        f"Phi_6 = {vals['Phi_6']}",
        f"v = {vals['v']}",
        f"|E| = {vals['E_edges']}",
        "",
        "Computed closed-form predictions:",
        f"alpha^{-1} = {_format_fraction(vals['alpha_inv'])}",
        f"sin^2(theta_W) = {vals['sin2_theta_w']} = {float(vals['sin2_theta_w']):.12f}",
        f"neutrino/WIMP exponent (v - q!) = {vals['neutrino_wimp_exponent']}",
        f"Omega_b = {_format_fraction(vals['Omega_b'])}",
        f"Omega_DM = {_format_fraction(vals['Omega_DM'])}",
        f"Omega_L = {_format_fraction(vals['Omega_L'])}",
        f"Key rate (Phi_3 / v) = {vals['key_rate']} = {float(vals['key_rate']):.6f}",
        f"F3 visibility = {vals['F3_visibility']} = {float(vals['F3_visibility']):.6f}",
    ]
    print("\n".join(lines))


if __name__ == "__main__":
    main()
