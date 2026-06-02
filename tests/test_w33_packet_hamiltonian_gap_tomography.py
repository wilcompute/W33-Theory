from analysis.w33_packet_hamiltonian_gap_tomography import main


def test_packet_hamiltonian_gap_tomography_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 20


def test_packet_hamiltonian_gap_tomography_gaps():
    r = main()
    assert r['gap_identities']['256-64'] == '192 = 16*12 = tomotope total flag count'
    assert r['gap_identities']['256-216'] == '40 = W33 vertex count'
    assert r['gap_identities']['216-64'] == '152 = 192-40'


def test_packet_hamiltonian_gap_tomography_blocks():
    r = main()
    assert r['block_identities']['K-64I'] == '152Q1 + 192Q4'
    assert r['block_identities']['K-64I-152Q1'] == '192Q4, rank 4'
    assert r['block_identities']['256I-K'] == '40Q1 + 192Q5'
    assert r['block_identities']['256I-K-40Q1'] == '192Q5, rank 5'
