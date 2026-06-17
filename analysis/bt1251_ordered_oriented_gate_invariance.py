#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from itertools import permutations, product
from pathlib import Path

BASE_SPHERE = [1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1]
BASE_BALLS = {"B4": 534, "B8": 14994, "B12": 51803, "B14": 51840}


def build():
    ordered_variants = 24
    oriented_variants = 16
    total_label_variants = ordered_variants * oriented_variants
    return {
        "bt": 1251,
        "title": "Ordered and oriented gate invariance for symmetric Cayley tomography",
        "base_unordered_set": ["(0,0,0,2)", "(0,2,0,0)", "(0,0,2,2)", "(1,0,0,0)"],
        "ordered_variants": ordered_variants,
        "orientation_variants": oriented_variants,
        "total_labeled_oriented_variants": total_label_variants,
        "reason": "The BT1233 metric uses the symmetric alphabet {g_i, g_i^{-1}}. Permuting labels or replacing any g_i by g_i^{-1}=g_i^2 leaves the same unlabelled alphabet.",
        "sphere_histogram_invariant": True,
        "ball_checkpoints_invariant": True,
        "reference_sphere": BASE_SPHERE,
        "reference_balls": BASE_BALLS,
        "tomography_consequence": "Ordered/oriented labels can matter for pulse calibration and transcript semantics, but not for the unlabelled symmetric Cayley sphere/ball fingerprint. To distinguish orientations one must add labelled-word or directed-channel observables."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1251_ordered_oriented_gate_invariance_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1251, "variants": result["total_labeled_oriented_variants"], "invariant": result["sphere_histogram_invariant"], "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
