#!/usr/bin/env python3
"""BT986 — Edgewise Regge curvature convergence proxy on S^2."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class SphereMesh:
    verts: list[tuple[float, float, float]]
    tris: list[tuple[int, int, int]]

    def edgewise_project(self) -> "SphereMesh":
        verts = [np.array(v, dtype=float) for v in self.verts]
        mids: dict[tuple[int, int], int] = {}

        def mid(a: int, b: int) -> int:
            key = (a, b) if a < b else (b, a)
            if key not in mids:
                x = (verts[a] + verts[b]) / 2.0
                verts.append(x / np.linalg.norm(x))
                mids[key] = len(verts) - 1
            return mids[key]

        out = []
        for a, b, c in self.tris:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            out.extend([(a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca)])
        return SphereMesh([tuple(v) for v in verts], out)


def octahedron() -> SphereMesh:
    verts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    tris = [(4, 0, 2), (4, 2, 1), (4, 1, 3), (4, 3, 0),
            (5, 2, 0), (5, 1, 2), (5, 3, 1), (5, 0, 3)]
    return SphereMesh(verts, tris)


def angle_at(p, q, r) -> float:
    p, q, r = np.array(p), np.array(q), np.array(r)
    u, v = q - p, r - p
    c = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    return math.acos(max(-1.0, min(1.0, c)))


def tri_area(p, q, r) -> float:
    p, q, r = np.array(p), np.array(q), np.array(r)
    return float(np.linalg.norm(np.cross(q - p, r - p)) / 2.0)


def metrics(mesh: SphereMesh) -> dict:
    n = len(mesh.verts)
    angle_sum = [0.0] * n
    min_angle = math.pi
    area = 0.0
    for a, b, c in mesh.tris:
        p, q, r = mesh.verts[a], mesh.verts[b], mesh.verts[c]
        area += tri_area(p, q, r)
        angles = [angle_at(p, q, r), angle_at(q, p, r), angle_at(r, p, q)]
        for idx, ang in zip((a, b, c), angles):
            angle_sum[idx] += ang
        min_angle = min(min_angle, *angles)
    deficits = [2 * math.pi - s for s in angle_sum]
    total_deficit = sum(deficits)
    scalar_regge = 2 * total_deficit
    return {
        "num_vertices": n,
        "num_triangles": len(mesh.tris),
        "min_angle_deg": math.degrees(min_angle),
        "area": area,
        "area_rel_error_vs_4pi": abs(area - 4 * math.pi) / (4 * math.pi),
        "total_deficit": total_deficit,
        "total_deficit_rel_error_vs_4pi": abs(total_deficit - 4 * math.pi) / (4 * math.pi),
        "scalar_regge_integral": scalar_regge,
        "scalar_regge_rel_error_vs_8pi": abs(scalar_regge - 8 * math.pi) / (8 * math.pi),
        "max_abs_deficit": max(abs(d) for d in deficits),
        "deficit_l2": math.sqrt(sum(d * d for d in deficits)),
    }


def main() -> None:
    mesh = octahedron()
    rows = []
    for level in range(7):
        if level > 0:
            mesh = mesh.edgewise_project()
        rows.append({"level": level, **metrics(mesh)})
    out = {
        "theorem": "BT986 edgewise Regge curvature convergence proxy on S2",
        "smooth_targets": {"area": 4 * math.pi, "total_deficit": 4 * math.pi, "scalar_curvature_integral": 8 * math.pi},
        "levels": rows,
        "reading": "Projected edgewise refinement keeps fatness near 45 degrees, area converges to 4pi, and Regge scalar curvature 2*sum(deficits) remains 8pi to roundoff while local deficits decay.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt986_edgewise_regge_sphere_convergence.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    for r in rows:
        print(r["level"], r["num_vertices"], r["num_triangles"], r["min_angle_deg"], r["area_rel_error_vs_4pi"], r["scalar_regge_rel_error_vs_8pi"], r["max_abs_deficit"])
    print("wrote data/bt986_edgewise_regge_sphere_convergence.json")


if __name__ == "__main__":
    main()
