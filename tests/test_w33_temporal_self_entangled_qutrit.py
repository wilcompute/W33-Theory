"""Tests for Part MCLXIII: temporal self-entangled qutrit bridge."""

from analysis.w33_temporal_self_entangled_qutrit import (
    bell_expectation_survives,
    projective_points,
    span_line,
    symplectic,
    temporal_self_entangled_qutrit_packet,
)


PACKET = temporal_self_entangled_qutrit_packet()


def test_temporal_qutrit_history_split():
    temporal = PACKET["temporal_qutrit"]
    assert temporal["past_future_basis_pairs"] == 9
    assert temporal["now_diagonal_histories"] == 3
    assert temporal["directed_change_histories"] == 6
    assert temporal["identity"] == "9 = 3 diagonal now histories + 6 directed past/future changes"
    assert temporal["purity"] == "1/3"
    assert temporal["entropy_trits"] == "1"


def test_choi_now_computation_survival_rule():
    now = PACKET["now_computation"]
    assert now["choi_identity"] == "<Omega|(I tensor U)|Omega> = Tr(U)/3"
    assert now["single_qutrit_pauli_survivors"] == 1
    assert now["single_qutrit_pauli_erased_nonidentity"] == 8
    assert now["two_qutrit_surviving_nonzero_vectors"] == 8
    assert now["two_qutrit_surviving_projective_rays"] == 4


def test_bell_stabilizer_generators_commute_and_define_line():
    shift_lock = (1, 0, 1, 0)
    phase_lock = (0, 1, 0, 2)
    assert symplectic(shift_lock, phase_lock) == 0
    line = span_line(shift_lock, phase_lock)
    assert len(line) == 4
    assert all(bell_expectation_survives(point) for point in line)
    assert PACKET["bell_stabilizer_line"]["line_size"] == 4
    assert PACKET["bell_stabilizer_line"]["commuting"] is True


def test_projective_two_qutrit_phase_space_is_w33_size():
    assert len(projective_points()) == 40
    geometry = PACKET["w33_observable_geometry"]
    assert geometry["nonzero_phase_vectors"] == 80
    assert geometry["projective_rays"] == 40
    assert geometry["isotropic_lines"] == 40
    assert geometry["line_size"] == 4
    assert geometry["lines_per_point"] == 4


def test_w33_srg_parameters_from_temporal_observables():
    srg = PACKET["w33_observable_geometry"]["srg"]
    assert srg["v"] == 40
    assert srg["k_values"] == [12]
    assert srg["edges"] == 240
    assert srg["lambda_counts"] == {2: 240}
    assert srg["mu_counts"] == {4: 540}


def test_temporal_bell_line_extends_to_spread():
    spread = PACKET["spread_packet"]
    assert spread["spread_size"] == 10
    assert spread["context_size"] == 4
    assert spread["covered_points"] == 40
    assert spread["contains_temporal_bell_line"] is True
    assert spread["identity"] == "10 disjoint now-contexts * 4 commuting rays = 40 W33 rays"


def test_packet_metadata_and_boundary():
    assert PACKET["part"] == "MCLXIII"
    assert PACKET["theorem"] == "Temporal self-entangled qutrit bridge"
    assert "finite temporal-qutrit" in PACKET["claim_boundary"]
    assert "not a continuum dynamics proof" in PACKET["claim_boundary"]


def test_all_checks_pass():
    failed = [name for name, value in PACKET["checks"].items() if not value]
    assert failed == []
    assert PACKET["n_verified"] == len(PACKET["checks"])
