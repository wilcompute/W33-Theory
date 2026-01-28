#!/usr/bin/env python3
"""Overlay Schlaefli triangle partition with balanced-orbit phase/root labels."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def line_key(line):
    # Normalize line tuple to JSON-friendly tuple
    return tuple(line)


def main():
    tri = json.loads((ROOT / 'artifacts' / 'h27_schlafli_triangle_structure.json').read_text())
    triangles = tri['triangles']

    iso = json.loads((ROOT / 'artifacts' / 'balanced_orbit_schlafli_isomorphism.json').read_text())
    mapping_full = iso['mapping_full']

    # Build reverse map: line -> (phase, root_type)
    line_to_info = {}
    for _, info in mapping_full.items():
        line = tuple(info['line'])
        line_to_info[line] = info

    phase_trip_counts = Counter()
    root_trip_counts = Counter()
    line_trip_counts = Counter()

    per_triangle = []
    for tri_lines in triangles:
        lines = [tuple(L) for L in tri_lines]
        phases = []
        roots = []
        types = []
        for L in lines:
            info = line_to_info[L]
            phases.append(int(info['phase']))
            roots.append(info['root_type'])
            types.append(L[0])
        phase_trip = tuple(sorted(phases))
        root_trip = tuple(sorted(roots))
        line_trip = tuple(sorted(types))
        phase_trip_counts[phase_trip] += 1
        root_trip_counts[root_trip] += 1
        line_trip_counts[line_trip] += 1
        per_triangle.append({
            "lines": lines,
            "phases": phases,
            "root_types": roots,
            "line_types": types,
        })

    results = {
        "phase_trip_counts": {str(k): v for k, v in sorted(phase_trip_counts.items())},
        "root_trip_counts": {str(k): v for k, v in sorted(root_trip_counts.items())},
        "line_trip_counts": {str(k): v for k, v in sorted(line_trip_counts.items())},
        "triangles": per_triangle,
    }

    out_path = ROOT / 'artifacts' / 'balanced_triangle_phase_alignment.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
