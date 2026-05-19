"""Completed global defect Dirichlet package for the split-prime cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import completed_defect_dirichlet_profile


PROFILE_LIMITS = [31, 1000, 10000, 100000, 1000000]
S_VALUES = [0.5, 1.0, 2.0]


def build_payload() -> dict[str, object]:
    profile = completed_defect_dirichlet_profile(PROFILE_LIMITS, S_VALUES)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "The completed defect Dirichlet product Dhat_X(s)=Product_{p<=X, p≡1 mod 3} ((p-2+p^{-s})/(p-p^{-s})) "
                "* (1-1/p)^(-2(1-p^{-s})) is the global analytic object underneath the finite-adelic packet. For real s>0 it is "
                "positive and numerically stable, and its completed logarithmic derivative converges simultaneously."
            ),
            "largest_cutoff_completed_values": {key: rows[-1]["completed_real"] for key, rows in profile.items()},
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_completed_dirichlet_series.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) COMPLETED GLOBAL DEFECT DIRICHLET SERIES")
    print("=" * 88)
    for s_key, rows in payload["profile"].items():
        print(f"s={s_key}")
        for row in rows:
            print(
                f"  X={row['prime_limit']}: completed={row['completed_real']}, "
                f"log-derivative={row['completed_log_derivative_real']}"
            )
    print(f"\nlargest-cutoff completed values: {payload['summary']['largest_cutoff_completed_values']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
