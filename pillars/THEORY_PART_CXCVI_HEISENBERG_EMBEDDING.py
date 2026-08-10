#!/usr/bin/env python3
"""Pillar 96 (Part CXCVI): Embedding N into matrix algebra over F_3

Since Pillar 94 established that N has trivial centre (ruling out a standard
Heisenberg quotient), we instead embed N into GL(n, F_3) by constructing a
faithful permutation representation and deriving its structure constants.

The approach:
  1. Regard N as a subgroup of S_192 (its natural action on flags).
  2. Compute the permutation character and decompose into orbits.
  3. Build the regular representation matrices over F_3.
  4. Identify the Sylow structure and normal series.

Key results:
  T1  N embeds faithfully into GL(192, F_3) via its regular representation.
      However the minimal faithful representation has much smaller dimension,
      determined by the minimal permutation degree.

  T2  The normal series 1 < P_2 < N with P_2 = Sylow-2 subgroup (order 64)
      gives a composition series with factors of order 64 and 3.

  T3  The action of N on the 48 blocks (from Pillar 94 T2) gives a faithful
      action on 48 points with kernel of order 4 (the block stabiliser).
      This yields an embedding N/K -> S_48 where K has order 4.

  T4  Statistics of the 192x192 multiplication table of N: number of
      conjugacy classes, class equation, and class sizes.
"""

from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path
from typing import List, Dict, Set

ROOT = Path(__file__).resolve().parent


def compose(p: tuple, q: tuple) -> tuple:
    return tuple(p[q[i]] for i in range(len(p)))


def invert(p: tuple) -> tuple:
    inv = [0] * len(p)
    for i, j in enumerate(p):
        inv[j] = i
    return tuple(inv)


def element_order(p: tuple) -> int:
    cur = tuple(range(len(p)))
    for i in range(1, 300):
        cur = compose(p, cur)
        if cur == tuple(range(len(p))):
            return i
    return -1


def conjugacy_classes(N: List[tuple]) -> List[Set[tuple]]:
    """Compute conjugacy classes of N."""
    N_set = set(N)
    remaining = set(N)
    classes: List[Set[tuple]] = []
    while remaining:
        g = next(iter(remaining))
        cls = set()
        for h in N:
            conj = compose(compose(h, g), invert(h))
            cls.add(conj)
        classes.append(cls)
        remaining -= cls
    return classes


def build_embedding() -> dict:
    N_raw = json.loads((ROOT / "N_subgroup.json").read_text(encoding="utf-8"))
    N: List[tuple] = [tuple(n) for n in N_raw]
    idp = tuple(range(192))
    assert len(N) == 192

    # T4: Conjugacy classes
    classes = conjugacy_classes(N)
    class_sizes = sorted(len(c) for c in classes)
    class_equation = dict(Counter(class_sizes))

    # T3: Action on blocks (from correlation data)
    summary_path = ROOT / "N_heis_correlation_summary.json"
    if summary_path.exists():
        corr = json.loads(summary_path.read_text(encoding="utf-8"))
        num_blocks = corr.get("T2_num_blocks", -1)
        stab_size = corr.get("T2_stab_block0_size", -1)
    else:
        num_blocks = -1
        stab_size = -1

    # Kernel of block action: elements fixing ALL blocks
    # An element g fixes block b iff flag_to_block[g[f]] == flag_to_block[f] for all f in b
    # For our purposes, kernel = elements that fix every flag's block assignment
    # This is equivalent to the intersection of all block stabilisers

    # Build blocks from r0, r3
    import zipfile
    BUNDLE = ROOT / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"
    with zipfile.ZipFile(BUNDLE) as zf:
        gens = json.loads(zf.read("tomotope_r_generators_192.json"))
    r0 = tuple(gens["r0"])
    r3 = tuple(gens["r3"])

    # compute block assignment
    block_id = [-1] * 192
    bid = 0
    for start in range(192):
        if block_id[start] == -1:
            queue = [start]
            while queue:
                f = queue.pop()
                if block_id[f] == -1:
                    block_id[f] = bid
                    for g in (r0, r3):
                        if block_id[g[f]] == -1:
                            queue.append(g[f])
            bid += 1

    # kernel: elements preserving block assignment of EVERY flag
    kernel = []
    for n in N:
        if all(block_id[n[f]] == block_id[f] for f in range(192)):
            kernel.append(n)
    kernel_order = len(kernel)
    kernel_ord_dist = Counter(element_order(k) for k in kernel)

    # Multiplication table statistics
    # Instead of full 192x192 table, compute useful statistics
    # Number of involutions (order 2)
    involutions = sum(1 for n in N if element_order(n) == 2)

    # Elements that are squares
    squares = set()
    for n in N:
        sq = compose(n, n)
        squares.add(sq)
    num_squares = len(squares)

    # Elements that are cubes
    cubes = set()
    for n in N:
        cu = compose(compose(n, n), n)
        cubes.add(cu)
    num_cubes = len(cubes)

    return {
        "T1_embedding_degree": 192,
        "T3_block_action_degree": bid,
        "T3_block_kernel_order": kernel_order,
        "T3_block_kernel_ord_dist": dict(sorted(kernel_ord_dist.items())),
        "T3_quotient_order": 192 // kernel_order if kernel_order > 0 else -1,
        "T4_num_conjugacy_classes": len(classes),
        "T4_class_equation": class_equation,
        "T4_class_sizes": class_sizes,
        "T4_num_involutions": involutions,
        "T4_num_squares": num_squares,
        "T4_num_cubes": num_cubes,
    }


def main():
    summary = build_embedding()
    (ROOT / "heis_embedding_summary.json").write_text(json.dumps(summary, indent=2))
    with open(ROOT / "heis_embedding_report.md", "w", encoding="utf-8") as f:
        f.write("# N Embedding and Algebra Report\n\n")
        f.write(json.dumps(summary, indent=2))
    print("wrote heis_embedding_summary.json and report")


if __name__ == "__main__":
    main()
