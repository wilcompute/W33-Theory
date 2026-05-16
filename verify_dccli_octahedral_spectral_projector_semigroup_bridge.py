#!/usr/bin/env python3
"""Part DCCLI: octahedral spectral-projector semigroup bridge.

Builds on DCCL by expressing the octahedral heat kernel in exact spectral
projector form.

For octahedral Laplacian L with spectrum {0,4,4,4,6,6}, define projectors
by Lagrange interpolation:

    P0 = (L-4I)(L-6I) / 24,
    P4 = L(6I-L) / 8,
    P6 = L(L-4I) / 12.

Then:
    P0 + P4 + P6 = I,
    Pk Pm = delta_km Pk,
    L = 4 P4 + 6 P6,
    exp(-tL) = P0 + e^{-4t} P4 + e^{-6t} P6.

This is the exact modal semigroup form of closure diffusion on octahedral
phase space.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccl_octahedral_laplacian_heat_kernel_bridge import build_bridge as build_dccl

OUT_PATH = ROOT / "data" / "dccli_octahedral_spectral_projector_semigroup_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    rank_p0: int
    rank_p4: int
    rank_p6: int
    spectral_gap: int
    all_identities_hold: bool


def as_matrix(a: list[list[float]]) -> np.ndarray:
    return np.array(a, dtype=float)


def to_list(a: np.ndarray, digits: int = 12) -> list[list[float]]:
    return np.round(a, decimals=digits).tolist()


def build_bridge() -> dict[str, Any]:
    dccl = build_dccl()
    L = as_matrix(dccl["graph_model"]["laplacian"])
    n = L.shape[0]
    I = np.eye(n)

    P0 = (L - 4 * I) @ (L - 6 * I) / 24.0
    P4 = L @ (6 * I - L) / 8.0
    P6 = L @ (L - 4 * I) / 12.0

    ranks = {
        "P0": int(round(np.trace(P0))),
        "P4": int(round(np.trace(P4))),
        "P6": int(round(np.trace(P6))),
    }

    sample_t = [0.0, 0.5, 1.0, 2.0]
    semigroup_samples = {}
    for t in sample_t:
        spectral = P0 + np.exp(-4 * t) * P4 + np.exp(-6 * t) * P6
        direct = as_matrix(dccl["sample_heat_kernels"][str(t)])
        semigroup_samples[str(t)] = {
            "spectral": spectral,
            "direct": direct,
        }

    identities = {
        "projectors_sum_to_identity": np.allclose(P0 + P4 + P6, I, atol=1e-12),
        "projectors_are_idempotent": (
            np.allclose(P0 @ P0, P0, atol=1e-12)
            and np.allclose(P4 @ P4, P4, atol=1e-12)
            and np.allclose(P6 @ P6, P6, atol=1e-12)
        ),
        "projectors_are_mutually_orthogonal": (
            np.allclose(P0 @ P4, 0, atol=1e-12)
            and np.allclose(P0 @ P6, 0, atol=1e-12)
            and np.allclose(P4 @ P6, 0, atol=1e-12)
        ),
        "projector_ranks_match_multiplicities": ranks == {"P0": 1, "P4": 3, "P6": 2},
        "laplacian_reconstruction_holds": np.allclose(4 * P4 + 6 * P6, L, atol=1e-12),
        "semigroup_spectral_formula_matches_direct_heat_kernel": all(
            np.allclose(item["spectral"], item["direct"], atol=1e-10)
            for item in semigroup_samples.values()
        ),
        "p0_is_uniform_mode_projector": np.allclose(P0, np.ones((n, n)) / n, atol=1e-12),
        "spectral_gap_is_4": dccl["summary"]["spectral_gap"] == 4,
    }

    summary = BridgeSummary(
        vertex_count=n,
        rank_p0=ranks["P0"],
        rank_p4=ranks["P4"],
        rank_p6=ranks["P6"],
        spectral_gap=4,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "projector_definition": {
            "P0": "(L-4I)(L-6I)/24",
            "P4": "L(6I-L)/8",
            "P6": "L(L-4I)/12",
            "heat_semigroup": "K_t = P0 + e^{-4t} P4 + e^{-6t} P6",
        },
        "projectors": {
            "P0": to_list(P0),
            "P4": to_list(P4),
            "P6": to_list(P6),
        },
        "sample_semigroup_checks": {
            t: {
                "spectral": to_list(item["spectral"]),
                "direct": to_list(item["direct"]),
            }
            for t, item in semigroup_samples.items()
        },
        "bridge_claim": {
            "exact_layer": (
                "The octahedral closure heat semigroup has exact modal form K_t=P0+e^{-4t}P4+e^{-6t}P6 with projector multiplicities 1,3,2 and exact Laplacian reconstruction L=4P4+6P6."
            ),
            "conditional_layer": (
                "Interpreting this finite projector semigroup as continuum harmonic mode decomposition requires a scaling limit."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
