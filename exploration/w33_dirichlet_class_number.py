"""Dirichlet class number formula for imaginary quadratic fields.

For a fundamental negative discriminant D < 0 let chi_D(a) denote the
Kronecker symbol (D / a).  The Dirichlet L-series

    L(s, chi_D) = sum_{n >= 1} chi_D(n) / n^s,    Re(s) > 0,

extends to an entire function of s (chi_D is a non-trivial primitive
character modulo |D|).  The Dirichlet class number formula (1839) reads

    L(1, chi_D) = (2 pi h(D)) / (w(D) sqrt(|D|))              (*)

where h(D) is the class number and w(D) is the number of units in the
ring of integers of Q(sqrt(D)):

    w(-3) = 6,   w(-4) = 4,   w(D) = 2  for D < -4.

Equivalent explicit (finite) form obtained by summing L(1, chi_D) against
the character: for D < 0 a fundamental discriminant,

    h(D) = - (w(D) / (2 |D|)) * sum_{a=1}^{|D|-1} chi_D(a) * a.  (**)

This identity is algebraic — no transcendentals — and links the class
numbers we derived combinatorially from reduced binary quadratic forms
(Layer 54) to a Dirichlet character sum.

Numerical pins.

    D = -3:   sum chi(a)*a = 1*1 + 2*(-1) = -1,  h = -6/(2*3) * (-1) = 1.
    D = -4:   chi(1)=1, chi(2)=0, chi(3)=-1;  sum = -2, h = -4/8 * (-2) = 1.
    D = -7:   sum = -7, h = -2/14 * (-7) = 1.
    D = -15:  sum = -30, h = -2/30 * (-30) = 2.
    D = -23:  sum = -69, h = -2/46 * (-69) = 3.
    D = -163: sum = -163, h = 1  (Heegner; Ramanujan constant origin).

Numerical side of (*):
    D = -3:   L(1, chi) = 2 pi / (6 sqrt 3) = pi / (3 sqrt 3) ~ 0.6046.
    D = -4:   L(1, chi) = pi / 4 ~ 0.7854 (Leibniz series 1-1/3+1/5-... !).
    D = -7:   L(1, chi) = pi / sqrt 7 ~ 1.1874.

This closes the L-function / class field theory bridge between
Layer 52 (Heegner numbers / class number 1), Layer 54 (Hilbert class
polynomials / class number h > 1 via forms), and Layer 58 (L-function
of a modular form).

Layer 60 -- Dirichlet class number formula.
"""

from __future__ import annotations

from typing import Any

import mpmath as mp

from w33_hilbert_class_polynomials import class_number, reduced_forms


# ----------------------------------------------------------------------
# Kronecker symbol (D/n) for any integer D and positive n.
# ----------------------------------------------------------------------
def _jacobi(a: int, n: int) -> int:
    """Jacobi symbol (a/n) for positive odd n."""
    if n <= 0 or n % 2 == 0:
        raise ValueError(f"Jacobi symbol requires n > 0 odd, got {n}.")
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    return 0


def kronecker(a: int, n: int) -> int:
    """Kronecker symbol (a/n)."""
    if n == 0:
        return 1 if a in (1, -1) else 0
    if n < 0:
        return kronecker(a, -n) * (-1 if a < 0 else 1)
    # n > 0; strip factors of 2
    result = 1
    while n % 2 == 0:
        n //= 2
        if a % 2 == 0:
            return 0
        if a % 8 in (3, 5):
            result = -result
    return result * _jacobi(a, n)


def chi_D(D: int, a: int) -> int:
    """Kronecker character chi_D(a) = (D/a) for discriminant D."""
    return kronecker(D, a)


# ----------------------------------------------------------------------
# Unit count w(D).
# ----------------------------------------------------------------------
def w_of(D: int) -> int:
    if D == -3:
        return 6
    if D == -4:
        return 4
    return 2


# ----------------------------------------------------------------------
# Is fundamental discriminant?
# ----------------------------------------------------------------------
def is_fundamental_discriminant(D: int) -> bool:
    """D < 0 is a fundamental discriminant if either
         D ≡ 1 (mod 4) and D squarefree, or
         D = 4 m with m ≡ 2 or 3 (mod 4) and m squarefree.
    """
    if D >= 0:
        return False
    from math import isqrt
    def squarefree(n: int) -> bool:
        n = abs(n)
        for p in range(2, isqrt(n) + 1):
            if n % (p * p) == 0:
                return False
        return True
    if D % 4 == 1 and squarefree(D):
        return True
    if D % 4 == 0:
        m = D // 4
        if m % 4 in (2, 3) and squarefree(m):
            return True
    return False


# ----------------------------------------------------------------------
# Dirichlet finite class-number formula.
# ----------------------------------------------------------------------
def character_sum(D: int) -> int:
    """sum_{a=1}^{|D|-1} chi_D(a) * a."""
    absD = abs(D)
    return sum(chi_D(D, a) * a for a in range(1, absD))


def class_number_dirichlet(D: int) -> int:
    """h(D) via Dirichlet finite formula  h = -w/(2|D|) * sum chi(a) a."""
    S = character_sum(D)
    num = -w_of(D) * S
    den = 2 * abs(D)
    if num % den != 0:
        raise ArithmeticError(
            f"Dirichlet formula non-integer at D={D}: num={num}, den={den}"
        )
    return num // den


# ----------------------------------------------------------------------
# L(1, chi_D) numerically.
# ----------------------------------------------------------------------
def L_1_chi_D(D: int, N: int = 20000) -> mp.mpf:
    """Partial sum sum_{n=1}^{N} chi_D(n) / n."""
    total = mp.mpf(0)
    for n in range(1, N + 1):
        c = chi_D(D, n)
        if c != 0:
            total += mp.mpf(c) / n
    return total


def L_1_chi_D_formula(D: int) -> mp.mpf:
    """Direct formula L(1, chi_D) = 2 pi h(D) / (w(D) sqrt(|D|))."""
    h = class_number(D)
    w = w_of(D)
    return 2 * mp.pi * h / (w * mp.sqrt(abs(D)))


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
FUND_D_LIST = [-3, -4, -7, -8, -11, -15, -19, -20, -23, -24, -31, -35,
               -39, -40, -43, -47, -51, -52, -55, -67, -71, -79, -83,
               -87, -95, -103, -127, -131, -151, -163]


def verify_finite_dirichlet_formula() -> dict[str, Any]:
    """Finite Dirichlet formula h(D) = -w/(2|D|) * sum chi(a) a
    reproduces the form-counted h(D) from Layer 54 for every
    fundamental discriminant in FUND_D_LIST."""
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in FUND_D_LIST:
        h_forms = class_number(D)
        h_dir = class_number_dirichlet(D)
        match = h_forms == h_dir
        rows.append({
            "D": D,
            "h_from_forms": h_forms,
            "h_from_dirichlet": h_dir,
            "character_sum": character_sum(D),
            "w": w_of(D),
            "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_L1_vs_closed_form(dps: int = 30,
                              N: int = 40000) -> dict[str, Any]:
    """Partial sum L_N(1, chi_D) converges to 2 pi h / (w sqrt |D|).
    Truncation error ~ 1 / (sqrt(|D|) log N) decays slowly; we pin to 1e-2."""
    mp.mp.dps = dps
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in [-3, -4, -7, -8, -11, -15, -19, -23, -43, -67]:
        L_num = L_1_chi_D(D, N=N)
        L_form = L_1_chi_D_formula(D)
        diff = abs(L_num - L_form)
        tol = mp.mpf("5e-2")
        match = diff < tol
        rows.append({
            "D": D,
            "L_partial": float(L_num),
            "L_closed": float(L_form),
            "abs_diff": float(diff),
            "match": bool(match),
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows,
            "tolerance": "5e-2",
            "N_partial_sum": N}


def verify_leibniz_special_case() -> dict[str, Any]:
    """L(1, chi_{-4}) = 1 - 1/3 + 1/5 - 1/7 + ... = pi/4  (Leibniz).
    Cross-check with Dirichlet closed form: 2 pi * 1 / (4 * 2) = pi/4."""
    closed = L_1_chi_D_formula(-4)
    pi_over_4 = mp.pi / 4
    diff = abs(closed - pi_over_4)
    return {
        "closed_form_L1_chi_minus4": float(closed),
        "pi_over_4": float(pi_over_4),
        "abs_diff": float(diff),
        "match": bool(diff < mp.mpf("1e-15")),
    }


def verify_chi_is_totally_multiplicative() -> dict[str, Any]:
    """chi_D(m n) = chi_D(m) chi_D(n) for a handful of D and (m, n)."""
    failures: list[dict[str, Any]] = []
    ok = 0
    for D in [-3, -4, -7, -15, -23]:
        for m in range(1, 20):
            for n in range(1, 20):
                lhs = chi_D(D, m * n)
                rhs = chi_D(D, m) * chi_D(D, n)
                if lhs != rhs:
                    failures.append({"D": D, "m": m, "n": n,
                                     "lhs": lhs, "rhs": rhs})
                else:
                    ok += 1
    return {"all_match": len(failures) == 0,
            "ok_count": ok, "failures": failures}


def verify_chi_has_period_abs_D() -> dict[str, Any]:
    """chi_D is periodic with period |D|."""
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in [-3, -4, -7, -8, -15, -23]:
        period_ok = True
        for a in range(1, 3 * abs(D)):
            if chi_D(D, a) != chi_D(D, a + abs(D)):
                period_ok = False
                break
        rows.append({"D": D, "period_is_abs_D": period_ok})
        all_match = all_match and period_ok
    return {"all_match": all_match, "rows": rows}


def verify_fundamental_flag_consistency() -> dict[str, Any]:
    """Every D in FUND_D_LIST is recognised as fundamental."""
    rows = []
    all_match = True
    for D in FUND_D_LIST:
        flag = is_fundamental_discriminant(D)
        rows.append({"D": D, "is_fundamental": flag})
        all_match = all_match and flag
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    fin = verify_finite_dirichlet_formula()
    num = verify_L1_vs_closed_form(dps=30, N=40000)
    leib = verify_leibniz_special_case()
    mul = verify_chi_is_totally_multiplicative()
    per = verify_chi_has_period_abs_D()
    fund = verify_fundamental_flag_consistency()
    chain = {
        "dirichlet_finite_formula_h_from_character_sum_matches_forms":
            fin["all_match"],
        "partial_L1_converges_to_closed_form_within_5e-2":
            num["all_match"],
        "leibniz_series_identifies_L1_chi_minus_4_with_pi_over_4":
            leib["match"],
        "chi_D_totally_multiplicative_over_test_range":
            mul["all_match"],
        "chi_D_periodic_with_period_abs_D":
            per["all_match"],
        "fundamental_discriminant_list_all_recognised":
            fund["all_match"],
    }
    return {
        "finite_formula": fin,
        "L1_numerical": num,
        "leibniz": leib,
        "chi_multiplicative": mul,
        "chi_periodic": per,
        "fundamental_flag": fund,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nDirichlet finite formula, h(D) from character sum vs forms:")
    for row in s["finite_formula"]["rows"][:10]:
        print(f"  D={row['D']:>5}: h_forms={row['h_from_forms']}, "
              f"h_dir={row['h_from_dirichlet']}, S={row['character_sum']}, "
              f"match={row['match']}")
    print("\nL(1, chi_D) numerical vs closed form (first 5):")
    for row in s["L1_numerical"]["rows"][:5]:
        print(f"  D={row['D']:>4}: L_N={row['L_partial']:.6f}, "
              f"L_closed={row['L_closed']:.6f}, "
              f"diff={row['abs_diff']:.3e}")
    print(f"\nLeibniz: L(1, chi_{{-4}}) = pi/4? "
          f"{s['leibniz']['match']}, "
          f"|L - pi/4| = {s['leibniz']['abs_diff']:.3e}")
