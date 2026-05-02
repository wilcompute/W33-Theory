from fractions import Fraction

from PART_CLXIV_TOROIDAL_GENUS_REPTEND_BRIDGE import (
    Q,
    QP1,
    K,
    PHI6,
    RANK_SEED,
    J,
    BINARY_DUALITY,
    accepted_residues_mod12,
    crt_coords,
    hole_genus,
    polyhedron_rows,
    toroidal_genus_reptend_audit,
)


def test_hole_equation_accepted_residues():
    assert accepted_residues_mod12() == [Q, QP1, PHI6, K] == [3, 4, 7, 12]


def test_genus_values_at_special_residues():
    assert hole_genus(Q) == 0
    assert hole_genus(QP1) == 0
    assert hole_genus(PHI6) == 1
    assert hole_genus(K) == RANK_SEED == 6


def test_crt_gate_for_torus_and_closure():
    assert crt_coords(Q) == (0, 3)
    assert crt_coords(QP1) == (1, 0)
    assert crt_coords(PHI6) == (1, 3)
    assert crt_coords(K) == (0, 0)


def test_realization_split_sums_to_torus_residue():
    assert J + BINARY_DUALITY == PHI6 == 7


def test_toroidal_polyhedra_share_edges_and_dual_swap():
    rows = {r.name: r for r in polyhedron_rows()}
    assert rows["Csaszar"].edges == rows["Szilassi"].edges == 21
    assert rows["next vertex-complete h=6"].edges == rows["next face-complete h=6"].edges == 66
    assert rows["next vertex-complete h=6"].vertices == 12
    assert rows["next vertex-complete h=6"].faces == 44
    assert rows["next face-complete h=6"].vertices == 44
    assert rows["next face-complete h=6"].faces == 12


def test_flag_counts_from_rank_and_phi6():
    assert RANK_SEED * PHI6 == 42
    assert 2 * RANK_SEED * PHI6 == 84


def test_audit_checks_all_true():
    audit = toroidal_genus_reptend_audit()
    assert all(audit["checks"].values())
    assert audit["realization_bridge"]["identity"] == "5+2=7=Phi6=the h=1 torus residue"
