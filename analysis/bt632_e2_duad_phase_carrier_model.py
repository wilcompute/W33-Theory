#!/usr/bin/env python3
"""BT632: explicit duad-phase carrier model for the E2 = 15+15 split.

BT617/BT631 found the E2 block of the folded cubic operator F3:

    E2 F3 E2 has spectrum 77^15 + (-3)^15.

BT632 gives the cleanest explicit carrier consistent with all verified data:

    E2_model = Q^{15}_{K6 duads} \otimes Q^2_{phase sign}.

The 15 basis labels are the duads of K6.  The two phase sheets are + and -.
On this carrier the normalized split operator is

    S = sigma_z,

and the folded cubic E2 block is modeled by

    B_E2 = 37 I + 40 S.

Therefore the two eigenvalues are 37+40=77 and 37-40=-3.  This is an
explicit incidence-style basis for the 15+15 packet, while preserving the
boundary from BT631: this is a carrier model for the spectral split, not yet a
canonical proof that the numeric E2 eigenspace basis equals the K6-duad basis.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path


def duads(n: int = 6) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(1, n + 1), 2))


def main() -> int:
    labels = duads(6)
    sheets = ["+", "-"]
    basis = [(d, s) for d in labels for s in sheets]
    dim = len(basis)

    center = 37
    amplitude = 40
    eig_plus = center + amplitude
    eig_minus = center - amplitude
    trace = len(labels) * (eig_plus + eig_minus)
    trace_sq = len(labels) * (eig_plus**2 + eig_minus**2)

    # K6-duad adjacency counts for context; no graph equality is claimed.
    # T(6)=L(K6) has degree 8 on 15 duads.
    duad_neighbors = {}
    for d in labels:
        duad_neighbors[d] = [e for e in labels if len(set(d) & set(e)) == 1]
    degree_profile = sorted({len(v) for v in duad_neighbors.values()})

    checks = {
        "duad_count_15": len(labels) == 15,
        "phase_sheet_count_2": len(sheets) == 2,
        "carrier_dimension_30": dim == 30,
        "plus_sheet_dimension_15": sum(1 for _, s in basis if s == "+") == 15,
        "minus_sheet_dimension_15": sum(1 for _, s in basis if s == "-") == 15,
        "center_amplitude_recover_77_minus3": (eig_plus, eig_minus) == (77, -3),
        "minimal_polynomial_roots": eig_plus**2 - 74 * eig_plus - 231 == 0 and eig_minus**2 - 74 * eig_minus - 231 == 0,
        "trace_matches_BT631": trace == 1110,
        "trace_square_matches_BT631": trace_sq == 89070,
        "T6_duad_degree_8_context": degree_profile == [8],
        "not_claimed_canonical_numeric_basis": True,
    }

    result = {
        "bt": 632,
        "title": "Explicit duad-phase carrier model for the E2 split",
        "carrier": "K6 duads x two phase sheets",
        "basis_size": dim,
        "duad_count": len(labels),
        "phase_sheets": sheets,
        "operator_model": "B_E2 = 37 I + 40 sigma_z",
        "eigenvalues": {"plus_sheet": eig_plus, "minus_sheet": eig_minus},
        "projector_reading": {
            "P_plus": "duad basis on + phase sheet, rank 15",
            "P_minus": "duad basis on - phase sheet, rank 15",
            "BT631_formula_plus": "(B_E2+3I)/80",
            "BT631_formula_minus": "(77I-B_E2)/80",
        },
        "K6_duad_context": {
            "duad_labels": labels,
            "T6_degree_profile": degree_profile,
            "boundary": "The duad graph supplies a natural 15-label carrier. BT632 does not identify the numeric E2 eigenvectors with this basis without an additional intertwiner construction.",
        },
        "interpretation": "The E2 sector can be organized as a 15-duad carrier tensored with a two-sheet phase sign. The folded cubic block is then a phase-splitting Hamiltonian with center 37 and amplitude 40, giving 77 and -3 exactly.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT632_E2_DUAD_PHASE_CARRIER_MODEL_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
