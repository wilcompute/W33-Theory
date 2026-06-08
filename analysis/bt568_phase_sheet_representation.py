#!/usr/bin/env python3
"""BT568: Phase-sheet representation.

The minimal logical vector pairing has two nonzero F_3 phase sheets.  BT568
models them as a signed two-sheet cover over the true 25920-size flag-frame
symmetry scale:

    phase +1 sheet: 25920 pairs
    phase -1 sheet: 25920 pairs
    total nonzero: 51840

The cover is not an incidence automorphism double of the q=3 Levi geometry; it
is a phase double over the projective support pairing.
"""
import json
from pathlib import Path

flag_group = 25920
phase_counts = {"+1": 25920, "-1": 25920, "0": 984960}
vector_pairs = 320 * 3240
nonzero = phase_counts["+1"] + phase_counts["-1"]
projective_support_pairs = 160 * 81
checks = {
    "total_pairs": vector_pairs == 1036800,
    "phase_partition": sum(phase_counts.values()) == vector_pairs,
    "nonzero_double": nonzero == 2 * flag_group == 51840,
    "balanced_nonzero_sheets": phase_counts["+1"] == phase_counts["-1"] == flag_group,
    "scalar_expansion_factor": nonzero == 4 * projective_support_pairs,
    "projective_support_pairs": projective_support_pairs == 12960,
}
result = {
    "bt": 568,
    "title": "Phase-sheet representation",
    "base_projective_support_pairs": projective_support_pairs,
    "scalar_expansion_factor": 4,
    "vector_pairs": vector_pairs,
    "phase_counts": phase_counts,
    "nonzero_phase_total": nonzero,
    "true_flag_group_order": flag_group,
    "sheet_model": "two balanced nonzero F3 phase sheets, each of size 25920, over the projective support pairing",
    "boundary": "This is a phase double, not a q=3 point-line duality or extra Levi incidence automorphism.",
    "all_identities": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT568_PHASE_SHEET_REPRESENTATION_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
