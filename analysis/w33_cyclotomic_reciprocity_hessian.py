"""Centered reciprocity, zero Hessian, and odd-cumulant tower for the completed cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_global_centered_reciprocity,
    completed_higher_cumulant_profile,
    completed_local_centered_reciprocity,
)


PROFILE_LIMITS = [19, 31, 1000, 10000, 100000, 1000000]
ORDERS = [1, 2, 3, 4, 5, 7]
OFFSETS = [0.2, 0.25]
LOCAL_PRIMES = [7, 13, 19]


def build_payload() -> dict[str, object]:
    higher = completed_higher_cumulant_profile(PROFILE_LIMITS, ORDERS)
    local_reciprocity = {
        str(p): {
            str(offset): completed_local_centered_reciprocity(p, offset)
            for offset in OFFSETS
        }
        for p in LOCAL_PRIMES
    }
    global_reciprocity = {
        str(offset): [
            {
                "prime_limit": X,
                "product": completed_global_centered_reciprocity(X, offset),
                "abs_error_from_one": abs(completed_global_centered_reciprocity(X, offset) - 1.0),
            }
            for X in PROFILE_LIMITS
        ]
        for offset in OFFSETS
    }
    return {
        "higher_cumulants": higher,
        "local_centered_reciprocity": local_reciprocity,
        "global_centered_reciprocity": global_reciprocity,
        "summary": {
            "statement": (
                "For the completed split-prime product C_X(t), the centered involution C_X(1+u) C_X(1-u)=1 holds exactly. "
                "Hence log C_X(1+u) is odd in u, all even derivatives at t=1 vanish exactly, and the odd completed cumulants are "
                "explicit split-prime sums."
            ),
            "largest_cutoff_cumulants": {key: rows[-1]["log_derivative_at_one"] for key, rows in higher.items()},
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_reciprocity_hessian.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = Path("PART_MCI_cyclotomic_reciprocity_hessian_theorem_results.json")
    result.write_text(json.dumps(payload["summary"], indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) COMPLETED RECIPROCITY / HESSIAN / ODD-CUMULANT TOWER")
    print("=" * 88)
    for key, rows in payload["higher_cumulants"].items():
        print(f"order {key}: {rows[-1]['log_derivative_at_one']}")
    for offset, rows in payload["global_centered_reciprocity"].items():
        print(f"offset {offset}: max error {max(row['abs_error_from_one'] for row in rows)}")
    print(f"wrote {out}")
    print(f"wrote {result}")


if __name__ == "__main__":
    main()