def test_cclxiii_ovoid_curvature_smoke():
    mu = 4
    Phi4 = 10
    v = 40
    lam = 2
    assert mu * Phi4 == v == 40
    assert lam * Phi4 == 20
    assert (lam / mu) * v == 20
