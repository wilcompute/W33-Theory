#!/usr/bin/env python3
"""
Part CCLVIII — Bernoulli Numbers, Ramanujan Congruence Prime 691, and
                 the W(3,3) closure of the small-prime tower.

The von Staudt-Clausen theorem
    den(B_{2n}) = prod_{p prime, (p-1) | 2n} p
gives the exact denominator of Bernoulli number B_{2n}.  At index 2n = K
(the W(3,3) regularity), the denominator is

    den(B_K) = den(B_12) = lam * q * (mu+1) * Phi_6 * Phi_3 = 2 * 3 * 5 * 7 * 13 = 2730,

which is exactly the product of the FIVE distinct W(3,3) primes
(documented in MONSTER_BERNOULLI_TRIANGLE.md).

We extend the closure in two directions:

  1. NUMERATOR.  The numerator of B_12 is -691, the famous Ramanujan
     congruence prime governing  tau(n) = sigma_11(n)  (mod 691).
     We exhibit two pure W(3,3) closed forms:

         691 = lam * v * lam^q     +  q * (Phi_3 + mu)
             = (lam^Phi_6) * (mu+1) +  q * (Phi_3 + mu)
             = 640                   +  51

  2. DENOMINATOR TOWER.  Every Bernoulli denominator den(B_{2n}) for
     2n in {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24} factors entirely
     into W(3,3) integer expressions.  Specifically the small-prime
     tower {2, 3, 5, 7, 11, 13, 17, 19, 23} has W(3,3) closed forms:

         2  = lam
         3  = q
         5  = mu + 1
         7  = Phi_6
        11  = k - 1
        13  = Phi_3
        17  = Phi_3 + mu
        19  = f - mu - 1
        23  = Phi_3 + Phi_4

The full prime tower up through 23 lies inside the W(3,3) integer ring.
Combined with the von Staudt-Clausen theorem, this means
EVERY Bernoulli denominator up to B_24 is a pure W(3,3) integer
expression, AND the famous Ramanujan congruence prime 691 in the B_12
numerator is also a W(3,3) closed form.

Key chain:
  1. den(B_2)  = lam * q                             (= 6)
  2. den(B_4)  = q * Phi_4                           (= 30 = h(E_8))
  3. den(B_6)  = lam * q * Phi_6                     (= 42)
  4. den(B_10) = lam * q * (k - 1)                   (= 66)
  5. den(B_12) = lam * q * (mu+1) * Phi_6 * Phi_3   (= 2730)
  6. den(B_16) = lam * q * (mu+1) * (Phi_3 + mu)    (= 510)
  7. den(B_18) = lam * q * Phi_6 * (f - mu - 1)     (= 798)
  8. den(B_20) = lam * q * (mu+1) * (k - 1)          (= 330)
  9. den(B_22) = lam * q * (Phi_3 + Phi_4)           (= 138)
 10. num(B_12) = -691 = -(lam^Phi_6 * (mu+1) + q * (Phi_3 + mu))
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# --- W(3,3) base constants ---------------------------------------------------
Q = 3
V = 40
K = 12
LAM = 2
MU = 4
F = 24                        # mult(r=+2)
G = 15                        # mult(s=-4)
EDGES = V * K // 2            # = 240
PHI3 = Q ** 2 + Q + 1         # = 13
PHI4 = Q ** 2 + 1             # = 10
PHI6 = Q ** 2 - Q + 1         # = 7
LAP_TOP = LAM ** MU           # = 16
LAP_MID = K - 2               # = 10 = Phi_4
M_LAM = LAM                    # eigen +2 (alias)
M_NEG = -MU                    # eigen -4 (alias)
AUT_ORDER = LAM ** PHI6 * Q ** MU * (MU + 1)  # = 51840


# --- Small-prime tower in W(3,3) closed forms --------------------------------
PRIME_FORMS = {
    2: LAM,
    3: Q,
    5: MU + 1,
    7: PHI6,
    11: K - 1,
    13: PHI3,
    17: PHI3 + MU,
    19: F - MU - 1,
    23: PHI3 + PHI4,
}


# --- Bernoulli denominators (von Staudt-Clausen) -----------------------------
def den_bernoulli(n_double: int) -> int:
    """den(B_{2n}) = prod_{p prime, (p-1) | 2n} p"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    d = 1
    for p in primes:
        if n_double % (p - 1) == 0:
            d *= p
    return d


# --- W(3,3) closed forms for the relevant denominators -----------------------
DEN_W33_FORMS = {
    2:  LAM * Q,                                              # 6
    4:  Q * PHI4,                                              # 30
    6:  LAM * Q * PHI6,                                        # 42
    8:  Q * PHI4,                                              # 30  (== B_4)
    10: LAM * Q * (K - 1),                                     # 66
    12: LAM * Q * (MU + 1) * PHI6 * PHI3,                      # 2730
    14: LAM * Q,                                               # 6   (== B_2)
    16: LAM * Q * (MU + 1) * (PHI3 + MU),                      # 510
    18: LAM * Q * PHI6 * (F - MU - 1),                          # 798
    20: LAM * Q * (MU + 1) * (K - 1),                          # 330
    22: LAM * Q * (PHI3 + PHI4),                                # 138
    24: LAM * Q * (MU + 1) * PHI6 * PHI3,                      # 2730  (==B_12)
}


# --- The Ramanujan 691 prime -------------------------------------------------
# 691 = lam*v*lam^q + q*(Phi_3+mu) = lam^Phi_6*(mu+1) + q*(Phi_3+mu)
RAM_691_FORM_A = LAM * V * LAM ** Q + Q * (PHI3 + MU)
RAM_691_FORM_B = LAM ** PHI6 * (MU + 1) + Q * (PHI3 + MU)
RAM_691_LARGER = LAM * V * LAM ** Q
RAM_691_SHIFT = Q * (PHI3 + MU)


# --- Checks ------------------------------------------------------------------
checks: list[tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


# Small-prime closed forms
for p, formula in PRIME_FORMS.items():
    _ck(f"prime {p} = W(3,3) form", p == formula)

# Bernoulli denominators -- the verifier matches W(3,3) form to actual den
for n2, w33_form in DEN_W33_FORMS.items():
    _ck(f"den(B_{n2}) = {w33_form}", den_bernoulli(n2) == w33_form)

# 2730 = primary cyclotomic product
_ck("den(B_12) = lam*q*(mu+1)*Phi_6*Phi_3 = 2730",
    LAM * Q * (MU + 1) * PHI6 * PHI3 == 2730)

# Ramanujan 691 closed forms
_ck("691 form A: lam*v*lam^q + q*(Phi_3+mu)",
    RAM_691_FORM_A == 691)
_ck("691 form B: lam^Phi_6*(mu+1) + q*(Phi_3+mu)",
    RAM_691_FORM_B == 691)
_ck("forms agree", RAM_691_FORM_A == RAM_691_FORM_B == 691)

# 691 prime structurally
_ck("691 is prime", all(691 % d != 0 for d in range(2, 27)))

# 691 = 640 + 51 decomposition
_ck("691 = 640 + 51", 640 + 51 == 691)
_ck("640 = lam^Phi_6 * (mu+1)", LAM ** PHI6 * (MU + 1) == 640)
_ck("640 = lam * v * lam^q", LAM * V * LAM ** Q == 640)
_ck("51 = q * (Phi_3 + mu)", Q * (PHI3 + MU) == 51)

# 30 cross-link (h(E_8))
_ck("h(E_8) = q*Phi_4 = den(B_4) = 30", Q * PHI4 == 30 and den_bernoulli(4) == 30)

# 5 = mu+1, the icosahedral 5-fold
_ck("Five distinct W(3,3) primes in den(B_12)",
    {LAM, Q, MU + 1, PHI6, PHI3} == {2, 3, 5, 7, 13})

# Number of W(3,3) prime factors in 2730 = mu+1 = 5
_ck("# W(3,3) primes in 2730 = mu+1", len({2, 3, 5, 7, 13}) == MU + 1)

# Ramanujan congruence: tau(n) ≡ sigma_11(n) mod 691
# Internal consistency: 11 = k - 1, weight 11 = k - 1 in Eisenstein E_12
_ck("Ramanujan weight: 11 = k - 1", 11 == K - 1)

# Sum of W(3,3) primes in tower up through 23
small_primes = list(PRIME_FORMS.keys())
sum_primes = sum(small_primes)  # 2+3+5+7+11+13+17+19+23 = 100
_ck("sum of 9 small W(3,3) primes = 100 = Phi_4^2",
    sum_primes == 100 and sum_primes == PHI4 ** 2)

# Number of small primes up through 23 = q^2 = 9 (cf McKay primes count)
_ck("# small W(3,3) primes <= 23 = q^2", len(small_primes) == Q ** 2)


Verified = all(v for _, v in checks)


def _build_results() -> dict[str, Any]:
    return {
        "part": "CCLVIII",
        "title": "Bernoulli, Ramanujan 691, and the W(3,3) Small-Prime Tower",
        "Verified": Verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "constants": {
            "Q": Q, "V": V, "K": K, "LAM": LAM, "MU": MU,
            "F": F, "G": G, "EDGES": EDGES,
            "PHI3": PHI3, "PHI4": PHI4, "PHI6": PHI6,
        },
        "small_prime_w33_forms": PRIME_FORMS,
        "bernoulli_denominators": {
            f"B_{n2}": {
                "denom": den_bernoulli(n2),
                "w33_form": form,
            } for n2, form in DEN_W33_FORMS.items()
        },
        "ramanujan_691": {
            "value": 691,
            "form_A": "lam*v*lam^q + q*(Phi_3+mu)",
            "form_B": "lam^Phi_6*(mu+1) + q*(Phi_3+mu)",
            "decomposition": {
                "large_part": RAM_691_LARGER,
                "shift": RAM_691_SHIFT,
                "sum": RAM_691_LARGER + RAM_691_SHIFT,
            },
        },
        "tower_summary": {
            "small_primes_up_to_23": small_primes,
            "count": len(small_primes),
            "count_eq_q_squared": len(small_primes) == Q ** 2,
            "sum": sum_primes,
            "sum_eq_phi4_squared": sum_primes == PHI4 ** 2,
        },
    }


if __name__ == "__main__":
    results = _build_results()
    out = Path(__file__).resolve().parents[1] / "PART_CCLVIII_bernoulli_ramanujan_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print(f"Wrote {out}")
