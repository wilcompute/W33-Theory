#!/usr/bin/env python3
"""Search for a simple phase formula after Schlaefli index permutations.

We test whether there exists a permutation of indices 1..6 (and optional E<->C swap)
such that phases satisfy affine formulas in i (mod 3):
  E_i: a*i+b, C_i: c*i+d, L_ij: e*i+f*j+g (mod 3)
"""
from __future__ import annotations

from itertools import permutations, product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    iso = json.loads((ROOT / 'artifacts' / 'balanced_orbit_schlafli_isomorphism.json').read_text())
    mapping_full = iso['mapping_full']

    # Build line -> phase dict
    line_phase = {}
    for _, info in mapping_full.items():
        line = tuple(info['line'])
        line_phase[line] = int(info['phase'])

    indices = [1, 2, 3, 4, 5, 6]

    def phase_E(i, perm, swap):
        line = ('E', perm[i-1]) if not swap else ('C', perm[i-1])
        return line_phase[line]

    def phase_C(i, perm, swap):
        line = ('C', perm[i-1]) if not swap else ('E', perm[i-1])
        return line_phase[line]

    def phase_L(i, j, perm, swap):
        # L-lines unaffected by E/C swap; indices permuted
        ii, jj = perm[i-1], perm[j-1]
        if ii > jj:
            ii, jj = jj, ii
        return line_phase[('L', ii, jj)]

    solutions = []
    for perm in permutations(indices):
        for swap in [False, True]:
            # Precompute observed phases
            E_obs = {i: phase_E(i, perm, swap) for i in indices}
            C_obs = {i: phase_C(i, perm, swap) for i in indices}
            L_obs = {(i, j): phase_L(i, j, perm, swap) for i in indices for j in indices if i < j}

            # Search coefficients
            for a, b, c, d, e, f, g in product([0, 1, 2], repeat=7):
                ok = True
                for i in indices:
                    if (a * (i % 3) + b) % 3 != E_obs[i]:
                        ok = False
                        break
                if not ok:
                    continue
                for i in indices:
                    if (c * (i % 3) + d) % 3 != C_obs[i]:
                        ok = False
                        break
                if not ok:
                    continue
                for (i, j), val in L_obs.items():
                    if (e * (i % 3) + f * (j % 3) + g) % 3 != val:
                        ok = False
                        break
                if ok:
                    solutions.append({
                        "perm": perm,
                        "swap_EC": swap,
                        "coeffs": (a, b, c, d, e, f, g),
                    })
            if solutions:
                break
        if solutions:
            break

    results = {
        "num_solutions": len(solutions),
        "solutions": solutions[:3],
    }
    out_path = ROOT / 'artifacts' / 'schlafli_phase_formula_perm.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
