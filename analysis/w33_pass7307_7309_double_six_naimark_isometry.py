#!/usr/bin/env python3
"""Passes 7307--7309: the new double-six slices realize the old Naimark shadow.

Pass 3694 constructed an ETF(36,15) from the centered 40-line x 36-spread
incidence matrix and proved that its Naimark complement has dimension 21=1+20.
Pass 7241 subsequently built a literal 45-tritangent x 36-double-six matrix N,
and the parallel Pass 7249--7304 packet proved that centered N is a rank-20
two-distance tight frame.  This verifier adds the missing cross-carrier step:
it aligns B and N with the certified spread/double-six scheme isomorphism,
proves their centered row spaces are orthogonal complementary primitive
sectors, and completes the common 36-carrier isometry.  One scalar mode gives
the Naimark ETF; an integer lowering gives a shift-add transform.

The proof is exact integer linear algebra.  It also supplies a multiplier-free
integer lowering K with coefficients {-4,-3,6,8,9} and

    K^T K = 2592 I_36 = (36 sqrt(2))^2 I_36.

This is a finite frame/isometry and fixed-point transform certificate.  It is
not a fabricated photonic device, a loss/noise model, or a continuum theory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_pass4992_4999_common import build_base  # noqa: E402


DEFAULT_OUTPUT = ROOT / "data" / "PART_W33_PASS7307_7309_DOUBLE_SIX_NAIMARK_ISOMETRY.json"


def canonical_matrix_hash(matrix: np.ndarray) -> str:
    payload = json.dumps(matrix.astype(int).tolist(), separators=(",", ":"))
    return sha256(payload.encode("ascii")).hexdigest()


def mask_rows(matrix: np.ndarray) -> list[str]:
    masks: list[str] = []
    for row in matrix.astype(int):
        value = sum(int(bit) << index for index, bit in enumerate(row))
        masks.append(f"{value:09x}")
    return masks


def build_carriers() -> dict[str, Any]:
    base = build_base()

    # B is the old 40 W33-line x 36-spread incidence matrix.
    B = np.zeros((40, 36), dtype=np.int64)
    for spread_index, spread in enumerate(base["spreads"]):
        for line_index in spread:
            B[int(line_index), spread_index] = 1

    # Pass7241 uses M[t,D]=1 for two-line incidence and N=J+M mod 2 for
    # disjointness.  Align its double-six columns to spread columns using the
    # explicit scheme isomorphism already stored in the common builder.
    M = np.asarray(base["M"], dtype=np.int64) % 2
    N_double_six = (1 + M) % 2
    mapping = {int(d): int(s) for d, s in base["iso_ds_sp"].items()}
    assert sorted(mapping) == list(range(36))
    assert sorted(mapping.values()) == list(range(36))
    N = np.zeros((45, 36), dtype=np.int64)
    for double_six_index, spread_index in mapping.items():
        N[:, spread_index] = N_double_six[:, double_six_index]

    # A is the overlap-four spread graph SRG(36,15,6,6).  Under the mapping,
    # A-edges are double-six overlap-four pairs and N-column intersection 3;
    # complementary pairs are double-six overlap six and N-intersection 6.
    A = np.zeros((36, 36), dtype=np.int64)
    BtB = B.T @ B
    for left in range(36):
        for right in range(left + 1, 36):
            if int(BtB[left, right]) == 4:
                A[left, right] = A[right, left] = 1

    return {"base": base, "B": B, "N": N, "A": A, "mapping": mapping}


def build_certificate() -> dict[str, Any]:
    built = build_carriers()
    B = built["B"]
    N = built["N"]
    A = built["A"]
    mapping = built["mapping"]

    I = np.eye(36, dtype=np.int64)
    J = np.ones((36, 36), dtype=np.int64)

    checks: dict[str, bool] = {}
    checks["B_shape_40_by_36"] = B.shape == (40, 36)
    checks["N_shape_45_by_36"] = N.shape == (45, 36)
    checks["B_column10_row9"] = set(map(int, B.sum(axis=0))) == {10} and set(map(int, B.sum(axis=1))) == {9}
    checks["N_column15_row12"] = set(map(int, N.sum(axis=0))) == {15} and set(map(int, N.sum(axis=1))) == {12}
    checks["A_is_srg_36_15_6_6"] = (
        set(map(int, A.sum(axis=1))) == {15}
        and np.array_equal(A @ A, 9 * I + 6 * J)
    )

    raw_B_gram = B.T @ B
    raw_N_gram = N.T @ N
    checks["raw_B_gram"] = np.array_equal(raw_B_gram, 9 * I + 3 * A + J)
    checks["raw_N_gram"] = np.array_equal(raw_N_gram, 9 * I - 3 * A + 6 * J)

    pair_profile = Counter()
    for left in range(36):
        for right in range(left + 1, 36):
            pair_profile[(int(A[left, right]), int(raw_N_gram[left, right]))] += 1
    checks["aligned_pair_profile"] = pair_profile == Counter({(0, 6): 360, (1, 3): 270})

    # Integer-scaled primitive idempotents:
    #   P15n = 12 E15, P20n = 18 E20, J = 36 E1.
    P15n = 6 * I + 2 * A - J
    P20n = 9 * I - 3 * A + J
    checks["P15_exact_projector_rank15"] = (
        np.array_equal(P15n @ P15n, 12 * P15n) and int(np.trace(P15n)) == 12 * 15
    )
    checks["P20_exact_projector_rank20"] = (
        np.array_equal(P20n @ P20n, 18 * P20n) and int(np.trace(P20n)) == 18 * 20
    )
    checks["projectors_orthogonal"] = np.count_nonzero(P15n @ P20n) == 0
    checks["projectors_resolve_identity"] = np.array_equal(3 * P15n + 2 * P20n + J, 36 * I)

    # C4=4(B-J/4), D3=3(N-J/3) keep every calculation integral.
    C4 = 4 * B - np.ones((40, 36), dtype=np.int64)
    D3 = 3 * N - np.ones((45, 36), dtype=np.int64)
    checks["visible_gram_is_18E15"] = np.array_equal(C4.T @ C4, 24 * P15n)
    checks["slice_gram_is_18E20"] = np.array_equal(D3.T @ D3, 9 * P20n)
    checks["visible_and_slice_rows_are_orthogonal"] = np.count_nonzero(C4 @ D3.T) == 0

    centered_slice_gram9 = D3.T @ D3
    slice_off = Counter(
        int(centered_slice_gram9[left, right] // 9)
        for left in range(36)
        for right in range(left + 1, 36)
    )
    checks["slice_frame_is_two_distance"] = slice_off == Counter({1: 360, -2: 270})

    # The one common row u=(1/sqrt(2))*1 completes 18(E20+E1), an ETF(36,21).
    # We verify its Gram without introducing floating point: twice the shadow
    # Gram is 2*(D^T D)+(J), with D=D3/3.
    shadow_gram_times18 = 2 * centered_slice_gram9 + 9 * J
    checks["slice_plus_common_is_naimark_shadow"] = np.array_equal(
        shadow_gram_times18,
        18 * P20n + 9 * J,
    )
    # This matrix is 18 times the actual shadow Gram, hence diagonal 189 and
    # off-diagonal +/-27 correspond to actual 21/2 and +/-3/2.
    checks["shadow_etf_angles_one_seventh"] = (
        set(map(int, np.diag(shadow_gram_times18))) == {189}
        and {
            int(shadow_gram_times18[i, j])
            for i in range(36)
            for j in range(i + 1, 36)
        }
        == {-27, 27}
    )

    # Fully integral hardware lowering.  Two identical common rows replace the
    # single sqrt(2) common row.  The resulting 87 x 36 matrix has orthogonal
    # columns and a scalar round trip.
    K = np.vstack(
        (
            3 * C4,
            4 * D3,
            6 * np.ones((2, 36), dtype=np.int64),
        )
    )
    KtK = K.T @ K
    checks["integer_transform_shape_87_by_36"] = K.shape == (87, 36)
    checks["integer_transform_exact_isometry"] = np.array_equal(KtK, 2592 * I)
    checks["integer_transform_coefficients_shift_add_only"] = set(map(int, np.unique(K))) == {-4, -3, 6, 8, 9}

    # NumPy comparisons produce numpy.bool_ values; freeze plain JSON booleans.
    checks = {name: bool(value) for name, value in checks.items()}
    status = "PASS" if all(checks.values()) else "FAIL"
    mapping_list = [mapping[index] for index in range(36)]
    coefficient_census = {str(int(k)): int(v) for k, v in zip(*np.unique(K, return_counts=True))}

    result: dict[str, Any] = {
        "schema": "w33.pass7307_7309.double_six_naimark_isometry.v1",
        "status": status,
        "passes": "7307-7309",
        "checks": checks,
        "objects": {
            "visible": "centered 40 W33-line x 36-spread incidence B-J/4",
            "shadow": "centered 45-tritangent x 36-double-six doily-slice incidence N-J/3",
            "alignment": "Pass4992 explicit spread/double-six scheme isomorphism",
            "double_six_to_spread_mapping": mapping_list,
            "B_sha256": canonical_matrix_hash(B),
            "N_aligned_sha256": canonical_matrix_hash(N),
            "B_row_masks_36bit_hex": mask_rows(B),
            "N_row_masks_36bit_hex": mask_rows(N),
        },
        "projector_resolution": {
            "carrier_dimension": 36,
            "split": "36 = 15 + 20 + 1",
            "E15": "(6I+2A-J)/12",
            "E20": "(9I-3A+J)/18",
            "E1": "J/36",
            "identity": "E15+E20+E1=I36",
            "visible_gram": "(B-J/4)^T(B-J/4)=18E15",
            "slice_gram": "(N-J/3)^T(N-J/3)=18E20",
            "cross_gram": "(B-J/4)(N-J/3)^T=0",
        },
        "naimark_completion": {
            "old_visible_frame": "ETF(36,15), normalized coherence 1/5",
            "new_geometric_shadow_sector": "36-vector two-distance 18-tight frame in dimension 20; inner products 1 and -2, norm 10",
            "common_mode": "append u=(1/sqrt(2))*1_36",
            "completed_shadow": "ETF(36,21), norm^2 21/2, off-diagonal +/-3/2, normalized coherence 1/7",
            "full_real_isometry": "T=[B-J/4; N-J/3; u], T^T T=18I36",
            "minimal_rank_statement": "The 45 tritangent lanes realize the rank-20 part of the old 21-dimensional guard; one scalar common mode completes it.",
        },
        "integer_hardware_transform": {
            "shape": [87, 36],
            "definition": "K=[3(4B-J40x36); 4(3N-J45x36); 6J2x36]",
            "identity": "K^T K=2592I36=(36sqrt(2))^2 I36",
            "coefficient_census": coefficient_census,
            "visible_row_lowering": "12*sum(selected 10 inputs)-3*sum(all 36 inputs)",
            "shadow_row_lowering": "12*sum(selected 12 inputs)-4*sum(all 36 inputs)",
            "common_row_lowering": "6*sum(all 36 inputs), repeated twice for integerization",
            "multiplier_boundary": "All constants are shift-add realizable; synthesis cost and timing require a separate RTL/Yosys certificate.",
        },
        "prior_art_boundary": {
            "already_owned": [
                "Pass3694: abstract ETF(36,15) and rank-21 Naimark complement",
                "Parseval target audit: abstract shared shadow split 21=1+20",
                "Pass4992: explicit spread/double-six association-scheme alignment",
                "Pass7241: literal N=J+M doily-slice incidence and col(N)=Cspread",
                "Pass7249-7304: centered N is already a rank-20 two-distance tight frame",
            ],
            "new_composition": (
                "The aligned B/N carriers have zero cross-Gram, resolve E15+E20+E1=I36, "
                "complete the rank-21 Naimark ETF with one common mode, and yield the exact integer K transform."
            ),
        },
        "physics_boundary": (
            "T/sqrt(18) is an exact finite real isometry, so standard unitary-dilation mathematics applies after row-space compression. "
            "No interferometer mesh, loss budget, phase-error tolerance, fabrication result, particle assignment, or continuum dynamics is proved here."
        ),
    }
    semantic = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    result["semantic_sha256"] = sha256(semantic.encode("ascii")).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    if args.check:
        frozen = json.loads(args.check.read_text(encoding="utf-8"))
        if frozen != result:
            raise SystemExit("frozen certificate mismatch")
        print(f"PASS frozen certificate {result['semantic_sha256']}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "semantic_sha256": result["semantic_sha256"]}, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
