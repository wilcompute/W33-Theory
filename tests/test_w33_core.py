import numpy as np
import pytest

from THEORY_PART_CLXVII_FINAL_SYNTHESIS import build_witting_states, is_orthogonal


def test_build_witting_states_shape():
    states = build_witting_states()
    assert isinstance(states, list)
    assert len(states) == 40
    for v in states:
        assert isinstance(v, np.ndarray)
        assert v.shape == (4,)


def test_is_orthogonal_consistency():
    states = build_witting_states()
    # pick known orthogonal pairs from construction
    # basis vectors 0 and 1 are orthogonal
    assert is_orthogonal(0, 1)
    # vector 0 is not orthogonal to a state with overlap
    # find any j where not orthogonal
    non_orth = [j for j in range(40) if not is_orthogonal(0, j) and j != 0]
    assert len(non_orth) > 0


def test_adj_spectrum():
    states = build_witting_states()
    # build adjacency
    A = np.zeros((40, 40), dtype=int)
    for i in range(40):
        for j in range(40):
            if i != j and is_orthogonal(i, j):
                A[i, j] = 1

    # eigenvalues
    vals = np.linalg.eigvalsh(A)
    rounded = [round(v) for v in vals]
    counts = {v: rounded.count(v) for v in set(rounded)}
    assert counts.get(12, 0) == 1
    assert counts.get(2, 0) == 24
    assert counts.get(-4, 0) == 15
