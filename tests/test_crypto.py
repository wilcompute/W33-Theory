import numpy as np
from THEORY_PART_CXLIV_CRYPTO import build_witting_states, find_bases, Sigma, rho_A, compute_correlation


def test_states_and_bases_counts():
    states = build_witting_states()
    assert len(states) == 40
    bases = find_bases(states)
    assert len(bases) == 40


def test_reduced_density_maximally_mixed():
    assert np.allclose(rho_A, np.eye(4) / 4)


def test_same_basis_perfect_correlation():
    bases = find_bases(build_witting_states())
    b0 = list(bases[0])
    probs = compute_correlation(b0, b0)
    # diagonal sum should be 1 (perfect correlation)
    assert abs(np.trace(probs) - 1.0) < 1e-8
