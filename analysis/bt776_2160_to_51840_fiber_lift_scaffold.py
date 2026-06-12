#!/usr/bin/env python3
"""BT776 — 2160-to-51840 fiber-lift scaffold.

BT773 proved the intrinsic selector bus

    2160 = 45*48 = 540*4 = 240*9.

This verifier builds the deterministic 24-fold local tetrad lift over that bus:

    51840 = 2160 * 24 = 45 * 48 * 24.

The 24 fiber labels are the 4! ordered tetrads of the packet half opposite the
stored nonedge.  This is the correct cardinal bridge to the full root-torsor
stack, but it is deliberately named a scaffold: it does not claim the missing
BT763 root-torsor-to-Q(4,3) transport table has been constructed.
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
OUT = ROOT / "data" / "PART_BT776_2160_TO_51840_FIBER_LIFT_SCAFFOLD_summary.json"
SAMPLE = ROOT / "data" / "generated_octet_packets" / "bt776_51840_lift_sample.json"


def main():
    pts, lines, idx, G, point_lines = build_w33()
    packets = make_packets(G)
    nonedges, nonedge_to_id, line_pair_to_id, charts, chart_nonedges, chart_key_to_id = build_chart_system(G, lines, idx, point_lines)

    slots = []
    for packet in packets:
        pid = packet["packet_id"]
        A = tuple(packet["half_a"])
        B = tuple(packet["half_b"])
        for half_name, half, opposite in (("A", A, B), ("B", B, A)):
            for u, v in itertools.combinations(half, 2):
                e = tuple(sorted((u, v)))
                eid = nonedge_to_id[e]
                for selector in opposite:
                    l1 = line_pair_to_id[tuple(sorted((selector, u)))]
                    l2 = line_pair_to_id[tuple(sorted((selector, v)))]
                    cid = chart_key_to_id[(selector, min(l1, l2), max(l1, l2))]
                    slots.append({
                        "slot_id": len(slots),
                        "packet_id": pid,
                        "half": half_name,
                        "opposite_half": opposite,
                        "stored_nonedge_id": eid,
                        "selector_center": selector,
                        "chart_id": cid,
                    })

    rows = []
    packet_count = Counter()
    slot_count = Counter()
    chart_count = Counter()
    nonedge_count = Counter()
    fiber_count = Counter()
    for s in slots:
        for fiber_id, order in enumerate(itertools.permutations(s["opposite_half"])):
            row_id = len(rows)
            if row_id < 12:
                rows.append({
                    "row_id": row_id,
                    "slot_id": s["slot_id"],
                    "packet_id": s["packet_id"],
                    "chart_id": s["chart_id"],
                    "stored_nonedge_id": s["stored_nonedge_id"],
                    "selector_center": s["selector_center"],
                    "fiber_id": fiber_id,
                    "ordered_opposite_tetrad": list(order),
                })
            packet_count[s["packet_id"]] += 1
            slot_count[s["slot_id"]] += 1
            chart_count[s["chart_id"]] += 1
            nonedge_count[s["stored_nonedge_id"]] += 1
            fiber_count[fiber_id] += 1

    total_rows = sum(slot_count.values())
    checks = {
        "base_slots_2160": len(slots) == 2160,
        "fiber_size_24": Counter(slot_count.values()) == Counter({24: 2160}),
        "total_rows_51840": total_rows == 51840,
        "packets_45_each_1152": len(packet_count) == 45 and Counter(packet_count.values()) == Counter({1152: 45}),
        "charts_240_each_216": len(chart_count) == 240 and Counter(chart_count.values()) == Counter({216: 240}),
        "nonedges_540_each_96": len(nonedge_count) == 540 and Counter(nonedge_count.values()) == Counter({96: 540}),
        "fiber_labels_24_each_2160": len(fiber_count) == 24 and Counter(fiber_count.values()) == Counter({2160: 24}),
    }

    sample_payload = {
        "bt776_schema_version": "1.0",
        "description": "First 12 rows of the 2160*24 local tetrad lift scaffold.",
        "boundary": "Sample only; full row set is generated deterministically by the verifier.",
        "rows": rows,
    }
    SAMPLE.parent.mkdir(parents=True, exist_ok=True)
    SAMPLE.write_text(json.dumps(sample_payload, indent=2, sort_keys=True) + "\n")

    result = {
        "theorem": "BT776 2160-to-51840 Fiber-Lift Scaffold",
        "factorization": {
            "root_torsor_cardinality": "51840 = 2160 * 24",
            "packet_form": "51840 = 45 packets * 48 selector slots * 24 ordered tetrads",
            "chart_form": "51840 = 240 charts * 9 stored nonedge incidences * 24 ordered tetrads",
        },
        "summary": {
            "base_slots": len(slots),
            "fiber_size": 24,
            "total_rows": total_rows,
            "packets": len(packet_count),
            "charts": len(chart_count),
            "nonedges": len(nonedge_count),
            "fiber_labels": len(fiber_count),
            "sample_payload": str(SAMPLE.relative_to(ROOT)),
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This is a cardinal and incidence-compatible 24-fold scaffold over the BT773 bus. It is not the full BT763 root-torsor transport table."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
