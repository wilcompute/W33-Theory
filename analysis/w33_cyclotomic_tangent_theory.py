"""Tangent/cumulant theory at t=1 for the completed split-prime cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import completed_tangent_profile


PROFILE_LIMITS = [19, 31, 1000, 10000, 100000, 1000000]


def build_payload() -> dict[str, object]:
    profile = completed_tangent_profile(PROFILE_LIMITS)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "The completed product C_X(t) has exact tangent log-derivative at t=1 given by kappa_X = Sum_{p<=X, p≡1 mod 3} "
                "(2/(p-1) + 2 log(1-1/p)). This is also E[T_X] + 2 log M_X, so the divergent log log X packet mean is converted "
                "into a convergent cumulant constant once the split-prime Mertens kernel is factored off."
            ),
            "largest_cutoff_cumulant_constant": profile[-1]["completed_tangent_constant"],
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_tangent_theory.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC TANGENT / CUMULANT THEORY AT t=1")
    print("=" * 88)
    for row in payload["profile"]:
        print(
            f"X={row['prime_limit']}: mean={row['packet_mean']}, 2logM={row['twice_log_mertens']}, "
            f"kappa={row['completed_tangent_constant']}"
        )
    print(f"\nlargest-cutoff cumulant constant: {payload['summary']['largest_cutoff_cumulant_constant']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
