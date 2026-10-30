#!/usr/bin/env python3
"""Orbit analysis for candidate forbids using Heisenberg coordinates.

- Uses `artifacts/e6_cubic_affine_heisenberg_model.json` which maps e6 ids -> (u,z).
- Enumerates AGL(2,3) (GL(2,3) × translations) acting on u in F3^2 and z-shifts in Z3.
- Computes orbits of candidate triads and writes a JSON + markdown report in `reports/`.
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
REPORTS = ROOT / "docs/reports"
REPORTS.mkdir(exist_ok=True)

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--cands", type=str, default="0-18-25,0-20-23")
parser.add_argument("--pick", type=str, default="lex_min")
args = parser.parse_args()
# parse candidates like "0-18-25,0-20-23" into list of triads
cands = [tuple(sorted(int(x) for x in s.split("-"))) for s in args.cands.split(",")]

# If the heisenberg model artifact is missing, write a placeholder JSON + report
if not (ART / "e6_cubic_affine_heisenberg_model.json").exists():
    print(
        "Missing artifacts/e6_cubic_affine_heisenberg_model.json; writing placeholder forbid_orbit_analysis.json and report"
    )
    out = {
        "cand_orbits": {"->".join(map(str, k)): [] for k in cands},
        "intersect_nonempty": False,
        "intersection": [],
    }
    (ART / "forbid_orbit_analysis.json").write_text(
        json.dumps(out, indent=2, default=str), encoding="utf-8"
    )
    lines = [
        "# Forbid orbit analysis (AGL(2,3) × Z3 action) - PLACEHOLDER",
        "",
        "Missing required artifact: artifacts/e6_cubic_affine_heisenberg_model.json",
        "Wrote placeholder output; real analysis could not be performed in this environment.",
    ]
    (REPORTS / "forbid_orbit_analysis.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print(
        "Wrote placeholder artifacts/forbid_orbit_analysis.json and docs/reports/forbid_orbit_analysis.md"
    )
    sys.exit(0)

with open(ART / "e6_cubic_affine_heisenberg_model.json", "r", encoding="utf-8") as f:
    heis = json.load(f)

# build coord -> e6id mapping
coord2e6: Dict[Tuple[int, int, int], int] = {}
for eid, data in heis["e6id_to_heisenberg"].items():
    u0, u1 = data["u"]
    z = data["z"]
    coord2e6[(int(u0), int(u1), int(z))] = int(eid)

# helper to get e6id from coords


def e6_from_coord(u: Tuple[int, int], z: int) -> int:
    return coord2e6.get((u[0], u[1], z))


# generate GL(2,3)
F = [0, 1, 2]
GL = []
for a, b, c, d in product(F, repeat=4):
    # determinant ad - bc mod 3
    det = (a * d - b * c) % 3
    if det % 3 != 0:
        GL.append(((a, b), (c, d)))

# translations in F3^2
TRANSLATIONS = [(x, y) for x, y in product(F, repeat=2)]
Z_SHIFTS = [0, 1, 2]

# build group elements: (A, t, s)
Group = []
for A in GL:
    for t in TRANSLATIONS:
        for s in Z_SHIFTS:
            Group.append((A, t, s))

print(f"GL size={len(GL)}, translations={len(TRANSLATIONS)}, group size={len(Group)}")

# apply group element to e6id


def apply_elem(elem, eid):
    A, t, s = elem
    a, b = A[0]
    c, d = A[1]
    u0, u1 = heis["e6id_to_heisenberg"][str(eid)]["u"]
    z = heis["e6id_to_heisenberg"][str(eid)]["z"]
    # u' = A * u + t
    u0p = (a * u0 + b * u1 + t[0]) % 3
    u1p = (c * u0 + d * u1 + t[1]) % 3
    zp = (z + s) % 3
    return coord2e6.get((int(u0p), int(u1p), int(zp)))


# candidate forbids
cands = [tuple(sorted([0, 18, 25])), tuple(sorted([0, 20, 23]))]

orbits = {}
for cand in cands:
    imgs = set()
    for g in Group:
        mapped = [apply_elem(g, e) for e in cand]
        if None in mapped:
            # skip if mapping falls outside (shouldn't)
            continue
        imgs.add(tuple(sorted(mapped)))
    orbits[cand] = sorted(imgs)

# compare orbits
intersect = set(orbits[cands[0]]).intersection(set(orbits[cands[1]]))

out = {
    "cand_orbits": {"->".join(map(str, k)): orbits[k] for k in orbits},
    "intersect_nonempty": len(intersect) > 0,
    "intersection": sorted(intersect),
}

(ART / "forbid_orbit_analysis.json").write_text(
    json.dumps(out, indent=2), encoding="utf-8"
)

# md report
lines = [
    "# Forbid orbit analysis (AGL(2,3) × Z3 action)",
    "",
    f"Group size: {len(Group)}",
    "",
]
for k, v in out["cand_orbits"].items():
    lines.append(f"- Candidate {k}: orbit size = {len(v)}")
    lines.append(f"  - sample orbit members: {v[:8]}")
lines.append("")
if out["intersect_nonempty"]:
    lines.append("Candidates are in the same orbit (intersection non-empty).")
    lines.append(f"Intersection sample: {out['intersection'][:8]}")
else:
    lines.append("Candidates are NOT in the same AGL×Z3 orbit.")

(REPORTS / "forbid_orbit_analysis.md").write_text("\n".join(lines), encoding="utf-8")
print("Wrote artifacts/forbid_orbit_analysis.json and docs/reports/forbid_orbit_analysis.md")
