"""Theta series of the E_8 and Leech lattices.

Closes the lattice side of the moonshine stack by pinning two identities
that connect Layer 50's Eisenstein / Delta / j-function data to the deep
root and kissing-number constants:

    (i)  theta_{E_8}(q) = E_4(q)
         coefficient of q^k = |{v in E_8 : (v, v) = 2k}|
         leading coefficients  1, 240, 2160, 6720, 17520, 30240, ...
         (we enumerate the E_8 integer and half-integer cosets directly
          up to q^4 and pin against E_4.)

    (ii) theta_{Lambda_{24}}(q) = E_4(q)^3 - 720 Delta(q)
         coefficient of q^k = |{v in Leech : (v, v) = 2k}|
         leading coefficients  1, 0, 196560, 16773120, 398034000, ...
         (Leech is even-unimodular of rank 24 with no norm-2 vectors;
          k(Leech) = 196560 is the kissing number in 24 dimensions.)

The kissing numbers k(E_8) = 240 and k(Lambda_{24}) = 196560 are the
known-optimal sphere-packing kissing numbers in 8 and 24 dimensions,
and both are built from W(3,3)'s spectral data via the Eisenstein chain:

    240 = coefficient of q in E_4, matches |roots(E_8)|,
         appears as 240 = 5 . 48 in the (3,5,6,12) Coxeter arithmetic.
    196560 = 16773120/85.3... = no simple factor form; emerges from
         E_4^3[q^2] - 720 tau(2) = 179280 + 17280.
"""

from __future__ import annotations

import itertools
from typing import Any, Iterator

from w33_eisenstein_delta_moonshine import (
    _mul_series,
    _pow_series,
    delta_from_eisenstein,
    eisenstein_E4,
)


# ----------------------------------------------------------------------
# Recursive integer / odd-integer vector enumeration.
# ----------------------------------------------------------------------
def _enum_integer(dim: int, max_sq: int) -> Iterator[tuple[tuple[int, ...], int]]:
    if dim == 0:
        yield (), 0
        return
    b = int(max_sq ** 0.5) + 1
    for v in range(-b, b + 1):
        vv = v * v
        if vv > max_sq:
            continue
        for rest, rest_sq in _enum_integer(dim - 1, max_sq - vv):
            yield (v,) + rest, vv + rest_sq


def _enum_odd(dim: int, max_sq: int) -> Iterator[tuple[tuple[int, ...], int]]:
    if dim == 0:
        yield (), 0
        return
    b = int(max_sq ** 0.5) + 1
    # smallest odd >= -b, largest odd <= b
    start = -b if b % 2 == 1 else -b - 1
    stop = b if b % 2 == 1 else b + 1
    for v in range(start, stop + 1, 2):
        vv = v * v
        if vv > max_sq:
            continue
        for rest, rest_sq in _enum_odd(dim - 1, max_sq - vv):
            yield (v,) + rest, vv + rest_sq


# ----------------------------------------------------------------------
# E_8 theta by direct enumeration.
# ----------------------------------------------------------------------
def e8_theta_coefficients(max_k: int = 4) -> list[int]:
    """theta_{E_8}(q) coefficient list up to q^{max_k}.

    E_8 = (Z^8, sum even) cup (Z^8 + (1/2,...,1/2) with sum even).
    Equivalently: integer class {v in Z^8 : sum v_i even} plus
                  half-integer class {u/2 : u in (2Z+1)^8, sum u in 4Z}.
    """
    out = [0] * (max_k + 1)
    out[0] = 1  # zero vector

    # Integer coset: v ∈ Z^8, sum v_i^2 = 2k (even), sum v_i even.
    for v, n2 in _enum_integer(8, 2 * max_k):
        if n2 == 0:
            continue
        if n2 > 2 * max_k:
            continue
        if n2 % 2 != 0:
            continue
        if sum(v) % 2 != 0:
            continue
        out[n2 // 2] += 1

    # Half-integer coset: u ∈ (2Z+1)^8, (u,u) = 8k, sum u ∈ 4Z.
    for u, n2 in _enum_odd(8, 8 * max_k):
        if n2 > 8 * max_k:
            continue
        if n2 % 8 != 0:  # should always hold: 8 odd squares ≡ 8 (mod 8)
            continue
        if sum(u) % 4 != 0:
            continue
        out[n2 // 8] += 1

    return out


# ----------------------------------------------------------------------
# Theta-vs-Eisenstein identity pin.
# ----------------------------------------------------------------------
E8_THETA_REFERENCE: list[int] = [1, 240, 2160, 6720, 17520, 30240]


def verify_E8_theta_equals_E4(max_k: int = 4) -> dict[str, Any]:
    """theta_{E_8}[k] = E_4[k] for all k <= max_k, via direct enumeration
    of E_8 vectors and polynomial evaluation of E_4."""
    theta = e8_theta_coefficients(max_k)
    E4 = eisenstein_E4(max_k + 1)
    rows: list[dict[str, Any]] = []
    all_match = True
    for k in range(max_k + 1):
        match = theta[k] == E4[k]
        rows.append({
            "k": k,
            "theta_E8": theta[k],
            "E4": E4[k],
            "match": match,
        })
        all_match = all_match and match
    return {
        "all_match": all_match,
        "rows": rows,
        "kissing_number_E8": theta[1],
        "kissing_number_E8_equals_240": theta[1] == 240,
    }


# ----------------------------------------------------------------------
# Leech lattice theta: theta_{Lambda_{24}} = E_4^3 - 720 Delta.
# ----------------------------------------------------------------------
LEECH_THETA_REFERENCE: dict[int, int] = {
    0: 1,
    1: 0,            # no norm-2 vectors
    2: 196560,       # kissing number
    3: 16773120,
    4: 398034000,
    5: 4629381120,
}


def leech_theta_coefficients(N: int = 7) -> list[int]:
    """theta_{Lambda_{24}}(q) = E_4^3 - 720 Delta, truncated to q^{N-1}."""
    E4 = eisenstein_E4(N)
    E4_cubed = _pow_series(E4, 3, N)
    D = delta_from_eisenstein(N)
    out = [E4_cubed[i] - 720 * D[i] for i in range(N)]
    return out


def verify_leech_theta_reference(N: int = 6) -> dict[str, Any]:
    theta = leech_theta_coefficients(N + 1)
    rows: list[dict[str, Any]] = []
    all_match = True
    for k in range(N + 1):
        if k not in LEECH_THETA_REFERENCE:
            continue
        expected = LEECH_THETA_REFERENCE[k]
        match = theta[k] == expected
        rows.append({
            "k": k,
            "theta_leech": theta[k],
            "reference": expected,
            "match": match,
        })
        all_match = all_match and match
    return {
        "all_match": all_match,
        "rows": rows,
        "kissing_number_Leech": theta[2],
        "kissing_number_Leech_equals_196560": theta[2] == 196560,
        "no_norm_2_vectors_in_Leech": theta[1] == 0,
    }


# ----------------------------------------------------------------------
# Cross-identity: theta_{Lambda} - theta_{E_8}^3 = constant . Delta.
# ----------------------------------------------------------------------
def verify_leech_E8_cube_delta_identity(N: int = 7) -> dict[str, Any]:
    """theta_{Lambda_{24}}(q) = theta_{E_8}(q)^3 - 720 . Delta(q) exactly.

    Since theta_{E_8} = E_4 and theta_{Lambda} = E_4^3 - 720 Delta, this
    is tautological; we verify it at the coefficient level for sanity."""
    E4 = eisenstein_E4(N)
    E4_cubed = _pow_series(E4, 3, N)
    D = delta_from_eisenstein(N)
    theta_leech = leech_theta_coefficients(N)
    rebuilt = [E4_cubed[i] - 720 * D[i] for i in range(N)]
    return {
        "all_match": rebuilt == theta_leech,
        "first_6_coefficients": theta_leech[:6],
        "E4_cubed_first_6": E4_cubed[:6],
        "minus_720_Delta_first_6": [-720 * D[i] for i in range(6)],
    }


# ----------------------------------------------------------------------
# Direct-count sanity pins on the E_8 first shell.
# ----------------------------------------------------------------------
def count_e8_norm_2_direct() -> int:
    """Enumerate E_8 minimal vectors (norm 2) in the two cosets and
    confirm the total is 240 = 112 + 128."""
    integer_count = 0
    # Integer coset norm 2: 2 nonzero coords of ±1.
    for pair in itertools.combinations(range(8), 2):
        for sx in (-1, 1):
            for sy in (-1, 1):
                v = [0] * 8
                v[pair[0]] = sx
                v[pair[1]] = sy
                assert sum(x * x for x in v) == 2
                assert sum(v) % 2 == 0
                integer_count += 1
    # Half-integer coset norm 2: all coords ±1/2 with sum in 2Z.
    half_count = 0
    for signs in itertools.product((-1, 1), repeat=8):
        s = sum(signs)  # sum of eight ±1's; sum of u_i values
        # v = u/2 where u ∈ {±1}^8; sum v = s/2, need integer ∈ 2Z.
        # s must be ≡ 0 (mod 4).
        if s % 4 == 0:
            half_count += 1
    return integer_count + half_count


def verify_e8_first_shell_decomposition() -> dict[str, Any]:
    """240 = 112 (integer coset ±1,±1,0,...,0) + 128 (half-integer coset)."""
    integer_count = 4 * 28  # C(8,2) = 28, 2^2 = 4 sign patterns
    half_count = 0
    for signs in itertools.product((-1, 1), repeat=8):
        if sum(signs) % 4 == 0:
            half_count += 1
    total = integer_count + half_count
    return {
        "integer_coset": integer_count,
        "half_integer_coset": half_count,
        "total": total,
        "matches_240": total == 240,
        "matches_direct_count": count_e8_norm_2_direct() == 240,
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    e8_check = verify_E8_theta_equals_E4(max_k=4)
    leech_check = verify_leech_theta_reference(N=5)
    identity = verify_leech_E8_cube_delta_identity(N=7)
    first_shell = verify_e8_first_shell_decomposition()
    chain = {
        "theta_E8_equals_E4_up_to_q4": e8_check["all_match"],
        "kissing_number_E8_is_240": e8_check["kissing_number_E8_equals_240"],
        "theta_leech_matches_reference_up_to_q5": leech_check["all_match"],
        "kissing_number_Leech_is_196560": leech_check[
            "kissing_number_Leech_equals_196560"
        ],
        "leech_has_no_norm_2_vectors": leech_check["no_norm_2_vectors_in_Leech"],
        "leech_equals_E8_cubed_minus_720_delta": identity["all_match"],
        "e8_first_shell_is_112_plus_128": first_shell["matches_240"],
    }
    return {
        "E8_theta_vs_E4": e8_check,
        "leech_theta_reference": leech_check,
        "leech_identity": identity,
        "e8_first_shell": first_shell,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nE_8 theta vs E_4 (direct enumeration):")
    for row in s["E8_theta_vs_E4"]["rows"]:
        print(f"  q^{row['k']}: theta={row['theta_E8']}, "
              f"E4={row['E4']}, match={row['match']}")
    print("\nLeech theta vs reference:")
    for row in s["leech_theta_reference"]["rows"]:
        print(f"  q^{row['k']}: theta={row['theta_leech']}, "
              f"ref={row['reference']}, match={row['match']}")
    print("\nE_8 first shell decomposition:")
    for k, v in s["e8_first_shell"].items():
        print(f"  {k}: {v}")
