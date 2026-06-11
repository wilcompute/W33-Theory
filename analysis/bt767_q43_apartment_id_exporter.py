#!/usr/bin/env python3
"""BT767 — stable Q(4,3) apartment ID exporter.

BT760 verified the target-side Q(4,3) oriented-apartment mirror harness.
BT767 turns that into a stable serialization layer: canonical apartment IDs,
oriented frame IDs, and mirror-frame IDs.

The exported data is target-side only.  It is necessary but not sufficient for
identifying BT750's r^6 with Pluecker orientation reversal.
"""
from __future__ import annotations

import json
from itertools import product, combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt767_q43_apartment_id_export.json"

F = range(3)


def inv(a):
    return 1 if a == 1 else 2


def norm(v):
    for x in v:
        if x % 3:
            c = inv(x % 3)
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def qform(v):
    return (v[0] * v[1] + v[2] * v[3] + v[4] * v[4]) % 3


def bilinear(u, v):
    return (u[0] * v[1] + v[0] * u[1] + u[2] * v[3] + v[2] * u[3] + 2 * u[4] * v[4]) % 3


def build_q43():
    pts = sorted({norm(v) for v in product(F, repeat=5) if any(v) and qform(v) == 0})
    p_index = {p: i for i, p in enumerate(pts)}
    lines = []
    for a, b in combinations(pts, 2):
        if bilinear(a, b) != 0:
            continue
        span = sorted({norm(tuple((s * a[i] + t * b[i]) % 3 for i in range(5))) for s, t in product(F, repeat=2) if (s, t) != (0, 0)})
        if len(span) == 4 and all(qform(x) == 0 for x in span):
            lines.append(tuple(sorted(p_index[x] for x in span)))
    lines = sorted(set(lines))
    incidences = {i: set() for i in range(len(pts))}
    for li, line in enumerate(lines):
        for p in line:
            incidences[p].add(li)
    return pts, lines, incidences


def oriented_octagons(lines, incidences):
    # Incidence graph nodes are p0..p39 and l0..l39. Enumerate simple 8-cycles
    # alternating p,l,p,l,p,l,p,l, canonicalized up to oriented rotation.
    line_points = [set(x) for x in lines]
    found = set()
    oriented = []
    for p0 in range(40):
        for l0 in sorted(incidences[p0]):
            for p1 in sorted(line_points[l0] - {p0}):
                for l1 in sorted(incidences[p1] - {l0}):
                    for p2 in sorted(line_points[l1] - {p1, p0}):
                        for l2 in sorted(incidences[p2] - {l1, l0}):
                            for p3 in sorted(line_points[l2] - {p2, p1, p0}):
                                for l3 in sorted((incidences[p3] & incidences[p0]) - {l2, l1, l0}):
                                    frame = (f"p{p0}", f"l{l0}", f"p{p1}", f"l{l1}", f"p{p2}", f"l{l2}", f"p{p3}", f"l{l3}")
                                    can = canonical_oriented(frame)
                                    if can not in found:
                                        found.add(can)
                                        oriented.append(can)
    return sorted(oriented)


def rotations(frame):
    t = tuple(frame)
    return [t[i:] + t[:i] for i in range(len(t))]


def canonical_oriented(frame):
    return min(rotations(tuple(frame)))


def canonical_unoriented(frame):
    t = tuple(frame)
    return min(rotations(t) + rotations(tuple(reversed(t))))


def mirror(frame):
    return canonical_oriented(tuple(reversed(frame)))


def main():
    pts, lines, incidences = build_q43()
    oriented = oriented_octagons(lines, incidences)
    by_un = {}
    for frame in oriented:
        by_un.setdefault(canonical_unoriented(frame), []).append(frame)
    records = []
    for ap_idx, un in enumerate(sorted(by_un)):
        frames = sorted(by_un[un])
        for o_idx, frame in enumerate(frames):
            records.append({
                "q43_apartment_id": f"q43_apartment_{ap_idx:04d}",
                "q43_oriented_frame_id": f"q43_apartment_{ap_idx:04d}_ori_{o_idx:02d}",
                "q43_oriented_frame": list(frame),
                "q43_mirror_frame": list(mirror(frame)),
                "q43_unoriented_key": list(un),
            })
    mirror_fixed = sum(1 for r in records if r["q43_oriented_frame"] == r["q43_mirror_frame"])
    summary = {
        "theorem": "BT767 stable Q43 apartment ID exporter",
        "points": len(pts),
        "lines": len(lines),
        "unoriented_apartments": len(by_un),
        "oriented_apartment_frames": len(records),
        "mirror_fixed_oriented_frames": mirror_fixed,
        "checks": {
            "q43_points_40": len(pts) == 40,
            "q43_lines_40": len(lines) == 40,
            "orientation_reversal_fixed_point_free": mirror_fixed == 0,
            "every_unoriented_apartment_has_two_orientations_minimum": all(len(v) >= 2 for v in by_un.values()),
        },
        "boundary": "Target-side stable apartment IDs only. No root-torsor rows are transported here."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"summary": summary, "records": records}, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
