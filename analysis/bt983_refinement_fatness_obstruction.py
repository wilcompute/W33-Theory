#!/usr/bin/env python3
"""
(R3 attack) The refinement-fatness obstruction and its fix.

The continuum lift (R3) wants the refinement tower's spectral action / Regge
curvature to converge to the smooth Einstein-Hilbert action. The named tools
(Cheeger-Mueller-Schrader curvature convergence; Dodziuk-Patodi /
Whitney-form spectral convergence) REQUIRE a shape-regular ("fat") mesh
sequence: a fatness/min-angle bound away from 0 as the mesh -> 0.

CLAIM (from the literature, verified numerically here): the BARYCENTRIC
refinement tower used in the corpus is NOT shape-regular -- the minimal angle
collapses to 0 -- so CMS/Dodziuk-Patodi do NOT apply to it. The EDGEWISE
(midpoint / Freudenthal-Kuhn) tower IS shape-regular (min angle constant),
so the theorems DO apply. This corrects the route and reduces the gravity
convergence to a known theorem on the fat tower.

We demonstrate on a triangle (2-simplex): track the minimal interior angle
across refinement levels for both schemes.
"""
from __future__ import annotations

import json
import math


def angles(tri):
    """interior angles (degrees) of a triangle given as 3 (x,y) points."""
    (ax, ay), (bx, by), (cx, cy) = tri
    def ang(p, q, r):
        # angle at p
        v1 = (q[0]-p[0], q[1]-p[1])
        v2 = (r[0]-p[0], r[1]-p[1])
        dot = v1[0]*v2[0] + v1[1]*v2[1]
        n1 = math.hypot(*v1)
        n2 = math.hypot(*v2)
        c = max(-1.0, min(1.0, dot/(n1*n2)))
        return math.degrees(math.acos(c))
    A = (ax, ay); B = (bx, by); C = (cx, cy)
    return [ang(A, B, C), ang(B, A, C), ang(C, A, B)]


def mid(p, q):
    return ((p[0]+q[0])/2, (p[1]+q[1])/2)


def centroid(tri):
    return (sum(p[0] for p in tri)/3, sum(p[1] for p in tri)/3)


def barycentric_subdiv(tri):
    """6 triangles: medians (centroid + edge midpoints)."""
    A, B, C = tri
    G = centroid(tri)
    Mab, Mbc, Mca = mid(A, B), mid(B, C), mid(C, A)
    return [(A, Mab, G), (Mab, B, G), (B, Mbc, G),
            (Mbc, C, G), (C, Mca, G), (Mca, A, G)]


def edgewise_subdiv(tri):
    """4 triangles: connect edge midpoints (edgewise k=2 / Freudenthal).
    All 4 children are SIMILAR to the parent -> shape preserved."""
    A, B, C = tri
    Mab, Mbc, Mca = mid(A, B), mid(B, C), mid(C, A)
    return [(A, Mab, Mca), (Mab, B, Mbc), (Mca, Mbc, C), (Mab, Mbc, Mca)]


def min_angle_over_mesh(mesh):
    return min(min(angles(t)) for t in mesh)


def main():
    # start: equilateral triangle (min angle 60 deg)
    seed = [(0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3)/2)]
    LEVELS = 5

    bary = [seed]
    edge = [seed]
    bary_min = [min_angle_over_mesh(bary)]
    edge_min = [min_angle_over_mesh(edge)]
    for _ in range(LEVELS):
        bary = [c for t in bary for c in barycentric_subdiv(t)]
        edge = [c for t in edge for c in edgewise_subdiv(t)]
        bary_min.append(min_angle_over_mesh(bary))
        edge_min.append(min_angle_over_mesh(edge))

    print("level | #tris(bary) min-angle(bary) | #tris(edge) min-angle(edge)")
    nb, ne = 1, 1
    for k in range(LEVELS+1):
        print(f"  {k}   |   {nb:>7}     {bary_min[k]:7.3f}     |   "
              f"{ne:>7}     {edge_min[k]:7.3f}")
        nb *= 6
        ne *= 4

    print()
    print(f"barycentric min angle: {bary_min[0]:.2f} -> {bary_min[-1]:.4f} deg"
          f"  (COLLAPSING to 0 -> NOT shape-regular)")
    print(f"edgewise   min angle: {edge_min[0]:.2f} -> {edge_min[-1]:.4f} deg"
          f"  (CONSTANT -> shape-regular / fat)")
    bary_collapses = bary_min[-1] < 0.5 * bary_min[0]
    edge_constant = abs(edge_min[-1] - edge_min[0]) < 1e-6
    print()
    print("CONCLUSION:")
    print(" - Barycentric tower violates the CMS / Dodziuk-Patodi fatness")
    print("   hypothesis (min angle -> 0): those convergence theorems do NOT")
    print("   apply to it.")
    print(" - Edgewise (Freudenthal-Kuhn) tower keeps fatness bounded: the")
    print("   hypotheses HOLD, so CMS gives Regge-curvature -> integral R, and")
    print("   Dodziuk-Patodi gives combinatorial -> de Rham spectrum.")
    print(" - The EH term of the spectral action = a_2 ~ integral R = the")
    print("   Regge deficit-angle action; on the fat tower its convergence is")
    print("   the Cheeger-Mueller-Schrader theorem, not an open problem.")

    out = {
        "theorem": "(R3) refinement-fatness obstruction + edgewise fix",
        "barycentric_min_angle_by_level": [round(x, 4) for x in bary_min],
        "edgewise_min_angle_by_level": [round(x, 4) for x in edge_min],
        "barycentric_collapses": bool(bary_collapses),
        "edgewise_shape_regular": bool(edge_constant),
        "reading": ("barycentric tower fails CMS/Dodziuk-Patodi fatness; "
                    "edgewise/Freudenthal-Kuhn tower satisfies it, reducing "
                    "the EH (a_2 ~ int R = Regge) convergence to CMS."),
    }
    with open("data/bt983_refinement_fatness_obstruction.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt983_refinement_fatness_obstruction.json")


if __name__ == "__main__":
    main()
