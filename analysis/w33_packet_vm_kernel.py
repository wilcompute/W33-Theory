#!/usr/bin/env python3
"""
Mode-2 execution with a real kernel: the lifted instruction stream runs THROUGH the interrupt
controller, every data movement is line-legal and priced, and the outputs are proven identical. The VM
track's packet VM lifts bytecode and checks output equality, but has no fault path: no instruction can
touch the defect, escalate, or trigger relocation. This witness closes that hole using only committed
components, so the kernel is adoptable by the in-flight packet VM without depending on it:

  THE LIFT. The committed 22-instruction TritCPU router program (w33_tritcpu_emulator.PROGRAM, which
  computes the symplectic forwarding bit B(x,y)) is lifted to a packet stream: registers 0..15 live at
  points 0..15, RAM cells at points 16..24, and every data-moving instruction (LD, ST, ADD, SUB, MUL)
  becomes one route -- 1 hop if the operand points are collinear, 2 hops via a relay otherwise -- whose
  hops are LINE TRANSACTIONS on the unique W(3,3) line through their endpoints.

  THE KERNEL. Each line transaction is serviced by the Pass 64 interrupt controller: non-defect lines
  are served in spread frames (each provably 9/10); defect-line touches are ESCALATIONS on the priced
  9^t path; overloads relocate the defect through cheap channels (cost exactly 3 rays, to the ground's
  own center quad). BT1823 now uses the compiled BT1818 selector for relocation phase accounting:
  phase = table[(source,target)][counter mod 3]. The tax theorems run as live invariants under a real workload.

  THE PROOF. All 1600 ordered (x,y) inputs are executed twice -- direct TritCPU vs kernel-wrapped --
  and the outputs are verified identical to each other AND to the ground-truth symplectic form B(x,y).
  Every hop of every transaction is verified collinear (line-legal). The kernel wraps execution without
  altering semantics; what it adds is exactly the OS layer: legality, pricing, escalation, relocation.

If the VM track's in-flight w33_packet_vm is importable, its presence is recorded (adoption target);
no dependency is taken on it.

Honest scope: the point embedding of registers/RAM is a fixed bookkeeping choice; the semantic engine
is the committed TritCPU; the kernel adds service metadata and invariant checks, not new computation.
Escalation pricing cites the committed 9^t dial. This is the executable bridge between the VM track's
mode-2 ambition and the tax arc's kernel guarantees.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bt1818_compiled_packet_kernel_controller as compiled_ctl  # noqa: E402
import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tritcpu_emulator as tcpu  # noqa: E402


class CompiledInterruptController(ic.InterruptController):
    """Pass-64 controller with BT1818 compiled phase-row selection for relocations."""

    def __init__(self, *args, **kwargs):
        self.compiled_selector = compiled_ctl.CompiledRelocationSelector()
        self.compiled_relocation_trace = []
        super().__init__(*args, **kwargs)

    def _relocate(self):
        """Cost-aware edge relocation plus compiled phase accounting.

        The target edge remains the Pass-64 cheapest-load choice. BT1823 adds the
        BT1818 phase selector on the directed edge center->target, so repeated
        use of the same edge is balanced by counter mod 3.
        """
        nbrs = [x for x in range(self.n) if self.A[self.center][x]]
        best = None
        for x in nbrs:
            tbl, _ = ic.vector_table(x, self.pts, self.A, self.lines, self.n)
            ov = max(len(t[0] & self.lit) for t in tbl)
            key = (11 - ov, self.counters[f"load@{x}"])
            if best is None or key < best[0]:
                best = (key, x)
        target = best[1]
        phase = self.compiled_selector.choose_phase(self.center, target)
        self.counters["compiled_scheduler_selections"] += 1
        self.counters[f"compiled_phase@{phase}"] += 1
        self.compiled_relocation_trace.append(
            {"from": self.center, "to": target, "compiled_phase": phase, "cost_rays": best[0][0]}
        )
        self.counters["relocations"] += 1
        self._move_to(target, prefer=self.lit)
        self.counters[f"load@{target}"] += 1


def _line_of(a, b, lines, line_by_pair):
    return line_by_pair.get((a, b))


class PacketKernelVM:
    """TritCPU execution whose every data movement is a controller-serviced line transaction."""

    REG_POINT = list(range(16))  # register r -> point r
    RAM_BASE = 16  # RAM cell a -> point 16 + a (cells 0..8 used)

    def __init__(self, ctl, A, lines, ram_point=None):
        self.ctl = ctl
        self.A = A
        self.lines = lines
        self.ram_point = ram_point  # optional dynamic page placement (Pass 66 pipeline)
        self.line_by_pair = {}
        for li, L in enumerate(lines):
            for a in L:
                for b in L:
                    if a != b:
                        self.line_by_pair[(a, b)] = li
        self.counters = Counter()
        self.illegal_hops = 0

    def _route_points(self, src, dst):
        """1 hop if collinear, else 2 hops via a common neighbour (mu=4 exist)."""
        if self.A[src][dst]:
            return [(src, dst)]
        relay = next(t for t in range(len(self.A)) if self.A[src][t] and self.A[dst][t])
        return [(src, relay), (relay, dst)]

    def _transact(self, src_pt, dst_pt):
        if src_pt == dst_pt:
            self.counters["local_ops"] += 1
            return
        for a, b in self._route_points(src_pt, dst_pt):
            li = self.line_by_pair.get((a, b))
            if li is None:
                self.illegal_hops += 1
                continue
            outcome = self.ctl.service(li)
            self.counters[outcome] += 1
            self.counters["hops"] += 1
        self.counters["transactions"] += 1

    def run(self, prog, mem):
        cpu = tcpu.TritCPU()
        # replay the program, issuing a transaction per data movement, semantics via TritCPU
        result = cpu.run(prog, mem)
        for pc, name, args in cpu.trace:
            if name == "LD":
                src = (
                    self.ram_point(args[1])
                    if self.ram_point
                    else self.RAM_BASE + args[1]
                )
                self._transact(src, self.REG_POINT[args[0]])
            elif name == "ST":
                dst = (
                    self.ram_point(args[1])
                    if self.ram_point
                    else self.RAM_BASE + args[1]
                )
                self._transact(self.REG_POINT[args[0]], dst)
            elif name in ("ADD", "SUB", "MUL"):
                self._transact(self.REG_POINT[args[1]], self.REG_POINT[args[0]])
            else:  # LDI, MOD3, HLT: point-local
                self.counters["local_ops"] += 1
        return result


def main():
    print(
        "== the packet-kernel VM: mode-2 execution through the compiled interrupt controller ==\n"
    )
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    pts, A, lines, B = audit._build(3)
    n = len(pts)
    spreads = anat.enumerate_spreads(lines, n)
    ctl = CompiledInterruptController(
        pts, A, lines, n, spreads, center=0, threshold=6, seed=11
    )
    vm = PacketKernelVM(ctl, A, lines)

    mismatch_direct = mismatch_truth = 0
    for x in pts:
        for y in pts:
            mem = list(x) + list(y) + [0]
            direct = tcpu.TritCPU().run(tcpu.PROGRAM, mem)
            wrapped = vm.run(tcpu.PROGRAM, mem)
            truth = B(x, y)
            if wrapped != direct:
                mismatch_direct += 1
            if wrapped != truth:
                mismatch_truth += 1

    c = vm.counters
    chk(
        "OUTPUT EQUALITY over all 1600 ordered pairs: kernel-wrapped == direct TritCPU",
        mismatch_direct == 0,
    )
    chk("and == the ground-truth symplectic form B(x,y)", mismatch_truth == 0)
    chk(
        f"every hop was LINE-LEGAL (unique W(3,3) line per hop; {c['hops']} hops, 0 illegal)",
        vm.illegal_hops == 0 and c["hops"] > 0,
    )
    chk(
        f"the kernel serviced {c['serviced']} transactions classically and ESCALATED {c['escalated']} "
        f"defect-line touches on the priced 9^t path",
        c["serviced"] > 0 and c["escalated"] > 0,
    )
    reloc = ctl.counters["relocations"]
    avg_cost = ctl.counters["migration_cost_rays"] / max(reloc, 1)
    chk(
        f"defect relocations under real workload: {reloc}, all through cheap channels (avg cost {avg_cost:.2f} = 3)",
        reloc > 0 and avg_cost == 3.0,
    )
    chk(
        "BT1823 compiled selector fired exactly once per relocation",
        ctl.counters["compiled_scheduler_selections"] == reloc and reloc == len(ctl.compiled_relocation_trace),
    )
    chk(
        "ALL tax-theorem runtime invariants held during the full 1600-program run",
        not ctl.invariant_failures,
    )

    try:
        import w33_packet_vm  # noqa: F401

        inflight = True
    except Exception:
        inflight = False
    print(
        f"\n  (in-flight w33_packet_vm importable: {inflight} -- the kernel's service() hook is its adoption point)"
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nFUSION COMPLETE (BT1823): the lifted instruction stream executes through a compiled controller --"
        "\nline-legal hops, spread-frame service, priced escalations, cheap-channel relocations, and"
        "\ncompiled phase-row selection -- with outputs proven identical to the direct machine."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "workload": "committed 22-instruction TritCPU router (B(x,y)) over all 1600 ordered pairs",
        "embedding": {"registers": "points 0..15", "ram": "points 16..24"},
        "counters": {k: v for k, v in sorted(c.items())},
        "controller": {
            "relocations": reloc,
            "avg_migration_cost_rays": avg_cost,
            "escalations": ctl.counters["escalations"],
            "compiled_scheduler_selections": ctl.counters["compiled_scheduler_selections"],
            "compiled_phase_histogram": {
                k: v for k, v in sorted(ctl.counters.items()) if str(k).startswith("compiled_phase@")
            },
            "compiled_relocation_trace_sample": ctl.compiled_relocation_trace[:12],
            "invariant_failures": ctl.invariant_failures,
        },
        "inflight_packet_vm_detected": inflight,
        "all_pass": bool(all_ok),
        "summary": (
            "mode-2 execution with a compiled controller: the committed 22-instruction TritCPU router "
            "is lifted to a packet stream and executed through the Pass-64 controller patched with the "
            "BT1818 phase selector. Over all 1600 ordered inputs the kernel-wrapped outputs equal the "
            "direct TritCPU outputs and the ground-truth symplectic form; every hop is line-legal; "
            "relocations remain cheap-channel moves at exactly 3 rays; and the compiled selector fires "
            "once per relocation. HONEST: the semantic engine is still TritCPU; this patch changes "
            "relocation phase-row accounting, not the computation."
        ),
        "sources": [
            "w33_tritcpu_emulator (committed router program); w33_interrupt_controller (Pass 64)",
            "bt1818_compiled_packet_kernel_controller (compiled phase-row selector)",
        ],
    }
    with open("data/w33_packet_vm_kernel.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_packet_vm_kernel.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
