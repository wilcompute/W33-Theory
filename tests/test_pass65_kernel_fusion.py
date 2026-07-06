"""Pass 65: the kernel fusion -- packet-kernel VM, defect-aware placement, walk telemetry.

- the lifted TritCPU router executes through the interrupt controller with outputs equal to the
  direct machine and the symplectic ground truth (sampled), all hops line-legal;
- placement: the 27-point safe zone is the AG(2,3) phase directory; the page bill is a constant
  9 points for every relocation (adjacent AND non-adjacent overlap = 18);
- telemetry: every relocation step lands in the pre-move center quad, along an edge, at 3 rays.
"""

import os
import random
import sys
from collections import Counter

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_defect_aware_placement as dap  # noqa: E402
import w33_defect_walk_telemetry as dwt  # noqa: E402
import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_packet_vm_kernel as pvk  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tritcpu_emulator as tcpu  # noqa: E402


def _setup():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    spreads = anat.enumerate_spreads(lines, n)
    return pts, A, lines, B, n, spreads


def test_kernel_vm_output_equality_sampled():
    pts, A, lines, B, n, spreads = _setup()
    ctl = ic.InterruptController(
        pts, A, lines, n, spreads, center=0, threshold=6, seed=1
    )
    vm = pvk.PacketKernelVM(ctl, A, lines)
    rng = random.Random(5)
    for _ in range(150):
        x, y = pts[rng.randrange(n)], pts[rng.randrange(n)]
        mem = list(x) + list(y) + [0]
        assert (
            vm.run(tcpu.PROGRAM, mem)
            == tcpu.TritCPU().run(tcpu.PROGRAM, mem)
            == B(x, y)
        )
    assert vm.illegal_hops == 0 and vm.counters["hops"] > 0
    assert not ctl.invariant_failures


def test_placement_bill_constant_nine():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    safe, triples, nb = dap.safe_zone_and_triples(0, pts, A, lines, n)
    assert sorted(x for t in triples for x in t) == safe and len(safe) == 27
    nonn = [frozenset(x for x in range(n) if x != p and not A[p][x]) for p in range(n)]
    ovs = {len(nonn[p] & nonn[q]) for p in range(n) for q in range(p + 1, n)}
    assert ovs == {18}, "safe-zone overlap must be a constant 18 for every center pair"


def test_walk_law_short_run():
    pts, A, lines, B, n, spreads = _setup()
    ctl = dwt.TelemetryController(
        pts, A, lines, n, spreads, center=0, threshold=2, seed=3
    )
    rng = random.Random(7)
    for _ in range(4000):
        ctl.service(rng.randrange(len(lines)))
    assert len(ctl.walk) >= 20
    for s in ctl.walk:
        assert s["to"] in s["quad"] and A[s["from"]][s["to"]] and s["cost_rays"] == 3
    assert not ctl.invariant_failures
