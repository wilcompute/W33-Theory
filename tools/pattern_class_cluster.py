#!/usr/bin/env python3
"""Cluster the 8 pattern classes by feature vectors (support sizes + neighbor profiles).

Outputs artifacts/pattern_class_clusters.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def kmeans(X, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    # init centers by sampling
    idx = rng.choice(len(X), size=k, replace=False)
    centers = X[idx].copy()

    for _ in range(iters):
        # assign
        dists = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        labels = np.argmin(dists, axis=1)
        new_centers = np.zeros_like(centers)
        for i in range(k):
            pts = X[labels == i]
            if len(pts) > 0:
                new_centers[i] = pts.mean(axis=0)
            else:
                new_centers[i] = centers[i]
        if np.allclose(new_centers, centers):
            break
        centers = new_centers
    return labels, centers


def main():
    table = json.loads((ROOT / "artifacts" / "pattern_class_feature_table.json").read_text())

    classes = sorted(int(k) for k in table["class_summary"].keys())

    # Build features: support size counts (1..4) + avg neighbor counts (8)
    X = []
    for c in classes:
        s = table["class_summary"][str(c)]
        support = s.get("support_size_counts", {})
        sup = np.array([support.get(str(i), support.get(i, 0)) for i in [1,2,3,4]], dtype=float)
        # normalize support by class size
        if s["size"] > 0:
            sup = sup / s["size"]
        nbr = np.array(s["avg_neighbor_class_counts"], dtype=float) / 12.0
        X.append(np.concatenate([sup, nbr]))
    X = np.vstack(X)

    results = {}
    for k in [2,3,4,5]:
        labels, centers = kmeans(X, k, iters=200, seed=0)
        clusters = {str(i): [int(classes[j]) for j in range(len(classes)) if labels[j] == i] for i in range(k)}
        results[str(k)] = clusters

    out = {
        "feature_dim": X.shape[1],
        "clusters": results,
        "classes": classes,
    }

    (ROOT / "artifacts" / "pattern_class_clusters.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/pattern_class_clusters.json")
    print(out["clusters"])


if __name__ == "__main__":
    main()
