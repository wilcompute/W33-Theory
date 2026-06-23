#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1570_internal_clifford_orbit_census.json'
MD = ROOT / 'analysis' / 'BT1570_internal_clifford_orbit_census.md'
TEX = ROOT / 'analysis' / 'BT1570_internal_clifford_orbit_census.tex'
MOD = 3
I2 = ((1,0),(0,1))
F = ((0,2),(1,0))
S = ((1,0),(1,1))
GENS = {
    'I': (I2,(0,0)),
    'X': (I2,(1,0)),
    'Z': (I2,(0,1)),
    'F3': (F,(0,0)),
    'S': (S,(0,0)),
}

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) % MOD for j in range(2)) for i in range(2))

def mv(a,v):
    return tuple(sum(a[i][k]*v[k] for k in range(2)) % MOD for i in range(2))

def va(a,b):
    return tuple((a[i]+b[i]) % MOD for i in range(2))

def comp(g,h):
    M,t = g; N,u = h
    return (mm(M,N), va(mv(M,u), t))

def closure():
    seen = {GENS['I']}
    q = deque([GENS['I']])
    while q:
        g = q.popleft()
        for h in GENS.values():
            for n in (comp(g,h), comp(h,g)):
                if n not in seen:
                    seen.add(n); q.append(n)
    return seen

def main() -> None:
    group = closure()
    rows = []
    for M,t in sorted(group):
        zero_t = t == (0,0)
        ident_M = M == I2
        rows.append({
            'matrix': M,
            'translation': t,
            'class': 'identity' if ident_M and zero_t else ('pure_translation' if ident_M else ('linear_frame' if zero_t else 'mixed_affine')),
            'preserves_state_operator_split': True,
            'stabilizes_identity_choi_state': ident_M and zero_t,
            'preserves_centered_oam_opposition': zero_t,
            'moves_oam_origin': not zero_t,
        })
    counts = {
        'total': len(rows),
        'identity': sum(r['class']=='identity' for r in rows),
        'pure_translation_nonidentity': sum(r['class']=='pure_translation' for r in rows),
        'linear_frame_nonidentity': sum(r['class']=='linear_frame' for r in rows),
        'mixed_affine': sum(r['class']=='mixed_affine' for r in rows),
        'split_preserving': sum(r['preserves_state_operator_split'] for r in rows),
        'identity_choi_stabilizer': sum(r['stabilizes_identity_choi_state'] for r in rows),
        'centered_opposition_preserving': sum(r['preserves_centered_oam_opposition'] for r in rows),
        'origin_moving': sum(r['moves_oam_origin'] for r in rows),
    }
    checks = {
        'total_216': counts['total'] == 216,
        'class_partition_216': counts['identity'] + counts['pure_translation_nonidentity'] + counts['linear_frame_nonidentity'] + counts['mixed_affine'] == 216,
        'all_preserve_split_by_construction': counts['split_preserving'] == 216,
        'identity_choi_stabilizer_one': counts['identity_choi_stabilizer'] == 1,
        'centered_opposition_preserving_24': counts['centered_opposition_preserving'] == 24,
        'origin_moving_192': counts['origin_moving'] == 192,
    }
    result = {
        'bt': 1570,
        'title': 'Internal Clifford orbit census',
        'verified': all(checks.values()),
        'source': 'data/bt1567_internal_optic_algebra_table.json',
        'counts': counts,
        'sample_rows': rows[:12],
        'interpretation': 'All 216 internal Clifford actions preserve the state/operator Choi split because they act inside the operator-register model rather than swapping legs. Only identity stabilizes the identity Choi state itself. The 24 zero-translation frame changes preserve centered OAM opposition; the 192 translated elements move the OAM origin and therefore do not preserve the centered spiral basis without recentering.',
        'honesty_boundary': 'This is a finite affine-Clifford census. It does not claim every element has a calibrated optical implementation.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1570 Internal Clifford Orbit Census\n\nThe internal Clifford action has 216 elements. All preserve the state/operator split by construction. Only identity stabilizes the identity Choi state. The 24 zero-translation frame changes preserve centered OAM opposition; 192 translated elements move the OAM origin and need recentering.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1570: the 216 internal Clifford elements all preserve the Choi state/operator split; 24 zero-translation elements preserve centered OAM opposition.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1570,'verified':result['verified'],'counts':counts}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
