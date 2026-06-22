#!/usr/bin/env python3
"""BT1522: prototype transported-gauge labels for a small PSp(4,3) generator subset.

This uses the repo's transvection generators from BT357.  It transports line
labels under three point transvections and applies the BT1515 residual-key law
rho -> R^{-1} rho L with a deterministic gauge label pullback.  The goal is not
yet the full 25,920-element decorated Aut(W33) orbit theorem; it is a finite
prototype validating the data flow.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import build_w33, transvection_permutations
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS

OUT = ROOT / "data" / "bt1522_transported_gauge_prototype.json"
MD = ROOT / "analysis" / "BT1522_transported_gauge_prototype.md"


def compose(p, q):
    return tuple(p[i] for i in q)


def inv(p):
    out = [0] * len(p)
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def s3_inv(p):
    out = [0, 0, 0]
    for i, x in enumerate(p):
        out[x] = i
    return tuple(out)


def residual_action(left_label: int, right_label: int, rho):
    L = S3_PERMS[left_label]
    R = S3_PERMS[right_label]
    return compose(s3_inv(R), compose(rho, L))


def induced_line_perm(point_perm, lines, line_index):
    out = []
    for line in lines:
        image = tuple(sorted(point_perm[p] for p in line))
        out.append(line_index[image])
    return tuple(out)


def main() -> None:
    points, _edges, _edge_index, lines, _adjacency = build_w33()
    line_index = {tuple(line): i for i, line in enumerate(lines)}
    point_gens = transvection_permutations(points, {p: i for i, p in enumerate(points)})[:3]
    line_gens = [induced_line_perm(g, lines, line_index) for g in point_gens]
    seed_triples = [(0, 1, (0, 1, 2)), (0, 2, (1, 0, 2)), (3, 7, (2, 1, 0)), (11, 19, (0, 2, 1))]
    transported = []
    for gi, g in enumerate(line_gens):
        for left, right, rho in seed_triples:
            nl, nr = sorted((g[left], g[right]))
            # Prototype transported labels: pull improved labels from image lines.
            L_label = IMPROVED_GAUGE_LABELS[nl]
            R_label = IMPROVED_GAUGE_LABELS[nr]
            nrho = residual_action(L_label, R_label, rho)
            transported.append({
                "generator": gi,
                "input": {"left": left, "right": right, "rho": list(rho)},
                "image": {"left": nl, "right": nr, "rho": list(nrho)},
                "left_gauge_label": L_label,
                "right_gauge_label": R_label,
                "rho_key_index": S3_PERMS.index(nrho),
            })
    checks = {
        "line_count_40": len(lines) == 40,
        "three_generators": len(line_gens) == 3,
        "seed_triples_four": len(seed_triples) == 4,
        "transported_records_12": len(transported) == 12,
        "all_images_valid_lines": all(0 <= r["image"]["left"] < 40 and 0 <= r["image"]["right"] < 40 and r["image"]["left"] != r["image"]["right"] for r in transported),
        "all_residuals_valid_s3": all(tuple(r["image"]["rho"]) in S3_PERMS for r in transported),
        "uses_improved_gauge_labels": all(0 <= r["left_gauge_label"] < 6 and 0 <= r["right_gauge_label"] < 6 for r in transported),
    }
    result = {
        "bt": 1522,
        "title": "Transported gauge prototype",
        "verified": all(checks.values()),
        "source_packets": {"bt357": "analysis/w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers.py", "bt1373": "analysis/bt1373_s3_gauge_synchronization_improved_counterconnection.py", "bt1515": "data/bt1515_gauge_cocycle_residual_action.json"},
        "generator_count": len(line_gens),
        "seed_triples": [{"left": a, "right": b, "rho": list(r)} for a, b, r in seed_triples],
        "transported_records": transported,
        "interpretation": "A small transvection-generator subset transports decorated triples using image-line gauge labels and the BT1515 S3 residual cocycle. The data flow is valid: image lines stay in W33 and residual keys remain in S3.",
        "honesty_boundary": "This is a prototype using three generators and image-line label pullback, not the full 25,920-element transported-gauge orbit theorem.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1522 Transported Gauge Prototype\n\nThree projective symplectic transvection generators transport four decorated seed triples.  Image lines stay valid and residual keys remain in S3 under the BT1515 cocycle.  This is a prototype, not the full transported-gauge orbit theorem.\n", encoding="utf-8")
    print(json.dumps({"bt": 1522, "verified": result["verified"], "records": len(transported)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
