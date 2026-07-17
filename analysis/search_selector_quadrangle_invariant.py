#!/usr/bin/env python3
"""Search for the cyclic phase invariant separating failing selector quadrangles.

BT362 showed that all 1620 minimal Z quadrangles share the same local D4 lift:
8 incident sheets = 4 boundary lines * 2 present phases.  The one missing phase
on each line is matched across skew lines.

This script searches for the invariant in the cyclic sequence of missing phases
(m0, m1, m2, m3) that distinguishes the 108 failures from the 1512 flat quadrangles.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (
    build_w33,
    generate_projective_symplectic_group,
    minimal_supports,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (
    selector_failure_edge_supports,
    sheet_orbit,
)
from analysis.w33_golden_selector_z20_cochain_lift import (
    build_transport_edges,
    build_unique_quadrangles,
    load_selector_data,
)

def main():
    points, edges, edge_index, lines, adjacency = build_w33()
    _x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)
    
    # 1. Map sheets to (line_index, phase_index)
    # We define phase_index by sorting the sheets in each line fiber
    sheet_to_line = {}
    point_frequency = []
    for sheet in sheets:
        freq = Counter()
        for support in sheet:
            for edge_id in support:
                for pt in edges[edge_id]:
                    freq[pt] += 1
        anchor = tuple(sorted(pt for pt, count in freq.items() if count == 108))
        sheet_to_line[sheets.index(sheet)] = next(i for i, l in enumerate(lines) if tuple(l) == anchor)

    line_fibers = defaultdict(list)
    for s_idx, l_idx in sheet_to_line.items():
        line_fibers[l_idx].append(s_idx)
    for l_idx in line_fibers:
        line_fibers[l_idx].sort()

    sheet_to_phase = {}
    for l_idx, fiber in line_fibers.items():
        for phase, s_idx in enumerate(fiber):
            sheet_to_phase[s_idx] = phase

    # 2. Map intersection points to phase matchings for skew lines
    sheet_intersections = [[0] * 120 for _ in range(120)]
    for i in range(120):
        for j in range(120):
            sheet_intersections[i][j] = len(sheets[i] & sheets[j])

    # 3. Load quadrangles and holonomy
    selector_lines, sigma = load_selector_data()
    _t_edges, t_edge_index = build_transport_edges(selector_lines)
    quadrangles = build_unique_quadrangles(selector_lines, sigma, t_edge_index)
    
    # Map edges to line index once
    edge_to_line = {}
    for l_idx, line in enumerate(lines):
        for u, v in combinations(line, 2):
            edge_to_line[edge_index[tuple(sorted((u, v)))]] = l_idx

    # Incident sheets per support
    incident_sheets = defaultdict(list)
    for s_idx, sheet in enumerate(sheets):
        for support in sheet:
            incident_sheets[support].append(s_idx)

    print(f"Analyzing {len(quadrangles)} quadrangles...")
    
    results = []
    for q in quadrangles:
        pts = tuple(q.points)
        support = tuple(sorted(edge_index[tuple(sorted((pts[i], pts[(i+1)%4])))] for i in range(4)))
        incident = set(incident_sheets[support])
        
        # Missing phases: for each boundary line, which phase index is missing?
        missing = []
        for l_idx in q.lines:
            fiber = line_fibers[l_idx]
            m_s_idx = next(s for s in fiber if s not in incident)
            missing.append(sheet_to_phase[m_s_idx])
            
        # We need the relative phase too. 
        # But let's first see if the raw missing indices (m0, m1, m2, m3) tell us anything.
        results.append({
            'holonomy': q.holonomy,
            'missing': tuple(missing)
        })

    # Group by holonomy
    hol_to_missing = defaultdict(Counter)
    for r in results:
        hol_to_missing[r['holonomy']][r['missing']] += 1

    print("\nHolonomy to Missing Phase Sequence Profile:")
    for hol, counts in sorted(hol_to_missing.items()):
        print(f"Holonomy {hol}: {dict(counts)}")

    # Is there a shift invariant? (m0, m1, m2, m3) -> (m1, m2, m3, m0) etc.
    def canonical(seq):
        opts = []
        for i in range(4):
            opts.append(seq[i:] + seq[:i])
        opts += [o[::-1] for o in opts]
        return min(opts)

    hol_to_canonical = defaultdict(Counter)
    for r in results:
        hol_to_canonical[r['holonomy']][canonical(r['missing'])] += 1

    print("\nHolonomy to Canonical Phase Sequence Profile:")
    for hol, counts in sorted(hol_to_canonical.items()):
        print(f"Holonomy {hol}: {dict(counts)}")

if __name__ == "__main__":
    main()
