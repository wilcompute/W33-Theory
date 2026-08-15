from analysis.w33_pass5428_allq_oriented_apartment_tomography import row as oriented_row
from analysis.w33_pass5429_allq_unsigned_apartment_inverse_conditioning import row as inverse_row
from analysis.w33_pass5431_allodd_modular_footprint_defect_exact_sequence import row as defect_row
from analysis.w33_pass5434_allq_unsigned_apartment_determinant import exponents
from analysis.w33_pass5435_allq_unsigned_apartment_characteristic_polynomial import row as charpoly_row


def test_q3_oriented_tomography_anchor():
    r=oriented_row(3)
    assert r['flags']==160
    assert r['cycle_rank']==81
    assert r['apartments']==1620
    assert r['unit_frame_bound']=='20'


def test_unsigned_conditioning_extremes():
    for q in (2,3,4,5,7,8,9,11,13):
        r=inverse_row(q)
        assert r['lambda_max']==8*q**4
        assert r['lambda_min']==(q-1)**2*(q*q+1)
        assert r['gram_condition_number']>=1


def test_modular_extra_point_kernel_defect_dimension_identity():
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    for q,rk in anchors.items():
        r=defect_row(q,rk)
        assert r['extra_point_kernel_defect_dimension']==0
        assert r['dim_M0_mod_CW']==r['radical_dimension']


def test_unsigned_determinant_q3_factorization_exponents():
    r=exponents(3)
    assert r['power_2']==81
    assert r['power_q']==160
    assert r['power_q_minus_1']==270
    assert r['power_q2_plus_1']==105
    assert 81+270+105==456


def test_characteristic_polynomial_degree_and_field_clock():
    for q in (2,3,4,5,7,8,9,11,13,16,32):
        r=charpoly_row(q)
        assert 1+2*r['f']+2*r['g']+q**4==r['flags']
    assert charpoly_row(8)['sqrt_2q_rational']
    assert charpoly_row(32)['sqrt_2q_rational']
    assert not charpoly_row(3)['sqrt_2q_rational']
    assert not charpoly_row(16)['sqrt_2q_rational']
