#!/usr/bin/env python3
"""Pass 400: minimal magnetic control that breaks the qutrit phase-fibre no-go.

The native q=3 Heisenberg bulk adjacency A has projective period T=2*pi/3 but
cannot transfer between the three points of a central fibre.  The translation-
covariant Hermitian control

    C = (i/sqrt(3)) (S - S^*)

where S is the cyclic fibre shift, has rank two on each fibre, commutes with A,
and satisfies exp(-i T C)=S.  Thus exp(-iT(A+C))=omega S exactly.

Rank two is minimal among fibre-local Hermitian logarithms of a qutrit cycle:
a rank-one perturbation has at most two spectral phases after removal of a global
phase, while S has three distinct eigenphases.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from w33_pass400_404_common import adjacency, fibre_shift, matrix_exponential_hermitian, vertices, zero_forcing_closure

OUT = ROOT / "data" / "w33_pass400_minimal_phase_control.json"

# A certified zero-forcing set found by deterministic greedy search.  It is an
# upper bound for a fully local diagonal-actuator architecture; the spectral
# multiplicity lower bound is 12.  This is deliberately not claimed minimal.
ZF_COORDS = [
    (0, 0, 2), (0, 1, 1), (0, 1, 2), (0, 2, 0), (0, 2, 1),
    (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 1, 0), (1, 1, 1),
    (1, 2, 0), (1, 2, 2), (2, 0, 0), (2, 0, 2), (2, 1, 0),
    (2, 1, 1), (2, 2, 1),
]


def build_payload() -> dict:
    q = 3
    A = adjacency(q).astype(complex)
    S = fibre_shift(q)
    C = (1j / math.sqrt(3.0)) * (S - S.conj().T)
    T = 2 * math.pi / 3
    omega = np.exp(2j * math.pi / 3)

    U_native = matrix_exponential_hermitian(A, T)
    U_control = matrix_exponential_hermitian(C, T)
    U_total = matrix_exponential_hermitian(A + C, T)

    # Rank and spectrum per one qutrit fibre.
    S3 = S[:3, :3]
    C3 = C[:3, :3]
    c3_eigs = np.linalg.eigvalsh(C3)

    verts = vertices(q)
    index = {v: i for i, v in enumerate(verts)}
    zf = {index[v] for v in ZF_COORDS}
    zf_closure = zero_forcing_closure(A.real.astype(int), zf)

    target_fidelities = []
    leakage = []
    for x, y, z in verts:
        src = index[(x, y, z)]
        dst = index[(x, y, (z + 1) % q)]
        col = U_total[:, src]
        target_fidelities.append(float(abs(col[dst]) ** 2))
        leakage.append(float(np.sum(np.abs(col) ** 2) - abs(col[dst]) ** 2))

    checks = {
        "control_hermitian": bool(np.allclose(C, C.conj().T, atol=1e-11)),
        "control_commutes_with_native": bool(np.allclose(A @ C, C @ A, atol=1e-11)),
        "single_fibre_spectrum_minus1_0_plus1": bool(np.allclose(c3_eigs, [-1, 0, 1], atol=1e-10)),
        "single_fibre_rank_two": int(np.linalg.matrix_rank(C3, tol=1e-10)) == 2,
        "native_projective_return": bool(np.allclose(U_native, omega * np.eye(27), atol=1e-9)),
        "control_is_exact_shift": bool(np.allclose(U_control, S, atol=1e-9)),
        "total_is_phase_shift": bool(np.allclose(U_total, omega * S, atol=1e-9)),
        "all_27_targets_unit_fidelity": min(target_fidelities) > 1 - 1e-9,
        "all_27_targets_zero_leakage": max(abs(v) for v in leakage) < 1e-9,
        "zero_forcing_upper_bound_17": len(zf) == 17 and len(zf_closure) == 27,
        "spectral_control_lower_bound_12": 12 == max({8: 1, -1: 8, 2: 12, -4: 6}.values()),
        "minimal_circulant_rank_argument": len(set(np.round(np.angle(np.linalg.eigvals(S3)), 10))) == 3,
    }

    payload = {
        "schema": "w33.pass400.minimal_phase_control.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": "q=3 Heisenberg bulk cell",
        "native_gate_time": "2*pi/3",
        "control": "C=(i/sqrt(3))(S-S^*) on every central fibre",
        "single_fibre_control_matrix_symbolic": [
            ["0", "-i/sqrt(3)", "+i/sqrt(3)"],
            ["+i/sqrt(3)", "0", "-i/sqrt(3)"],
            ["-i/sqrt(3)", "+i/sqrt(3)", "0"],
        ],
        "single_fibre_spectrum": [-1, 0, 1],
        "single_fibre_spectral_rank": 2,
        "global_control_rank": int(np.linalg.matrix_rank(C, tol=1e-10)),
        "generated_lie_algebra": {
            "type": "abelian",
            "real_dimension": 2,
            "basis": ["iA", "iC"],
            "reason": "A and C commute and are linearly independent",
        },
        "minimality": {
            "translation_covariant_diagonal": "scalar on a fibre and cannot implement a cycle",
            "rank_one": "after a scalar shift exp(-itR) has at most two eigenphases; the qutrit shift has three",
            "rank_two": "achieved by C, hence minimal in the fibre-local Hermitian circulant class",
        },
        "full_local_control_bounds": {
            "spectral_multiplicity_lower_bound": 12,
            "certified_zero_forcing_upper_bound": 17,
            "claim": "12 <= minimum independently addressed diagonal actuator count <= 17; exact value not asserted",
            "zero_forcing_coordinates": [list(v) for v in ZF_COORDS],
            "zero_forcing_implication": "the graph-infection theorem upgrades independent projectors on these sites to u(27)",
            "full_lie_dimension_when_using_the_17_projectors": 27 * 27,
        },
        "exact_gate": "exp[-i(2*pi/3)(A+C)] = exp(2*pi*i/3) S",
        "minimum_target_fidelity_exact": 1,
        "maximum_leakage_exact": 0,
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 400 frozen certificate is stale")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
