"""Independent action, tensor and anomaly checks for the exact cubic packet."""

from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import toe_20261108_exact_signed_cubic_stabilizer as cubic
import toe_20261108_three_copy_cubic_vacuum as vacuum


def test_root_transvections_preserve_the_cubic_in_integer_coordinates():
    certificate = cubic.calculate()
    terms = cubic.signed_terms(cubic.CUBIC)
    x = np.random.default_rng(8426).integers(-5, 6, size=27)
    expected = sum(s*x[i]*x[j]*x[k] for (i,j,k),s in terms.items())
    count = 0
    for generator in certificate['cubic_27']['generators']:
        if all(i == j for i,j,_ in generator):
            continue
        e = np.zeros((27,27), dtype=np.int64)
        for i,j,v in generator:
            e[i,j] = v
        assert not np.any(e @ e)
        for parameter in (-2, 3):
            y = x + parameter*(e@x)
            assert sum(s*y[i]*y[j]*y[k] for (i,j,k),s in terms.items()) == expected
        count += 1
    assert count == 72


def test_ordered_bracket_contracts_to_alternating_three_copy_form():
    rng = np.random.default_rng(114)
    fields = rng.integers(-3, 4, size=(81,3))
    records = vacuum.native.build_records()
    expected = sum(s*fields[i,0]*fields[j,1]*fields[k,2] for i,j,k,s in records)
    assert expected != 0
    wedge = cubic.alternating_terms(cubic.signed_terms(cubic.CUBIC))
    actual = 0
    for term, sign in wedge.items():
        x,y,z = fields[list(term)]
        actual += sign * int(x @ np.cross(y,z))
    assert actual == expected
    fields[:,1] = fields[:,0]
    assert sum(s*fields[i,0]*fields[j,1]*fields[k,2] for i,j,k,s in records) == 0


def test_prior_conjugate_decuplet_cancels_the_family_trace_probe():
    anomaly = cubic.calculate()['anomalies']
    charges = anomaly['family_probe_diagonal']
    dual_weights = [-sum(n*q for n,q in zip(exponents,charges))
                    for exponents in product(range(4), repeat=3) if sum(exponents) == 3]
    assert len(dual_weights) == 10
    assert sum(x**3 for x in dual_weights) + anomaly['chiral_81_family_probe_trace'] == 0


@pytest.fixture(scope='module')
def point():
    result = vacuum.calculate()
    X = np.zeros((81,3), dtype=np.int64)
    for j, support in enumerate(result['chosen_supports']):
        X[support,j] = 1
    return X, vacuum.gauge_generators(cubic.calculate()), vacuum.native.build_records()


def test_independent_complex_species_rotation_preserves_zero_residuals(point):
    X, generators, records = point
    U = np.array([[3,4,0],[-4,3,0],[0,0,5j]])
    Y = X @ U
    assert np.array_equal(Y.conj().T @ Y,75*np.eye(3))
    assert all(not np.any(vacuum.bracket(Y[:,a],Y[:,b],records)) for a,b in combinations(range(3),2))
    assert all(np.trace(Y.conj().T @ g @ Y) == 0 for g in generators)


def test_actual_potential_quartic_along_species_tangent_and_quadratic_radially(point):
    X, generators, records = point

    def energy(Y):
        f = sum(np.linalg.norm(vacuum.bracket(Y[:,a],Y[:,b],records))**2 for a,b in combinations(range(3),2))
        d = sum(abs(np.trace(Y.conj().T @ g @ Y))**2 for g in generators)
        gram = np.linalg.norm(Y.conj().T @ Y-3*np.eye(3))**2
        return f+d+gram

    e = 0.01
    assert energy(X+1j*e*X) / energy(X+0.5j*e*X) == pytest.approx(16, rel=1e-9)
    assert energy(X+e*X) / energy(X+0.5*e*X) == pytest.approx(4, rel=0.01)


def test_server_replay_at_different_prime_certifies_native_ranks_and_brackets():
    server = json.loads((ROOT/'data/toe_20261108_signed_cubic_server.json').read_text())
    assert server['prime'] == 103
    assert server['symmetric27']['rank'] == cubic.calculate()['cubic_27']['rank_over_Q']
    assert server['exterior81']['rank'] == cubic.calculate()['alternating_81']['exact_rank']
    assert server['bracketL1'] == [0,0,0]
