#!/usr/bin/env python3
"""Utilities to load and verify the explicit W33->E8 bijection artifact.

Provides small, dependency-free helpers used by unit tests.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

Artifact = Dict[str, object]


def load_explicit_bijection(artifact_path: Path | None = None) -> Artifact:
    """Load artifacts/explicit_bijection_decomposition.json.

    If `artifact_path` is None, the default artifact path is used.
    """
    if artifact_path is None:
        artifact_path = ROOT / "artifacts" / "explicit_bijection_decomposition.json"
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    return data


def verify_bijective_mapping(data: Artifact) -> Tuple[bool, str]:
    mapping = data["edge_to_root_index"]
    if len(mapping) != 240:
        return False, f"mapping length != 240: {len(mapping)}"
    vals = list(mapping.values())
    if len(set(vals)) != 240:
        return False, "root indices not unique"
    root_coords = data["root_coords"]
    max_idx = len(root_coords) - 1
    if any(r < 0 or r > max_idx for r in vals):
        return False, "root index out of range"
    return True, "ok"


def root_norms(data: Artifact) -> List[int]:
    """Return list of integer dot(r,r) for each root in artifact."""
    roots = data["root_coords"]
    norms = [sum(int(x) * int(x) for x in r) for r in roots]
    return norms


def dot_pair_classes(data: Artifact):
    """Recompute dot-pair classes using same u1,u2 and return counts per class."""
    roots = data["root_coords"]
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)
    classes = {}
    for i, r in enumerate(roots):
        d = (
            sum(int(r[j]) * u1[j] for j in range(8)),
            sum(int(r[j]) * u2[j] for j in range(8)),
        )
        classes.setdefault(d, []).append(i)
    counts = sorted([len(v) for v in classes.values()])
    return counts


def inner_product_values_for_mapped_edges(data: Artifact) -> List[int]:
    """Compute inner products (dot) between all distinct mapped roots and return set of values (as ints)."""
    roots = data["root_coords"]
    mapping = data["edge_to_root_index"]
    vals = list(mapping.values())
    ips = set()
    for i in range(len(vals)):
        ri = roots[vals[i]]
        for j in range(i + 1, len(vals)):
            rj = roots[vals[j]]
            ip = sum(int(ri[k]) * int(rj[k]) for k in range(8))
            ips.add(ip)
    return sorted(ips)


def mapping_class_counts(data: Artifact):
    """Return counts of edges mapped into root classes grouped by class size.

    Returns a dict mapping class size -> number of edges mapped to classes of that size.
    Also returns a detailed mapping: class_key -> count of edges mapped to that specific class.
    """
    # Recompute dot-pair classes to know which root indices belong to each class
    roots = data["root_coords"]
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)
    classes = {}
    for i, r in enumerate(roots):
        d = (
            sum(int(r[j]) * u1[j] for j in range(8)),
            sum(int(r[j]) * u2[j] for j in range(8)),
        )
        classes.setdefault(d, []).append(i)

    # Build reverse map root_idx -> class_key
    root_to_class = {ri: k for k, v in classes.items() for ri in v}

    # Count edges mapped into each class
    mapping = data["edge_to_root_index"]
    class_counts = {}
    for eidx, ridx in mapping.items():
        key = root_to_class[ridx]
        class_counts.setdefault(key, 0)
        class_counts[key] += 1

    # Aggregate by class size
    size_agg = {}
    for k, v in classes.items():
        sz = len(v)
        cnt = class_counts.get(k, 0)
        size_agg.setdefault(sz, 0)
        size_agg[sz] += cnt

    return size_agg, class_counts
