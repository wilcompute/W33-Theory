#!/usr/bin/env python3
"""Exact cryptographic entropy of the W33 support-only observer.

Pass 2836 computed Shannon information erased by the support map
    supp : F_q^4 -> {0,1}^4.
This companion computes the classical adversarial guessing probability,
conditional min-entropy, and averaged collision probability exactly.

For a support mask of Hamming weight k there are (q-1)^k equiprobable
preimages. There are C(4,k) such masks. Consequently every one of the
16 masks contributes exactly 1/q^4 to both the optimal classical guessing
probability and the averaged collision probability:

    P_guess(X | supp X) = 16/q^4,
    H_min(X | supp X) = 4 log2(q/2).

At q=3 this is log2(81/16) ~= 2.33985 bits.

This is a classical side-information statement. It is NOT a lower bound on
H_min(X | supp(X), E) for an adversary holding arbitrary quantum side
information E; if E contains a perfect copy/encoding of X that entropy can
fall to zero.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_support_min_entropy.json"


def exact_row(q: int) -> dict:
    if not isinstance(q, int) or q < 2:
        raise ValueError("q must be an integer >= 2")
    total = q**4

    mask_rows = []
    shannon_cond = 0.0
    p_guess = Fraction(0, 1)
    p_collision = Fraction(0, 1)
    for k in range(5):
        masks = comb(4, k)
        fibre = (q - 1) ** k
        probability_per_mask = Fraction(fibre, total)
        best_guess_given_mask = Fraction(1, fibre)
        collision_given_mask = Fraction(1, fibre)
        p_guess += masks * probability_per_mask * best_guess_given_mask
        p_collision += masks * probability_per_mask * collision_given_mask
        if fibre > 1:
            shannon_cond += masks * float(probability_per_mask) * math.log2(fibre)
        mask_rows.append({
            "weight": k,
            "masks": masks,
            "fibre_size": fibre,
            "probability_per_mask": str(probability_per_mask),
            "best_guess_given_mask": str(best_guess_given_mask),
        })

    closed = Fraction(16, total)
    assert p_guess == closed
    assert p_collision == closed

    hmin = -math.log2(float(p_guess))
    h2_avg = -math.log2(float(p_collision))
    shannon_closed = 4 * (q - 1) * math.log2(q - 1) / q if q > 2 else 0.0
    assert abs(shannon_cond - shannon_closed) < 1e-12
    assert abs(hmin - 4 * math.log2(q / 2)) < 1e-12

    return {
        "q": q,
        "state_count": total,
        "support_masks": 16,
        "mask_fibres": mask_rows,
        "optimal_classical_guessing_probability": str(p_guess),
        "optimal_classical_guessing_probability_float": float(p_guess),
        "conditional_min_entropy_bits": hmin,
        "averaged_collision_probability": str(p_collision),
        "averaged_collision_entropy_bits": h2_avg,
        "conditional_shannon_entropy_bits": shannon_cond,
        "closed_forms": {
            "P_guess": "16/q^4",
            "H_min_bits": "4*log2(q/2)",
            "P_collision_avg": "16/q^4",
            "H_collision_avg_bits": "4*log2(q/2)",
            "H_Shannon_bits": "4*(q-1)*log2(q-1)/q",
        },
    }


def main() -> int:
    rows = [exact_row(q) for q in (2, 3, 4, 5, 7, 8, 9, 11)]
    q3 = next(row for row in rows if row["q"] == 3)
    pass2836 = json.loads(
        (ROOT / "data" / "PART_W33_PASS2835_2836_WITTING_LINE_AND_LANDAUER.json")
        .read_text(encoding="utf-8")
    )

    old_shannon = pass2836["pass_2836"]["H_cond_float"]
    checks = {
        "q3_guessing_probability_is_16_over_81":
            q3["optimal_classical_guessing_probability"] == "16/81",
        "q3_min_entropy_is_log2_81_over_16":
            abs(q3["conditional_min_entropy_bits"] - math.log2(81 / 16)) < 1e-12,
        "q3_shannon_matches_pass2836":
            abs(q3["conditional_shannon_entropy_bits"] - old_shannon) < 1e-12,
        "q2_support_reveals_full_state":
            rows[0]["conditional_min_entropy_bits"] == 0.0
            and rows[0]["conditional_shannon_entropy_bits"] == 0.0,
        "all_rows_match_closed_guessing_formula":
            all(
                row["optimal_classical_guessing_probability"]
                == str(Fraction(16, row["q"] ** 4))
                for row in rows
            ),
        "classical_min_entropy_never_exceeds_shannon":
            all(
                row["conditional_min_entropy_bits"]
                <= row["conditional_shannon_entropy_bits"] + 1e-12
                for row in rows
            ),
    }

    out = {
        "schema": "w33.support-min-entropy.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "source": (
            "Companion to Pass 2836. The state X is uniform on F_q^4 and the "
            "observer receives only the zero/nonzero support mask."
        ),
        "q3_headline": {
            "P_guess_X_given_support": "16/81",
            "H_min_bits": q3["conditional_min_entropy_bits"],
            "H_Shannon_bits": q3["conditional_shannon_entropy_bits"],
            "interpretation": (
                "Seeing support leaves 2.33985 bits of classical min-entropy, "
                "while the average Shannon uncertainty is 8/3 bits."
            ),
        },
        "rows": rows,
        "quantum_side_information_boundary": (
            "These values condition only on the classical support mask. They do "
            "not certify randomness against arbitrary quantum side information E. "
            "A QKD/randomness proof must bound H_min(X|support,E) in its stated "
            "adversary model; that quantity can be smaller and can be zero if E "
            "fully determines X."
        ),
        "extractor_boundary": (
            "The leftover-hash lemma can use a proven smooth min-entropy bound as "
            "an extractor budget, but this certificate does not supply smoothing, "
            "finite-size statistics, or a quantum-proof extractor claim."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "q3_P_guess": "16/81",
        "q3_H_min_bits": q3["conditional_min_entropy_bits"],
        "q3_H_shannon_bits": q3["conditional_shannon_entropy_bits"],
    }, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
