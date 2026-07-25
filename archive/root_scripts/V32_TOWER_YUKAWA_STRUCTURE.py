#!/usr/bin/env python3
"""
V32 — L∞ Tower Yukawa Structure: l3 through l6
================================================

Analyzes the generational (i3) and within-generation (i27) structure
of the corrected L∞ tower at each level.

Key questions:
1. Does the 4:1 eigenvalue ratio (= μ from SRG) persist at higher levels?
2. How does the generation coupling pattern evolve? (l3 = inter-gen only)
3. What is the support structure within each generation?
4. Can we extract running Yukawa couplings from the tower?
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"


def load_grade_infrastructure():
    """Load E8 metadata and build SC-index → grade/generation maps."""
    meta_path = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
    sc_path = ARTIFACTS / "e8_structure_constants_w33_discrete.json"

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    sc = json.loads(sc_path.read_text(encoding="utf-8"))
    cartan_dim = sc["basis"]["cartan_dim"]
    sc_roots = [tuple(r) for r in sc["basis"]["roots"]]

    grade_by_orbit = {}
    i27_by_orbit = {}
    i3_by_orbit = {}
    for row in meta["rows"]:
        rt = tuple(row["root_orbit"])
        grade_by_orbit[rt] = row["grade"]
        i27_by_orbit[rt] = row.get("i27")
        i3_by_orbit[rt] = row.get("i3")

    # SC index → info
    idx_grade = {}
    idx_i27 = {}
    idx_i3 = {}
    for i, rt in enumerate(sc_roots):
        sc_idx = cartan_dim + i
        g = grade_by_orbit.get(rt, "?")
        idx_grade[sc_idx] = g
        if g == "g1":
            idx_i27[sc_idx] = i27_by_orbit.get(rt)
            idx_i3[sc_idx] = i3_by_orbit.get(rt)
    for ci in range(cartan_dim):
        idx_grade[ci] = "cartan"

    return cartan_dim, sc_roots, idx_grade, idx_i27, idx_i3


def analyze_level(name, jsonl_path, idx_grade, idx_i27, idx_i3, max_lines=0):
    """Analyze generational structure of one tower level."""
    print(f"\n{'=' * 72}")
    print(f"  {name}")
    print(f"{'=' * 72}")

    entries = []
    n = 0
    with open(jsonl_path) as f:
        for line in f:
            entries.append(json.loads(line))
            n += 1
            if max_lines and n >= max_lines:
                break

    print(f"  Entries loaded: {len(entries)}")
    if not entries:
        return

    # Determine input arity
    arity = len(entries[0]["in"])
    print(f"  Input arity: {arity}")

    # Output grade distribution
    out_grades = Counter()
    for e in entries:
        oi = e.get("out")
        if oi is not None:
            out_grades[idx_grade.get(oi, "?")] += 1
        else:
            # multi-term
            for t in e.get("terms", []):
                out_grades[idx_grade.get(t[0], "?")] += 1

    print(f"  Output grade distribution: {dict(sorted(out_grades.items()))}")

    # Input grade distribution (all inputs are g1)
    in_grade_check = Counter()
    for e in entries:
        for x in e["in"]:
            in_grade_check[idx_grade.get(x, "?")] += 1
    print(f"  Input grades: {dict(sorted(in_grade_check.items()))}")

    # Generation (i3) distribution of inputs
    gen_tuples = Counter()
    for e in entries:
        gens = tuple(sorted(idx_i3.get(x, -1) for x in e["in"]))
        gen_tuples[gens] += 1

    print(f"  Generation tuple distribution (sorted):")
    for gt, count in sorted(gen_tuples.items(), key=lambda x: -x[1]):
        print(f"    {gt}: {count}")

    # Coefficient distribution
    coeff_hist = Counter()
    for e in entries:
        if "coeff" in e:
            coeff_hist[e["coeff"]] += 1
        else:
            for t in e.get("terms", []):
                coeff_hist[t[1]] += 1
    print(f"  Coefficient distribution (top 10):")
    for c, cnt in coeff_hist.most_common(10):
        print(f"    {c}: {cnt}")

    # Max abs coeff
    max_c = max(abs(c) for c in coeff_hist.keys())
    print(f"  Max |coeff|: {max_c}")

    # For g1 outputs (l4, l7): analyze which generation gets mapped to which
    if all(idx_grade.get(e.get("out", -1)) == "g1" for e in entries if "out" in e):
        print(f"\n  Output generation (i3) distribution:")
        out_gen_counts = Counter()
        for e in entries:
            if "out" in e:
                out_gen_counts[idx_i3.get(e["out"], -1)] += 1
        print(f"    {dict(sorted(out_gen_counts.items()))}")

        # Input gen tuple → output gen
        gen_io = Counter()
        for e in entries:
            if "out" in e:
                in_gens = tuple(sorted(idx_i3.get(x, -1) for x in e["in"]))
                out_gen = idx_i3.get(e["out"], -1)
                gen_io[(in_gens, out_gen)] += 1
        print(f"  Input gen → Output gen (top 15):")
        for (ig, og), cnt in gen_io.most_common(15):
            print(f"    {ig} → {og}: {cnt}")

    return entries


def main():
    t0 = time.time()
    print("=" * 72)
    print("  V32 — L∞ TOWER YUKAWA STRUCTURE: l3 THROUGH l6")
    print("=" * 72)

    cartan_dim, sc_roots, idx_grade, idx_i27, idx_i3 = load_grade_infrastructure()

    files = {
        "l3 (triples → g0)": ROOT / "V24_output_v13_full" / "l3_patch_triples_full.jsonl",
        "l4 (quads → g1)": ROOT / "V24_output_v13_full" / "l4_patch_quads_full.jsonl",
        "l5 (quintuples → g2)": ROOT / "V24_output_v13_full" / "l5_patch_quintuples_full.jsonl",
        "l6 (sextuples → g0)": ROOT / "V24_output_v13_full" / "l6_patch_sextuples_full.jsonl",
    }

    for name, path in files.items():
        if path.exists():
            # For l5 and l6, limit to avoid excessive memory
            max_lines = 50000 if "l5" in name or "l6" in name else 0
            analyze_level(name, path, idx_grade, idx_i27, idx_i3, max_lines=max_lines)
        else:
            print(f"\n  MISSING: {path}")

    # ══════════════════════════════════════════════════════════════════════
    #  SPECIAL ANALYSIS: l4 GENERATION MIXING MATRIX
    # ══════════════════════════════════════════════════════════════════════
    print(f"\n{'=' * 72}")
    print(f"  SPECIAL: l4 GENERATION MIXING MATRIX")
    print(f"{'=' * 72}")

    l4_path = files["l4 (quads → g1)"]
    if l4_path.exists():
        l4_data = []
        with open(l4_path) as f:
            for line in f:
                l4_data.append(json.loads(line))

        # l4: g1^4 → g1. Build 3×3 generation mixing matrix
        # G[in_gen_profile → out_gen]
        gen_mixing = np.zeros((3, 3, 3, 3))  # in_gens (sorted) → out_gen
        gen_mixing_flat = Counter()

        for e in l4_data:
            in_gens = tuple(sorted(idx_i3.get(x, -1) for x in e["in"]))
            out_gen = idx_i3.get(e["out"], -1)
            if out_gen < 0 or any(g < 0 for g in in_gens):
                continue
            gen_mixing_flat[(in_gens, out_gen)] += abs(e["coeff"])

        print(f"  Generation mixing patterns:")
        for (ig, og), cnt in sorted(gen_mixing_flat.items(), key=lambda x: -x[1]):
            print(f"    {ig} → gen{og}: {cnt}")

        # Which generation combinations appear in l4?
        in_gen_combos = Counter()
        for e in l4_data:
            in_gens = tuple(sorted(idx_i3.get(x, -1) for x in e["in"]))
            in_gen_combos[in_gens] += 1
        print(f"\n  Input generation combinations in l4:")
        for g, cnt in sorted(in_gen_combos.items(), key=lambda x: -x[1]):
            print(f"    {g}: {cnt}")

    elapsed = time.time() - t0
    print(f"\n  Elapsed: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
