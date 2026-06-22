#!/usr/bin/env python3
"""BT1524: expand transported-gauge prototype to all 40 transvection generators."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

from w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import build_w33, transvection_permutations
from bt1373_s3_gauge_synchronization_improved_counterconnection import IMPROVED_GAUGE_LABELS, S3_PERMS

OUT = ROOT / "data" / "bt1524_all_transvection_gauge_expansion.json"
MD = ROOT / "analysis" / "BT1524_all_transvection_gauge_expansion.md"


def compose(p, q):
    return tuple(p[i] for i in q)


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
    point_gens = transvection_permutations(points, {p: i for i, p in enumerate(points)})
    line_gens = [induced_line_perm(g, lines, line_index) for g in point_gens]
    seed_triples = [(0, 1, (0, 1, 2)), (0, 2, (1, 0, 2)), (3, 7, (2, 1, 0)), (11, 19, (0, 2, 1)), (12, 28, (1, 2, 0)), (23, 39, (2, 0, 1))]
    records = []
    for gi, g in enumerate(line_gens):
        for left, right, rho in seed_triples:
            nl, nr = sorted((g[left], g[right]))
            L_label = IMPROVED_GAUGE_LABELS[nl]
            R_label = IMPROVED_GAUGE_LABELS[nr]
            nrho = residual_action(L_label, R_label, rho)
            records.append({
                "generator": gi,
                "input": [left, right, list(rho)],
                "image": [nl, nr, list(nrho)],
                "left_gauge_label": L_label,
                "right_gauge_label": R_label,
                "rho_key_index": S3_PERMS.index(nrho),
            })
    checks = {
        "line_count_40": len(lines) == 40,
        "transvection_generator_count_40": len(line_gens) == 40,
        "seed_triples_six": len(seed_triples) == 6,
        "transported_records_240": len(records) == 240,
        "all_images_valid_lines": all(0 <= r["image"][0] < 40 and 0 <= r["image"][1] < 40 and r["image"][0] != r["image"][1] for r in records),
        "all_residuals_valid_s3": all(tuple(r["image"][2]) in S3_PERMS for r in records),
        "all_six_residual_keys_reached": sorted({r["rho_key_index"] for r in records}) == list(range(6)),
        "uses_improved_gauge_labels": all(0 <= r["left_gauge_label"] < 6 and 0 <= r["right_gauge_label"] < 6 for r in records),
    }
    result = {
        "bt": 1524,
        "title": "All transvection transported-gauge expansion",
        "verified": all(checks.values()),
        "source_packets": {"bt1522": "data/bt1522_transported_gauge_prototype.json", "bt357": "analysis/w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers.py", "bt1515": "data/bt1515_gauge_cocycle_residual_action.json"},
        "generator_count": len(line_gens),
        "seed_triple_count": len(seed_triples),
        "transported_record_count": len(records),
        "rho_key_profile": {str(k): sum(1 for r in records if r["rho_key_index"] == k) for k in range(6)},
        "sample_records": records[:12],
        "interpretation": "The transported-gauge prototype now covers all 40 projective transvection generators. Across 240 transported seed records, image lines remain valid and all six S3 residual keys occur.",
        "honesty_boundary": "This is all-generator local expansion, not closure over the full 25,920-element projective symplectic group.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1524 All Transvection Gauge Expansion\n\nExpanded BT1522 from three generators to all forty projective transvection generators. Six decorated seed triples give 240 transported records; image lines stay valid and all six S3 residual keys occur. This is still not the full 25,920-element orbit theorem.\n", encoding="utf-8")
    print(json.dumps({"bt": 1524, "verified": result["verified"], "records": len(records)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
