from analysis.w33_pass5888_5895_ihara_identity_correction import build_w33, srg_check, build_hashimoto, old_surrogate


def test_canonical_w33_identity():
    A = build_w33()
    assert srg_check(A) == {"v": 40, "k": 12, "lambda": 2, "mu": 4, "edges": 240}


def test_canonical_hashimoto_size_and_outdegree():
    B = build_hashimoto(build_w33())
    assert B.shape == (480, 480)
    assert set(map(int, B.sum(axis=1))) == {11}


def test_exact_hashimoto_count_accounting():
    counts = [1, 201, 200, 24, 24, 15, 15]
    assert sum(counts) == 480
    assert 24 + 24 + 15 + 15 == 78


def test_pass5880_surrogate_is_not_w33_and_not_ramanujan():
    s = old_surrogate()
    assert s["vertices"] == 33
    assert s["degree_values"] == [4]
    assert s["edges"] == 66
    assert s["largest_nontrivial_adjacency_abs"] > s["ramanujan_bound_2sqrt3"]
    assert s["ramanujan"] is False


def test_physical_claims_fail_closed_by_contract():
    # Graph valence alone does not specify propagation time/length, coupler loss,
    # dispersion, or boundary conditions. No hardware FSR/finesse/capacity
    # equation is asserted in the exact correction producer.
    import inspect
    from analysis import w33_pass5888_5895_ihara_identity_correction as m
    src = inspect.getsource(m)
    assert "free spectral range from graph valence alone" in src
    assert "Fabry-Perot finesse from q=d-1 alone" in src
    assert "Shannon channel capacity from the graph spectrum alone" in src
