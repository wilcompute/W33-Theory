#!/usr/bin/env python3
"""
V23 — Exact δL7 on candidate 8-tuples using full l7 table (7,106,177 entries).

Chain so far:
  V11: K3 exact (579 nonzero, all single-term)
  V13: K3 = δm proven (cocycle lock)
  V15: Exact δL4 → l4 (7,675 entries), support=234
  V19: l5 exact (85,429 entries, support=234)
  V20: Exact δL5 → l6 exact (777,495 entries, support=234)
  V22: Exact δL6 → l7 exact (7,106,177 entries, support=248 = full E8!)

V23: Compute EXACT δL7 on all candidate 8-tuples → full l8 table.

Key simplification:
  [g1, g1] → g2 only (never g1), so the second CE sum vanishes.
  δl_n(x0,...,xn) = Σᵢ (-1)ⁱ [xᵢ, l_n(x0,...,x̂ᵢ,...,xn)]
  l_{n+1} = -δl_n

l7 entries include:
  - 7,038,170 single-term entries: l7(t7) = coeff * e_{out}
  - 68,007 multi-term entries: l7(t7) = Σ_k coeff_k * e_{out_k} (all Cartan)

Both types contribute to δl7 and must be included.
"""

import json
import struct
import sys
import time
import os
from collections import Counter
from pathlib import Path

ROOT = Path(r"c:\Repos\Theory of Everything")
ARTIFACTS = ROOT / "artifacts"
L7_DIR = ROOT / "V22_output_corrected"
OUT_DIR = ROOT / "V23_output"


# ── Load E8 bracket ──────────────────────────────────────────────────────────

def load_bracket():
    """Load E8 structure constants and build bracket dict."""
    sc = json.loads((ARTIFACTS / "e8_structure_constants_w33_discrete.json").read_text(encoding="utf-8"))
    roots = sc["basis"]["roots"]
    br = {}
    for kk, lst in sc["brackets"].items():
        i, j = (int(x) for x in kk.split(","))
        br[(i, j)] = tuple((int(k), int(c)) for k, c in lst)
    return br, roots


def load_g1_indices(roots):
    """Load g1 basis indices (in the structure-constants root ordering)."""
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


# ── Load l7 table ────────────────────────────────────────────────────────────

def load_l7_table(path):
    """
    Load l7 JSONL into dict: tuple(7 ints) → list of (out_idx, coeff).
    
    Single-term entries: {"in": [...], "out": idx, "coeff": c} → [(idx, c)]
    Multi-term entries:  {"in": [...], "terms": [[idx, c], ...]} → [(idx, c), ...]
    """
    l7 = {}
    n_single = 0
    n_multi = 0
    t0 = time.time()
    with open(path, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            e = json.loads(line)
            key = tuple(e["in"])
            if "terms" in e:
                l7[key] = tuple((int(idx), int(c)) for idx, c in e["terms"])
                n_multi += 1
            else:
                l7[key] = ((int(e["out"]), int(e["coeff"])),)
                n_single += 1
            if line_num % 1_000_000 == 0:
                elapsed = time.time() - t0
                print(f"  Loading l7... {line_num:,} entries ({elapsed:.1f}s, mem~{get_mem_mb():.0f}MB)")
    elapsed = time.time() - t0
    print(f"  Loaded l7: {len(l7):,} entries ({n_single:,} single + {n_multi:,} multi) in {elapsed:.1f}s, mem~{get_mem_mb():.0f}MB")
    return l7


# ── δl7 computation ─────────────────────────────────────────────────────────

def delta_l7(t8, l7_dict, bracket):
    """
    Compute δl7 on a sorted 8-tuple of g1 indices.
    
    δl7(x0,...,x7) = Σᵢ₌₀⁷ (-1)ⁱ [xᵢ, l7(x0,...,x̂ᵢ,...,x7)]
    
    Handles both single-term and multi-term l7 entries.
    Returns dict: {basis_index: coeff} (only nonzero entries).
    """
    result = {}
    for i in range(8):
        sub7 = t8[:i] + t8[i+1:]
        terms = l7_dict.get(sub7)
        if terms is None:
            continue
        xi = t8[i]
        sign = (-1) ** i
        for out, coeff in terms:
            br = bracket(xi, out)
            for k, bv in br:
                v = sign * coeff * bv
                if v == 0:
                    continue
                result[k] = result.get(k, 0) + v
                if result[k] == 0:
                    del result[k]
    return result


# ── Exact l8 computation ────────────────────────────────────────────────────

def compute_exact_l8_streaming(l7_dict, bracket, g1, output_path):
    """
    Enumerate all candidate 8-tuples from l7 entries and compute exact δl7.
    
    Streams results directly to JSONL file to avoid memory exhaustion.
    Only keeps a set of seen-nonzero packed keys in memory.
    
    l8(t8) = -δl7(t8)
    """
    n_l7 = len(l7_dict)

    def pack8(t8):
        return struct.pack('8H', *t8)

    seen_nonzero = set()  # Only stores 16-byte packed keys

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
    l7_items = list(l7_dict.keys())
    print(f"  Starting l8 computation: {n_l7:,} l7 entries × ~{len(g1)} g1 expansions")
    print(f"  Streaming output to: {output_path}")

    with open(output_path, "w", encoding="utf-8") as fout:
        for idx, t7 in enumerate(l7_items):
            t7_set = set(t7)
            for g in g1:
                if g in t7_set:
                    continue
                n_candidates += 1

                # Form sorted 8-tuple
                t8 = tuple(sorted(list(t7) + [g]))
                t8_key = pack8(t8)

                # Skip if already computed as nonzero
                if t8_key in seen_nonzero:
                    n_skipped += 1
                    continue

                n_unique_computed += 1

                # Compute δl7
                res = delta_l7(t8, l7_dict, bracket)

                if not res:
                    continue

                # Nonzero result: l8 = -δl7
                seen_nonzero.add(t8_key)
                n_nonzero += 1

                items = list(res.items())
                if len(items) == 1:
                    n_single += 1
                    k, v = items[0]
                    neg_v = -v
                    coeff_counter[neg_v] += 1
                    output_counter[k] += 1
                    fout.write(json.dumps({"in": list(t8), "out": k, "coeff": neg_v}) + "\n")
                else:
                    n_multi += 1
                    terms = [[k, -v] for k, v in items]
                    for k, v in terms:
                        coeff_counter[v] += 1
                        output_counter[k] += 1
                    fout.write(json.dumps({"in": list(t8), "terms": terms}) + "\n")

            # Progress every 100k l7 entries
            if (idx + 1) % 100_000 == 0 or idx == n_l7 - 1:
                elapsed = time.time() - t0
                rate = (idx + 1) / elapsed if elapsed > 0 else 0
                eta = (n_l7 - idx - 1) / rate if rate > 0 else 0
                print(f"  [{idx+1:>8d}/{n_l7}] candidates={n_candidates:,} "
                      f"unique_computed={n_unique_computed:,} nonzero={n_nonzero:,} "
                      f"(single={n_single:,} multi={n_multi:,}) "
                      f"skipped={n_skipped:,} "
                      f"elapsed={elapsed:.1f}s ETA={eta:.0f}s "
                      f"mem~{get_mem_mb():.0f}MB")

    elapsed = time.time() - t0

    stats = {
        "n_l7_entries": n_l7,
        "n_raw_candidates": n_candidates,
        "n_unique_computed": n_unique_computed,
        "n_skipped_dedup": n_skipped,
        "n_nonzero": n_nonzero,
        "n_single_term": n_single,
        "n_multi_term": n_multi,
        "nonzero_rate_on_unique": n_nonzero / max(n_unique_computed, 1),
        "time_s": round(elapsed, 2),
        "coeff_hist_top": [{"coeff": c, "count": n} for c, n in coeff_counter.most_common(30)],
        "output_support_size": len(output_counter),
        "top_outputs": [{"basis": k, "count": n} for k, n in output_counter.most_common(20)],
    }

    return stats


def get_mem_mb():
    """Approximate memory usage in MB."""
    try:
        import psutil
        return psutil.Process().memory_info().rss / 1024 / 1024
    except ImportError:
        return 0


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # Set encoding
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 70)
    print("V23 — Exact δL7 → l8")
    print("=" * 70)

    # Load data
    print("\n1. Loading E8 bracket...")
    br_full, roots = load_bracket()
    bracket = BracketCache(br_full)
    print(f"   Bracket entries: {len(br_full):,}")

    print("\n2. Loading g1 indices (V13 convention)...")
    g1 = load_g1_indices(roots)
    print(f"   g1 count: {len(g1)}")

    print("\n3. Loading l7 table...")
    l7_path = L7_DIR / "l7_patch_septuples_full.jsonl"
    l7_dict = load_l7_table(l7_path)

    # Cross-validate: all l7 input indices should be within g1
    g1_set = set(g1)
    bad = 0
    for t7 in list(l7_dict.keys())[:10000]:
        for x in t7:
            if x not in g1_set:
                bad += 1
                break
    if bad > 0:
        print(f"   WARNING: {bad}/10000 sampled l7 entries have non-g1 inputs!")
    else:
        print(f"   Cross-validation OK: all sampled l7 inputs are in g1")

    print("\n4. Computing exact δl7 → l8 (streaming to disk)...")
    l8_path = OUT_DIR / "l8_patch_octuples_full.jsonl"
    stats = compute_exact_l8_streaming(l7_dict, bracket, g1, l8_path)

    print(f"\n   δL7 results:")
    print(f"   Nonzero: {stats['n_nonzero']:,} ({stats['n_single_term']:,} single + {stats['n_multi_term']:,} multi)")
    print(f"   Nonzero rate: {stats['nonzero_rate_on_unique']:.6f}")
    print(f"   Output support: {stats['output_support_size']}")
    print(f"   Time: {stats['time_s']:.1f}s")

    # File size
    l8_size = l8_path.stat().st_size / (1024 * 1024)
    print(f"   l8 table: {l8_size:.1f} MB")

    # Write report
    print("\n5. Writing report...")
    report = {
        "description": "V23: Exact δL7 → l8",
        "l7_input": {
            "entries": stats["n_l7_entries"],
            "source": str(L7_DIR / "l7_patch_septuples_full.jsonl"),
        },
        "deltaL7_exact": stats,
        "l8_table": {
            "entries": stats["n_nonzero"],
            "file": str(l8_path),
            "size_mb": round(l8_size, 1),
        },
    }
    report_path = OUT_DIR / "v23_exact_deltaL7.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"   Report: {report_path}")

    # Write markdown report
    md_lines = [
        "# V23 — Exact δL7 → Full l8 Table",
        "",
        "## Inputs",
        f"- **l7 table**: {stats['n_l7_entries']:,} entries (V22 exact)",
        f"- **g1 basis**: {len(g1)} elements (V13 metadata convention)",
        "",
        "## Results",
        f"- Raw candidates: {stats['n_raw_candidates']:,}",
        f"- Unique computed: {stats['n_unique_computed']:,}",
        f"- Skipped (dedup): {stats['n_skipped_dedup']:,}",
        f"- **Nonzero l8**: {stats['n_nonzero']:,}",
        f"  - Single-term: {stats['n_single_term']:,}",
        f"  - Multi-term: {stats['n_multi_term']:,}",
        f"- Nonzero rate: {stats['nonzero_rate_on_unique']:.6f}",
        f"- Output support: {stats['output_support_size']}",
        f"- Time: {stats['time_s']:.1f}s",
        "",
        "## Coefficient histogram (top 30)",
    ]
    for ch in stats["coeff_hist_top"]:
        md_lines.append(f"- coeff {ch['coeff']:+d}: {ch['count']:,}")
    md_lines.extend(["", "## Top 20 output basis elements"])
    for oe in stats["top_outputs"]:
        md_lines.append(f"- basis {oe['basis']}: {oe['count']:,}")

    md_path = OUT_DIR / "V23_REPORT.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"   Report: {md_path}")

    print("\n" + "=" * 70)
    print("V23 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
