#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1652_fano_gauge_untwister.json'
MD = ROOT / 'analysis' / 'BT1652_fano_gauge_untwister.md'
TEX = ROOT / 'analysis' / 'BT1652_fano_gauge_untwister.tex'

POINT_MASS = [240, 232, 224, 232, 224, 224, 224]
TOTAL = sum(POINT_MASS)
POINTS = 7
LOWER = TOTAL // POINTS
UPPER = LOWER + 1

# Nonzero vectors in F_2^3 label Fano points 1..7.
VECTORS = [(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1) if (a,b,c) != (0,0,0)]
INDEX = {v: i for i, v in enumerate(VECTORS)}

def mat_mul_vec(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(3)) % 2 for i in range(3))

def det2(M):
    # determinant over F2 by permutation expansion.
    total = 0
    for p in itertools.permutations(range(3)):
        prod = 1
        for i,j in enumerate(p):
            prod &= M[i][j]
        total ^= prod
    return total

def gl32_permutations():
    perms = []
    for entries in itertools.product((0,1), repeat=9):
        M = [list(entries[i*3:(i+1)*3]) for i in range(3)]
        if det2(M) != 1:
            continue
        perm = [INDEX[mat_mul_vec(M, v)] for v in VECTORS]
        perms.append(tuple(perm))
    return sorted(set(perms))

def main() -> None:
    gauges = gl32_permutations()
    masses = []
    for perm in gauges:
        # New point i receives old point perm[i].
        masses.append(tuple(POINT_MASS[perm[i]] for i in range(POINTS)))
    histograms = Counter(tuple(sorted(m)) for m in masses)
    spans = Counter(max(m)-min(m) for m in masses)
    l1_tilts = Counter(sum(abs(x - TOTAL/POINTS) for x in m) for m in masses)
    balanced_target = tuple([LOWER]*(POINTS-(TOTAL-LOWER*POINTS)) + [UPPER]*(TOTAL-LOWER*POINTS))
    near_balanced_exists = any(sorted(m) == list(balanced_target) for m in masses)
    checks = {
        'fano_gauge_count_168': len(gauges) == 168,
        'total_1600': TOTAL == 1600,
        'all_gauges_preserve_mass_multiset': len(histograms) == 1,
        'all_spans_are_16': spans == {16:168},
        'near_balanced_228_229_absent': not near_balanced_exists,
        'point_mass_histogram_224x4_232x2_240x1': Counter(POINT_MASS) == {224:4, 232:2, 240:1},
    }
    result = {
        'bt': 1652,
        'title': 'Fano gauge untwister',
        'verified': all(checks.values()),
        'source': 'data/bt1648_fano_charge_conservation.json',
        'point_mass': POINT_MASS,
        'point_mass_histogram': {str(k): v for k, v in sorted(Counter(POINT_MASS).items())},
        'fano_gauge_count': len(gauges),
        'gauge_span_histogram': {str(k): v for k, v in sorted(spans.items())},
        'balanced_target_multiset': sorted(balanced_target),
        'near_balanced_representative_exists': near_balanced_exists,
        'invariant_reading': 'Fano gauges move the location of the point-mass tilt but preserve its multiset {240,232,232,224,224,224,224}. Therefore no Fano/Witting relabeling gauge in this class produces a balanced 228/229 representative.',
        'honesty_boundary': 'This classifies the finite Fano GL(3,2) relabeling orbit of the BT1648 point-mass vector. It does not rule out a different physical incidence design outside this charge class.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1652 Fano Gauge Untwister\n\nThe Fano gauge group has 168 point relabelings. Across this full orbit, the point-mass vector only moves location; its multiset remains {240,232,232,224,224,224,224}. Thus no balanced 228/229 representative exists inside the tested Fano/Witting relabeling class. The tilt is an invariant of this charge class, not a gauge artifact.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1652: Fano gauges move the point-mass tilt but cannot balance it; the multiset $\{240,232,232,224^4\}$ is invariant.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1652,'verified':result['verified'],'gauges':len(gauges)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
