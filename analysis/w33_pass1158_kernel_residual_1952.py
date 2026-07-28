#!/usr/bin/env python3
"""
Pass 1158: Systematic attack on the 1952-dimensional cubic-map kernel residual.

After removing the proven 3*81=243-dim Steinberg packet from the 2195-dim
cubic-map kernel, the residual has dimension 1952.

This pass performs an exact integer divisibility census and identifies
candidate irreducible summands of W(E6) that could account for 1952:

Known Sp(4,3) / W(E6) module dimensions relevant to this geometry:
  1, 6, 10, 15, 20, 21, 24, 25, 27, 28, 32, 40, 45, 60, 64, 81, 90, 105,
  120, 160, 189, 210, 216, 240, 270, 315, 336, 378, 405, 420, 512, 560, 630.

1952 factored: 1952 = 2^5 * 61.  61 is prime.
This is the key obstruction: 61 divides 1952 but almost no standard
group-module dimension for W(E6) or Sp(4,3) is divisible by 61.

Consequences:
  - 1952 cannot be a direct sum of modules all of dimension < 61 unless
    the count is large (e.g. 1952/1 = 1952 trivials -- trivially excluded).
  - The most natural decomposition avenue is NOT a sum of equal-dimensional
    summands but a mixed decomposition.
  - Most promising route: look for a 32*61 = 1952 pattern -- but 61 does
    not appear as a standard W(E6) irrep dimension.
  - Alternative: 1952 = 1920 + 32 = (e.g. 1920-dim summand) + (32-dim residual).
    1920 = 2^7 * 3 * 5 -- more group-theoretically natural.
  - Or: 1952 = 7*276 + 20 where 276 = C(24,2) = dim(wedge^2 of 24-dim eigenspace).
    This leaves a 20-dim residual which could be the W33 standard 20-dim module.

Outputs: data/KERNEL_RESIDUAL_1952_2026_07_27.json
"""
import json
from pathlib import Path
from datetime import datetime

KERNEL_TOTAL = 2195
STEINBERG_PACKET = 243
RESIDUAL = KERNEL_TOTAL - STEINBERG_PACKET  # 1952

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

CANDIDATE_DIMS = [1,6,10,15,20,21,24,25,27,28,32,40,45,60,64,81,90,105,
                  120,160,189,210,216,240,270,276,315,336,378,405,420,512,560,630]

def find_decompositions(target, dims, max_summands=8):
    """Find all representations target = sum of elements of dims (with repetition)
    using at most max_summands terms, preferring small number of summands."""
    results = []
    dims_sorted = sorted(set(d for d in dims if d <= target), reverse=True)
    def backtrack(remaining, path):
        if remaining == 0:
            results.append(list(path))
            return
        if len(path) >= max_summands:
            return
        for d in dims_sorted:
            if d > remaining:
                continue
            if path and d > path[-1]:
                continue  # keep sorted
            path.append(d)
            backtrack(remaining - d, path)
            path.pop()
    backtrack(target, [])
    return sorted(results, key=lambda x: (len(x), x))

def main():
    assert RESIDUAL == 1952
    factors = factorize(RESIDUAL)
    # Key decompositions
    decomps = find_decompositions(RESIDUAL, CANDIDATE_DIMS, max_summands=6)
    top_decomps = decomps[:20]  # show top 20
    # Special analysis: 7*276 + 20
    wedge2_24 = 276  # C(24,2)
    k = RESIDUAL // wedge2_24
    rem = RESIDUAL % wedge2_24
    wedge_analysis = {
        'wedge2_of_24dim_eigenspace': wedge2_24,
        'copies_of_276': k,
        'remainder': rem,
        'formula': f'{k}*{wedge2_24} + {rem} = {k*wedge2_24 + rem}',
        'interpretation': '20-dim residual could be the W33 standard 20-dim module'
            if rem == 20 else f'Remainder {rem} needs identification',
    }
    # 61 analysis
    prime_obstruction = {
        '1952_factored': '2^5 * 61',
        '61_is_prime': True,
        'implication': '1952 cannot split into equal blocks of size dividing standard module dims unless 61 divides one summand dim or the count involves 61',
        'most_natural_split': '1920 + 32 where 1920 = 2^7 * 3 * 5',
        '1920_check': 1952 - 1920 == 32,
    }
    result = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1158.kernel_residual_1952.v1',
        'status': 'ANALYSIS_COMPLETE',
        'kernel_total': KERNEL_TOTAL,
        'steinberg_packet_dim': STEINBERG_PACKET,
        'residual_dim': RESIDUAL,
        'residual_factorization': factors,
        'prime_obstruction_analysis': prime_obstruction,
        'wedge2_24_analysis': wedge_analysis,
        'top_candidate_decompositions': top_decomps,
        'recommended_next': '1952 = 1920 + 32: identify the 1920-dim summand as a W(E6) or Sp(4,3) module and the 32-dim piece as the line-nonedge species module (rank 32, TOM 81).',
    }
    out = Path('data/KERNEL_RESIDUAL_1952_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f'PASS 1158 residual={RESIDUAL}, factored={factors}')
    print(f'  Wedge2(24) analysis: {k}*276 + {rem}')
    print(f'  1952 = 1920 + 32: {1952-1920==32}')
    return result

if __name__ == '__main__':
    main()
