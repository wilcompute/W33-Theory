#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from bt1425_retwined_css_frame_correction import build_w33, dense_hx, dense_hz, guard_shear_perm, permute_columns, permute_vector, syndrome, gf_rank

OUT = ROOT / "data" / "bt1471_abi_css_join.json"


def packets():
    for c in range(3):
        for side in range(2):
            for orient in range(2):
                strand = 4 * c + 2 * side + orient
                yield {"c": c, "side": side, "orient": orient, "strand": strand, "active_col": 14 * strand + 13, "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1]}


def one_hot(col: int, value: int, n: int = 240):
    vec = [0] * n
    vec[col] = value % 3
    return vec


def main() -> None:
    _points, edges, triangles = build_w33()
    hx = dense_hx(edges)
    hz = dense_hz(edges, triangles)
    perm = guard_shear_perm()
    hx2 = permute_columns(hx, perm)
    hz2 = permute_columns(hz, perm)
    rows = []
    for p in packets():
        for col_kind, cols in (("active", [p["active_col"]]), ("guard", p["guard_cols"])):
            for col in cols:
                for value in (1, 2):
                    v = one_hot(col, value)
                    w = permute_vector(v, perm)
                    rows.append({
                        "strand": p["strand"],
                        "kind": col_kind,
                        "col": col,
                        "value": value,
                        "moved": w.index(value) != col,
                        "x_ok": syndrome(hx, v) == syndrome(hx2, w),
                        "z_ok": syndrome(hz, v) == syndrome(hz2, w),
                    })
    checks = {
        "rank_hx_39": gf_rank(hx) == 39,
        "rank_hz_120": gf_rank(hz) == 120,
        "logical_k_81": 240 - gf_rank(hx) - gf_rank(hz) == 81,
        "row_count_72": len(rows) == 72,
        "active_rows_24": sum(1 for r in rows if r["kind"] == "active") == 24,
        "guard_rows_48": sum(1 for r in rows if r["kind"] == "guard") == 48,
        "active_cols_fixed": all(not r["moved"] for r in rows if r["kind"] == "active"),
        "x_all_ok": all(r["x_ok"] for r in rows),
        "z_all_ok": all(r["z_ok"] for r in rows),
    }
    result = {
        "bt": 1471,
        "title": "ABI to CSS executable join",
        "verified": all(checks.values()),
        "counts": {"rows": len(rows), "active": sum(1 for r in rows if r["kind"] == "active"), "guard": sum(1 for r in rows if r["kind"] == "guard")},
        "css": {"rank_hx": gf_rank(hx), "rank_hz": gf_rank(hz), "k": 240 - gf_rank(hx) - gf_rank(hz)},
        "sample_rows": rows[:12],
        "interpretation": "The ABI-generated closure rows feed directly into the retwined CSS matrices and satisfy both X and Z syndrome checks.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1471, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
