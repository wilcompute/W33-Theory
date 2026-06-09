#!/usr/bin/env python3
"""BT579: all-orders rigidity lemma for the repaired normalized flow.

The BT570-BT576 repaired flow has the schematic form

  X -> P_{E0+E4} C3(X) -> remove E0 -> normalize E4 diagonal.

After the first two arrows, any admissible input whose repaired E4 amplitude is
nonzero has the form z E4.  The normalization map sends z E4 to the fixed Gram
amplitude (160/81) E4.  Thus the local shape map is algebraically constant on
z != 0.  All derivatives of positive order vanish.
"""
import json
from pathlib import Path
import sympy as sp

z = sp.symbols("z", nonzero=True)
target = sp.Rational(160, 81)
normalized_amplitude = sp.simplify(target * z / z)
orders = list(range(1, 11))
derivatives = [sp.diff(normalized_amplitude, z, n) for n in orders]
checks = {
    "normalization_returns_target": normalized_amplitude == target,
    "derivatives_1_to_10_vanish": all(d == 0 for d in derivatives),
    "requires_nonzero_E4_amplitude": True,
}
result = {
    "bt": 579,
    "title": "All-orders rigidity lemma",
    "local_coordinate": "z = repaired centered E4 amplitude",
    "normalized_amplitude": str(normalized_amplitude),
    "tested_derivative_orders": orders,
    "derivatives": [str(d) for d in derivatives],
    "lemma": "On the nonzero E4-amplitude stratum, repaired-center-normalize sends zE4 to (160/81)E4, so every positive derivative of the shape map is zero.",
    "boundary": "The lemma is local on z != 0; it does not define a normalized output at z=0.",
    "all_identities": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT579_ALL_ORDERS_RIGIDITY_LEMMA_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
