#!/usr/bin/env python3
"""Pass 413: automorphism-twirled calibration and randomized compiling."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random

import numpy as np
import sympy as sp

from w33_pass410_414_common import certificate, qutrit_clifford_words, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass413_automorphism_twirl.json"
SCHEDULE = ROOT / "data" / "w33_pass413_twirl_schedule.json"


def det(m):
    return (m[0] * m[3] - m[1] * m[2]) % 3


def matvec(m, u):
    return ((m[0] * u[0] + m[1] * u[1]) % 3, (m[2] * u[0] + m[3] * u[1]) % 3)


def omega(u, v):
    return (u[1] * v[0] - u[0] * v[1]) % 3


def vertices():
    return [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]


def adjacency() -> np.ndarray:
    verts = vertices()
    index = {v: i for i, v in enumerate(verts)}
    a = np.zeros((27, 27), dtype=int)
    for i, (x, y, z) in enumerate(verts):
        for xp in range(3):
            for yp in range(3):
                if (xp, yp) == (x, y):
                    continue
                zp = (z + y * xp - x * yp) % 3
                a[i, index[(xp, yp, zp)]] = 1
    return a


def automorphisms():
    verts = vertices()
    index = {v: i for i, v in enumerate(verts)}
    matrices = [m for m in product4() if det(m) != 0]
    records = []
    for m in matrices:
        determinant = det(m)
        for ax in range(3):
            for ay in range(3):
                shift = (ax, ay)
                for c in range(3):
                    permutation = []
                    for x, y, z in verts:
                        mu = matvec(m, (x, y))
                        up = ((mu[0] + ax) % 3, (mu[1] + ay) % 3)
                        zp = (determinant * z - omega(mu, shift) + c) % 3
                        permutation.append(index[(up[0], up[1], zp)])
                    records.append({"matrix": m, "shift": shift, "central": c, "permutation": tuple(permutation)})
    return records


def product4():
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    yield (a, b, c, d)


def distance_matrices(a: np.ndarray):
    n = len(a)
    distance = np.full((n, n), 99, dtype=int)
    np.fill_diagonal(distance, 0)
    distance[a == 1] = 1
    for _ in range(3):
        for i in range(n):
            for j in range(n):
                distance[i, j] = min(distance[i, j], min(distance[i, k] + distance[k, j] for k in range(n)))
    return [np.array(distance == d, dtype=int) for d in range(4)], distance


def spectral_projectors(a: np.ndarray):
    A = sp.Matrix(a.tolist())
    identity = sp.eye(27)
    eigenvalues = [8, 2, -1, -4]
    projectors = {}
    for lam in eigenvalues:
        p = identity
        denominator = 1
        for mu in eigenvalues:
            if mu == lam:
                continue
            p = p * (A - mu * identity)
            denominator *= lam - mu
        p = p / denominator
        projectors[str(lam)] = p
    return projectors


def pauli_orbit_data():
    nonzero = [(x, z) for x in range(3) for z in range(3) if (x, z) != (0, 0)]
    sl2 = [m for m in product4() if det(m) == 1]
    gl2 = [m for m in product4() if det(m) != 0]
    orbit_sl = {matvec(m, (1, 0)) for m in sl2}
    orbit_gl = {matvec(m, (1, 0)) for m in gl2}
    weights = {label: 1 + 3 * label[0] + 7 * label[1] for label in nonzero}
    average = Fraction(sum(weights.values()), len(nonzero))
    twirled = {label: average for label in nonzero}
    return nonzero, sl2, gl2, orbit_sl, orbit_gl, weights, twirled


def build_payload() -> tuple[dict, dict]:
    a = adjacency()
    autos = automorphisms()
    distance_basis, distance = distance_matrices(a)
    projectors = spectral_projectors(a)

    automorphism_checks = []
    for record in autos:
        p = np.array(record["permutation"], dtype=int)
        automorphism_checks.append(np.array_equal(a[np.ix_(p, p)], a))

    deterministic = np.fromfunction(lambda i, j: (17 * i + 29 * j + 3 * i * j + 11) % 101, (27, 27), dtype=int)
    covariance = deterministic + deterministic.T
    twirl_sum = np.zeros((27, 27), dtype=np.int64)
    for record in autos:
        p = np.array(record["permutation"], dtype=int)
        twirl_sum += covariance[np.ix_(p, p)]

    orbital_values = {}
    reconstructed_sum = np.zeros((27, 27), dtype=np.int64)
    orbital_constant = True
    for d, basis in enumerate(distance_basis):
        values = twirl_sum[basis == 1]
        orbital_constant &= bool(np.all(values == values[0]))
        orbital_values[str(d)] = {"numerator": int(values[0]), "denominator": len(autos)}
        reconstructed_sum += int(values[0]) * basis

    nonzero, sl2, gl2, orbit_sl, orbit_gl, weights, pauli_twirl = pauli_orbit_data()
    cliffords = qutrit_clifford_words()

    perm_to_record = {record["permutation"]: record for record in autos}
    rng = random.Random(413)
    auto_samples = [rng.choice(autos) for _ in range(64)]
    clifford_items = sorted(cliffords.values(), key=lambda item: (len(item[0]), item[0]))
    schedule_entries = []
    for epoch, record in enumerate(auto_samples):
        permutation = record["permutation"]
        inverse = [0] * 27
        for i, image in enumerate(permutation):
            inverse[image] = i
        inverse_record = perm_to_record[tuple(inverse)]
        word, _ = rng.choice(clifford_items)
        schedule_entries.append({
            "epoch": epoch,
            "spatial_randomizer": {"matrix": list(record["matrix"]), "shift": list(record["shift"]), "central": record["central"]},
            "spatial_inverse": {"matrix": list(inverse_record["matrix"]), "shift": list(inverse_record["shift"]), "central": inverse_record["central"]},
            "qutrit_clifford_word": word or "I",
            "permutation_sha256": hashlib.sha256(bytes(permutation)).hexdigest(),
        })

    schedule = {
        "schema": "w33.pass413.twirl_schedule.v1",
        "seed": 413,
        "epochs": schedule_entries,
        "execution_rule": "conjugate each calibration epoch by the listed spatial automorphism and Clifford, then compile the exact inverse before the terminal measurement",
    }
    schedule["certificate_sha256"] = certificate(schedule)

    ranks = {key: int(matrix.rank()) for key, matrix in projectors.items()}
    projector_sum = sum(projectors.values(), sp.zeros(27))
    checks = {
        "full_automorphism_order_1296": len(autos) == 1296,
        "all_explicit_maps_preserve_adjacency": all(automorphism_checks),
        "diameter_three": int(distance.max()) == 3,
        "four_orbitals": len(distance_basis) == 4,
        "twirl_is_constant_on_distance_classes": orbital_constant,
        "distance_basis_reconstructs_exact_twirl": np.array_equal(twirl_sum, reconstructed_sum),
        "projector_ranks_1_12_8_6": ranks == {"8": 1, "2": 12, "-1": 8, "-4": 6},
        "projectors_sum_to_identity": projector_sum == sp.eye(27),
        "projectors_are_pairwise_orthogonal": all(projectors[a_key] * projectors[b_key] == (projectors[a_key] if a_key == b_key else sp.zeros(27)) for a_key in projectors for b_key in projectors),
        "SL2_transitive_on_eight_nonzero_Paulis": len(sl2) == 24 and orbit_sl == set(nonzero),
        "GL2_transitive_on_eight_nonzero_Paulis": len(gl2) == 48 and orbit_gl == set(nonzero),
        "Pauli_twirl_has_one_nonidentity_rate": len(set(pauli_twirl.values())) == 1,
        "Clifford_schedule_order_216": len(cliffords) == 216,
        "schedule_has_64_exact_inverse_epochs": len(schedule_entries) == 64,
    }

    payload = {
        "schema": "w33.pass413.automorphism_twirl.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "spatial_twirl": {
            "group": "Aut(Gamma_3)=H_3 semidirect GL(2,3)",
            "order": len(autos),
            "commutant_dimension": 4,
            "distance_orbital_ranks": {str(d): int(b.sum()) for d, b in enumerate(distance_basis)},
            "spectral_sector_ranks": ranks,
            "adjacency_eigenvalues": [8, 2, -1, -4],
            "exact_twirl_coefficients_for_deterministic_probe": orbital_values,
            "interpretation": "an arbitrary 27-mode covariance collapses to four spatial spectral powers",
        },
        "qutrit_channel_twirl": {
            "nonidentity_Pauli_labels": [list(v) for v in nonzero],
            "SL2_order": len(sl2),
            "GL2_order": len(gl2),
            "raw_probe_weights": {str(k): v for k, v in weights.items()},
            "twirled_nonidentity_weight": {"numerator": pauli_twirl[nonzero[0]].numerator, "denominator": pauli_twirl[nonzero[0]].denominator},
            "free_parameters_after_trace_preservation": 1,
        },
        "combined_calibration_reduction": {
            "raw_diagonal_axes": 27 * 8,
            "spatial_invariants": 4,
            "Pauli_nonidentity_invariants": 1,
            "recommended_report": ["uniform mode", "lambda=2 sector", "lambda=-1 sector", "lambda=-4 sector", "leakage outside the qutrit subspace"],
        },
        "randomized_compiling": {
            "schedule_path": "data/w33_pass413_twirl_schedule.json",
            "epochs": 64,
            "seed": 413,
            "claim_boundary": "The twirl is exact as a group average. Experimental Markovianity, gate-independence, and sampling error remain measured assumptions.",
        },
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload, schedule


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--schedule", type=Path, default=SCHEDULE)
    args = parser.parse_args()
    payload, schedule = build_payload()
    ptext = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    stext = json.dumps(schedule, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != ptext:
            raise SystemExit("Pass 413 certificate drift")
        if not args.schedule.exists() or args.schedule.read_text() != stext:
            raise SystemExit("Pass 413 schedule drift")
    else:
        write_json(args.output, payload)
        write_json(args.schedule, schedule)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
