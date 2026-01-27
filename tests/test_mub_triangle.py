import numpy as np
from THEORY_PART_CLII_STATE_PARTICIPATION import get_mub_system, participation

# Precompute the full set of triangles across all MUB systems so multiple tests can reference it
all_triangles = set()
for v in range(40):
    for triangle in get_mub_system(v):
        all_triangles.add(triangle)


def test_triangle_counts_and_participation():
    # total triangles: 160 unique triangles across all MUBs
    all_triangles = set()
    for v in range(40):
        for triangle in get_mub_system(v):
            all_triangles.add(triangle)
    assert len(all_triangles) == 160

    # each state appears in exactly 12 MUB systems
    counts = [len(participation[s]) for s in range(40)]
    assert all(c == 12 for c in counts)


def test_triangle_unique_completion():
    # each triangle completes to exactly one vertex
    for triangle in all_triangles:
        completions = [v for v in range(40) if triangle in get_mub_system(v)]
        assert len(completions) == 1
