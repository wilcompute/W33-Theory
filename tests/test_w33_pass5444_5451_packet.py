from analysis.w33_pass5444_allq_apartment_basis_volume_budget import row as volume_row
from analysis.w33_pass5446_allodd_footprint_double_quotient_ladder import row as ladder_row
from analysis.w33_pass5449_allq_apartment_lattice_index_sum_squares import row as lattice_row
from analysis.w33_pass5450_unsigned_gram_pell_square_class import odd_square_class, pell_qs
from analysis.w33_pass5451_pell_weil_clock_compatibility import pell_qs as weil_pell_qs


def test_q3_volume_budget_factorization():
    r=volume_row(3)
    assert r['flags']==160
    assert r['cycle_rank']==81
    assert r['upper_bound_exponents']=={'q+1':132,'q^2+1':58}
    assert 2*132+58==322


def test_allodd_double_quotient_anchors():
    q3=ladder_row(3)
    q5=ladder_row(5)
    assert q3['CF_dim']==15
    assert q3['apartment_kernel_Dap_K0_dim']==66
    assert q5['CF_dim']==65
    assert q5['apartment_kernel_Dap_K0_dim']==560
    assert q5['transpose_radical_dim']==64
    assert q5['transpose_nonsingular_quotient_dim']==1


def test_lattice_sum_of_squares_matches_volume_ratio():
    a=volume_row(3)['upper_bound_exponents']
    b=lattice_row(3)['exponents']
    assert a==b=={'q+1':132,'q^2+1':58}


def test_negative_pell_square_class():
    seq=pell_qs(6)
    assert seq==[(1,1),(7,5),(41,29),(239,169),(1393,985),(8119,5741)]
    for q,m in seq:
        assert q*q-2*m*m==-1
        assert odd_square_class(q)==m*m
    assert odd_square_class(3)==5
    assert odd_square_class(5)==13


def test_pell_implies_split_mod8_clock():
    for q,m in weil_pell_qs(10):
        assert q%8 in (1,7)
    assert 9%8==1
    assert odd_square_class(9)==41
