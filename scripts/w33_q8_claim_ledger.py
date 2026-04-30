"""Generated claim-tier ledger for the Q8 spectral-action surface.

The ledger classifies claims into four tiers:
- exact_finite_theorem
- near_exact_phenomenology
- frontier_conjecture
- conflict

It is derived from the executable Q8 master audit so paper and docs can be
validated against a single source of truth.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

# Allow running as `python scripts/...` from repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.w33_q8_spectral_action_master_audit import q8_spectral_action_master_audit


def _frac_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


@lru_cache(maxsize=1)
def q8_claim_ledger() -> Dict[str, object]:
    """Return the claim-tier ledger anchored to the master audit."""
    audit = q8_spectral_action_master_audit()
    constants = audit["w33_constants"]
    conflicts = audit["boundary_conflicts"]

    alpha_phen_fraction = Fraction(137, 1) + Fraction(880, 24445)
    alpha_int = (constants["k"] - 1) ** 2 + constants["mu"] ** 2

    return {
        "source": "scripts/w33_q8_spectral_action_master_audit.py",
        "version": 1,
        "exact_finite_theorem": [
            {
                "id": "alpha_integer_part_gaussian_norm",
                "claim": "alpha^-1 integer part is fixed by Gaussian norm |(k-1)+i*mu|^2",
                "value": alpha_int,
                "formula": "(k-1)^2 + mu^2",
                "tier_note": "exact finite arithmetic identity",
            },
            {
                "id": "pmns_projective_incidence_packet",
                "claim": "PMNS packet is the promoted incidence-geometry closure",
                "sin2_theta12": "4/13",
                "sin2_theta23": "7/13",
                "sin2_theta13": "2/91",
                "tier_note": "exact finite theorem surface",
            },
            {
                "id": "qcd_beta0_cyclotomic",
                "claim": "QCD one-loop beta coefficient equals Phi6 at q=3",
                "value": audit["spectral_action_arithmetic_packet"]["qcd_beta0_text"],
                "formula": "(11*Nc-2*Nf)/3 with Nc=3,Nf=6",
                "tier_note": "exact finite arithmetic identity",
            },
            {
                "id": "monster_leech_gap",
                "claim": "Monster-Leech arithmetic gap equals mu*q^4",
                "value": audit["monster_leech_packet"]["mckay_minus_leech"],
                "formula": "196884-196560 = mu*q^4",
                "tier_note": "exact finite arithmetic identity",
            },
        ],
        "near_exact_phenomenology": [
            {
                "id": "alpha_table_fraction",
                "claim": "high-precision alpha^-1 table fraction",
                "value_fraction": _frac_text(alpha_phen_fraction),
                "value_decimal_12": f"{float(alpha_phen_fraction):.12f}",
                "tier_note": "phenomenology layer; do not promote to exact theorem",
            }
        ],
        "frontier_conjecture": [
            {
                "id": "global_selector_lift",
                "claim": "global selector/lift law on the fixed W(3,3) carrier remains open",
                "tier_note": "frontier program, not exact closure",
            },
            {
                "id": "late_flavor_atmospheric_corrections",
                "claim": "late flavor atmospheric-angle correction packet remains frontier",
                "tier_note": "bridge-level phenomenology/frontier",
            },
        ],
        "conflict": [
            {
                "id": key,
                "details": value,
            }
            for key, value in conflicts.items()
        ],
        "conflict_count": len(conflicts),
    }


def write_q8_claim_ledger(path: Path) -> Path:
    """Materialize the generated claim ledger as JSON."""
    ledger = q8_claim_ledger()
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    output = write_q8_claim_ledger(Path("w33_q8_claim_ledger.json"))
    print(output)
