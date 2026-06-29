"""Pass 52: the q-scan parity law and the bench op-counts.

Two property tests of the audit's neighbourhood:
  - qscan: every W(q) layer constant follows its closed form, and the substrate is contextual (CF>0)
    exactly when q is odd -- so q=2 is classical (an ovoid of 5 exists, CF=0) and q=3 is contextual
    (no ovoid, CF=1/10). This pins that q=3 is the FORCED minimal contextual member, not a free choice.
  - bench: the deterministic operation counts (7 mod-3 ops/route decision, <=2 hops, mu=4 multipath)
    are exactly the geometry's, independent of wall-clock time.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import holonet_bench as bench  # noqa: E402
import w33_master_audit as audit  # noqa: E402


def test_qscan_all_pass():
    rows, checks, all_ok = audit.qscan((2, 3))
    failed = [n for n, ok in checks if not ok]
    assert all_ok, f"qscan failures: {failed}"


def test_parity_law_contextual_iff_q_odd():
    rows, _, _ = audit.qscan((2, 3))
    by_q = {r["q"]: r for r in rows}
    # q=2 even: ovoid exists, non-contextual
    assert by_q[2]["ovoid_exists"] is True
    assert by_q[2]["contextual_fraction"] == 0.0
    # q=3 odd: no ovoid, contextual, CF = 1/10
    assert by_q[3]["ovoid_exists"] is False
    assert by_q[3]["contextual_fraction"] == 0.1
    assert by_q[3]["alpha"] == 7 and by_q[3]["hoffman"] == 10


def test_qscan_closed_forms():
    rows, _, _ = audit.qscan((2, 3))
    for r in rows:
        q = r["q"]
        assert r["n"] == (q + 1) * (q**2 + 1)
        assert r["k"] == q * (q + 1)
        assert r["Sp4q"] == q**4 * (q**2 - 1) * (q**4 - 1)


def test_bench_op_counts():
    ledger, ok = bench.run_bench(reps=8)
    c = ledger["deterministic_op_counts"]
    assert c["route_decision_mod3_ops"] == 7
    assert c["hops_per_packet"] <= 2
    assert c["multipath_mu"] == 4
    assert ok
