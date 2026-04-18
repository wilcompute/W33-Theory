"""Hilbert class polynomials H_D(x) for imaginary quadratic discriminants.

For a negative fundamental discriminant D with class number h(D), the
Hilbert class polynomial is

    H_D(x) = prod_{[a,b,c]} (x - j(tau_{[a,b,c]})) in Z[x],

where the product runs over all h(D) SL_2(Z)-inequivalent reduced binary
quadratic forms [a, b, c] of discriminant D and

    tau_{[a,b,c]} = (-b + sqrt(D)) / (2a).

Theorem (class field theory, Weber / Deuring).  H_D(x) has integer
coefficients, is monic, irreducible over Q, and its roots are algebraic
integers — the j-invariants of elliptic curves with CM by the order of
discriminant D.  The splitting field Q(sqrt D)(j(tau_D)) is the
Hilbert class field of Q(sqrt D).

This layer closes the CM ladder beyond the class-number-1 base:

    Layer 52 (9 Heegner numbers, degree 1):
        H_{-3}  = x
        H_{-4}  = x - 1728
        H_{-7}  = x + 3375
        ...
        H_{-163} = x + 640320^3

    this Layer (class number 2 and 3):
        H_{-15}(x) = x^2 + 191025 x - 121287375         (h = 2)
        H_{-20}(x) = x^2 - 1264000 x - 681472000        (h = 2)
        H_{-24}(x) = x^2 - 4834944 x + 14670139392      (h = 2)
        H_{-23}(x) = x^3 + 3491750 x^2 - 5151296875 x
                      + 12771880859375                    (h = 3)
        H_{-31}(x) = x^3 + 39491307 x^2 - 58682638134 x
                      + 1566028350940383                  (h = 3)

    plus the Heegner-1 coincidences:
        H_{-163}(x) = x + 262537412640768000 (linear!)
"""

from __future__ import annotations

from typing import Any

import mpmath as mp


# ----------------------------------------------------------------------
# Reduced binary quadratic forms [a, b, c] of given negative discriminant.
# ----------------------------------------------------------------------
def reduced_forms(D: int) -> list[tuple[int, int, int]]:
    """List reduced primitive binary quadratic forms of discriminant D < 0.

    Conditions: b^2 - 4ac = D;  |b| <= a <= c;
                gcd(a, b, c) = 1;
                if |b| = a or a = c, then b >= 0.
    """
    if D >= 0 or D % 4 not in (0, 1):
        raise ValueError(f"D = {D} is not a valid negative discriminant.")
    forms: list[tuple[int, int, int]] = []
    abs_D = -D
    # a <= sqrt(-D/3)
    import math
    a_max = int(math.isqrt(abs_D // 3)) + 1
    for a in range(1, a_max + 1):
        for b in range(-a, a + 1):
            if (b * b - D) % (4 * a) != 0:
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            # Boundary condition: if |b|=a or a=c, require b>=0.
            if (abs(b) == a or a == c) and b < 0:
                continue
            # Primitive: gcd(a,b,c) = 1.
            from math import gcd
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            forms.append((a, b, c))
    return forms


def class_number(D: int) -> int:
    return len(reduced_forms(D))


# ----------------------------------------------------------------------
# CM point tau for a form and its q-value.
# ----------------------------------------------------------------------
def form_to_tau(a: int, b: int, c: int) -> mp.mpc:
    """tau = (-b + i sqrt(-D)) / (2a) for D = b^2 - 4ac < 0."""
    D = b * b - 4 * a * c
    if D >= 0:
        raise ValueError("Positive discriminant form.")
    return mp.mpc(mp.mpf(-b) / (2 * a), mp.sqrt(-D) / (2 * a))


# ----------------------------------------------------------------------
# j-function at a CM point via q-expansion + adaptive term count.
# ----------------------------------------------------------------------
# First 30 coefficients of (j - 744) = 1/q + 196884 q + 21493760 q^2 + ... (OEIS A000521)
J_COEFFS_EXPANSION: list[int] = [
    196884,
    21493760,
    864299970,
    20245856256,
    333202640600,
    4252023300096,
    44656994071935,
    401490886656000,
    3176440229784420,
    22567393309593600,
    146211911499519294,
    874313719685775360,
    4872010111798142520,
    25497827389410525184,
    126142916465781843075,
    593121772421445058560,
    2662842413150775245160,
    11459912788444786513920,
    47438786801234168813250,
    189449976248893390028800,
    731811377318137519245696,
    2740630712513624654929920,
    9971041659937182693533820,
    35307453186561427099877376,
    122054634182323573315252104,
    412463390495514941051024640,
    1365808217381277708561875904,
    4434007813930041865342435840,
    14133873762765142529451225300,
    44273269634895040832135317440,
]


def j_at_tau(tau: mp.mpc, n_terms: int = 30) -> mp.mpc:
    """j(tau) = 1/q + 744 + sum_{n>=1} c_n q^n with q = exp(2 pi i tau)."""
    q = mp.exp(2j * mp.pi * tau)
    j = 1 / q + mp.mpf(744)
    for i in range(min(n_terms, len(J_COEFFS_EXPANSION))):
        j += J_COEFFS_EXPANSION[i] * q ** (i + 1)
    return j


# ----------------------------------------------------------------------
# Reference Hilbert class polynomials (monic, coeffs in Z).
# Keys are (negative) fundamental discriminants.
# Values are coefficient lists, constant first: H_D(x) = sum c_i x^i.
# ----------------------------------------------------------------------
HILBERT_CLASS_POLYS: dict[int, list[int]] = {
    # Class number 1 (9 Heegner).
    -3:   [0, 1],                        # x
    -4:   [-1728, 1],                    # x - 1728
    -7:   [3375, 1],                     # x + 3375
    -8:   [-8000, 1],                    # x - 8000
    -11:  [32768, 1],                    # x + 32768
    -19:  [884736, 1],                   # x + 884736
    -43:  [884736000, 1],                # x + 884736000
    -67:  [147197952000, 1],             # x + 147197952000
    -163: [262537412640768000, 1],       # x + 262537412640768000
    # Class number 2.
    -15:  [-121287375, 191025, 1],       # x^2 + 191025 x - 121287375
    -20:  [-681472000, -1264000, 1],     # x^2 - 1264000 x - 681472000
    -24:  [14670139392, -4834944, 1],    # x^2 - 4834944 x + 14670139392
    -35:  [-134217728000, 117964800, 1], # x^2 + 117964800 x - 134217728000
    -40:  [9103145472000, -425692800, 1],  # x^2 - 425692800 x + 9103145472000
    -51:  [6262062317568, 5541101568, 1],  # x^2 + 5541101568 x + 6262062317568
    -52:  [-567663552000000, -6896880000, 1],  # x^2 - 6896880000 x - 567663552000000
    # Class number 3.
    -23:  [12771880859375, -5151296875, 3491750, 1],  # x^3 + 3491750 x^2 - 5151296875 x + 12771880859375
    -31:  [1566028350940383, -58682638134, 39491307, 1],
}


# ----------------------------------------------------------------------
# Numerical polynomial from the CM j-values.
# ----------------------------------------------------------------------
def build_poly_from_roots(roots: list[mp.mpc]) -> list[mp.mpc]:
    """Monic polynomial H(x) = prod (x - r_i), returned as [c_0,...,c_n]."""
    poly: list[mp.mpc] = [mp.mpc(1)]
    for r in roots:
        new_poly = [mp.mpc(0)] * (len(poly) + 1)
        for i, c in enumerate(poly):
            new_poly[i + 1] += c
            new_poly[i] += -r * c
        poly = new_poly
    return poly


def numerical_class_poly(D: int, dps: int = 60, n_terms: int = 30) -> list[mp.mpc]:
    mp.mp.dps = dps
    forms = reduced_forms(D)
    taus = [form_to_tau(a, b, c) for (a, b, c) in forms]
    js = [j_at_tau(tau, n_terms=n_terms) for tau in taus]
    return build_poly_from_roots(js)


# ----------------------------------------------------------------------
# Verifier: numerical Hilbert polynomial rounds to reference integers.
# ----------------------------------------------------------------------
def verify_hilbert_polynomial(D: int, dps: int = 80) -> dict[str, Any]:
    mp.mp.dps = dps
    num_poly = numerical_class_poly(D, dps=dps, n_terms=30)
    ref = HILBERT_CLASS_POLYS[D]
    if len(num_poly) != len(ref):
        return {"D": D, "match": False, "reason": "degree mismatch",
                "degree_expected": len(ref) - 1,
                "degree_numerical": len(num_poly) - 1}
    deviations: list[float] = []
    coeff_checks: list[dict[str, Any]] = []
    all_match = True
    for i, (nc, rc) in enumerate(zip(num_poly, ref)):
        real_err = abs(nc.real - rc)
        imag_err = abs(nc.imag)
        scale = max(abs(mp.mpf(rc)), mp.mpf(1))
        match = (real_err < scale * mp.mpf("1e-20")) and imag_err < mp.mpf("1e-10")
        deviations.append(float(real_err) if real_err < mp.mpf("1e10") else None)
        coeff_checks.append({
            "i": i,
            "expected": rc,
            "numerical_real": float(nc.real) if abs(nc.real) < 1e18 else str(nc.real),
            "abs_err": float(real_err) if real_err < mp.mpf("1e10") else str(real_err),
            "match": bool(match),
        })
        all_match = all_match and bool(match)
    return {
        "D": D,
        "class_number": len(reduced_forms(D)),
        "match": bool(all_match),
        "degree": len(ref) - 1,
        "coeff_checks": coeff_checks,
    }


def verify_all_tabulated(dps: int = 80) -> dict[str, Any]:
    results = [verify_hilbert_polynomial(D, dps=dps) for D in HILBERT_CLASS_POLYS]
    return {
        "all_match": all(r["match"] for r in results),
        "rows": results,
        "dps_used": dps,
    }


# ----------------------------------------------------------------------
# Sanity: class numbers of tabulated discriminants.
# ----------------------------------------------------------------------
EXPECTED_CLASS_NUMBERS: dict[int, int] = {
    -3: 1, -4: 1, -7: 1, -8: 1, -11: 1, -19: 1, -43: 1, -67: 1, -163: 1,
    -15: 2, -20: 2, -24: 2, -35: 2, -40: 2, -51: 2, -52: 2,
    -23: 3, -31: 3,
}


def verify_class_numbers() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    all_match = True
    for D, h_expected in EXPECTED_CLASS_NUMBERS.items():
        h = class_number(D)
        match = h == h_expected
        rows.append({"D": D, "h": h, "expected": h_expected, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Special linear check: for each Heegner d, our polynomial is x - j(tau_d).
# ----------------------------------------------------------------------
HEEGNER_DISCRIMINANTS = [-3, -4, -7, -8, -11, -19, -43, -67, -163]


def verify_linear_case_is_monic_x_minus_j(dps: int = 60) -> dict[str, Any]:
    mp.mp.dps = dps
    rows: list[dict[str, Any]] = []
    all_match = True
    for D in HEEGNER_DISCRIMINANTS:
        forms = reduced_forms(D)
        assert len(forms) == 1, f"D={D} is class-number-1 but got {len(forms)} forms"
        tau = form_to_tau(*forms[0])
        j = j_at_tau(tau, n_terms=30)
        expected_constant = HILBERT_CLASS_POLYS[D][0]  # -j
        err = abs(j.real - (-expected_constant))
        match = err < mp.mpf("1e-15")
        rows.append({
            "D": D,
            "j": float(j.real) if abs(j.real) < 1e18 else str(j.real),
            "-H_D[0]": -expected_constant,
            "abs_err": float(err) if err < 1e10 else str(err),
            "match": bool(match),
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    class_nums = verify_class_numbers()
    linear = verify_linear_case_is_monic_x_minus_j(dps=60)
    polys = verify_all_tabulated(dps=80)
    chain = {
        "class_numbers_match_tabulated": class_nums["all_match"],
        "heegner_linear_polys_equal_x_minus_j": linear["all_match"],
        "all_hilbert_polynomials_match_numerical_integer_rounding":
            polys["all_match"],
    }
    return {
        "class_numbers": class_nums,
        "linear_case": linear,
        "all_polys": polys,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nClass numbers (expected vs computed):")
    for row in s["class_numbers"]["rows"]:
        print(f"  D={row['D']:>5}: h = {row['h']} (expected {row['expected']})"
              f"  match={row['match']}")
    print("\nHilbert class polynomial verification (degree h(D)):")
    for row in s["all_polys"]["rows"]:
        print(f"  D={row['D']:>5}, h={row['class_number']}: match={row['match']}"
              f"  deg={row['degree']}")
