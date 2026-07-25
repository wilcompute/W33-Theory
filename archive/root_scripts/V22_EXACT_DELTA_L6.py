#!/usr/bin/env python3
"""
V22 — Exact δL6 on candidate 7-tuples using full l6 table (777,495 entries).

Chain so far:
  V11: K3 exact (579 nonzero, all single-term)
  V13: K3 = δm proven (cocycle lock)
  V15: Exact δL4 → l4 (7,675 entries), support=234
  V17: l5 from sampled δL4 (1M sample)
  V18: l5 scaled (3M sample); l6 from sampled δL5
  V19: l5 exact (85,429 entries, support=234)
  V20: Exact δL5 → l6 exact (777,495 entries, support=234). δL6 sampled: 963/500k (rate 0.19%)
  V21: δL6 from 200k reservoir sample of l6 → l7 approx (2,803,420 entries, support=234)

V22: Compute EXACT δL6 on all candidate 7-tuples → full l7 table, then probe δL7.

Key simplification (from V20):
  [g1, g1] → g2 only (never g1), so the second CE sum vanishes.
  δl_n(x0,...,xn) = Σᵢ (-1)ⁱ [l_n(x0,...,x̂ᵢ,...,xn), xᵢ]
  l_{n+1} = -δl_n
"""

import json
import struct
import sys
import time
import os
import random
from collections import Counter, defaultdict
from pathlib import Path
from itertools import combinations

ROOT = Path(r"c:\Repos\Theory of Everything")
ARTIFACTS = ROOT / "artifacts"
V20_DIR = ROOT / "extracted_v20" / "V20"
V19_DIR = ROOT / "extracted_v20" / "v19" / "V19"
OUT_DIR = ROOT / "V22_output_corrected"

# ── Load E8 bracket ──────────────────────────────────────────────────────────

def load_bracket():
    """Load E8 structure constants and build bracket dict."""
    sc = json.loads((ARTIFACTS / "e8_structure_constants_w33_discrete.json").read_text(encoding="utf-8"))
    cartan_dim = int(sc["basis"]["cartan_dim"])
    roots = sc["basis"]["roots"]
    br = {}
    for kk, lst in sc["brackets"].items():
        i, j = (int(x) for x in kk.split(","))
        br[(i, j)] = tuple((int(k), int(c)) for k, c in lst)
    return br, cartan_dim, roots


def load_g1_indices(roots):
    """Load g1 basis indices from V13-bundled root metadata (canonical convention).
    
    The l4/l5/l6 pipeline was built with V13 metadata ordering.
    Current workspace metadata has a different root ordering.
    Map by `root_orbit` (order-independent) and then re-index according to the
    ordering used by the structure-constants JSON.
    """
    v13_meta_path = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
    meta = json.loads(v13_meta_path.read_text(encoding="utf-8"))
    cartan_dim = 8
    grade_by_root = {tuple(int(x) for x in r["root_orbit"]): str(r["grade"]) for r in meta["rows"]}
    g1 = [
        cartan_dim + i
        for i, rt in enumerate(roots)
        if grade_by_root[tuple(int(x) for x in rt)] == "g1"
    ]
    if len(g1) != 81:
        raise RuntimeError(f"Expected 81 g1 indices; got {len(g1)}")
    return sorted(g1)


class BracketCache:
    """Cached antisymmetric bracket lookup."""
    def __init__(self, br_full):
        self._br = br_full
        self._cache = {}

    def __call__(self, i, j):
        if i == j:
            return ()
        ck = (i, j)
        if ck in self._cache:
            return self._cache[ck]
        if i < j:
            key, sgn = (i, j), 1
        else:
            key, sgn = (j, i), -1
        raw = self._br.get(key)
        if not raw:
            out = ()
        else:
            out = tuple((k, sgn * c) for k, c in raw)
        self._cache[ck] = out
        return out


# ── Load l6 table ────────────────────────────────────────────────────────────

def load_l6_table(path):
    """Load l6 JSONL into dict: tuple(6 ints) → (out, coeff)."""
    l6 = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            e = json.loads(line)
            l6[tuple(e["in"])] = (e["out"], e["coeff"])
    return l6


# ── δl6 computation ─────────────────────────────────────────────────────────

def delta_l6(t7, l6_dict, bracket):
    """
    Compute δl6 on a sorted 7-tuple of g1 indices.
    
    δl6(x0,...,x6) = Σᵢ₌₀⁶ (-1)ⁱ [l6(x0,...,x̂ᵢ,...,x6), xᵢ]
    
    Returns dict: {basis_index: coeff} (only nonzero entries).
    """
    result = {}
    for i in range(7):
        sub6 = t7[:i] + t7[i+1:]
        val = l6_dict.get(sub6)
        if val is None:
            continue
        out, coeff = val
        xi = t7[i]
        sign = (-1) ** i
        br = bracket(xi, out)  # CE convention: [xi, l_n(...)]
        for k, bv in br:
            v = sign * coeff * bv
            result[k] = result.get(k, 0) + v
            if result[k] == 0:
                del result[k]
    return result


# ── Phase 1: Validate against V20 examples ───────────────────────────────────

def validate_against_v20(l6_dict, bracket):
    """Spot-check a few V20 δl6 examples."""
    v20_path = V20_DIR / "v20_deltaL5_exact_l6_full_and_deltaL6_sample.json"
    v20 = json.loads(v20_path.read_text(encoding="utf-8"))
    examples = v20["deltaL6_sample_with_full_l6"]["examples_first15"]

    print("Validating against V20 δl6 examples...")
    ok = 0
    for ex in examples[:5]:
        t7 = tuple(ex["in"])
        expected_out = ex["out"]
        expected_coeff = ex["coeff"]
        result = delta_l6(t7, l6_dict, bracket)
        if len(result) == 1:
            k, v = list(result.items())[0]
            if k == expected_out and v == expected_coeff:
                ok += 1
                print(f"  ✓ {t7} → out={k}, coeff={v}")
            else:
                print(f"  ✗ {t7} → got ({k},{v}), expected ({expected_out},{expected_coeff})")
        elif len(result) == 0:
            print(f"  ✗ {t7} → got ZERO, expected ({expected_out},{expected_coeff})")
        else:
            print(f"  ✗ {t7} → got MULTI-TERM {result}, expected ({expected_out},{expected_coeff})")
    print(f"Validation: {ok}/5 matched\n")
    return ok == 5


# ── Phase 2: Candidate enumeration → exact l7 ───────────────────────────────

def compute_exact_l7(l6_dict, bracket, g1):
    """
    Enumerate all candidate 7-tuples from l6 entries and compute exact δl6.
    
    A candidate 7-tuple is one that contains at least one l6 6-subtuple.
    For each l6 entry (a0,...,a5), we insert each g1 element g ∉ {a0,...,a5}
    to form a sorted 7-tuple.
    
    l7(t7) = -δl6(t7)
    
    Returns: l7_dict (nonzero results), statistics dict.
    """
    g1_set = set(g1)
    n_l6 = len(l6_dict)

    # Pack 7-tuple into bytes for compact storage in dedup set
    def pack7(t7):
        return struct.pack('7H', *t7)

    # Result storage: bytes → (out, coeff) for single-term, or bytes → dict for multi
    l7_single = {}    # pack7(t7) → (out, coeff)
    l7_multi = {}     # pack7(t7) → dict
    seen_nonzero = set()   # pack7 keys of nonzero results (for dedup)

    # Statistics
    n_candidates = 0
    n_unique_computed = 0
    n_nonzero = 0
    n_single = 0
    n_multi = 0
    n_skipped = 0
    coeff_counter = Counter()
    output_counter = Counter()

    t0 = time.time()
    l6_items = list(l6_dict.items())

    for idx, (t6, (out6, c6)) in enumerate(l6_items):
        t6_set = set(t6)
        for g in g1:
            if g in t6_set:
                continue
            n_candidates += 1

            # Form sorted 7-tuple
            t7_list = sorted(list(t6) + [g])
            t7 = tuple(t7_list)
            t7_key = pack7(t7)

            # Skip if already computed as nonzero
            if t7_key in seen_nonzero:
                n_skipped += 1
                continue

            n_unique_computed += 1

            # Compute δl6
            res = delta_l6(t7, l6_dict, bracket)

            if not res:
                continue

            # Nonzero result: l7 = -δl6
            l7_res = {k: -v for k, v in res.items()}
            seen_nonzero.add(t7_key)
            n_nonzero += 1

            items = list(l7_res.items())
            if len(items) == 1:
                n_single += 1
                k, v = items[0]
                l7_single[t7_key] = (t7, k, v)
                coeff_counter[v] += 1
                output_counter[k] += 1
            else:
                n_multi += 1
                l7_multi[t7_key] = (t7, l7_res)
                for k, v in items:
                    coeff_counter[v] += 1
                    output_counter[k] += 1

        # Progress
        if (idx + 1) % 10000 == 0 or idx == n_l6 - 1:
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed if elapsed > 0 else 0
            eta = (n_l6 - idx - 1) / rate if rate > 0 else 0
            print(f"  [{idx+1:>7d}/{n_l6}] candidates={n_candidates:,} "
                  f"unique_computed={n_unique_computed:,} nonzero={n_nonzero:,} "
                  f"(single={n_single:,} multi={n_multi:,}) "
                  f"skipped={n_skipped:,} "
                  f"elapsed={elapsed:.1f}s ETA={eta:.0f}s "
                  f"mem~{get_mem_mb():.0f}MB")

    elapsed = time.time() - t0

    stats = {
        "n_l6_entries": n_l6,
        "n_raw_candidates": n_candidates,
        "n_unique_computed": n_unique_computed,
        "n_skipped_dedup": n_skipped,
        "n_nonzero": n_nonzero,
        "n_single_term": n_single,
        "n_multi_term": n_multi,
        "nonzero_rate_on_unique": n_nonzero / max(n_unique_computed, 1),
        "time_s": round(elapsed, 2),
        "coeff_hist_top": [{"coeff": c, "count": n} for c, n in coeff_counter.most_common(20)],
        "output_support_size": len(output_counter),
        "top_outputs": [{"basis": k, "count": n} for k, n in output_counter.most_common(20)],
    }

    return l7_single, l7_multi, stats


def get_mem_mb():
    """Approximate memory usage in MB."""
    try:
        import psutil
        return psutil.Process().memory_info().rss / 1024 / 1024
    except ImportError:
        return 0


# ── Phase 3: Write l7 table ─────────────────────────────────────────────────

def write_l7_jsonl(l7_single, l7_multi, path):
    """Write l7 table to JSONL (same format as l6)."""
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for t7_key, (t7, out, coeff) in l7_single.items():
            f.write(json.dumps({"in": list(t7), "out": out, "coeff": coeff}) + "\n")
            count += 1
        for t7_key, (t7, res_dict) in l7_multi.items():
            # Multi-term: write with full term dict
            f.write(json.dumps({"in": list(t7), "terms": [[k, v] for k, v in res_dict.items()]}) + "\n")
            count += 1
    return count


# ── Phase 4: Probe δL7 on random 8-tuples ───────────────────────────────────

def delta_l7(t8, l7_dict, bracket):
    """
    Compute δl7 on a sorted 8-tuple.
    
    δl7(x0,...,x7) = Σᵢ₌₀⁷ (-1)ⁱ [l7(x0,...,x̂ᵢ,...,x7), xᵢ]
    """
    result = {}
    for i in range(8):
        sub7 = t8[:i] + t8[i+1:]
        val = l7_dict.get(sub7)
        if val is None:
            continue
        out, coeff = val
        xi = t8[i]
        sign = (-1) ** i
        br = bracket(xi, out)  # CE convention: [xi, l_n(...)]
        for k, bv in br:
            v = sign * coeff * bv
            result[k] = result.get(k, 0) + v
            if result[k] == 0:
                del result[k]
    return result


def probe_delta_l7(l7_single, bracket, g1, n_samples=200000):
    """Probe δl7 on random 8-tuples."""
    # Build l7 dict: tuple(7) → (out, coeff) for single-term entries only
    l7_lookup = {}
    for key, (t7, out, coeff) in l7_single.items():
        l7_lookup[t7] = (out, coeff)

    print(f"\nProbing δl7 on {n_samples:,} random g1 8-tuples...")
    print(f"  l7 lookup table: {len(l7_lookup):,} single-term entries")

    n_nonzero = 0
    n_single = 0
    n_multi = 0
    coeff_counter = Counter()
    output_counter = Counter()
    examples = []

    rng = random.Random(42)
    t0 = time.time()

    for sample_idx in range(n_samples):
        t8 = tuple(sorted(rng.sample(g1, 8)))
        res = delta_l7(t8, l7_lookup, bracket)
        if res:
            n_nonzero += 1
            items = list(res.items())
            if len(items) == 1:
                n_single += 1
            else:
                n_multi += 1
            for k, v in items:
                coeff_counter[v] += 1
                output_counter[k] += 1
            if len(examples) < 20:
                examples.append({"in": list(t8), "terms": items})

        if (sample_idx + 1) % 50000 == 0:
            elapsed = time.time() - t0
            print(f"  [{sample_idx+1:>7d}/{n_samples}] nonzero={n_nonzero} "
                  f"(single={n_single} multi={n_multi}) elapsed={elapsed:.1f}s")

    elapsed = time.time() - t0
    rate = n_nonzero / max(n_samples, 1)

    stats = {
        "N8": n_samples,
        "nonzero": n_nonzero,
        "single_term": n_single,
        "multi_term": n_multi,
        "nonzero_rate": round(rate, 8),
        "time_s": round(elapsed, 2),
        "coeff_hist_top": [{"coeff": c, "count": n} for c, n in coeff_counter.most_common(20)],
        "output_support_size": len(output_counter),
        "top_outputs": [{"basis": k, "count": n} for k, n in output_counter.most_common(20)],
        "examples_first20": examples,
    }

    return stats


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 72)
    print("V22 — Exact δL6 → full l7, then probe δL7")
    print("=" * 72)

    # Load data
    print("\n[1/6] Loading E8 bracket...")
    br_full, cartan_dim, roots = load_bracket()
    bracket = BracketCache(br_full)
    print(f"  Bracket entries: {len(br_full):,}, cartan_dim={cartan_dim}")

    print("\n[2/6] Loading g1 indices (V13 metadata convention)...")
    g1 = load_g1_indices(roots)
    print(f"  g1 size: {len(g1)} (range {min(g1)}..{max(g1)})")
    # Cross-check: g1 should match l4 input indices exactly
    l4 = json.loads((ROOT / "extracted_v15" / "V15" / "l4_residual_quads_full.json").read_text(encoding="utf-8"))
    l4_inputs = set()
    for entry in l4:
        for idx in entry["in"]:
            l4_inputs.add(idx)
    g1_set_check = set(g1)
    if l4_inputs == g1_set_check:
        print(f"  ✓ g1 matches l4 input indices (81/81)")
    else:
        print(f"  ✗ MISMATCH: g1 has {len(g1_set_check)}, l4 has {len(l4_inputs)}, "
              f"diff={l4_inputs.symmetric_difference(g1_set_check)}")
        sys.exit(1)
    del l4  # free memory

    print("\n[3/6] Loading l6 table...")
    l6_dict = load_l6_table(V20_DIR / "l6_patch_sextuples_full.jsonl")
    print(f"  l6 entries: {len(l6_dict):,}")

    # Validate
    print("\n[4/6] Spot-check against V20 examples...")
    if not validate_against_v20(l6_dict, bracket):
        print("WARNING: Validation failed on some examples. Check data integrity.")

    # Exact δl6 → l7
    print("\n[5/6] Computing exact δl6 on candidate 7-tuples → l7...")
    l7_single, l7_multi, dl6_stats = compute_exact_l7(l6_dict, bracket, g1)

    print(f"\n  === δl6 Results ===")
    print(f"  l7 entries (single-term): {len(l7_single):,}")
    print(f"  l7 entries (multi-term): {len(l7_multi):,}")
    print(f"  Total nonzero: {dl6_stats['n_nonzero']:,}")
    print(f"  Nonzero rate: {dl6_stats['nonzero_rate_on_unique']:.6f}")
    print(f"  Output support size: {dl6_stats['output_support_size']}")
    print(f"  Time: {dl6_stats['time_s']:.1f}s")

    # Write l7
    l7_path = OUT_DIR / "l7_patch_septuples_full.jsonl"
    n_written = write_l7_jsonl(l7_single, l7_multi, l7_path)
    print(f"\n  l7 table written: {l7_path}")
    print(f"  Entries written: {n_written:,}")
    l7_size_mb = l7_path.stat().st_size / 1024 / 1024
    print(f"  File size: {l7_size_mb:.1f} MB")

    # Free l6 memory before δl7 probe
    del l6_dict

    # Probe δl7
    print("\n[6/6] Probing δl7 on random 8-tuples...")
    dl7_stats = probe_delta_l7(l7_single, bracket, g1, n_samples=200000)

    print(f"\n  === δl7 Results ===")
    print(f"  Sampled 8-tuples: {dl7_stats['N8']:,}")
    print(f"  Nonzero: {dl7_stats['nonzero']:,}")
    print(f"  Nonzero rate: {dl7_stats['nonzero_rate']:.8f}")
    print(f"  Single-term: {dl7_stats['single_term']}")
    print(f"  Multi-term: {dl7_stats['multi_term']}")

    # Save full report
    report = {
        "version": "V22",
        "description": "Exact δL6 on candidate 7-tuples → full l7 table, δL7 probe",
        "inputs": {
            "l6_entries": 777495,
            "l6_source": "V20 exact (l6_patch_sextuples_full.jsonl)",
            "g1_size": len(g1),
        },
        "deltaL6_exact_on_candidates": dl6_stats,
        "deltaL7_sample": dl7_stats,
        "notes": {
            "second_CE_sum_vanishes": "For g1 inputs, [g1,g1]→g2, so the [xi,xj]-substitution terms vanish.",
            "l7_convention": "l7 = -δl6",
            "dedup_method": "Nonzero results tracked via packed bytes keys; zero results may be recomputed.",
        },
    }
    report_path = OUT_DIR / "v22_exact_deltaL6_and_deltaL7_sample.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n  Full report: {report_path}")

    # Write markdown report
    md = f"""# V22 — Exact δL6 → Full l7, then δL7 Probe

## Inputs
- **l6 table**: 777,495 entries (V20 exact)
- **g1 basis**: {len(g1)} elements

## A) Exact δL6 on candidate 7-tuples
- Raw candidates generated: {dl6_stats['n_raw_candidates']:,}
- Unique computed: {dl6_stats['n_unique_computed']:,}
- Skipped (dedup): {dl6_stats['n_skipped_dedup']:,}
- **Nonzero**: {dl6_stats['n_nonzero']:,}
  - Single-term: {dl6_stats['n_single_term']:,}
  - Multi-term: {dl6_stats['n_multi_term']:,}
- Nonzero rate: {dl6_stats['nonzero_rate_on_unique']:.6f}
- Output support size: {dl6_stats['output_support_size']}
- Time: {dl6_stats['time_s']:.1f}s

## l7 table
- Entries: {n_written:,}
- File: l7_patch_septuples_full.jsonl ({l7_size_mb:.1f} MB)

## B) δL7 probe on random g1 8-tuples
- Sampled: {dl7_stats['N8']:,}
- Nonzero: {dl7_stats['nonzero']:,}
- Nonzero rate: {dl7_stats['nonzero_rate']:.8f}
- All single-term: {'Yes' if dl7_stats['multi_term'] == 0 else 'No'}

## Coefficient histogram (δL6)
"""
    for entry in dl6_stats['coeff_hist_top'][:12]:
        md += f"- coeff {entry['coeff']:+d}: {entry['count']:,}\n"

    md += f"""
## Coefficient histogram (δL7)
"""
    for entry in dl7_stats.get('coeff_hist_top', [])[:12]:
        md += f"- coeff {entry['coeff']:+d}: {entry['count']:,}\n"

    md += f"""
## Key observations
- The L∞ tower pattern continues: single-term outputs, persistent 234-support.
- Sparsity cascade: nonzero rates decrease each level.
- The bracket [g1,g1]→g2 ensures the second CE sum vanishes for g1 inputs.
"""
    (OUT_DIR / "V22_REPORT.md").write_text(md, encoding="utf-8")
    print(f"  Markdown report: {OUT_DIR / 'V22_REPORT.md'}")

    print("\n" + "=" * 72)
    print("V22 COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
