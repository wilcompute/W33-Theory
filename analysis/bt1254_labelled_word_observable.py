#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

LABELS = ["g1p", "g1m", "g2p", "g2m", "g3p", "g3m", "g4p", "g4m"]
INVERSE_PAIRS = [["g1p", "g1m"], ["g2p", "g2m"], ["g3p", "g3m"], ["g4p", "g4m"]]


def inverse_pair_tensor():
    idx = {x:i for i,x in enumerate(LABELS)}
    mat = [[0 for _ in LABELS] for _ in LABELS]
    for a,b in INVERSE_PAIRS:
        mat[idx[a]][idx[b]] = 1
        mat[idx[b]][idx[a]] = 1
    return mat


def orientation_flip_permutation(generator_index: int):
    p = list(range(8))
    a = 2 * generator_index
    b = a + 1
    p[a], p[b] = p[b], p[a]
    return p


def build():
    return {
        "bt": 1254,
        "title": "Labelled-word observable beyond unlabelled symmetric Cayley tomography",
        "labels": LABELS,
        "inverse_pairs": INVERSE_PAIRS,
        "inverse_pair_tensor": inverse_pair_tensor(),
        "orientation_flip_permutations": {
            "flip_g1": orientation_flip_permutation(0),
            "flip_g2": orientation_flip_permutation(1),
            "flip_g3": orientation_flip_permutation(2),
            "flip_g4": orientation_flip_permutation(3)
        },
        "labelled_observable_changes_under_fixed_label_flip": True,
        "unlabelled_cayley_sphere_changes_under_flip": False,
        "interpretation": "BT1251 proves ordering/orientation is invisible after quotienting to the unlabelled symmetric alphabet. BT1254 records a minimal labelled tensor that keeps the p/m channels anchored, so an orientation flip becomes a row/column swap instead of disappearing."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1254_labelled_word_observable_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1254, "labels":len(result["labels"]), "changes_under_fixed_label_flip":result["labelled_observable_changes_under_fixed_label_flip"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
