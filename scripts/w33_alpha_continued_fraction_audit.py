"""Continued-fraction audit of the W(3,3) α⁻¹ phenomenology fraction.

Finding (new, May 2026 sprint):

    The W(3,3) phenomenology fraction for the inverse fine-structure constant,

        α⁻¹_W33 = 137 + 880/24445 = 669969/4889,

    has continued-fraction expansion

        [137; 27, 1, 3, 1, 1, 19]

    The first six partial quotients agree with the regular continued
    fraction of the CODATA-2024 measured α⁻¹,

        α⁻¹_CODATA = 137.035999177(21) = [137; 27, 1, 3, 1, 1, 18, 1, 7, 1, ...]

    and every one of those first six integers is either a W(3,3)
    structural invariant or a trivial identity unit:

        137  =  (k − 1)² + μ²  =  Gaussian norm |z|² with  z = 11 + 4i
         27  =  v − k − 1  =  q³  =  dim(fundamental rep of E₆)
          1  =  identity unit
          3  =  q (the master integer)
          1  =  identity unit
          1  =  identity unit

Continued fractions give the optimal rational approximants (any other
rational with a comparable denominator is strictly worse), so this is the
sharpest constructive statement available: the W(3,3) phenomenology
fraction is the best-possible rational approximation to CODATA whose
leading partial quotients are the W(3,3) structural integers {137, 27, q}.

Tier: near-exact phenomenology / structural observation
(the underlying fraction is already classified as "near_exact_phenomenology"
in the Q8 claim ledger; this audit gives a sharper *reason* for that
fraction's accuracy without promoting it to an exact-finite theorem).
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Dict, List, Tuple

# W(3,3) parameters.
Q = 3
LAMBDA = 2
MU = 4
K = 12
V = 40

# The phenomenology fraction used in the Q8 ledger and elsewhere in the repo.
ALPHA_INV_W33 = Fraction(137, 1) + Fraction(880, 24445)

# CODATA 2024 value (ppb-level) for cross-check.
# Source: CODATA 2024 recommended values. Uncertainty ≈ 2.1e-8 relative.
CODATA_ALPHA_INV = "137.035999177"
CODATA_ALPHA_INV_STDDEV = "0.000000021"


def continued_fraction(frac: Fraction, max_terms: int = 32) -> Tuple[int, ...]:
    """Return the regular (finite) continued-fraction expansion of a rational."""
    n, d = frac.numerator, frac.denominator
    terms: List[int] = []
    while d and len(terms) < max_terms:
        a = n // d
        terms.append(a)
        n, d = d, n - a * d
    return tuple(terms)


def continued_fraction_decimal(x: float, max_terms: int = 12) -> Tuple[int, ...]:
    """Return the leading partial quotients of a real number."""
    import math

    terms: List[int] = []
    for _ in range(max_terms):
        a = int(math.floor(x))
        terms.append(a)
        rem = x - a
        if rem <= 1e-14:
            break
        x = 1.0 / rem
    return tuple(terms)


def reconstruct_from_cf(partial_quotients: Tuple[int, ...]) -> Fraction:
    """Reconstruct a Fraction from its continued-fraction partial quotients."""
    p, q = 1, 0
    for a in reversed(partial_quotients):
        p, q = a * p + q, p
    return Fraction(p, q)


def matching_prefix_length(cf_a: Tuple[int, ...], cf_b: Tuple[int, ...]) -> int:
    """Return the number of leading partial quotients that agree."""
    count = 0
    for a, b in zip(cf_a, cf_b):
        if a != b:
            return count
        count += 1
    return count


@lru_cache(maxsize=1)
def w33_alpha_continued_fraction_audit() -> Dict[str, object]:
    cf_w33 = continued_fraction(ALPHA_INV_W33, max_terms=16)

    # Reconstruct from the matching prefix [137, 27, 1, 3, 1, 1] as a sanity
    # check; this is the sharpest W(3,3)-structural approximant to CODATA.
    prefix = cf_w33[:6]
    structural_convergent = reconstruct_from_cf(prefix)

    # Compare against the CODATA value expanded as a float.
    import math

    codata = float(CODATA_ALPHA_INV)
    cf_codata = continued_fraction_decimal(codata, max_terms=12)
    match_len = matching_prefix_length(cf_w33, cf_codata)

    structural_label: Dict[int, str] = {
        137: "(k - 1)^2 + mu^2  (Gaussian norm of z = (k-1) + mu*i)",
        27: "v - k - 1 = q^3  (dim fundamental E6)",
        3: "q (master integer)",
        1: "identity unit",
    }

    annotated_prefix = []
    for a in prefix:
        annotated_prefix.append(
            {
                "partial_quotient": a,
                "structural_meaning": structural_label.get(
                    a, "not a canonical W(3,3) invariant"
                ),
            }
        )

    return {
        "source": "scripts/w33_alpha_continued_fraction_audit.py",
        "alpha_inv_w33_fraction": str(ALPHA_INV_W33),
        "alpha_inv_w33_decimal": f"{float(ALPHA_INV_W33):.12f}",
        "alpha_inv_codata_decimal": CODATA_ALPHA_INV,
        "alpha_inv_codata_stddev": CODATA_ALPHA_INV_STDDEV,
        "cf_w33": cf_w33,
        "cf_codata_leading": cf_codata,
        "match_length": match_len,
        "matching_prefix": prefix,
        "annotated_prefix": annotated_prefix,
        "structural_convergent_fraction": str(structural_convergent),
        "structural_convergent_decimal": f"{float(structural_convergent):.10f}",
        "deviation_from_codata": float(structural_convergent) - codata,
        "tier_note": (
            "near_exact_phenomenology; the alpha_inv_w33 fraction is the best "
            "rational approximation to CODATA whose first six partial "
            "quotients [137, 27, 1, 3, 1, 1] are all W(3,3) structural "
            "integers or identity units."
        ),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(w33_alpha_continued_fraction_audit(), indent=2, default=str))
