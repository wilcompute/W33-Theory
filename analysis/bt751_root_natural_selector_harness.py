#!/usr/bin/env python3
"""BT751 — root-natural selector harness.

This is the executable scaffold following BT748--BT750.

Known inputs:
  BT748: presentation pairs admit equivariant coordinates
         (root triple tau, chirality eps, centralizer coordinate c),
         with 540 x 2 x 48 = 51840.
  BT749: locally, the 24 lifts over one rectangle map 2-to-1 onto the
         12 reflections of D12; chirality is the reflection-class split.
  BT750: the two lifts fixed by a reflection are central-half-turn partners
         {k, r^6 k}, and they are different Levi octagons.

Consequence:
  A root-natural one-lift-per-rectangle selector cannot be "constant phase"
  alone.  It must choose:
      chirality eps, dihedral phase phi, and duo bit delta.

This harness records the three tests every future selector implementation must
pass.  It is deliberately lightweight: it is a machine-readable contract plus
helper formulas, not a full reimplementation of the 51840-pair coordinate
enumerator.  The heavy coordinate enumerator should import this contract and
emit the result fields below.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class SelectorContract:
    theorem: str = "BT751 root-natural selector harness"
    total_rectangles: int = 2160
    root_triples: int = 540
    chiralities: int = 2
    inner_centralizer_half_fiber: int = 48
    local_lifts_per_rectangle: int = 24
    chiral_lifts_per_rectangle: int = 12
    dihedral_phases_per_chirality: int = 6
    duo_bits_per_phase: int = 2
    expected_selected_rows: int = 2160
    expected_rank_mod_1000003: int = 81
    expected_hits_per_root_triple: int = 4
    expected_global_register_dim: int = 4


def expected_root_uniform_distribution(contract: SelectorContract) -> dict[str, int]:
    """Root-natural selector should hit every root-triple fiber four times."""
    assert contract.expected_selected_rows == (
        contract.root_triples * contract.expected_hits_per_root_triple
    )
    return {str(contract.expected_hits_per_root_triple): contract.root_triples}


def necessary_local_choice(contract: SelectorContract) -> dict[str, object]:
    """BT750's local obstruction: phase alone is not a selector."""
    return {
        "phase_only_choices_per_rectangle": contract.duo_bits_per_phase,
        "phase_plus_duo_choices_per_rectangle": 1,
        "reason": (
            "BT750 shows the two phase-duo partners are r^6-related but present "
            "different Levi octagons; selecting a reflection/phase leaves two "
            "apartments unless the duo bit is also fixed."
        ),
    }


def test_fields_template() -> dict[str, object]:
    """Fields a completed root-natural selector verifier must fill."""
    c = SelectorContract()
    return {
        "contract": asdict(c),
        "candidate_parameters": {
            "chirality": "Type-A or Type-B",
            "dihedral_phase": "0..5 within the selected reflection class",
            "duo_bit": "0 or 1, the r^6 central-half-turn coordinate",
            "base_pair": "presentation-pair key used to trivialize torsor coordinates",
        },
        "required_tests": {
            "T1_one_lift_per_rectangle": {
                "expected_selected_rows": c.expected_selected_rows,
                "pass_condition": "exactly one selected lift for each of 2160 rectangles",
            },
            "T2_rank": {
                "expected_rank_mod_1000003": c.expected_rank_mod_1000003,
                "pass_condition": "signed selector matrix has rank 81 over GF(1000003)",
            },
            "T3_root_uniformity": {
                "expected_distribution": expected_root_uniform_distribution(c),
                "pass_condition": "every one of 540 root-triple fibers is hit exactly 4 times",
            },
            "T4_gluing_flatness": {
                "expected_global_register_dim": c.expected_global_register_dim,
                "pass_condition": "BT741-style gluing quotient is connected and leaves F2^4",
            },
            "T5_chirality_stability": {
                "pass_condition": "all selected lifts lie in one absolute chirality torsor",
            },
            "T6_apartment_noncollapse": {
                "pass_condition": "central half-turn duo partners are not identified as the same octagon",
            },
        },
        "necessary_local_choice": necessary_local_choice(c),
        "boundary": (
            "This is a verifier harness/specification.  It does not assert that "
            "a candidate already passes T1--T6; it pins down what the next heavy "
            "coordinate enumerator must prove."
        ),
    }


def main() -> None:
    out = test_fields_template()
    path = Path("data/bt751_root_natural_selector_harness.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
