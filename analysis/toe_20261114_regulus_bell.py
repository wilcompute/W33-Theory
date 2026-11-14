"""Bell spectrum and exact PPT obstruction for the shortened F8 regulus."""

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from toe_20261114_regulus_quotient_witness import determinant, trace


OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_regulus_bell.json"
STABILIZER = (0, 12 | (51 << 6), 53 | (17 << 6), 57 | (34 << 6))


def pairing(u, v):
    return trace(determinant(u & 63, v >> 6) ^ determinant(v & 63, u >> 6))


def representative(v):
    return min(v ^ s for s in STABILIZER)


def calculate():
    assert {u ^ v for u, v in product(STABILIZER, repeat=2)} == set(STABILIZER)
    assert not any(pairing(u, v) for u, v in product(STABILIZER, repeat=2))
    centralizer = [v for v in range(4096) if not any(pairing(v, s) for s in STABILIZER)]
    labels = sorted({representative(v) for v in centralizer})
    weights = Counter(representative(v) for v in centralizer if v and not determinant(v & 63, v >> 6))
    assert Counter(weights.values()) == {1: 63, 2: 36}
    assert len(labels) == 256 and 0 not in weights

    # Choose a quadratic refinement of the logical symplectic form.
    # Its zero locus identifies symmetric Bell vectors in this chart.
    quadratic = {0: 0}
    for v in labels:
        if v not in quadratic:
            quadratic.update({representative(u ^ v): z ^ pairing(u, v)
                              for u, z in list(quadratic.items())})
    assert all(quadratic[representative(u ^ v)] == quadratic[u] ^ quadratic[v] ^ pairing(u, v)
               for u, v in product(labels, repeat=2))
    symmetric = [u for u in labels if quadratic[u] == 0]
    assert len(symmetric) == 136
    spectrum = [sum(w*(-1)**(quadratic[v] ^ pairing(u, v)) for v, w in weights.items())
                for u in labels]
    assert Counter(spectrum) == {-9: 184, 23: 72}
    high = [u for u, e in zip(labels, spectrum) if e == 23]
    assert set(high) <= set(symmetric)
    # Partial transpose is diagonal in the same Bell basis, with
    # eigenvalues obtained from this sign matrix divided by 16.
    transform = np.array([[(-1)**quadratic[representative(u ^ v)] for v in symmetric]
                          for u in labels], dtype=np.int64)
    objective = np.array([23 if u in high else -9 for u in symmetric], dtype=np.int64)
    lp = linprog(objective, A_ub=-transform, b_ub=np.zeros(len(labels)),
                 A_eq=np.ones((1, len(symmetric))), b_eq=[1], method="highs")
    assert lp.success
    probabilities = [Fraction(float(x)).limit_denominator(100000) for x in lp.x]
    assert all(p >= 0 for p in probabilities) and sum(probabilities) == 1
    denominator = int(np.lcm.reduce([p.denominator for p in probabilities]))
    integers = np.array([int(p*denominator) for p in probabilities], dtype=np.int64)
    assert int(objective @ integers) == 0 and (transform @ integers >= 0).all()
    # The original multiplicities are a feasible dual. On symmetric
    # columns the quadratic refinement polarizes into the Bell spectrum.
    dual = np.array([weights[u] for u in labels], dtype=np.int64)
    assert (dual >= 0).all()
    np.testing.assert_array_equal(dual @ transform, objective)
    return dict(status="PASS", stabilizer=STABILIZER, weighted_logical_terms=dict(single=63, double=36),
                quadratic_refinement=sorted(quadratic.items()), high_bell_labels=high,
                bell_spectrum=dict(low=-9, low_multiplicity=184, high=23, high_multiplicity=72),
                ppt_witness_denominator=denominator,
                ppt_dual_support=[[u, int(x)] for u, x in zip(labels, dual) if x],
                ppt_witness_support=[[v, int(n)] for v, n in zip(symmetric, integers) if n])


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["bell_spectrum"], result["ppt_witness_denominator"], flush=True)
