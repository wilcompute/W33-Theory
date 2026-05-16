from __future__ import annotations

from scripts.reproduce_w33_core import (
    adjacency_spectrum,
    alpha_docs_variant,
    alpha_paper_variant,
    build_w33_adjacency,
    canonical_projective_points_f3_4,
    srg_lambda_mu,
)


def test_projective_point_count():
    assert len(canonical_projective_points_f3_4()) == 40


def test_w33_srg_parameters():
    _points, adj = build_w33_adjacency()
    assert int(adj.sum() // 2) == 240
    assert set(int(x) for x in adj.sum(axis=0)) == {12}
    assert srg_lambda_mu(adj) == (2, 4)


def test_w33_adjacency_spectrum():
    _points, adj = build_w33_adjacency()
    assert adjacency_spectrum(adj) == {12: 1, 2: 24, -4: 15}


def test_alpha_formula_drift_is_explicitly_tracked():
    docs_value = alpha_docs_variant()
    paper_value = alpha_paper_variant()

    assert abs(docs_value - 137.03600360036003) < 1e-12
    assert abs(paper_value - 137.0359991818368) < 1e-12
    assert docs_value != paper_value
    assert abs(docs_value - paper_value) > 1e-6
