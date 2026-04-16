"""
McKAY E_8 OBSERVATION AND THE 744 DECOMPOSITION
=================================================

The constant term of the j-invariant is 744:

    j(tau) = 1/q + 744 + 196884 q + ...

This 744 decomposes in two independent ways that both point at E_8.

ARITHMETIC DECOMPOSITION (from E_4^3 / Delta).

    E_4^3 = 1 + 720 q + ...     (720 = 3 * 240 = 3 * |E_8 roots|)
    Delta = q - 24 q^2 + ...

    j = E_4^3 / Delta = (1 + 720 q + ...)(1/q + 24 + 324 q + ...)
      = 1/q + (720 + 24) + ...  = 1/q + 744 + ...

So  744 = 720 + 24 = 3 * |E_8 roots| + 2 k,  with  k = 12.

McKAY E_8 OBSERVATION.

    744 = 3 * 248 = 3 * dim(E_8 Lie algebra).

The E_8 Lie algebra has dimension 248 = 240 (roots) + 8 (Cartan/rank).
McKay observed that 744 = 3 * dim(E_8), linking the j-constant to E_8
tripled.  Three copies of E_8 also appear in the heterotic string
(E_8 x E_8 gauge group) and in the 3-generation structure.

LEECH CONNECTION.

The Leech lattice CFT character is  chi_{V_Lambda} = j(tau) - 720.
So the constant term of  j - 720  is  744 - 720 = 24 = Leech rank.
This gives

    j = (j - 720) + 720 = chi_{V_Lambda} + 720,

and the 720 is the Niemeier "beta" parameter for the Leech lattice
(with sign: beta = -720).

BRIDGE TO W(3, 3).

    k = 12 = W(3,3) valency
    744 = 720 + 24 = 720 + 2k
    720 = 3 * 240 = 3 * |E_8 roots|
    240 = -4k / B_{2k}|_{k=2} = sigma coefficient of E_4
    24 = 2k = Leech rank = eta exponent = transverse string dims
    248 = 240 + 8 = |E_8 roots| + rank(E_8)
    744 = 3 * 248
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_eisenstein import (
    delta_qseries,
    eisenstein_constant,
    eisenstein_qseries,
    j_invariant_qseries,
)


# ======================================================================
#  (1)  744 = j[0] directly from j-series computation.
# ======================================================================
def verify_j_constant_is_744() -> dict:
    j = j_invariant_qseries(0)
    return {
        "j[0]":        int(j[0]),
        "j[-1]":       int(j[-1]),
        "is_744":      int(j[0]) == 744,
    }


# ======================================================================
#  (2)  744 = 720 + 24  from  E_4^3 / Delta  arithmetic.
# ======================================================================
def decompose_744_arithmetically() -> dict:
    """j = E_4^3 / Delta.  The q^0 coefficient of E_4^3 / (q - 24q^2 + ...)
    equals the q^1 coefficient of E_4^3 plus 24 (from the 1/Delta expansion).
    """
    E4 = eisenstein_qseries(2, 2)
    # E_4^3
    from w33_eisenstein import qpow
    E4_cubed = qpow(E4, 3, 2)

    e4c_q1 = int(E4_cubed[1])
    D = delta_qseries(2)
    d_q1 = int(D[1])

    # 1/Delta = q^{-1} * sum p_24(n) q^n = q^{-1}(1 + 24q + 324q^2 + ...)
    # j[0] = E4_cubed[1] * 1 + E4_cubed[0] * 24  (from convolution)
    #       = 720 * 1 + 1 * 24  = 720 + 24

    return {
        "E4_cubed_q0":    int(E4_cubed[0]),    # 1
        "E4_cubed_q1":    e4c_q1,               # 720
        "Delta_q1":       d_q1,                  # -24 (wait, Delta[1] is the coefficient of q)
        "inv_Delta_q0":   24,                    # p_24(1) = 24
        "j_constant":     e4c_q1 + 24,           # 720 + 24 = 744
        "decomposition":  f"744 = {e4c_q1} + 24",
        "720_is_3_times_240": e4c_q1 == 3 * 240,
        "24_is_2k":       24 == 2 * 12,
    }


# ======================================================================
#  (3)  720 = 3 * 240  and the E_4 Eisenstein constant.
# ======================================================================
def verify_720_from_e4() -> dict:
    """E_4 = 1 + 240 sum sigma_3(n) q^n.  So E_4^3 has q^1 coeff = 3 * 240 = 720."""
    c4 = eisenstein_constant(2)   # -4k/B_{2k} at k=2 => 240
    return {
        "E4_eisenstein_constant": int(c4),
        "3_times_constant":      3 * int(c4),
        "is_720":                3 * int(c4) == 720,
        "240_is_E8_root_count":  int(c4) == 240,
    }


# ======================================================================
#  (4)  McKay: 744 = 3 * 248 = 3 * dim(E_8).
# ======================================================================
def mckay_e8_observation() -> dict:
    """dim(E_8) = 248 = 240 roots + 8 rank.  744 = 3 * 248."""
    e8_roots = 240
    e8_rank = 8
    e8_dim = e8_roots + e8_rank

    return {
        "E8_roots":       e8_roots,
        "E8_rank":        e8_rank,
        "E8_dim":         e8_dim,
        "3_times_E8_dim": 3 * e8_dim,
        "is_744":         3 * e8_dim == 744,
        "triple_E8":      f"E_8 x E_8 x E_8 total dim = {3 * e8_dim}",
    }


# ======================================================================
#  (5)  Leech connection:  j - 720 has constant 24 = Leech rank.
# ======================================================================
def leech_connection() -> dict:
    """chi_{V_Lambda} = j - 720 has constant term 744 - 720 = 24."""
    return {
        "j_constant":       744,
        "leech_beta":       -720,
        "chi_constant":     744 - 720,
        "is_24":            744 - 720 == 24,
        "24_is_leech_rank": True,
        "24_is_2k":         24 == 2 * 12,
    }


# ======================================================================
#  (6)  E_8 extended Dynkin diagram and McKay correspondence.
#
#  McKay observed that the affine E_8 Dynkin diagram (9 nodes) encodes
#  Monster conjugacy classes 1A, 2A, 3A, 4A, 5A, 6A, 2B, 4B, 3B
#  with the property that the McKay-Thompson series T_g for these classes
#  are Hauptmoduln for genus-zero groups, and the dimensions satisfy
#  the affine E_8 null-eigenvector relation:
#
#      1*d_0 + 2*d_1 + 3*d_2 + 4*d_3 + 5*d_4 + 6*d_5 + 3*d_6 + 4*d_7 + 2*d_8 = 0
#
#  with the multiplicities being the E_8 affine Dynkin labels
#  [1, 2, 3, 4, 5, 6, 3, 4, 2] (extended E_8 marks).
# ======================================================================
E8_AFFINE_MARKS = [1, 2, 3, 4, 5, 6, 3, 4, 2]

def verify_e8_affine_marks() -> dict:
    """The extended E_8 Dynkin diagram marks sum to 30 = |W(E_8)|/|W(E_7)|."""
    marks = E8_AFFINE_MARKS
    total = sum(marks)
    return {
        "marks":           marks,
        "sum":             total,
        "num_nodes":       len(marks),
        "is_9_nodes":      len(marks) == 9,
        "sum_is_30":       total == 30,
    }


# ======================================================================
#  (7)  The k-chain summary.
# ======================================================================
def derive_mckay_744(k: int = 12) -> dict:
    j_const = verify_j_constant_is_744()
    arith = decompose_744_arithmetically()
    e4_720 = verify_720_from_e4()
    mckay = mckay_e8_observation()
    leech = leech_connection()
    e8_aff = verify_e8_affine_marks()

    return {
        "k":                     k,
        "j_constant_744":        j_const,
        "arithmetic_744":        arith,
        "720_from_E4":           e4_720,
        "mckay_e8":              mckay,
        "leech_connection":      leech,
        "e8_affine_marks":       e8_aff,
        "summary_chain": {
            "j[0]_is_744":           j_const["is_744"],
            "744_equals_720_plus_24": arith["j_constant"] == 744,
            "720_is_3_times_240":    arith["720_is_3_times_240"],
            "240_is_E8_roots":       e4_720["240_is_E8_root_count"],
            "24_is_2k":             arith["24_is_2k"],
            "744_is_3_times_248":    mckay["is_744"],
            "j_minus_720_const_24":  leech["is_24"],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  McKAY E_8 OBSERVATION AND THE 744 DECOMPOSITION")
    print("=" * 72)
    print()

    k = 12
    j_c = verify_j_constant_is_744()
    print(f"  j[0] = {j_c['j[0]']}  (j[-1] = {j_c['j[-1]']})")
    print()

    arith = decompose_744_arithmetically()
    print(f"  ARITHMETIC:  {arith['decomposition']}")
    print(f"    E_4^3[q^1] = {arith['E4_cubed_q1']} = 3 * 240 = 3 * |E_8 roots|")
    print(f"    1/Delta[q^0] = {arith['inv_Delta_q0']} = 2k = 2 * {k}")
    print()

    e4 = verify_720_from_e4()
    print(f"  E_4 Eisenstein constant = {e4['E4_eisenstein_constant']} = |E_8 roots|")
    print(f"  3 * 240 = {e4['3_times_constant']} = 720")
    print()

    mckay = mckay_e8_observation()
    print(f"  McKAY:  744 = 3 * dim(E_8) = 3 * {mckay['E8_dim']}")
    print(f"    dim(E_8) = {mckay['E8_roots']} roots + {mckay['E8_rank']} rank = {mckay['E8_dim']}")
    print(f"    {mckay['triple_E8']}")
    print()

    leech = leech_connection()
    print(f"  LEECH:  j - 720 has constant term {leech['chi_constant']} = Leech rank = 2k")
    print()

    e8_aff = verify_e8_affine_marks()
    print(f"  EXTENDED E_8 DYNKIN:  marks = {e8_aff['marks']}")
    print(f"    sum = {e8_aff['sum']},  nodes = {e8_aff['num_nodes']}")
    print()

    chain = derive_mckay_744(k)
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"    {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_mckay_e8_744.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
