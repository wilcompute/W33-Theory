"""Finite-adelic PGF for the W(3,q) cyclotomic valuation packet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (
    finite_adelic_expected_valuation,
    finite_adelic_valuation_euler_factor,
    finite_adelic_valuation_pgf,
    finite_adelic_variance_valuation,
)


def build_payload() -> dict[str, object]:
    packets = {}
    for primes in ([7], [7, 13], [7, 13, 19], [7, 13, 19, 31]):
        key = "x".join(str(p) for p in primes)
        mean = finite_adelic_expected_valuation(primes)
        packets[key] = {
            "split_primes": list(primes),
            "pgf_at_0": finite_adelic_valuation_pgf(primes, 0.0),
            "pgf_at_1": finite_adelic_valuation_pgf(primes, 1.0),
            "euler_factor_s_1": finite_adelic_valuation_euler_factor(primes, 1.0),
            "expected_valuation_fraction": f"{mean.numerator}/{mean.denominator}",
            "expected_valuation": float(mean),
            "variance_fraction": f"{mean.numerator}/{mean.denominator}",
            "variance": float(finite_adelic_variance_valuation(primes)),
        }

    return {
        "packets": packets,
        "summary": {
            "statement": (
                "For any finite set S of split primes p congruent to 1 mod 3, the total valuation packet T_S = sum_{p in S} v_p(Phi3(q)) has exact PGF equal to the product of the local factors G_p(t)=(p-2+t)/(p-t). Equivalently its finite Euler factor is the product of the local Euler factors, and its mean and variance both equal sum_{p in S} 2/(p-1). For the first three split primes 7,13,19 this exact packet mean is 11/18 = 1/3 + 1/6 + 1/9 = 1/q + 1/q! + 1/q^2."
            )
        },
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_finite_adelic_pgf.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC FINITE-ADELIC PGF")
    print("=" * 88)
    for key, packet in payload["packets"].items():
        print(
            f"S={key}: G(0)={packet['pgf_at_0']}, G(1)={packet['pgf_at_1']}, "
            f"E[T]={packet['expected_valuation_fraction']}, Var(T)={packet['variance_fraction']}, "
            f"Euler(s=1)={packet['euler_factor_s_1']}"
        )
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()