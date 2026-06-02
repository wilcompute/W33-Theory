from analysis.w33_fano_hinge_affine_symmetry import main


def test_fano_hinge_affine_symmetry_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 21


def test_fano_hinge_affine_symmetry_groups():
    r = main()
    assert r['groups']['GL_3_2_order'] == 168
    assert r['groups']['odd_hyperplane_stabilizer_order'] == 24
    assert r['groups']['affine_chart_symmetry_order'] == 192
    assert r['groups']['full_K44_automorphism_order'] == 1152
    assert r['groups']['index_in_full_K44_auto'] == 6


def test_fano_hinge_affine_symmetry_192_decompositions():
    r = main()
    assert set(r['decompositions_of_192'].values()) == {192}
    assert r['objects']['fano_lines'] == 7
    assert r['objects']['toroidal_axes'] == 'seven nonzero Fano points'
