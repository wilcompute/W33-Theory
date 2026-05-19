"""Exact local-global valuation criterion for the Eisenstein prime-ideal packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (  # noqa: E402
    eisenstein_local_global_valuation_packet,
    exact_branch_congruence_valuation,
)


SAMPLES = [
    (4, "Phi3"),
    (5, "Phi6"),
    (18, "Phi3"),
    (19, "Phi6"),
]


def build_payload() -> dict[str, object]:
    packet_rows = {
        f"{family}_{q}": eisenstein_local_global_valuation_packet(q, family)
        for q, family in SAMPLES
    }
    local_examples = {
        "Phi3_q18_p7": exact_branch_congruence_valuation(18, 7, "Phi3"),
        "Phi6_q19_p7": exact_branch_congruence_valuation(19, 7, "Phi6"),
        "Phi3_q4_p7": exact_branch_congruence_valuation(4, 7, "Phi3"),
        "Phi6_q5_p7": exact_branch_congruence_valuation(5, 7, "Phi6"),
    }
    return {
        "local_examples": local_examples,
        "packet_rows": packet_rows,
        "summary": {
            "statement": (
                "For a split prime p ≡ 1 mod 3 and the matching branch residue r, the Eisenstein valuation is exact: v_{pi_r}(q-ω)=n iff q ≡ r mod p^n but not mod p^(n+1), and similarly v_{pi_r}(q+ω)=n on the Phi6 branch. "
                "Equivalently, the exact split-prime exponent in Phi3(q) or Phi6(q) is the exact Hensel depth of q on the chosen branch."
            ),
            "all_examples_exact": all(row["all_exact"] for row in packet_rows.values()),
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_eisenstein_local_global_valuation.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = Path("PART_MCIV_eisenstein_local_global_valuation_theorem_results.json")
    result.write_text(json.dumps(payload["summary"], indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) EISENSTEIN LOCAL-GLOBAL VALUATION THEOREM")
    print("=" * 88)
    for name, row in payload["local_examples"].items():
        print(f"{name}: valuation={row['branch_valuation']}, exact={row['exact_criterion_holds']}")
    print(f"wrote {out}")
    print(f"wrote {result}")


if __name__ == "__main__":
    main()
