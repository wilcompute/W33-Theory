#!/usr/bin/env python3
"""BT595: Ihara nonbacktracking leakage derivation.

BT594 observed the arithmetic lock

    244/121 = 2*(1 + 1/11^2),

where 11 = k-1 is the nonbacktracking outdegree of a 12-regular W33 carrier.
BT595 packages this as a small derivation from the normalized even two-step
Hashimoto/Ihara transfer.

Boundary: this is a radial transfer derivation of the scalar leakage ratio, not
a full diagonalization of the 480x480 directed-edge Hashimoto operator.
"""
from fractions import Fraction
import json
from pathlib import Path

# W33 / project constants
q = 3
v = 40
k = 12
phi6 = 7
chi = 4
f5 = 5

# Hashimoto / Ihara scale for a k-regular carrier
p = k - 1                # nonbacktracking outdegree
rho = Fraction(1, p)     # nonbacktracking radius scale
rho2 = rho * rho

# Even two-step transfer: two directions times stay-or-two-step radial term.
even_transfer = 2 * (1 + rho2)
raw_leakage = Fraction(244, 121)
weighted_leakage = Fraction(976, 605)

# Equivalent numerator readings.
num_i = 2 * (p * p + 1)
num_ii = v * phi6 - chi * q * q
num_iii = 2 * (k * k - 2 * k + 2)  # since p=k-1

derivation = [
    f"p = k - 1 = {p}",
    f"rho = 1/p = {rho}",
    f"even_transfer = 2*(1+rho^2) = {even_transfer}",
    f"244 = 2*(p^2+1) = {num_i}",
    f"244 = v*Phi6 - chi*q^2 = {num_ii}",
    f"976/605 = (chi/F5)*(244/121) = {Fraction(chi, f5) * raw_leakage}",
]

checks = {
    "raw_equals_even_transfer": raw_leakage == even_transfer,
    "denominator_is_p_squared": raw_leakage.denominator == p * p,
    "numerator_formula_i": raw_leakage.numerator == num_i,
    "numerator_formula_ii": raw_leakage.numerator == num_ii,
    "numerator_formula_iii": raw_leakage.numerator == num_iii,
    "weighted_is_euler_pentagonal_modulation": weighted_leakage == Fraction(chi, f5) * raw_leakage,
}

result = {
    "bt": 595,
    "title": "Ihara nonbacktracking leakage derivation",
    "constants": {
        "q": q,
        "v": v,
        "k": k,
        "Phi6": phi6,
        "chi": chi,
        "F5": f5,
        "p_nonbacktracking": p,
        "rho": str(rho),
    },
    "derived_ratios": {
        "raw_cubic_leakage": str(raw_leakage),
        "even_two_step_ihara_transfer": str(even_transfer),
        "weighted_cubic_leakage": str(weighted_leakage),
        "weighted_modulation": "chi/F5",
    },
    "derivation": derivation,
    "interpretation": "The scalar raw cubic leakage ratio is the normalized even two-step nonbacktracking transfer at p=k-1=11. The multiplicity-weighted leakage is the same transfer multiplied by chi/F5.",
    "boundary": "This derives the scalar ratio; it does not yet diagonalize the full directed-edge Hashimoto operator.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT595_IHARA_NONBACKTRACKING_LEAKAGE_DERIVATION_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
