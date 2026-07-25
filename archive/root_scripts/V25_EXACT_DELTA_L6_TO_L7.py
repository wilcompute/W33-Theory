#!/usr/bin/env python3
"""
V25 — Exact δL6 → l7 from a corrected l6 table (V24).

This computes

    l7(t7) = -δ l6(t7)

on candidate g1 7-tuples, where δ is the “action-only” CE-style operator used in
V22/V23:

    δ l_n(x0,...,xn) = Σ_i (-1)^i [ x_i , l_n(x0,...,x̂_i,...,xn) ].

We restrict to g1 inputs, so we only ever need l6 values on g1 sextuples. The
result is streamed to JSONL (no in-memory l7 table).

Notes:
  - Uses the basis ordering from `artifacts/e8_structure_constants_w33_discrete.json`.
  - Builds g1 indices by matching `root_orbit` (order-independent).
  - Uses the firewall-filtered bracket by zeroing the 162 forbidden g1×g1 pairs.
    (This filter does not affect l7 because l6 outputs are grade g0.)
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

DEFAULT_SC_JSON = ARTIFACTS / "e8_structure_constants_w33_discrete.json"
DEFAULT_META_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
DEFAULT_COUPLINGS_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_g1g1_couplings_cubic_firewall.json"
DEFAULT_L6_JSONL = ROOT / "V24_output_v13_full" / "l6_patch_sextuples_full.jsonl"
DEFAULT_OUT_DIR = ROOT / "V25_output"

Pair = Tuple[int, int]
Terms = Tuple[Tuple[int, int], ...]  # tuple[(basis_index, coeff)]


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Compute exact l7 = -δl6 on candidate g1 7-tuples (streaming).")
    ap.add_argument("--sc", type=Path, default=DEFAULT_SC_JSON, help="structure constants JSON")
    ap.add_argument("--meta", type=Path, default=DEFAULT_META_JSON, help="root metadata JSON (grades by root_orbit)")
    ap.add_argument("--couplings", type=Path, default=DEFAULT_COUPLINGS_JSON, help="firewall g1×g1 couplings JSON")
    ap.add_argument("--l6-jsonl", type=Path, default=DEFAULT_L6_JSONL, help="input l6 JSONL (sextuples)")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="output directory")
    ap.add_argument(
        "--max-source-entries",
        type=int,
        default=0,
        help="Only expand the first N l6 entries (0 = all). Still loads full l6 for exact δ.",
    )
    ap.add_argument(
        "--progress-every",
        type=int,
        default=25_000,
        help="Print progress every N processed l6 entries (0 disables).",
    )
    return ap.parse_args()


def _load_structure_constants(path: Path) -> tuple[int, List[Tuple[int, ...]], Dict[Pair, Terms]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    basis = data["basis"]
    cartan_dim = int(basis["cartan_dim"])
    roots = [tuple(int(x) for x in r) for r in basis["roots"]]

    brackets_raw: Dict[str, List[List[int]]] = data["brackets"]
    br: Dict[Pair, Terms] = {}
    for key, terms in brackets_raw.items():
        i_str, j_str = key.split(",")
        i, j = int(i_str), int(j_str)
        br[(i, j)] = tuple((int(k), int(c)) for k, c in terms)
    return cartan_dim, roots, br


def _load_grade_by_root(path: Path) -> Dict[Tuple[int, ...], str]:
    meta = json.loads(path.read_text(encoding="utf-8"))
    out: Dict[Tuple[int, ...], str] = {}
    for row in meta["rows"]:
        rt = tuple(int(x) for x in row["root_orbit"])
        out[rt] = str(row["grade"])
    if len(out) != 240:
        raise RuntimeError(f"Expected 240 root grades; got {len(out)}")
    return out


def _g1_indices(cartan_dim: int, roots: List[Tuple[int, ...]], grade_by_root: Dict[Tuple[int, ...], str]) -> List[int]:
    g1 = [cartan_dim + i for i, rt in enumerate(roots) if grade_by_root[rt] == "g1"]
    if len(g1) != 81:
        raise RuntimeError(f"Expected 81 g1 indices; got {len(g1)}")
    return sorted(g1)


def _load_forbidden_pairs(path: Path) -> set[Pair]:
    data = json.loads(path.read_text(encoding="utf-8"))
    forb: set[Pair] = set()
    for rec in data.get("couplings", []):
        if not rec.get("firewall_forbidden"):
            continue
        a = int(rec["in"][0]["basis"])
        b = int(rec["in"][1]["basis"])
        i, j = (a, b) if a < b else (b, a)
        forb.add((i, j))
    if len(forb) != 162:
        raise RuntimeError(f"Expected 162 forbidden pairs; got {len(forb)}")
    return forb


class BracketCacheFiltered:
    """Antisymmetric bracket with firewall-filtered g1×g1 pairs zeroed."""

    def __init__(self, br_full: Dict[Pair, Terms], g1_set: set[int], forbidden_pairs: set[Pair]):
        self._br = br_full
        self._g1 = g1_set
        self._forb = forbidden_pairs
        self._cache: Dict[Pair, Terms] = {}

    def __call__(self, i: int, j: int) -> Terms:
        if i == j:
            return ()
        ck = (int(i), int(j))
        cached = self._cache.get(ck)
        if cached is not None:
            return cached

        if i < j:
            key, sgn = (i, j), 1
        else:
            key, sgn = (j, i), -1

        if (i in self._g1) and (j in self._g1) and (key in self._forb):
            out: Terms = ()
            self._cache[ck] = out
            return out

        raw = self._br.get(key)
        if not raw:
            out = ()
        elif sgn == 1:
            out = raw
        else:
            out = tuple((k, -c) for k, c in raw)

        self._cache[ck] = out
        return out


def _vec_add(dst: Dict[int, int], src: Dict[int, int]) -> None:
    for k, v in src.items():
        nv = dst.get(k, 0) + v
        if nv:
            dst[k] = nv
        else:
            dst.pop(k, None)


def delta_ln(t_np1: Tuple[int, ...], ln: Dict[Tuple[int, ...], Terms], bracket: BracketCacheFiltered) -> Dict[int, int]:
    """Compute δl_n on a sorted (n+1)-tuple, with l_n stored as Terms tuples."""
    result: Dict[int, int] = {}
    n1 = len(t_np1)
    for i in range(n1):
        sub = t_np1[:i] + t_np1[i + 1 :]
        terms = ln.get(sub)
        if terms is None:
            continue
        xi = int(t_np1[i])
        sign = (-1) ** i
        for out, coeff in terms:
            br = bracket(xi, out)
            for k, bv in br:
                v = sign * coeff * bv
                if v == 0:
                    continue
                nv = result.get(k, 0) + v
                if nv:
                    result[k] = nv
                else:
                    result.pop(k, None)
    return result


def load_ln_jsonl(path: Path, n_in: int) -> tuple[Dict[Tuple[int, ...], Terms], dict]:
    ln: Dict[Tuple[int, ...], Terms] = {}
    n_single = 0
    n_multi = 0
    max_terms = 0
    max_abs_coeff = 0

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            ins = entry.get("in")
            if not isinstance(ins, list) or len(ins) != n_in:
                raise RuntimeError(f"Line {line_no}: expected `in` length {n_in}")
            key = tuple(int(x) for x in ins)
            if key != tuple(sorted(key)):
                raise RuntimeError(f"Line {line_no}: expected sorted `in` tuple")

            if "coeff" in entry:
                n_single += 1
                terms: Terms = ((int(entry["out"]), int(entry["coeff"])),)
                max_abs_coeff = max(max_abs_coeff, abs(int(entry["coeff"])))
            else:
                n_multi += 1
                raw_terms = entry.get("terms")
                if not isinstance(raw_terms, list) or not raw_terms:
                    raise RuntimeError(f"Line {line_no}: missing/invalid `terms`")
                terms = tuple((int(k), int(c)) for k, c in raw_terms)
                max_terms = max(max_terms, len(terms))
                for _, c in terms:
                    max_abs_coeff = max(max_abs_coeff, abs(int(c)))

            ln[key] = terms

    stats = {
        "entries": len(ln),
        "single_entries": n_single,
        "multi_entries": n_multi,
        "max_terms_in_entry": max_terms,
        "max_abs_coeff_in_table": max_abs_coeff,
    }
    return ln, stats


def get_mem_mb() -> float:
    try:
        import psutil

        return psutil.Process().memory_info().rss / 1024 / 1024
    except Exception:
        return 0.0


def main() -> None:
    args = _parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    out_jsonl = args.out_dir / "l7_patch_septuples_full.jsonl"
    report_json = args.out_dir / "v25_exact_deltaL6_to_l7_report.json"

    t0 = time.time()
    cartan_dim, roots, br_full = _load_structure_constants(args.sc)
    grade_by_root = _load_grade_by_root(args.meta)
    g1 = _g1_indices(cartan_dim, roots, grade_by_root)
    forbidden_pairs = _load_forbidden_pairs(args.couplings)
    bracket = BracketCacheFiltered(br_full, set(g1), forbidden_pairs)

    print("=" * 78)
    print("V25 — Exact δL6 → l7 (correct indexing, streaming)")
    print("=" * 78)
    print(f"structure_constants: {args.sc}")
    print(f"root_metadata:       {args.meta}")
    print(f"couplings:           {args.couplings}")
    print(f"g1 size:             {len(g1)}")
    print(f"l6 jsonl:            {args.l6_jsonl}")

    print("\n1) Loading l6 table...")
    l6, l6_stats = load_ln_jsonl(args.l6_jsonl, n_in=6)
    print(f"   l6 entries: {l6_stats['entries']:,} (single={l6_stats['single_entries']:,} multi={l6_stats['multi_entries']:,})")
    print(f"   l6 max |coeff|: {l6_stats['max_abs_coeff_in_table']}")
    if l6_stats["multi_entries"]:
        print(f"   l6 max terms in one entry: {l6_stats['max_terms_in_entry']}")

    # Candidate enumeration
    def pack7(t7: Tuple[int, int, int, int, int, int, int]) -> bytes:
        return struct.pack("7H", *t7)

    seen_nonzero: set[bytes] = set()

    n_candidates = 0
    n_computed = 0
    n_skipped = 0
    n_nonzero = 0
    n_single = 0
    n_multi = 0
    coeff_hist = Counter()
    output_support = Counter()
    multi_term_counts = Counter()
    max_abs_coeff = 0

    print("\n2) Computing l7 = -δl6 on candidate 7-tuples...")
    t1 = time.time()
    total_l6 = len(l6)
    limit = args.max_source_entries if args.max_source_entries else total_l6
    limit = min(limit, total_l6)

    with out_jsonl.open("w", encoding="utf-8") as fout:
        for idx, (t6, _) in enumerate(l6.items(), 1):
            if idx > limit:
                break
            t6_set = set(t6)
            for g in g1:
                if g in t6_set:
                    continue
                n_candidates += 1
                t7 = tuple(sorted((*t6, g)))  # type: ignore[assignment]
                key = pack7(t7)  # type: ignore[arg-type]
                if key in seen_nonzero:
                    n_skipped += 1
                    continue
                n_computed += 1

                res = delta_ln(t7, l6, bracket)  # δl6
                if not res:
                    continue

                seen_nonzero.add(key)
                n_nonzero += 1

                items = tuple(sorted((int(k), int(-v)) for k, v in res.items()))  # l7 = -δl6
                if len(items) == 1:
                    n_single += 1
                    out, coeff = items[0]
                    coeff_hist[coeff] += 1
                    output_support[out] += 1
                    max_abs_coeff = max(max_abs_coeff, abs(int(coeff)))
                    fout.write(json.dumps({"in": list(t7), "out": out, "coeff": coeff}) + "\n")
                else:
                    n_multi += 1
                    multi_term_counts[len(items)] += 1
                    terms = [[k, c] for k, c in items]
                    for out, coeff in items:
                        output_support[out] += 1
                        max_abs_coeff = max(max_abs_coeff, abs(int(coeff)))
                    fout.write(json.dumps({"in": list(t7), "terms": terms}) + "\n")

            if args.progress_every and (idx % args.progress_every == 0 or idx == limit):
                elapsed = time.time() - t1
                rate = idx / elapsed if elapsed > 0 else 0.0
                eta = (limit - idx) / rate if rate > 0 else 0.0
                print(
                    f"  [{idx:>7d}/{limit}] candidates={n_candidates:,} computed={n_computed:,} nonzero={n_nonzero:,} "
                    f"skipped={n_skipped:,} elapsed={elapsed:.1f}s ETA={eta:.0f}s mem~{get_mem_mb():.0f}MB",
                    flush=True,
                )

    elapsed = time.time() - t1
    print("\nDONE")
    print(f"  raw candidates: {n_candidates:,}")
    print(f"  computed (attempts): {n_computed:,}")
    print(f"  skipped (known-nonzero dedup): {n_skipped:,}")
    print(f"  nonzero l7: {n_nonzero:,} (single={n_single:,} multi={n_multi:,})")
    print(f"  output support: {len(output_support)} / 248")
    print(f"  max |coeff|: {max_abs_coeff}")
    print(f"  wrote: {out_jsonl}")
    print(f"  time: {elapsed:.2f}s")

    report = {
        "version": "V25",
        "inputs": {
            "structure_constants": str(args.sc),
            "root_metadata": str(args.meta),
            "couplings": str(args.couplings),
            "l6_jsonl": str(args.l6_jsonl),
            "g1_size": len(g1),
            "forbidden_pairs": len(forbidden_pairs),
            "max_source_entries": int(args.max_source_entries),
        },
        "l6_stats": l6_stats,
        "deltaL6_to_l7": {
            "raw_candidates": int(n_candidates),
            "computed_attempts": int(n_computed),
            "skipped_dedup": int(n_skipped),
            "nonzero": int(n_nonzero),
            "single_term": int(n_single),
            "multi_term": int(n_multi),
            "nonzero_rate_on_attempts": n_nonzero / max(n_computed, 1),
            "output_support_size": len(output_support),
            "max_abs_coeff": int(max_abs_coeff),
            "coeff_hist_top": [{"coeff": int(c), "count": int(n)} for c, n in coeff_hist.most_common(30)],
            "multi_term_count_hist": [{"terms": int(k), "count": int(v)} for k, v in sorted(multi_term_counts.items())],
            "top_outputs": [{"basis": int(k), "count": int(v)} for k, v in output_support.most_common(25)],
            "time_s": round(elapsed, 2),
        },
        "paths": {"l7_jsonl": str(out_jsonl)},
        "elapsed_total_s": round(time.time() - t0, 2),
    }
    report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nreport: {report_json}")


if __name__ == "__main__":
    main()
