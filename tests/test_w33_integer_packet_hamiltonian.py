from analysis.w33_integer_packet_hamiltonian import main


def test_integer_packet_hamiltonian_all_checks_pass():
    r = main()
    assert r['n_verified'] == r['n_checks'] == 18


def test_integer_packet_hamiltonian_spectrum():
    r = main()
    assert r['spectrum'] == {'216': 1, '256': 4, '64': 5}
    assert r['projector_formula'] == 'K = 216 Q1 + 256 Q4 + 64 Q5'
    assert r['invariants']['trace'] == 1560


def test_integer_packet_hamiltonian_polynomials():
    r = main()
    assert r['polynomial_T5'] == 'K = -9 A_T5^2 + 55 A_T5 + 210 I'
    assert r['polynomial_Petersen'] == 'K = -9 A_Pet^2 - 37 A_Pet + 222 I'
    assert r['invariants']['minimal_polynomial'] == '(x-216)(x-256)(x-64)'
