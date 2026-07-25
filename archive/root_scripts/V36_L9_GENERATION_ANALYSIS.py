#!/usr/bin/env python3
"""
V36: L9 Generation Pattern Analysis

Samples l9 binary buckets to determine the 9-fold generation pattern.
Since l9 returns to g0, all 9 inputs should be g1, and the generation
pattern (how many of each gen 0,1,2 appear) determines the physical
interpretation of l9 in the L∞ tower.
"""

import json
import pathlib
import struct
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent
META = ROOT / 'extracted_v13' / 'W33-Theory-master' / 'artifacts' / 'e8_root_metadata_table.json'
SC   = ROOT / 'artifacts' / 'e8_structure_constants_w33_discrete.json'
BUCKET_DIR = ROOT / 'V30_output_v13_full' / 'l9_buckets'

REC_SIZE = 11
KEY_LEN = 9
TAIL_FMT = struct.Struct('<bB')  # out_idx (uint8), coeff (int8)
# Actually: out_idx is uint8 and coeff is int8
# Let me check V30 format more carefully

# ── Load metadata ────────────────────────────────────────────────────────────

meta = json.loads(META.read_text())
sc_data = json.loads(SC.read_text())
sc_roots = [tuple(r) for r in sc_data['basis']['roots']]
cartan_dim = sc_data['basis']['cartan_dim']

grade_by_orbit = {}
i27_by_orbit = {}
i3_by_orbit = {}
for row in meta['rows']:
    rt = tuple(row['root_orbit'])
    grade_by_orbit[rt] = row['grade']
    i27_by_orbit[rt] = row.get('i27')
    i3_by_orbit[rt] = row.get('i3')

# Build SC index → (grade, i27, i3) maps
idx_grade = {}
idx_i27 = {}
idx_i3 = {}
for i, rt in enumerate(sc_roots):
    sc_idx = cartan_dim + i
    g = grade_by_orbit.get(rt, '?')
    idx_grade[sc_idx] = g
    if g == 'g1':
        idx_i27[sc_idx] = i27_by_orbit.get(rt)
        idx_i3[sc_idx] = i3_by_orbit.get(rt)
for ci in range(cartan_dim):
    idx_grade[ci] = 'cartan'

print("=" * 70)
print("V36: L9 GENERATION PATTERN ANALYSIS")
print("=" * 70)

# ── Sample buckets ──────────────────────────────────────────────────────────

# Find available buckets
bucket_files = sorted(BUCKET_DIR.glob("bucket_*.bin"))
print(f"\nTotal bucket files: {len(bucket_files)}")

# Sample a subset to get statistically significant patterns
SAMPLE_BUCKETS = 50  # Sample 50 buckets
sample_files = bucket_files[:SAMPLE_BUCKETS]

gen_pattern_counts = Counter()  # generation tuple → count
grade_pattern_counts = Counter()  # grade tuple → count
total_records = 0
n_all_g1 = 0
n_not_all_g1 = 0

for bf in sample_files:
    with open(bf, 'rb') as f:
        data = f.read()

    n_rec = len(data) // REC_SIZE
    for i in range(n_rec):
        offset = i * REC_SIZE
        t9 = data[offset:offset + KEY_LEN]  # 9 basis indices
        # Don't need out_idx and coeff for generation analysis

        total_records += 1

        # Get grades and generations for all 9 inputs
        grades = tuple(sorted(idx_grade.get(x, '?') for x in t9))
        grade_pattern_counts[grades] += 1

        if all(idx_grade.get(x) == 'g1' for x in t9):
            n_all_g1 += 1
            # Get generation pattern
            gens = tuple(sorted(idx_i3.get(x, -1) for x in t9))
            gen_pattern_counts[gens] += 1
        else:
            n_not_all_g1 += 1

    if total_records >= 5_000_000:
        break

print(f"\nSampled {total_records:,} records from {len(sample_files)} buckets")

# ── Grade pattern analysis ──────────────────────────────────────────────────

print(f"\n── GRADE PATTERNS IN L9 ────────────────────────────────────────")
print(f"  All g1: {n_all_g1:,} ({100*n_all_g1/total_records:.1f}%)")
print(f"  Not all g1: {n_not_all_g1:,} ({100*n_not_all_g1/total_records:.1f}%)")

if n_not_all_g1 > 0:
    print(f"\n  Top non-g1 grade patterns:")
    for pat, cnt in grade_pattern_counts.most_common(20):
        if pat != tuple(sorted(['g1']*9)):
            pct = 100 * cnt / total_records
            print(f"    {pat}: {cnt:,} ({pct:.2f}%)")

# ── Generation pattern analysis ─────────────────────────────────────────────

if n_all_g1 > 0:
    print(f"\n── GENERATION PATTERNS (9 inputs, each gen 0/1/2) ────────────")
    print(f"  Total all-g1 records: {n_all_g1:,}\n")

    for pat, cnt in gen_pattern_counts.most_common(30):
        pct = 100 * cnt / n_all_g1
        # Count how many of each generation
        n0 = pat.count(0)
        n1 = pat.count(1)
        n2 = pat.count(2)
        print(f"    ({n0},{n1},{n2}): {cnt:,} ({pct:.2f}%)")

    # Summarize by (n0, n1, n2) partition
    print(f"\n  Summary by generation partition:")
    partition_counts = Counter()
    for pat, cnt in gen_pattern_counts.items():
        n0 = pat.count(0)
        n1 = pat.count(1)
        n2 = pat.count(2)
        partition_counts[(n0, n1, n2)] += cnt

    for part, cnt in sorted(partition_counts.items()):
        pct = 100 * cnt / n_all_g1
        print(f"    gen(0,1,2) = {part}: {cnt:,} ({pct:.2f}%)")

    # Check Z/3 constraint: sum of generations should be 0 mod 3
    # (since l9 → g0, total grade = 9 × 1 = 9 ≡ 0 mod 3)
    print(f"\n  Z/3 constraint: Σ gen_i mod 3 should relate to grade cycling")
    z3_counts = Counter()
    for pat, cnt in gen_pattern_counts.items():
        s = sum(pat) % 3
        z3_counts[s] += cnt
    for s, cnt in sorted(z3_counts.items()):
        pct = 100 * cnt / n_all_g1
        print(f"    Σgen mod 3 = {s}: {cnt:,} ({pct:.2f}%)")

print("\n" + "=" * 70)
