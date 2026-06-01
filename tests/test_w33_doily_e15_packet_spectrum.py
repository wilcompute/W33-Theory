from analysis.w33_doily_e15_packet_spectrum import main


def test_doily_e15_packet_spectrum_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 22


def test_doily_e15_packet_spectrum_doily_packets():
    r = main()
    assert r['doily_packets']['lines'] == 15
    assert r['doily_packets']['incidences'] == 45
    assert r['doily_packets']['packet_rank'] == 10
    assert r['doily_packets']['packet_gram_spectrum'] == {'216': 1, '96': 9, '0': 5}


def test_doily_e15_packet_spectrum_nonisotropic_packets():
    r = main()
    assert r['nonisotropic_packets']['lines'] == 20
    assert r['nonisotropic_packets']['incidences'] == 60
    assert r['nonisotropic_packets']['packet_rank'] == 15
    assert r['nonisotropic_packets']['packet_gram_spectrum'] == {'288': 1, '144': 5, '48': 9}
