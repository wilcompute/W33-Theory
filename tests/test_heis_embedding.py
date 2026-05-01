#!/usr/bin/env python3
"""Tests for Pillar 96: N embedding into matrix algebra."""

from __future__ import annotations

import json
from pathlib import Path

from THEORY_PART_CXCVI_HEISENBERG_EMBEDDING import build_embedding


def test_embedding_file_created():
    from THEORY_PART_CXCVI_HEISENBERG_EMBEDDING import main

    main()
    repo = Path(__file__).resolve().parent.parent
    assert (repo / "pillars" / "heis_embedding_summary.json").exists()


def test_embedding_properties():
    s = build_embedding()
    # 48 blocks
    assert s["T3_block_action_degree"] == 48
    # kernel order divides 192
    assert 192 % s["T3_block_kernel_order"] == 0
    # conjugacy classes partition 192 elements
    assert sum(s["T4_class_sizes"]) == 192
    # number of conjugacy classes > 0
    assert s["T4_num_conjugacy_classes"] > 0
    # involutions count
    assert s["T4_num_involutions"] > 0


def test_class_equation_sums():
    s = build_embedding()
    total = sum(k * v for k, v in s["T4_class_equation"].items())
    assert total == 192
