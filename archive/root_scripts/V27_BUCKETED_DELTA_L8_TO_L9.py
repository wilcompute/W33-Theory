#!/usr/bin/env python3
"""
V27 — Bucketed/out-of-core exact l9 = -δl8 (streaming, no in-memory l8 dict).

Pipeline:
  (A) MAP:    stream l8 JSONL and emit per-(t9, out) contribution records into hashed buckets
  (B) REDUCE: for each bucket, aggregate contributions per t9 and write the final l9 JSONL

Differential (same convention as V24/V25/V26):
  δl_n(x0,...,xn) = Σ_i (-1)^i [ x_i , l_n(x0,...,x̂_i,...,xn) ]
  l_{n+1} = -δl_n

Notes:
  - Uses the basis ordering from `artifacts/e8_structure_constants_w33_discrete.json`.
  - Builds grades by matching `root_orbit` (order-independent).
  - Uses the firewall-filtered bracket by zeroing the 162 forbidden g1×g1 pairs.
    (This filter does not affect [g1, g2], but we keep the same bracket wrapper.)
  - MAP expands each l8 entry only along g1 neighbors of its g2 output (exactly 19),
    rather than all 73 possible insertions.
  - Bucket record format (fixed-size, little-endian):
        packed_t9 (18 bytes; 9×uint16) +
        out_idx   (uint16) +
        coeff     (int32)
    Total: 24 bytes/record.
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
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"

DEFAULT_SC_JSON = ARTIFACTS / "e8_structure_constants_w33_discrete.json"
DEFAULT_META_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_root_metadata_table.json"
DEFAULT_COUPLINGS_JSON = ROOT / "extracted_v13" / "W33-Theory-master" / "artifacts" / "e8_g1g1_couplings_cubic_firewall.json"
DEFAULT_L8_JSONL = ROOT / "V26_output_v13_full" / "l8_patch_octuples_full.jsonl"
DEFAULT_OUT_DIR = ROOT / "V27_output"

Pair = Tuple[int, int]
Terms = Tuple[Tuple[int, int], ...]  # tuple[(basis_index, coeff)]

# Binary bucket record encoding
PACK8 = struct.Struct("<8H")
PACKH = struct.Struct("<H")
REC_TAIL = struct.Struct("<Hi")  # out_idx:uint16, coeff:int32
REC_SIZE = 18 + REC_TAIL.size  # packed_t9 (18 bytes) + (H,i)
UNPACK9 = struct.Struct("<9H")


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Bucketed exact l9 = -δl8 (out-of-core).")
    ap.add_argument("--sc", type=Path, default=DEFAULT_SC_JSON, help="structure constants JSON")
    ap.add_argument("--meta", type=Path, default=DEFAULT_META_JSON, help="root metadata JSON (grades by root_orbit)")
    ap.add_argument("--couplings", type=Path, default=DEFAULT_COUPLINGS_JSON, help="firewall g1×g1 couplings JSON")
    ap.add_argument("--l8-jsonl", type=Path, default=DEFAULT_L8_JSONL, help="input l8 JSONL (octuples)")
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
        help="Process only the first N l8 lines in MAP stage (0 = all).",
    )
    ap.add_argument(
        "--stage",
        choices=["map", "reduce", "all"],
        default="all",
        help="Run MAP only, REDUCE only, or both (default: all).",
    )
    ap.add_argument("--bucket-start", type=int, default=0, help="First bucket to reduce (inclusive).")
    ap.add_argument("--bucket-end", type=int, default=0, help="Last bucket to reduce (exclusive, 0 = buckets).")
    ap.add_argument("--keep-buckets", action="store_true", help="Do not delete bucket files after reduction.")
    ap.add_argument(
        "--no-write-jsonl",
        action="store_true",
        help="Do not write the full l9 JSONL (still aggregates and reports stats).",
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


def _g_grade_indices(
    cartan_dim: int, roots: List[Tuple[int, ...]], grade_by_root: Dict[Tuple[int, ...], str], grade: str
) -> List[int]:
    out = [cartan_dim + i for i, rt in enumerate(roots) if grade_by_root[rt] == grade]
    if len(out) != 81:
        raise RuntimeError(f"Expected 81 {grade} indices; got {len(out)}")
    return sorted(out)


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


def _neighbors_by_out(bracket: BracketCacheFiltered, g1: List[int], g2: List[int]) -> Dict[int, List[Tuple[int, Terms]]]:
    """For each g2 output basis index `out`, list g in g1 with nonzero [g,out]."""
    out: Dict[int, List[Tuple[int, Terms]]] = {}
    for out_idx in g2:
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
    l8_jsonl: Path,
    bucket_dir: Path,
    buckets: int,
    max_lines: int,
    progress_every: int,
    bracket: BracketCacheFiltered,
    g1: List[int],
    g2: List[int],
) -> dict:
    os.makedirs(bucket_dir, exist_ok=True)
    paths = _bucket_paths(bucket_dir, buckets)
    for p in paths:
        if p.exists():
            p.unlink()

    neighbors = _neighbors_by_out(bracket, g1, g2)

    pow2 = _is_pow2(buckets)
    mask = buckets - 1

    files = [p.open("wb") for p in paths]

    n_lines = 0
    n_records = 0
    n_skipped_in_tuple = 0
    n_bad_format = 0

    t0 = time.time()
    try:
        with l8_jsonl.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                if max_lines and n_lines >= max_lines:
                    break
                line = line.strip()
                if not line:
                    continue
                n_lines += 1

                entry = json.loads(line)
                ins = entry.get("in")
                if not isinstance(ins, list) or len(ins) != 8:
                    n_bad_format += 1
                    continue
                t8 = tuple(int(x) for x in ins)
                if t8 != tuple(sorted(t8)):
                    raise RuntimeError(f"Line {line_no}: expected sorted t8")

                # l8 is expected to be single-term (corrected tower), but support multi-term inputs defensively.
                if "coeff" in entry:
                    l8_terms: Terms = ((int(entry["out"]), int(entry["coeff"])),)
                else:
                    raw_terms = entry.get("terms")
                    if not isinstance(raw_terms, list) or not raw_terms:
                        n_bad_format += 1
                        continue
                    l8_terms = tuple((int(k), int(c)) for k, c in raw_terms)

                packed_t8 = PACK8.pack(*t8)
                mv_t8 = memoryview(packed_t8)

                for out_idx, coeff in l8_terms:
                    nbrs = neighbors.get(out_idx)
                    if nbrs is None:
                        raise RuntimeError(
                            f"Line {line_no}: l8 output {out_idx} not in g2; "
                            "this bucketed MAP currently assumes l8 outputs are g2 roots."
                        )

                    for g, br_terms in nbrs:
                        pos = bisect_left(t8, g)
                        if pos < 8 and t8[pos] == g:
                            n_skipped_in_tuple += 1
                            continue

                        sign = 1 if (pos & 1) == 0 else -1  # (-1)^pos
                        g_bytes = PACKH.pack(g)
                        packed_t9 = bytes(mv_t8[: 2 * pos]) + g_bytes + bytes(mv_t8[2 * pos :])

                        if pow2:
                            b = zlib.crc32(packed_t9) & mask
                        else:
                            b = zlib.crc32(packed_t9) % buckets

                        for out2, bcoeff in br_terms:
                            v = sign * coeff * bcoeff
                            if v == 0:
                                continue
                            files[b].write(packed_t9)
                            files[b].write(REC_TAIL.pack(int(out2), int(v)))
                            n_records += 1

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
        "l8_lines": int(n_lines),
        "records_written": int(n_records),
        "skipped_due_to_g_in_t8": int(n_skipped_in_tuple),
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
    write_jsonl: bool,
) -> dict:
    os.makedirs(out_dir, exist_ok=True)
    out_jsonl = out_dir / "l9_patch_9tuples_full.jsonl"

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
    max_abs_coeff = 0
    coeff_hist = Counter()
    output_support = Counter()
    multi_terms_hist = Counter()

    t0 = time.time()
    fout = out_jsonl.open("w", encoding="utf-8") if write_jsonl else None
    try:
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
                        key = bytes(mv[off : off + 18])
                        out_idx, coeff = REC_TAIL.unpack_from(mv, off + 18)
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
                            d = cur  # type: ignore[assignment]
                            d[int(out_idx)] = d.get(int(out_idx), 0) + int(coeff)

                    if progress_every and (n_records % progress_every == 0):
                        elapsed = time.time() - t0
                        print(f"  [REDUCE] records={n_records:,} elapsed={elapsed:.1f}s", flush=True)

            for key, val in acc.items():
                n_unique += 1
                t9 = list(UNPACK9.unpack(key)) if fout is not None else None

                if isinstance(val, list) and len(val) == 2:
                    out_idx, s = int(val[0]), int(val[1])
                    if s == 0:
                        continue
                    n_nonzero += 1
                    n_single += 1
                    coeff = -s  # l9 = -δl8
                    if abs(coeff) > max_abs_coeff:
                        max_abs_coeff = abs(coeff)
                    coeff_hist[coeff] += 1
                    output_support[out_idx] += 1
                    if fout is not None:
                        fout.write(json.dumps({"in": t9, "out": out_idx, "coeff": coeff}) + "\n")
                elif isinstance(val, dict):
                    terms = [[int(i), -int(c)] for i, c in val.items() if c]
                    if not terms:
                        continue
                    terms.sort(key=lambda t: t[0])
                    n_nonzero += 1
                    if len(terms) == 1:
                        n_single += 1
                        out_idx, coeff = terms[0]
                        if abs(coeff) > max_abs_coeff:
                            max_abs_coeff = abs(coeff)
                        coeff_hist[coeff] += 1
                        output_support[out_idx] += 1
                        if fout is not None:
                            fout.write(json.dumps({"in": t9, "out": out_idx, "coeff": coeff}) + "\n")
                    else:
                        n_multi += 1
                        multi_terms_hist[len(terms)] += 1
                        for out_idx, coeff in terms:
                            output_support[out_idx] += 1
                            if abs(coeff) > max_abs_coeff:
                                max_abs_coeff = abs(coeff)
                            coeff_hist[coeff] += 1
                        if fout is not None:
                            fout.write(json.dumps({"in": t9, "terms": terms}) + "\n")
                else:
                    vec = val  # type: ignore[assignment]
                    terms = [[i, -int(c)] for i, c in enumerate(vec) if c]
                    if not terms:
                        continue
                    n_nonzero += 1
                    if len(terms) == 1:
                        n_single += 1
                        out_idx, coeff = terms[0]
                        if abs(coeff) > max_abs_coeff:
                            max_abs_coeff = abs(coeff)
                        coeff_hist[coeff] += 1
                        output_support[out_idx] += 1
                        if fout is not None:
                            fout.write(json.dumps({"in": t9, "out": out_idx, "coeff": coeff}) + "\n")
                    else:
                        n_multi += 1
                        multi_terms_hist[len(terms)] += 1
                        for out_idx, coeff in terms:
                            output_support[out_idx] += 1
                            if abs(coeff) > max_abs_coeff:
                                max_abs_coeff = abs(coeff)
                            coeff_hist[coeff] += 1
                        if fout is not None:
                            fout.write(json.dumps({"in": t9, "terms": terms}) + "\n")

            if (not keep_buckets) and p.exists():
                p.unlink()
    finally:
        if fout is not None:
            fout.close()

    elapsed = time.time() - t0
    return {
        "stage": "reduce",
        "bucket_dir": str(bucket_dir),
        "buckets": int(buckets),
        "bucket_range": [int(bucket_start), int(bucket_end)],
        "records_read": int(n_records),
        "unique_t9_seen": int(n_unique),
        "nonzero_l9": int(n_nonzero),
        "single_term": int(n_single),
        "multi_term": int(n_multi),
        "keys_upgraded_to_dict": int(n_upgraded),
        "max_abs_coeff": int(max_abs_coeff),
        "output_support_size": int(len(output_support)),
        "coeff_hist_top": [{"coeff": int(c), "count": int(n)} for c, n in coeff_hist.most_common(30)],
        "multi_terms_hist": [{"terms": int(k), "count": int(v)} for k, v in sorted(multi_terms_hist.items())],
        "top_outputs": [{"basis": int(k), "count": int(v)} for k, v in output_support.most_common(25)],
        "elapsed_s": round(elapsed, 2),
        "out_jsonl": str(out_jsonl) if write_jsonl else None,
    }


def main() -> None:
    args = _parse_args()

    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    out_dir: Path = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    bucket_dir = out_dir / "l9_buckets"
    report_json = out_dir / "v27_bucketed_deltaL8_to_l9_report.json"

    cartan_dim, roots, br_full = _load_structure_constants(args.sc)
    grade_by_root = _load_grade_by_root(args.meta)
    g1 = _g_grade_indices(cartan_dim, roots, grade_by_root, "g1")
    g2 = _g_grade_indices(cartan_dim, roots, grade_by_root, "g2")
    forbidden_pairs = _load_forbidden_pairs(args.couplings)
    bracket = BracketCacheFiltered(br_full, set(g1), forbidden_pairs)

    print("=" * 78)
    print("V27 — Bucketed exact l9 = -δl8")
    print("=" * 78)
    print(f"l8 jsonl:       {args.l8_jsonl}")
    print(f"out dir:        {out_dir}")
    print(f"buckets:        {args.buckets}")
    print(f"max l8 lines:   {args.max_lines or 'ALL'}")
    print(f"stage:          {args.stage}")
    print(f"bucket range:   [{args.bucket_start}, {args.bucket_end or args.buckets})")

    t0 = time.time()
    report: dict = {
        "version": "V27",
        "inputs": {
            "structure_constants": str(args.sc),
            "root_metadata": str(args.meta),
            "couplings": str(args.couplings),
            "l8_jsonl": str(args.l8_jsonl),
            "g1_size": len(g1),
            "g2_size": len(g2),
            "forbidden_pairs": len(forbidden_pairs),
        },
        "params": {
            "buckets": int(args.buckets),
            "max_lines": int(args.max_lines),
            "stage": str(args.stage),
            "bucket_start": int(args.bucket_start),
            "bucket_end": int(args.bucket_end),
            "keep_buckets": bool(args.keep_buckets),
            "write_jsonl": not bool(args.no_write_jsonl),
            "progress_every": int(args.progress_every),
        },
    }

    if args.stage in ("map", "all"):
        print("\n[1/2] MAP stage: streaming l8 → bucket records ...")
        rep_map = map_stage(
            l8_jsonl=args.l8_jsonl,
            bucket_dir=bucket_dir,
            buckets=args.buckets,
            max_lines=args.max_lines,
            progress_every=args.progress_every,
            bracket=bracket,
            g1=g1,
            g2=g2,
        )
        report["map"] = rep_map
        print(
            f"  MAP done: lines={rep_map['l8_lines']:,} records={rep_map['records_written']:,} time={rep_map['elapsed_s']}s"
        )

    if args.stage in ("reduce", "all"):
        print("\n[2/2] REDUCE stage: aggregating buckets → l9 JSONL ...")
        rep_reduce = reduce_stage(
            bucket_dir=bucket_dir,
            buckets=args.buckets,
            bucket_start=args.bucket_start,
            bucket_end=args.bucket_end,
            out_dir=out_dir,
            progress_every=args.progress_every,
            keep_buckets=args.keep_buckets,
            write_jsonl=not args.no_write_jsonl,
        )
        report["reduce"] = rep_reduce
        print(
            f"  REDUCE done: nonzero_l9={rep_reduce['nonzero_l9']:,} "
            f"(single={rep_reduce['single_term']:,} multi={rep_reduce['multi_term']:,}) "
            f"time={rep_reduce['elapsed_s']}s"
        )

    report["elapsed_total_s"] = round(time.time() - t0, 2)
    report_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nreport: {report_json}")


if __name__ == "__main__":
    main()
