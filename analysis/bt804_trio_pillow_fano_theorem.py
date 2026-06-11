#!/usr/bin/env python3
"""
BT804 - The Trio Theorem: tetrahedral pillow quotients and the Fano/QR
        decomposition of the Csaszar triple space.

Two exact discoveries about the tetrahedron / Csaszar / Szilassi trio:

  PART 1 (PILLOW).  Every geometric realization keeps exactly C2 (BT803).
  A 180-degree rotation of an embedded torus restricts to an
  orientation-preserving involution of the surface; Riemann-Hurwitz forces
  exactly 4 fixed points (chi(T)=0 = 2*chi(S^2) - #fix => #fix = 4).
  We verify, for all 7 realizations, the fixed-cell census
  (vertices + setwise-fixed edges + setwise-fixed faces with a fixed
  interior point) totals 4, and compute the quotient cell structure:
  the SPHERE with 4 orbifold points - the TETRAHEDRAL PILLOW.  The
  tetrahedron is the ground state h=0; the Csaszar/Szilassi tori are
  its double covers branched over the 4 pillow points.  The trio is one
  object: torus = pillow^2.

  PART 2 (FANO/QR).  Relabel the Csaszar complex to its cyclic Z7 form.
  The 35 triples of Z7 fall into 5 cyclic orbits classified by circular
  gap multisets {1,1,5}, {1,2,4}, {1,4,2}, {1,3,3}, {2,2,3}.  The QR
  difference-set orbit {1,2,4} (= quadratic residues mod 7 = the BT774
  reptend even-position set) is the FANO PLANE; {1,4,2} is its mirror.
  We compute which orbits form the 14 Csaszar faces, whether the Fano
  lines are face-disjoint, and whether the Fano triangles partition the
  21 edges of K7 = the Csaszar 1-skeleton (Steiner system edge split).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations
import json
import math
import re

import numpy as np


# ---------------------------------------------------------------------------
# dataset parsing (same as BT803, with the C0 = 6 sqrt 2 repair)
# ---------------------------------------------------------------------------

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
            if cm.group(1).startswith("V"):
                continue
            consts[cm.group(1)] = float(cm.group(2))
        if kind == "Csaszar" and ver == 3 and "C0" not in consts:
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
                v = consts[core] if core in consts else float(core)
                coords.append(-v if neg else v)
            verts[idx] = tuple(coords)
        faces = []
        for fm in re.finditer(r"\{([^}]+)\}", b.split("Faces:")[-1]):
            faces.append([int(x) for x in fm.group(1).split(",")])
        out.append(dict(kind=kind, version=ver,
                        vertices=[verts[i] for i in sorted(verts)],
                        faces=faces))
    return out


def edges_of(faces):
    es = set()
    for f in faces:
        m = len(f)
        for i in range(m):
            es.add(frozenset((f[i], f[(i + 1) % m])))
    return es


def find_c2(d):
    """Return the nontrivial geometric symmetry (distance-preserving
    combinatorial automorphism)."""
    verts = d["vertices"]
    n = len(verts)
    dist = [[round(math.dist(verts[i], verts[j]), 6) for j in range(n)]
            for i in range(n)]
    fs = {frozenset(f) for f in d["faces"]}
    sols = []

    def bt(mapping, used):
        i = len(mapping)
        if i == n:
            p = tuple(mapping)
            if p != tuple(range(n)) and \
               all(frozenset(p[x] for x in f) in fs for f in fs):
                sols.append(p)
            return
        for j in range(n):
            if j in used:
                continue
            if all(dist[i][k] == dist[j][mapping[k]] for k in range(i)):
                bt(mapping + [j], used | {j})
    bt([], set())
    assert len(sols) == 1
    return sols[0]


def main():
    data = parse_dataset("data/Toroidal-Polyhedra-Realizations.txt")
    assert len(data) == 7

    # ---------------- PART 1: pillow quotients ---------------------------
    print("PART 1: C2 quotients (tetrahedral pillow)")
    pillow = {}
    for d in data:
        g = find_c2(d)
        n = len(d["vertices"])
        fs = {frozenset(f) for f in d["faces"]}
        es = edges_of(d["faces"])
        fix_v = [i for i in range(n) if g[i] == i]
        fix_e = [e for e in es
                 if frozenset(g[x] for x in e) == e and
                 not all(g[x] == x for x in e)]   # swapped endpoints
        fix_f = []
        for f in fs:
            if frozenset(g[x] for x in f) == f:
                # involution on the face with how many fixed vertices?
                k = sum(1 for x in f if g[x] == x)
                fix_f.append((sorted(f), k))
        # surface fixed points: each fixed vertex; each swapped edge's
        # midpoint; each setwise-fixed face contributes a fixed interior
        # point only if the involution acts freely on its vertices
        # (180-degree rotation about the face center).
        interior_face_fix = [f for f, k in fix_f if k == 0]
        # a setwise-fixed triangle with one fixed vertex reflects across a
        # vertex-edge axis: its fixed set is an arc hitting the fixed vertex
        # and the opposite edge midpoint (already counted there).
        total_fix = len(fix_v) + len(fix_e) + len(interior_face_fix)
        tag = f"{d['kind'][0]}{d['version']}"
        # equivariant subdivision: split each swapped edge at its midpoint;
        # fan each freely-rotated fixed face at its center.  After that the
        # involution is good (no setwise-fixed open cells except points)
        # and quotient cells = orbits.
        ef = len(fix_e)
        ff = len(interior_face_fix)
        fsz = {len(next(iter(fs)))}  # face size (3 or 6, uniform)
        s = next(iter(fsz))
        Vq = len(fix_v) + ef + ff + (n - len(fix_v)) // 2
        Eq = (len(es) + ef + s * ff) // 2
        Fq = (len(fs) + (s - 1) * ff) // 2
        chi_q = Vq - Eq + Fq
        pillow[tag] = dict(fix_v=len(fix_v), fix_e=ef, fix_f=ff,
                           total_fix=total_fix,
                           quotient=(Vq, Eq, Fq), chi=chi_q)
        print(f"  {tag}: fixV={len(fix_v)} fixE={ef} fixF(free)={ff} "
              f"total={total_fix} quotient V,E,F={Vq},{Eq},{Fq} "
              f"chi={chi_q}")
        assert total_fix == 4, tag        # Riemann-Hurwitz
        assert chi_q == 2, tag            # quotient is a SPHERE (pillow)
    print("  Riemann-Hurwitz: 4 fixed points on every realization  PASS")
    print("  (quotient = sphere with 4 branch points: the TETRAHEDRAL")
    print("   PILLOW; torus = pillow double cover; chi check: orbit-cell")
    print("   chi = chi(T)/2 + #fix/2 = 0/2 + 2 = 2 with folded cells")
    print("   counted once: V-E+F above is the open-cell orbit count 1 +")
    print("   #fix/2 - 1 ... reported raw)")

    # ---------------- PART 2: Fano / QR decomposition --------------------
    print("\nPART 2: cyclic form + Fano/QR structure")
    cs = next(d for d in data if d["kind"] == "Csaszar" and d["version"] == 1)
    fs = {frozenset(f) for f in cs["faces"]}

    # find a relabeling under which the complex is Z7-cyclic
    cyc = None
    for p in permutations(range(7)):
        relab = {frozenset(p[x] for x in f) for f in fs}
        shift = {frozenset((x + 1) % 7 for x in f) for f in relab}
        if shift == relab:
            cyc = relab
            break
    assert cyc is not None
    print("  cyclic Z7 form found: complex invariant under x -> x+1")

    def gap_class(tri):
        a, b, c = sorted(tri)
        gaps = sorted(((b - a) % 7, (c - b) % 7, (a - c) % 7))
        return tuple(gaps)

    face_classes = Counter(gap_class(f) for f in cyc)
    print(f"  face gap classes: {dict(face_classes)}")

    all_classes = Counter(gap_class(t) for t in combinations(range(7), 3))
    print(f"  all 35 triples by class: {dict(all_classes)}")

    QR = {1, 2, 4}     # quadratic residues mod 7 = Fano difference set
    fano = {frozenset(((0 + s), (1 + s) % 7, (3 + s) % 7)) for s in range(7)}
    fano = {frozenset(x % 7 for x in f) for f in fano}
    assert len(fano) == 7
    fano_classes = Counter(gap_class(f) for f in fano)
    print(f"  Fano lines (diff set {{0,1,3}}, gaps = QR {sorted(QR)}): "
          f"class {dict(fano_classes)}")

    inter = fano & cyc
    print(f"  Fano lines that are Csaszar faces: {len(inter)}")

    # Steiner edge partition: the 7 Fano triangles partition the 21 edges
    edge_cover = Counter()
    for f in fano:
        for e in combinations(sorted(f), 2):
            edge_cover[e] += 1
    print(f"  Fano triangle edge cover of K7: "
          f"{dict(Counter(edge_cover.values()))} (perfect iff all 1)")

    # the mirror Fano
    mirror = {frozenset((-x) % 7 for x in f) for f in fano}
    mirror_classes = Counter(gap_class(f) for f in mirror)
    print(f"  mirror Fano classes: {dict(mirror_classes)}; "
          f"mirror == fano: {mirror == fano}")

    # THE DOUBLE-FANO IDENTITY: faces = Fano u mirror-Fano exactly
    assert cyc == fano | mirror
    assert not (fano & mirror)
    rest = [t for t in (frozenset(t) for t in combinations(range(7), 3))
            if t not in cyc]
    print(f"  DOUBLE-FANO THEOREM: the 14 Csaszar faces = Fano (7) "
          f"DISJOINT-UNION mirror-Fano (7); remaining triples = {len(rest)}"
          f" = 3 x 7 (classes (1,1,5),(1,3,3),(2,2,3))")

    out = {
        "theorem": "BT804 trio pillow + Fano/QR",
        "pillow": pillow,
        "face_gap_classes": {str(k): v for k, v in face_classes.items()},
        "all_classes": {str(k): v for k, v in all_classes.items()},
        "fano_is_face": len(inter),
        "fano_edge_partition": dict(Counter(edge_cover.values())),
        "mirror_equals_fano": mirror == fano,
        "qr_link": "Fano difference gaps {1,2,4} = QR mod 7 = BT774 "
                   "reptend even-position residues",
    }
    with open("data/bt804_trio_pillow_fano_theorem.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt804_trio_pillow_fano_theorem.json")


if __name__ == "__main__":
    main()
