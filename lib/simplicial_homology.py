from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


Simplex = Tuple[int, ...]  # oriented simplex given by an ordered tuple of vertices


def faces(simplex: Simplex) -> List[Tuple[int, Simplex]]:
    """Return signed faces of a simplex.

    For simplex (v0,...,vk), the i-th face removes v_i with sign (-1)^i.
    """

    out: List[Tuple[int, Simplex]] = []
    for i in range(len(simplex)):
        face = simplex[:i] + simplex[i + 1 :]
        sign = -1 if (i % 2 == 1) else 1
        out.append((sign, face))
    return out


def boundary_matrix(
    k_simplices: Sequence[Simplex],
    km1_simplices: Sequence[Simplex],
    *,
    p: int,
) -> List[List[int]]:
    """Build the boundary matrix ∂_k over Z/pZ as dense rows.

    Rows index (k-1)-simplices, cols index k-simplices.
    Entry is the signed incidence (mod p).

    This stays reasonably small for W33 sizes (<= 240x160 etc).
    """

    idx = {s: i for i, s in enumerate(km1_simplices)}
    m = len(km1_simplices)
    n = len(k_simplices)
    M = [[0] * n for _ in range(m)]

    for j, s in enumerate(k_simplices):
        for sign, f in faces(s):
            i = idx.get(f)
            if i is None:
                continue
            M[i][j] = (M[i][j] + sign) % p

    return M


def rank_mod_p(M: List[List[int]], p: int) -> int:
    """Row-reduction rank over F_p.

    Mod-p Gauss elimination with partial pivoting.
    """

    if not M:
        return 0

    m = len(M)
    n = len(M[0]) if m else 0
    r = 0
    c = 0

    def inv_mod(a: int) -> int:
        return pow(a % p, p - 2, p)  # p prime

    while r < m and c < n:
        pivot = None
        for i in range(r, m):
            if M[i][c] % p != 0:
                pivot = i
                break
        if pivot is None:
            c += 1
            continue

        if pivot != r:
            M[r], M[pivot] = M[pivot], M[r]

        pv = M[r][c] % p
        inv_pv = inv_mod(pv)
        # normalize row
        rowr = M[r]
        for j in range(c, n):
            rowr[j] = (rowr[j] * inv_pv) % p

        # eliminate other rows
        for i in range(m):
            if i == r:
                continue
            factor = M[i][c] % p
            if factor == 0:
                continue
            rowi = M[i]
            for j in range(c, n):
                rowi[j] = (rowi[j] - factor * rowr[j]) % p

        r += 1
        c += 1

    return r


@dataclass(frozen=True)
class HomologySummary:
    primes: Tuple[int, ...]
    betti_by_prime: Dict[int, Dict[int, int]]  # prime -> {k: beta_k}
    betti_estimate: Dict[int, int]  # k -> beta_k (using max-rank across primes)
    euler_characteristic: int


def betti_numbers_via_primes(
    simplices_by_dim: Dict[int, List[Simplex]],
    *,
    primes: Tuple[int, ...] = (1000003, 1000033, 1000037),
) -> HomologySummary:
    """Compute Betti numbers using mod-p ranks (fast, robust).

    For almost all primes, rank over F_p equals rank over Q.
    We estimate Betti numbers by using the *maximum* observed rank across
    several large primes (which matches Q-rank with high probability).
    """

    max_dim = max(simplices_by_dim.keys())

    betti_by_prime: Dict[int, Dict[int, int]] = {}
    ranks_by_prime: Dict[int, Dict[int, int]] = {}

    for p in primes:
        ranks: Dict[int, int] = {}
        for k in range(1, max_dim + 1):
            Mk = boundary_matrix(simplices_by_dim[k], simplices_by_dim[k - 1], p=p)
            # copy because elimination is in-place
            rk = rank_mod_p([row[:] for row in Mk], p)
            ranks[k] = rk
        ranks_by_prime[p] = ranks

        betti: Dict[int, int] = {}
        for k in range(0, max_dim + 1):
            n_k = len(simplices_by_dim.get(k, []))
            r_k = ranks.get(k, 0)  # rank of ∂_k
            r_kp1 = ranks.get(k + 1, 0)  # rank of ∂_{k+1}
            betti[k] = n_k - r_k - r_kp1
        betti_by_prime[p] = betti

    # Estimate by maximizing ranks across primes (then recompute betti).
    rank_est: Dict[int, int] = {}
    for k in range(1, max_dim + 1):
        rank_est[k] = max(ranks_by_prime[p][k] for p in primes)

    betti_est: Dict[int, int] = {}
    for k in range(0, max_dim + 1):
        n_k = len(simplices_by_dim.get(k, []))
        r_k = rank_est.get(k, 0)
        r_kp1 = rank_est.get(k + 1, 0)
        betti_est[k] = n_k - r_k - r_kp1

    # Euler characteristic from simplex counts
    chi = 0
    for k, sk in simplices_by_dim.items():
        chi += ((-1) ** k) * len(sk)

    return HomologySummary(primes=primes, betti_by_prime=betti_by_prime, betti_estimate=betti_est, euler_characteristic=chi)
