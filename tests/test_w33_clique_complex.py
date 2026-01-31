from tools.w33_clique_complex_py import compute_clique_complex_summary


def test_w33_clique_complex_summary_structure():
    s = compute_clique_complex_summary()
    assert s["vertices"] == 40
    assert isinstance(s["edges"], int)
    assert isinstance(s["triangles"], int)
    assert isinstance(s["tetrahedra"], int)
    # basic sanity: tetrahedra <= triangles <= edges
    assert s["tetrahedra"] <= s["triangles"] <= s["edges"]
