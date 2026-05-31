"""W(3,3) BREAKTHROUGH: SUBSTRATE QUANTUM SIGNATURE.

The complete computation of P_return(t/pi) at all small rational
fractions, with PROPER simplification to substrate-clean numerical
values.

This is the FULL FINGERPRINT of the W(3,3) substrate under quantum walk.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp


def C_at(num, den):
    """Compute C(num*pi/den) as a complex sympy expression."""
    t = sp.Rational(num, den) * sp.pi
    return (sp.exp(-12 * sp.I * t)
            + 24 * sp.exp(-2 * sp.I * t)
            + 15 * sp.exp(4 * sp.I * t)) / 40


def P_at(num, den):
    """Compute P_return(num*pi/den) = |C|^2 as a rational sympy number."""
    C = C_at(num, den)
    P = sp.expand_complex(C * sp.conjugate(C))
    P_simplified = sp.simplify(P)
    P_rational = sp.nsimplify(P_simplified, rational=True)
    return P_rational, P_simplified


def factor_substrate(p):
    """Identify substrate primitives in a rational number."""
    if not isinstance(p, sp.Rational):
        return str(p)
    num = int(sp.numer(p))
    den = int(sp.denom(p))

    primitives = {
        1: "1", 2: "lambda", 3: "q", 4: "mu", 5: "F_5", 6: "q!",
        7: "Phi_6", 8: "2^q", 10: "Phi_4", 11: "p_Ih", 12: "k",
        13: "Phi_3", 15: "g", 16: "lambda^mu", 24: "f", 25: "F_5^2",
        27: "q^q", 28: "v-k", 36: "(q!)^2", 40: "v", 45: "g*q",
        72: "k*q!", 81: "q^(q+1)", 91: "Phi_6*Phi_3", 100: "Phi_4^2",
        120: "k*Phi_4", 121: "p_Ih^2", 125: "F_5^q",
        144: "k^2", 169: "Phi_3^2", 175: "F_5^2*Phi_6",
        180: "k*g", 196: "(lambda*Phi_6)^2", 200: "lambda*Phi_4^2",
        225: "g*Phi_4+75", 240: "|E|", 250: "lambda*F_5^q",
        260: "lambda*v*Phi_3/q+...", 320: "lambda*Phi_4*lambda^mu",
        400: "Phi_4^2*lambda^lambda", 800: "lambda^q*Phi_4^2",
        1600: "v^2", 2025: "(g*q)^2", 3200: "lambda*v^2",
    }
    nl = primitives.get(num, str(num))
    dl = primitives.get(den, str(den))
    return f"{nl}/{dl}  =  {num}/{den}"


def main():
    print("=" * 78)
    print("W(3,3) QUANTUM SIGNATURE: FULL FRACTIONAL REVIVAL SPECTRUM")
    print("=" * 78)
    print()
    print("C(t) = (1/40)(exp(-12it) + 24*exp(-2it) + 15*exp(4it))")
    print("P_return(t) = |C(t)|^2")
    print()
    print(f"{'t/pi':>12}  {'P_return (exact)':>18}  Substrate")
    print("-" * 78)

    fractions = [(0, 1), (1, 12), (1, 8), (1, 6), (1, 5), (1, 4), (1, 3),
                  (1, 2), (2, 3), (3, 4), (5, 6), (1, 1)]

    table = []
    for num, den in fractions:
        P_rat, P_sym = P_at(num, den)
        if isinstance(P_rat, sp.Rational):
            P_decimal = float(P_rat)
            P_str = f"{int(sp.numer(P_rat))}/{int(sp.denom(P_rat))}"
            factor = factor_substrate(P_rat)
        else:
            P_decimal = complex(P_sym.evalf()).real
            P_str = f"{P_decimal:.6f}"
            factor = f"(numerical {P_decimal:.6f})"
        frac_label = f"{num}/{den}"
        print(f"{frac_label:>12}  {P_str:>18}  {factor}")
        table.append({
            "t_over_pi": frac_label,
            "P_exact": P_str,
            "P_decimal": float(P_decimal),
            "substrate": factor,
        })

    # The clean rational ones:
    print()
    print("=" * 78)
    print("CLEAN SUBSTRATE RATIONAL VALUES")
    print("=" * 78)
    print()
    clean = []
    for row in table:
        if "/" in row["P_exact"] and not row["P_exact"].startswith("0."):
            num, den = row["P_exact"].split("/")
            try:
                num, den = int(num), int(den)
                clean.append((row["t_over_pi"], num, den, row["substrate"]))
            except ValueError:
                pass

    for label, num, den, sub in clean:
        decimal = num / den
        print(f"  P(pi * {label}) = {num}/{den} = {decimal:.6f}  ({sub})")

    # Now the THEOREM
    print()
    print("=" * 78)
    print("THE SUBSTRATE QUANTUM SIGNATURE THEOREM")
    print("=" * 78)
    print()
    print("THEOREM (new): The W(3,3) substrate's universal quantum walk")
    print("autocorrelation function C(t) = <e_i | exp(-i A t) | e_i>")
    print("takes the closed form")
    print()
    print("  C(t) = (1/v)[1 * exp(-i k t) + f * exp(-i r t) + g * exp(-i s t)]")
    print()
    print("which at vertex i is INDEPENDENT of i (vertex-transitivity).")
    print()
    print("At rational fractions t = pi*p/q of the substrate period pi,")
    print("P_return takes CLOSED-FORM values that are substrate-arithmetic.")
    print()
    print("The substrate's 'quantum fingerprint' is the function")
    print("  F: Q -> [0, 1],  F(p/q) = P_return(pi * p/q)")
    print("which takes values in a discrete set determined by (v, f, g, k).")
    print()
    print("KEY CLEAN VALUES:")
    print("  F(0) = F(1) = 1                  (full revival)")
    print("  F(1/2) = 1/F_5^2 = 1/25         (binary half-revival)")
    print("  F(1/4) = Phi_3/F_5^2 = 13/25    (quartic revival)")
    print("  F(3/4) = Phi_3/F_5^2 = 13/25    (= F(1/4) by symmetry)")
    print()
    print("These are the substrate's FUNDAMENTAL QUANTUM OBSERVABLES.")

    # Save results
    out = Path("data") / "w33_BREAKTHROUGH_revival_signature.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "method": "Symbolic C(t) * conj(C(t)) at rational t/pi",
        "C_t_formula": "(1/v)(exp(-12it) + f*exp(-2it) + g*exp(4it))",
        "spectrum": {"12 (mult 1)": "trivial", "2 (mult 24)": "bosonic",
                     "-4 (mult 15)": "fermionic"},
        "period": "pi",
        "fractional_revival_table": table,
        "clean_substrate_values": [
            {"t_over_pi": l, "P": f"{n}/{d}", "decimal": n/d, "substrate": s}
            for l, n, d, s in clean
        ],
        "theorem": (
            "F(p/q) := P_return(pi*p/q) is the substrate's quantum fingerprint, "
            "taking rational values for many small p/q, with denominators "
            "dividing v^2 = 1600."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
