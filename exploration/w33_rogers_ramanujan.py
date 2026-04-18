"""The Rogers-Ramanujan identities.

Two of the deepest q-series identities connecting partitions to eta
products via residues mod 5:

    G(q) = sum_{n>=0} q^{n^2} / (q; q)_n
         = prod_{n>=1} 1 / ((1 - q^{5n-4})(1 - q^{5n-1}))
         = generating function for partitions with parts ≡ ±1 (mod 5),
         = generating function for partitions with consecutive parts
           differing by ≥ 2.

    H(q) = sum_{n>=0} q^{n(n+1)} / (q; q)_n
         = prod_{n>=1} 1 / ((1 - q^{5n-3})(1 - q^{5n-2}))
         = generating function for partitions with parts ≡ ±2 (mod 5),
         = generating function for partitions with consecutive parts
           differing by ≥ 2 and smallest part ≥ 2.

Consequence:

    G(q) . H(q) = phi(q^5) / phi(q),   phi(q) = prod_{n>=1}(1 - q^n),

so G(q) H(q) is an eta-quotient (up to a power of q^{1/6}), closing the
ring: Layer 47 (partition / phi^{-1}) x Layer 48 (eta) x Layer 50
(modular forms) x this Layer.

The mod-5 structure reflects the first Ramanujan congruence
p(5n+4) ≡ 0 (mod 5) pinned in Layer 47.
"""

from __future__ import annotations

from typing import Any


# ----------------------------------------------------------------------
# q-series arithmetic (minimal local copies to avoid import chain).
# ----------------------------------------------------------------------
def _multiply_by_inverse_1_minus_qm(series: list[int], m: int, N: int) -> None:
    """In-place multiply series by 1/(1 - q^m), truncated to N terms."""
    for i in range(m, N):
        series[i] += series[i - m]


def _multiply_by_1_minus_qm(series: list[int], m: int, N: int) -> None:
    """In-place multiply series by (1 - q^m)."""
    for i in range(N - 1, m - 1, -1):
        series[i] -= series[i - m]


def _mul_series(a: list[int], b: list[int], N: int) -> list[int]:
    out = [0] * N
    for i in range(N):
        ai = a[i]
        if ai == 0:
            continue
        for j in range(N - i):
            out[i + j] += ai * b[j]
    return out


def euler_phi(N: int) -> list[int]:
    """phi(q) = prod_{n>=1} (1 - q^n), via pentagonal-number theorem."""
    out = [0] * N
    out[0] = 1
    k = 1
    while True:
        e1 = k * (3 * k - 1) // 2
        e2 = k * (3 * k + 1) // 2
        sign = (-1) ** k
        progress = False
        if e1 < N:
            out[e1] += sign
            progress = True
        if e2 < N:
            out[e2] += sign
            progress = True
        if not progress:
            break
        k += 1
    return out


def euler_phi_at_q5(N: int) -> list[int]:
    """phi(q^5) = prod_{n>=1}(1 - q^{5n})."""
    out = [0] * N
    out[0] = 1
    for m in range(5, N, 5):
        _multiply_by_1_minus_qm(out, m, N)
    return out


# ----------------------------------------------------------------------
# Rogers-Ramanujan sum (LHS) and product (RHS) for G and H.
# ----------------------------------------------------------------------
def rogers_ramanujan_G_sum(N: int) -> list[int]:
    """LHS: G(q) = sum_{n>=0} q^{n^2} / (q; q)_n, truncated to q^{N-1}."""
    result = [0] * N
    result[0] = 1  # n=0 term
    current = [0] * N
    current[0] = 1  # 1/(q; q)_0 = 1
    for n in range(1, N):
        _multiply_by_inverse_1_minus_qm(current, n, N)
        offset = n * n
        if offset >= N:
            break
        for i in range(N - offset):
            result[i + offset] += current[i]
    return result


def rogers_ramanujan_H_sum(N: int) -> list[int]:
    """LHS: H(q) = sum_{n>=0} q^{n(n+1)} / (q; q)_n."""
    result = [0] * N
    result[0] = 1  # n=0 term (exponent 0 * 1 = 0)
    current = [0] * N
    current[0] = 1
    for n in range(1, N):
        _multiply_by_inverse_1_minus_qm(current, n, N)
        offset = n * (n + 1)
        if offset >= N:
            break
        for i in range(N - offset):
            result[i + offset] += current[i]
    return result


def rogers_ramanujan_G_product(N: int) -> list[int]:
    """RHS: G(q) = 1 / prod_{m ≡ ±1 mod 5} (1 - q^m)."""
    out = [0] * N
    out[0] = 1
    for m in range(1, N):
        if m % 5 in (1, 4):
            _multiply_by_inverse_1_minus_qm(out, m, N)
    return out


def rogers_ramanujan_H_product(N: int) -> list[int]:
    """RHS: H(q) = 1 / prod_{m ≡ ±2 mod 5} (1 - q^m)."""
    out = [0] * N
    out[0] = 1
    for m in range(1, N):
        if m % 5 in (2, 3):
            _multiply_by_inverse_1_minus_qm(out, m, N)
    return out


# ----------------------------------------------------------------------
# Partition count interpretations.
# ----------------------------------------------------------------------
def _partitions_distinct_diff(n: int, min_part: int, min_diff: int = 2,
                               cache: dict[tuple[int, int], int] | None = None) -> int:
    """Number of partitions of n with smallest part >= min_part and
    consecutive parts differing by at least min_diff."""
    if cache is None:
        cache = {}
    if n == 0:
        return 1
    if n < 0 or n < min_part:
        return 0
    key = (n, min_part)
    if key in cache:
        return cache[key]
    total = 0
    # Smallest part k >= min_part, remaining n - k with next smallest >= k + min_diff.
    for k in range(min_part, n + 1):
        total += _partitions_distinct_diff(n - k, k + min_diff, min_diff, cache)
    cache[key] = total
    return total


def partitions_with_diff_at_least_2(n_max: int) -> list[int]:
    """Partition counts p_G(n): parts differing by >= 2, for n=0..n_max."""
    return [_partitions_distinct_diff(n, 1, 2, {}) for n in range(n_max + 1)]


def partitions_diff_2_smallest_2(n_max: int) -> list[int]:
    """Partition counts p_H(n): parts differing by >= 2 and smallest >= 2."""
    return [_partitions_distinct_diff(n, 2, 2, {}) for n in range(n_max + 1)]


def partitions_parts_pm1_mod5(n_max: int) -> list[int]:
    """Partition counts: partitions of n into parts ≡ ±1 (mod 5)."""
    out = [0] * (n_max + 1)
    out[0] = 1
    for m in range(1, n_max + 1):
        if m % 5 in (1, 4):
            for i in range(m, n_max + 1):
                out[i] += out[i - m]
    return out


def partitions_parts_pm2_mod5(n_max: int) -> list[int]:
    """Partition counts: partitions of n into parts ≡ ±2 (mod 5)."""
    out = [0] * (n_max + 1)
    out[0] = 1
    for m in range(1, n_max + 1):
        if m % 5 in (2, 3):
            for i in range(m, n_max + 1):
                out[i] += out[i - m]
    return out


# ----------------------------------------------------------------------
# Verifiers.
# ----------------------------------------------------------------------
def verify_G_identity(N: int = 40) -> dict[str, Any]:
    """G_sum == G_product as q-series."""
    lhs = rogers_ramanujan_G_sum(N)
    rhs = rogers_ramanujan_G_product(N)
    return {
        "all_match": lhs == rhs,
        "first_10_coeffs": lhs[:10],
        "N_checked": N,
    }


def verify_H_identity(N: int = 40) -> dict[str, Any]:
    """H_sum == H_product as q-series."""
    lhs = rogers_ramanujan_H_sum(N)
    rhs = rogers_ramanujan_H_product(N)
    return {
        "all_match": lhs == rhs,
        "first_10_coeffs": lhs[:10],
        "N_checked": N,
    }


def verify_partition_interpretation_G(n_max: int = 20) -> dict[str, Any]:
    """p_G(n) = partitions with parts ≡ ±1 mod 5 = G[n]."""
    diff = partitions_with_diff_at_least_2(n_max)
    mod5 = partitions_parts_pm1_mod5(n_max)
    G_coeffs = rogers_ramanujan_G_sum(n_max + 1)
    match_diff_mod5 = diff == mod5
    match_series = diff == G_coeffs
    return {
        "diff_geq_2_counts": diff,
        "parts_pm1_mod5_counts": mod5,
        "G_series_coeffs": G_coeffs,
        "diff_equals_mod5": match_diff_mod5,
        "counts_equal_series": match_series,
        "all_match": match_diff_mod5 and match_series,
    }


def verify_partition_interpretation_H(n_max: int = 20) -> dict[str, Any]:
    """p_H(n) = partitions with parts ≡ ±2 mod 5 = H[n]."""
    diff = partitions_diff_2_smallest_2(n_max)
    mod5 = partitions_parts_pm2_mod5(n_max)
    H_coeffs = rogers_ramanujan_H_sum(n_max + 1)
    return {
        "diff_geq_2_min_2_counts": diff,
        "parts_pm2_mod5_counts": mod5,
        "H_series_coeffs": H_coeffs,
        "diff_equals_mod5": diff == mod5,
        "counts_equal_series": diff == H_coeffs,
        "all_match": diff == mod5 == H_coeffs,
    }


def verify_GH_product_equals_eta_quotient(N: int = 30) -> dict[str, Any]:
    """G(q) . H(q) . phi(q) = phi(q^5) as integer q-series."""
    G = rogers_ramanujan_G_product(N)
    H = rogers_ramanujan_H_product(N)
    phi = euler_phi(N)
    phi5 = euler_phi_at_q5(N)
    GH = _mul_series(G, H, N)
    GH_phi = _mul_series(GH, phi, N)
    return {
        "all_match": GH_phi == phi5,
        "GH_phi_first_10": GH_phi[:10],
        "phi_q5_first_10": phi5[:10],
    }


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def derive_all() -> dict[str, Any]:
    g_id = verify_G_identity(N=40)
    h_id = verify_H_identity(N=40)
    g_part = verify_partition_interpretation_G(n_max=20)
    h_part = verify_partition_interpretation_H(n_max=20)
    gh_eta = verify_GH_product_equals_eta_quotient(N=30)
    chain = {
        "rogers_ramanujan_G_sum_equals_product": g_id["all_match"],
        "rogers_ramanujan_H_sum_equals_product": h_id["all_match"],
        "G_counts_partitions_diff_geq_2_equals_pm1_mod5": g_part["all_match"],
        "H_counts_partitions_diff_geq_2_min_2_equals_pm2_mod5": h_part["all_match"],
        "GH_times_phi_equals_phi_q5": gh_eta["all_match"],
    }
    return {
        "G_identity": g_id,
        "H_identity": h_id,
        "G_partition_interpretation": g_part,
        "H_partition_interpretation": h_part,
        "GH_eta_quotient": gh_eta,
        "summary_chain": chain,
    }


if __name__ == "__main__":
    s = derive_all()
    print("summary_chain:")
    for k, v in s["summary_chain"].items():
        print(f"  {k}: {v}")
    print("\nG(q) first 10 coefficients:")
    print(" ", s["G_identity"]["first_10_coeffs"])
    print("\nH(q) first 10 coefficients:")
    print(" ", s["H_identity"]["first_10_coeffs"])
    print("\nG x H x phi equals phi(q^5) first 10:")
    print(" ", s["GH_eta_quotient"]["phi_q5_first_10"])
