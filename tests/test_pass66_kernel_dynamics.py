"""Pass 66: kernel dynamics -- stationarity, the rebuilt line, the pipeline, the self-logging fabric.

- the cheap-channel graph on the 360 grounds is 8-regular and connected (=> uniform stationary walk);
- the rebuilt-line rule holds for all 480 ordered edges, and the 3 rebuilt center-quads meet in
  exactly the old center;
- a live pipeline runs router programs with dynamic page placement across relocations, outputs
  correct, and every relocation origin decodes uniquely from 3 markers + geometry alone.
"""

import os
import random
import sys

import numpy as np

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_kernel_dynamics as kd  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_packet_vm_kernel as pvk  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tritcpu_emulator as tcpu  # noqa: E402


def test_cheap_channel_graph_connected_regular():
    pts, A, lines, B = audit._build(3)
    olist, M = kd.cheap_channel_graph(pts, A, lines, B)
    assert len(olist) == 360
    assert set(M.sum(1)) == {8}
    seen, fr = {0}, [0]
    while fr:
        nxt = []
        for x in fr:
            for y in np.nonzero(M[x])[0]:
                if int(y) not in seen:
                    seen.add(int(y))
                    nxt.append(int(y))
        fr = nxt
    assert len(seen) == 360, "cheap-channel graph must be connected"


def test_rebuilt_line_rule_and_intersection():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    assert kd.rebuilt_line_rule(pts, A, lines, n)
    # the 3 rebuilt center-quads meet in exactly {old center}, for every ordered edge
    import w33_interrupt_controller as ic

    for p in range(n):
        for p2 in (x for x in range(n) if A[p][x]):
            tbl2, _ = ic.vector_table(p2, pts, A, lines, n)
            quads = [set(perp) for (_, _, perp) in tbl2 if p in perp]
            assert set.intersection(*quads) == {p}


def test_pipeline_and_self_logging():
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    spreads = anat.enumerate_spreads(lines, n)
    ker = kd.SelfLoggingKernel(
        pts, A, lines, n, spreads, center=0, threshold=2, seed=13
    )
    ker.pts = pts
    vm = pvk.PacketKernelVM(ker, A, lines, ram_point=ker.ram_point)
    rng = random.Random(21)
    for _ in range(120):
        x, y = pts[rng.randrange(n)], pts[rng.randrange(n)]
        assert vm.run(tcpu.PROGRAM, mem := list(x) + list(y) + [0]) == B(x, y)
        for _ in range(8):
            ker.service(rng.randrange(len(lines)))
    assert not ker.invariant_failures
    decoded, truth = ker.decode_walk()
    assert len(truth) > 10
    assert (
        decoded == truth
    ), "every relocation origin must decode uniquely from the markers"
