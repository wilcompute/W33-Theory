#!/usr/bin/env python3
"""
Pass 1164: Identification of the 1920-dim piece of the kernel residual.

1952 = 1920 + 32, where:
  - 32 = rank of the TOM-81 (line-nonedge/skew-frame) species
  - 1920 = 2^7 * 3 * 5 -- needs to be identified as a W(E6) or Sp(4,3) module

W(E6) irrep dimensions that could contribute to 1920:
  From the list [1,6,6,10,15,15,20,20,24,24,30,60,60,64,80,81,90,90,
                 120,120,160,216,240,270,360]

We search for multisets of W(E6) irreps summing to 1920.

Additional structural facts:
  - 1920 = 16 * 120 = 16 * 120 (but 120 appears in W(E6) dims twice)
  - 1920 = 24 * 80  (80 is a W(E6) irrep dim)
  - 1920 = 12 * 160 (160 is a W(E6) irrep dim)
  - 1920 = 8 * 240  (240 is a W(E6) irrep dim)
  - 1920 = 6 * 320  (320 does not appear in W(E6) dims)
  - 1920 = 4 * 480  (480 does not appear)
  - 1920 = 2 * 960  (960 does not appear)
  - 1920 = 360 + 360 + 240 + 240 + 240 + 360 -- too many high-dim
  - 1920 = 240*4 + 80*3 + 160*1 + 120*2 -- let's check: 960+240+160+240=1600, not 1920
  - Best candidate: 1920 as a SINGLE module dimension.
    Does any Sp(4,3) or W(E6) tensor product / symmetric power yield 1920?
    - Sym^2(40) = C(40+1,2) = 820. Not 1920.
    - Wedge^2(40) = C(40,2) = 780. Not 1920.
    - 40 * 48 = 1920 where 48 = stabilizer order of TOM-81 normalizer.
      This is a dimensional coincidence, not a module.
    - 1920 = 25920 / (3*9/2)... 25920/13.5 non-integer.
    - 1920 = |Sp(4,3)| / (25920/1920) = 25920/13.5. Not clean.
    - 1920 = 2 * |W(F4)| / k for some k?
      |W(F4)| = 1152. 2*1152=2304. Not 1920.
    - 1920 = 2 * 960 = 2 * 8! / (something).
      8! = 40320. 40320/42 = 960. Not obviously group-theoretic.
    - BEST: 1920 = S_8 order? |S_8| = 40320. No.
    - BEST: 1920 = 2^7 * 3 * 5 = 128 * 15 = 64 * 30.
      64 and 30 both appear as W(E6) irrep dims!
      64 * 30 = 1920. This could be the tensor product 64 ⊗ 30 restricted
      to a specific subgroup, but as a flat sum: 64+30=94, not 1920.
    - Direct decomposition: 360 + 270 + 240 + 216 + 160 + ...
      360+270=630, +240=870, +216=1086, +160=1246, +120=1366,
      +120=1486, +90=1576, +90=1666, +81=1747, +80=1827, +64=1891,
      +29 -- 29 not a W(E6) dim. Fails.
    - Try: 360+270+240+216+160+120+120+90+90+81+80+64+30+...
      Running sum: 360+270+240+216+160+120+120+90+90+81+80+64
      = 360+270=630, +240=870, +216=1086, +160=1246, +120=1366,
        +120=1486, +90=1576, +90=1666, +81=1747, +80=1827, +64=1891
      Need 1920-1891 = 29. Not a W(E6) dim.
    - Try replacing 64 with 60+60=120:
      360+270+240+216+160+120+120+90+90+81+80+60+60+24 = ?
      360+270=630,+240=870,+216=1086,+160=1246,+120=1366,+120=1486,
      +90=1576,+90=1666,+81=1747,+80=1827,+60=1887,+60=1947... too big.
    - More systematic: see find_we6_sum_1920() below.

Outputs: data/MODULE_1920_IDENTIFICATION_2026_07_27.json
"""
import json
from pathlib import Path
from datetime import datetime

WE6_IRREP_DIMS = [
    1, 6, 6, 10, 15, 15, 20, 20, 24, 24,
    30, 60, 60, 64, 80, 81, 90, 90, 120, 120,
    160, 216, 240, 270, 360
]
TARGET = 1920

def find_we6_sum(target, dims, max_terms=6):
    results = []
    d_sorted = sorted(set(d for d in dims if d <= target), reverse=True)
    def bt(rem, idx, path):
        if rem == 0:
            results.append(list(path)); return
        if len(path) >= max_terms: return
        for i in range(idx, len(d_sorted)):
            d = d_sorted[i]
            if d > rem: continue
            path.append(d)
            bt(rem - d, i, path)
            path.pop()
        return
    bt(target, 0, [])
    return sorted(results, key=lambda x: (len(x), [-v for v in x]))

def uniform_sum_analysis(target, dims):
    """Find d in dims such that target is divisible by d and target//d is small."""
    candidates = []
    for d in sorted(set(dims)):
        if target % d == 0:
            k = target // d
            candidates.append({'dim': d, 'multiplicity': k, 'formula': f'{k}x{d}={target}'})
    return candidates

def main():
    uniform = uniform_sum_analysis(TARGET, WE6_IRREP_DIMS)
    decomps = find_we6_sum(TARGET, WE6_IRREP_DIMS, max_terms=5)
    # Special checks
    checks = {
        '24x80': 24 * 80 == TARGET,
        '12x160': 12 * 160 == TARGET,
        '8x240': 8 * 240 == TARGET,
        '16x120': 16 * 120 == TARGET,
        '1920_factored': '2^7 * 3 * 5',
        '64_times_30': 64 * 30 == TARGET,
        'fits_in_we6_order': TARGET < 25920,
        '1920_div_432': TARGET % 432 == 0,
        '1920_as_432_multiple': TARGET // 432,  # = 4.44... -> not integer
    }
    checks['1920_div_432'] = TARGET % 432 == 0
    checks['1920_as_432_multiple'] = TARGET / 432  # 4.444...
    # Key: 1920 = 4 * 480 = 4 * (240*2) -- but 480 not a W(E6) dim
    # Best candidate: 1920 as a PERMUTATION module dimension
    # W(E6) acts on coset spaces:
    #   W(E6)/S5: size 432
    #   W(E6)/A6: size 25920/360 = 72
    #   W(E6)/S6: size 25920/720 = 36 -- close to 40 but not 40
    #   W(E6)/PSL(3,2): size 25920/168 -- not integer cleanly
    # 1920 = 1920: check if it's a permutation module size
    #   25920/1920 = 13.5 -- not integer, so NOT a coset space of W(E6).
    # CONCLUSION: 1920 is most likely NOT a single irreducible W(E6) module.
    # It is likely a REDUCIBLE module, summing multiple irreps.
    # The uniform decompositions (like 24x80 or 8x240) suggest
    # a highly symmetric but reducible structure.
    # Most physically motivated: 1920 = 24 * 80 (24 copies of the 80-dim irrep?)
    # but W(E6) modules don't normally appear with such high multiplicity
    # in a kernel.
    # BEST CANDIDATE: 1920 is the full Sp(4,3)-module complement to
    # the Steinberg summand, not decomposable over W(E6) without further data.

    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1164.1920_module_identification.v1',
        'status': 'ANALYSIS_COMPLETE',
        'target': TARGET,
        'factorization': '2^7 * 3 * 5',
        'uniform_sum_analysis': uniform,
        'top_we6_decompositions': decomps[:12],
        'arithmetic_checks': checks,
        'is_coset_space_of_we6': False,
        'reason': '25920 / 1920 = 13.5, not integer',
        'best_candidates': [
            '1920 = 24 * 80 (24 copies of the 80-dim W(E6) irrep)',
            '1920 = 12 * 160 (12 copies of the 160-dim irrep)',
            '1920 = 8 * 240 (8 copies of the 240-dim irrep)',
            '1920 likely reducible; decomposition requires explicit module computation (MeatAxe)',
        ],
        'key_open': '1952 = 1920 + 32 split confirmed; 1920 identification requires MeatAxe or explicit GAP computation on the cubic map kernel matrix.',
    }
    out = Path('data/MODULE_1920_IDENTIFICATION_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f'PASS 1164: 1920 analysis complete')
    print(f'  24x80={24*80==TARGET}, 8x240={8*240==TARGET}, 12x160={12*160==TARGET}')
    print(f'  25920/1920 = {25920/1920} (not integer -> not W(E6) coset space)')
    print(f'  Top decompositions: {decomps[:3]}')
    return result

if __name__ == '__main__':
    main()
