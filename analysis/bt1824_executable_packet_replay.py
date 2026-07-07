#!/usr/bin/env python3
"""BT1824: executable seeded-vs-compiled packet replay.

Runs the committed 1600-input TritCPU router workload twice: once through the
original Pass-65 InterruptController and once through the BT1823 compiled
controller now exposed by w33_packet_vm_kernel. The semantic expectation is zero
output mismatch; the controller counters may differ only in relocation-phase
bookkeeping.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_packet_vm_kernel as kernel  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tritcpu_emulator as tcpu  # noqa: E402

OUT = Path("data/PART_BT1824_EXECUTABLE_PACKET_REPLAY_results.json")


def run_workload(controller_cls):
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    spreads = anat.enumerate_spreads(lines, n)
    ctl = controller_cls(pts, A, lines, n, spreads, center=0, threshold=6, seed=11)
    vm = kernel.PacketKernelVM(ctl, A, lines)
    mismatches = 0
    truth_mismatches = 0
    for x in pts:
        for y in pts:
            mem = list(x) + list(y) + [0]
            direct = tcpu.TritCPU().run(tcpu.PROGRAM, mem)
            wrapped = vm.run(tcpu.PROGRAM, mem)
            truth = B(x, y)
            mismatches += int(wrapped != direct)
            truth_mismatches += int(wrapped != truth)
    reloc = ctl.counters["relocations"]
    avg_cost = ctl.counters["migration_cost_rays"] / max(reloc, 1)
    return {
        "mismatches_direct": mismatches,
        "mismatches_truth": truth_mismatches,
        "vm_counters": dict(vm.counters),
        "controller_counters": dict(ctl.counters),
        "relocations": reloc,
        "avg_migration_cost_rays": avg_cost,
        "invariant_failures": list(ctl.invariant_failures),
        "compiled_trace_len": len(getattr(ctl, "compiled_relocation_trace", [])),
    }


def theorem_summary():
    seeded = run_workload(ic.InterruptController)
    compiled = run_workload(kernel.CompiledInterruptController)
    checks = {
        "seeded_zero_mismatches": seeded["mismatches_direct"] == seeded["mismatches_truth"] == 0,
        "compiled_zero_mismatches": compiled["mismatches_direct"] == compiled["mismatches_truth"] == 0,
        "compiled_selector_fires_once_per_relocation": compiled["compiled_trace_len"] == compiled["relocations"],
        "both_keep_avg_migration_cost_three": seeded["avg_migration_cost_rays"] == compiled["avg_migration_cost_rays"] == 3.0,
        "no_invariant_failures": not seeded["invariant_failures"] and not compiled["invariant_failures"],
    }
    return {
        "theorem": "BT1824 Executable Packet Replay",
        "workload": "1600 ordered W33 point pairs through the 22-instruction TritCPU router",
        "seeded_controller": seeded,
        "compiled_controller": compiled,
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Executable replay script. Results are generated when the script is run in the repo environment; this connector commit adds the executable witness."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
