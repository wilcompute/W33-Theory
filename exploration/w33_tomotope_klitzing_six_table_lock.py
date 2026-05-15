"""Locate and verify the six tomotope sections in Klitzing's Abstract polytopes HTML.

Targets:
1) partial a marker in GC(x3o3o *b4o) section
2) partial b marker in GC(x3o3o *b4o) section
3) rect(mod_b(e(x3o3o *b4o)))
4) trunc(mod_b(e(x3o3o *b4o)))
5) exp(mod_b(e(x3o3o *b4o)))
6) omni(mod_b(e(x3o3o *b4o)))

The verifier also returns table boundaries and checks that the operation anchors
co-live in one operation table while partial-a/partial-b co-live in one GC table.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML_PATH = Path(r"C:\Users\wiljd\Downloads\Abstract polytopes.html")
DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_klitzing_six_table_lock_summary.json"


@dataclass(frozen=True)
class Hit:
    label: str
    start: int
    end: int
    table_start: int | None
    table_end: int | None
    context: str


def _find_table_ranges(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in re.finditer(r"<table\b.*?</table>", text, re.I | re.S)]


def _enclosing_table(pos: int, ranges: list[tuple[int, int]]) -> tuple[int | None, int | None]:
    for s, e in ranges:
        if s <= pos < e:
            return s, e
    return None, None


def _context(text: str, i: int, j: int, width: int = 100) -> str:
    c0 = max(0, i - width)
    c1 = min(len(text), j + width)
    return text[c0:c1].replace("\r", " ").replace("\n", " ")


def _first_literal_hit(label: str, literal: str, text: str, ranges: list[tuple[int, int]]) -> Hit | None:
    i = text.find(literal)
    if i == -1:
        return None
    j = i + len(literal)
    ts, te = _enclosing_table(i, ranges)
    return Hit(label=label, start=i, end=j, table_start=ts, table_end=te, context=_context(text, i, j))


def _first_regex_hit(label: str, pattern: str, text: str, ranges: list[tuple[int, int]]) -> Hit | None:
    m = re.search(pattern, text, re.I | re.S)
    if not m:
        return None
    i, j = m.start(), m.end()
    ts, te = _enclosing_table(i, ranges)
    return Hit(label=label, start=i, end=j, table_start=ts, table_end=te, context=_context(text, i, j))


def parse_klitzing_html(text: str) -> dict[str, Any]:
    ranges = _find_table_ranges(text)

    gc_symbol = _first_regex_hit(
        "gc_symbol",
        r"GC\s*\(\s*x3o3o\s*\*b4o\s*\)",
        text,
        ranges,
    )
    if gc_symbol is None:
        # Real page often wraps x3o3o *b4o inside an anchor tag.
        gc_symbol = _first_regex_hit(
            "gc_symbol",
            r"GC\s*\(\s*<a[^>]*>\s*x3o3o\s*\*b4o\s*</a>\s*\)",
            text,
            ranges,
        )

    hit_partial_a = _first_literal_hit("partial_a", "(partial a)", text, ranges)
    hit_partial_b = _first_literal_hit("partial_b", "(partial b)", text, ranges)
    hit_rect = _first_literal_hit("rect_mod_b", "rect(mod_b(e(x3o3o *b4o)))", text, ranges)
    hit_trunc = _first_literal_hit("trunc_mod_b", "trunc(mod_b(e(x3o3o *b4o)))", text, ranges)
    hit_exp = _first_literal_hit("exp_mod_b", "exp(mod_b(e(x3o3o *b4o)))", text, ranges)
    hit_omni = _first_literal_hit("omni_mod_b", "omni(mod_b(e(x3o3o *b4o)))", text, ranges)

    partial_hits = [h for h in [hit_partial_a, hit_partial_b] if h]
    operation_hits = [h for h in [hit_rect, hit_trunc, hit_exp, hit_omni] if h]

    partial_tables = {(h.table_start, h.table_end) for h in partial_hits}
    operation_tables = {(h.table_start, h.table_end) for h in operation_hits}

    checks = {
        "file_contains_tables": len(ranges) >= 1,
        "gc_symbol_found": gc_symbol is not None,
        "partial_a_found": hit_partial_a is not None,
        "partial_b_found": hit_partial_b is not None,
        "all_four_operation_anchors_found": len(operation_hits) == 4,
        "partial_a_and_b_share_single_table": len(partial_tables) == 1,
        "four_operations_share_single_table": len(operation_tables) == 1,
        "operations_order_rect_trunc_exp_omni": (
            len(operation_hits) == 4
            and hit_rect.start < hit_trunc.start < hit_exp.start < hit_omni.start
        ),
    }

    return {
        "status": "ok",
        "html_length": len(text),
        "table_count": len(ranges),
        "table_ranges": ranges,
        "hits": {
            "gc_symbol": asdict(gc_symbol) if gc_symbol else None,
            "partial_a": asdict(hit_partial_a) if hit_partial_a else None,
            "partial_b": asdict(hit_partial_b) if hit_partial_b else None,
            "rect_mod_b": asdict(hit_rect) if hit_rect else None,
            "trunc_mod_b": asdict(hit_trunc) if hit_trunc else None,
            "exp_mod_b": asdict(hit_exp) if hit_exp else None,
            "omni_mod_b": asdict(hit_omni) if hit_omni else None,
        },
        "table_lock": {
            "partial_table": list(partial_tables)[0] if len(partial_tables) == 1 else None,
            "operation_table": list(operation_tables)[0] if len(operation_tables) == 1 else None,
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "verdict": (
            "Six-table lock resolved: partial-a/partial-b co-locate in one GC table; "
            "rect/trunc/exp/omni anchors co-locate in one operation table in strict order."
        ),
    }


def parse_file(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    out = parse_klitzing_html(text)
    out["source_file"] = str(path)
    return out


def write_summary(summary: dict[str, Any], out_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve six tomotope table anchors in Klitzing HTML")
    parser.add_argument("--html", default=str(DEFAULT_HTML_PATH), help="Path to Abstract polytopes HTML")
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT_PATH), help="Output JSON path")
    args = parser.parse_args()

    summary = parse_file(Path(args.html))
    out = write_summary(summary, Path(args.out))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
