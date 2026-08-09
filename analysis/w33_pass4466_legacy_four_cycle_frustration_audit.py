#!/usr/bin/env python3
"""Pass 4466 -- audit the Pass-4433 four-cycle frustration observable.

The historical helper in
analysis/w33_pass4433_4435_second_quadrangle_and_mechanism.py says

    "Every simple 4-cycle ... Counted once."

but it loops over every unordered diagonal pair and every pair of common
neighbours.  Consequently every underlying simple C4 is represented twice.
For a GQ(s,t) point-collinearity graph it also includes the C4s lying wholly in
one geometric K_{s+1} line, not only the induced generalized-quadrangle
apartments.

For a line signing the internal K_{s+1} cycles always have parity +1.  Hence the
legacy frustration observable is a deterministic dilution of the true induced-
quadrangle/apartment fraction, not an independent observable.

Let
    Q       = number of induced quadrangles,
    C_line  = 3 L C(s+1,4) simple C4s lying in geometric lines.

The legacy helper contains 2(Q+C_line) records, and if f_Q is the true apartment
frustration fraction then

    f_legacy = Q/(Q+C_line) * f_Q.

For W(3,3):
    Q=1620, C_line=120, records=3480,
    f_legacy=(27/29) f_Q.

Thus its random-line-signing mean is 27/58 rather than 1/2.  Crucially, the
standardized z-score against a random line-signing baseline is unchanged,
because the transformation is multiplication by a positive constant.  So Pass
4433's quoted W33 z≈+1.16 is not invalidated; the observable's label and raw
normalization are what need correction.

The dilution is strongly s-dependent.  For the recent cross-GQ examples:
    GQ(3,9): factor 243/245,
    GQ(9,3): factor 81/137.
This means raw legacy frustration fractions cannot be compared directly across
those dual parameter sets even before spectral questions enter.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry, simple_four_cycles
from w33_pass4465_general_gq_line_signing_trace import formulas

ROOT = Path(__file__).resolve().parents[1]


def legacy_records(A: np.ndarray):
    """Exact logic of Pass 4433's historical four_cycles helper."""
    n = len(A)
    nb = [set(np.nonzero(A[i])[0].tolist()) for i in range(n)]
    out = []
    for u in range(n):
        for w in range(u + 1, n):
            common = sorted(nb[u] & nb[w])
            for a, b in itertools.combinations(common, 2):
                out.append((u, a, w, b))
    return out


def dilution(s: int, t: int):
    row = formulas(s, t)
    C_line = 3 * row.lines * math.comb(s + 1, 4)
    factor = Fraction(row.quadrangles, row.quadrangles + C_line)
    return {
        "s": s,
        "t": t,
        "induced_quadrangles_Q": row.quadrangles,
        "line_internal_simple_C4": C_line,
        "legacy_records": 2 * (row.quadrangles + C_line),
        "legacy_to_apartment_factor": f"{factor.numerator}/{factor.denominator}",
        "factor_float": float(factor),
        "random_legacy_mean": float(factor) / 2.0,
        "random_legacy_sd": float(factor) / (2.0 * math.sqrt(row.quadrangles)),
    }


def main() -> int:
    _, lines, A, _, edge_line = geometry()
    induced = simple_four_cycles(A)
    historical = legacy_records(A)

    # Canonicalise each historical record to its four undirected edges.
    historical_edge_sets = []
    for u, a, w, b in historical:
        historical_edge_sets.append(
            frozenset(
                {
                    frozenset((u, a)),
                    frozenset((a, w)),
                    frozenset((w, b)),
                    frozenset((b, u)),
                }
            )
        )
    multiplicities = {}
    for C in historical_edge_sets:
        multiplicities[C] = multiplicities.get(C, 0) + 1

    assert len(historical) == 3480
    assert len(multiplicities) == 1740
    assert set(multiplicities.values()) == {2}
    assert len(induced) == 1620

    # Split unique simple cycles into line-internal and induced.
    internal, genuine = 0, 0
    for C in multiplicities:
        verts = set().union(*C)
        containing = [L for L in lines if verts <= L]
        if containing:
            internal += 1
        else:
            genuine += 1
    assert internal == 120
    assert genuine == 1620

    examples = {
        "GQ(2,2)": dilution(2, 2),
        "GQ(3,3)": dilution(3, 3),
        "GQ(3,9)": dilution(3, 9),
        "GQ(9,3)": dilution(9, 3),
    }
    assert examples["GQ(3,3)"]["legacy_to_apartment_factor"] == "27/29"
    assert examples["GQ(3,9)"]["legacy_to_apartment_factor"] == "243/245"
    assert examples["GQ(9,3)"]["legacy_to_apartment_factor"] == "81/137"

    # Verify the W33 frustration scaling directly on deterministic random line signs.
    edge_to_line = edge_line
    rng = np.random.default_rng(4466)
    max_residual = 0.0
    for _ in range(64):
        sigma = rng.choice(np.array([-1, 1], dtype=np.int64), size=40)
        bad_apartment = 0
        for C in induced:
            hol = 1
            for e in C:
                hol *= int(sigma[edge_to_line[e]])
            bad_apartment += int(hol < 0)
        fQ = bad_apartment / 1620.0

        bad_legacy = 0
        for u, a, w, b in historical:
            prod = 1
            for x, y in ((u, a), (a, w), (w, b), (b, u)):
                prod *= int(sigma[edge_to_line[frozenset((x, y))]])
            bad_legacy += int(prod < 0)
        flegacy = bad_legacy / 3480.0
        residual = abs(flegacy - (27.0 / 29.0) * fQ)
        max_residual = max(max_residual, residual)
        assert residual < 1e-15

    result = {
        "pass": 4466,
        "theorem": "legacy four-cycle frustration normalization audit",
        "historical_source": "analysis/w33_pass4433_4435_second_quadrangle_and_mechanism.py",
        "historical_docstring_claim": "Every simple 4-cycle ... Counted once.",
        "W33_exact_census": {
            "legacy_records": 3480,
            "unique_underlying_simple_C4": 1740,
            "record_multiplicity_per_simple_C4": 2,
            "induced_apartments": 1620,
            "line_internal_simple_C4": 120,
            "legacy_to_apartment_factor": "27/29",
            "random_legacy_mean": 27.0 / 58.0,
            "random_apartment_mean": 0.5,
            "direct_scaling_max_residual_64_samples": max_residual,
        },
        "general_formula": {
            "C_line": "3 L C(s+1,4)",
            "legacy_records": "2(Q+C_line)",
            "f_legacy": "Q/(Q+C_line) * f_apartment",
            "z_score_invariance": (
                "For a fixed GQ and a random-line-signing baseline, f_legacy is a positive scalar multiple "
                "of f_apartment, so standardized z scores are unchanged."
            ),
        },
        "examples": examples,
        "correction": (
            "Pass 4433's W33 z-score is not withdrawn.  Its raw 'four-cycle frustration' should be read "
            "as a diluted apartment frustration.  Cross-GQ raw fractions require the parameter-dependent "
            "undilution above before comparison."
        ),
        "boundary": (
            "This audit corrects enumeration semantics and normalization only.  It does not alter Pass 4433's "
            "separate Ramanujan/non-Ramanujan spectral verdicts."
        ),
    }

    out = ROOT / "data" / "PART_W33_PASS4466_LEGACY_FOUR_CYCLE_FRUSTRATION_AUDIT.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4466 -- legacy four-cycle frustration audit")
    print("  historical W33 records = 3480")
    print("  unique simple C4 = 1740 = 1620 apartments + 120 line-internal")
    print("  every simple C4 is recorded twice")
    print("  f_legacy = (27/29) f_apartment on W33")
    print("  z scores against same-family random baselines are invariant")
    print("  dual-pair dilution: GQ(3,9)=243/245, GQ(9,3)=81/137")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
