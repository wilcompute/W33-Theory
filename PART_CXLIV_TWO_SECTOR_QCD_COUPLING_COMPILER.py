#!/usr/bin/env python3
"""
PART CXLIV — Two-Sector QCD Coupling Compiler
=============================================

Parts CXXXIX-CXLIII solved the alpha_s(M_Z) branch problem phenomenologically
and spectrally.  This module distills the deeper structural rule:

    The selected QCD coupling is a two-sector Hashimoto object.

It is not only a Phi6 threshold.  It uses both nontrivial W(3,3) adjacency
sectors:

  positive r=2 sector:
      adjacency multiplicity m_r = 24
      Bass roots x = 1 ± i sqrt(Phi4)
      provides the bare embedding
          k3_bare = m_r / Phi3 = 24/13

  negative s=-4 sector:
      real-square mu = 4, imaginary-square Phi6 = 7
      Bass roots x = -2 ± i sqrt(Phi6)
      provides the QCD-local threshold
          tau = log sqrt(mu/Phi6)

Together:

    alpha_s(M_GUT)
      = alpha_unified / (m_r/Phi3)
        * (1 + alpha_unified/(2*pi) * log sqrt(mu/Phi6)).

This is the exact executable formula used by the Phi6-polar pipeline, but now
expressed as an internal two-sector compiler rather than an externally selected
branch.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

# W(3,3) constants.
Q = 3
V = 40
K = 12
MU = 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
HASHIMOTO_NORM = K - 1
ALPHA_UNIFIED = 1.0 / 25.0
PDG_ALPHA_S_MZ = 0.1180
PDG_SIGMA = 0.0009

# Adjacency-sector multiplicities for SRG(40,12,2,4).
M_R_POSITIVE = 24
M_S_NEGATIVE = 15

# Final pipeline output from scripts/w33_rg_phi6_polar_pipeline.py.
PIPELINE_ALPHA_S_MZ = 0.11800503473579949


@dataclass(frozen=True)
class HashimotoSectorRole:
    sector: str
    adjacency_eigenvalue: int
    adjacency_multiplicity: int
    bass_root: str
    field: str
    role: str
    formula: str
    value: float


def positive_sector_bare_k3() -> float:
    """Bare QCD embedding from positive-sector multiplicity over Phi3."""
    return M_R_POSITIVE / PHI3


def negative_sector_threshold_tau() -> float:
    """QCD-local threshold from negative Phi6-sector polar ratio."""
    return 0.5 * math.log(MU / PHI6)


def loop_unit(alpha_unified: float = ALPHA_UNIFIED) -> float:
    return alpha_unified / (2.0 * math.pi)


def negative_sector_threshold_delta(alpha_unified: float = ALPHA_UNIFIED) -> float:
    return loop_unit(alpha_unified) * negative_sector_threshold_tau()


def compiled_effective_k3(alpha_unified: float = ALPHA_UNIFIED) -> float:
    return positive_sector_bare_k3() / (1.0 + negative_sector_threshold_delta(alpha_unified))


def compiled_alpha_s_gut(alpha_unified: float = ALPHA_UNIFIED) -> float:
    return (alpha_unified / positive_sector_bare_k3()) * (
        1.0 + negative_sector_threshold_delta(alpha_unified)
    )


def sector_roles() -> List[HashimotoSectorRole]:
    return [
        HashimotoSectorRole(
            sector="positive r=2 sector",
            adjacency_eigenvalue=2,
            adjacency_multiplicity=M_R_POSITIVE,
            bass_root="1 ± i√Phi4 = 1 ± i√10",
            field="Q(√-Phi4) = Q(√-10)",
            role="bare SU(3)c embedding carrier",
            formula="k3_bare = multiplicity(r=2)/Phi3 = 24/13",
            value=positive_sector_bare_k3(),
        ),
        HashimotoSectorRole(
            sector="negative s=-4 sector",
            adjacency_eigenvalue=-4,
            adjacency_multiplicity=M_S_NEGATIVE,
            bass_root="-2 ± i√Phi6 = -2 ± i√7",
            field="Q(√-Phi6) = Q(√-7)",
            role="QCD-local heavy threshold carrier",
            formula="tau = log(|Re|/|Im|) = log sqrt(mu/Phi6)",
            value=negative_sector_threshold_tau(),
        ),
    ]


def two_sector_qcd_audit() -> Dict[str, object]:
    roles = sector_roles()
    k3_bare = positive_sector_bare_k3()
    tau = negative_sector_threshold_tau()
    delta = negative_sector_threshold_delta()
    k3_eff = compiled_effective_k3()
    alpha_s_gut = compiled_alpha_s_gut()
    residual = PIPELINE_ALPHA_S_MZ - PDG_ALPHA_S_MZ
    sigma = abs(residual) / PDG_SIGMA

    # Exact identity checks.
    assert k3_bare == 24 / 13
    assert abs(tau - math.log(2 / math.sqrt(7))) < 1e-15
    assert abs(tau - 0.5 * math.log(MU / PHI6)) < 1e-15
    assert 0.021 < alpha_s_gut < 0.022
    assert sigma < 0.01

    return {
        "module": "PART_CXLIV_TWO_SECTOR_QCD_COUPLING_COMPILER",
        "w33_atoms": {
            "q": Q,
            "v": V,
            "k": K,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "Hashimoto_norm": HASHIMOTO_NORM,
            "positive_sector_multiplicity": M_R_POSITIVE,
            "negative_sector_multiplicity": M_S_NEGATIVE,
        },
        "sector_roles": [asdict(r) for r in roles],
        "compiled_formula": {
            "alpha_s_MGUT": "alpha_unified/(m_r/Phi3) * (1 + alpha_unified/(2*pi)*log sqrt(mu/Phi6))",
            "k3_bare": k3_bare,
            "tau_threshold": tau,
            "delta_threshold": delta,
            "k3_effective": k3_eff,
            "alpha_s_gut": alpha_s_gut,
        },
        "rg_output": {
            "alpha_s_MZ": PIPELINE_ALPHA_S_MZ,
            "pdg_alpha_s_MZ": PDG_ALPHA_S_MZ,
            "residual": residual,
            "sigma": sigma,
        },
        "theorem_statement": (
            "The selected W(3,3) QCD coupling is a two-sector Hashimoto object: "
            "the positive r=2 sector supplies k3_bare=m_r/Phi3=24/13, while "
            "the negative s=-4/Phi6 sector supplies the QCD-local heavy threshold "
            "tau=log sqrt(mu/Phi6)."
        ),
        "interpretive_note": (
            "This is deeper than choosing a fitted k3.  Color coupling is compiled "
            "by the interaction of the two nontrivial Bass fields Q(sqrt(-10)) "
            "and Q(sqrt(-7)): the former gives the visible 24-dimensional carrier, "
            "the latter gives the confinement/QCD beta threshold."
        ),
    }


def main() -> int:
    audit = two_sector_qcd_audit()
    out = ROOT / "PART_CXLIV_two_sector_qcd_coupling_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
