"""Global perfect-power theorem for Phi3(q) and Phi6(q)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (
    cyclotomic_known_perfect_power_solutions,
    cyclotomic_ljunggren_reduction,
    cyclotomic_perfect_power_scan,
    cyclotomic_perfect_power_theorem,
)



def build_payload() -> dict[str, object]:
    theorem = cyclotomic_perfect_power_theorem()
    scan = cyclotomic_perfect_power_scan(limit_q=100000)
    return {
        "theorem": theorem,
        "reductions": {
            "Phi3_q18": cyclotomic_ljunggren_reduction(18, "Phi3"),
            "Phi6_q19": cyclotomic_ljunggren_reduction(19, "Phi6"),
        },
        "scan": scan,
        "known_solutions": cyclotomic_known_perfect_power_solutions(),
        "summary": {
            "statement": (
                "The cyclotomic perfect-power problem reduces exactly to x^2+3=4y^n via x=2q+1 on Phi3 and x=2q-1 on Phi6. "
                "Invoking the classical Ljunggren theorem leaves only the nontrivial solution (x,y,n)=(37,7,3), which lifts back to Phi3(18)=7^3 and Phi6(19)=7^3."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_perfect_power_theorem.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC PERFECT-POWER THEOREM")
    print("=" * 88)
    print(f"Known solutions: {payload['known_solutions']}")
    print(f"Phi3 q=18 reduction: {payload['reductions']['Phi3_q18']['equation']}")
    print(f"Phi6 q=19 reduction: {payload['reductions']['Phi6_q19']['equation']}")
    print(f"Scan hits: Phi3={payload['scan']['phi3_hits']}, Phi6={payload['scan']['phi6_hits']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
