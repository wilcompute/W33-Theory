"""Exact Conwell/Klein/Hamming/E8/twistor-frame regression controls."""
from analysis.w33_20261029_klein_e8_hamming_twistor_transform import (
    certificate, generators, partition_rulings, transform_certificate,
    hamming_code, lift_e8, even_quotient, quadratic,
)


def test_quadric_counts_and_thirty_hamming_lifts():
    x=even_quotient(); assert len(x)==64
    assert sum(quadratic(p)==0 for p in x)==36
    gs=generators();assert len(gs)==30
    assert len({hamming_code(g) for g in gs})==30
    for g in gs:
        code,roots=lift_e8(g)
        assert len(code)==16 and len(roots)==240


def test_two_rulings_and_incidence_transform():
    alpha,beta=partition_rulings(generators())
    assert len(alpha)==len(beta)==15
    M,B=transform_certificate(alpha,beta)
    assert len(M)==15 and all(sum(row)==7 for row in M)
    assert all(v in (-1,2) for row in B for v in row)


def test_eight_qubit_overlap_spectrum_and_stabilizer_group():
    c=certificate()
    assert c['thirty_state_Gram_spectrum']=={'9':1,'3/2':14,'0':15}
    assert c['thirty_state_span_dimension']==15
    assert c['S8_orbit_stabilizer']['single_code_stabilizer']==1344
    assert c['pairwise_state_overlaps']=={'1/4':210,'1/8':120,'1/2':105}
