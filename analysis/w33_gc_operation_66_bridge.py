#!/usr/bin/env python3
"""Bridge W33 scheduler 66 to the Grünbaum-Coxeter operation table.

The local Grünbaum-Coxeter table records operation counts for the 11-cell,
57-cell, and tomotope.  This verifier extracts the narrow facts that matter for
the current architecture:

* maximal expanded 11-cell starts with 66;
* omnitruncated 11-cell starts with 660 = 10*66 = |PSL(2,11)|;
* rectified 11-cell exposes 55 and 66 in the same table block;
* expanded/omnitruncated tomotope expose 48 and 96.

The bridge is intentionally finite and checked against the local text file.  It
does not assert geometric realization, amalgamation, or cover equivalence.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_gc_operation_66_bridge.json"
DEFAULT_MD = ROOT / "docs" / "w33_gc_operation_66_bridge.md"
DEFAULT_SOURCE = Path("/mnt/c/Users/wiljd/OneDrive/Desktop/Cleanup/Grünbaum-Coxeter polytopes.txt")


def first_count_after(text: str, marker: str) -> int:
    start = text.index(marker)
    block = text[start : start + 900]
    match = re.search(r"\|\s*(\d+)\s*\|", block)
    if not match:
        raise ValueError(f"could not find first count after {marker!r}")
    return int(match.group(1))


def block_contains(text: str, marker: str, pattern: str, window: int = 1200) -> bool:
    start = text.index(marker)
    return re.search(pattern, text[start : start + window]) is not None


def psl2_order(q: int) -> int:
    # q(q^2-1)/gcd(2,q-1), for odd q.
    return q * (q * q - 1) // 2


def build_payload(source_path: Path = DEFAULT_SOURCE) -> dict[str, Any]:
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    text = source_path.read_text(encoding="utf-8", errors="replace")
    selector_path = ROOT / "data" / "w33_perfect_route_selector_runtime.json"
    selector = json.loads(selector_path.read_text(encoding="utf-8"))
    full_load = int(next(iter(selector["line_loads"]["full_histogram"].keys())))
    direct_load = int(next(iter(selector["line_loads"]["direct_histogram"].keys())))
    nonlocal_load = int(next(iter(selector["line_loads"]["nonlocal_histogram"].keys())))

    expanded_11 = first_count_after(text, "maximal expanded 11-cell")
    omni_11 = first_count_after(text, "omnitruncated 11-cell")
    rectified_11 = first_count_after(text, "rectified 11-cell")
    expanded_57 = first_count_after(text, "maximal expanded 57-cell")
    omni_57 = first_count_after(text, "omnitruncated 57-cell")
    expanded_tomotope = first_count_after(text, "maximal expanded tomotope")
    omni_tomotope = first_count_after(text, "omnitruncated tomotope")

    k12_edges = 66
    k12_vertices = 12
    k12_cycle_rank = k12_edges - k12_vertices + 1
    checks = {
        "selector_pass": selector["status"] == "PASS",
        "scheduler_full_load_66": full_load == 66,
        "scheduler_decomposition_12_plus_54": direct_load + nonlocal_load == full_load,
        "expanded_11_first_count_66": expanded_11 == 66,
        "omni_11_first_count_660": omni_11 == 660,
        "omni_11_is_10_times_66": omni_11 == 10 * expanded_11,
        "omni_11_equals_psl2_11_order": omni_11 == psl2_order(11),
        "rectified_11_first_count_55": rectified_11 == 55,
        "rectified_11_contains_66": block_contains(
            text, "rectified 11-cell", r"\|\s*\*\s*66\s*\|"
        ),
        "rectified_11_55_is_k12_cycle_rank": rectified_11 == k12_cycle_rank,
        "expanded_57_first_count_570": expanded_57 == 570,
        "omni_57_first_count_3420": omni_57 == 3420,
        "omni_57_is_six_times_expanded_57": omni_57 == 6 * expanded_57,
        "expanded_tomotope_first_count_48": expanded_tomotope == 48,
        "omni_tomotope_first_count_96": omni_tomotope == 96,
        "tomotope_omni_is_double_expanded": omni_tomotope == 2 * expanded_tomotope,
        "tomotope_expanded_is_4_times_k": expanded_tomotope == 4 * k12_vertices,
    }
    return {
        "schema": "w33.gc_operation_66_bridge.v1",
        "theorem": "W33 scheduler 66 is the maximal-expanded 11-cell count in the GC operation table",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source": str(source_path),
        "w33_scheduler": {
            "direct_line_load": direct_load,
            "nonlocal_line_load": nonlocal_load,
            "full_line_load": full_load,
            "decomposition": "66 = 12 + 54",
        },
        "gc_counts": {
            "rectified_11_first": rectified_11,
            "maximal_expanded_11_first": expanded_11,
            "omnitruncated_11_first": omni_11,
            "maximal_expanded_57_first": expanded_57,
            "omnitruncated_57_first": omni_57,
            "maximal_expanded_tomotope_first": expanded_tomotope,
            "omnitruncated_tomotope_first": omni_tomotope,
        },
        "bridges": {
            "expanded_11_equals_scheduler": "66 = full W33 line-bus load = E(K12)",
            "omni_11_order": "660 = 10*66 = |PSL(2,11)|",
            "rectified_11_cycle_rank": "55 = 66 - 12 + 1 = beta1(K12)",
            "tomotope_body": "48 = 4*12 and 96 = 2*48",
            "boundary": "Counts are exact table bridges; no cover/isomorphism claim is made.",
        },
        "checks": checks,
        "interpretation": (
            "The W33 route selector's 66 lands on the same integer spine as the "
            "11-cell operation tower: rectification exposes 55/66, maximal "
            "expansion starts at 66, and omnitruncation starts at 660. The "
            "tomotope operation tower sits on the 48/96 body counts already used "
            "by the Holonet tomotope packet ABI."
        ),
        "honesty_boundary": (
            "This is a text-backed arithmetic bridge against the local GC table. "
            "It does not prove the W33 selector is a 11-cell operation or that "
            "the tomotope cover tower is isomorphic to the W33 route selector."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    c = payload["gc_counts"]
    return f"""# W(3,3) GC Operation 66 Bridge

The perfect W33 route selector produces a full line-bus load:

```text
66 = 12 direct + 54 nonlocal
```

The local Grünbaum-Coxeter operation table exposes the same spine:

| Object / operation | First count | Bridge |
|---|---:|---|
| Rectified 11-cell | {c['rectified_11_first']} | `55 = 66 - 12 + 1 = beta1(K12)` |
| Maximal expanded 11-cell | {c['maximal_expanded_11_first']} | `66 = E(K12) = W33 full line-bus load` |
| Omnitruncated 11-cell | {c['omnitruncated_11_first']} | `660 = 10*66 = |PSL(2,11)|` |
| Maximal expanded 57-cell | {c['maximal_expanded_57_first']} | `570 = 10*57` |
| Omnitruncated 57-cell | {c['omnitruncated_57_first']} | `3420 = 6*570` |
| Maximal expanded tomotope | {c['maximal_expanded_tomotope_first']} | `48 = 4*12` |
| Omnitruncated tomotope | {c['omnitruncated_tomotope_first']} | `96 = 2*48` |

Boundary: exact count bridge only. No geometric realization, cover, or
isomorphism claim is made here.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)
    payload = build_payload(Path(args.source))
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(f"scheduler load: {payload['w33_scheduler']['full_line_load']}")
    print(f"expanded 11-cell: {payload['gc_counts']['maximal_expanded_11_first']}")
    print(f"omnitruncated 11-cell: {payload['gc_counts']['omnitruncated_11_first']}")
    print(f"tomotope expanded/omni: {payload['gc_counts']['maximal_expanded_tomotope_first']}/{payload['gc_counts']['omnitruncated_tomotope_first']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
