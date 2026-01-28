#!/usr/bin/env python3
"""Search for simple phase formulas on Schlaefli labels.

We test if the balanced-orbit phase assignment can be expressed as
simple Z3 formulas in indices:
  E_i: a*s(i)+b,  C_i: c*s(i)+d,  L_ij: e*s(i)+f*s(j)+g
with s(i) in Z3 and coefficients in Z3.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    iso = json.loads(
        (ROOT / "artifacts" / "balanced_orbit_schlafli_isomorphism.json").read_text()
    )
    mapping_full = iso["mapping_full"]

    # Build line -> phase dict
    line_phase = {}
    for _, info in mapping_full.items():
        line = tuple(info["line"])
        line_phase[line] = int(info["phase"])

    indices = [1, 2, 3, 4, 5, 6]

    # Pre-split lines by type
    E_lines = [(i,) for i in indices]
    C_lines = [(i,) for i in indices]
    L_lines = [(i, j) for i in indices for j in indices if i < j]

    # Extract observed phases
    E_obs = {i: line_phase[("E", i)] for i in indices}
    C_obs = {i: line_phase[("C", i)] for i in indices}
    L_obs = {(i, j): line_phase[("L", i, j)] for i in indices for j in indices if i < j}

    solutions = []

    # Search over assignments s(i) in Z3
    for s_vals in product([0, 1, 2], repeat=6):
        s = {indices[i]: s_vals[i] for i in range(6)}

        # Search over coefficients
        for a, b, c, d, e, f, g in product([0, 1, 2], repeat=7):
            ok = True
            # E_i
            for i in indices:
                if (a * s[i] + b) % 3 != E_obs[i]:
                    ok = False
                    break
            if not ok:
                continue
            # C_i
            for i in indices:
                if (c * s[i] + d) % 3 != C_obs[i]:
                    ok = False
                    break
            if not ok:
                continue
            # L_ij
            for i, j in L_obs:
                if (e * s[i] + f * s[j] + g) % 3 != L_obs[(i, j)]:
                    ok = False
                    break
            if ok:
                solutions.append(
                    {
                        "s": s,
                        "coeffs": (a, b, c, d, e, f, g),
                    }
                )
        if solutions:
            break  # take first s with any solution

    results = {
        "num_solutions": len(solutions),
        "solutions": solutions[:5],
    }
    out_path = ROOT / "artifacts" / "schlafli_phase_formula.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
