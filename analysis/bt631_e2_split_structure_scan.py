#!/usr/bin/env python3
"""BT631: scan the E2 split 77^15 + (-3)^15 for small-graph structure.

BT617 found that the folded cubic operator F3 has an E2 block with spectrum

    77^15 + (-3)^15.

BT631 checks whether this split carries the fingerprints of familiar 15-point
substrates.  The clean observation is that the affine normalization

    A = (B + 3 I) / 80

has eigenvalues 1^15 and 0^15 on the E2 block, i.e. it is an idempotent after
splitting the 30-dimensional E2 sector into two equal halves.  Equivalently,

    B^2 - 74 B - 231 I = 0

on E2, because (77 and -3) are the two roots.

The two rank-15 halves match the dimensions of the K6 duad carrier and the
15 negative/root-pair count, but the spectrum is a two-projector split rather
than the adjacency spectrum of Petersen/T(6)/K6-duad graphs.  This is a useful
boundary: E2 is a 15+15 packet, not yet a canonical graph module.
"""
from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    eig_hi = 77
    eig_lo = -3
    mult_hi = 15
    mult_lo = 15
    dim_e2 = mult_hi + mult_lo

    trace = eig_hi * mult_hi + eig_lo * mult_lo
    trace_sq = eig_hi * eig_hi * mult_hi + eig_lo * eig_lo * mult_lo
    determinant_signless_abs = (abs(eig_hi), abs(eig_lo))

    # Minimal polynomial on E2: (x-77)(x+3)=x^2-74x-231.
    minpoly = {"x2": 1, "x": -74, "constant": -231}

    # Projector onto the +77 eigenspace from the E2 block B:
    # P_hi=(B+3I)/80; P_lo=(77I-B)/80.
    spectral_gap = eig_hi - eig_lo
    projector_denominator = spectral_gap
    projector_ranks = {"P_hi_rank": mult_hi, "P_lo_rank": mult_lo}

    candidate_graph_spectra = {
        "K6_line_graph_T6": "8^1, 2^5, -2^9 on 15 vertices",
        "Petersen": "3^1, 1^5, -2^4 on 10 vertices",
        "K6_duad_permutation_carrier": "dimension 15 = 1+5+9 under S6",
        "A2_or_fifteen_root_pairs": "15 is a count match, but no adjacency spectrum match is forced by 77/-3 alone",
    }

    checks = {
        "E2_dimension_30": dim_e2 == 30,
        "equal_15_15_split": mult_hi == mult_lo == 15,
        "spectral_gap_80": spectral_gap == 80,
        "minimal_polynomial_correct": eig_hi**2 - 74 * eig_hi - 231 == 0 and eig_lo**2 - 74 * eig_lo - 231 == 0,
        "projector_denominator_80": projector_denominator == 80,
        "trace_1110": trace == 1110,
        "trace_square_exact": trace_sq == 89070,
        "not_T6_adjacency_spectrum": (eig_hi, eig_lo) != (8, -2),
        "not_Petersen_adjacency_spectrum": (eig_hi, eig_lo) != (3, -2),
    }

    result = {
        "bt": 631,
        "title": "E2 split structure scan",
        "input_from_BT617": "E2 F3 E2 has spectrum 77^15 + (-3)^15",
        "eigen_data": {
            "eigenvalues": {"77": mult_hi, "-3": mult_lo},
            "dimension": dim_e2,
            "trace": trace,
            "trace_square": trace_sq,
            "absolute_eigenvalue_pair": determinant_signless_abs,
        },
        "minimal_polynomial_on_E2": "x^2 - 74x - 231 = 0",
        "projector_split": {
            "P_hi": "((E2F3E2)+3E2)/80",
            "P_lo": "((77E2)-(E2F3E2))/80",
            "ranks": projector_ranks,
            "interpretation": "E2 splits into two rank-15 halves under F3.",
        },
        "candidate_structure_scan": candidate_graph_spectra,
        "interpretation": "The 15+15 split is real and exact. It resonates with the 15-dimensional K6 duad carrier and root-pair counts, but the two-eigenvalue block is a projector split, not yet an adjacency module for Petersen, T(6), or an A2 graph. A future test must construct an actual basis or incidence object for the two rank-15 projectors.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT631_E2_SPLIT_STRUCTURE_SCAN_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
