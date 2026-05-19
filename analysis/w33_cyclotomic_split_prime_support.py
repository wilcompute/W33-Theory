"""Split-prime support law for the W(3,q) cyclotomic packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import cyclotomic_prime_support_scan


def build_payload() -> dict[str, object]:
    scan = cyclotomic_prime_support_scan(limit_q=20000)
    return {
        **scan,
        "summary": {
            "statement": (
                "Every prime divisor of Phi3(q)=q^2+q+1 is either 3 or congruent to 1 mod 3, and every prime divisor of "
                "Phi6(q)=q^2-q+1 is either 3 or congruent to 1 mod 6. So the entire cyclotomic packet already lives on the "
                "split-prime side before the squarefree defect refinement is imposed."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_split_prime_support.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC SPLIT-PRIME SUPPORT LAW")
    print("=" * 88)
    print(f"Phi3 exact support on q<= {payload['limit_q']}: {payload['phi3_exact_support']}")
    print(f"Phi6 exact support on q<= {payload['limit_q']}: {payload['phi6_exact_support']}")
    print(f"First Phi3 support primes: {payload['phi3_first_support_primes']}")
    print(f"First Phi6 support primes: {payload['phi6_first_support_primes']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
