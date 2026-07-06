"""Pass 62: the interrupt controller -- the tax arc running inside the VM track's microkernel.

- closed-form vector table: ground(T) = T + (Gamma(p) - T_perp) == the ILP enumeration; the unlit
  quad is the center quad, a transversal of the defect star;
- the migration price law: same-center overlap always 5 (re-vector = 6 rays); collinear max 8
  (edge migration = 3 rays); the 8 cheap channels sit 2-per-center at the ground's own center quad;
- the controller holds every theorem as a runtime invariant over a seeded 2100-event run and
  relocates only through cheap channels (average cost exactly 3 rays).
"""

import os
import random
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_interrupt_controller as ic  # noqa: E402
import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402


def _geometry():
    pts, A, lines, B = audit._build(3)
    return pts, A, lines, B, len(pts)


def test_closed_form_vector_table():
    pts, A, lines, B, n = _geometry()
    for p in (0, 7, 23):
        tbl, nb = ic.vector_table(p, pts, A, lines, n)
        assert len(tbl) == 9, f"vector table at {p} must have 9 entries"
        for lit, t, perp in tbl:
            assert set(perp) <= nb, "center quad must lie in the perp"
            assert lit == frozenset(t) | (nb - set(perp))


def test_migration_price_law():
    pts, A, lines, B, n = _geometry()
    n_orbit, spec, cheap, cen = ic.migration_price_law(pts, A, lines, B)
    assert n_orbit == 360
    assert sorted({ov for (rel, ov) in spec if rel == "same"}) == [5]
    assert sorted({ov for (rel, ov) in spec if rel == "collinear"}) == [0, 2, 3, 8]
    assert sorted({ov for (rel, ov) in spec if rel == "noncollinear"}) == [1, 2, 4, 6]
    assert set(cheap.values()) == {8} and len(cheap) == 360


def test_controller_invariants_and_cheap_relocation():
    pts, A, lines, B, n = _geometry()
    spreads = anat.enumerate_spreads(lines, n)
    ctl = ic.InterruptController(
        pts, A, lines, n, spreads, center=0, threshold=4, seed=7
    )
    rng = random.Random(42)
    for _ in range(1200):
        ctl.service(rng.randrange(len(lines)))
    assert not ctl.invariant_failures, ctl.invariant_failures
    c = ctl.counters
    assert c["relocations"] > 0
    assert (
        c["migration_cost_rays"] / c["relocations"] == 3.0
    ), "relocations must use cheap channels"
