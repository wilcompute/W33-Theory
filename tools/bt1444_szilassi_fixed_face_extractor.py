#!/usr/bin/env python3
"""BT1444: extract the fixed Szilassi face from actual realization data."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
OUT = ROOT / "data" / "bt1444_szilassi_fixed_face_extractor.json"


def parse_szilassi_blocks():
    txt = DATA.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=(?:Csaszar|Szilassi) Polyhedron \(version \d\))", txt)
    out = []
    for b in blocks:
        m = re.match(r"(Csaszar|Szilassi) Polyhedron \(version (\d)\)", b)
        if not m or m.group(1) != "Szilassi":
            continue
        version = int(m.group(2))
        consts = {}
        for cm in re.finditer(r"^([A-Z]\d*)\s*=\s*([0-9.]+)", b, re.M):
            consts[cm.group(1)] = float(cm.group(2))
        verts = {}
        for vm in re.finditer(r"^V(\d+)\s*=\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)", b, re.M):
            idx = int(vm.group(1))
            coords = []
            for tok in vm.group(2, 3, 4):
                tok = tok.strip()
                neg = tok.startswith("-")
                core = tok.lstrip("+-").strip()
                val = consts.get(core, float(core) if core not in consts else consts[core])
                coords.append(-val if neg else val)
            verts[idx] = tuple(coords)
        faces = [[int(x) for x in fm.group(1).split(",")] for fm in re.finditer(r"\{([^}]+)\}", b.split("Faces:")[-1])]
        out.append({"version": version, "vertices": verts, "faces": faces})
    return out


def rz_half_turn(v):
    x, y, z = v
    return (-x, -y, z)


def find_partner(target, verts, tol=1e-9):
    for idx, v in verts.items():
        if all(abs(a - b) < tol for a, b in zip(target, v)):
            return idx
    raise ValueError((target, verts))


def cyclic_shift_amount(a, b):
    if len(a) != len(b):
        return None
    n = len(a)
    for s in range(n):
        if a[s:] + a[:s] == b:
            return s
    return None


def main():
    rows = []
    for d in parse_szilassi_blocks():
        verts = d["vertices"]
        faces = d["faces"]
        vmap = {i: find_partner(rz_half_turn(v), verts) for i, v in verts.items()}
        face_sets = [set(f) for f in faces]
        face_map = []
        fixed = []
        for i, f in enumerate(faces):
            image = {vmap[x] for x in f}
            j = next(k for k, fs in enumerate(face_sets) if fs == image)
            face_map.append(j)
            if j == i:
                fixed.append(i)
        if len(fixed) != 1:
            raise AssertionError((d["version"], fixed))
        idx = fixed[0]
        fixed_face = faces[idx]
        image_order = [vmap[x] for x in fixed_face]
        shift = cyclic_shift_amount(fixed_face, image_order)
        centroid = [sum(verts[i][c] for i in fixed_face) / len(fixed_face) for c in range(3)]
        rows.append({
            "version": d["version"],
            "vertex_map": {str(k): v for k, v in sorted(vmap.items())},
            "face_map": face_map,
            "fixed_face_index": idx,
            "fixed_face_vertices": fixed_face,
            "fixed_face_image_order": image_order,
            "boundary_cyclic_shift": shift,
            "centroid": centroid,
            "fixed_face_z_values": sorted({round(verts[i][2], 10) for i in fixed_face}),
        })
    checks = {
        "two_szilassi_realizations": len(rows) == 2,
        "same_fixed_face_index": sorted({r["fixed_face_index"] for r in rows}) == [4],
        "same_fixed_face_vertices": all(r["fixed_face_vertices"] == [11, 9, 12, 10, 8, 13] for r in rows),
        "face_orbits_are_2_2_2_1": all(sorted([len({i, r["face_map"][i]}) for i in range(7)]) == [1, 2, 2, 2, 2, 2, 2] for r in rows),
        "boundary_shift_is_three": all(r["boundary_cyclic_shift"] == 3 for r in rows),
        "centroids_on_rotation_axis": all(abs(r["centroid"][0]) < 1e-9 and abs(r["centroid"][1]) < 1e-9 for r in rows),
    }
    result = {
        "bt": 1444,
        "title": "Szilassi fixed-face extractor",
        "verified": all(checks.values()),
        "rotation": "R(x,y,z)=(-x,-y,z)",
        "realizations": rows,
        "interpretation": "Both Szilassi realizations have a unique fixed hexagon under the coordinate C2 symmetry; the boundary maps to itself by a shift of three vertices.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1444, "verified": result["verified"], "fixed_face": rows[0]["fixed_face_vertices"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
