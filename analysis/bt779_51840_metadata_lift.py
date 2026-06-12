#!/usr/bin/env python3
"""BT779 — 51840 metadata lift over the BT776 scaffold.

Adds a deterministic 540*2*48 metadata shape over the BT773/BT776 bus.
The 540 ids are W33 stored nonedges.  The 2-way bit is permutation parity.
The 48-way id is selector_index*12 + parity_rank.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from bt766_intrinsic_k44_octet_quotient import build_w33
from bt770_octet_nonedge_packet_abi import make_packets
from bt773_octet_packet_selector_bus import build_chart_system

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT779_51840_METADATA_LIFT_summary.json"


def parity(seq):
    n = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                n += 1
    return n % 2


def parity_ranks(base):
    perms = sorted(itertools.permutations(base))
    out = {0: {}, 1: {}}
    for bit in (0, 1):
        bucket = [p for p in perms if parity([base.index(x) for x in p]) == bit]
        for i, p in enumerate(bucket):
            out[bit][p] = i
    return out


def main():
    pts, lines, idx, G, point_lines = build_w33()
    packets = make_packets(G)
    nonedges, nonedge_to_id, line_pair_to_id, charts, chart_nonedges, chart_key_to_id = build_chart_system(G, lines, idx, point_lines)

    triple_count = Counter()
    id540_count = Counter()
    bit_count = Counter()
    id48_count = Counter()
    packet_count = Counter()
    chart_count = Counter()
    total = 0

    for packet in packets:
        pid = packet["packet_id"]
        A = tuple(packet["half_a"])
        B = tuple(packet["half_b"])
        for half, opposite in ((A, B), (B, A)):
            opposite = tuple(sorted(opposite))
            ranks = parity_ranks(opposite)
            for u, v in itertools.combinations(half, 2):
                id540 = nonedge_to_id[tuple(sorted((u, v)))]
                for selector_index, selector in enumerate(opposite):
                    l1 = line_pair_to_id[tuple(sorted((selector, u)))]
                    l2 = line_pair_to_id[tuple(sorted((selector, v)))]
                    chart_id = chart_key_to_id[(selector, min(l1, l2), max(l1, l2))]
                    for order in sorted(itertools.permutations(opposite)):
                        rel = [opposite.index(x) for x in order]
                        bit = parity(rel)
                        id48 = selector_index * 12 + ranks[bit][order]
                        triple_count[(id540, bit, id48)] += 1
                        id540_count[id540] += 1
                        bit_count[bit] += 1
                        id48_count[id48] += 1
                        packet_count[pid] += 1
                        chart_count[chart_id] += 1
                        total += 1

    checks = {
        "rows_51840": total == 51840,
        "ids_540_each_96": len(id540_count) == 540 and Counter(id540_count.values()) == Counter({96: 540}),
        "bits_2_each_25920": bit_count == Counter({0: 25920, 1: 25920}),
        "ids_48_each_1080": len(id48_count) == 48 and Counter(id48_count.values()) == Counter({1080: 48}),
        "triples_540_2_48_once": len(triple_count) == 540 * 2 * 48 and Counter(triple_count.values()) == Counter({1: 540 * 2 * 48}),
        "packets_45_each_1152": len(packet_count) == 45 and Counter(packet_count.values()) == Counter({1152: 45}),
        "charts_240_each_216": len(chart_count) == 240 and Counter(chart_count.values()) == Counter({216: 240}),
    }

    result = {
        "theorem": "BT779 51840 Metadata Lift",
        "factorization": "51840 = 540 * 2 * 48",
        "rule": {
            "id540": "stored W33 nonedge id",
            "bit2": "ordered opposite tetrad parity",
            "id48": "selector_index * 12 + parity_rank",
        },
        "summary": {
            "rows": total,
            "id540_count": len(id540_count),
            "bit_count": len(bit_count),
            "id48_count": len(id48_count),
            "packet_count": len(packet_count),
            "chart_count": len(chart_count),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This proves a deterministic 540*2*48 metadata lift over the BT776 scaffold. It is still a candidate shape, not the missing external row table."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
