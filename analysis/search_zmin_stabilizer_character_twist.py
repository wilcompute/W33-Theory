#!/usr/bin/env python3
"""BT359 follow-up: extract Z-min stabilizer and search for a character twist.

We want to find a character on the 32-element Z-min stabilizer fiber that
cancels the 108 golden selector failures.
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
    act_support,
    build_w33,
    generate_projective_symplectic_group,
    minimal_supports,
)
from analysis.w33_golden_selector_z20_cochain_lift import (
    build_transport_edges,
    build_unique_quadrangles,
    load_selector_data,
)

def apply_group_element(element, points):
    return tuple(element[p] for p in points)

def main():
    print("Building W33 geometry...")
    points, edges, edge_index, lines, adjacency = build_w33()
    print(f"Points: {len(points)}, Edges: {len(edges)}, Lines: {len(lines)}")
    
    print("Finding minimal supports...")
    _x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    print(f"Found {len(z_supports)} Z-min supports.")
    
    print("Generating PSp(4,3) group...")
    # group = generate_projective_symplectic_group(points)
    # print(f"Group size: {len(group)}")
    
    # Let's skip the full group search and use the matrices directly.
    from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import canonical
    
    def get_sp43_generators():
        # Generators for Sp(4,3)
        # J = [[0,0,1,0], [0,0,0,1], [2,0,0,0], [0,2,0,0]]
        pass
    
    # Let's look at a single Z-min support (quadrangle)
    z0 = list(z_supports)[0]
    print(f"Sample Z-min support: {z0}")
    # z0 is a tuple of 4 edges. Each edge is a tuple of 2 points.
    
    # We need to find the 108 failure quadrangles in terms of Z20 cochain.
    # w33_golden_selector_z20_cochain_lift.py does this.
    
    selector_lines, sigma = load_selector_data()
    t_edges, t_edge_index = build_transport_edges(selector_lines)
    quads = build_unique_quadrangles(selector_lines, sigma, t_edge_index)
    
    failures = [q for q in quads if q.holonomy == -1]
    print(f"Failures: {len(failures)} / {len(quads)}")

    # 2. Map directed quadrangles to the stabilizer
    selector_lines, sigma = load_selector_data()
    t_edges, t_edge_index = build_transport_edges(selector_lines)
    quads = build_unique_quadrangles(selector_lines, sigma, t_edge_index)
    
    failures = [q for q in quads if q.holonomy == -1]
    print(f"Failures: {len(failures)} / {len(quads)}")
    
    failure_supports = {tuple(sorted(edge_index[tuple(sorted((q.points[i], q.points[(i+1)%4])))] for i in range(4))) for q in failures}
    
    # Instead of full orbit search, just check stabilizers.
    s0 = list(failure_supports)[0]
    s0_stab = [g for g in group if act_support(g, s0, edges, edge_index) == s0]
    print(f"Failure support stabilizer size: {len(s0_stab)}")
    
    # How many elements map s0 to other failure supports?
    maps_to_failures = 0
    mapped_images = set()
    for g in group:
        img = act_support(g, s0, edges, edge_index)
        if img in failure_supports:
            maps_to_failures += 1
            mapped_images.add(img)
    print(f"Group elements mapping s0 to failures: {maps_to_failures}")
    print(f"Unique images in failures: {len(mapped_images)}")
    
    # 4. Analyze the holonomy values in the stabilizer
    print("\nAnalyzing holonomy values for failures...")
    h_counts = Counter()
    for q in failures:
        # q.holonomy is already -1/1, but we need the group element
        # Wait, the 'quads' objects in w33_golden_selector_z20_cochain_lift
        # might not have the full group element.
        pass

    # Let's re-calculate holonomy as a group element for one failure
    q0 = failures[0]
    # We need to find the transport elements g_ij
    # In w33_golden_selector_z20_cochain_lift, transport is just a sign?
    # No, it should be a group element in the stabilizer search.
    
    print("Failure 0 points:", q0.points)
    # The selector lines at these points:
    l0, l1, l2, l3 = [selector_lines[p] for p in q0.points]
    print("Lines:", l0, l1, l2, l3)

