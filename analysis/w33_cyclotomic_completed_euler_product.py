"""Completed split-prime Euler product for the W(3,q) cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import split_prime_completed_pgf_profile


PROFILE_LIMITS = [1000, 10000, 100000, 1000000]
T_VALUES = [0.0, 0.5, 0.75]


def build_payload() -> dict[str, object]:
    profile = split_prime_completed_pgf_profile(PROFILE_LIMITS, T_VALUES)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "The renormalized split-prime Euler product C_X(t)=G_X(t) * Product_{p<=X, p≡1 mod 3}(1-1/p)^(-2(1-t)) "
                "has its logarithmic singularity removed term-by-term. Its local factors are 1+O(1/p^2), so the infinite "
                "completed product converges absolutely, and the old normalized PGF shadow is recovered exactly by multiplying "
                "back the normalized residue-class Mertens kernel."
            ),
            "largest_cutoff_completed_constants": {
                key: rows[-1]["completed_pgf"] for key, rows in profile.items()
            },
            "largest_cutoff_mertens_constant_estimate": profile["0.0"][-1]["normalized_mertens"],
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_completed_euler_product.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC COMPLETED EULER PRODUCT")
    print("=" * 88)
    for t_key, rows in payload["profile"].items():
        print(f"t={t_key}")
        for row in rows:
            print(
                f"  X={row['prime_limit']}: completed={row['completed_pgf']}, "
                f"normalized_mertens={row['normalized_mertens']}, recovered_shadow={row['shadow_recovered']}"
            )
    print(f"\ncompleted constants at largest cutoff: {payload['summary']['largest_cutoff_completed_constants']}")
    print(f"mertens constant estimate at largest cutoff: {payload['summary']['largest_cutoff_mertens_constant_estimate']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
