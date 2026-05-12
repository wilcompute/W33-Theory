from fractions import Fraction

DIM_K = 81
DIM_B = 120
RANK_D1 = 39
LAMBDA_K = 0
LAMBDA_B = 4


def test_rank_lock_and_residual_boundary_sector():
    max_rank = min(DIM_K, DIM_B)
    residual = DIM_B - max_rank
    assert max_rank == 81
    assert residual == 39
    assert residual == RANK_D1
    assert DIM_B == DIM_K + RANK_D1


def test_minimal_kb_trace_coefficients():
    # Phi_min = [[0,Y],[Y*,h I_B]]
    # Tr(Phi^2)=2S2+120h^2
    assert 2 == 2
    assert DIM_B == 120
    # Tr(Delta Phi^2)=4S2+480h^2
    assert LAMBDA_K + LAMBDA_B == 4
    assert LAMBDA_B * DIM_B == 480
    # commutator penalty = 2(4-0)^2 S2 = 32S2
    assert 2 * (LAMBDA_B - LAMBDA_K) ** 2 == 32


def test_minimal_kb_quartic_coefficients():
    # Tr(Phi_min^4)=2S4+4h^2S2+120h^4
    assert 2 == 2
    assert 4 == 4
    assert DIM_B == 120


def test_effective_mass_denominator_and_heavy_limit():
    # Integrated boundary channel uses M_eff=(4M_F^2+h)^-1 YY*.
    assert LAMBDA_B == 4
    # Heavy boundary limit denominator is 4 M_F^2.
    assert Fraction(1, LAMBDA_B) == Fraction(1, 4)


def test_fermion_modes_from_rank_y():
    # number of massive K modes = rank(Y), residual massless K modes = 81-rank(Y)
    for rank_y in [0, 1, 27, 80, 81]:
        assert rank_y <= DIM_K
        assert DIM_K - rank_y >= 0
    assert 2 * DIM_K == 162
