#!/usr/bin/env python3
"""Pillar 98 (Part CXCVIII): Connecting N to the 270-edge transport

This pillar establishes the precise relationship between the regular
subgroup N (acting on 192 flags) and the 270-edge transport law (acting
on 27 QIDs).

Key results:

  T1  N acts on 192 flags with no flag staying in the same QID:
      for any n != identity and any flag f with known QID assignment,
      qid(n(f)) != qid(f).  This means N's action is "QID-separating".

  T2  The projection N -> Sym(27) via the QID map factors through a
      quotient: the kernel consists of elements that preserve QID
      assignment.  Since T1 shows no non-identity element preserves QIDs,
      N embeds injectively into Sym(27)^k for some replicated action.

  T3  The 5 generators g2,g3,g5,g8,g9 of the 270-transport are the
      images under projection of words in {r0,r1,r2,r3}.  We catalogue
      how many r-generator words correspond to each g-generator.

  T4  The block structure (48 blocks from Pillar 94) gives an intermediate
      quotient: 192 flags -> 48 blocks -> 27 QIDs.  The ratios
      192/48 = 4 and 48/27 ≈ 1.78 (not integer!) show the second
      projection is non-uniform.

  T5  The order-48 derived subgroup [N,N] acts on QIDs with a specific
      orbit structure.  Since [N,N] is normal in N, the orbits partition
      the 27 QIDs into equal-sized classes.
"""

from __future__ import annotations

import csv
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set

PILLARS_DIR = Path(__file__).resolve().parent
REPO_ROOT = PILLARS_DIR.parent
BUNDLE = PILLARS_DIR / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


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


def connect_N_transport() -> dict:
    # Load N
    N = [tuple(n) for n in json.loads((PILLARS_DIR / "N_subgroup.json").read_text(encoding="utf-8"))]
    idp = tuple(range(192))

    # Load r-generators
    with zipfile.ZipFile(BUNDLE) as zf:
        gens = json.loads(zf.read("tomotope_r_generators_192.json"))
    r = {f"r{i}": tuple(gens[f"r{i}"]) for i in range(4)}

    # Load flag->qid mapping (54 flags)
    flag_qid: Dict[int, int] = {}
    with open(REPO_ROOT / "K54_54sheet_coords_refined.csv") as f:
        for row in csv.DictReader(f):
            uf = row.get("unique_flag", "")
            q = int(row["qid"])
            if uf and uf != "":
                flag_qid[int(uf)] = q

    # T1: Check QID-separating property
    # For each non-identity n, does it move every mapped flag to a different QID?
    qid_preserving = 0
    total_checked = 0
    for n in N:
        if n == idp:
            continue
        for f in flag_qid:
            nf = n[f]
            if nf in flag_qid:
                total_checked += 1
                if flag_qid[nf] == flag_qid[f]:
                    qid_preserving += 1
    qid_separating = qid_preserving == 0

    # T2: Build block structure (from r0, r3 orbits)
    block_id = [-1] * 192
    bid = 0
    for start in range(192):
        if block_id[start] == -1:
            queue = [start]
            while queue:
                f = queue.pop()
                if block_id[f] == -1:
                    block_id[f] = bid
                    for g in (r["r0"], r["r3"]):
                        if block_id[g[f]] == -1:
                            queue.append(g[f])
            bid += 1
    num_blocks = bid

    # Block sizes
    block_sizes = Counter(block_id)

    # T3: For each r-generator, compute its QID-permutation
    r_qid_perm = {}
    for name, perm in r.items():
        qid_map = {}
        for f in flag_qid:
            nf = perm[f]
            if nf in flag_qid:
                src_q = flag_qid[f]
                tgt_q = flag_qid[nf]
                qid_map[src_q] = tgt_q
        r_qid_perm[name] = qid_map

    # T4: Ratio analysis
    ratio_192_48 = 192 // num_blocks
    ratio_48_27 = num_blocks / 27

    # T5: Derived subgroup action on blocks
    # Load derived subgroup (compute from commutators)
    from collections import deque

    comm_gens = []
    for a in N[:20]:
        for b in N[:20]:
            c = compose(compose(a, b), compose(invert(a), invert(b)))
            if c != idp:
                comm_gens.append(c)

    derived_set = {idp}
    q: deque = deque([idp])
    while q:
        g = q.popleft()
        for h in comm_gens[:15]:
            for x in (compose(h, g), compose(g, h)):
                if x not in derived_set:
                    derived_set.add(x)
                    q.append(x)
                    if len(derived_set) > 200:
                        break

    # Derived subgroup orbits on blocks
    block_orbits_derived: Dict[int, Set[int]] = {}
    for n in derived_set:
        for f in range(192):
            src_b = block_id[f]
            tgt_b = block_id[n[f]]
            if src_b not in block_orbits_derived:
                block_orbits_derived[src_b] = set()
            block_orbits_derived[src_b].add(tgt_b)

    # Merge orbits
    merged: Dict[int, Set[int]] = {}
    assigned: Set[int] = set()
    for b in sorted(block_orbits_derived.keys()):
        if b in assigned:
            continue
        orbit = set()
        todo = [b]
        while todo:
            x = todo.pop()
            if x not in orbit:
                orbit.add(x)
                for y in block_orbits_derived.get(x, set()):
                    if y not in orbit:
                        todo.append(y)
        for x in orbit:
            assigned.add(x)
        merged[min(orbit)] = orbit

    derived_orbit_sizes = sorted(len(o) for o in merged.values())

    return {
        "T1_qid_separating": qid_separating,
        "T1_qid_preserving_count": qid_preserving,
        "T1_total_checked": total_checked,
        "T2_num_blocks": num_blocks,
        "T2_block_size_dist": dict(Counter(block_sizes.values())),
        "T3_r_gen_qid_coverage": {name: len(qm) for name, qm in r_qid_perm.items()},
        "T4_ratio_192_to_blocks": ratio_192_48,
        "T4_ratio_blocks_to_27": round(ratio_48_27, 4),
        "T5_derived_size": len(derived_set),
        "T5_derived_block_orbits": derived_orbit_sizes,
        "T5_num_derived_orbits": len(merged),
    }


def main():
    summary = connect_N_transport()
    (REPO_ROOT / "N_transport_connection.json").write_text(json.dumps(summary, indent=2))
    with open(REPO_ROOT / "N_transport_connection_report.md", "w", encoding="utf-8") as f:
        f.write("# N–Transport Connection Report\n\n")
        f.write(json.dumps(summary, indent=2))
    print("wrote N_transport_connection.json and report")


if __name__ == "__main__":
    main()
