#!/usr/bin/env python3
"""BT1818: compiled scheduler controller for the packet-kernel path.

This module is the direct integration target for w33_packet_vm_kernel.py: it
uses the BT1808/BT1814 three-row edge table as the relocation selector. The
controller keeps the Pass-64 semantics but replaces seed choice on a directed
edge by a counter modulo 3.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1808_td43_edge_scheduler as sched  # noqa: E402

OUT = Path("data/PART_BT1818_COMPILED_PACKET_KERNEL_CONTROLLER_results.json")


def compiled_edge_table():
    _pts, _adj, _lines, _rows, exposures, _schedule = sched.build_schedule()
    table = {}
    for edge, choices in exposures.items():
        ordered = sorted(choices, key=lambda x: (x["phase"], x["triad"], x["quad"]))
        table[edge] = [choice["phase"] for choice in ordered]
    return table


class CompiledRelocationSelector:
    def __init__(self):
        self.table = compiled_edge_table()
        self.counters = Counter()

    def choose_phase(self, source: int, target: int) -> int:
        choices = self.table[(source, target)]
        key = (source, target)
        phase = choices[self.counters[key] % len(choices)]
        self.counters[key] += 1
        return phase


def theorem_summary(rounds: int = 12):
    selector = CompiledRelocationSelector()
    assert len(selector.table) == 480
    assert {len(v) for v in selector.table.values()} == {3}
    loads = Counter()
    for edge in sorted(selector.table):
        for _ in range(rounds):
            phase = selector.choose_phase(*edge)
            loads[(edge, phase)] += 1
    assert len(loads) == 1440
    assert set(loads.values()) == {rounds // 3}
    return {
        "theorem": "BT1818 Compiled Packet-Kernel Controller Integration",
        "directed_edges": 480,
        "phase_rows_per_edge": 3,
        "compiled_rows": 1440,
        "selection_rule": "phase = table[(source,target)][counter[(source,target)] mod 3]",
        "checked_rounds_per_edge": rounds,
        "max_reuse_per_phase_row": rounds // 3,
        "checks": {
            "compiled_table_has_all_directed_edges": True,
            "three_phase_rows_per_edge": True,
            "counter_mod_3_balances_repeated_edge_use": True
        },
        "honest_scope": "Compiled relocation selector for the packet-kernel path. It preserves the finite scheduler law; full host CI was not run here."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
