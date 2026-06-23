#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1567_internal_optic_algebra_table.json'
MD = ROOT / 'analysis' / 'BT1567_internal_optic_algebra_table.md'
TEX = ROOT / 'analysis' / 'BT1567_internal_optic_algebra_table.tex'

MOD = 3
I2 = ((1,0),(0,1))
F = ((0,2),(1,0))   # qutrit Fourier symplectic action
S = ((1,0),(1,1))   # quadratic phase shear
X = (1,0)           # translation in X exponent
Z = (0,1)           # translation in Z exponent


def matmul(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) % MOD for j in range(2)) for i in range(2))

def matvec(a,v):
    return tuple(sum(a[i][k]*v[k] for k in range(2)) % MOD for i in range(2))

def vadd(a,b):
    return tuple((a[i]+b[i]) % MOD for i in range(2))

def compose(g,h):
    # g after h: (M,t)(N,u)=(MN, M u + t)
    M,t = g
    N,u = h
    return (matmul(M,N), vadd(matvec(M,u),t))

GENS = {
    'I': (I2,(0,0)),
    'X': (I2,X),
    'Z': (I2,Z),
    'F3': (F,(0,0)),
    'S': (S,(0,0)),
}


def closure():
    start = GENS['I']
    seen = {start}
    q = deque([start])
    while q:
        g = q.popleft()
        for h in GENS.values():
            for new in (compose(g,h), compose(h,g)):
                if new not in seen:
                    seen.add(new)
                    q.append(new)
    return seen

def name_key(g):
    M,t = g
    return f"M{M}_t{t}"

def main() -> None:
    group = closure()
    small_table = {}
    for a,ga in GENS.items():
        small_table[a] = {}
        for b,gb in GENS.items():
            small_table[a][b] = name_key(compose(ga,gb))
    checks = {
        'five_named_generators': len(GENS) == 5,
        'single_qutrit_projective_clifford_size_216': len(group) == 216,
        'translations_9_present': sum(1 for M,t in group if M == I2) == 9,
        'symplectic_part_24': len({M for M,t in group}) == 24,
        'composition_table_5_by_5': len(small_table) == 5 and all(len(row)==5 for row in small_table.values()),
    }
    result = {
        'bt':1567,
        'title':'Internal optic algebra table',
        'verified': all(checks.values()),
        'source':'tools/bt1565_self_applied_photonic_circuit_model.py',
        'generators': {k: {'matrix': v[0], 'translation': v[1]} for k,v in GENS.items()},
        'closure_size': len(group),
        'symplectic_part_size': len({M for M,t in group}),
        'translation_part_size': sum(1 for M,t in group if M == I2),
        'named_composition_table': small_table,
        'interpretation':'The internal optic operations I, X, Z, F3, and S generate the full single-qutrit projective Clifford action of size 216 on the state/operator Choi legs: 9 translations times 24 symplectic frame changes.',
        'honesty_boundary':'This is a finite algebra table for internal register actions, not a laboratory implementation of every element.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1567 Internal Optic Algebra Table\n\nThe internal operations I, X, Z, F3, and S generate the finite single-qutrit projective Clifford action. The closure size is 216, split as 9 translations and 24 symplectic frame changes. This is an internal register algebra table, not a lab implementation claim for every element.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1567: internal operations $I,X,Z,F_3,S$ close to the single-qutrit projective Clifford action of size $216=9\\cdot24$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1567,'verified':result['verified'],'closure':len(group)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
