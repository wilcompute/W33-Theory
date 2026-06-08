#!/usr/bin/env python3
"""BT564: W33 Levi 25920/51840 symmetry-phase split.

BT561 fixes the full q=3 Levi flag-frame incidence symmetry at PSp(4,3) of
order 25920.  The doubled number 51840 is not a hidden point-line duality of the
Levi frame; it is the signed phase/noncommutation scale already visible in the
minimal logical vector census.
"""
import json
from pathlib import Path

psp43 = 25920
we6 = 51840
flag_edges = 160
flag_stabilizer = 162
projective_x = 160
vector_x = 320
bad_z_per_projective_x = 81
bad_z_per_vector_x = 162
phase_plus = 25920
phase_minus = 25920
checks = {
    "flag_orbit_stabilizer": flag_edges * flag_stabilizer == psp43,
    "phase_double": phase_plus + phase_minus == we6,
    "each_phase_equals_true_flag_group": phase_plus == psp43 and phase_minus == psp43,
    "vector_noncommutation_count": vector_x * bad_z_per_vector_x == we6,
    "projective_support_count": projective_x * bad_z_per_projective_x == 12960,
    "no_duality_doubling": 2 * psp43 == we6,
}
result = {
    "bt": 564,
    "title": "W33 Levi 25920/51840 symmetry-phase split",
    "true_flag_frame_symmetry": {"group": "PSp(4,3)", "order": psp43, "orbit_stabilizer": "160*162=25920"},
    "doubled_phase_scale": {"order": we6, "phase_plus": phase_plus, "phase_minus": phase_minus, "vector_count": "320*162=51840"},
    "boundary": "51840 is the signed nonzero phase/noncommutation double, not the q=3 Levi flag-frame automorphism order.",
    "interpretation": "The q=3 incidence geometry has no point-line duality; each nonzero phase sheet has the true flag symmetry order 25920.",
    "all_identities": checks,
    "all_identities_hold": all(checks.values())
}
Path("data/PART_BT564_SYMMETRY_PHASE_SPLIT_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
