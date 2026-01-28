#!/usr/bin/env python3
"""Check whether generator maps preserve antipodal root pairs.

For a root permutation g, we test if g(-r) = -g(r) for each root r.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0.0] * 8
                    r[i] = float(si)
                    r[j] = float(sj)
                    roots.append(tuple(r))
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


def main():
    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}

    data = json.loads((ROOT / "artifacts" / "sp43_we6_generator_map.json").read_text())
    gens = [g["root_perm"] for g in data["generator_maps"]]

    results = []
    for gi, g in enumerate(gens):
        ok = 0
        for i, r in enumerate(roots):
            j = root_to_idx[tuple(-x for x in r)]
            s = g[i]
            sj = g[j]
            expected = root_to_idx[tuple(-x for x in roots[s])]
            if sj == expected:
                ok += 1
        results.append(
            {
                "gen_index": gi,
                "antipodal_preserved": ok,
                "total": len(roots),
            }
        )

    out = {
        "results": results,
        "all_preserve": all(r["antipodal_preserved"] == r["total"] for r in results),
    }
    out_path = ROOT / "artifacts" / "antipodal_preservation.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
