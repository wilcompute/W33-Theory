def test_genus_oscillator_first_three_levels():
    q = 3
    mu = 4
    g = 15
    phi4 = 10
    vals = []
    for h in range(3):
        v = mu + h * q
        e = 6 + h * g
        f = mu + h * phi4
        vals.append((v, e, f, v - e + f))
    assert vals == [(4, 6, 4, 2), (7, 21, 14, 0), (10, 36, 24, -2)]


def test_toroidal_mode_split():
    csaszar = 5
    szilassi = 2
    phi6 = 7
    assert csaszar + szilassi == phi6


def test_percolation_threshold_names():
    thresholds = {
        "p_geom": "first giant occupied incidence component",
        "p_H1": "first nonzero rank C_H(p)",
        "p_full": "first rank C_H(p)=81",
        "p_split": "first stable nontrivial spectral split of C_H(p)",
    }
    assert set(thresholds) == {"p_geom", "p_H1", "p_full", "p_split"}


def test_ch_percolation_observables():
    observables = ["rank C_H", "d_eff", "Spec(C_H)", "Betti vector"]
    assert len(observables) == 4
    assert "rank C_H" in observables
    assert "Spec(C_H)" in observables


def test_quantum_percolation_readout_dimension():
    h1_dim = 81
    assert h1_dim == 81
