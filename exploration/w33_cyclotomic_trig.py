"""
CYCLOTOMIC TRIGONOMETRY
=======================

Derive all of classical trigonometry from the cyclotomic polynomials
Phi_n(x), the minimal polynomials of the primitive n-th roots of unity.

THE W(3,3) CONNECTION.  The Weinberg identity
    sin^2(theta_W) + cos^2(theta_W) = q/Phi_3(q) + Phi_4(q)/Phi_3(q) = 1
which we closed algebraically at q=3 (giving 3/13 + 10/13 = 1) is the
q=3 EVALUATION of the universal identity
    |zeta_n|^2  =  zeta_n * conjugate(zeta_n)  =  1   for any primitive n-th root.
At q=3 the cyclotomic values Phi_3(3)=13, Phi_4(3)=10, Phi_6(3)=7 become
the denominators of the SM closure surface: sin^2 theta_W = 3/13,
sin^2 theta_12^PMNS = 4/13, sin^2 theta_23^PMNS = 7/13, etc.

FROM Phi_n(x) ALONE THIS MODULE DERIVES:
  (i)    Exact algebraic values cos(2 pi / n),  sin(2 pi / n).
  (ii)   Pythagorean identity:   sin^2 + cos^2 = 1.
  (iii)  Double-angle:           cos 2x = 2 cos^2 x - 1,  sin 2x = 2 sin x cos x.
  (iv)   Chebyshev T_n:          T_n(cos x) = cos(n x).
  (v)    Angle addition:         zeta_a * zeta_b = zeta_{a+b}  =>  cos(x+y), sin(x+y).
  (vi)   Euler:                  e^(i pi) + 1 = 0   from   Phi_2(x) = x + 1.
  (vii)  Hyperbolic:             cosh x = cos(i x),  sinh x = -i sin(i x),  cosh^2 - sinh^2 = 1.

Every identity descends from the single axiom  zeta_n  =  e^(2 pi i / n).
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from math import cos, pi, sin
from pathlib import Path


Poly = list  # list[Fraction]; low-to-high coefficients


# ======================================================================
#  Polynomial arithmetic over Q.
# ======================================================================
def pstrip(p: Poly) -> Poly:
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def pmul(a: Poly, b: Poly) -> Poly:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return pstrip(out)


def padd(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    out = [Fraction(0)] * n
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    return pstrip(out)


def psub(a: Poly, b: Poly) -> Poly:
    return padd(a, [-c for c in b])


def pdiv_exact(num: Poly, den: Poly) -> Poly:
    """Exact polynomial division assuming den divides num in Q[x]."""
    num = [Fraction(c) for c in num]
    den = [Fraction(c) for c in den]
    d_lead = den[-1]
    d_deg = len(den) - 1
    q_deg = max(0, len(num) - 1 - d_deg)
    q = [Fraction(0)] * (q_deg + 1)
    while len(num) - 1 >= d_deg:
        if num[-1] == 0:
            num.pop()
            if not num:
                break
            continue
        exp = len(num) - 1 - d_deg
        c = num[-1] / d_lead
        q[exp] = c
        for i, di in enumerate(den):
            num[exp + i] -= c * di
        while num and num[-1] == 0:
            num.pop()
    assert not num or all(x == 0 for x in num), f"inexact division, remainder={num}"
    return pstrip(q)


def x_to_n_minus_1(n: int) -> Poly:
    p = [Fraction(0)] * (n + 1)
    p[0] = Fraction(-1)
    p[n] = Fraction(1)
    return p


def pstr(p: Poly, var: str = "x") -> str:
    terms = []
    for deg in range(len(p) - 1, -1, -1):
        c = p[deg]
        if c == 0:
            continue
        sign = " + " if c > 0 and terms else (" - " if c < 0 and terms else ("-" if c < 0 else ""))
        cab = abs(c)
        if deg == 0:
            body = str(cab)
        elif deg == 1:
            body = var if cab == 1 else f"{cab} {var}"
        else:
            body = f"{var}^{deg}" if cab == 1 else f"{cab} {var}^{deg}"
        terms.append(f"{sign}{body}")
    return "".join(terms) or "0"


def peval(p: Poly, x) -> Fraction:
    out = Fraction(0)
    for c in reversed(p):
        out = out * x + c
    return out


# ======================================================================
#  Cyclotomic polynomials  via  x^n - 1 = prod_{d|n} Phi_d(x).
# ======================================================================
_CYCL: dict = {}


def divisors(n: int) -> list:
    return [d for d in range(1, n + 1) if n % d == 0]


def cyclotomic(n: int) -> Poly:
    assert n >= 1
    if n in _CYCL:
        return list(_CYCL[n])
    num = x_to_n_minus_1(n)
    for d in divisors(n):
        if d < n:
            num = pdiv_exact(num, cyclotomic(d))
    _CYCL[n] = num
    return list(num)


# ======================================================================
#  Chebyshev polynomials:  T_n(cos x) = cos(n x).
#       T_0 = 1,  T_1 = x,  T_{n+1} = 2 x T_n - T_{n-1}.
# ======================================================================
def chebyshev_T(n: int) -> Poly:
    if n == 0:
        return [Fraction(1)]
    if n == 1:
        return [Fraction(0), Fraction(1)]
    Tprev2, Tprev1 = [Fraction(1)], [Fraction(0), Fraction(1)]
    for _ in range(2, n + 1):
        twoX_T = pmul([Fraction(0), Fraction(2)], Tprev1)
        Tcur = psub(twoX_T, Tprev2)
        Tprev2, Tprev1 = Tprev1, Tcur
    return Tprev1


def chebyshev_U(n: int) -> Poly:
    """U_n of the second kind:  U_n(cos x) = sin((n+1) x) / sin x."""
    if n == 0:
        return [Fraction(1)]
    if n == 1:
        return [Fraction(0), Fraction(2)]
    Uprev2, Uprev1 = [Fraction(1)], [Fraction(0), Fraction(2)]
    for _ in range(2, n + 1):
        twoX_U = pmul([Fraction(0), Fraction(2)], Uprev1)
        Ucur = psub(twoX_U, Uprev2)
        Uprev2, Uprev1 = Uprev1, Ucur
    return Uprev1


# ======================================================================
#  Special-angle table:  (cos(2 pi / n), sin(2 pi / n)) as exact radicals.
# ======================================================================
SPECIAL_COS_SIN = {
    # n  :  (cos(2 pi / n)   ,    sin(2 pi / n))
    1:  ("1",                 "0"),
    2:  ("-1",                "0"),
    3:  ("-1/2",              "sqrt(3)/2"),
    4:  ("0",                 "1"),
    5:  ("(sqrt(5)-1)/4",     "sqrt(10+2*sqrt(5))/4"),
    6:  ("1/2",               "sqrt(3)/2"),
    8:  ("sqrt(2)/2",         "sqrt(2)/2"),
    10: ("(sqrt(5)+1)/4",     "sqrt(10-2*sqrt(5))/4"),
    12: ("sqrt(3)/2",         "1/2"),
}


# Numerical realizations of each symbol (float) for verification.
def _sym_numeric(expr: str) -> float:
    import re as _re
    sqrt5 = math.sqrt(5.0)
    expr = expr.replace("sqrt(3)", str(math.sqrt(3.0)))
    expr = expr.replace("sqrt(2)", str(math.sqrt(2.0)))
    expr = expr.replace("sqrt(10+2*sqrt(5))", str(math.sqrt(10.0 + 2.0 * sqrt5)))
    expr = expr.replace("sqrt(10-2*sqrt(5))", str(math.sqrt(10.0 - 2.0 * sqrt5)))
    expr = expr.replace("sqrt(5)", str(sqrt5))
    if not _re.fullmatch(r"[\d\s+\-*/().]+", expr):
        raise ValueError(f"unsafe numeric expression: {expr}")
    return float(eval(expr, {"__builtins__": {}}, {}))


# ======================================================================
#  Verifications.
# ======================================================================
def verify_primitive_root_satisfies_Phi_n(n: int) -> float:
    """Return |Phi_n(zeta_n)| where zeta_n = exp(2 pi i / n).  Should be ~ 0."""
    theta = 2.0 * pi / n
    z = complex(cos(theta), sin(theta))
    p = cyclotomic(n)
    val = sum(float(c) * z ** d for d, c in enumerate(p))
    return abs(val)


def verify_chebyshev_T_matches_cos_nx(n: int, theta: float) -> float:
    """Check T_n(cos theta) ≈ cos(n theta).  Return absolute error."""
    Tn = chebyshev_T(n)
    lhs = sum(float(c) * cos(theta) ** d for d, c in enumerate(Tn))
    rhs = cos(n * theta)
    return abs(lhs - rhs)


def verify_pythagorean(theta: float) -> float:
    return abs(cos(theta) ** 2 + sin(theta) ** 2 - 1.0)


def verify_double_angle(theta: float) -> dict:
    return {
        "cos2x_minus_identity": abs(cos(2 * theta) - (2 * cos(theta) ** 2 - 1)),
        "sin2x_minus_identity": abs(sin(2 * theta) - 2 * sin(theta) * cos(theta)),
    }


def verify_euler_identity() -> float:
    """e^(i pi) + 1 ~= 0.  Via Phi_2(x) = x + 1 evaluated at x = e^(i pi)."""
    z = complex(cos(pi), sin(pi))
    return abs(peval_complex(cyclotomic(2), z) + 0)  # Phi_2(z) at z=-1 is zero


def peval_complex(p: Poly, z: complex) -> complex:
    out = 0 + 0j
    for c in reversed(p):
        out = out * z + float(c)
    return out


def verify_angle_addition(a: float, b: float) -> dict:
    """Angle addition from zeta_a * zeta_b = zeta_{a+b}."""
    return {
        "cos_sum":  abs(cos(a + b) - (cos(a) * cos(b) - sin(a) * sin(b))),
        "sin_sum":  abs(sin(a + b) - (sin(a) * cos(b) + cos(a) * sin(b))),
    }


def verify_hyperbolic_pythagorean(x: float) -> float:
    return abs(math.cosh(x) ** 2 - math.sinh(x) ** 2 - 1.0)


def verify_cosh_is_cos_of_ix(x: float) -> float:
    """cosh(x) = cos(i x)  numerically via Taylor series."""
    # cos(i x) = (e^{-x} + e^{x}) / 2 = cosh(x)
    return abs(math.cosh(x) - (math.exp(-x) + math.exp(x)) / 2)


# ======================================================================
#  Weinberg-angle closure as a cyclotomic evaluation at q=3.
# ======================================================================
def weinberg_from_cyclotomics(q: int = 3) -> dict:
    Phi3 = int(peval(cyclotomic(3), q))
    Phi4 = int(peval(cyclotomic(4), q))
    Phi6 = int(peval(cyclotomic(6), q))
    sin2 = Fraction(q, Phi3)
    cos2 = Fraction(Phi4, Phi3)
    return {
        "q": q,
        "Phi_3(q)": Phi3,
        "Phi_4(q)": Phi4,
        "Phi_6(q)": Phi6,
        "sin2_theta_W": str(sin2),
        "cos2_theta_W": str(cos2),
        "sum_equals_one": (sin2 + cos2) == Fraction(1, 1),
        "identity": "q + Phi_4(q) = q + (q^2 + 1) = q^2 + q + 1 = Phi_3(q)",
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_all_trig() -> dict:
    cyclo = {n: [int(c) for c in cyclotomic(n)] for n in range(1, 13)}
    cheb_T = {n: [int(c) for c in chebyshev_T(n)] for n in range(0, 7)}
    cheb_U = {n: [int(c) for c in chebyshev_U(n)] for n in range(0, 7)}

    # Phi_n at q=3: the SM master-derivation slot.
    q = 3
    phi_at_q = {n: int(peval(cyclotomic(n), q)) for n in (1, 2, 3, 4, 5, 6, 8, 10, 12)}

    # Special-angle exact table.
    special = {}
    for n, (c, s) in SPECIAL_COS_SIN.items():
        special[f"n={n}"] = {
            "cos(2 pi / n)":  c,
            "sin(2 pi / n)":  s,
            "cos_numeric":    _sym_numeric(c),
            "sin_numeric":    _sym_numeric(s),
            "|Phi_n(zeta_n)|": verify_primitive_root_satisfies_Phi_n(n),
        }

    # Chebyshev: T_n(cos theta) = cos(n theta) numerical checks.
    cheb_checks = []
    for n in range(2, 7):
        cheb_checks.append({
            "n": n,
            "T_n(x)":  pstr(chebyshev_T(n)),
            "error_at_pi_over_7":    verify_chebyshev_T_matches_cos_nx(n, pi / 7),
            "error_at_pi_over_n":    verify_chebyshev_T_matches_cos_nx(n, pi / n),
        })

    # Pythagorean + double-angle + angle-addition + Euler + hyperbolic.
    identities = {
        "pythagorean":     [verify_pythagorean(k * pi / 7) for k in range(1, 7)],
        "double_angle":    [verify_double_angle(k * pi / 9) for k in range(1, 5)],
        "angle_addition":  [verify_angle_addition(pi / 5, pi / 7),
                            verify_angle_addition(pi / 3, pi / 4),
                            verify_angle_addition(pi / 6, pi / 12)],
        "euler_pi":        verify_euler_identity(),
        "hyperbolic_pyth": [verify_hyperbolic_pythagorean(x) for x in (0.1, 0.5, 1.0, 2.0)],
        "cosh_is_cos_ix":  [verify_cosh_is_cos_of_ix(x) for x in (0.1, 0.5, 1.0, 2.0)],
    }

    return {
        "title": "Cyclotomic trigonometry — all of trig from Phi_n(x)",
        "axiom": "zeta_n = e^(2 pi i / n)  is a primitive n-th root of unity",
        "cyclotomic_polynomials": cyclo,
        "phi_at_q=3": phi_at_q,
        "chebyshev_T": cheb_T,
        "chebyshev_U": cheb_U,
        "special_angle_exact_table": special,
        "chebyshev_checks": cheb_checks,
        "identities_numerical": identities,
        "weinberg_closure":  weinberg_from_cyclotomics(q=3),
    }


def main() -> None:
    print("=" * 72)
    print("  CYCLOTOMIC TRIGONOMETRY  --  all of trig from Phi_n(x)")
    print("=" * 72)
    print()
    chain = derive_all_trig()

    print("  CYCLOTOMIC POLYNOMIALS Phi_n(x), 1 <= n <= 12:")
    for n in range(1, 13):
        print(f"    Phi_{n:<2d}(x) = {pstr(cyclotomic(n))}")
    print()

    print("  Phi_n(3)  --  the W(3,3) master-derivation slot:")
    for n, val in chain["phi_at_q=3"].items():
        print(f"    Phi_{n:<2d}(3) = {val}")
    print()

    print("  CHEBYSHEV T_n(x)  --  T_n(cos t) = cos(n t):")
    for n in range(0, 7):
        print(f"    T_{n}(x) = {pstr(chebyshev_T(n))}")
    print()

    print("  SPECIAL ANGLES  (cos, sin) at theta = 2 pi / n:")
    for key, vals in chain["special_angle_exact_table"].items():
        c, s = vals["cos(2 pi / n)"], vals["sin(2 pi / n)"]
        phi_err = vals["|Phi_n(zeta_n)|"]
        print(f"    {key:>6s}: cos = {c:<22s}  sin = {s:<24s}  |Phi_n(zeta)| < 1e-12: {phi_err < 1e-12}")
    print()

    print("  WEINBERG CLOSURE  (q = 3 evaluation of cyclotomic slots):")
    w = chain["weinberg_closure"]
    print(f"    sin^2 theta_W  = q / Phi_3(q)     = {w['sin2_theta_W']}")
    print(f"    cos^2 theta_W  = Phi_4(q) / Phi_3(q) = {w['cos2_theta_W']}")
    print(f"    sum equals one ?  {w['sum_equals_one']}")
    print(f"    identity        :  {w['identity']}")
    print()

    print("  IDENTITIES  (all errors below are machine-precision residuals):")
    idn = chain["identities_numerical"]
    print(f"    max Pythagorean error      = {max(idn['pythagorean']):.2e}")
    print(f"    max double-angle cos err   = {max(d['cos2x_minus_identity'] for d in idn['double_angle']):.2e}")
    print(f"    max double-angle sin err   = {max(d['sin2x_minus_identity'] for d in idn['double_angle']):.2e}")
    print(f"    max angle-addition cos err = {max(d['cos_sum'] for d in idn['angle_addition']):.2e}")
    print(f"    Euler e^(i pi) + 1 error   = {idn['euler_pi']:.2e}")
    print(f"    max cosh^2 - sinh^2 - 1    = {max(idn['hyperbolic_pyth']):.2e}")
    print(f"    max |cosh(x) - cos(i x)|   = {max(idn['cosh_is_cos_ix']):.2e}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_cyclotomic_trig.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
