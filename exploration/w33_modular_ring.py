"""
THE MODULAR FORM RING:  M_*(SL(2,Z)) = C[E_4, E_6]
=====================================================

EVERY modular form for SL(2, Z) is a polynomial in E_4 and E_6.
This is why the entire tower — Eisenstein series, Delta, j, tau,
Leech, 196884, 744, 691 — is determined by just two objects.

DIMENSION FORMULA.

    dim M_k(SL(2, Z)) =
        floor(k/12) + 1    if  k  not-congruent  2  (mod 12),
        floor(k/12)          if  k  congruent  2  (mod 12).

    (For k even, k >= 0.   dim = 0 for k < 0 or k odd.)

Consequences:
    dim M_4  = 1    =>    M_4  = C * E_4
    dim M_6  = 1    =>    M_6  = C * E_6
    dim M_8  = 1    =>    E_8  = E_4^2            (forced!)
    dim M_10 = 1    =>    E_10 = E_4 * E_6        (forced!)
    dim M_12 = 2    =>    M_12 = C * E_4^3  +  C * E_6^2
    dim S_12 = 1    =>    Delta spans S_12         (unique cusp form!)
    dim M_14 = 1    =>    E_14 = E_4^2 * E_6      (forced!)

MONOMIAL BASIS.

The monomials E_4^a * E_6^b with 4a + 6b = k form a basis for M_k.
The number of such monomials equals dim M_k — a purely combinatorial fact.

WHY THIS CLOSES THE TOWER.

Since M_k = span{E_4^a * E_6^b : 4a + 6b = k}:
  - Delta = (E_4^3 - E_6^2) / 1728    (the unique weight-12 cusp form)
  - j = E_4^3 / Delta                   (ratio eliminates weight)
  - tau(n) = [q^n] Delta                (expansion of a polynomial in E_4, E_6)
  - All Eisenstein constants from B_2k  (which determine E_4 and E_6)

So the two generators E_4, E_6 — each with a single Eisenstein constant
(240 and -504 respectively) — encode ALL of:
  - Ramanujan tau, the 691-congruence, Hecke eigenvalues
  - The j-invariant, 744, 196884, Monster dimensions
  - E_8 theta function (= E_4), Leech theta, Niemeier family

BRIDGE TO W(3, 3).

    k = 12 = valency of W(3, 3)
    E_4 constant 240 = -4 * 2 / B_4 = 20 * k
    E_6 constant -504 = -4 * 3 / B_6 = -42 * k
    dim S_{2k} = dim S_12 = 1  =>  unique cusp form  =>  Delta  =>  j  =>  Monster
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from w33_eisenstein import (
    delta_qseries,
    eisenstein_constant,
    eisenstein_qseries,
    qmul,
    qpow,
)


# ======================================================================
#  Dimension formula for M_k(SL(2,Z)).
# ======================================================================
def dim_Mk(k: int) -> int:
    """Dimension of M_k(SL(2,Z)) for even k >= 0."""
    if k < 0 or k % 2 != 0:
        return 0
    if k % 12 == 2:
        return k // 12
    return k // 12 + 1


def dim_Sk(k: int) -> int:
    """Dimension of cusp forms S_k(SL(2,Z))."""
    if k < 12:
        return 0
    return dim_Mk(k) - 1


# ======================================================================
#  Monomial count: #{(a,b) : 4a + 6b = k, a,b >= 0}.
# ======================================================================
def monomial_count(k: int) -> int:
    """Number of pairs (a,b) with 4a + 6b = k."""
    if k < 0 or k % 2 != 0:
        return 0
    count = 0
    for b in range(k // 6 + 1):
        rem = k - 6 * b
        if rem >= 0 and rem % 4 == 0:
            count += 1
    return count


def list_monomials(k: int) -> list:
    """List all (a,b) with 4a + 6b = k."""
    monomials = []
    for b in range(k // 6 + 1):
        rem = k - 6 * b
        if rem >= 0 and rem % 4 == 0:
            a = rem // 4
            monomials.append((a, b))
    return monomials


# ======================================================================
#  Verify dim M_k = monomial count for all even k up to some limit.
# ======================================================================
def verify_dimension_equals_monomial_count(k_max: int = 60) -> list:
    results = []
    for k in range(0, k_max + 1, 2):
        d = dim_Mk(k)
        m = monomial_count(k)
        results.append({
            "k":               k,
            "dim_Mk":          d,
            "monomial_count":  m,
            "match":           d == m,
            "monomials":       list_monomials(k),
        })
    return results


# ======================================================================
#  Key structural identities forced by dim = 1.
# ======================================================================
def verify_E8_equals_E4_squared(order: int = 5) -> dict:
    """dim M_8 = 1 forces E_8 = E_4^2."""
    E4 = eisenstein_qseries(2, order)
    E8 = eisenstein_qseries(4, order)
    E4_sq = qpow(E4, 2, order)
    match = all(E4_sq[i] == E8[i] for i in range(order + 1))
    return {
        "dim_M8":      dim_Mk(8),
        "E4_squared":  [int(x) for x in E4_sq[:order + 1]],
        "E8_direct":   [int(x) for x in E8[:order + 1]],
        "match":       match,
        "forced_by":   "dim M_8 = 1",
    }


def verify_E10_equals_E4_E6(order: int = 5) -> dict:
    """dim M_10 = 1 forces E_10 = E_4 * E_6."""
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E10 = eisenstein_qseries(5, order)
    E4_E6 = qmul(E4, E6, order)
    match = all(E4_E6[i] == E10[i] for i in range(order + 1))
    return {
        "dim_M10":     dim_Mk(10),
        "E4_E6":       [int(x) for x in E4_E6[:order + 1]],
        "E10_direct":  [int(x) for x in E10[:order + 1]],
        "match":       match,
        "forced_by":   "dim M_10 = 1",
    }


def verify_E14_equals_E4sq_E6(order: int = 5) -> dict:
    """dim M_14 = 1 forces E_14 = E_4^2 * E_6."""
    E4 = eisenstein_qseries(2, order)
    E6 = eisenstein_qseries(3, order)
    E14 = eisenstein_qseries(7, order)
    E4_sq = qpow(E4, 2, order)
    product = qmul(E4_sq, E6, order)
    match = all(product[i] == E14[i] for i in range(order + 1))
    return {
        "dim_M14":     dim_Mk(14),
        "product":     [int(x) for x in product[:order + 1]],
        "E14_direct":  [int(x) for x in E14[:order + 1]],
        "match":       match,
        "forced_by":   "dim M_14 = 1",
    }


# ======================================================================
#  The unique cusp form: dim S_12 = 1 => Delta.
# ======================================================================
def verify_unique_cusp_form() -> dict:
    """dim S_12 = 1 means Delta is THE cusp form of weight 12."""
    return {
        "dim_M12":    dim_Mk(12),
        "dim_S12":    dim_Sk(12),
        "S12_unique": dim_Sk(12) == 1,
        "monomials_weight_12": list_monomials(12),
        "basis":      "E_4^3, E_6^2",
        "cusp_form":  "Delta = (E_4^3 - E_6^2) / 1728",
    }


# ======================================================================
#  Eisenstein constants determine everything.
# ======================================================================
def eisenstein_constants_from_k(k: int = 12) -> dict:
    """Show that E_4 and E_6 constants encode k."""
    c4 = eisenstein_constant(2)   # 240
    c6 = eisenstein_constant(3)   # -504
    return {
        "k":          k,
        "c_E4":       int(c4),
        "c_E6":       int(c6),
        "c_E4 / k":   Fraction(int(c4), k),
        "c_E6 / k":   Fraction(int(c6), k),
        "c_E4 = 20k": int(c4) == 20 * k,
        "c_E6 = -42k": int(c6) == -42 * k,
    }


# ======================================================================
#  Driver.
# ======================================================================
def derive_modular_ring(k: int = 12) -> dict:
    dims = verify_dimension_equals_monomial_count(60)
    e8_id = verify_E8_equals_E4_squared()
    e10_id = verify_E10_equals_E4_E6()
    e14_id = verify_E14_equals_E4sq_E6()
    cusp = verify_unique_cusp_form()
    eis_consts = eisenstein_constants_from_k(k)

    return {
        "dimension_table":   dims,
        "all_dims_match":    all(d["match"] for d in dims),
        "E8_equals_E4_sq":   e8_id,
        "E10_equals_E4_E6":  e10_id,
        "E14_equals_E4sq_E6": e14_id,
        "unique_cusp_form":  cusp,
        "eisenstein_constants": eis_consts,
        "summary_chain": {
            "dim_Mk_equals_monomial_count": all(d["match"] for d in dims),
            "E8_forced_by_dim_1":           e8_id["match"],
            "E10_forced_by_dim_1":          e10_id["match"],
            "E14_forced_by_dim_1":          e14_id["match"],
            "S12_unique_cusp_form":         cusp["S12_unique"],
            "c_E4_is_20k":                  eis_consts["c_E4 = 20k"],
            "c_E6_is_minus_42k":            eis_consts["c_E6 = -42k"],
        },
    }


def main() -> None:
    print("=" * 72)
    print("  MODULAR FORM RING:  M_*(SL(2,Z)) = C[E_4, E_6]")
    print("=" * 72)
    print()

    print("  DIMENSION TABLE  (dim M_k = monomial count):")
    for d in verify_dimension_equals_monomial_count(30):
        monos = ", ".join(f"E4^{a}*E6^{b}" for a, b in d["monomials"])
        print(f"    k={d['k']:>2d}:  dim={d['dim_Mk']}  monomials={d['monomial_count']}"
              f"  [{monos}]  match={d['match']}")
    print()

    print("  FORCED IDENTITIES (dim = 1):")
    e8 = verify_E8_equals_E4_squared()
    print(f"    E_8 = E_4^2:  match={e8['match']}  (dim M_8 = {e8['dim_M8']})")
    e10 = verify_E10_equals_E4_E6()
    print(f"    E_10 = E_4 * E_6:  match={e10['match']}  (dim M_10 = {e10['dim_M10']})")
    e14 = verify_E14_equals_E4sq_E6()
    print(f"    E_14 = E_4^2 * E_6:  match={e14['match']}  (dim M_14 = {e14['dim_M14']})")
    print()

    cusp = verify_unique_cusp_form()
    print(f"  UNIQUE CUSP FORM:  dim S_12 = {cusp['dim_S12']}")
    print(f"    {cusp['cusp_form']}")
    print()

    k = 12
    ec = eisenstein_constants_from_k(k)
    print(f"  EISENSTEIN CONSTANTS ENCODE k = {k}:")
    print(f"    c(E_4) = {ec['c_E4']} = 20 * {k}:  {ec['c_E4 = 20k']}")
    print(f"    c(E_6) = {ec['c_E6']} = -42 * {k}:  {ec['c_E6 = -42k']}")
    print()

    chain = derive_modular_ring(k)
    print("  SUMMARY CHAIN:")
    for key, val in chain["summary_chain"].items():
        print(f"    {key}: {val}")
    print()

    out = Path(__file__).resolve().parent.parent / "data" / "w33_modular_ring.json"
    out.write_text(json.dumps(chain, indent=2, default=str))
    print(f"  wrote {out}")


if __name__ == "__main__":
    main()
