#!/usr/bin/env python3
"""Pass 3030 (BONKERS): exact nonabelian Fourier engine for class-invariant D4 noise.

A conjugation-invariant D4 error kernel is a class function. By Schur's lemma its Fourier
transform contains four one-dimensional scalars and one scalar two-dimensional block.
Thus eight physical symbol probabilities propagate through five spectral channels.
Bayesian multiplication still occurs in the symbol domain; only group convolution and
prediction diagonalize.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np

from bt3025_3031_common import D4, D4_INDEX, inverse, multiply

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3030_D4_FOURIER_BELIEF_results.json"

# Total masses of the five conjugacy classes: e, r^2, {r,r^3}, axis reflections,
# diagonal reflections. These are an explicit synthetic demonstration kernel.
CLASS_MASS = (Fraction(90,100), Fraction(1,100), Fraction(2,100), Fraction(3,100), Fraction(4,100))


def class_id(g):
    a,b = g
    if b == 0:
        if a == 0: return 0
        if a == 2: return 1
        return 2
    return 3 if a % 2 == 0 else 4


def element_probability(g):
    sizes=(1,1,2,2,2)
    return CLASS_MASS[class_id(g)] / sizes[class_id(g)]


def character(a,b,g):
    """One-dimensional representation r->a, s->b, with a,b in {+1,-1}."""
    rotation, reflection = g
    return (a ** rotation) * (b ** reflection)


def main():
    probabilities = [element_probability(g) for g in D4]
    assert sum(probabilities) == 1

    convolution = np.zeros((8,8), dtype=float)
    for true_index, true in enumerate(D4):
        for observation_index, observation in enumerate(D4):
            error = multiply(observation, inverse(true))
            convolution[observation_index,true_index] = float(element_probability(error))
    assert np.allclose(convolution.sum(axis=0),1)

    one_dimensional = {}
    for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
        eigenvalue = sum(element_probability(g)*character(a,b,g) for g in D4)
        one_dimensional[f"r_to_{a}_s_to_{b}"] = str(eigenvalue)

    # Standard two-dimensional D4 character is [2,-2,0,0,0] on the five classes;
    # the scalar Fourier block is (1/2) sum_g p(g) chi(g) = p(e)-p(r^2).
    two_dimensional_scalar = CLASS_MASS[0] - CLASS_MASS[1]
    expected = sorted([1.0,0.86,0.88,0.90] + [0.89]*4)
    observed = sorted(float(x.real) for x in np.linalg.eigvals(convolution))
    assert np.allclose(observed,expected)

    payload = {
        "schema": "w33.pass3030.d4_fourier_belief_engine.v1",
        "status": "COMPLETE_EXACT_CLASS_FUNCTION_DIAGONALIZATION",
        "synthetic_class_masses": [str(x) for x in CLASS_MASS],
        "one_dimensional_fourier_eigenvalues": one_dimensional,
        "two_dimensional_block_scalar": str(two_dimensional_scalar),
        "regular_representation_eigenvalue_multiset": {
            "1":1,"43/50":1,"22/25":1,"9/10":1,"89/100":4
        },
        "spectral_contraction_off_trivial": "9/10",
        "physical_symbol_count": 8,
        "spectral_channel_count": 5,
        "interpretation": "Four one-dimensional characters plus one scalar two-dimensional irrep block propagate any conjugation-invariant D4 convolution exactly.",
        "hardware_use": "Implement drift prediction and likelihood convolution as five fixed spectral gains; transform back before nonlinear Bayesian normalization.",
        "checks": {
            "class_masses_sum_one": sum(CLASS_MASS)==1,
            "matrix_stochastic": bool(np.allclose(convolution.sum(axis=0),1)),
            "eigenvalues_exactly_reproduced": True,
        },
        "claim_boundary": "Exact finite harmonic analysis for conjugation-invariant D4 convolution. General non-class noise requires a full 2x2 Fourier block, and Bayesian evidence multiplication does not diagonalize.",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status":payload["status"],"one_dimensional":one_dimensional,"two_dimensional":str(two_dimensional_scalar)}, sort_keys=True))


if __name__ == "__main__":
    main()
