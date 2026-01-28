#!/usr/bin/env python3
"""Search for order-6 elements in W(E6) with 40 orbits on E8 roots.

We embed W(E6) as subgroup of W(E8) via simple reflections on E8 root lattice.
We then test orbit partition sizes on E8 roots.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from sage.all import RootSystem

ROOT = Path(__file__).resolve().parents[1]


def main():
    R8 = RootSystem(['E', 8]).root_lattice()
    W8 = R8.weyl_group()

    # Use E6 simple reflections embedded in E8: take reflections 1..6 of E8
    # This is a subgroup but not necessarily the standard E6 embedding; still a strong test.
    gens = [W8.simple_reflection(i) for i in range(1, 7)]
    W6 = W8.subgroup(gens)

    roots = list(R8.roots())
    root_index = {tuple(r.to_vector()): i for i, r in enumerate(roots)}

    random.seed(0)
    max_iter = 500

    for it in range(max_iter):
        # random word in W6
        length = random.randint(6, 30)
        w = gens[random.randint(0, 5)]
        for _ in range(length):
            w = w * gens[random.randint(0, 5)]

        if w.order() != 6:
            continue

        # compute orbit sizes
        orbit_map = {}
        sizes = []
        ok = True
        for idx, r in enumerate(roots):
            if idx in orbit_map:
                continue
            orb = []
            cur = r
            for _ in range(6):
                j = root_index[tuple(cur.to_vector())]
                if j in orbit_map:
                    ok = False
                    break
                orbit_map[j] = True
                orb.append(j)
                cur = w.action(cur)
            if not ok:
                break
            sizes.append(len(orb))
        if ok and len(sizes) == 40 and all(s == 6 for s in sizes):
            out = {
                "found": True,
                "iteration": it,
                "word_length": length,
            }
            out_path = ROOT / "artifacts" / "we6_order6_partition_found.json"
            out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
            print("Found at iter", it)
            return

    out = {"found": False, "iterations": max_iter}
    out_path = ROOT / "artifacts" / "we6_order6_partition_found.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Not found")


if __name__ == "__main__":
    main()
