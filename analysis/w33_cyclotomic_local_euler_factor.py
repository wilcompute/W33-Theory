"""Local Euler factor for the W(3,q) cyclotomic valuation process."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (
    local_expected_valuation,
    local_valuation_euler_factor,
    local_valuation_pgf,
    local_variance_valuation,
)


def build_payload() -> dict[str, object]:
    split_primes = [7, 13, 19, 31, 37, 43, 61, 67]
    table = []
    for p in split_primes:
        table.append(
            {
                "prime": p,
                "pgf_at_0": local_valuation_pgf(p, 0.0),
                "pgf_at_1": local_valuation_pgf(p, 1.0),
                "expected_valuation": local_expected_valuation(p),
                "variance_valuation": local_variance_valuation(p),
                "reciprocal_denominator": (p - 1) // 2,
                "euler_factor_s_1": local_valuation_euler_factor(p, 1.0),
            }
        )

    return {
        "split_prime_table": table,
        "summary": {
            "statement": (
                "For every split prime p congruent to 1 mod 3, the local valuation law of the cyclotomic defect tree has PGF G_p(t)=(p-2+t)/(p-t). Equivalently the local Euler factor is E[p^{-sV}] = (p-2+p^{-s})/(p-p^{-s}). The mean and variance coincide exactly at 2/(p-1). For the first split primes p=7,13,19 these become 1/3, 1/6, and 1/9, i.e. 1/q, 1/q!, and 1/q^2."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_local_euler_factor.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC LOCAL EULER FACTOR")
    print("=" * 88)
    for row in payload["split_prime_table"]:
        print(
            f"p={row['prime']}: G_p(0)={row['pgf_at_0']}, G_p(1)={row['pgf_at_1']}, "
            f"E[V]={row['expected_valuation']}, Var(V)={row['variance_valuation']}, "
            f"denominator={(row['reciprocal_denominator'])}, Euler(s=1)={row['euler_factor_s_1']}"
        )
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()