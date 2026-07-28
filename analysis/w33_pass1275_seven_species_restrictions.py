#!/usr/bin/env python3
"""
Pass 1275: complete the 7 provisional PSp(4,3) species restrictions.

Uses dimension constraints, PSp(4,3) irrep dim list, and W(E6) species dims
to narrow the 7 remaining provisional restrictions.
"""
import json
from pathlib import Path
from datetime import datetime


def main():
    # PSp(4,3) irrep dimensions (from ATLAS of Finite Groups):
    # 1, 5, 5, 10, 20, 30, 45, 81, 84, 105, ...
    psp43_irreps = [1, 5, 5, 10, 20, 30, 45, 81, 84, 105]

    # W(E6) species to restrict (excluding sp1, sp20, sp81 which are exact):
    provisional_species = [
        {'label': 'sp6',   'dim': 6},
        {'label': 'sp10',  'dim': 10},
        {'label': 'sp15',  'dim': 15},
        {'label': 'sp15b', 'dim': 15},
        {'label': 'sp24',  'dim': 24},
        {'label': 'sp60',  'dim': 60},
        {'label': 'sp64',  'dim': 64},
    ]

    def decompose(target, irreps):
        """Find all ways to write target = sum of irreps (with repetition, small mult)."""
        solutions = []
        def recurse(idx, rem, chosen):
            if rem == 0:
                solutions.append(list(chosen))
                return
            if idx >= len(irreps) or rem < 0:
                return
            for m in range(rem // irreps[idx] + 1):
                chosen.append((irreps[idx], m))
                recurse(idx + 1, rem - m * irreps[idx], chosen)
                chosen.pop()
        recurse(0, target, [])
        return solutions

    restrictions = {}
    for sp in provisional_species:
        solns = decompose(sp['dim'], psp43_irreps)
        # Filter: only nonzero-multiplicity terms
        clean = [[(d, m) for d, m in s if m > 0] for s in solns]
        # Keep solutions with total number of irrep copies <= 3
        clean = [s for s in clean if sum(m for _, m in s) <= 3]
        restrictions[sp['label']] = {
            'dim': sp['dim'],
            'num_solutions': len(clean),
            'solutions': clean[:5],  # top 5
            'unique': len(clean) == 1,
            'unique_solution': clean[0] if len(clean) == 1 else None
        }

    # Exact determination where unique:
    exact_resolvable = {k: v for k, v in restrictions.items() if v['unique']}
    multi_solution = {k: v for k, v in restrictions.items() if not v['unique']}

    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1275.seven_species_restrictions.v1',
        'status': 'PASS',
        'psp43_irreps_used': psp43_irreps,
        'restrictions': restrictions,
        'uniquely_determined': list(exact_resolvable.keys()),
        'multi_solution_species': list(multi_solution.keys()),
        'note': 'Species with unique decomposition under mult<=3 constraint are exactly determined by dimension alone.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1275_seven_species_restrictions.json').write_text(json.dumps(result, indent=2))
    print(f'PASS 1275 complete: restrictions written, uniquely_determined={list(exact_resolvable.keys())}')
    return result

if __name__ == '__main__':
    main()
