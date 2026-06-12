#!/usr/bin/env python3
"""BT773 — 2160 octet packet selector bus theorem.

BT770 gives 45 octet packets.  Each packet contains 12 stored W33 nonedges:
6 inside one K4 half and 6 inside the opposite K4 half.  Every stored nonedge
has exactly four opposite-half selector centers.  Therefore each packet has
12*4 = 48 selector slots and the full bus has

    45 * 48 = 2160 = 540 * 4.

This verifier proves that these 2160 packet slots are exactly the chart/nonedge
incidences of the 240 centered local K_{3,3} charts, each chart containing 9
W33 nonedges.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

from bt766_intrinsic_k44_octet_quotient import build_w33
from bt770_octet_nonedge_packet_abi import make_packets

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT773_OCTET_PACKET_SELECTOR_BUS_summary.json"


def build_chart_system(G, lines, idx, point_lines):
    nonedges = []
    nonedge_to_id = {}
    for a, b in itertools.combinations(range(40), 2):
        if not G.has_edge(a, b):
            e = tuple(sorted((a, b)))
            nonedge_to_id[e] = len(nonedges)
            nonedges.append(e)

    line_pair_to_id = {}
    for li, L in enumerate(lines):
        ids = sorted(idx[p] for p in L)
        for a, b in itertools.combinations(ids, 2):
            line_pair_to_id[tuple(sorted((a, b)))] = li

    charts = []
    chart_nonedges = []
    chart_key_to_id = {}
    for p in range(40):
        for l1, l2 in itertools.combinations(sorted(point_lines[p]), 2):
            A = sorted(idx[x] for x in lines[l1] if idx[x] != p)
            B = sorted(idx[x] for x in lines[l2] if idx[x] != p)
            nes = tuple(sorted(nonedge_to_id[tuple(sorted((a, b)))] for a in A for b in B))
            cid = len(charts)
            charts.append((p, l1, l2))
            chart_nonedges.append(nes)
            chart_key_to_id[(p, l1, l2)] = cid
    return nonedges, nonedge_to_id, line_pair_to_id, charts, chart_nonedges, chart_key_to_id


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
                    key = (selector, min(l1, l2), max(l1, l2))
                    cid = chart_key_to_id[key]
                    slots.append({
                        "packet_id": pid,
                        "half": half_name,
                        "stored_nonedge_id": eid,
                        "stored_nonedge": e,
                        "selector_center": selector,
                        "chart_id": cid,
                    })

    slot_pairs = {(s["chart_id"], s["stored_nonedge_id"]) for s in slots}
    chart_pairs = {(cid, eid) for cid, nes in enumerate(chart_nonedges) for eid in nes}

    packet_slot_count = Counter(s["packet_id"] for s in slots)
    nonedge_slot_count = Counter(s["stored_nonedge_id"] for s in slots)
    chart_slot_count = Counter(s["chart_id"] for s in slots)
    selector_count = Counter(s["selector_center"] for s in slots)

    checks = {
        "slot_count_2160": len(slots) == 2160,
        "packet_count_45_each_48_slots": len(packet_slot_count) == 45 and Counter(packet_slot_count.values()) == Counter({48: 45}),
        "nonedge_count_540_each_4_slots": len(nonedge_slot_count) == 540 and Counter(nonedge_slot_count.values()) == Counter({4: 540}),
        "chart_count_240_each_9_slots": len(chart_slot_count) == 240 and Counter(chart_slot_count.values()) == Counter({9: 240}),
        "selector_points_40_each_54_slots": len(selector_count) == 40 and Counter(selector_count.values()) == Counter({54: 40}),
        "packet_slots_equal_chart_nonedge_incidences": slot_pairs == chart_pairs,
        "all_slots_select_valid_centered_chart": all(s["stored_nonedge_id"] in chart_nonedges[s["chart_id"]] for s in slots),
    }

    result = {
        "theorem": "BT773 2160 Octet Packet Selector Bus Theorem",
        "factorizations": {
            "by_packet": "45 packets * 48 slots",
            "by_nonedge": "540 W33 nonedges * 4 opposite selectors",
            "by_chart": "240 centered local K3,3 charts * 9 nonedges",
        },
        "summary": {
            "slots": len(slots),
            "packets": len(packet_slot_count),
            "nonedges": len(nonedge_slot_count),
            "charts": len(chart_slot_count),
            "selector_centers": len(selector_count),
            "packet_slot_distribution": {str(k): int(v) for k, v in sorted(Counter(packet_slot_count.values()).items())},
            "nonedge_slot_distribution": {str(k): int(v) for k, v in sorted(Counter(nonedge_slot_count.values()).items())},
            "chart_slot_distribution": {str(k): int(v) for k, v in sorted(Counter(chart_slot_count.values()).items())},
            "selector_center_distribution": {str(k): int(v) for k, v in sorted(Counter(selector_count.values()).items())},
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This fuses the 45 packet ABI to the 2160 chart/nonedge selector bus. It is a W33-intrinsic incidence bijection, not a root-torsor transport table."
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
