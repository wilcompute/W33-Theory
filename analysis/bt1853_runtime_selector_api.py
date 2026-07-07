#!/usr/bin/env python3
"""BT1853: canonical runtime selector API.

Single import point for the winner-2 E8 selector constants used by aperture,
trace, and shot protocol witnesses.
"""
from __future__ import annotations

import json
from pathlib import Path

CANONICAL_BASIS_NAME = "E8_selector_winner2_BT954_BT956_BT959"
METRIC_WINNER = 2
CANONICAL_SELECTOR_PAIRS = ((3, 68), (4, 42), (38, 65), (90, 144))
SELECTOR_PAIRS_BY_STRIATION = {
    0: (3, 68),
    1: (4, 42),
    2: (38, 65),
    3: (90, 144),
}
SOURCE_CHAIN = (
    "BT951 support-minimum 60",
    "BT954 vertex metric winner 2",
    "BT956 tetracode metric winner 2",
    "BT959 transported S4 rigidity inside support-60 minimizers",
)
BOUNDARY = "local A2/Weyl/glue stabilizer refinement remains open"

OUT = Path("data/PART_BT1853_RUNTIME_SELECTOR_API_results.json")


def selector_pair_for_striation(striation: int) -> tuple[int, int]:
    if striation not in SELECTOR_PAIRS_BY_STRIATION:
        raise KeyError(f"invalid striation {striation}; expected 0..3")
    return SELECTOR_PAIRS_BY_STRIATION[striation]


def selector_record(striation: int) -> dict:
    a, b = selector_pair_for_striation(striation)
    return {
        "e8_metric_winner": METRIC_WINNER,
        "e8_selector_pair_a": a,
        "e8_selector_pair_b": b,
        "canonical_basis_name": CANONICAL_BASIS_NAME,
        "tetracode_quotient_status": "transported_S4_closed_local_A2_open",
    }


def theorem_summary():
    return {
        "theorem": "BT1853 Canonical Runtime Selector API",
        "canonical_basis_name": CANONICAL_BASIS_NAME,
        "metric_winner": METRIC_WINNER,
        "canonical_selector_pairs": [list(p) for p in CANONICAL_SELECTOR_PAIRS],
        "selector_pairs_by_striation": {str(k): list(v) for k, v in SELECTOR_PAIRS_BY_STRIATION.items()},
        "source_chain": list(SOURCE_CHAIN),
        "boundary": BOUNDARY,
        "checks": {
            "four_striations": sorted(SELECTOR_PAIRS_BY_STRIATION) == [0, 1, 2, 3],
            "winner_two": METRIC_WINNER == 2,
            "s4_rigidity_in_source_chain": any("S4" in s for s in SOURCE_CHAIN),
            "local_A2_boundary_recorded": "A2" in BOUNDARY
        },
        "honest_scope": "Reusable constants/API only; it centralizes the selected basis but does not compute new quotient data."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if all(summary["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
