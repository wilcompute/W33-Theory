#!/usr/bin/env python3
"""Collect canonical combinatorial structures mentioned in the fgmarcelis top-nav
(PG(3,2), 27 lines, MOG) and write consolidated artifacts for downstream use.

Writes:
 - artifacts/fgmarcelis_topnav_structures.json
 - (verifies existing artifacts for PG(3,2) and 27-lines)

This is safe, non-destructive and idempotent.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "fgmarcelis_topnav_structures.json"

# helper to import THE_EXACT_MAP (provides build_mog_map)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main():
    # PG(3,2) artifacts (already harvested earlier)
    pg32_points_path = ROOT / "artifacts" / "pg32_points_from_remaining15.json"
    pg32_lines_path = ROOT / "artifacts" / "pg32_lines_from_remaining15.json"

    pg32 = None
    if pg32_points_path.exists() and pg32_lines_path.exists():
        pg32 = {
            "points_file": str(pg32_points_path),
            "lines_file": str(pg32_lines_path),
        }

    # 27 lines artifact (CKM script produces summary + intersection data)
    ckm_path = next(
        (
            path
            for path in [
                ROOT / "CKM_27_LINES.json",
                ROOT / "archive" / "json" / "CKM_27_LINES.json",
            ]
            if path.exists()
        ),
        None,
    )
    lines27 = None
    if ckm_path is not None:
        lines27 = {"ckm_file": str(ckm_path)}

    # MOG mapping from THE_EXACT_MAP (pos_to_line_mog)
    mog_map = None
    try:
        exact_path = next(
            path
            for path in [
                ROOT / "THE_EXACT_MAP.py",
                ROOT / "exploration" / "THE_EXACT_MAP.py",
            ]
            if path.exists()
        )
        exact = _load_module(exact_path, "THE_EXACT_MAP")
        mog_map = {str(k): int(v) for k, v in exact.pos_to_line_mog.items()}
    except (FileNotFoundError, StopIteration):
        mog_map = None

    out = {
        "source": "fgmarcelis top-nav (selected pages)",
        "pg32": pg32,
        "27_lines": lines27,
        "mog_map_pos_to_line": mog_map,
    }

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote:", OUT)
    return out


if __name__ == "__main__":
    main()
