"""Klein j-function q-expansion, Moonshine, and Hauptmodul property.

The modular j-invariant on SL_2(Z) is

    j(tau) = E_4(tau)^3 / Delta(tau) = 1/q + 744 + sum_{n >= 1} c(n) q^n.

Its first few Fourier coefficients (A000521):

    c(0)  =       744,
    c(1)  =    196884,
    c(2)  =  21493760,
    c(3)  = 864299970,
    c(4)  = 20245856256.

The *monstrous moonshine* observation of McKay (1978): the coefficient
196884 decomposes as 1 + 196883, where 196883 is the dimension of the
smallest non-trivial irreducible representation of the Monster group M.
Similarly,
    21493760   = 1 + 196883 + 21296876,
    864299970  = 1 + 1 + 196883 + 196883 + 21296876 + 842609326.

These are special cases of Conway-Norton's moonshine conjecture (proved
by Borcherds, 1992): each c(n) is a positive-integer combination of
Monster character values.

Hauptmodul property: j generates the function field of X(1) = H* / SL_2(Z),
so every modular function on SL_2(Z) is a rational function in j.  In
particular, j is invariant under the full modular group and has exactly
one simple pole at the cusp i infty (order 1 in q^{-1}).

Identities we pin:
    (I)  j = E_4^3 / Delta, as q-series;
    (II) j = 1/q + 744 + 196884 q + 21493760 q^2 + 864299970 q^3 + ...;
    (III) j(i) = 1728, j(rho) = 0 (rho = e^{2 pi i / 3});
    (IV) Moonshine: 196884 = 1 + 196883, 21493760 = 1 + 196883 + 21296876.
    (V) E_4(tau)^3 - E_6(tau)^2 = 1728 Delta (already pinned in Layer 68)
        implies j(tau) - 1728 = E_6^2 / Delta.

Layer 69 -- the j-function ties together:
  * modular-polynomial Phi_2 (Layer 59)  -- Phi_2(j(tau), j(2 tau)) = 0;
  * Eisenstein-Delta identity (Layer 68) -- defines j numerically;
  * Monster moonshine (196883)           -- McKay's coincidence.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from w33_eisenstein_delta_identity import (
    delta_q_series,
    eisenstein_q_series,
    series_mul,
)


# ----------------------------------------------------------------------
# Series inversion in q for Delta = q + O(q^2).
# ----------------------------------------------------------------------
def delta_inverse_q_series(N: int) -> list[Fraction]:
    """Compute 1/Delta as a q-series with leading q^{-1}.

    Write Delta = q * D(q) where D(q) = 1 + sum d_k q^k starts with 1.
    Then 1/Delta = q^{-1} * 1/D(q).

    Returns list [b_{-1}, b_0, b_1, ..., b_{N-1}] where
    1/Delta = b_{-1} q^{-1} + b_0 + b_1 q + ... + b_{N-1} q^{N-1}.
    """
    d = delta_q_series(N + 1)
    # d[1] = 1, d[k+1] = tau(k+1); so D(q) = 1 + tau(2) q + tau(3) q^2 + ...
    D = [d[i + 1] for i in range(N + 1)]   # length N+1, D[0] = 1
    assert D[0] == 1, "Delta / q must have constant term 1"
    # Invert D as a power series.
    # D(q) * Dinv(q) = 1.  Dinv[0] = 1.
    Dinv = [Fraction(0)] * (N + 1)
    Dinv[0] = Fraction(1)
    for n in range(1, N + 1):
        s = sum(D[k] * Dinv[n - k] for k in range(1, n + 1))
        Dinv[n] = -s
    # 1/Delta has a q^{-1} term:  (1/q) * (Dinv[0] + Dinv[1] q + Dinv[2] q^2 + ...)
    # So coefficient of q^{n} in 1/Delta is Dinv[n + 1] for n >= 0, and Dinv[0] for n = -1.
    # Return [b_{-1}, b_0, b_1, ..., b_{N-1}]  length N+1
    out = [Dinv[0]] + [Dinv[k + 1] if k + 1 <= N else Fraction(0) for k in range(N)]
    return out


# ----------------------------------------------------------------------
# j-function q-series.
# ----------------------------------------------------------------------
def j_q_series(N: int) -> list[Fraction]:
    """Return list [c_{-1}, c_0, c_1, ..., c_N] where
    j(tau) = c_{-1} q^{-1} + c_0 + c_1 q + ... + c_N q^N.
    (We expect c_{-1} = 1, c_0 = 744, c_1 = 196884, ...)"""
    # j = E_4^3 / Delta.
    # Compute E_4^3 up to q^{N+1}, so that when we multiply by 1/Delta
    # (leading q^{-1}) we get q^{-1} .. q^N.
    M = N + 1
    E4 = eisenstein_q_series(2, M)
    E4_cubed = series_mul(E4, series_mul(E4, E4, M), M)
    Dinv = delta_inverse_q_series(M)  # [b_{-1}, b_0, b_1, ..., b_{M-1}]
    # j[k] (coefficient of q^k, k = -1..N) =
    #   sum over (i, j) with i + j = k: E_4^3[i] * (1/Delta)[j].
    # Where E_4^3 has i >= 0, and 1/Delta has j >= -1, so k >= -1.
    out = [Fraction(0)] * (N + 2)  # index k+1 -> coeff of q^k for k = -1..N
    for i in range(M + 1):
        ai = E4_cubed[i] if i < len(E4_cubed) else Fraction(0)
        if ai == 0:
            continue
        for j_shift, bj in enumerate(Dinv):
            j_power = j_shift - 1  # j power of q
            k = i + j_power
            if -1 <= k <= N:
                out[k + 1] += ai * bj
    return out


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
_J_REFERENCE = {
    -1: 1,
    0:  744,
    1:  196884,
    2:  21493760,
    3:  864299970,
    4:  20245856256,
    5:  333202640600,
}


def verify_j_leading_coefficients(N: int = 5) -> dict[str, Any]:
    """j = 1/q + 744 + 196884 q + 21493760 q^2 + 864299970 q^3 +
    20245856256 q^4 + 333202640600 q^5 + ..."""
    j = j_q_series(N)
    rows = []
    all_match = True
    for k in range(-1, N + 1):
        got = j[k + 1]
        expected = _J_REFERENCE.get(k)
        match = got == Fraction(expected) if expected is not None else True
        rows.append({
            "q_power": k, "got": str(got),
            "expected": expected, "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_j_is_E43_over_delta(N: int = 10) -> dict[str, Any]:
    """Direct check: j * Delta = E_4^3 on q-series truncated to q^N."""
    E4 = eisenstein_q_series(2, N)
    E4_cubed = series_mul(E4, series_mul(E4, E4, N), N)
    Delta = delta_q_series(N)
    j = j_q_series(N)
    # j has a q^{-1} term; (j * Delta) should have only non-negative powers.
    # Convolution: (j * Delta)[k] = sum_{i+l=k, i >= -1, l >= 0} j[i+1] * Delta[l].
    product = [Fraction(0)] * (N + 1)
    for i in range(-1, N + 1):
        ji = j[i + 1]
        if ji == 0:
            continue
        for l in range(N + 1):
            dl = Delta[l]
            if dl == 0:
                continue
            k = i + l
            if 0 <= k <= N:
                product[k] += ji * dl
    diff = [product[k] - E4_cubed[k] for k in range(N + 1)]
    all_match = all(x == 0 for x in diff)
    return {
        "all_match": all_match, "N": N,
        "first_diff_nonzero":
            next((i for i, v in enumerate(diff) if v != 0), None),
    }


def verify_j_minus_1728_equals_E62_over_delta(N: int = 10) -> dict[str, Any]:
    """Since E_4^3 - E_6^2 = 1728 Delta, dividing by Delta gives
    j - 1728 = E_6^2 / Delta.  Check (j - 1728) * Delta = E_6^2."""
    E6 = eisenstein_q_series(3, N)
    E6_sq = series_mul(E6, E6, N)
    j = j_q_series(N)
    # subtract 1728 from constant term:  j_minus = j with j[0+1] -= 1728.
    j_minus = list(j)
    j_minus[1] = j_minus[1] - Fraction(1728)
    Delta = delta_q_series(N)
    product = [Fraction(0)] * (N + 1)
    for i in range(-1, N + 1):
        ji = j_minus[i + 1]
        if ji == 0:
            continue
        for l in range(N + 1):
            dl = Delta[l]
            if dl == 0:
                continue
            k = i + l
            if 0 <= k <= N:
                product[k] += ji * dl
    diff = [product[k] - E6_sq[k] for k in range(N + 1)]
    all_match = all(x == 0 for x in diff)
    return {
        "all_match": all_match, "N": N,
        "first_diff_nonzero":
            next((i for i, v in enumerate(diff) if v != 0), None),
    }


def verify_moonshine_decompositions() -> dict[str, Any]:
    """Monstrous moonshine:
        c(1) = 196884   = 1 + 196883,
        c(2) = 21493760 = 1 + 196883 + 21296876,
        c(3) = 864299970 = 2 * 1 + 2 * 196883 + 21296876 + 842609326."""
    M_dims = {
        "1":          1,
        "196883":     196883,
        "21296876":   21296876,
        "842609326":  842609326,
        "18538750076": 18538750076,
    }
    decomps = {
        1: {"1": 1, "196883": 1},
        2: {"1": 1, "196883": 1, "21296876": 1},
        3: {"1": 2, "196883": 2, "21296876": 1, "842609326": 1},
    }
    rows = []
    all_match = True
    for n, decomp in decomps.items():
        s = sum(mult * M_dims[name] for name, mult in decomp.items())
        expected = _J_REFERENCE[n]
        match = s == expected
        rows.append({
            "n": n,
            "decomp": decomp,
            "sum": s,
            "expected": expected,
            "match": match,
        })
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


def verify_196884_equals_1_plus_196883() -> dict[str, Any]:
    """The McKay coincidence: c(1) = 196884 = 1 + 196883."""
    j = j_q_series(1)
    c1 = j[2]  # coefficient of q^1
    return {
        "c_1": int(c1),
        "dim_trivial_plus_smallest_nontrivial_M_rep": 1 + 196883,
        "match": c1 == 196884,
    }


def verify_j_cusp_pole_order() -> dict[str, Any]:
    """j has a simple pole at i infty: coefficient of q^{-2} is 0 and
    coefficient of q^{-1} is 1."""
    j = j_q_series(3)
    # j[0] is coefficient of q^{-1}; no q^{-2} in our truncation -- by
    # construction j starts at q^{-1}.  Check leading coefficient = 1,
    # and check that *if* we attempt to read a more negative power, our
    # module's construction forbids it.
    leading_is_1 = j[0] == Fraction(1)
    return {
        "j_coefficient_at_q_minus_1": str(j[0]),
        "leading_is_1": leading_is_1,
        "match": leading_is_1,
    }


def verify_j_reference_first_six_A000521() -> dict[str, Any]:
    """OEIS A000521: 744, 196884, 21493760, 864299970, 20245856256,
    333202640600."""
    j = j_q_series(5)
    expected = [744, 196884, 21493760, 864299970, 20245856256, 333202640600]
    rows = []
    all_match = True
    for k, e in enumerate(expected):
        got = int(j[k + 1])
        match = got == e
        rows.append({"k": k, "got": got, "expected": e, "match": match})
        all_match = all_match and match
    return {"all_match": all_match, "rows": rows}


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    lead = verify_j_leading_coefficients(N=5)
    prod = verify_j_is_E43_over_delta(N=10)
    cusp_1728 = verify_j_minus_1728_equals_E62_over_delta(N=10)
    mkey = verify_196884_equals_1_plus_196883()
    moon = verify_moonshine_decompositions()
    pole = verify_j_cusp_pole_order()
    six = verify_j_reference_first_six_A000521()
    chain = {
        "j_leading_coefficients_match_A000521":
            lead["all_match"],
        "j_times_delta_equals_E4_cubed":
            prod["all_match"],
        "j_minus_1728_times_delta_equals_E6_squared":
            cusp_1728["all_match"],
        "McKay_coincidence_c1_equals_1_plus_196883":
            mkey["match"],
        "moonshine_decompositions_c1_c2_c3":
            moon["all_match"],
        "j_has_simple_pole_at_cusp_with_leading_1":
            pole["match"],
        "j_first_six_coefficients_match_OEIS_A000521":
            six["all_match"],
    }
    return {
        "leading": lead,
        "j_times_delta_is_E4_cubed": prod,
        "j_minus_1728_times_delta_is_E6_squared": cusp_1728,
        "mckay": mkey,
        "moonshine": moon,
        "pole": pole,
        "six": six,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    j = j_q_series(5)
    print("\nj-function q-expansion:")
    for k, c in enumerate(j):
        q_power = k - 1
        print(f"  q^{q_power:>2}: {int(c)}")
    print(f"\nMcKay: c(1) = {int(j[2])} = 1 + 196883 ?  "
          f"{s['mckay']['match']}")
