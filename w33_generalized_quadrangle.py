#!/usr/bin/env sage
"""
Explore whether W33's incidence structure is related to the building for PSp(4,3).

The building for a group of Lie type consists of simplices corresponding to
parabolic subgroups. For PSp(4,3) (type C2), the building is a generalized
quadrangle!

A generalized quadrangle GQ(s,t) has:
- Points and lines
- Each point is on t+1 lines
- Each line contains s+1 points
- No triangles (if two points are not collinear, they have exactly one common neighbor)

For PSp(4,3), the classical GQ is GQ(3,3) or related.
"""

from sage.all import *
import json

with open("claude_workspace/data/w33_sage_incidence_h1.json") as f:
    data = json.load(f)

print("=== Is W33 a Generalized Quadrangle? ===")
print()

# Load W33 lines
from lib.w33_io import W33DataPaths, load_w33_lines
from pathlib import Path

here = Path('.').resolve()
import sys
sys.path.insert(0, str(here / 'claude_workspace'))

paths = W33DataPaths.from_this_file(str(here / 'claude_workspace' / 'w33_sage_incidence_and_h1.py'))
lines = load_w33_lines(paths)

n_points = 40
n_lines = 40

print(f"W33 has {n_points} points and {n_lines} lines")
print()

# Compute basic statistics
points_per_line = [len(line) for line in lines]
print(f"Points per line: {set(points_per_line)}")

# Compute lines per point
lines_per_point = [0] * n_points
for line_idx, pts in enumerate(lines):
    for p in pts:
        lines_per_point[p] += 1

print(f"Lines per point: {set(lines_per_point)}")
print()

# For GQ(s,t): each line has s+1 points, each point is on t+1 lines
s_plus_1 = list(set(points_per_line))[0] if len(set(points_per_line)) == 1 else None
t_plus_1 = list(set(lines_per_point))[0] if len(set(lines_per_point)) == 1 else None

if s_plus_1 and t_plus_1:
    s = s_plus_1 - 1
    t = t_plus_1 - 1
    print(f"Regular structure: s = {s}, t = {t}")
    print(f"This would be GQ({s}, {t})")
    print()
    
    # Check the GQ counting formula:
    # |points| = (s+1)(st+1)
    # |lines| = (t+1)(st+1)
    expected_points = (s+1) * (s*t + 1)
    expected_lines = (t+1) * (s*t + 1)
    print(f"GQ({s},{t}) should have:")
    print(f"  Points: (s+1)(st+1) = {expected_points}")
    print(f"  Lines:  (t+1)(st+1) = {expected_lines}")
    print(f"W33 has: {n_points} points, {n_lines} lines")
    print(f"Match: {expected_points == n_points and expected_lines == n_lines}")

# Check the non-collinearity condition (no triangles)
print()
print("=== Checking for triangles ===")

# Build adjacency
point_to_lines = [set() for _ in range(n_points)]
for line_idx, pts in enumerate(lines):
    for p in pts:
        point_to_lines[p].add(line_idx)

# Check if any three points form a triangle
# (mutually collinear but not all on the same line)
triangle_count = 0
for line_idx, pts in enumerate(lines):
    pts_list = list(pts)
    for i in range(len(pts_list)):
        for j in range(i+1, len(pts_list)):
            for k in range(j+1, len(pts_list)):
                # These three are collinear (on this line)
                # Check if any two are on another common line
                p1, p2, p3 = pts_list[i], pts_list[j], pts_list[k]
                common_12 = point_to_lines[p1] & point_to_lines[p2]
                common_23 = point_to_lines[p2] & point_to_lines[p3]
                common_13 = point_to_lines[p1] & point_to_lines[p3]
                
                # They should share exactly one line (this one)
                if len(common_12) > 1 or len(common_23) > 1 or len(common_13) > 1:
                    triangle_count += 1

print(f"Potential triangle issues: {triangle_count}")

# Check GQ axiom: two non-collinear points have exactly one common neighbor
print()
print("=== Checking GQ axiom (non-collinear points) ===")

# Build collinearity relation
collinear = [[False]*n_points for _ in range(n_points)]
for line_idx, pts in enumerate(lines):
    for p1 in pts:
        for p2 in pts:
            collinear[p1][p2] = True

# For non-collinear pairs, count common neighbors
common_neighbor_counts = {}
for p1 in range(n_points):
    for p2 in range(p1+1, n_points):
        if not collinear[p1][p2]:
            # Count common neighbors (points collinear to both)
            common = sum(1 for q in range(n_points) if collinear[p1][q] and collinear[p2][q] and q != p1 and q != p2)
            if common not in common_neighbor_counts:
                common_neighbor_counts[common] = 0
            common_neighbor_counts[common] += 1

print("Distribution of common neighbors for non-collinear pairs:")
for cnt, freq in sorted(common_neighbor_counts.items()):
    print(f"  {cnt} common neighbors: {freq} pairs")

# GQ axiom requires exactly 1 common neighbor
if common_neighbor_counts == {1: sum(common_neighbor_counts.values())}:
    print("\n★ W33 IS a Generalized Quadrangle! ★")
else:
    print("\nW33 is NOT a generalized quadrangle (GQ axiom fails)")

# Let's also check the dual
print()
print("=== W33 Dual Structure ===")
print("W33 is self-dual (40 points ↔ 40 lines)")
print("The automorphism group O(5,3):C2 likely includes a polarity (duality)")

# Check if there's an element that swaps points and lines
generators_data = data["incidence"]["generators"]
print()
print("Looking for polarity in generators...")
for i, gen in enumerate(generators_data):
    pts = gen["points"]
    lns = gen["lines"]
    # A polarity would swap the role of points and lines
    # Hard to detect directly, but we can check if any generator
    # induces a similar permutation on both
    if pts == lns:
        print(f"Generator {i}: acts identically on points and lines (possible polarity component)")
