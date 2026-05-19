"""p-adic valuation-tree audit for the W(3,q) cyclotomic defect locus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.arithmetic import prime_factorization
from w33.cyclotomic import phi3_value, phi6_value, valuation_tree


def p_adic_valuation(n: int, p: int) -> int:
    v = 0
    while n % p == 0 and n > 0:
        n //= p
        v += 1
    return v


def build_payload() -> dict[str, object]:
    split_primes = [7, 13, 19]
    trees = {str(p): valuation_tree(p, max_power=5) for p in split_primes}

    heawood_cube = {
        "phi3": {
            "q": 18,
            "value": phi3_value(18),
            "valuation_at_7": p_adic_valuation(phi3_value(18), 7),
            "factorization": prime_factorization(phi3_value(18)),
        },
        "phi6": {
            "q": 19,
            "value": phi6_value(19),
            "valuation_at_7": p_adic_valuation(phi6_value(19), 7),
            "factorization": prime_factorization(phi6_value(19)),
        },
    }

    return {
        "split_primes": split_primes,
        "trees": trees,
        "heawood_cube_depth_three": heawood_cube,
        "summary": {
            "statement": (
                "For each split prime p congruent to 1 mod 3, the cyclotomic defect locus forms two infinite Hensel branches modulo p^n. The p-adic measure of q with v_p(Phi3(q)) >= n (and likewise for Phi6) is exactly 2/p^n, so the exact valuation law is geometric: P(v_p = n) = 2(p-1)/p^(n+1). The first visible depth-3 node is the Heawood cube Phi3(18)=Phi6(19)=7^3."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_valuation_tree.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC p-ADIC VALUATION TREE")
    print("=" * 88)
    for p in payload["split_primes"]:
        tree = payload["trees"][str(p)]
        print(f"p={p}")
        print(f"  Phi3 roots mod p^1..p^5: {tree['phi3_roots']}")
        print(f"  Phi6 roots mod p^1..p^5: {tree['phi6_roots']}")
        print(f"  density v_p>=n: {tree['density_at_least']}")
        print(f"  density v_p=n: {tree['density_exact']}")
    cube = payload["heawood_cube_depth_three"]
    print("\nHeawood cube depth-3 node:")
    print(f"  Phi3: {cube['phi3']}")
    print(f"  Phi6: {cube['phi6']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()