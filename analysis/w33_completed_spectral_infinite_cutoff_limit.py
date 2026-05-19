"""Infinite-cutoff odd Taylor limit for the completed defect spectral L-family."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import completed_defect_spectral_infinite_cutoff_profile


def main() -> None:
    prime_limits = [1000, 10000, 100000, 1000000]
    s_values = [0.5, 1.0, 2.0]
    odd_orders = [1, 3, 5, 7]
    payload = {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "odd_orders": odd_orders,
        "profile": completed_defect_spectral_infinite_cutoff_profile(prime_limits, s_values, odd_orders),
    }

    data_path = Path("data") / "w33_completed_spectral_infinite_cutoff_limit.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result_path = Path("PART_MCVII_completed_spectral_infinite_cutoff_limit_results.json")
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Completed spectral infinite-cutoff limit profile generated.")
    sample = payload["profile"]["1.0"]["1"][-1]
    print(
        "s=1.0, order=1, prime_limit="
        f"{sample['prime_limit']}, coefficient={sample['coefficient_real']} + {sample['coefficient_imag']}i, "
        f"tail_bound={sample['tail_bound']}"
    )


if __name__ == "__main__":
    main()
