#!/usr/bin/env python3
"""BT367: The Global Selector Obstruction Solver - A Cohomology Sweep.

BT366 proved that each skew-line pair carries a canonical phase matching (a permutation Sigma_ij in S3).
BT367 searches for a global assignment of phases (a "signing" s_i in S3 for each line i)
such that Sigma_ij = s_j * s_i^-1 for all skew pairs (i, j).

If this holds, the qutrit bundle is trivial (untwisted).
If it fails, we measure the obstruction (the "holonomy") which defines the
topological complexity of the Holonet's optical address bus.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    build_w33,
)

OUT = ROOT / "data" / "w33_BREAKTHROUGH_367_global_obstruction_results.json"


def get_permutation(pairs: list[list[int]]) -> tuple[int, ...]:
    """Converts a list of (left, right) matching pairs to a permutation tuple."""
    p = [0, 0, 0]
    for l, r in pairs:
        p[l] = r
    return tuple(p)


def compose(p1: tuple[int, ...], p2: tuple[int, ...]) -> tuple[int, ...]:
    """Composes p2 * p1."""
    return tuple(p2[p1[i]] for i in range(3))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    """Returns the inverse permutation."""
    inv = [0, 0, 0]
    for i, v in enumerate(p):
        inv[v] = i
    return tuple(inv)


def main() -> int:
    cert_path = (
        ROOT / "data" / "w33_BREAKTHROUGH_366_selector_phase_transport_certificate.json"
    )
    if not cert_path.exists():
        print(
            "BT366 certificate not found. Run analysis/w33_BREAKTHROUGH_366_selector_phase_transport_certificate.py first."
        )
        return 1

    # We need the full cert, but the sample in JSON only has 8 records.
    # Re-running the logic to get ALL records.
    from analysis.w33_BREAKTHROUGH_366_selector_phase_transport_certificate import (
        build_payload,
    )

    full_payload = build_payload()
    # We need to hack build_payload to return ALL records or just run the logic here.
    # Let's just run the logic to extract Sigma_ij for all 540 pairs.

    records = []
    # Re-extract all records (build_payload was returning a sample)
    # Actually, let's just modify the local logic to get the 540 permutations.

    # We'll use a local version of the transport loop.
    from collections import Counter
    from itertools import combinations

    from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
        generate_projective_symplectic_group,
    )
    from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (
        selector_failure_edge_supports,
        sheet_orbit,
    )
    from analysis.w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle import (
        sheet_anchor_line,
    )

    points, edges, edge_index, lines, _ = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)
    anchor_by_sheet = [sheet_anchor_line(sheet, edges, lines) for sheet in sheets]
    fibers = defaultdict(list)
    for s_idx, l_idx in enumerate(anchor_by_sheet):
        fibers[l_idx].append(s_idx)

    # Precompute all sheet intersections
    intersections = [
        [len(sheets[l] & sheets[r]) for r in range(120)] for l in range(120)
    ]

    sigma = {}  # (i, j) -> permutation in S3

    for left_line, right_line in combinations(sorted(fibers), 2):
        left_fiber = sorted(fibers[left_line])
        right_fiber = sorted(fibers[right_line])
        # Check if skew
        if set(lines[left_line]) & set(lines[right_line]):
            continue

        mapping = {}
        for l_phase, l_sheet in enumerate(left_fiber):
            for r_phase, r_sheet in enumerate(right_fiber):
                if intersections[l_sheet][r_sheet] == 4:
                    mapping[l_phase] = r_phase

        perm = tuple(mapping[i] for i in range(3))
        sigma[(left_line, right_line)] = perm
        sigma[(right_line, left_line)] = inverse(perm)

    # Now we have the 1-cocycle sigma on the skew-edge graph of W(3,3).
    # The skew-edge graph has 40 vertices (lines) and 540 edges.

    # Let's try to propagate a global signing.
    signs = {0: (0, 1, 2)}  # Line 0 starts with identity phase mapping
    queue = [0]
    conflicts = 0
    satisfied = 0

    # Breadth-first propagation
    skew_neighbors = defaultdict(list)
    for u, v in sigma:
        skew_neighbors[u].append(v)

    while queue:
        u = queue.pop(0)
        for v in skew_neighbors[u]:
            expected_sign_v = compose(signs[u], sigma[(u, v)])
            if v in signs:
                if signs[v] != expected_sign_v:
                    conflicts += 1
                else:
                    satisfied += 1
            else:
                signs[v] = expected_sign_v
                queue.append(v)

    # Analyze holonomy: If conflicts == 0, the bundle is trivial.
    # If not, the bundle has a Z3 (or S3) obstruction.

    results = {
        "lines_processed": len(signs),
        "total_skew_edges": len(sigma) // 2,
        "satisfied_constraints": satisfied,
        "conflicts": conflicts,
        "is_trivial": conflicts == 0,
        "topology": "trivial" if conflicts == 0 else "twisted",
        "cocycle_sample": {str(k): list(v) for k, v in list(sigma.items())[:5]},
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
