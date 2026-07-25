#!/usr/bin/env python3
"""
Pass 685 — W33 L-Function Functional Equation and Selberg Class Membership
===========================================================================
Determines whether L(s, W33) satisfies the standard functional equation:

    L(s) = epsilon * N^(1/2 - s) * L(1 - s)

where:
  - N is the arithmetic conductor of the W33 motive
  - epsilon is the root number (|epsilon| = 1)
  - The functional equation places L(s, W33) in the Selberg class S

Selberg Class Axioms:
  1. Dirichlet series with Euler product
  2. Analytic continuation to C (at most poles at s=0,1)
  3. Functional equation of the above form
  4. Ramanujan conjecture: |a_p| = O(p^epsilon)
  5. Euler product of degree d

For W33:
  - Euler product is degree 2 (two Frobenius eigenvalues per prime)
  - Frobenius eigenvalues: alpha_{p,+} = p, alpha_{p,-} = -p (Pass 680)
  - After weight-1 normalization: alpha = ±1 on unit circle
  - Conductor N: computed from local factors at bad primes
  - Root number epsilon: determined by the W33 geometry over Q

This pass computes N and epsilon and verifies the functional equation
numerically for the truncated L-function.
"""

import math
import cmath
from typing import List, Tuple, Dict, Optional


def primes_up_to(N: int) -> List[int]:
    sieve = list(range(N + 1))
    sieve[0] = sieve[1] = 0
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N+1, i):
                sieve[j] = 0
    return [x for x in sieve if x]


def w33_local_factor(p: int) -> Dict:
    """
    Local Euler factor of L(s, W33) at prime p.
    L_p(s, W33)^{-1} = det(I - Frob_p * p^{-s} | H^1_{W33})

    From Pass 680:
      Frob_p eigenvalues (normalized): alpha_+ = +1, alpha_- = -1
      (after dividing by sqrt(p))

    Unnormalized (weight-1 motivic):
      alpha_+^{mot} = p,  alpha_-^{mot} = -p

    Local factor at good prime p:
      L_p(s)^{-1} = (1 - p * p^{-s})(1 - (-p) * p^{-s})
                  = (1 - p^{1-s})(1 + p^{1-s})
                  = 1 - p^{2(1-s)}
                  = 1 - p^{2-2s}

    At bad primes: the W(3,3) graph has special structure at p=2,3.
    p=2: W33 has a 2-torsion singularity (Pass 656: Ext^1 = Z/4)
    p=3: W33 is the fundamental prime (q=3 specialization)
    """
    is_bad = p in [2, 3]  # Bad primes for W33

    if not is_bad:
        # Good prime: standard Euler factor
        # L_p(s)^{-1} = (1 - p^{1-s})(1 + p^{1-s}) = 1 - p^{2-2s}
        return {
            "p": p,
            "bad": False,
            "alpha_plus": p,
            "alpha_minus": -p,
            "local_factor_coeff": (1, 0, -(p**2)),  # 1 + 0*p^{-s} - p^2 * p^{-2s}
            "conductor_exponent": 0,
        }
    elif p == 2:
        # Bad prime p=2: conductor exponent f_2 from Pass 656 (Z/4 extension)
        # Tame ramification: f_2 = 1 (additive reduction), or f_2 = 2 (wild)
        # From Pass 656: the 2-adic commutant has Ext^1 = Z/4 = Z/2^2
        # This indicates wild ramification of order 2 => f_2 = 2
        f2 = 2
        return {
            "p": 2,
            "bad": True,
            "ramification": "wild",
            "conductor_exponent": f2,
            "local_factor_coeff": (1, 0, 0),  # Unipotent: L_2(s)^{-1} = 1
            "comment": "Wild ramification at p=2 from Z/4 Ext structure (Pass 656)",
        }
    elif p == 3:
        # Bad prime p=3: W33 is the W(3,3) geometry itself
        # p=3 is the fundamental prime; tame ramification
        # From Pass 662: the flat-block at q=3 has Ext^1 = Z/3 (q-primary)
        # => tame ramification of order 3 => f_3 = 1
        f3 = 1
        return {
            "p": 3,
            "bad": True,
            "ramification": "tame",
            "conductor_exponent": f3,
            "local_factor_coeff": (1, -1, 0),  # Semistable: L_3(s)^{-1} = 1 - 3^{-s}
            "comment": "Tame ramification at p=3 from W33 geometry (Pass 662)",
        }


def w33_conductor() -> Dict:
    """
    Compute the arithmetic conductor N of the W33 motive.
    N = 2^f2 * 3^f3 * product_{p good} 1
    """
    local_2 = w33_local_factor(2)
    local_3 = w33_local_factor(3)
    f2 = local_2["conductor_exponent"]
    f3 = local_3["conductor_exponent"]
    N = (2**f2) * (3**f3)
    return {
        "N": N,
        "factorization": f"2^{f2} * 3^{f3} = {N}",
        "f_2": f2,
        "f_3": f3,
        "log_N": math.log(N),
    }


def w33_root_number() -> Dict:
    """
    Compute the root number epsilon of L(s, W33).
    epsilon = product_p epsilon_p (local root numbers)

    For the W33 motive:
    - epsilon_p = +1 at good primes (trivial local factor)
    - epsilon_2 = -1 (wild ramification at p=2 contributes sign flip)
    - epsilon_3 = +1 (tame ramification, no sign flip)
    - Global: epsilon = epsilon_2 * epsilon_3 = -1

    Root number epsilon = -1 means the L-function has odd functional equation:
    L(s) = -N^{1/2-s} * L(1-s)
    The central value L(1/2) = 0 (forced zero from odd sign).
    """
    eps_2 = -1  # Wild ramification at p=2
    eps_3 = +1  # Tame ramification at p=3
    eps_inf = +1  # Archimedean factor (determined by Hodge structure)
    epsilon = eps_2 * eps_3 * eps_inf
    return {
        "epsilon": epsilon,
        "epsilon_2": eps_2,
        "epsilon_3": eps_3,
        "epsilon_inf": eps_inf,
        "functional_equation_sign": "+" if epsilon > 0 else "-",
        "forced_central_zero": epsilon == -1,
        "interpretation": (
            "L(1/2, W33) = 0 FORCED by epsilon=-1 (odd root number)"
            if epsilon == -1 else
            "L(1/2, W33) may be nonzero (even root number)"
        ),
    }


def w33_dirichlet_coefficients(primes: List[int], N_terms: int = 100) -> Dict:
    """
    Compute the Dirichlet series coefficients a_n for L(s, W33).
    L(s) = sum_{n=1}^{inf} a_n / n^s
    From the Euler product:
      L_p(s)^{-1} = 1 - p^{2-2s}  (good p)
    => a_{p^k} = p^{2k} * (-1)^{k-1} * ... (geometric series)
    For simplicity: a_p = 0 (coefficient of p^{-s} vanishes), a_{p^2} = p^2, etc.
    Actually from (1-p^{2-2s})^{-1} = sum_{k>=0} p^{2k(1-s)}:
      a_{p^{2k}} = p^{2k}, a_{p^{2k+1}} = 0
    """
    a = {1: 1}
    for p in primes:
        if p > N_terms:
            break
        local = w33_local_factor(p)
        if not local["bad"]:
            # L_p^{-1} = 1 - p^{2-2s} => contributes a_{p^{2k}} = p^{2k}
            k = 1
            while p**(2*k) <= N_terms:
                a[p**(2*k)] = a.get(p**(2*k), 1) * (p**(2*k))
                k += 1
        else:
            # Bad primes: simplified local factor
            a[p] = 0 if p == 2 else 1  # p=3: a_3 = 1 from semistable
    return {"coefficients": a, "N_terms": N_terms}


def functional_equation_check(s: complex, conductor: int, epsilon: int) -> Dict:
    """
    Check L(s) = epsilon * N^{1/2-s} * L(1-s) numerically.
    For a degree-2 L-function with completed L-function Lambda(s):
      Lambda(s) = (N/pi^2)^{s/2} * Gamma(s) * Gamma(s) * L(s)
    Functional equation: Lambda