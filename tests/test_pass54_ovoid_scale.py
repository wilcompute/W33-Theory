"""Pass 54: explicit even-q ovoids (the control model) and the scaling routing win.

  - The even orders q=2 and q=4 admit an explicit ovoid -- a (q^2+1)-point set meeting every context
    exactly once -- so assigning 1 to those points is a noncontextual model and CF=0. The odd order q=3
    admits none. This is the predicted data for the demonstrator's control arm.
  - holonet bench --compare --scale: the baseline routing-state cost grows with q while the Holonet
    stays at 0 bytes and 2 hops.
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
import w33_ovoid_construct as ov  # noqa: E402


def test_even_q_ovoids_constructed_and_verified():
    for q in (2, 4):
        ovoid, pts, lines, A, max_sat = ov.find_ovoid(q)
        assert ovoid is not None, f"q={q} should have an ovoid"
        ok, rep = ov.verify_ovoid(ovoid, pts, lines, A, q)
        assert ok, rep
        assert rep["size"] == q**2 + 1
        assert rep["covers_every_line_once"] is True
        assert rep["is_cap_pairwise_noncollinear"] is True


def test_q3_has_no_ovoid():
    ovoid, pts, lines, A, max_sat = ov.find_ovoid(3)
    assert ovoid is None
    assert max_sat == 36 and len(lines) == 40


def test_compare_scale_diverges_holonet_zero():
    ledger, ok = bench.run_compare_scale()
    assert ok
    rows = ledger["rows"]
    # baseline strictly increasing; holonet always zero and 2 hops
    for i in range(len(rows) - 1):
        assert rows[i]["baseline_routing_bytes"] < rows[i + 1]["baseline_routing_bytes"]
    for r in rows:
        assert r["holonet_routing_bytes"] == 0
        assert r["holonet_hops"] == 2
