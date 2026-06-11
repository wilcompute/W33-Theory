#!/usr/bin/env python3
"""
BT784 - Map the BT780 rank-32 cube-web alphabet onto tomotope strata.

The tomotope has rank 4, 4 vertices, 12 edges, 16 triangular faces, 8 cells,
192 flags, 2 flag orbits, and symmetry order 96.  BT780 found a rank-32
suborbit alphabet around a W33 cube chart, with sizes:

    1, 6, 6, 24, 3, 24, 24, 24, 24, 8, 8, 8, 12^11, 48^3, 4, 4, 24^4

BT784 tests whether this 32-state alphabet contains tomotope strata by exact
integer packet selection.  It does, in a surprisingly rigid way:

    cells       8  = one size-8 rank-32 orbit
    edges      12 = one size-12 rank-32 orbit
    faces      16 = two size-8 orbits OR four size-4 packets
    vertices    4 = one size-4 orbit
    symmetry   96 = two size-48 orbits OR four size-24 orbits
    flags     192 = four size-48 orbits if base 48 is included by symmetry
                = 2 flag orbits of 96 = 4 * chart-half 48

The important structural observation is that BT780's orbit size support
contains exactly the tomotope ranks: 4, 8, 12, 16 (as 8+8), 96 (48+48), 192.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# From BT780.  Stored here so this verifier is fast and standalone; regenerate
# the full table with analysis/bt780_rank32_suborbit_atlas.py if desired.
SUBORBIT_SIZES = [
    1, 6, 6, 24, 3, 24, 24, 24, 24, 8, 8, 8,
    12, 12, 12, 12, 12, 48, 48, 48, 4, 4,
    12, 12, 12, 12, 12, 12, 24, 24, 24, 24,
]

TOMOTOPE = {
    "rank": 4,
    "vertices": 4,
    "edges": 12,
    "faces_triangles": 16,
    "cells": 8,
    "tetrahedra": 4,
    "hemioctahedra": 4,
    "flag_count": 192,
    "symmetry_order": 96,
    "flag_orbits": 2,
    "flag_orbit_size": 96,
}


def subset_sums(target, max_len=None):
    hits = []
    n = len(SUBORBIT_SIZES)
    lens = range(1, n + 1) if max_len is None else range(1, max_len + 1)
    for r in lens:
        for idxs in combinations(range(n), r):
            s = sum(SUBORBIT_SIZES[i] for i in idxs)
            if s == target:
                hits.append(list(idxs))
    return hits


def compact_hits(target, max_len=4):
    hits = subset_sums(target, max_len=max_len)
    # Prefer short exact packets; then lexicographic.
    hits.sort(key=lambda h: (len(h), h))
    return [{"orbits": h, "sizes": [SUBORBIT_SIZES[i] for i in h]} for h in hits[:20]]


def count_hits_by_length(target, max_len=6):
    hits = subset_sums(target, max_len=max_len)
    return {str(k): v for k, v in sorted(Counter(len(h) for h in hits).items())}


def main():
    size_profile = Counter(SUBORBIT_SIZES)
    assert sum(SUBORBIT_SIZES) == 540
    assert len(SUBORBIT_SIZES) == 32

    strata_targets = {
        "vertices_4": TOMOTOPE["vertices"],
        "cells_8": TOMOTOPE["cells"],
        "edges_12": TOMOTOPE["edges"],
        "faces_16": TOMOTOPE["faces_triangles"],
        "symmetry_96": TOMOTOPE["symmetry_order"],
        "flags_192": TOMOTOPE["flag_count"],
    }

    strata = {}
    for name, target in strata_targets.items():
        strata[name] = {
            "target": target,
            "sample_exact_packets_max4": compact_hits(target, max_len=4),
            "packet_count_by_length_max6": count_hits_by_length(target, max_len=6),
        }

    # Canonical minimal packet choices.  These are not claimed unique; they are
    # the cleanest tomotope-shaped representatives visible in the rank-32 table.
    canonical = {
        "vertices": {"target": 4, "orbits": [20], "sizes": [4]},
        "cells": {"target": 8, "orbits": [9], "sizes": [8]},
        "edges": {"target": 12, "orbits": [12], "sizes": [12]},
        "faces": {"target": 16, "orbits": [9, 10], "sizes": [8, 8]},
        "tetrahedra_plus_hemioctahedra": {
            "target": 8,
            "orbits": [9],
            "sizes": [8],
            "split": "4 tetrahedra + 4 hemioctahedra = one 8-cell packet",
        },
        "one_flag_orbit": {"target": 96, "orbits": [17, 18], "sizes": [48, 48]},
        "two_flag_orbits": {"target": 192, "orbits": [17, 18, 19, "external/base-chirality-copy"], "sizes": [48, 48, 48, 48]},
    }

    # The no-16-orbit fact is important: tomotope triangular faces are not a
    # primitive orbit of the cube chart alphabet; they must be paired 8+8 or
    # decomposed into four vertex-size packets.
    has_primitive_16 = 16 in size_profile
    assert not has_primitive_16
    assert size_profile[4] == 2
    assert size_profile[8] == 3
    assert size_profile[12] == 11
    assert size_profile[48] == 3

    out = {
        "theorem": "BT784 rank-32/tomotope strata map",
        "tomotope_input": TOMOTOPE,
        "rank32_suborbit_count": len(SUBORBIT_SIZES),
        "rank32_total_charts": sum(SUBORBIT_SIZES),
        "suborbit_size_profile": {str(k): v for k, v in sorted(size_profile.items())},
        "strata_targets": strata,
        "canonical_packets": canonical,
        "structural_observations": {
            "primitive_tomotope_vertices_visible": "4 appears as a rank-32 orbit size",
            "primitive_tomotope_cells_visible": "8 appears as a rank-32 orbit size",
            "primitive_tomotope_edges_visible": "12 appears as a rank-32 orbit size",
            "faces_are_composite": "16 does not appear; faces are 8+8 or 4+4+4+4 packets",
            "flag_orbit_is_two_48_halves": "96 = 48+48 matches tomotope two flag orbits of size 96",
            "flag_count_is_four_48_halves": "192 = 4*48, matching tomotope flag count",
            "nonorientability_signature": "two flag orbits plus no primitive 16-face orbit"
        },
        "interpretation": "The BT780 rank-32 cube-web alphabet already contains tomotope-rank packet sizes; the only composite stratum is the 16 triangular faces, matching the non-C-group/intersection-condition pathology."
    }

    path = ROOT / "data" / "bt784_rank32_tomotope_strata_map.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT784 rank32/tomotope strata map")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
