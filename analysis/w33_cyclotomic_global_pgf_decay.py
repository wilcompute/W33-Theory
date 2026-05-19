"""Global logarithmic PGF decay for the split-prime cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import split_prime_packet_pgf_profile


PROFILE_LIMITS = [1000, 10000, 100000, 1000000]
T_VALUES = [0.0, 0.5, 0.75]


def build_payload() -> dict[str, object]:
    profile = split_prime_packet_pgf_profile(PROFILE_LIMITS, T_VALUES)
    return {
        "profile": profile,
        "summary": {
            "statement": (
                "For fixed t<1, the finite split-prime PGF G_X(t)=Product_{p<=X, p≡1 mod 3}(p-2+t)/(p-t) decays like "
                "(log X)^(-(1-t)). Equivalently the normalized packet G_X(t)*(log X)^(1-t) approaches a stable constant shadow."
            ),
            "largest_cutoff_normalized": {
                key: rows[-1]["normalized_pgf"] for key, rows in profile.items()
            },
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_global_pgf_decay.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC GLOBAL PGF DECAY")
    print("=" * 88)
    for t_key, rows in payload["profile"].items():
        print(f"t={t_key}")
        for row in rows:
            print(
                f"  X={row['prime_limit']}: G_X={row['pgf']}, "
                f"normalized={row['normalized_pgf']} with exponent {row['normalizing_exponent']}"
            )
    print(f"\nnormalized constants at largest cutoff: {payload['summary']['largest_cutoff_normalized']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
