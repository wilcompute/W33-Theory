#!/usr/bin/env python3
"""
PART CXLII — Hashimoto Heavy-Spectrum Threshold Derivation
==========================================================

Part CXLI found that the sub-percent GUT thresholds needed to pin the RG
embedding factor are almost exactly square-root logarithms of W(3,3) atoms:

    24/13 branch:  log sqrt(mu/Phi6)
    13/7 branch:   log sqrt((k-1)/q)

This module explains where those square roots come from inside the
Hashimoto/Ihara spectrum itself.

From Part CXXXVIII, the two nontrivial Bass quadratic sectors are

    lambda =  2:  x =  1 ± i sqrt(Phi4) =  1 ± i sqrt(10)
    lambda = -4:  x = -2 ± i sqrt(Phi6) = -2 ± i sqrt(7)

with norm |x|^2 = k-1 = 11.

Therefore:

  1. The negative adjacency / Phi6 sector has real-square 4 = mu and
     imaginary-square 7 = Phi6, so its polar real/imaginary mass ratio is

         |Re x| / |Im x| = 2/sqrt(7) = sqrt(mu/Phi6).

     This is exactly the primitive CXLI threshold on the k3=24/13 branch.

  2. Every Ramanujan root has modulus sqrt(k-1)=sqrt(11).  Comparing this
     shell modulus to the q-clock sqrt(q)=sqrt(3) gives

         |x| / sqrt(q) = sqrt((k-1)/q).

     This is exactly the primitive CXLI threshold on the k3=13/7 branch.

So the CXLI square-root logs are not ad hoc.  They are the two most primitive
mass ratios already present in the field-labeled Hashimoto spectrum:

    polar ratio inside the Phi6 sector,
    radial Ramanujan modulus relative to the q-clock.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from PART_CXXXIX_RG_EMBEDDING_INVERSION import ALPHA_UNIFIED, solve_k3_for_target
from PART_CXL_RG_THRESHOLD_PINNING import delta_gut_for_candidate

ROOT = Path(__file__).resolve().parent

# W(3,3) atoms.
Q = 3
LAMBDA = 2
MU = 4
K = 12
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
HASHIMOTO_NORM = K - 1


@dataclass(frozen=True)
class HashimotoFieldSector:
    label: str
    adjacency_eigenvalue: int
    adjacency_multiplicity: int
    root_label: str
    real_square: int
    imaginary_square: int
    norm_square: int
    field_label: str

    @property
    def real_imag_ratio(self) -> float:
        return math.sqrt(self.real_square / self.imaginary_square)

    @property
    def real_imag_log(self) -> float:
        return math.log(self.real_imag_ratio)

    @property
    def modulus(self) -> float:
        return math.sqrt(self.norm_square)


def hashimoto_field_sectors() -> List[HashimotoFieldSector]:
    """The two nontrivial W(3,3) Hashimoto quadratic sectors."""
    return [
        HashimotoFieldSector(
            label="positive r=2 / Phi4 sector",
            adjacency_eigenvalue=2,
            adjacency_multiplicity=24,
            root_label="1 ± i*sqrt(Phi4) = 1 ± i*sqrt(10)",
            real_square=1,
            imaginary_square=PHI4,
            norm_square=HASHIMOTO_NORM,
            field_label="Q(sqrt(-Phi4)) = Q(sqrt(-10))",
        ),
        HashimotoFieldSector(
            label="negative s=-4 / Phi6 sector",
            adjacency_eigenvalue=-4,
            adjacency_multiplicity=15,
            root_label="-2 ± i*sqrt(Phi6) = -2 ± i*sqrt(7)",
            real_square=MU,
            imaginary_square=PHI6,
            norm_square=HASHIMOTO_NORM,
            field_label="Q(sqrt(-Phi6)) = Q(sqrt(-7))",
        ),
    ]


def loop_unit() -> float:
    return ALPHA_UNIFIED / (2.0 * math.pi)


def effective_k3_from_bare_and_tau(k3_bare: float, tau: float) -> float:
    """Apply delta=(alpha/2pi)*tau to a bare k3 and return effective k3."""
    delta = loop_unit() * tau
    return k3_bare / (1.0 + delta)


@dataclass(frozen=True)
class DerivedThresholdBranch:
    branch_label: str
    bare_k3: float
    tau_source: str
    tau: float
    delta_template: float
    delta_target: float
    effective_k3_template: float
    effective_k3_target: float
    k3_error: float
    relative_k3_error_ppm: float


def branch_from_tau(branch_label: str, bare_k3: float, tau: float, tau_source: str) -> DerivedThresholdBranch:
    k3_eff, _ = solve_k3_for_target()
    delta_template = loop_unit() * tau
    delta_target = delta_gut_for_candidate(bare_k3, k3_eff)
    k3_template = effective_k3_from_bare_and_tau(bare_k3, tau)
    return DerivedThresholdBranch(
        branch_label=branch_label,
        bare_k3=bare_k3,
        tau_source=tau_source,
        tau=tau,
        delta_template=delta_template,
        delta_target=delta_target,
        effective_k3_template=k3_template,
        effective_k3_target=k3_eff,
        k3_error=k3_template - k3_eff,
        relative_k3_error_ppm=(k3_template / k3_eff - 1.0) * 1.0e6,
    )


def derived_threshold_branches() -> List[DerivedThresholdBranch]:
    sectors = {s.label: s for s in hashimoto_field_sectors()}
    phi6_sector = sectors["negative s=-4 / Phi6 sector"]

    tau_phi6_polar = phi6_sector.real_imag_log
    tau_radial_q_clock = math.log(math.sqrt(HASHIMOTO_NORM / Q))

    return [
        branch_from_tau(
            branch_label="24/13 branch from Phi6-sector polar ratio",
            bare_k3=24 / PHI3,
            tau=tau_phi6_polar,
            tau_source="log(|Re(-2+i√7)|/|Im(-2+i√7)|)=log sqrt(mu/Phi6)",
        ),
        branch_from_tau(
            branch_label="13/7 branch from Ramanujan radial/q-clock ratio",
            bare_k3=PHI3 / PHI6,
            tau=tau_radial_q_clock,
            tau_source="log(|mu_Hashimoto|/sqrt(q))=log sqrt((k-1)/q)",
        ),
    ]


def hashimoto_heavy_spectrum_audit() -> Dict[str, object]:
    sectors = hashimoto_field_sectors()
    branches = derived_threshold_branches()
    sectors_by_label = {s.label: s for s in sectors}
    phi6_sector = sectors_by_label["negative s=-4 / Phi6 sector"]

    # Exact structural identities.
    assert phi6_sector.real_square == MU
    assert phi6_sector.imaginary_square == PHI6
    assert phi6_sector.norm_square == HASHIMOTO_NORM
    assert abs(phi6_sector.real_imag_log - math.log(math.sqrt(MU / PHI6))) < 1e-15
    assert abs(math.log(math.sqrt(HASHIMOTO_NORM / Q)) - 0.6496414920651304) < 1e-12

    branch_24, branch_137 = branches
    assert abs(branch_24.relative_k3_error_ppm) < 10.0
    assert abs(branch_137.relative_k3_error_ppm) < 20.0

    return {
        "module": "PART_CXLII_HASHIMOTO_HEAVY_SPECTRUM_DERIVATION",
        "w33_atoms": {
            "q": Q,
            "lambda": LAMBDA,
            "mu": MU,
            "k": K,
            "k_minus_1_hashimoto_norm": HASHIMOTO_NORM,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
        },
        "hashimoto_field_sectors": [asdict(s) | {
            "real_imag_ratio": s.real_imag_ratio,
            "real_imag_log": s.real_imag_log,
            "modulus": s.modulus,
        } for s in sectors],
        "derived_threshold_branches": [asdict(b) for b in branches],
        "exact_derivations": {
            "phi6_polar_ratio": "|Re(-2+i*sqrt(7))|/|Im(-2+i*sqrt(7))| = 2/sqrt(7) = sqrt(mu/Phi6)",
            "ramanujan_q_clock_ratio": "|root|/sqrt(q) = sqrt(k-1)/sqrt(q) = sqrt((k-1)/q)",
            "24_over_13_branch": "k3_bare=24/Phi3, tau=log sqrt(mu/Phi6)",
            "13_over_7_branch": "k3_bare=Phi3/Phi6, tau=log sqrt((k-1)/q)",
        },
        "theorem_statement": (
            "The two primitive heavy-threshold logarithms found in CXLI are "
            "derived directly from the Hashimoto quadratic spectrum: the 24/13 "
            "branch uses the Phi6-sector polar ratio |Re|/|Im|=sqrt(mu/Phi6), "
            "while the 13/7 branch uses the universal Ramanujan modulus divided "
            "by the q-clock, sqrt((k-1)/q)."
        ),
        "interpretive_note": (
            "This upgrades CXLI from a numerical log match to a spectral derivation "
            "of the threshold templates.  The remaining unresolved choice is branch "
            "selection: whether the W(3,3)/E8 heavy spectrum selects the Phi6 polar "
            "threshold with bare k3=24/13 or the radial q-clock threshold with bare "
            "k3=13/7.  Both are ppm-close before any multi-heavy correction."
        ),
    }


def main() -> int:
    audit = hashimoto_heavy_spectrum_audit()
    out = ROOT / "PART_CXLII_hashimoto_heavy_spectrum_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
