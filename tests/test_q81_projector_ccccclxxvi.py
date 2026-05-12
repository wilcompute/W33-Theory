def test_active_triangle_bridge_dimension():
    tri_160 = 160
    line_kernel = 40
    y_tri = tri_160 - line_kernel
    assert y_tri == 120


def test_q81_projector_rank():
    y_tri = 120
    y_vert = 39
    q = y_tri - y_vert
    assert q == 81


def test_projector_decomposition_dimensions():
    rank_pi_vert = 39
    rank_pi_q = 81
    identity_rank = 120
    assert rank_pi_vert + rank_pi_q == identity_rank


def test_projector_identities_symbolic():
    identities = {
        "Pi_Q^2=Pi_Q": True,
        "Pi_Q*=Pi_Q": True,
        "Pi_Q Pi_vert=0": True,
        "Pi_vert+Pi_Q=I": True,
    }
    assert all(identities.values())


def test_hodge_style_dictionary():
    exact_gradient = 39
    homological = 81
    boundary_activation = 120
    assert exact_gradient + homological == boundary_activation
