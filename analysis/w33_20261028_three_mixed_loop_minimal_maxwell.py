#!/usr/bin/env python3
"""Minimal three-channel, native-cone gauge completion on the H27 voltage cover.

Uses actual selected105 short faces, six translated 16-edge commutators,
the established H(theta) family, and native acoustic metric M.
Algebraic results are exact; Bloch generic ranks are finite-field witnesses.
Physics: four Euclidean spatial periods, no Lorentzian or quantum TOE claim.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import sys

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261027_native_bloch_face_module import geometry  # noqa: E402


def frac_matrix(rows):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in rows])


def rank_mod(rows, p, width=135):
    piv = {}
    for row in rows:
        vec = [int(x) % p for x in row]
        for c in range(width):
            value = vec[c]
            if value == 0:
                continue
            if c in piv:
                pivot = piv[c]
                for j in range(c, width):
                    vec[j] = (vec[j] - value * pivot[j]) % p
            else:
                inverse = pow(value, -1, p)
                piv[c] = [(x * inverse) % p for x in vec]
                break
    return len(piv)


def bloch_row(face, voltages, z, p):
    result = [0] * len(voltages)
    position = [0, 0, 0, 0]
    for edge, sign in face:
        edge, sign = int(edge), int(sign)
        if sign == -1:
            for j in range(4):
                position[j] -= int(voltages[edge][j])
        monomial = sign
        for j in range(4):
            exponent = position[j]
            value = pow(z[j], exponent, p) if exponent >= 0 else pow(pow(z[j], -1, p), -exponent, p)
            monomial = (monomial * value) % p
        result[edge] = (result[edge] + monomial) % p
        if sign == 1:
            for j in range(4):
                position[j] += int(voltages[edge][j])
    assert position == [0, 0, 0, 0], "Not a closed native-voltage loop"
    return result


@lru_cache(maxsize=1)
def certificate():
    previous = json.loads((ROOT / "data/w33_20261027_native_bloch_face_module.json").read_text())
    family = json.loads((ROOT / "data/w33_20261027_five_front_followthrough.json").read_text())
    faces = json.loads((ROOT / "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())
    H0 = frac_matrix(previous["engineered_matched_metric"]["six_loop_flux_coupling_H"])
    J = frac_matrix(family["metric_classification"]["J"])
    R = sp.Matrix([[1, 0, 5, -5, 1, 0],
                   [0, 1, -1, 0, 1, 0],
                   [0, 0, 5, -5, 0, 1]])
    Hminus = H0 - 2 * J
    Hplus = H0 + 2 * J
    P = [0, 1, 5]
    K = Hminus.extract(P, P)
    assert K == sp.Matrix([[sp.Rational(25, 9), -sp.Rational(5, 3), -sp.Rational(26, 9)],
                           [-sp.Rational(5, 3), sp.Rational(11, 3), 2],
                           [-sp.Rational(26, 9), 2, sp.Rational(28, 9)]])
    assert Hminus == R.T * K * R
    assert R.rank() == Hminus.rank() == Hplus.rank() == 3
    minors = [K[:i, :i].det() for i in range(1, 4)]
    assert all(x > 0 for x in minors)
    pp = [1, 2, 3]
    kp = Hplus.extract(pp, pp)
    rp = kp.inv() * Hplus.extract(pp, range(6))
    assert Hplus == rp.T * kp * rp and all(kp[:i, :i].det() > 0 for i in range(1, 4))

    M = frac_matrix(previous["effective_symbol"]["harmonic_link_gram_M"])
    W = sp.Matrix(previous["deck_loop_periods"])
    assert W.det() == 1 and M.det() == 54**2
    n = sp.Matrix(sp.symbols("n0:4"))
    y = W * n
    pairs = list(combinations(range(4), 2))
    C = sp.Matrix([[y[i] * W[j, a] - y[j] * W[i, a]
                    for a in range(4)] for i, j in pairs])
    target = ((n.dot(M * n)) * M - (M * n) * (M * n).T) / 27
    assert (C.T * R.T * K * R * C - target).applyfunc(sp.expand) == sp.zeros(4)
    assert (C.T * J * C).applyfunc(sp.expand) == sp.zeros(4)

    # Six positive nontrivial integer harmonics plus three positive unit
    # harmonics make an explicit compact, nonnegative periodic potential.
    eps = sp.Rational(1, 10000)
    charges = [(3, -4, -4), (3, -4, -3), (3, 4, -3),
               (4, -4, -3), (4, -3, -4), (4, 4, -3)]
    weights = [sp.Rational(49937, 630000), sp.Rational(21313, 378000),
               sp.Rational(49241, 1350000), sp.Rational(1241, 90000),
               sp.Rational(142189, 3150000), sp.Rational(1, 56)]
    reconstructed = eps * sp.eye(3)
    for charge, weight in zip(charges, weights):
        q = sp.Matrix(charge)
        assert weight > 0
        reconstructed += weight * q * q.T
    assert reconstructed == K

    incidence, voltages, edges, lookup, neighbors = geometry()
    assert len(edges) == 135 and len(voltages) == 135
    selected = [f["boundary"] for f in faces["independent_face_basis"]]
    loops = previous["commutator_boundaries"]
    assert len(selected) == 105 and len(loops) == 6
    controls = []
    for modulus, values in ((101, (2, 3, 5, 7)),
                            (103, (2, 3, 5, 7)),
                            (107, (3, 4, 7, 11))):
        short = [bloch_row(f, voltages, values, modulus) for f in selected]
        extra = [bloch_row(f, voltages, values, modulus) for f in loops]
        mixed = [[sum(int(R[i, j]) * extra[j][e] for j in range(6)) % modulus
                  for e in range(135)] for i in range(3)]
        rank_short = rank_mod(short, modulus)
        rank_total = rank_mod(short + mixed, modulus)
        histogram = {}
        for ids in combinations(range(6), 3):
            rnk = rank_mod(short + [extra[i] for i in ids], modulus)
            histogram[str(rnk)] = histogram.get(str(rnk), 0) + 1
        assert rank_short == 105 and rank_total == 108
        assert histogram == {"108": 16, "107": 4} or histogram == {"107": 4, "108": 16}

        D = np.zeros((135, 27), dtype=np.int64)
        for e, (a, b) in enumerate(edges):
            mon = 1
            for j in range(4):
                exponent = int(voltages[e][j])
                base = values[j]
                mon = mon * (pow(base, exponent, modulus) if exponent >= 0
                             else pow(pow(base, -1, modulus), -exponent, modulus)) % modulus
            D[e, int(a)] = modulus - 1
            D[e, int(b)] = mon
        F = np.array(short + mixed, dtype=np.int64)
        assert not np.any((F @ D) % modulus)
        assert rank_mod(D.tolist(), modulus, 27) == 27
        controls.append({"prime": modulus, "values": list(values),
                         "short_rank": rank_short, "three_mixed_rank": rank_total,
                         "three_individual_rank_histogram": histogram,
                         "gradient_rank": 27, "Ward_identity_exact": True})

    return {
        "status": "EXACT_THREE_MIXED_LOOP_NATIVE_MAXWELL_CONE",
        "base_faces": 105, "native_commutators": 6,
        "minimal_extra_flux_channels": 3,
        "H_endpoint": "H0-2J",
        "H_endpoint_rank": 3,
        "both_endpoints_positive_semidefinite_rank_three": True,
        "mixing_R_3x6": R.tolist(),
        "positive_K_3x3": [[str(x) for x in row] for row in K.tolist()],
        "positive_K_leading_principal_minors": list(map(str, minors)),
        "native_M_4x4": [[str(x) for x in row] for row in M.tolist()],
        "four_variable_symbol_identity":
            "(R*C(n))^T K (R*C(n)) = ((n^T M n) M - (M n)(M n)^T)/27",
        "three_mixed_channel_bloch_controls": controls,
        "compact_potential": {
            "mixed_loop_angles": "g=R*f with six literal commutator phases f",
            "formula": "V(g)=1/10000 sum_i(1-cos(g_i))+sum_{a=1}^6 w_a(1-cos(q_a.g))",
            "unit_harmonic_weight": "1/10000",
            "charge_vectors": [list(x) for x in charges],
            "positive_weights": [str(x) for x in weights],
            "unique_minimum_in_g_torus": "g=0 modulo 2pi",
            "Hessian_in_six_f_angles": "R^T K R = H0-2J",
            "number_of_cosine_harmonics": 9
        },
        "caution": ("This is a compact, gauge-invariant finite-loop model and exact "
                    "leading Euclidean common-cone identity; not an experimentally "
                    "selected coupling, no Lorentzian time, no Einstein dynamics. "
                    "Three null directions in six-flux metric remain, and finite-k "
                    "spectral properties may differ from six-flux completion.")
    }


if __name__ == "__main__":
    data = json.dumps(certificate(), indent=2) + "\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(data, encoding="utf-8")
    else:
        print(data, end="")
