"""Residue-class classifier for the W(3,q) cyclotomic defect locus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (
    cyclotomic_perfect_power_scan,
    defect_density_partial_product,
    defect_residue_classifier,
    empirical_defect_density,
)


def main() -> None:
    payload = defect_residue_classifier(limit_q=1000, prime_limit=200)
    payload["perfect_power_scan"] = cyclotomic_perfect_power_scan(limit_q=100000)
    payload["density_estimate"] = defect_density_partial_product(prime_limit=200000)
    payload["empirical_density"] = empirical_defect_density(limit_q=20000)
    out = Path("data") / "w33_cyclotomic_defect_residue_classifier.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 88)
    print("W(3,q) CYCLOTOMIC DEFECT RESIDUE CLASSIFIER")
    print("=" * 88)
    print(f"q <= {payload['limit_q']} | split primes <= {payload['prime_limit']}")
    print(f"exact classifier: {payload['exact_classifier']}")
    print("\nFirst split-prime residue classes:")
    for p in payload["split_primes"][:8]:
        row = payload["residue_table"][str(p)]
        print(
            f"  p={p}: order-3 units mod p^2 = {row['order3_units']} | "
            f"Phi3 roots mod p^2 = {row['Phi3']} | Phi6 roots mod p^2 = {row['Phi6']}"
        )
    print("\nFirst Phi3 failures:")
    for row in payload["phi3_failures"][:8]:
        print(f"  q={row['q']}: p={row.get('prime')} residues={row.get('residues_mod_p2')} value={row['value']}")
    print("\nFirst Phi6 failures:")
    for row in payload["phi6_failures"][:8]:
        print(f"  q={row['q']}: p={row.get('prime')} residues={row.get('residues_mod_p2')} value={row['value']}")
    print("\nCube-root restatement:")
    print(f"  {payload['cube_root_restatement']}")
    print("\nPerfect-power scan:")
    print(f"  Phi3 hits: {payload['perfect_power_scan']['phi3_hits']}")
    print(f"  Phi6 hits: {payload['perfect_power_scan']['phi6_hits']}")
    print("\nDefect density:")
    print(f"  Euler-product estimate: {payload['density_estimate']['defect_density_estimate']}")
    print(f"  Empirical Phi3 density on q<=20000: {payload['empirical_density']['phi3_density']}")
    print(f"  Empirical Phi6 density on q<=20000: {payload['empirical_density']['phi6_density']}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()