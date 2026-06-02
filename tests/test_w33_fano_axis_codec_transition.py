from analysis.w33_fano_axis_codec_transition import main


def test_fano_axis_codec_transition_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 25


def test_fano_axis_codec_transition_quotient_graph():
    r = main()
    assert r['quotient_graph']['edge_count'] == 16
    assert r['quotient_graph']['generators'] == ['001', '010', '100', '111']
    assert r['quotient_graph']['graph'] == 'K4,4 with parity bipartition of F2^3'


def test_fano_axis_codec_transition_fano_split():
    r = main()
    assert r['fano_split']['line_count'] == 7
    assert r['fano_split']['incidence_count'] == 21
    assert len(r['fano_split']['odd_adjacent_axes']) == 4
    assert len(r['fano_split']['even_nonadjacent_axes']) == 3
    assert r['codec_transition_lifts']['same_family_last_bit_flips'] == 24
    assert r['codec_transition_lifts']['cs_duality_first_bit_flips'] == 8
