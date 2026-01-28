#!/usr/bin/env python3
"""Compare Coxeter-6 orbit phases to F3^4 phase assignment.

We take the canonical Z3 phase on W33 vertices (x4 coordinate), and map each
vertex to its E8 Coxeter-6 orbit. For each orbit, we compute the multiset of
root indices modulo 3 (0..5 index in orbit) and compare to the vertex phase.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    return proj_points


def main():
    # Coxeter orbits
    cox = json.loads((ROOT / 'artifacts' / 'e8_coxeter6_orbits.json').read_text())
    orbits = cox['orbits']

    # W33 vertex -> orbit map
    orb_map = json.loads((ROOT / 'artifacts' / 'e8_root_to_w33_edge.json').read_text())
    orbit_to_w33 = {int(k): int(v) for k, v in orb_map['orbit_to_w33_vertex'].items()}
    w33_to_orbit = {v: k for k, v in orbit_to_w33.items()}

    # W33 projective points
    points = build_w33()

    # vertex phase = x4
    v_phase = {i: points[i][3] % 3 for i in range(len(points))}

    # analyze each orbit
    orbit_phase_summary = {}
    for oi, orbit in enumerate(orbits):
        v = orbit_to_w33[oi]
        phase = v_phase[v]
        idx_mod3 = [i % 3 for i in range(len(orbit))]  # fixed 0..5
        cnt = Counter(idx_mod3)
        orbit_phase_summary[oi] = {
            'vertex_phase': phase,
            'root_index_mod3_counts': dict(cnt)
        }

    # aggregate counts per vertex phase
    phase_to_orbit_counts = defaultdict(list)
    for oi, info in orbit_phase_summary.items():
        phase_to_orbit_counts[info['vertex_phase']].append(info['root_index_mod3_counts'])

    results = {
        'orbit_phase_summary': orbit_phase_summary,
        'phase_to_orbit_counts': {k: v for k, v in phase_to_orbit_counts.items()},
    }

    out_path = ROOT / 'artifacts' / 'e8_coxeter_phase_vs_f3.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print({k: len(v) for k,v in phase_to_orbit_counts.items()})
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    main()
