#!/usr/bin/env python3
"""BT583: phase-cover homology toy model.

This is the smallest algebraic model of the BT580 cover skeleton.  For each
base incidence, the four scalar lifts form a 4-cycle square.  The deck action
pairs opposite phase sheets by flipping one scalar coordinate.

The local square has beta_1=1.  Across 12960 independent base incidences, the
fiber-only toy homology has rank 12960.  This is deliberately a toy fiber
homology: it is not the W33 Levi H1=81, which lives in the point-line Levi graph.
"""
import json
from pathlib import Path

BASE = 12960
vertices_per_fiber = 4
edges_per_fiber = 4
components_per_fiber = 1
beta1_per_fiber = edges_per_fiber - vertices_per_fiber + components_per_fiber
checks = {
    "local_square_beta1": beta1_per_fiber == 1,
    "global_vertices": BASE * vertices_per_fiber == 51840,
    "global_edges": BASE * edges_per_fiber == 51840,
    "global_components": BASE * components_per_fiber == 12960,
    "global_beta1": BASE * beta1_per_fiber == 12960,
    "not_Levi_H1": BASE * beta1_per_fiber != 81,
}
result = {
    "bt": 583,
    "title": "Phase-cover homology toy model",
    "local_fiber": "4 vertices, 4 edges, one square cycle",
    "local_beta1": beta1_per_fiber,
    "global_vertices": BASE * vertices_per_fiber,
    "global_edges": BASE * edges_per_fiber,
    "global_components": BASE,
    "global_fiber_beta1": BASE,
    "interpretation": "The scalar-cover fiber has a trivial square-cycle homology of rank 12960. This is separate from the geometric Levi H1=81.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}
Path("data/PART_BT583_PHASE_COVER_HOMOLOGY_TOY_MODEL_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
