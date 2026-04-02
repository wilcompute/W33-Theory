"""Exact dual Bose-Mesner bridge between W33 and the 45-point transport graph.

The recent hard-computation phases gave an exact three-channel calculus on the
W(3,3) adjacency matrix A: every spectral kernel f(A) lies in span{I, A, J}.

The transport selector program gave an exact SRG(45,32,22,24) quotient graph T
with its own rank-3 Bose-Mesner algebra and selector identity
    (T^2 + 2T - 8I) / 1080 = J / 45.

The key exact bridge is that A and T have the same two nontrivial eigenvalues:
    W33:       {12, 2, -4}
    transport: {32, 2, -4}

So they share the same nontrivial spectral polynomial x^2 + 2x - 8. The
constant mode differs, but the mean-zero spectral calculus is identical.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
else:
    ROOT = Path(__file__).resolve().parents[1]

for candidate in (ROOT, ROOT / "exploration", ROOT / "pillars"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from exploration._optional_deps import require_networkx
from exploration.w33_three_channel_operator_bridge import build_w33_adjacency
from exploration.w33_center_quad_transport_bridge import reconstructed_quotient_graph


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_dual_bose_mesner_bridge_summary.json"
nx = require_networkx("exploration/w33_dual_bose_mesner_bridge.py")


def _fraction_text(value: Fraction) -> str:
    return str(value)


def _shared_mean_zero_coefficients(
    value_at_2: Fraction | int,
    value_at_minus_4: Fraction | int,
) -> tuple[Fraction, Fraction]:
    u = Fraction(value_at_2)
    v = Fraction(value_at_minus_4)
    alpha = (2 * u + v) / 3
    beta = (u - v) / 6
    return alpha, beta


def _transport_adjacency() -> np.ndarray:
    graph, _ = reconstructed_quotient_graph()
    nodes = sorted(graph)
    return nx.to_numpy_array(graph, nodelist=nodes, dtype=int)


def _constant_projector(matrix: np.ndarray) -> np.ndarray:
    n = matrix.shape[0]
    return np.ones((n, n), dtype=float) / n


@lru_cache(maxsize=1)
def build_dual_bose_mesner_bridge_summary() -> dict[str, Any]:
    w33 = build_w33_adjacency().astype(float)
    transport = _transport_adjacency().astype(float)

    n_w = w33.shape[0]
    n_t = transport.shape[0]
    i_w = np.eye(n_w, dtype=float)
    i_t = np.eye(n_t, dtype=float)
    j_w = np.ones((n_w, n_w), dtype=float)
    j_t = np.ones((n_t, n_t), dtype=float)

    numerator_w = w33 @ w33 + 2.0 * w33 - 8.0 * i_w
    numerator_t = transport @ transport + 2.0 * transport - 8.0 * i_t

    shared_positive = _shared_mean_zero_coefficients(1, 0)
    shared_negative = _shared_mean_zero_coefficients(0, 1)

    q_w = i_w - j_w / n_w
    q_t = i_t - j_t / n_t

    return {
        "status": "ok",
        "w33": {
            "vertices": n_w,
            "spectrum": {"12": 1, "2": 24, "-4": 15},
            "constant_projector_formula": "(A^2 + 2A - 8I) / 160 = J / 40",
            "constant_projector_matches_exactly": bool(
                np.allclose(numerator_w / 160.0, _constant_projector(w33), atol=1e-12)
            ),
        },
        "transport": {
            "vertices": n_t,
            "spectrum": {"32": 1, "2": 24, "-4": 20},
            "constant_projector_formula": "(T^2 + 2T - 8I) / 1080 = J / 45",
            "constant_projector_matches_exactly": bool(
                np.allclose(numerator_t / 1080.0, _constant_projector(transport), atol=1e-12)
            ),
        },
        "shared_nontrivial_polynomial": {
            "polynomial": "x^2 + 2x - 8",
            "kills_mean_zero_on_w33": bool(
                np.allclose(numerator_w @ q_w, np.zeros_like(w33), atol=1e-12)
            ),
            "kills_mean_zero_on_transport": bool(
                np.allclose(numerator_t @ q_t, np.zeros_like(transport), atol=1e-12)
            ),
        },
        "shared_mean_zero_calculus": {
            "formula": {
                "alpha": "(2 f(2) + f(-4)) / 3",
                "beta": "(f(2) - f(-4)) / 6",
                "meaning": "On the mean-zero subspace, f(M) = alpha I + beta M for both M = A and M = T.",
            },
            "positive_channel_coefficients": {
                "alpha": _fraction_text(shared_positive[0]),
                "beta": _fraction_text(shared_positive[1]),
            },
            "negative_channel_coefficients": {
                "alpha": _fraction_text(shared_negative[0]),
                "beta": _fraction_text(shared_negative[1]),
            },
        },
        "bridge_verdict": (
            "W33 and the 45-point transport quotient have different constant modes "
            "but the same nontrivial spectrum {2,-4}. So the new hard-computation "
            "three-channel calculus and the transport-selector calculus are the same "
            "exact mean-zero Bose-Mesner package. The polynomial x^2 + 2x - 8 "
            "annihilates the mean-zero sector of both graphs and produces the "
            "constant projector after one scale change, which is why the operator, "
            "selector, and transport bridges keep reproducing the same rational data."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_dual_bose_mesner_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    write_summary()
