from PART_CLXXXI_REPO_HINT_ATLAS import (
    Q,
    Q2,
    Q3,
    Q4,
    PHI6,
    J,
    J_INV,
    E6_DIM,
    E8_DIM,
    hint_continents,
    next_bridges,
    repo_hint_atlas_audit,
)


def test_core_atoms():
    assert (Q, Q2, Q3, Q4) == (3, 9, 27, 81)
    assert (PHI6, J, J_INV, E6_DIM, E8_DIM) == (7, 5, 8, 78, 248)


def test_hint_continent_registry():
    continents = hint_continents()
    assert len(continents) == 8
    assert set(c.priority for c in continents) == set(range(1, 9))
    assert all(len(c.representative_files) >= 2 for c in continents)
    assert min(continents, key=lambda c: c.priority).name == "CCT crosswalk / loop-clock / trit economy"


def test_required_families_present():
    names = {c.name for c in hint_continents()}
    assert "firewall / L-infinity / Jacobi repair" in names
    assert "toroidal heptad / realization centroids / projectors" in names
    assert "sporadic / Moonshine / Suzuki tower" in names
    assert "quotient / packet transport / Witting bridge" in names


def test_next_bridge_order():
    bridges = next_bridges()
    assert [b.rank for b in bridges] == [1, 2, 3, 4, 5]
    assert bridges[0].bridge == "CCT loop carrier weld"
    assert bridges[0].deliverable == "PART_CLXXXII_CCT_HASHIMOTO_CARRIER_WELD.py"
    assert all(b.deliverable.startswith("PART_CLXXXII") for b in bridges)


def test_audit_checks_all_true():
    audit = repo_hint_atlas_audit()
    assert all(audit["checks"].values())
    assert audit["highest_value_next_move"]["bridge"] == "CCT loop carrier weld"
