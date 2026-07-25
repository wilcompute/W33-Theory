#!/usr/bin/env python3
"""
V26 — Bucketed/out-of-core exact l8 = -δl7 (streaming, no in-memory l7 dict).

We avoid loading the 22M-row l7 table into a Python dict by using a 2-stage pipeline:

  (A) MAP:   stream l7 JSONL and emit per-(t8, out) contribution records into hashed buckets
  (B) REDUCE: for each bucket, aggregate contributions per t8 and write the final l8 JSONL

Differential (same convention as V24/V25):
  δl_n(x0,...,xn) = Σ_i (-1)^i [ x_i , l_n(x0,...,x̂_i,...,xn) ]
  l_{n+1} = -δl_n

Implementation notes
  - Uses the structure-constants basis ordering from `artifacts/e8_structure_constants_w33_discrete.json`.
  - Uses the firewall-filtered bracket: 162 forbidden g1×g1 pairs are zeroed.
  - For speed, MAP expands each l7 entry only along g1 neighbors of its output (≈16),
    not along all 74 possible insertions.
  - Bucket record format (fixed-size, little-endian):
        packed_t8 (16 bytes; 8×uint16) +
        out_idx   (uint16) +
        coeff     (int32)
    Total: 22 bytes/record.

This script is designed to support a “pilot” run using `--max-lines` to estimate
full-run size/time before committing to the full 22.3M-line MAP stage.
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import sys
import time
import zlib
from bisect import bisect_left
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

DEFAULT_SC_JSON = ARTIFACTS / "e8_structure_constants_w33_discrete.json"
DEFAULT_META_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
DEFAULT_COUPLINGS_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_g1g1_couplings_cubic_firewall.json"
DEFAULT_L7_JSONL = ROOT / "V25_output_v13_full" / "l7_patch_septuples_full.jsonl"
DEFAULT_OUT_DIR = ROOT / "V26_output"

Pair = Tuple[int, int]
Terms = Tuple[Tuple[int, int], ...]  # tuple[(basis_index, coeff)]

# Binary bucket record encoding
PACK7 = struct.Struct("<7H")
PACKH = struct.Struct("<H")
REC_TAIL = struct.Struct("<Hi")  # out_idx:uint16, coeff:int32
REC_SIZE = 16 + REC_TAIL.size  # packed_t8 (16 bytes) + (H,i)
UNPACK8 = struct.Struct("<8H")


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Bucketed exact l8 = -δl7 (out-of-core).")
    ap.add_argument("--sc", type=Path, default=DEFAULT_SC_JSON, help="structure constants JSON")
    ap.add_argument("--meta", type=Path, default=DEFAULT_META_JSON, help="root metadata JSON (grades by root_orbit)")
    ap.add_argument("--couplings", type=Path, default=DEFAULT_COUPLINGS_JSON, help="firewall g1×g1 couplings JSON")
    ap.add_argument("--l7-jsonl", type=Path, default=DEFAULT_L7_JSONL, help="input l7 JSONL (septuples)")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="output directory")
    ap.add_argument(
        "--buckets",
        type=int,
        default=256,
        help="Number of hash buckets (recommended: power of 2). Pilot default: 256.",
    )
    ap.add_argument(
        "--max-lines",
        type=int,
        default=0,
        help="Process only the first N l7 lines in MAP stage (0 = all).",
    )
    ap.add_argument(
        "--stage",
        choices=["map", "reduce", "all"],
        default="all",
        help="Run MAP only, REDUCE only, or both (default: all).",
    )
    ap.add_argument(
        "--bucket-start",
        type=int,
        default=0,
        help="First bucket to reduce (inclusive).",
    )
    ap.add_argument(
        "--bucket-end",
        type=int,
        default=0,
        help="Last bucket to reduce (exclusive, 0 = buckets).",
    )
    ap.add_argument(
        "--keep-buckets",
        action="store_true",
        help="Do not delete bucket files after reduction.",
    )
    ap.add_argument(
        "--progress-every",
        type=int,
        default=250_000,
        help="Progress print frequency (MAP: lines, REDUCE: records). 0 disables.",
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


def _neighbors_by_out(bracket: BracketCacheFiltered, g1: List[int]) -> Dict[int, List[Tuple[int, Terms]]]:
    """For each g1 output basis index `out`, list g in g1 with nonzero [g,out]."""
    out: Dict[int, List[Tuple[int, Terms]]] = {}
    for out_idx in g1:
        nbrs: List[Tuple[int, Terms]] = []
        for g in g1:
            if g == out_idx:
                continue
            terms = bracket(g, out_idx)
            if terms:
                nbrs.append((g, terms))
        out[out_idx] = nbrs
    return out


def _bucket_paths(bucket_dir: Path, buckets: int) -> List[Path]:
    width = max(4, len(str(buckets - 1)))
    return [bucket_dir / f"bucket_{i:0{width}d}.bin" for i in range(buckets)]


def _is_pow2(n: int) -> bool:
    return n > 0 and (n & (n - 1) == 0)


def map_stage(
    *,
    l7_jsonl: Path,
    bucket_dir: Path,
    buckets: int,
    max_lines: int,
    progress_every: int,
    bracket: BracketCacheFiltered,
    g1: List[int],
) -> dict:
    os.makedirs(bucket_dir, exist_ok=True)
    paths = _bucket_paths(bucket_dir, buckets)
    for p in paths:
        if p.exists():
            p.unlink()

    neighbors = _neighbors_by_out(bracket, g1)

    pow2 = _is_pow2(buckets)
    mask = buckets - 1

    # Open all bucket files once (pilot default buckets=256 is safe).
    files = [p.open("wb") for p in paths]

    n_lines = 0
    n_records = 0
    n_skipped_in_tuple = 0
    n_skipped_zero_bracket = 0
    n_bad_format = 0

    t0 = time.time()
    try:
        with l7_jsonl.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if max_lines and n_lines >= max_lines:
                    break
                line = line.strip()
                if not line:
                    continue
                n_lines += 1

                entry = json.loads(line)
                ins = entry.get("in")
                if not isinstance(ins, list) or len(ins) != 7:
                    n_bad_format += 1
                    continue
                t7 = tuple(int(x) for x in ins)
                if t7 != tuple(sorted(t7)):
                    raise RuntimeError(f"Line {line_no}: expected sorted t7")

                # l7 is expected to be single-term in the corrected tower.
                if "coeff" in entry:
                    l7_terms: Terms = ((int(entry["out"]), int(entry["coeff"])),)
                else:
                    raw_terms = entry.get("terms")
                    if not isinstance(raw_terms, list) or not raw_terms:
                        n_bad_format += 1
                        continue
                    l7_terms = tuple((int(k), int(c)) for k, c in raw_terms)

                packed_t7 = PACK7.pack(*t7)
                mv_t7 = memoryview(packed_t7)

                for out_idx, coeff in l7_terms:
                    nbrs = neighbors.get(out_idx)
                    if nbrs is None:
                        raise RuntimeError(
                            f"Line {line_no}: l7 output {out_idx} not in g1; "
                            "this bucketed MAP currently assumes l7 outputs are g1 roots."
                        )

                    for g, br_terms in nbrs:
                        pos = bisect_left(t7, g)
                        if pos < 7 and t7[pos] == g:
                            n_skipped_in_tuple += 1
                            continue

                        sign = 1 if (pos & 1) == 0 else -1  # (-1)^pos
                        g_bytes = PACKH.pack(g)
                        packed_t8 = bytes(mv_t7[: 2 * pos]) + g_bytes + bytes(mv_t7[2 * pos :])

                        if pow2:
                            b = zlib.crc32(packed_t8) & mask
                        else:
                            b = zlib.crc32(packed_t8) % buckets

                        for out2, bcoeff in br_terms:
                            v = sign * coeff * bcoeff
                            if v == 0:
                                continue
                            files[b].write(packed_t8)
                            files[b].write(REC_TAIL.pack(int(out2), int(v)))
                            n_records += 1

                        if not br_terms:
                            n_skipped_zero_bracket += 1

                if progress_every and (n_lines % progress_every == 0):
                    elapsed = time.time() - t0
                    rate = n_lines / elapsed if elapsed > 0 else 0.0
                    print(
                        f"  [MAP] lines={n_lines:,} records={n_records:,} "
                        f"elapsed={elapsed:.1f}s rate={rate:,.0f} lines/s",
                        flush=True,
                    )
    finally:
        for fp in files:
            fp.close()

    elapsed = time.time() - t0
    return {
        "stage": "map",
        "l7_lines": int(n_lines),
        "records_written": int(n_records),
        "skipped_due_to_g_in_t7": int(n_skipped_in_tuple),
        "bad_format_lines": int(n_bad_format),
        "elapsed_s": round(elapsed, 2),
        "bucket_dir": str(bucket_dir),
        "buckets": int(buckets),
        "max_lines": int(max_lines),
    }


def reduce_stage(
    *,
    bucket_dir: Path,
    buckets: int,
    bucket_start: int,
    bucket_end: int,
    out_dir: Path,
    progress_every: int,
    keep_buckets: bool,
) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    out_jsonl = out_dir / "l8_patch_octuples_full.jsonl"

    paths = _bucket_paths(bucket_dir, buckets)
    if bucket_end <= 0:
        bucket_end = buckets
    if not (0 <= bucket_start < bucket_end <= buckets):
        raise ValueError(f"Invalid bucket range: [{bucket_start}, {bucket_end}) for buckets={buckets}")

    n_records = 0
    n_unique = 0
    n_nonzero = 0
    n_single = 0
    n_multi = 0
    n_upgraded = 0
    coeff_hist = Counter()
    output_support = Counter()
    multi_terms_hist = Counter()

    t0 = time.time()
    with out_jsonl.open("w", encoding="utf-8") as fout:
        for b in range(bucket_start, bucket_end):
            p = paths[b]
            if not p.exists():
                continue

            acc: Dict[bytes, object] = {}

            with p.open("rb") as f:
                while True:
                    buf = f.read(REC_SIZE * 200_000)
                    if not buf:
                        break
                    if len(buf) % REC_SIZE != 0:
                        raise RuntimeError(f"Corrupt bucket file {p}: size not multiple of record size")

                    mv = memoryview(buf)
                    for off in range(0, len(buf), REC_SIZE):
                        key = bytes(mv[off : off + 16])
                        out_idx, coeff = REC_TAIL.unpack_from(mv, off + 16)
                        n_records += 1

                        cur = acc.get(key)
                        if cur is None:
                            if out_idx < 8:
                                vec = [0, 0, 0, 0, 0, 0, 0, 0]
                                vec[out_idx] = coeff
                                acc[key] = vec
                            else:
                                acc[key] = [out_idx, coeff]  # mutable for faster +=
                        elif isinstance(cur, list) and len(cur) == 2:
                            if out_idx == cur[0]:
                                cur[1] += coeff
                            else:
                                # Upgrade to sparse dict to support (rare) multi-term non-Cartan outputs.
                                d: Dict[int, int] = {int(cur[0]): int(cur[1])}
                                d[int(out_idx)] = d.get(int(out_idx), 0) + int(coeff)
                                acc[key] = d
                                n_upgraded += 1
                        elif isinstance(cur, list):
                            # Cartan vector (len==8)
                            if out_idx < 8:
                                cur[out_idx] += coeff
                            else:
                                d = {i: int(c) for i, c in enumerate(cur) if c}
                                d[int(out_idx)] = d.get(int(out_idx), 0) + int(coeff)
                                acc[key] = d
                                n_upgraded += 1
                        else:
                            # Sparse dict
                            d = cur  # type: ignore[assignment]
                            d[int(out_idx)] = d.get(int(out_idx), 0) + int(coeff)

                    if progress_every and (n_records % progress_every == 0):
                        elapsed = time.time() - t0
                        print(
                            f"  [REDUCE] records={n_records:,} unique~={n_unique:,} nonzero={n_nonzero:,} "
                            f"elapsed={elapsed:.1f}s",
                            flush=True,
                        )

            # Flush bucket results
            for key, val in acc.items():
                n_unique += 1
                t8 = list(UNPACK8.unpack(key))

                if isinstance(val, list) and len(val) == 2:
                    out_idx, s = int(val[0]), int(val[1])
                    if s == 0:
                        continue
                    n_nonzero += 1
                    n_single += 1
                    coeff = -s  # l8 = -δl7
                    coeff_hist[coeff] += 1
                    output_support[out_idx] += 1
                    fout.write(json.dumps({"in": t8, "out": out_idx, "coeff": coeff}) + "\n")
                elif isinstance(val, dict):
                    terms = [[int(i), -int(c)] for i, c in val.items() if c]
                    if not terms:
                        continue
                    terms.sort(key=lambda t: t[0])
                    n_nonzero += 1
                    if len(terms) == 1:
                        n_single += 1
                        out_idx, coeff = terms[0]
                        coeff_hist[coeff] += 1
                        output_support[out_idx] += 1
                        fout.write(json.dumps({"in": t8, "out": out_idx, "coeff": coeff}) + "\n")
                    else:
                        n_multi += 1
                        multi_terms_hist[len(terms)] += 1
                        for out_idx, coeff in terms:
                            output_support[out_idx] += 1
                            coeff_hist[coeff] += 1
                        fout.write(json.dumps({"in": t8, "terms": terms}) + "\n")
                else:
                    vec = val  # type: ignore[assignment]
                    terms = [[i, -int(c)] for i, c in enumerate(vec) if c]
                    if not terms:
                        continue
                    n_nonzero += 1
                    if len(terms) == 1:
                        n_single += 1
                        out_idx, coeff = terms[0]
                        coeff_hist[coeff] += 1
                        output_support[out_idx] += 1
                        fout.write(json.dumps({"in": t8, "out": out_idx, "coeff": coeff}) + "\n")
                    else:
                        n_multi += 1
                        multi_terms_hist[len(terms)] += 1
                        for out_idx, coeff in terms:
                            output_support[out_idx] += 1
                            coeff_hist[coeff] += 1
                        fout.write(json.dumps({"in": t8, "terms": terms}) + "\n")

            if (not keep_buckets) and p.exists():
                p.unlink()

    elapsed = time.time() - t0
    return {
        "stage": "reduce",
        "bucket_dir": str(bucket_dir),
        "buckets": int(buckets),
        "bucket_range": [int(bucket_start), int(bucket_end)],
        "records_read": int(n_records),
        "unique_t8_seen": int(n_unique),
        "nonzero_l8": int(n_nonzero),
        "single_term": int(n_single),
        "multi_term": int(n_multi),
        "keys_upgraded_to_dict": int(n_upgraded),
        "output_support_size": int(len(output_support)),
        "coeff_hist_top": [{"coeff": int(c), "count": int(n)} for c, n in coeff_hist.most_common(30)],
        "multi_terms_hist": [{"terms": int(k), "count": int(v)} for k, v in sorted(multi_terms_hist.items())],
        "top_outputs": [{"basis": int(k), "count": int(v)} for k, v in output_support.most_common(25)],
        "elapsed_s": round(elapsed, 2),
        "out_jsonl": str(out_jsonl),
    }


def main() -> None:
    args = _parse_args()

    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    out_dir: Path = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    bucket_dir = out_dir / "l8_buckets"
    report_json = out_dir / "v26_bucketed_deltaL7_to_l8_report.json"

    cartan_dim, roots, br_full = _load_structure_constants(args.sc)
    grade_by_root = _load_grade_by_root(args.meta)
    g1 = _g1_indices(cartan_dim, roots, grade_by_root)
    forbidden_pairs = _load_forbidden_pairs(args.couplings)
    bracket = BracketCacheFiltered(br_full, set(g1), forbidden_pairs)

    print("=" * 78)
    print("V26 — Bucketed exact l8 = -δl7")
    print("=" * 78)
    print(f"l7 jsonl:       {args.l7_jsonl}")
    print(f"out dir:        {out_dir}")
    print(f"buckets:        {args.buckets}")
    print(f"max l7 lines:   {args.max_lines or 'ALL'}")
    print(f"stage:          {args.stage}")
    print(f"bucket range:   [{args.bucket_start}, {args.bucket_end or args.buckets})")

    t0 = time.time()
    report: dict = {
        "version": "V26",
        "inputs": {
            "structure_constants": str(args.sc),
            "root_metadata": str(args.meta),
            "couplings": str(args.couplings),
            "l7_jsonl": str(args.l7_jsonl),
            "g1_size": len(g1),
            "forbidden_pairs": len(forbidden_pairs),
        },
        "params": {
            "buckets": int(args.buckets),
            "max_lines": int(args.max_lines),
            "stage": str(args.stage),
            "bucket_start": int(args.bucket_start),
            "bucket_end": int(args.bucket_end),
            "keep_buckets": bool(args.keep_buckets),
            "progress_every": int(args.progress_every),
        },
    }

    if args.stage in ("map", "all"):
        print("\n[1/2] MAP stage: streaming l7 → bucket records ...")
        rep_map = map_stage(
            l7_jsonl=args.l7_jsonl,
            bucket_dir=bucket_dir,
            buckets=args.buckets,
            max_lines=args.max_lines,
            progress_every=args.progress_every,
            bracket=bracket,
            g1=g1,
        )
        report["map"] = rep_map
        print(f"  MAP done: lines={rep_map['l7_lines']:,} records={rep_map['records_written']:,} time={rep_map['elapsed_s']}s")

    if args.stage in ("reduce", "all"):
        print("\n[2/2] REDUCE stage: aggregating buckets → l8 JSONL ...")
        rep_reduce = reduce_stage(
            bucket_dir=bucket_dir,
            buckets=args.buckets,
            bucket_start=args.bucket_start,
            bucket_end=args.bucket_end,
            out_dir=out_dir,
            progress_every=args.progress_every,
            keep_buckets=args.keep_buckets,
        )
        report["reduce"] = rep_reduce
        print(
            f"  REDUCE done: nonzero_l8={rep_reduce['nonzero_l8']:,} "
            f"(single={rep_reduce['single_term']:,} multi={rep_reduce['multi_term']:,}) "
            f"time={rep_reduce['elapsed_s']}s"
        )

    report["elapsed_total_s"] = round(time.time() - t0, 2)
    report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nreport: {report_json}")


if __name__ == "__main__":
    main()
