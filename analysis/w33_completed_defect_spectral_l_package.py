"""Completed defect spectral L-family package for the split-prime cyclotomic tower."""

from __future__ import annotations

import json
from pathlib import Path

from w33.cyclotomic import completed_defect_spectral_profile


def main() -> None:
    prime_limits = [31, 1000, 10000, 100000]
    s_values = [0.5, 1.0, 2.0]
    deformations = [0.25, 0.5, 1.0]
    payload = {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "profile": completed_defect_spectral_profile(prime_limits, s_values, deformations),
    }

    data_path = Path("data") / "w33_completed_defect_spectral_l_package.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result_path = Path("PART_MCV_completed_defect_spectral_l_package_results.json")
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Completed defect spectral L-package generated.")
    sample = payload["profile"]["1.0"]["1.0"][-1]
    print(f"s=1.0, deformation=1.0, prime_limit={sample['prime_limit']}, value={sample['value_real']} + {sample['value_imag']}i")
    print(f"Reciprocity error: {sample['abs_reciprocity_error']}")


if __name__ == "__main__":
    main()
