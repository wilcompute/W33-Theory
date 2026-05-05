#!/usr/bin/env python3
"""
PART CCCXXI - Empirical Targets v1
==================================

Purpose:
    Create the first versioned empirical target file for the W33 program.

Design rule:
    Do not smuggle stale or unverified measured constants into the repo.  Exact
    W33 finite-emulator predictions can be evaluated immediately.  Physical
    Standard Model / CODATA / PDG comparisons must cite a versioned data source
    before residuals are claimed.

What this file provides:
    - A versioned target schema.
    - Exact W33 theory values.
    - M0 finite-emulator targets marked READY.
    - M1/M2 physical targets marked DATA_REQUIRED unless measured values,
      uncertainty, scheme, scale, and source are supplied.
    - Residual machinery for future measured data.
    - No-refit/pass-fail semantics.

The first empirical target categories are:
    M0 finite emulator:
        projective observables = 40
        cluster edges = 240
        full stabilizer weight = 13
        critical edge half = 120
        critical mean degree = 6
        critical degree variance = 3
        critical stabilizer weight = 7
        expected fusion trials = 480
        Clifford resource quotients = [432,216,108,54]

    M1 dimensionless physics / resource:
        sin^2(theta_W)_GUT = 3/8     DATA_REQUIRED for RG comparison
        Koide Q = 2/3                DATA_REQUIRED for mass-scheme comparison
        p_fusion = 1/2               finite resource, READY if experiment supplied
        p_KLM = 1/4                  finite resource, READY if experiment supplied
        Markov contraction = 1/3     finite Markov emulator
        nonreverse probability = 11/12

    M2 dimensionful:
        not evaluated until anchors are fixed.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Optional, Union

ROOT = Path(__file__).resolve().parents[1]

Number = Union[int, float]

# W33 atoms.
q = 3
lam = q - 1
mu = q + 1
V = q**2 * (q**2 + 1)
K = q * (q + 1)
Phi3 = q**2 + q + 1
Phi4 = q**2 + 1
Phi6 = q**2 - q + 1
J = 5
J_inv = 8
H1 = q**4
ALBERT = q**3
E = V * K // 2
DIRECTED = 2 * E
TRIANGLES = V * K * lam // 6
TR_A3 = 6 * TRIANGLES

# Exact values.
PROJECTIVE_OBSERVABLES = (q**4 - 1) // (q - 1)
FULL_STABILIZER_WEIGHT = K + 1
FUSION_P = Fraction(lam, mu)
CRITICAL_EDGE_HALF = FUSION_P * E
CRITICAL_MEAN_DEGREE = FUSION_P * K
CRITICAL_DEGREE_VARIANCE = K * FUSION_P * (1 - FUSION_P)
CRITICAL_STABILIZER_WEIGHT = 1 + CRITICAL_MEAN_DEGREE
EXPECTED_FUSION_TRIALS = E / FUSION_P
CLIFFORD_ORDER = 51840
RESOURCE_LADDER = [E // 2, E, DIRECTED, TR_A3]
CLIFFORD_QUOTIENTS = [CLIFFORD_ORDER // x for x in RESOURCE_LADDER]

SIN2_THETA_W_GUT = Fraction(3, 8)
KOIDE = Fraction(2, 3)
KLM_P = Fraction(1, mu)
MARKOV_CONTRACTION = Fraction(1, q)
NONREVERSE_PROB = Fraction(K - 1, K)
REVERSE_PROB = Fraction(1, K)


@dataclass(frozen=True)
class TargetRecord:
    id: str
    tier: str
    name: str
    theory_value: Union[str, int, float, List[int]]
    theory_formula: str
    measured_value: Optional[Number]
    measurement_uncertainty: Optional[Number]
    scheme: str
    scale: str
    source: str
    status: str
    pass_fail_rule: str
    residual: Optional[float]
    z_score: Optional[float]


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def residual(theory: Number, measured: Optional[Number]) -> Optional[float]:
    if measured is None:
        return None
    return float(measured) - float(theory)


def z_score(theory: Number, measured: Optional[Number], sigma: Optional[Number]) -> Optional[float]:
    if measured is None or sigma is None or sigma == 0:
        return None
    return (float(measured) - float(theory)) / float(sigma)


def make_target(
    *,
    id: str,
    tier: str,
    name: str,
    theory_value: Union[str, int, float, List[int], Fraction],
    theory_formula: str,
    measured_value: Optional[Number] = None,
    measurement_uncertainty: Optional[Number] = None,
    scheme: str = "exact finite theorem",
    scale: str = "scale-free",
    source: str = "W33 exact theorem",
    status: str = "READY_EXACT",
    pass_fail_rule: str = "exact equality for finite emulator, or z-score threshold when measured data are supplied",
) -> TargetRecord:
    display_value: Union[str, int, float, List[int]]
    numeric_theory: Optional[float]
    if isinstance(theory_value, Fraction):
        display_value = frac_str(theory_value)
        numeric_theory = float(theory_value)
    elif isinstance(theory_value, (int, float)):
        display_value = theory_value
        numeric_theory = float(theory_value)
    else:
        display_value = theory_value
        numeric_theory = None

    r = residual(numeric_theory, measured_value) if numeric_theory is not None else None
    z = z_score(numeric_theory, measured_value, measurement_uncertainty) if numeric_theory is not None else None
    return TargetRecord(
        id=id,
        tier=tier,
        name=name,
        theory_value=display_value,
        theory_formula=theory_formula,
        measured_value=measured_value,
        measurement_uncertainty=measurement_uncertainty,
        scheme=scheme,
        scale=scale,
        source=source,
        status=status,
        pass_fail_rule=pass_fail_rule,
        residual=r,
        z_score=z,
    )


def empirical_targets_v1() -> List[TargetRecord]:
    return [
        make_target(
            id="M0_PROJECTIVE_OBSERVABLES",
            tier="M0",
            name="two-qutrit projective observables",
            theory_value=PROJECTIVE_OBSERVABLES,
            theory_formula="(q^4-1)/(q-1)=40",
        ),
        make_target(
            id="M0_CLUSTER_EDGES",
            tier="M0",
            name="W33 graph-state edges",
            theory_value=E,
            theory_formula="E=VK/2=240",
        ),
        make_target(
            id="M0_FULL_STABILIZER_WEIGHT",
            tier="M0",
            name="full W33 graph-state stabilizer weight",
            theory_value=FULL_STABILIZER_WEIGHT,
            theory_formula="K+1=Phi3=13",
        ),
        make_target(
            id="M0_CRITICAL_EDGE_HALF",
            tier="M0",
            name="critical fusion edge half",
            theory_value=int(CRITICAL_EDGE_HALF),
            theory_formula="pE=120 at p=lambda/mu=1/2",
        ),
        make_target(
            id="M0_CRITICAL_MEAN_DEGREE",
            tier="M0",
            name="critical retained mean degree",
            theory_value=int(CRITICAL_MEAN_DEGREE),
            theory_formula="pK=6=2q",
        ),
        make_target(
            id="M0_CRITICAL_DEGREE_VARIANCE",
            tier="M0",
            name="critical retained degree variance",
            theory_value=int(CRITICAL_DEGREE_VARIANCE),
            theory_formula="Kp(1-p)=3=q",
        ),
        make_target(
            id="M0_CRITICAL_STABILIZER_WEIGHT",
            tier="M0",
            name="critical mean stabilizer weight",
            theory_value=int(CRITICAL_STABILIZER_WEIGHT),
            theory_formula="1+pK=7=Phi6",
        ),
        make_target(
            id="M0_EXPECTED_FUSION_TRIALS",
            tier="M0",
            name="expected full W33 fusion trials",
            theory_value=int(EXPECTED_FUSION_TRIALS),
            theory_formula="E/p=480",
        ),
        make_target(
            id="M0_CLIFFORD_RESOURCE_QUOTIENTS",
            tier="M0",
            name="Clifford quotients over resource ladder",
            theory_value=CLIFFORD_QUOTIENTS,
            theory_formula="51840/[120,240,480,960]=[432,216,108,54]",
        ),
        make_target(
            id="M1_SIN2_THETA_W_GUT",
            tier="M1",
            name="GUT-boundary weak mixing angle",
            theory_value=SIN2_THETA_W_GUT,
            theory_formula="sin^2(theta_W)=3/8",
            scheme="requires gauge normalization and RG prescription",
            scale="unification boundary, not fixed in v1",
            source="external PDG/RG data required",
            status="DATA_REQUIRED",
            pass_fail_rule="fix unification scale/RG first, then compare run-down value with measured electroweak value",
        ),
        make_target(
            id="M1_KOIDE_CHARGED_LEPTON",
            tier="M1",
            name="charged-lepton Koide ratio",
            theory_value=KOIDE,
            theory_formula="Q=2/3",
            scheme="requires lepton mass scheme and scale",
            scale="mass-scheme dependent",
            source="external PDG/CODATA data required",
            status="DATA_REQUIRED",
            pass_fail_rule="fix mass scheme/scale first, then compare Q residual with uncertainty",
        ),
        make_target(
            id="M1_FUSION_PROBABILITY",
            tier="M1",
            name="Type-II fusion probability target",
            theory_value=FUSION_P,
            theory_formula="lambda/mu=1/2",
            scheme="specified photonic fusion implementation",
            scale="scale-free laboratory probability",
            source="experimental implementation required",
            status="EXPERIMENT_REQUIRED",
        ),
        make_target(
            id="M1_KLM_PROBABILITY",
            tier="M1",
            name="simplest KLM conditional phase probability target",
            theory_value=KLM_P,
            theory_formula="1/mu=1/4",
            scheme="specified KLM/postselection circuit",
            scale="scale-free laboratory probability",
            source="experimental implementation required",
            status="EXPERIMENT_REQUIRED",
        ),
        make_target(
            id="M1_MARKOV_CONTRACTION",
            tier="M1",
            name="W33 Markov nontrivial contraction",
            theory_value=MARKOV_CONTRACTION,
            theory_formula="SLEM=1/q=1/3",
            scheme="finite W33 Markov walk",
            scale="scale-free",
            source="finite emulator or exact spectrum",
            status="READY_EXACT",
        ),
        make_target(
            id="M1_NONREVERSE_PROBABILITY",
            tier="M1",
            name="ordinary-to-nonbacktracking nonreverse probability",
            theory_value=NONREVERSE_PROB,
            theory_formula="(K-1)/K=11/12",
            scheme="finite W33 random walk after oriented edge",
            scale="scale-free",
            source="finite emulator or exact combinatorics",
            status="READY_EXACT",
        ),
        make_target(
            id="M1_REVERSE_PROBABILITY",
            tier="M1",
            name="ordinary immediate reverse probability",
            theory_value=REVERSE_PROB,
            theory_formula="1/K=1/12",
            scheme="finite W33 random walk after oriented edge",
            scale="scale-free",
            source="finite emulator or exact combinatorics",
            status="READY_EXACT",
        ),
        make_target(
            id="M2_DIMENSIONFUL_ANCHORS",
            tier="M2",
            name="dimensionful observable map",
            theory_value="not evaluated in v1",
            theory_formula="requires hbar, c, and one energy/mass/length anchor",
            scheme="not fixed in v1",
            scale="not fixed in v1",
            source="external physical constants required",
            status="ANCHORS_REQUIRED",
            pass_fail_rule="after anchors are fixed, every non-anchor dimensionful observable is tested without refitting",
        ),
    ]


def targets_summary(targets: List[TargetRecord]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for target in targets:
        out[target.status] = out.get(target.status, 0) + 1
    return out


def empirical_targets_audit() -> Dict[str, object]:
    targets = empirical_targets_v1()
    checks = {
        "w33_atoms": (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480),
        "finite_counts": PROJECTIVE_OBSERVABLES == 40 and FULL_STABILIZER_WEIGHT == 13,
        "critical_values": CRITICAL_EDGE_HALF == 120 and CRITICAL_MEAN_DEGREE == 6 and CRITICAL_DEGREE_VARIANCE == 3 and CRITICAL_STABILIZER_WEIGHT == 7,
        "expected_trials": EXPECTED_FUSION_TRIALS == 480,
        "clifford_quotients": CLIFFORD_QUOTIENTS == [432, 216, 108, 54],
        "dimensionless_targets": SIN2_THETA_W_GUT == Fraction(3, 8) and KOIDE == Fraction(2, 3),
        "resource_probabilities": FUSION_P == Fraction(1, 2) and KLM_P == Fraction(1, 4),
        "walk_probabilities": MARKOV_CONTRACTION == Fraction(1, 3) and NONREVERSE_PROB == Fraction(11, 12) and REVERSE_PROB == Fraction(1, 12),
        "target_count": len(targets) == 17,
        "status_summary": targets_summary(targets) == {"READY_EXACT": 12, "DATA_REQUIRED": 2, "EXPERIMENT_REQUIRED": 2, "ANCHORS_REQUIRED": 1},
        "no_unverified_measured_values": all(t.measured_value is None for t in targets if t.status in {"DATA_REQUIRED", "ANCHORS_REQUIRED"}),
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "schema_version": "empirical_targets_v1",
        "module": "PART_CCCXXI_EMPIRICAL_TARGETS_V1",
        "status": "versioned empirical target file with exact predictions and unresolved external-data slots",
        "data_policy": "No fresh measured constants are inserted without a versioned external source. DATA_REQUIRED targets have no residuals yet.",
        "w33_atoms": {
            "q": q,
            "lambda": lam,
            "mu": mu,
            "V": V,
            "K": K,
            "Phi3": Phi3,
            "Phi4": Phi4,
            "Phi6": Phi6,
            "J": J,
            "J_inverse": J_inv,
            "H1": H1,
            "Albert": ALBERT,
            "E": E,
            "directed": DIRECTED,
            "triangles": TRIANGLES,
            "triangle_trace": TR_A3,
        },
        "targets": [asdict(t) for t in targets],
        "status_summary": targets_summary(targets),
        "residual_policy": {
            "residual": "measured_value - theory_value",
            "z_score": "residual / measurement_uncertainty",
            "rule": "computed only after measured value, uncertainty, scheme, scale, and source are supplied",
        },
        "checks": checks,
        "theorem_statement": (
            "Empirical Targets v1 is the first versioned comparison layer for the W33 program.  It separates exact finite targets from physical "
            "targets requiring external data, locks the residual convention, and prevents unverified constants from being treated as evidence."
        ),
        "honesty_boundary": (
            "This file does not claim agreement with current PDG/CODATA values.  It prepares the exact target schema; measured values must be "
            "added from a cited, versioned source before physical residuals are interpreted."
        ),
    }


def main() -> int:
    audit = empirical_targets_audit()
    out = ROOT / "empirical_targets_v1.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    mirror = ROOT / "PART_CCCXXI_empirical_targets_v1_results.json"
    mirror.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    print(f"Wrote {mirror}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
