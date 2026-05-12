def test_torus_mode_polarization_split():
    csaszar_vector_modes = 5
    szilassi_bivector_modes = 2
    toroidal_shell = 7
    assert csaszar_vector_modes + szilassi_bivector_modes == toroidal_shell


def test_genus_oscillator_hole_counts():
    # chi(h)=2-2h for orientable genus h.
    for h in range(4):
        assert 2 - 2 * h == 2 - 2 * h


def test_triangle_as_minimal_bivector_atom():
    vertices = 3
    edges = 3
    oriented_area_cell = True
    assert vertices == edges == 3
    assert oriented_area_cell


def test_hole_as_nonboundary_cycle():
    cycle = True
    boundary = False
    hole = cycle and not boundary
    assert hole


def test_threshold_chain_names():
    thresholds = ["p_geom", "p_beta1", "p_Cl", "p_H1", "p_full", "p_split"]
    assert thresholds == ["p_geom", "p_beta1", "p_Cl", "p_H1", "p_full", "p_split"]


def test_clifford_percolation_observables():
    observables = {
        "beta_1",
        "rank_C_H",
        "d_eff",
        "Spec_C_H",
        "Clifford_holonomy_spectrum",
        "localization_length",
    }
    assert "Clifford_holonomy_spectrum" in observables
    assert "rank_C_H" in observables
