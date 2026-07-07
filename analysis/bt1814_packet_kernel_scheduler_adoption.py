#!/usr/bin/env python3
"""BT1814: packet-kernel adoption of the BT1808 compiled schedule."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402
import bt1808_td43_edge_scheduler as bt1808  # noqa: E402

OUT = Path("data/PART_BT1814_PACKET_KERNEL_SCHEDULER_ADOPTION_results.json")


def edge_slot_table():
    pts, adj, _lines, _rows, exposures, _schedule = bt1808.build_schedule()
    table = {}
    for edge, choices in exposures.items():
        ordered = sorted(choices, key=lambda x: (x["phase"], x["triad"], x["quad"]))
        table[edge] = [choice["phase"] for choice in ordered]
    return pts, adj, table


def theorem_summary(rounds: int = 12):
    pts, adj, table = edge_slot_table()
    assert len(table) == 480
    assert {len(v) for v in table.values()} == {3}

    use_counts = Counter()
    per_edge_max = {}
    for edge, phases in table.items():
        for i in range(rounds):
            phase = phases[i % 3]
            use_counts[(edge, phase)] += 1
        per_edge_max[edge] = max(use_counts[(edge, p)] for p in phases)

    assert set(per_edge_max.values()) == {rounds // 3}
    assert len(use_counts) == 1440

    return {
        "theorem": "BT1814 Packet-Kernel Compiled Scheduler Adoption Theorem",
        "directed_edges": 480,
        "phase_choices_per_edge": 3,
        "adoption_contract": "Packet-kernel relocation can choose the next phase row for edge p->q by table[(p,q)][counter % 3].",
        "checked_rounds_per_edge": rounds,
        "max_phase_reuse_per_edge": rounds // 3,
        "compiled_rows": 1440,
        "sample_edges": [{"edge": list(edge), "phases": phases} for edge, phases in list(sorted(table.items()))[:8]],
        "checks": {
            "all_directed_edges_have_three_compiled_phase_rows": True,
            "round_robin_use_is_balanced_for_checked_rounds": True,
            "packet_kernel_needs_counter_mod_3_only": True
        },
        "honest_scope": "Adoption witness for the packet-kernel relocation hook. It supplies the deterministic phase-row table; integrating it into a hardware driver remains an implementation task."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
