"""Finite-copy postselection bounds for the native split E6 charge boost."""

import json
from itertools import product
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261113_e6_postselection.json"
BOOST = ROOT / "data/toe_20261113_pauli_e6_positivity.json"


def calculate():
    boost = json.loads(BOOST.read_text(encoding="utf-8"))
    witness = boost["output_pauli_expectation_above_one"]["label"]
    gain = sp.Integer(boost["boost_scale"])**boost["boost_weights"][witness]
    assert gain == 2
    x = sp.symbols("x", real=True)

    # Compress any instrument on commuting inputs to response probabilities
    # conditioned on each string of Pauli eigenspaces.
    weights = {}
    for copies in range(1, 7):
        likelihoods = [sp.prod((1+sign*x)/2 for sign in signs)
                       for signs in product((-1, 1), repeat=copies)]
        assert sp.expand(sum(likelihoods)) == 1
        outside = sp.Rational(3, 4)
        assert all(w.subs(x, outside) > 0 for w in likelihoods)
        assert gain*outside > 1
        same_sign = likelihoods[0]+likelihoods[-1]
        expectation = sp.factor((likelihoods[-1]-likelihoods[0])/same_sign)
        weights[copies] = dict(unanimous_success=str(sp.factor(same_sign)),
                               unanimous_expectation=str(expectation))

    r = sp.symbols("r", positive=True)
    a = ((1+r)/(1-r))**2
    endpoint_bound = sp.factor((a-1)/(a+1))
    assert sp.simplify(endpoint_bound - 2*r/(1+r*r)) == 0
    error = sp.factor(gain*r-endpoint_bound)
    assert sp.simplify(error - 2*r**3/(1+r*r)) == 0
    # The unanimous filter attains the endpoint bound and its pointwise
    # error increases with absolute input, yielding the interval minimax.
    unanimous_two = 2*x/(1+x*x)
    derivative = sp.factor(sp.diff(gain*x-unanimous_two, x))
    assert derivative == 2*x**2*(x**2+3)/(x**2+1)**2
    radius = sp.Rational(1, 4)
    # Measure every Pauli on an independent block of copies, then
    # project the amplified estimator onto the charge-state body.
    scale = sp.Integer(boost["boost_scale"])
    squared_gains = sum(scale**(2*w) for w in boost["boost_weights"].values())
    assert squared_gains == sp.Rational(81, 2)
    return dict(status="PASS", pauli_axis=witness, gain=int(gain),
                finite_copy_exactness="impossible on any nonempty interval",
                positive_full_rank_witness_input="3/4",
                nonphysical_target_expectation="3/2",
                general_endpoint_bound="tanh(n atanh(r))",
                unanimous_controls=weights, two_copy_minimax_error=str(error),
                two_copy_minimum_success="1/2",
                deterministic_full_body_approximation=dict(
                    independent_measurement_groups=27, squared_gains=str(squared_gains),
                    trace_distance_bound="sqrt(squared_gains / copies_per_group) / 2"),
                example=dict(radius=str(radius), two_copy_worst_error=str(error.subs(r, radius)),
                             one_copy_worst_error=str(radius)))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
