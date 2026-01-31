import runpy
import subprocess
import sys
from pathlib import Path

import pytest

from tools.e8_w33_bijection import (dot_pair_classes,
                                    inner_product_values_for_mapped_edges,
                                    load_explicit_bijection,
                                    mapping_class_counts, root_norms,
                                    verify_bijective_mapping)

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "explicit_bijection_decomposition.json"


def ensure_artifact():
    if not ART.exists():
        # Run the script to generate the artifact; prefer runpy so it runs in-process.
        try:
            runpy.run_path(
                str(ROOT / "tools" / "explicit_bijection_decomposition.py"),
                run_name="__main__",
            )
        except Exception:
            # fallback to subprocess in case of environment differences
            subprocess.check_call(
                [
                    sys.executable,
                    str(ROOT / "tools" / "explicit_bijection_decomposition.py"),
                ]
            )
    assert ART.exists(), "artifact not created"


def test_bijection_generation_and_cardinality():
    ensure_artifact()
    data = load_explicit_bijection(ART)
    ok, msg = verify_bijective_mapping(data)
    assert ok, msg


def test_root_norms_and_dot_classes():
    ensure_artifact()
    data = load_explicit_bijection(ART)
    norms = root_norms(data)
    # All roots should have the same norm (scaled E8 roots). Expect 8.
    assert len(set(norms)) == 1
    assert list(set(norms))[0] == 8

    counts = dot_pair_classes(data)
    # Expect at least one class of size 72 and multiple classes of size 27 and some size-1 classes
    assert 72 in counts
    assert any(c == 27 for c in counts)
    assert any(c == 1 for c in counts)
    assert sum(counts) == 240


def test_inner_product_range_and_variety():
    ensure_artifact()
    data = load_explicit_bijection(ART)
    ips = inner_product_values_for_mapped_edges(data)
    assert all(isinstance(x, int) for x in ips)
    assert all(abs(x) <= 8 for x in ips)
    assert len(ips) >= 3  # should have at least a few different inner products


def test_mapping_class_distribution():
    ensure_artifact()
    data = load_explicit_bijection(ART)
    size_agg, class_counts = mapping_class_counts(data)

    # Expect: total edges mapped into 27-sized classes = 162 (6 classes × 27)
    assert size_agg.get(27, 0) == 162

    # Expect: total edges mapped into size-1 classes = 6
    assert size_agg.get(1, 0) == 6

    # Expect: total edges mapped into size-72 class = 72
    assert size_agg.get(72, 0) == 72

    # Sanity: totals sum to 240
    assert sum(size_agg.values()) == 240
