#!/usr/bin/env python3
"""Pass 179: the sentinel/context Poisson pair with exact normalization.

Passes 167/175 opened the theta series of the sentinel lattice and its
dual.  This witness closes the pair analytically:

1. EXTENDED EXACT SHELLS.  Both theta series to scaled norm 40, exact
   integers from the weight enumerators (sentinel side) and the
   MacWilliams transform (context side).

2. THE EXACT POISSON NORMALIZATION.  Put

       A = {x in Z^40 : x mod 2 in S},
       B = {z in Z^40 : z mod 2 in S^perp}.

   Since [Z^40:A]=2^25 and [Z^40:B]=2^15, and since the Euclidean dual
   is A^vee=(1/2)B, Poisson summation gives, for every t>0,

     sum_{x in A} e^{-pi t |x|^2}
       = 2^{-25} t^{-20} sum_{z in B} e^{-pi |z|^2 / (4t)}.

   The finite shell evaluations at three t-values are retained only as
   numerical corroboration of this normalization.  They are not a proof
   of an infinite theta identity; the proof is the exact dual-lattice and
   covolume calculation above.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass167_sentinel_theta_macwilliams import (
    SENTINEL_ENUMERATOR,
    krawtchouk,
    poly_mul,
    poly_pow,
)

OUT = ROOT / "data" / "w33_pass179_poisson_modular_pair.json"

CAP = 80  # unscaled |x|^2 cap -> scaled norms to 40


def shells_from_enumerator(enumerator, cap):
    even_series = [0] * (cap + 1)
    even_series[0] = 1
    for m in range(2, 50, 2):
        if m * m <= cap:
            even_series[m * m] += 2
    odd_series = [0] * (cap + 1)
    for m in range(1, 50, 2):
        if m * m <= cap:
            odd_series[m * m] += 2
    shells = [0] * (cap // 2 + 1)
    for w, count in enumerator.items():
        if w > cap:
            continue
        odd_part = poly_pow(odd_series, w, cap) if w else [1] + [0] * cap
        even_part = poly_pow(even_series, 40 - w, cap)
        combined = poly_mul(odd_part, even_part, cap)
        for norm in range(0, cap + 1, 2):
            shells[norm // 2] += count * combined[norm]
    return shells


def macwilliams_transform(enumerator, dimension):
    """Return all 41 coefficients and exact-division diagnostics."""
    coefficients = []
    remainders = []
    denominator = 2**dimension
    for w in range(41):
        total = sum(count * krawtchouk(40, w, u) for u, count in enumerator.items())
        quotient, remainder = divmod(total, denominator)
        coefficients.append(quotient)
        remainders.append(remainder)
    return coefficients, remainders


def main():
    checks = {}

    # Exact full MacWilliams transform, including zero coefficients and
    # every integer division.  Transforming back checks the entire
    # enumerator rather than only its weight-four opening.
    dual_full, dual_remainders = macwilliams_transform(SENTINEL_ENUMERATOR, 15)
    dual_enum = {w: value for w, value in enumerate(dual_full) if value}
    primal_back_full, primal_back_remainders = macwilliams_transform(dual_enum, 25)
    expected_primal_full = [SENTINEL_ENUMERATOR.get(w, 0) for w in range(41)]
    checks["macwilliams_every_division_exact"] = not any(dual_remainders)
    checks["macwilliams_all_coefficients_nonnegative"] = all(
        value >= 0 for value in dual_full
    )
    checks["macwilliams_full_context_size_2_25"] = sum(dual_full) == 2**25
    checks["macwilliams_full_involution"] = (
        not any(primal_back_remainders) and primal_back_full == expected_primal_full
    )
    checks["macwilliams_opening"] = dual_full[:7] == [1, 0, 0, 0, 40, 0, 240]

    # Exact normalization certificate.  A has binary residue code S of
    # dimension 15, while B has residue code S^perp of dimension 25.
    # Thus their Euclidean indices are 2^25 and 2^15.  Scaling B by 1/2
    # multiplies covolume by 2^-40, so covol((1/2)B)=2^-25=covol(A)^-1.
    # Moreover 2e_i in A forces every element of A^vee to be z/2 with
    # z integral, and parity orthogonality is exactly z mod 2 in S^perp;
    # hence A^vee=(1/2)B, with no numerical approximation.
    index_a = 2 ** (40 - 15)
    index_b = 2 ** (40 - 25)
    dual_covolume = Fraction(index_b, 2**40)
    checks["sentinel_and_context_indices"] = (
        sum(SENTINEL_ENUMERATOR.values()) == 2**15
        and sum(dual_full) == 2**25
        and index_a == 2**25
        and index_b == 2**15
    )
    checks["euclidean_dual_covolume_reciprocal"] = dual_covolume == Fraction(1, index_a)
    checks["half_form_determinants_reciprocal"] = Fraction(
        index_a**2, 2**40
    ) == 2**10 and Fraction(index_b**2, 2**40) == Fraction(1, 2**10)

    sentinel_shells = shells_from_enumerator(SENTINEL_ENUMERATOR, CAP)
    context_shells = shells_from_enumerator(dual_enum, CAP)
    checks["sentinel_head"] = sentinel_shells[:5] == [1, 0, 80, 0, 14640]
    checks["context_head"] = context_shells[:4] == [1, 0, 720, 15360]
    checks["all_nonnegative"] = all(v >= 0 for v in sentinel_shells) and all(
        v >= 0 for v in context_shells
    )

    # Finite-window numerical corroboration only.  No finite list of
    # shells can certify the infinite identity; exactness comes from
    # A^vee=(1/2)B and covol(A)=2^25 above.
    poisson_corrob = {}
    all_close = True
    for t in (0.45, 0.5, 0.55):
        lhs = sum(
            n * math.exp(-2 * math.pi * t * k) for k, n in enumerate(sentinel_shells)
        )
        rhs = (
            2**-25
            * t**-20
            * sum(
                n * math.exp(-math.pi * k / (2 * t))
                for k, n in enumerate(context_shells)
            )
        )
        relative = abs(lhs - rhs) / lhs
        poisson_corrob[str(t)] = {
            "lhs": lhs,
            "rhs": rhs,
            "relative_error": relative,
        }
        if relative > 1e-12:
            all_close = False
    checks["finite_window_normalization_corrob"] = all_close

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass179.poisson_modular_pair.v1",
        "status": "PASS" if all_pass else "FAIL",
        "pair": {
            "A": "{x in Z^40 : x mod 2 in S}",
            "B": "{z in Z^40 : z mod 2 in S^perp}",
            "euclidean_dual": "A^vee = (1/2)B",
            "euclidean_indices": {"A": index_a, "B": index_b},
            "euclidean_covolumes": {
                "A": "2^25",
                "(1/2)B": "2^-25",
            },
            "half_form_determinants": {"A": "2^10", "B": "2^-10"},
            "identity": (
                "sum_{x in A} e^{-pi t |x|^2} = 2^-25 t^-20 "
                "sum_{z in B} e^{-pi |z|^2/(4t)}, for every t>0"
            ),
            "exact_basis": (
                "2e_i in A forces A^vee into (1/2)Z^40; reducing the "
                "pairing modulo 2 gives z mod 2 in S^perp, and the "
                "converse follows from the same parity pairing"
            ),
        },
        "macwilliams": {
            "context_weight_enumerator": {
                str(w): int(value) for w, value in enumerate(dual_full) if value
            },
            "all_41_divisions_exact": not any(dual_remainders),
            "transform_back_matches_all_41_coefficients": (
                primal_back_full == expected_primal_full
                and not any(primal_back_remainders)
            ),
        },
        "sentinel_shells_scaled_0_to_40": [int(v) for v in sentinel_shells],
        "context_shells_scaled_0_to_40": [int(v) for v in context_shells],
        "finite_shell_numerical_corrob": poisson_corrob,
        "reading": (
            "the infinite Poisson identity is exact because "
            "A^vee=(1/2)B and covol(A)=2^25; the three finite-shell "
            "evaluations only corroborate the factor 2^-25 t^-20 and "
            "the reciprocal argument 1/(4t)"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
