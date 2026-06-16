#!/usr/bin/env python3
"""BT1209 -- sample packet->centerquad isomorphisms for table dependence.

BT1208 writes the 2x2 table for one deterministic graph isomorphism.  This
sampler enumerates the first N isomorphisms supplied by NetworkX and computes the
raw/canonical Z2-vs-S3-sign table for each one.  It writes whether the table is
invariant over the sampled alignments.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "analysis", ROOT / "scripts", ROOT / "exploration", ROOT / "pillars"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from bt1208_raw_z2_s3_contingency_table_writer import contingency_for_mapping, packet_transport_with_s3
from exploration.w33_center_quad_transport_bridge import reconstructed_quotient_graph

OUT = ROOT / "data" / "PART_BT1209_ISOMORPHISM_DEPENDENCE_SAMPLE_results.json"


def table_signature(table: dict) -> tuple:
    return (
        tuple(sorted(table["raw_vs_s3_sign"].items())),
        tuple(sorted(table["canonical_vs_s3_sign"].items())),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-isomorphisms", type=int, default=64)
    args = parser.parse_args(argv)

    packet_graph, _s3_sign, _s3_perm = packet_transport_with_s3()
    center_graph, _raw = reconstructed_quotient_graph()
    matcher = nx.algorithms.isomorphism.GraphMatcher(packet_graph, center_graph)

    signature_counts: Counter[tuple] = Counter()
    examples = []
    for idx, mapping in enumerate(matcher.isomorphisms_iter()):
        if idx >= args.max_isomorphisms:
            break
        table = contingency_for_mapping(mapping)
        sig = table_signature(table)
        signature_counts[sig] += 1
        if len(examples) < 5:
            examples.append({"sample": idx, "raw_vs_s3_sign": table["raw_vs_s3_sign"], "canonical_vs_s3_sign": table["canonical_vs_s3_sign"]})

    payload = {
        "bt": 1209,
        "title": "isomorphism-dependence sample for Z2/S3 table",
        "max_isomorphisms_requested": args.max_isomorphisms,
        "samples_collected": sum(signature_counts.values()),
        "distinct_table_signatures": len(signature_counts),
        "sample_invariant": len(signature_counts) == 1,
        "examples": examples,
        "status": "invariance over sampled packet->centerquad graph isomorphisms is computed by this script",
        "checks": {
            "sampled_at_least_one": sum(signature_counts.values()) >= 1,
            "edge_count_720": packet_graph.number_of_edges() == center_graph.number_of_edges() == 720,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
