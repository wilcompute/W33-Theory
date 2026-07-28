#!/usr/bin/env python3
"""
Pass 1178: Sym^3(V24) plethysm decomposition search.

Goal: search for plausible W(E6)-irrep multiplicity patterns for the 2600-dim
module Sym^3(V24), using only exact arithmetic constraints and prior facts.

We do NOT claim uniqueness without a character table; this pass enumerates
low-complexity decompositions that can seed a later exact character computation.
"""
import json
from pathlib import Path
from datetime import datetime

WE6_DIMS = [1,6,6,10,15,15,20,20,24,24,30,60,60,64,80,81,90,90,120,120,160,216,240,270,360]
UNIQ = sorted(set(WE6_DIMS), reverse=True)
TARGET = 2600

def find_decomps(target, dims, max_results=25, max_mult=12):
    out = []
    def bt(rem, idx, cur):
        if rem == 0:
            out.append(dict(cur))
            return
        if idx >= len(dims) or len(out) >= max_results:
            return
        d = dims[idx]
        mmax = min(max_mult, rem // d)
        for m in range(mmax, -1, -1):
            if m:
                cur[d] = m
            bt(rem - m*d, idx+1, cur)
            if m:
                del cur[d]
    bt(target, 0, {})
    return out

def score(decomp):
    terms = sum(decomp.values())
    distinct = len(decomp)
    maxmult = max(decomp.values()) if decomp else 0
    heavy = sum(k*v for k,v in decomp.items() if k >= 160)
    return (terms, distinct, maxmult, -heavy)

def main():
    decomps = find_decomps(TARGET, UNIQ)
    decomps = sorted(decomps, key=score)
    best = decomps[:10]
    result = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1178.sym3_v24_plethysm_search.v1',
        'status': 'PASS',
        'target': TARGET,
        'interpretation': 'Candidate W(E6)-irrep multiplicity patterns for Sym^3(V24); arithmetic only, pending exact character table verification.',
        'best_candidates': best,
        'notes': [
            'These are dimension-feasible decompositions only.',
            'Exact plethysm requires the W(E6) character table or explicit matrices.',
            'Use these candidates to test against future character traces on simple reflections.'
        ]
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/SYM3_V24_PLETHYSM_SEARCH_2026_07_27.json').write_text(json.dumps(result, indent=2))
    print('PASS 1178 complete:', len(best), 'candidate decompositions stored')
    return result

if __name__ == '__main__':
    main()
