"""Finite-cutoff CRT factorization for the W(3,q) cyclotomic defect branches."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import finite_cutoff_avoidance_density, finite_cutoff_branch_classes, finite_cutoff_defect_density


def build_payload() -> dict[str, object]:
    packets = {}
    for prime_list in ([7], [7, 13], [7, 13, 19]):
        key = "x".join(str(p) for p in prime_list)
        phi3 = finite_cutoff_branch_classes(prime_list, family="Phi3", power=2)
        phi6 = finite_cutoff_branch_classes(prime_list, family="Phi6", power=2)
        packets[key] = {
            "phi3": phi3,
            "phi6": phi6,
            "simultaneous_density": finite_cutoff_defect_density(prime_list, power=2),
            "avoidance_density": finite_cutoff_avoidance_density(prime_list, power=2),
            "union_density": 1 - finite_cutoff_avoidance_density(prime_list, power=2),
        }

    return {
        "packets": packets,
        "summary": {
            "statement": (
                "For any finite set S of split primes p congruent to 1 mod 3, the cyclotomic defect branches factor exactly by the Chinese remainder theorem. At square depth p^2 each prime contributes two local branches, so the simultaneous branch count is exactly 2^|S| modulo M_S=product p^2. The simultaneous density is product 2/p^2, the avoidance density is product (1-2/p^2), and the union density is 1 minus that product."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_crt_branch_factorization.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC CRT BRANCH FACTORIZATION")
    print("=" * 88)
    for key, packet in payload["packets"].items():
        print(f"S={key}")
        print(f"  Phi3 classes: {packet['phi3']['classes']}")
        print(f"  Phi6 classes: {packet['phi6']['classes']}")
        print(f"  class count: {packet['phi3']['class_count']} | modulus: {packet['phi3']['modulus']}")
        print(f"  simultaneous density: {packet['simultaneous_density']}")
        print(f"  avoidance density: {packet['avoidance_density']}")
        print(f"  union density: {packet['union_density']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()