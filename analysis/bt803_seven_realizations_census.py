#!/usr/bin/env python3
"""
BT803 - The seven realizations: exact census of the Csaszar/Szilassi data.

data/Toroidal-Polyhedra-Realizations.txt holds 5 Csaszar + 2 Szilassi
geometric realizations = 7 total realizations of the two genus-1
seven-objects (7 vertices / 7 faces).  BT803 machine-verifies the dataset
and proves the structure theorems around it.

  T1. Parse all 7 realizations; verify V - E + F = 0 (genus 1), edge count
      21 = q * Phi6 each, face sizes (14 triangles / 7 hexagons).
  T2. The combinatorial automorphism group of the 7-vertex Moebius torus
      is the Frobenius group F42 = Z7 : Z6 of order 42 = lambda*q*Phi6
      (computed by brute force over S7); the Szilassi complex is its dual
      (same group).
  T3. SYMMETRY BREAKING THEOREM: every one of the 7 geometric realizations
      retains EXACTLY C2 of the 42 combinatorial symmetries (distance-
      matrix test over all automorphisms).  Breaking index = 42/2 = 21
      = the edge count: geometry pays one symmetry per edge.
  T4. Exact volumes via the divergence theorem (fan-triangulated faces),
      matched against the stated closed forms:
        C1: 125 = F_5^3 (EXACT, rational!)   C2: 16(21 sqrt15 - 2)
        C3: 72(11 - 2 sqrt2)   C4: 2644 sqrt2 / 3   C5: 816 sqrt2
        S1: 5226/5             S2: 7976/9
      Volume number fields: {Q, Q(sqrt15), Q(sqrt2) x3, Q, Q}.
  T5. Szilassi face planarity verified EXACTLY (rational coordinates,
      Fraction arithmetic: every hexagon has affine rank 2).
  T6. Census table: distinct edge lengths per realization
      (10,9,9,8,9 | 12,11); all seven have C2 with one fixed vertex
      (Csaszar) / no fixed vertex (Szilassi, free pairing 7x2=14).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
import json
import math
import re

import numpy as np


def parse_dataset(path):
    txt = open(path, encoding="utf-8").read()
    blocks = re.split(r"\n(?=(?:Csaszar|Szilassi) Polyhedron \(version \d\))",
                      txt)
    out = []
    for b in blocks:
        m = re.match(r"(Csaszar|Szilassi) Polyhedron \(version (\d)\)", b)
        if not m:
            continue
        kind, ver = m.group(1), int(m.group(2))
        consts = {}
        for cm in re.finditer(r"^([A-Z]\d*)\s*=\s*([0-9.]+)", b, re.M):
            name, val = cm.group(1), cm.group(2)
            if name.startswith("V"):
                continue
            consts[name] = float(val)
        if kind == "Csaszar" and ver == 3 and "C0" not in consts:
            # Dataset omission: C0 is used but never defined in version 3.
            # Inferred from the edge table: 2*C0 = 12*sqrt(2) (edge 7) and
            # V0V6 = sqrt(144 + 4 C0^2) = 12*sqrt(3) (edge 8) both force
            # C0 = 6*sqrt(2).  The exact volume check validates this.
            consts["C0"] = 6 * math.sqrt(2)
        verts = {}
        for vm in re.finditer(
                r"^V(\d+)\s*=\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)",
                b, re.M):
            idx = int(vm.group(1))
            coords = []
            for tok in vm.group(2, 3, 4):
                tok = tok.strip()
                neg = tok.startswith("-")
                core = tok.lstrip("+-").strip()
                if core in consts:
                    v = consts[core]
                else:
                    v = float(core)
                coords.append(-v if neg else v)
            verts[idx] = tuple(coords)
        faces = []
        fsec = b.split("Faces:")[-1]
        for fm in re.finditer(r"\{([^}]+)\}", fsec):
            faces.append([int(x) for x in fm.group(1).split(",")])
        vol_m = re.search(r"^Volume:\s*([^\n]+)$", b, re.M)
        out.append(dict(kind=kind, version=ver, consts=consts,
                        vertices=[verts[i] for i in sorted(verts)],
                        faces=faces, volume_str=vol_m.group(1).strip()))
    return out


def edges_of(faces):
    es = set()
    for f in faces:
        m = len(f)
        for i in range(m):
            es.add(frozenset((f[i], f[(i + 1) % m])))
    return es


def signed_volume(verts, faces):
    """Divergence theorem with fan triangulation; orientation-consistent
    faces assumed; return |volume|."""
    tot = 0.0
    for f in faces:
        v0 = np.array(verts[f[0]])
        for i in range(1, len(f) - 1):
            v1 = np.array(verts[f[i]])
            v2 = np.array(verts[f[i + 1]])
            tot += np.dot(v0, np.cross(v1, v2))
    return abs(tot) / 6.0


def main():
    data = parse_dataset("data/Toroidal-Polyhedra-Realizations.txt")
    assert len(data) == 7
    n_cs = sum(1 for d in data if d["kind"] == "Csaszar")
    n_sz = sum(1 for d in data if d["kind"] == "Szilassi")
    print(f"T1 parsed {n_cs} Csaszar + {n_sz} Szilassi = 7 realizations")
    assert (n_cs, n_sz) == (5, 2)

    for d in data:
        V = len(d["vertices"])
        F = len(d["faces"])
        E = len(edges_of(d["faces"]))
        assert E == 21, (d["kind"], d["version"], E)
        assert V - E + F == 0
        if d["kind"] == "Csaszar":
            assert (V, F) == (7, 14)
            assert all(len(f) == 3 for f in d["faces"])
        else:
            assert (V, F) == (14, 7)
            assert all(len(f) == 6 for f in d["faces"])
    print("T1 all 7: V-E+F = 0 (genus 1), 21 = q*Phi6 edges each  PASS")

    # ---- T2: combinatorial automorphisms of the Csaszar complex ----------
    cs = next(d for d in data if d["kind"] == "Csaszar" and d["version"] == 1)
    face_set = {frozenset(f) for f in cs["faces"]}
    autos = []
    for p in permutations(range(7)):
        if all(frozenset(p[x] for x in f) in face_set for f in face_set):
            autos.append(p)
    print(f"T2 |Aut(Moebius 7-torus)| = {len(autos)} "
          f"(expect 42 = lambda*q*Phi6, Frobenius Z7:Z6)")
    assert len(autos) == 42
    orders = Counter()
    ident = tuple(range(7))
    for p in autos:
        o, cur = 1, p
        while cur != ident:
            cur = tuple(p[cur[i]] for i in range(7))
            o += 1
        orders[o] += 1
    print(f"T2 element orders: {dict(sorted(orders.items()))} "
          f"(Frobenius Z7:Z6 profile)")

    # ---- T3: geometric symmetry = exactly C2 ------------------------------
    def geo_sym_count(d):
        verts = d["vertices"]
        n = len(verts)
        dist = [[round(math.dist(verts[i], verts[j]), 6) for j in range(n)]
                for i in range(n)]
        fs = {frozenset(f) for f in d["faces"]}
        count = 0
        fixed = []
        # combinatorial autos of THIS complex
        if n == 7:
            perms = permutations(range(7))
        else:
            # Szilassi: use edge graph automorphisms via distance filter
            # (brute 14! impossible; filter by distance profile rows)
            profs = defaultdict(list)
            for i in range(n):
                profs[tuple(sorted(dist[i]))].append(i)
            # backtracking on distance-matrix isomorphism
            perms = None
        if perms is not None:
            for p in perms:
                if not all(frozenset(p[x] for x in f) in fs for f in fs):
                    continue
                if all(dist[p[i]][p[j]] == dist[i][j]
                       for i in range(n) for j in range(i + 1, n)):
                    count += 1
                    fixed.append(sum(1 for i in range(n) if p[i] == i))
            return count, fixed
        # Szilassi backtracking
        sols = []

        def bt(mapping, used):
            i = len(mapping)
            if i == n:
                p = tuple(mapping)
                if all(frozenset(p[x] for x in f) in fs for f in fs):
                    sols.append(p)
                return
            for j in range(n):
                if j in used:
                    continue
                ok = all(dist[i][k] == dist[j][mapping[k]]
                         for k in range(i))
                if ok:
                    bt(mapping + [j], used | {j})
        bt([], set())
        return len(sols), [sum(1 for i in range(n) if p[i] == i)
                           for p in sols]

    breaking = {}
    for d in data:
        cnt, fixed = geo_sym_count(d)
        tag = f"{d['kind'][0]}{d['version']}"
        breaking[tag] = cnt
        print(f"T3 {tag}: geometric symmetries = {cnt} "
              f"(fixed-vertex counts {sorted(fixed)})")
        assert cnt == 2
    print("T3 SYMMETRY BREAKING: all 7 realizations keep exactly C2 of the")
    print("   42 combinatorial symmetries; index 21 = edge count  PASS")

    # ---- T4: exact volumes -------------------------------------------------
    expected = {
        ("Csaszar", 1): 125.0,
        ("Csaszar", 2): 16 * (21 * math.sqrt(15) - 2),
        ("Csaszar", 3): 72 * (11 - 2 * math.sqrt(2)),
        ("Csaszar", 4): 2644 * math.sqrt(2) / 3,
        ("Csaszar", 5): 816 * math.sqrt(2),
        ("Szilassi", 1): 5226 / 5,
        ("Szilassi", 2): 7976 / 9,
    }
    for d in data:
        vol = signed_volume(d["vertices"], d["faces"])
        exp = expected[(d["kind"], d["version"])]
        rel = abs(vol - exp) / exp
        tag = f"{d['kind'][0]}{d['version']}"
        print(f"T4 {tag}: volume = {vol:.6f} vs stated {exp:.6f} "
              f"(rel err {rel:.2e})")
        assert rel < 1e-9, (tag, vol, exp)
    print("T4 all stated closed-form volumes verified; vol(C1) = 125 = F_5^3")

    # ---- T5: exact Szilassi planarity --------------------------------------
    for d in data:
        if d["kind"] != "Szilassi":
            continue
        verts = [tuple(Fraction(x).limit_denominator(10**6) for x in v)
                 for v in d["vertices"]]
        for f in d["faces"]:
            p0 = verts[f[0]]
            vecs = [tuple(verts[i][k] - p0[k] for k in range(3))
                    for i in f[1:]]
            # affine rank must be 2: all 3x3 determinants vanish
            for a, b, c in combinations(range(len(vecs)), 3):
                M = [vecs[a], vecs[b], vecs[c]]
                det = (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
                       - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
                       + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
                assert det == 0, (d["version"], f)
        print(f"T5 Szilassi v{d['version']}: all 7 hexagons EXACTLY planar "
              f"(Fraction determinants)  PASS")

    # ---- T6: census ---------------------------------------------------------
    census = {}
    for d in data:
        verts = d["vertices"]
        lens = sorted({round(math.dist(verts[i], verts[j]), 6)
                       for e in edges_of(d["faces"]) for i, j in [tuple(e)]})
        tag = f"{d['kind'][0]}{d['version']}"
        census[tag] = len(lens)
    print(f"T6 distinct edge lengths: {census}")
    assert census == {"C1": 10, "C2": 9, "C3": 9, "C4": 8, "C5": 9,
                      "S1": 12, "S2": 11}

    out = {
        "theorem": "BT803 seven realizations census",
        "realizations": "5 Csaszar + 2 Szilassi = 7",
        "aut_order": 42,
        "aut_structure": "Frobenius Z7:Z6 = lambda*q*Phi6",
        "geometric_symmetry": "C2 for all 7 (index 21 = edges)",
        "volumes_verified": {f"{k[0][0]}{k[1]}": v
                             for k, v in expected.items()},
        "vol_C1": "125 = F_5^3 exact",
        "volume_fields": "Q, Q(sqrt15), Q(sqrt2), Q(sqrt2), Q(sqrt2), Q, Q",
        "distinct_edge_lengths": census,
        "szilassi_hexagons_exactly_planar": True,
    }
    with open("data/bt803_seven_realizations_census.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt803_seven_realizations_census.json")


if __name__ == "__main__":
    main()
