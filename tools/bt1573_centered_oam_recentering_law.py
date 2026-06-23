#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1573_centered_oam_recentering_law.json'
MD = ROOT / 'analysis' / 'BT1573_centered_oam_recentering_law.md'
TEX = ROOT / 'analysis' / 'BT1573_centered_oam_recentering_law.tex'
MOD = 3
I2 = ((1,0),(0,1))
F = ((0,2),(1,0))
S = ((1,0),(1,1))
GENS = {'I':(I2,(0,0)),'X':(I2,(1,0)),'Z':(I2,(0,1)),'F3':(F,(0,0)),'S':(S,(0,0))}

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
    seen={GENS['I']}; q=deque([GENS['I']])
    while q:
        g=q.popleft()
        for h in GENS.values():
            for n in (comp(g,h), comp(h,g)):
                if n not in seen:
                    seen.add(n); q.append(n)
    return seen

def recenter_for(t):
    return tuple((-x) % MOD for x in t)

def recenter_name(t):
    rx, rz = recenter_for(t)
    parts=[]
    if rx: parts.append(f'X^{rx}')
    if rz: parts.append(f'Z^{rz}')
    return 'I' if not parts else ' '.join(parts)

def kind(t):
    x,z=t
    if x and not z: return 'oam_shift_only'
    if z and not x: return 'phase_shift_only'
    if x and z: return 'mixed_shift_phase'
    return 'centered'

def main() -> None:
    group=closure()
    translated=[(M,t) for M,t in group if t!=(0,0)]
    rows=[]
    for M,t in sorted(translated):
        rows.append({'translation':t,'recenter_translation':recenter_for(t),'recenter_operator':recenter_name(t),'class':kind(t)})
    by_t=Counter(str(r['translation']) for r in rows)
    by_kind=Counter(r['class'] for r in rows)
    checks={
        'translated_192': len(rows)==192,
        'eight_nonzero_translation_classes': len(by_t)==8,
        'each_translation_has_24_frames': sorted(by_t.values())==[24]*8,
        'oam_shift_only_48': by_kind['oam_shift_only']==48,
        'phase_shift_only_48': by_kind['phase_shift_only']==48,
        'mixed_shift_phase_96': by_kind['mixed_shift_phase']==96,
        'recenter_law_defined_for_all': all(r['recenter_operator'] for r in rows),
    }
    result={'bt':1573,'title':'Centered OAM recentering law','verified':all(checks.values()),'source':'data/bt1570_internal_clifford_orbit_census.json','class_counts':dict(by_kind),'translation_class_size':24,'sample_rows':rows[:16],'interpretation':'The 192 translated Clifford elements split into eight nonzero translation classes, each with 24 symplectic frames. Recenter by the inverse translation: t=(a,b) requires X^{-a} Z^{-b}. OAM-only and phase-only translations contribute 48 each; mixed shift/phase translations contribute 96.','honesty_boundary':'This is finite recentering on the qutrit phase-space/OAM-label model, not a calibrated optical correction for all modes.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1573 Centered OAM Recentering Law\n\nThe 192 translated Clifford elements split into eight nonzero translation classes, each with 24 symplectic frames. Recenter by the inverse translation: t=(a,b) requires X^{-a}Z^{-b}. OAM-only and phase-only classes contribute 48 each, and mixed shift/phase classes contribute 96.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1573: the 192 translated Clifford elements recenter by inverse translations $t=(a,b)\\mapsto X^{-a}Z^{-b}$, in classes $48+48+96$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1573,'verified':result['verified'],'class_counts':dict(by_kind)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
