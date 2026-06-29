"""Pass 53: parity (not primality) law, the CF closed form, and the table-free routing win.

Three property tests:
  - The q-scan now reaches q=4 = GF(4), an EVEN COMPOSITE order. If contextuality vanished only for
    primes the q=4 row would be contextual; it is not (CF=0), so the cause is parity, not primality.
  - The contextual fraction obeys the exact closed form CF(q) = 0 for even q and 1/(q^2+1) for odd q.
  - holonet bench --compare builds a classical all-pairs forwarding table and verifies the Holonet
    routes the same pairs with zero table (address IS the route).
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


def test_gf4_is_a_real_field():
    # GF(4) (not integers mod 4) gives the correct SRG(85,20,3,5); mod-4 arithmetic would not.
    pts, A, lines, B = audit._build(4)
    n = len(pts)
    k = int(A.sum(1)[0])
    assert n == 85 and k == 20 and len(lines) == 85 and len(lines[0]) == 5


def test_parity_not_primality():
    rows, checks, all_ok = audit.qscan((2, 3, 4))
    assert all_ok, [n for n, ok in checks if not ok]
    by_q = {r["q"]: r for r in rows}
    # q=4 is even AND composite -> still has an ovoid -> CF=0 (parity, not primality)
    assert by_q[4]["ovoid_exists"] is True
    assert by_q[4]["contextual_fraction"] == 0.0
    # the odd member stays contextual
    assert by_q[3]["contextual_fraction"] > 0.0


def test_cf_closed_form():
    rows, _, _ = audit.qscan((2, 3, 4))
    for r in rows:
        q = r["q"]
        expected = 0.0 if q % 2 == 0 else 1.0 / (q**2 + 1)
        assert abs(r["contextual_fraction"] - expected) < 1e-9


def test_bench_compare_table_free():
    ledger, ok = bench.run_compare()
    assert ok
    assert ledger["holonet_address_routed"]["routing_table_bytes"] == 0
    assert ledger["baseline_table_routed"]["routing_table_bytes"] > 0
    assert ledger["routers_agree_on_sample"] is True
    assert ledger["holonet_address_routed"]["max_hops"] <= 2
