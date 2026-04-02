from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from exploration._optional_deps import require_networkx
from exploration.w33_center_quad_transport_bridge import reconstructed_quotient_graph
from exploration.w33_dual_bose_mesner_bridge import (
    build_dual_bose_mesner_bridge_summary,
)
from exploration.w33_three_channel_operator_bridge import build_w33_adjacency

nx = require_networkx("tests/test_w33_dual_bose_mesner_bridge.py")


def test_w33_and_transport_have_same_nontrivial_eigenvalues() -> None:
    w33 = np.sort(np.linalg.eigvalsh(build_w33_adjacency().astype(float)))
    graph, _ = reconstructed_quotient_graph()
    transport = np.sort(np.linalg.eigvalsh(nx.to_numpy_array(graph, dtype=float)))

    assert np.isclose(w33[-1], 12.0)
    assert np.isclose(transport[-1], 32.0)
    assert np.allclose(w33[:-1][[0, -1]], [-4.0, 2.0], atol=1e-12)
    assert np.allclose(transport[:-1][[0, -1]], [-4.0, 2.0], atol=1e-12)
    assert np.sum(np.isclose(w33, 2.0)) == 24
    assert np.sum(np.isclose(transport, 2.0)) == 24
    assert np.sum(np.isclose(w33, -4.0)) == 15
    assert np.sum(np.isclose(transport, -4.0)) == 20


def test_same_projector_numerator_selects_constant_mode_in_both_graphs() -> None:
    w33 = build_w33_adjacency().astype(float)
    graph, _ = reconstructed_quotient_graph()
    transport = nx.to_numpy_array(graph, dtype=float)

    i_w = np.eye(w33.shape[0], dtype=float)
    i_t = np.eye(transport.shape[0], dtype=float)
    j_w = np.ones_like(w33)
    j_t = np.ones_like(transport)

    numerator_w = w33 @ w33 + 2.0 * w33 - 8.0 * i_w
    numerator_t = transport @ transport + 2.0 * transport - 8.0 * i_t

    assert np.allclose(numerator_w / 160.0, j_w / 40.0, atol=1e-12)
    assert np.allclose(numerator_t / 1080.0, j_t / 45.0, atol=1e-12)


def test_shared_mean_zero_formula_is_exact() -> None:
    summary = build_dual_bose_mesner_bridge_summary()
    shared = summary["shared_mean_zero_calculus"]

    assert shared["positive_channel_coefficients"] == {"alpha": "2/3", "beta": "1/6"}
    assert shared["negative_channel_coefficients"] == {"alpha": "1/3", "beta": "-1/6"}


def test_summary_flags_dual_bridge_correctly() -> None:
    summary = build_dual_bose_mesner_bridge_summary()

    assert summary["w33"]["constant_projector_matches_exactly"] is True
    assert summary["transport"]["constant_projector_matches_exactly"] is True
    assert summary["shared_nontrivial_polynomial"]["polynomial"] == "x^2 + 2x - 8"
    assert summary["shared_nontrivial_polynomial"]["kills_mean_zero_on_w33"] is True
    assert summary["shared_nontrivial_polynomial"]["kills_mean_zero_on_transport"] is True
