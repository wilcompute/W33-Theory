"""Pass 59: the tax orbits.

  - the transvection closure on the 40 points is PSp(4,3), order 25920 = 51840/2 (the double-cover
    distinction the claim-tier spine warns about, enforced);
  - the 20 center-0 optima generate all 800 under the group, in exactly four orbits 360+40+360+40,
    with (center lit?, uniform load c) a complete orbit invariant;
  - the queue invariant holds globally: every one of the 800 optima loads its defect star uniformly,
    spectrum {2,3,4}.
"""

import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"
    ),
)

import w33_master_audit as audit  # noqa: E402
import w33_spread_star_anatomy as anat  # noqa: E402
import w33_tax_orbits as orb  # noqa: E402


def _setup():
    pts, A, lines, B = audit._build(3)
    gens, G = orb.build_group(pts, B)
    return pts, lines, B, gens, G


def test_point_group_is_psp43():
    pts, lines, B, gens, G = _setup()
    assert len(G) == 25920, "point action must be PSp(4,3), order 25920 = 51840/2"
    assert len({g[0] for g in G}) == 40, "must be transitive on points"


def test_four_orbits_360_40_360_40():
    pts, lines, B, gens, G = _setup()
    sols, star = anat._enumerate_optima_for_center(lines, len(pts), 0)
    seeds = [frozenset(i for i in range(len(pts)) if s[i]) for s in sols]
    orbits = orb.orbit_decomposition(seeds, gens)
    assert sorted(len(o) for o in orbits) == [40, 40, 360, 360]
    assert sum(len(o) for o in orbits) == 800


def test_global_uniform_loading():
    pts, lines, B, gens, G = _setup()
    sols, star = anat._enumerate_optima_for_center(lines, len(pts), 0)
    seeds = [frozenset(i for i in range(len(pts)) if s[i]) for s in sols]
    orbits = orb.orbit_decomposition(seeds, gens)
    loads = set()
    for o in orbits:
        for lit in o:
            center, occ = orb.optimum_profile(lit, lines)
            assert center is not None, "every orbit element must be a valid optimum"
            assert len(set(occ)) == 1, f"loading must be uniform, got {occ}"
            loads.add(occ[0])
    assert loads == {2, 3, 4}
