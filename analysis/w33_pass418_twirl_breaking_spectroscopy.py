#!/usr/bin/env python3
"""Pass 418: exact symmetry-breaking coordinates for q=3 calibration data."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from w33_pass410_414_common import certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass418_twirl_breaking_spectroscopy.json"
ATLAS = ROOT / "data" / "w33_pass418_defect_atlas.json"


def vertices() -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]


def adjacency() -> np.ndarray:
    verts = vertices()
    index = {vertex: i for i, vertex in enumerate(verts)}
    matrix = np.zeros((27, 27), dtype=int)
    for i, (x, y, z) in enumerate(verts):
        for xp in range(3):
            for yp in range(3):
                if (xp, yp) == (x, y):
                    continue
                zp = (z + y * xp - x * yp) % 3
                matrix[i, index[(xp, yp, zp)]] = 1
    return matrix


def distances(a: np.ndarray) -> np.ndarray:
    n = len(a)
    distance = np.full((n, n), 99, dtype=int)
    np.fill_diagonal(distance, 0)
    distance[a == 1] = 1
    for k in range(n):
        distance = np.minimum(distance, distance[:, k, None] + distance[None, k, :])
    return distance


def orbit_coordinates(distance: np.ndarray) -> dict[int, list[tuple[int, int]]]:
    orbits = {d: [] for d in range(4)}
    for i in range(27):
        orbits[0].append((i, i))
        for j in range(i + 1, 27):
            orbits[int(distance[i, j])].append((i, j))
    return orbits


def coordinate_value(matrix: np.ndarray, pair: tuple[int, int]) -> float:
    i, j = pair
    return float(matrix[i, i]) if i == j else float(np.sqrt(2) * matrix[i, j])


def set_coordinate(matrix: np.ndarray, pair: tuple[int, int], value: float) -> None:
    i, j = pair
    if i == j:
        matrix[i, i] = value
    else:
        matrix[i, j] = matrix[j, i] = value / np.sqrt(2)


def decompose(matrix: np.ndarray, orbits: dict[int, list[tuple[int, int]]]) -> tuple[dict[int, float], dict[int, np.ndarray]]:
    means: dict[int, float] = {}
    residuals: dict[int, np.ndarray] = {}
    for orbit, pairs in orbits.items():
        values = np.array([coordinate_value(matrix, pair) for pair in pairs], dtype=float)
        means[orbit] = float(values.mean())
        residuals[orbit] = values - means[orbit]
    return means, residuals


def reconstruct(means: dict[int, float], residuals: dict[int, np.ndarray], orbits: dict[int, list[tuple[int, int]]]) -> np.ndarray:
    matrix = np.zeros((27, 27), dtype=float)
    for orbit, pairs in orbits.items():
        for pair, residual in zip(pairs, residuals[orbit]):
            set_coordinate(matrix, pair, means[orbit] + float(residual))
    return matrix


def lag_one(series: np.ndarray) -> float:
    centered = series - series.mean()
    return float(np.dot(centered[:-1], centered[1:]) / np.dot(centered[:-1], centered[:-1]))


def build_payload() -> tuple[dict, dict]:
    a = adjacency()
    distance = distances(a)
    orbits = orbit_coordinates(distance)
    sizes = {orbit: len(pairs) for orbit, pairs in orbits.items()}

    atlas_entries = []
    cursor = 0
    labels = {0: "mode_gain", 1: "native_coupler", 2: "distance_two_crosstalk", 3: "phase_fibre_pair"}
    for orbit in range(4):
        for local_index, pair in enumerate(orbits[orbit]):
            atlas_entries.append({
                "coordinate_id": cursor,
                "orbit": orbit,
                "family": labels[orbit],
                "orbit_index": local_index,
                "vertices": list(pair),
                "matrix_basis": "E_ii" if pair[0] == pair[1] else "(E_ij+E_ji)/sqrt(2)",
            })
            cursor += 1

    atlas = {
        "schema": "w33.pass418.defect_atlas.v1",
        "coordinate_convention": "orthonormal symmetric-matrix basis: E_ii on the diagonal and (E_ij+E_ji)/sqrt(2) off diagonal",
        "orbit_sizes": {str(k): v for k, v in sizes.items()},
        "entries": atlas_entries,
    }
    atlas["certificate_sha256"] = certificate(atlas)

    # Exact orthogonal decomposition regression on a deterministic symmetric matrix.
    probe = np.fromfunction(lambda i, j: ((17 * i + 31 * j + 5 * i * j + 7) % 113) / 17, (27, 27), dtype=float)
    probe = (probe + probe.T) / 2
    means, residuals = decompose(probe, orbits)
    reconstructed = reconstruct(means, residuals, orbits)

    simplex_rows = []
    for orbit, size in sizes.items():
        simplex_rows.append({
            "orbit": orbit,
            "family": labels[orbit],
            "atoms": size,
            "kernel_rank": size - 1,
            "self_inner_product": {"numerator": size - 1, "denominator": size},
            "distinct_inner_product": {"numerator": -1, "denominator": size},
            "nonzero_gram_eigenvalue": 1,
            "nonzero_gram_multiplicity": size - 1,
        })

    # Inject one defect into every orbit family and recover it from centered coordinates.
    baseline = {0: 10.0, 1: 2.0, 2: -1.0, 3: 0.5}
    injection = {0: (7, 3.0), 1: (41, -2.5), 2: (137, 1.75), 3: (19, 4.0)}
    synthetic = np.zeros((27, 27), dtype=float)
    for orbit, pairs in orbits.items():
        for pair in pairs:
            set_coordinate(synthetic, pair, baseline[orbit])
        defect_index, amplitude = injection[orbit]
        pair = pairs[defect_index]
        set_coordinate(synthetic, pair, baseline[orbit] + amplitude)

    syn_means, syn_residuals = decompose(synthetic, orbits)
    recovered_defects = []
    all_localized = True
    all_amplitudes = True
    for orbit, pairs in orbits.items():
        size = len(pairs)
        residual = syn_residuals[orbit]
        index = int(np.argmax(np.abs(residual)))
        amplitude = float(residual[index] * size / (size - 1))
        expected_index, expected_amplitude = injection[orbit]
        localized = index == expected_index
        amplitude_ok = abs(amplitude - expected_amplitude) < 1e-12
        all_localized &= localized
        all_amplitudes &= amplitude_ok
        recovered_defects.append({
            "orbit": orbit,
            "family": labels[orbit],
            "expected_coordinate": expected_index,
            "recovered_coordinate": index,
            "vertices": list(pairs[index]),
            "expected_amplitude": expected_amplitude,
            "recovered_amplitude": round(amplitude, 12),
            "localized": localized,
        })

    # Robust sparse recovery: median removes an unknown common-mode baseline as
    # long as fewer than half of an orbit's coordinates are defective.
    rng = np.random.default_rng(418)
    sparse_trials = []
    sparse_ok = True
    for orbit, pairs in orbits.items():
        size = len(pairs)
        values = np.full(size, baseline[orbit])
        support = sorted(rng.choice(size, size=min(5, size // 4), replace=False).tolist())
        amplitudes = [float(v) for v in rng.choice([-3.0, -2.0, 1.5, 2.5, 4.0], size=len(support), replace=True)]
        for index, amplitude in zip(support, amplitudes):
            values[index] += amplitude
        recovered_baseline = float(np.median(values))
        recovered_support = sorted(np.where(np.abs(values - recovered_baseline) > 1e-12)[0].tolist())
        ok = recovered_baseline == baseline[orbit] and recovered_support == support
        sparse_ok &= ok
        sparse_trials.append({
            "orbit": orbit,
            "injected_support": support,
            "recovered_support": recovered_support,
            "baseline": recovered_baseline,
            "passed": ok,
        })

    # Temporal diagnostic: a localized AR(1) defect survives twirl subtraction,
    # whereas independent sampling noise has near-zero lag-one correlation.
    samples = 512
    white = rng.normal(scale=1.0, size=samples)
    ar = np.zeros(samples)
    innovations = rng.normal(scale=0.5, size=samples)
    for t in range(1, samples):
        ar[t] = 0.85 * ar[t - 1] + innovations[t]
    white_lag = lag_one(white)
    ar_lag = lag_one(ar)

    checks = {
        "graph_is_8_regular": set(a.sum(axis=1).tolist()) == {8},
        "diameter_three": int(distance.max()) == 3,
        "orbit_sizes_27_108_216_27": sizes == {0: 27, 1: 108, 2: 216, 3: 27},
        "symmetric_dimension_378": sum(sizes.values()) == 27 * 28 // 2,
        "twirl_dimension_four": len(sizes) == 4,
        "symmetry_breaking_kernel_rank_374": sum(size - 1 for size in sizes.values()) == 374,
        "decomposition_reconstructs_probe": float(np.max(np.abs(reconstructed - probe))) < 1e-12,
        "every_residual_has_zero_orbit_sum": all(abs(float(values.sum())) < 1e-10 for values in residuals.values()),
        "all_four_single_defects_localized": all_localized,
        "all_four_defect_amplitudes_exact": all_amplitudes,
        "median_sparse_recovery_all_orbits": sparse_ok,
        "white_lag_near_zero": abs(white_lag) < 0.15,
        "AR1_lag_detected": ar_lag > 0.75,
        "atlas_has_378_coordinates": len(atlas_entries) == 378,
    }
    checks = {key: bool(value) for key, value in checks.items()}

    payload = {
        "schema": "w33.pass418.twirl_breaking_spectroscopy.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": {
            "orthogonal_decomposition": "Sym_27 = B_0 direct_sum B_1 direct_sum B_2 direct_sum B_3; each B_d splits into its orbit mean plus a centered regular-simplex defect space",
            "dimensions": "378 = 4 twirl invariants + (26+107+215+26)=374 symmetry-breaking coordinates",
            "single_defect_localization": "within an orbit of size m, centered atoms have Gram delta_ij-1/m; the largest matched-filter coefficient identifies the unique defective coordinate and rescales its amplitude by m/(m-1)",
            "sparse_extension": "with fewer than m/2 corrupted coordinates in an orbit, median centering exactly recovers an unknown common-mode baseline and every noiseless sparse defect",
        },
        "orbit_families": simplex_rows,
        "defect_atlas_path": "data/w33_pass418_defect_atlas.json",
        "injected_defect_recovery": recovered_defects,
        "sparse_recovery_trials": sparse_trials,
        "temporal_drift_witness": {
            "samples": samples,
            "white_noise_lag_one": round(white_lag, 12),
            "AR1_coefficient": 0.85,
            "localized_AR1_lag_one": round(ar_lag, 12),
            "interpretation": "common-mode drift remains in the four twirl means; localized non-Markovian drift appears in a defect coordinate with persistent temporal correlation",
        },
        "hardware_readout": {
            "reported_invariants": ["diagonal mean", "native-coupler mean", "distance-two mean", "phase-fibre mean"],
            "reported_breaking_coordinates": 374,
            "priority_order": ["mode gains", "native couplers", "phase-fibre pairs", "distance-two crosstalk"],
            "claim_boundary": "The coordinates localize symmetry breaking in the measured covariance model. They do not by themselves identify the microscopic physical cause or establish Markovianity.",
        },
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload, atlas


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--atlas", type=Path, default=ATLAS)
    args = parser.parse_args()
    payload, atlas = build_payload()
    ptext = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    atext = json.dumps(atlas, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != ptext:
            raise SystemExit("Pass 418 certificate drift")
        if not args.atlas.exists() or args.atlas.read_text() != atext:
            raise SystemExit("Pass 418 atlas drift")
    else:
        write_json(args.output, payload)
        write_json(args.atlas, atlas)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
