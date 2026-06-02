from analysis.w33_branching_packet_energy_renormalization import main


def test_branching_packet_energy_renormalization_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 16


def test_branching_packet_energy_renormalization_spectra():
    r = main()
    assert r['full_packet_energy_spectrum'] == {'27/2': 1, '16': 4, '4': 5}
    assert r['renormalized_packet_spectra']['Q1_uniform'] == '27/2^1'
    assert r['renormalized_packet_spectra']['Q4_vertex'] == '16^4'
    assert r['renormalized_packet_spectra']['Q5_petersen'] == '4^5'


def test_branching_packet_energy_renormalization_weights():
    r = main()
    assert r['energy_weights']['S6_uniform_weight'] == 9
    assert r['energy_weights']['S6_observable_weight'] == 4
    assert r['ranks'] == {'Dq': 10, 'Q1_block': 1, 'Q4_block': 4, 'Q5_block': 5}
