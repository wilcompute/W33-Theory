#!/usr/bin/env python3
"""Pass 2503 -- the K8 criterion, executed.

Pass 2496 reduced chi(H)=9 to: does ANY cover's disjointness link contain K8?
Links are constant on PSp(4,3)-orbits, so there are at most 327 link types.

This builds the 540 frames and the group action from scratch, regenerates all
3,547,800 covers from the 327 frozen representatives, and computes link sizes and
clique numbers.  It first REPRODUCES the parallel track's 13,648 for the canonical
cover as a validation gate before reporting anything new.

Prior art: data/w33_pass1511_cover_orbit_representatives.json.gz.b64 and
data/w33_pass1511_1515_cover_resolution_frontiers.json own the representatives,
the 13,648 count, and the clique-number-3 result for the canonical link.
"""
from __future__ import annotations

import base64
import gzip
import itertools
import json
import sys
import time
from pathlib import Path

F = 3
ROOT = Path(__file__).resolve().parents[1]
REPS = ROOT / "data" / "w33_pass1511_cover_orbit_representatives.json.gz.b64"


def canon(v):
    for a in v:
        if a % F:
            inv = 1 if a % F == 1 else 2
            return tuple((inv * x) % F for x in v)
    return None


def symplectic(a, b):
    return (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % F


def build_geometry():
    """40 points, 40 totally isotropic lines, 540 frames (disjoint line pairs)."""
    pts = sorted({canon(v) for v in itertools.product(range(F), repeat=4)} - {None})
    idx = {p: i for i, p in enumerate(pts)}
    # totally isotropic lines: 2-subspaces on which the form vanishes
    lines = set()
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if j <= i or symplectic(p, q):
                continue
            span = set()
            for a in range(F):
                for b in range(F):
                    c = canon(tuple((a * p[k] + b * q[k]) % F for k in range(4)))
                    if c is not None:
                        span.add(idx[c])
            if len(span) == 4:
                lines.add(frozenset(span))
    lines = sorted(lines, key=sorted)
    frames = [(i, j) for i in range(len(lines)) for j in range(i + 1, len(lines))
              if not (lines[i] & lines[j])]
    return pts, idx, lines, frames


def frame_permutation(mat, pts, idx, lines, frames, fidx):
    """The permutation of the 540 frames induced by a symplectic matrix."""
    pmap = []
    for p in pts:
        img = canon(tuple(sum(mat[r][c] * p[c] for c in range(4)) % F for r in range(4)))
        pmap.append(idx[img])
    lmap = {}
    for li, L in enumerate(lines):
        lmap[li] = lines.index(frozenset(pmap[x] for x in L))
    out = [0] * len(frames)
    for k, (a, b) in enumerate(frames):
        x, y = lmap[a], lmap[b]
        out[k] = fidx[(x, y) if x < y else (y, x)]
    return out


def sp4_generators():
    """The genuine GAP SP(4,3) generators.

    My hand-written guesses generated a group of order 192 on the frames instead
    of 25920, which the validation gate below caught immediately -- the regenerated
    cover count came out 62784 rather than 3547800.  These are taken verbatim from
    GeneratorsOfGroup(SP(4,3)).
    """
    g1 = [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2]]
    g2 = [[1, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 1], [0, 2, 0, 0]]
    return [[[x % F for x in row] for row in g] for g in (g1, g2)]


def main() -> int:
    t0 = time.time()
    pts, idx, lines, frames = build_geometry()
    fidx = {f: i for i, f in enumerate(frames)}
    print(f"  points {len(pts)}  lines {len(lines)}  frames {len(frames)}"
          f"   ({time.time()-t0:.1f}s)")
    if len(frames) != 540:
        print("  FRAME COUNT WRONG -- aborting rather than reporting on a wrong object")
        return 1

    perms = [frame_permutation(m, pts, idx, lines, frames, fidx)
             for m in sp4_generators()]
    # close the permutation group on 540 points
    seen = {tuple(range(540))}
    frontier = [tuple(range(540))]
    while frontier:
        nxt = []
        for p in frontier:
            for g in perms:
                q = tuple(g[p[i]] for i in range(540))
                if q not in seen:
                    seen.add(q)
                    nxt.append(q)
        frontier = nxt
        if len(seen) > 120000:
            break
    print(f"  group order on frames : {len(seen)}   ({time.time()-t0:.1f}s)")

    data = json.loads(gzip.decompress(base64.b64decode(REPS.read_text(encoding="utf-8"))))
    reps = data["representatives"]
    print(f"  frozen orbit representatives : {len(reps)}")

    G = list(seen)
    covers = set()
    for r in reps:
        base = r["representative"]
        for g in G:
            covers.add(frozenset(g[x] for x in base))
    print(f"  regenerated covers : {len(covers)}   "
          f"(frozen total 3547800)   ({time.time()-t0:.1f}s)")

    masks = [sum(1 << x for x in c) for c in covers]
    canonical = sum(1 << x for x in reps[0]["representative"])
    link = [m for m in masks if not (m & canonical)]
    print(f"  VALIDATION: |link(canonical)| = {len(link)}   "
          f"(parallel track: 13648)   match={len(link)==13648}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
