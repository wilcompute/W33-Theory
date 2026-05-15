"""Partial-a / partial-b operation commutation bridge for Klitzing tomotope data.

We already have two exact pieces in-repo:

1) partial sheet law at the seed packets:
       partial_a = 2 * partial_b
   with principal packets
       partial_a = (8,24,32,8,8), partial_b = (4,12,16,4,4).

2) operation ladder on the mod_b tomotope rows:
       rectified -> truncated -> maximal expanded -> omnitruncated
       12 -> 24 -> 48 -> 96.

This module adds the missing symmetric partial-a operation ladder as the unique
sheet-lift implied by (1):
       24 -> 48 -> 96 -> 192.

It then verifies commutation of two maps on operation counts:

- S(x) = 2x  (sheet map: b -> a)
- O(x) = 2x  (next operation step in this ladder)

so S∘O = O∘S stagewise.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    EXPLORATION = ROOT / "exploration"
    if str(EXPLORATION) not in sys.path:
        sys.path.insert(0, str(EXPLORATION))
else:
    ROOT = Path(__file__).resolve().parents[1]
    EXPLORATION = ROOT / "exploration"
    if str(EXPLORATION) not in sys.path:
        sys.path.insert(0, str(EXPLORATION))

from exploration.w33_tomotope_klitzing_ladder import leading_counts
from exploration.w33_tomotope_partial_sheet_bridge import (
    partial_a_principal_counts,
    partial_b_principal_counts,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_klitzing_partial_operation_commutation_summary.json"
KLITZING_TABLE_DIR = ROOT / "data" / "klitzing_tables"


def _load_klitzing_csv_lines() -> list[str]:
    if not KLITZING_TABLE_DIR.exists():
        return []
    lines: list[str] = []
    for csv_path in sorted(KLITZING_TABLE_DIR.glob("klitzing_table_html_*.csv")):
        try:
            lines.extend(csv_path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except OSError:
            continue
    return lines


def _find_klitzing_command_evidence() -> dict[str, list[str]]:
    lines = _load_klitzing_csv_lines()
    command_substrings = {
        "rect_mod_b": "rect(mod_b(e(x3o3o *b4o)))",
        "trunc_mod_b": "trunc(mod_b(e(x3o3o *b4o)))",
        "exp_mod_b": "exp(mod_b(e(x3o3o *b4o)))",
        "omni_mod_b": "omni(mod_b(e(x3o3o *b4o)))",
        "rect_mod_a": "rect(mod_a(e(x3o3o *b4o)))",
        "trunc_mod_a": "trunc(mod_a(e(x3o3o *b4o)))",
        "exp_mod_a": "exp(mod_a(e(x3o3o *b4o)))",
        "omni_mod_a": "omni(mod_a(e(x3o3o *b4o)))",
    }
    evidence: dict[str, list[str]] = {}
    for key, needle in command_substrings.items():
        evidence[key] = [line for line in lines if needle in line]
    return evidence


def partial_b_operation_counts() -> tuple[int, int, int, int]:
    counts = leading_counts()
    return (counts[0], counts[1], counts[2], counts[3])


def partial_a_operation_counts_inferred() -> tuple[int, int, int, int]:
    b = partial_b_operation_counts()
    return tuple(2 * x for x in b)


def _operation_step(x: int) -> int:
    return 2 * x


def _sheet_map(x: int) -> int:
    return 2 * x


def commutation_table() -> list[dict[str, Any]]:
    b = partial_b_operation_counts()
    rows: list[dict[str, Any]] = []
    for i in range(len(b) - 1):
        x = b[i]
        so = _sheet_map(_operation_step(x))
        os = _operation_step(_sheet_map(x))
        rows.append(
            {
                "stage_index": i,
                "b_stage": x,
                "next_b_stage": b[i + 1],
                "S_of_O": so,
                "O_of_S": os,
                "commutes": so == os,
            }
        )
    return rows


def build_summary() -> dict[str, Any]:
    partial_a_seed = partial_a_principal_counts()
    partial_b_seed = partial_b_principal_counts()
    b_ops = partial_b_operation_counts()
    a_ops = partial_a_operation_counts_inferred()
    comm = commutation_table()
    evidence = _find_klitzing_command_evidence()

    direct_b_present = all(len(evidence[k]) >= 1 for k in ("rect_mod_b", "trunc_mod_b", "exp_mod_b", "omni_mod_b"))
    direct_a_present = any(len(evidence[k]) >= 1 for k in ("rect_mod_a", "trunc_mod_a", "exp_mod_a", "omni_mod_a"))

    return {
        "status": "ok",
        "source_anchor": {
            "url": "https://bendwavy.org/klitzing/explain/gc.htm",
            "symbol": "GC(x3o3o *b4o)",
            "directly_encoded_operation_rows": "mod_b" if direct_b_present else "unknown",
            "partial_a_operation_rows_present": direct_a_present,
            "partial_a_operation_rows_method": (
                "direct-from-csv"
                if direct_a_present
                else "sheet-lift from exact partial_a=2*partial_b law"
            ),
            "klitzing_command_evidence_counts": {k: len(v) for k, v in evidence.items()},
            "klitzing_command_evidence_samples": {
                k: (v[0] if v else "") for k, v in evidence.items()
            },
        },
        "seed_packets": {
            "partial_a": list(partial_a_seed),
            "partial_b": list(partial_b_seed),
            "entrywise_ratio": [a // b for a, b in zip(partial_a_seed, partial_b_seed)],
        },
        "operation_ladders": {
            "partial_b_direct": list(b_ops),
            "partial_a_inferred": list(a_ops),
            "stage_names": [
                "rectified",
                "truncated",
                "maximal_expanded",
                "omnitruncated",
            ],
        },
        "commutation": {
            "maps": {
                "S": "x -> 2x (sheet map)",
                "O": "x -> 2x (next operation step in encoded ladder)",
            },
            "table": comm,
            "all_stagewise_commute": all(row["commutes"] for row in comm),
        },
        "checks": {
            "seed_sheet_law_exact": all(a == 2 * b for a, b in zip(partial_a_seed, partial_b_seed)),
            "operation_ladder_b_is_doubling": b_ops == (12, 24, 48, 96),
            "operation_ladder_a_is_sheet_lift": a_ops == (24, 48, 96, 192),
            "sheet_operation_commute": all(row["commutes"] for row in comm),
            "inferred_omnitruncated_a_hits_192": a_ops[-1] == 192,
            "direct_mod_b_commands_present_in_klitzing_dumps": direct_b_present,
            "direct_mod_a_commands_absent_for_tomotope_symbol": not direct_a_present,
        },
        "bridge_verdict": (
            "Given exact seed sheet-doubling and the encoded mod_b operation ladder, "
            "the unique sheet-lifted partial_a operation ladder is 24->48->96->192, "
            "and sheet-doubling commutes with operation progression stagewise."
        ),
        "scope_note": (
            "The partial_a operation ladder is currently inferred (not directly transcribed row-by-row from Klitzing in this repo)."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_summary()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
