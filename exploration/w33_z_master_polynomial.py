"""The Z(x) master polynomial of Part XXII and the q-cyclotomic master lock.

From part22_fano_synthesis.tex (and the W36 paper / main.tex):

    Z(x) = (1 - 5x)^{10} . (1 + x)^{16} . (1 + 7x)^6.

This is the Dirac spectral determinant on the generalised quadrangle
GQ(3,3). The exponents are the W(3,3) spectral multiplicities
{Phi_4, 2^{q+1}, 2q} = {10, 16, 6}, summing to deg Z = 32 = 2^{q+lambda}
= dim Spin(10) Weyl spinor. The bases (-5, -1, +7) are the spectral
centres: 5 = q + lambda, 1, and 7 = Phi_6(q).

Part XXII's master theorem states:

    (i)   Z(0)  = 1,
    (ii)  Z(-1) = 0                 (anomaly cancellation),
    (iii) Z(1)  = 2^{54} = 2^{2q^3} (spinor degeneracy),
    (iv)  Z'(0) = 8 = dim O         (octonion dim),
    (v)   Z''(0)/2 = -248 = -dim E_8,
    (vi) -Z''(0) = 496 = 2^{q+1} (2^{q+lambda} - 1) = third perfect number,
    (vii) |Z(i)|^2 = 2^{32} . 13^{10} . 5^{12}
                   = 2^{2^{q+lambda}} . Phi_3^{Phi_4} . (q+lambda)^k,
    (viii) Trace tower: Tr(D^n) = 10.5^n + 16.(-1)^n + 6.(-7)^n,
           with -x d/dx log Z(x) = sum_{n>=1} Tr(D^n) x^n.

Independently, the q-cyclotomic curved master lock (see current-synthesis):

    c_EH(q) = v(q) . (q^2 - 1)                 with v(q) = (q+1)(q^2+1),
    a_2(q)  = Phi_6(q) . c_EH(q),
    c_6(q)  = q . Phi_3(q) . c_EH(q),

and the Weinberg lock as a polynomial identity in q:

    9 . c_EH(q) / c_6(q) = q / Phi_3(q),         free of 9 at q=3 giving 3/13.

The atmospheric sum rule sin^2 theta_23 = sin^2 theta_W + sin^2 theta_12 is
equivalent to q + mu = Phi_6, i.e. q(q-3) = 0, so q=3 is forced uniquely.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from sympy import Poly, Rational, binomial, expand, symbols


# ----------------------------------------------------------------------
# Symbolic Z(x) and its derivatives.
# ----------------------------------------------------------------------
x, q = symbols("x q", real=True)


def Z_poly_sym():
    """Return Z(x) = (1-5x)^{10} (1+x)^{16} (1+7x)^6 as sympy Poly."""
    return Poly((1 - 5 * x) ** 10 * (1 + x) ** 16 * (1 + 7 * x) ** 6, x)


def Z_at(value) -> int:
    """Integer value of Z at a rational/integer point."""
    return int(Z_poly_sym().eval(value))


def Z_taylor_coefficients(n_terms: int = 5) -> list[int]:
    """First n_terms Taylor coefficients of Z(x) at x=0 as integers.

    Z(x) = sum_{k>=0} c_k x^k.  We return [c_0, c_1, ..., c_{n_terms-1}].
    """
    p = Z_poly_sym()
    all_coeffs = p.all_coeffs()  # highest degree first
    # Pad / convert to ascending order, trim to n_terms.
    deg = p.degree()
    ascending = [0] * (deg + 1)
    for i, c in enumerate(all_coeffs):
        ascending[deg - i] = int(c)
    return ascending[:n_terms]


def Z_prime_at_zero() -> int:
    """Z'(0) = coefficient of x^1."""
    return Z_taylor_coefficients(2)[1]


def Z_double_prime_at_zero() -> int:
    """Z''(0) = 2 * (coefficient of x^2)."""
    return 2 * Z_taylor_coefficients(3)[2]


# ----------------------------------------------------------------------
# Modulus |Z(i)|^2 as an exact integer.
# ----------------------------------------------------------------------
def abs_Z_of_i_squared() -> int:
    """|Z(i)|^2 = |1 - 5i|^{20} . |1 + i|^{32} . |1 + 7i|^{12}
              = 26^{10} . 2^{16} . 50^6
              = 2^{32} . 13^{10} . 5^{12}."""
    return 26**10 * 2**16 * 50**6


# ----------------------------------------------------------------------
# Trace tower.
# ----------------------------------------------------------------------
DIRAC_EIGS: list[tuple[int, int]] = [(5, 10), (-1, 16), (-7, 6)]


def trace_D_power(n: int) -> int:
    """Tr(D^n) = sum multiplicity_j * eig_j^n over spectral sectors."""
    return sum(mult * (eig**n) for (eig, mult) in DIRAC_EIGS)


def trace_tower_row(n_max: int = 5) -> list[dict[str, Any]]:
    return [
        {
            "n": n,
            "trace": trace_D_power(n),
            "formula": "10*5^n + 16*(-1)^n + 6*(-7)^n",
        }
        for n in range(1, n_max + 1)
    ]


# ----------------------------------------------------------------------
# q-cyclotomic master lock.
# ----------------------------------------------------------------------
def v_of_q(qv: int) -> int:
    """v(q) = (q+1)(q^2+1).  At q=3: v=4.10=40 (vertices of W(3,q)/side)."""
    return (qv + 1) * (qv**2 + 1)


def Phi_3(qv: int) -> int:
    return qv**2 + qv + 1


def Phi_6(qv: int) -> int:
    return qv**2 - qv + 1


def c_EH(qv: int) -> int:
    return v_of_q(qv) * (qv**2 - 1)


def a_2_curved(qv: int) -> int:
    return Phi_6(qv) * c_EH(qv)


def c_6_curved(qv: int) -> int:
    return qv * Phi_3(qv) * c_EH(qv)


def weinberg_polynomial_identity(qv: int) -> Fraction:
    """9 c_EH(q) / c_6(q). By construction this equals 1 / (q . Phi_3(q) / (9 (q^2-1) v(q))) ...
    Actually: 9 c_EH / c_6 = 9 / (q Phi_3).  So at q=3: 9 / (3 . 13) = 9/39 = 3/13 [= q/Phi_3].
    """
    return Fraction(9 * c_EH(qv), c_6_curved(qv))


def weinberg_raw(qv: int) -> Fraction:
    """q / Phi_3(q), the promoted Weinberg lock value."""
    return Fraction(qv, Phi_3(qv))


# ----------------------------------------------------------------------
# Atmospheric sum rule.
# ----------------------------------------------------------------------
def atmospheric_sum_rule_gap(qv: int) -> Fraction:
    """sin^2 theta_23 - (sin^2 theta_W + sin^2 theta_12)
    = Phi_6(q)/Phi_3(q) - (q/Phi_3(q) + mu/Phi_3(q))
    where mu = q + 1.  Equals (Phi_6 - q - (q+1)) / Phi_3 = (q^2 - 3q) / Phi_3."""
    mu = qv + 1
    lhs = Fraction(Phi_6(qv), Phi_3(qv))
    rhs = Fraction(qv, Phi_3(qv)) + Fraction(mu, Phi_3(qv))
    return lhs - rhs


# ----------------------------------------------------------------------
# Pinning drivers.
# ----------------------------------------------------------------------
def verify_special_values() -> dict[str, Any]:
    """(i)-(iii) and leading Taylor coefficients."""
    z0 = Z_at(0)
    zm1 = Z_at(-1)
    z1 = Z_at(1)
    zp0 = Z_prime_at_zero()
    zpp0 = Z_double_prime_at_zero()
    return {
        "Z(0)": z0,
        "Z(-1)": zm1,
        "Z(1)": z1,
        "Z(1) == 2^54": z1 == 2**54,
        "Z'(0)": zp0,
        "Z'(0) == 8 (dim O)": zp0 == 8,
        "Z''(0)": zpp0,
        "Z''(0)/2 == -248 (-dim E_8)": zpp0 // 2 == -248,
        "-Z''(0) == 496 (third perfect number)": -zpp0 == 496,
        "496 == 16 * 31": 16 * 31 == 496,
        "degree": Z_poly_sym().degree(),
        "degree == 32": Z_poly_sym().degree() == 32,
    }


def verify_modulus_of_Z_of_i() -> dict[str, Any]:
    got = abs_Z_of_i_squared()
    expected = 2**32 * 13**10 * 5**12
    return {
        "|Z(i)|^2": got,
        "expected": expected,
        "match": got == expected,
    }


def verify_trace_tower() -> dict[str, Any]:
    rows = trace_tower_row(n_max=5)
    # Pins from part22:  Tr(D^1) = -8,  Tr(D^2) = 560,  Tr(D^3) = -824.
    expected = {1: -8, 2: 560, 3: -824}
    for row in rows:
        n = row["n"]
        if n in expected:
            row["expected"] = expected[n]
            row["match"] = row["trace"] == expected[n]
    return {"rows": rows, "all_pins_hold": all(
        row.get("match", True) for row in rows
    )}


def verify_q_cyclotomic_master_lock(qv: int = 3) -> dict[str, Any]:
    cEH = c_EH(qv)
    a2 = a_2_curved(qv)
    c6 = c_6_curved(qv)
    weinberg_ratio = weinberg_polynomial_identity(qv)
    weinberg_target = weinberg_raw(qv)
    return {
        "q": qv,
        "v(q)": v_of_q(qv),
        "c_EH(q)": cEH,
        "a_2(q) = Phi_6(q) c_EH": a2,
        "c_6(q) = q Phi_3(q) c_EH": c6,
        "c_EH(3) == 320": cEH == 320,
        "a_2(3) == 2240": a2 == 2240,
        "c_6(3) == 12480": c6 == 12480,
        "9 c_EH / c_6": (weinberg_ratio.numerator, weinberg_ratio.denominator),
        "q / Phi_3": (weinberg_target.numerator, weinberg_target.denominator),
        "weinberg_lock_holds": weinberg_ratio == weinberg_target,
        "sin2_theta_W_at_q3": (Fraction(qv, Phi_3(qv)).numerator,
                                Fraction(qv, Phi_3(qv)).denominator),
    }


def verify_atmospheric_sum_rule(qs: list[int] | None = None) -> dict[str, Any]:
    """Sum rule holds iff q(q-3) = 0.  We test q in {1,2,3,4,5,6,7}."""
    if qs is None:
        qs = [1, 2, 3, 4, 5, 6, 7]
    rows: list[dict[str, Any]] = []
    for qv in qs:
        gap = atmospheric_sum_rule_gap(qv)
        rows.append({
            "q": qv,
            "gap_num": gap.numerator,
            "gap_den": gap.denominator,
            "holds": gap == 0,
        })
    holds_set = {row["q"] for row in rows if row["holds"]}
    return {
        "rows": rows,
        "q_for_which_it_holds": sorted(holds_set),
        "selects_q_3_uniquely_positive": holds_set == {3}
        or holds_set == {0, 3},
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    spec = verify_special_values()
    mod = verify_modulus_of_Z_of_i()
    trace = verify_trace_tower()
    lock = verify_q_cyclotomic_master_lock(qv=3)
    atm = verify_atmospheric_sum_rule()
    chain = {
        "Z_master_identity_all_eight_pins": all([
            spec["Z(0)"] == 1,
            spec["Z(-1)"] == 0,
            spec["Z(1) == 2^54"],
            spec["Z'(0) == 8 (dim O)"],
            spec["Z''(0)/2 == -248 (-dim E_8)"],
            spec["-Z''(0) == 496 (third perfect number)"],
            spec["496 == 16 * 31"],
            spec["degree == 32"],
        ]),
        "modulus_of_Z_at_i_matches_cyclotomic_lock": mod["match"],
        "trace_tower_matches_part22_values": trace["all_pins_hold"],
        "q_cyclotomic_master_lock_at_q3_holds": (
            lock["c_EH(3) == 320"]
            and lock["a_2(3) == 2240"]
            and lock["c_6(3) == 12480"]
            and lock["weinberg_lock_holds"]
        ),
        "atmospheric_sum_rule_selects_q3_uniquely": atm[
            "selects_q_3_uniquely_positive"
        ],
    }
    return {
        "Z_special_values": spec,
        "Z_modulus_at_i": mod,
        "trace_tower": trace,
        "q_cyclotomic_master_lock": lock,
        "atmospheric_sum_rule": atm,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nspecial values:")
    for k, v in s["Z_special_values"].items():
        print(f"  {k}: {v}")
    print("\ntrace tower:")
    for row in s["trace_tower"]["rows"]:
        print(f"  n={row['n']}: Tr(D^n) = {row['trace']}", end="")
        if "expected" in row:
            print(f"  (expected {row['expected']}, match={row['match']})")
        else:
            print()
    print("\nq-cyclotomic master lock at q=3:")
    for k, v in s["q_cyclotomic_master_lock"].items():
        print(f"  {k}: {v}")
    print("\natmospheric sum rule q for which it holds:",
          s["atmospheric_sum_rule"]["q_for_which_it_holds"])
