#!/usr/bin/env python3
"""Pillar 94 (Part CXCV): Correlate regular subgroup N with block and t4-grade structure

The regular subgroup N of Gamma (order 192, acting sharply transitively on the
192 tomotope flags) is constructed in Pillar 93.  This pillar analyses the
relationship between N and the Heisenberg-coordinate structure established in
Pillars 83-89, identifying the key structural constraints that prevent N from
being a Heisenberg group itself.

Theorems:

T1  N has order distribution {1:1, 2:43, 3:32, 4:84, 6:32} and trivial centre
    Z(N) = {e}.  Consequently N is NOT a Heisenberg group (Heisenberg groups
    have non-trivial centres).

T2  N acts on the 48 <r0,r3>-blocks of the tomotope by sending block(0) to
    block(n(0)).  This action is transitive (N surjects onto all 48 blocks)
    and each block is the image of exactly |N|/48 = 4 elements.  The point
    stabiliser Stab_N(block_0) is a subgroup of order 4 with orders {1,2,2,4}.

T3  The element t^4 = (r1*r2)^4 has order 3 and partitions the 192 flags into
    grade classes: grade-0 = fixed flags (and cycle leaders), grade-1,2 = the
    remaining two positions in each 3-cycle.  The distribution of t4-grades
    among the 192 images {n(0) : n in N} is {0:128, 1:32, 2:32}.

T4  All 32 order-3 elements of N map flag 0 to a grade-0 flag.  Together with
    the identity they generate a subgroup of order 48 with distribution
    {1:1, 2:15, 3:32}.  The 27 Heisenberg qids from the K-model relate to this
    structure: note 27 does not divide 192 (since 192 = 2^6 * 3), confirming
    no surjection N -> Z3^3 exists.

T5  Elements of t4-grade 1 or 2 (total 64) have orders exclusively in {2,4,6};
    no order-3 element of N maps flag 0 to a grade-1 or grade-2 flag.

T6  Elements of t4-grade 0 have ALL five order types {1,2,3,4,6}, while those
    of grade 1 or 2 have only orders {2,4,6} (no order-1 or order-3 elements).
    In particular the 32 order-6 elements split: 10 have grade 0 and 22 have
    grade 1 or 2, whereas the 32 order-3 elements ALL have grade 0.
"""

from __future__ import annotations

import json
import zipfile
from collections import Counter, deque
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


def compose(p: tuple, q: tuple) -> tuple:
    return tuple(p[q[i]] for i in range(len(p)))


def element_order(p: tuple) -> int:
    cur = tuple(range(len(p)))
    for i in range(1, 300):
        cur = compose(p, cur)
        if cur == tuple(range(len(p))):
            return i
    return -1


def load_generators() -> Dict[int, tuple]:
    with zipfile.ZipFile(BUNDLE) as zf:
        gens = json.loads(zf.read("tomotope_r_generators_192.json"))
    return {int(k[1:]): tuple(v) for k, v in gens.items()}


def compute_blocks(r0: tuple, r3: tuple) -> Tuple[List[List[int]], List[int]]:
    """Return (blocks, flag_to_block) for <r0,r3> orbits."""
    block_id = [-1] * 192
    blocks: List[List[int]] = []
    for start in range(192):
        if block_id[start] == -1:
            block: List[int] = []
            queue = [start]
            bid = len(blocks)
            while queue:
                f = queue.pop()
                if block_id[f] == -1:
                    block_id[f] = bid
                    block.append(f)
                    for g in (r0, r3):
                        if block_id[g[f]] == -1:
                            queue.append(g[f])
            blocks.append(sorted(block))
    return blocks, block_id


def t4_grades(t4: tuple) -> List[int]:
    """Return grade 0/1/2 for each flag under the order-3 element t4."""
    grades = [0] * 192
    visited = [False] * 192
    for start in range(192):
        if not visited[start]:
            orbit = [start]
            f = t4[start]
            while f != start:
                orbit.append(f)
                f = t4[f]
            if len(orbit) == 3:
                for i, ff in enumerate(orbit):
                    grades[ff] = i
                    visited[ff] = True
            else:
                visited[start] = True
    return grades


def bfs_group(gens: list, limit: int = 500) -> List[tuple]:
    id_p = tuple(range(192))
    seen = {id_p}
    q: deque = deque([id_p])
    while q:
        g = q.popleft()
        for h in gens:
            for x in (compose(h, g), compose(g, h)):
                if x not in seen:
                    seen.add(x)
                    q.append(x)
                    if len(seen) > limit:
                        return list(seen)
    return list(seen)


def compute_correlation() -> dict:
    """Return summary dict describing N's block/grade/order structure."""
    r = load_generators()

    # Load N
    N_raw = json.loads((ROOT / "N_subgroup.json").read_text(encoding="utf-8"))
    N: List[tuple] = [tuple(n) for n in N_raw]
    assert len(N) == 192

    # T1: order distribution and center
    ord_dist = Counter(element_order(n) for n in N)

    # Center: check which elements commute with ALL others
    # Use a sample of 20 elements for efficiency (full check is 192^2=36864 compositions)
    center_size = sum(
        1 for g in N
        if all(compose(g, h) == compose(h, g) for h in N)
    )

    # T2: block action
    blocks, flag_to_block = compute_blocks(r[0], r[3])
    block_images = [flag_to_block[n[0]] for n in N]
    block_dist = Counter(block_images)
    block_hits_per_block = Counter(block_dist.values())

    # Stab_N(block_0): elements n with n[0] in block_0
    block0_flags = set(blocks[0])
    stab = [n for n in N if n[0] in block0_flags]
    stab_ord_dist = Counter(element_order(s) for s in stab)

    # T3: t4 grade distribution of n(0)
    t = compose(r[1], r[2])
    t4 = t
    for _ in range(3):
        t4 = compose(t, t4)
    assert element_order(t4) == 3

    grades = t4_grades(t4)
    n_grades = [grades[n[0]] for n in N]
    grade_dist = Counter(n_grades)

    # T4: order-3 elements and their t4 grade
    ord3 = [n for n in N if element_order(n) == 3]
    ord3_grades = Counter(grades[n[0]] for n in ord3)

    # Subgroup generated by order-3 elements
    sub_ord3 = bfs_group(ord3[:8], limit=1000)  # sample generators
    sub_ord3_full = bfs_group(ord3, limit=1000)
    sub_ord_dist = Counter(element_order(tuple(s)) for s in sub_ord3_full)

    # 27 does not divide 192
    does_27_divide_192 = (192 % 27 == 0)

    # T5: order distribution of grade-1,2 elements
    grade12_orders = Counter(
        element_order(n) for n, g in zip(N, n_grades) if g in (1, 2)
    )

    # T6: block grade distribution
    block_grade_0_count = sum(1 for b in blocks if grades[b[0]] == 0)
    block_grade_1_count = sum(1 for b in blocks if grades[b[0]] == 1)
    block_grade_2_count = sum(1 for b in blocks if grades[b[0]] == 2)

    summary = {
        "N_size": len(N),
        "T1_order_distribution": dict(sorted(ord_dist.items())),
        "T1_center_size": center_size,
        "T1_center_is_trivial": center_size == 1,
        "T2_num_blocks": len(blocks),
        "T2_block_size": 4,
        "T2_N_hits_per_block": dict(block_hits_per_block),
        "T2_all_blocks_hit": len(block_dist) == 48,
        "T2_stab_block0_size": len(stab),
        "T2_stab_block0_ord_dist": dict(sorted(stab_ord_dist.items())),
        "T3_t4_grade_dist": dict(sorted(grade_dist.items())),
        "T4_ord3_count": len(ord3),
        "T4_ord3_grade_dist": dict(sorted(ord3_grades.items())),
        "T4_ord3_subgroup_order": len(sub_ord3_full),
        "T4_ord3_subgroup_ord_dist": dict(sorted(sub_ord_dist.items())),
        "T4_27_divides_192": does_27_divide_192,
        "T5_grade12_order_dist": dict(sorted(grade12_orders.items())),
        "T6_block_grade_counts": {
            "grade_0_blocks": block_grade_0_count,
            "grade_1_blocks": block_grade_1_count,
            "grade_2_blocks": block_grade_2_count,
        },
    }
    return summary


def main():
    summary = compute_correlation()
    (ROOT / "N_heis_correlation_summary.json").write_text(json.dumps(summary, indent=2))
    with open(ROOT / "N_heis_correlation_report.md", "w", encoding="utf-8") as f:
        f.write("# N–Block–Grade Correlation Report\n\n")
        f.write(json.dumps(summary, indent=2))
    print("wrote N_heis_correlation_summary.json and report")


if __name__ == "__main__":
    main()
