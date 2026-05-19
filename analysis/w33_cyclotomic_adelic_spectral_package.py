"""Adelic spectral reciprocity package for the completed cyclotomic defect product."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_adelic_centered_reciprocity,
    completed_defect_adelic_log_artanh,
    completed_defect_adelic_product,
    completed_defect_dirichlet_reciprocity_profile,
    defect_spectral_involution,
    prime_weight,
)


PRIMES = [7, 13, 19]
S_VALUES = [0.5, 1.0]
PROFILE_LIMITS = [31, 1000, 10000, 100000, 1000000]


def build_payload() -> dict[str, object]:
    adelic_samples = {}
    for s in S_VALUES:
        z_by_prime = {p: prime_weight(p, s) for p in PRIMES}
        adelic_samples[str(s)] = {
            "z_by_prime": {str(p): z_by_prime[p].real for p in PRIMES},
            "product_real": completed_defect_adelic_product(z_by_prime).real,
            "product_imag": completed_defect_adelic_product(z_by_prime).imag,
            "log_artanh_real": completed_defect_adelic_log_artanh(z_by_prime).real,
            "log_artanh_imag": completed_defect_adelic_log_artanh(z_by_prime).imag,
            "centered_reciprocity_real": completed_defect_adelic_centered_reciprocity(z_by_prime).real,
            "centered_reciprocity_imag": completed_defect_adelic_centered_reciprocity(z_by_prime).imag,
            "local_spectral_involutions": {
                str(p): {
                    "real": defect_spectral_involution(p, s).real,
                    "imag": defect_spectral_involution(p, s).imag,
                }
                for p in PRIMES
            },
        }

    reciprocity_profile = completed_defect_dirichlet_reciprocity_profile(PROFILE_LIMITS, S_VALUES)
    return {
        "adelic_samples": adelic_samples,
        "reciprocity_profile": reciprocity_profile,
        "summary": {
            "statement": (
                "The completed defect Dirichlet factor is naturally a finite adelic spectral package in the independent local coordinates z_p = p^{-s}. "
                "In those coordinates the exact involution is z_p -> 2-z_p, equivalently u_p=z_p-1 -> -u_p, and the completed product is centered-self-reciprocal coordinatewise. "
                "The one-variable diagonal s restriction inherits only p-local involutions s -> -log_p(2-p^{-s})/log p, so the exact reciprocity is adelic rather than a single global reflection in s."
            ),
            "largest_cutoff_max_local_error": {
                key: rows[-1]["max_abs_local_error_from_one"]
                for key, rows in reciprocity_profile.items()
            },
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_adelic_spectral_package.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = Path("PART_MCII_cyclotomic_adelic_spectral_package_results.json")
    result.write_text(json.dumps(payload["summary"], indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC ADELIC SPECTRAL PACKAGE")
    print("=" * 88)
    for s_key, row in payload["adelic_samples"].items():
        print(f"s={s_key}: reciprocity={row['centered_reciprocity_real']} + {row['centered_reciprocity_imag']}i")
    print(f"wrote {out}")
    print(f"wrote {result}")


if __name__ == "__main__":
    main()
