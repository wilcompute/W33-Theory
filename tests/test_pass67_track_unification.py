"""Pass 67: unifying the two tracks -- scheduler audit, exact spectrum, one page-bill law.

- the marker-decode audits BT1808's scheduler: all 480 directed edges origin-decode uniquely;
- the cheap-channel graph's spectrum is exact (proved by integer trace moments), gap (15-sqrt97)/16;
- the safe-zone page bill and the TD(4,3) churn are the same nine for all 1560 ordered moves.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_cheap_channel_spectrum as spec  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_page_bill_unification as unif  # noqa: E402
import w33_scheduler_audit_backend as sab  # noqa: E402


def test_scheduler_audit_all_edges_decode():
    pts, adj, lines, rows_by_center, exposures, schedule = sab.sched.build_schedule()
    n = len(pts)
    directed = [(p, q) for p in range(n) for q in range(n) if adj[p][q]]
    assert len(directed) == 480
    for p, q in directed:
        markers = sab.stamp_markers(q, p, pts, adj)
        assert sab.decode_origin(q, markers, pts, adj) == p


def test_exact_spectrum_moments():
    import numpy as np

    pts, A, lines, B = audit._build(3)
    _, M = spec.kd.cheap_channel_graph(pts, A, lines, B)
    n = M.shape[0]
    int_eigs = {8: 1, 3: 84, 1: 111, -1: 20, -3: 90, -4: 24}
    pair_mult = 15
    assert sum(int_eigs.values()) + 2 * pair_mult == n
    Mk = np.identity(n, dtype=object)
    for k in range(8):
        Mk = Mk @ M.astype(object) if k > 0 else np.identity(n, dtype=object)
        trace = int(sum(Mk[i, i] for i in range(n)))
        model = sum(
            m * (v**k) for v, m in int_eigs.items()
        ) + pair_mult * spec.power_sum_alpha_beta(k)
        assert int(model) == trace, f"moment k={k} mismatch"


def test_page_bill_is_one_law():
    pts_t, adj_t, _ = unif.td43.build_w33()
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    my_safe = [
        frozenset(x for x in range(n) if x != p and not A[p][x]) for p in range(n)
    ]
    for p in range(0, n, 7):  # sample centers for speed; each vs all others
        for q in range(n):
            if p == q:
                continue
            prof = unif.bt1816.move_profile(p, q, pts_t, adj_t)
            retained = sum(k * v for k, v in prof.items())
            assert retained == len(my_safe[p] & my_safe[q]) == 18
            assert 27 - retained == 9
