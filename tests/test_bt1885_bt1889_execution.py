import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analysis"))

import bt1885_explicit_z40_representative_schema as bt1885  # noqa: E402
import bt1886_chain_A_over_2_operator_locator as bt1886  # noqa: E402
import bt1887_vertex_subset_embedding_test as bt1887  # noqa: E402
import bt1888_phase_action_sparse_z40 as bt1888  # noqa: E402


def test_bt1885_z40_schema():
    summary = bt1885.theorem_summary()
    assert summary["row_count"] == 8
    assert summary["checks"]["all_z40_vectors_length_40"]
    assert summary["checks"]["operator_validation_not_claimed"]


def test_bt1886_operator_locator():
    summary = bt1886.theorem_summary()
    assert summary["checks"]["w33_adjacency_candidate_recorded"]
    assert summary["checks"]["candidate_not_overclaimed_as_boundary"]


def test_bt1887_vertex_embedding():
    summary = bt1887.theorem_summary()
    assert summary["checks"]["all_sparse_forms_consistent"]
    assert summary["checks"]["boundary_operator_not_overclaimed"]


def test_bt1888_sparse_phase_action():
    summary = bt1888.theorem_summary()
    assert summary["checks"]["all_G40_contributions_preserved"]
    assert summary["checks"]["chain_boundary_operator_not_overclaimed"]
