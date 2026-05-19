"""Log-log growth law for the split-prime cyclotomic valuation packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import split_prime_packet_profile


PROFILE_LIMITS = [19, 31, 1000, 10000, 100000, 1000000]


def build_payload() -> dict[str, object]:
    profile = split_prime_packet_profile(PROFILE_LIMITS)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "If T_X is the total split-prime valuation packet over p<=X with p congruent to 1 mod 3, then "
                "E[T_X]=Var(T_X)=Sum_{p<=X, p≡1 mod 3} 2/(p-1). By the prime number theorem in arithmetic progressions, "
                "this grows like log log X with exact leading coefficient 1."
            ),
            "largest_cutoff_constant_estimate": profile[-1]["mean_minus_loglog"],
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_loglog_packet_growth.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC SPLIT-PRIME PACKET GROWTH")
    print("=" * 88)
    for row in payload["profile"]:
        mean_label = row["mean_fraction"] or f"~{row['mean']}"
        print(
            f"X={row['prime_limit']}: count={row['split_prime_count']}, E[T]={mean_label}, ~ {row['mean']}, "
            f"loglog={row['loglog']}, offset={row['mean_minus_loglog']}"
        )
    print(f"\nconstant estimate at largest cutoff: {payload['summary']['largest_cutoff_constant_estimate']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
