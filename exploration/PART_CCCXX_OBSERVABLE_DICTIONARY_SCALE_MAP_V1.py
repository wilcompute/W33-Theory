#!/usr/bin/env python3
"""
PART CCCXX - Observable Dictionary / Scale Map v1
=================================================

Purpose:
    Take CCCXIX's empirical closure protocol and instantiate the first concrete
    observable dictionary.  This does not pretend that all physical constants
    have already been derived.  Instead it defines the minimal calibration map
    needed for an empirical theory and locks the no-refit rules.

Core principle:
    The finite W33 theorem predicts dimensionless invariants exactly.  Physics
    becomes empirical when those invariants are mapped to observables by a fixed
    dictionary and compared with data without post-hoc refitting.

Scale-map v1 has three levels:

    M0. No-scale finite predictions.
        Direct lab-emulator predictions.  No physical units required.

    M1. Dimensionless physical predictions.
        Compare exact W33 ratios to measured dimensionless observables after a
        specified scale/scheme/RG prescription.

    M2. Dimensionful predictions.
        Require three conversion choices: action unit, speed/causal unit, and
        one energy or length anchor.  All further dimensionful predictions must
        then be locked consequences, not new fits.

No-refit rule:
    Once the dictionary, scale anchors, and RG/continuum rule are fixed, all
    residuals must be evaluated without moving the anchors.

Current exact candidate targets:
    finite resources:
        projective observables = 40
        W33 edges = 240
        stabilizer weight = 13
        critical stabilizer weight = 7
        expected fusion trials = 480

    dimensionless physics candidates:
        sin^2(theta_W)_unification = 3/8
        Koide charged-lepton ratio = 2/3
        p_fusion = 1/2
        p_KLM = 1/4
        Markov nontrivial contraction = 1/q = 1/3
        nonbacktracking nonreverse probability = 11/12

    dimensionful placeholder:
        Need action, speed, and energy/length anchor before making absolute
        mass/length/time predictions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

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
HASHIMOTO_BRANCH = K - 1

# Exact dimensionless targets.
TARGET_SIN2_THETA_W_GUT = Fraction(3, 8)
TARGET_KOIDE = Fraction(2, 3)
TARGET_FUSION = Fraction(lam, mu)
TARGET_KLM = Fraction(1, mu)
TARGET_MARKOV_CONTRACTION = Fraction(1, q)
TARGET_MARKOV_POSITIVE_MODE = Fraction(1, 2 * q)
TARGET_MARKOV_NEGATIVE_MODE = Fraction(-1, q)
TARGET_NONREVERSE_PROB = Fraction(K - 1, K)
TARGET_RETURN_PROB = Fraction(1, K)

# Exact finite-emulator predictions.
PROJECTIVE_OBSERVABLES = (q**4 - 1) // (q - 1)
FULL_STABILIZER_WEIGHT = K + 1
CRITICAL_FUSION_P = Fraction(lam, mu)
CRITICAL_EDGE_HALF = CRITICAL_FUSION_P * E
CRITICAL_MEAN_DEGREE = CRITICAL_FUSION_P * K
CRITICAL_DEGREE_VARIANCE = K * CRITICAL_FUSION_P * (1 - CRITICAL_FUSION_P)
CRITICAL_STABILIZER_WEIGHT = 1 + CRITICAL_MEAN_DEGREE
EXPECTED_FUSION_TRIALS = E / CRITICAL_FUSION_P
CLIFFORD_ORDER = 51840
RESOURCE_LADDER = [E // 2, E, DIRECTED, TR_A3]
CLIFFORD_QUOTIENTS = [CLIFFORD_ORDER // x for x in RESOURCE_LADDER]

# Dimensionful requirements.
REQUIRED_DIMENSIONFUL_ANCHORS = [
    "action_unit_anchor (usually hbar)",
    "causal_speed_anchor (usually c)",
    "one energy/mass/length anchor fixing the remaining unit scale",
]


@dataclass(frozen=True)
class ObservableDictionaryEntry:
    id: str
    level: str
    observable: str
    w33_value: str | int
    formula: str
    required_inputs: str
    comparison_rule: str
    failure_rule: str


@dataclass(frozen=True)
class ScaleMapRule:
    id: str
    statement: str
    reason: str


def observable_dictionary() -> List[ObservableDictionaryEntry]:
    return [
        ObservableDictionaryEntry(
            "M0-FINITE-OBSERVABLES",
            "M0",
            "two-qutrit projective observables",
            PROJECTIVE_OBSERVABLES,
            "(q^4-1)/(q-1)=40",
            "finite qutrit Pauli emulator",
            "construct phase space and verify W33 commutation geometry",
            "count != 40 or commutation graph != W33",
        ),
        ObservableDictionaryEntry(
            "M0-CLUSTER-EDGES",
            "M0",
            "W33 cluster edges",
            E,
            "E=VK/2=240",
            "graph-state implementation of W33",
            "verify 40 vertices, degree 12, 240 edges",
            "edge/degree counts fail",
        ),
        ObservableDictionaryEntry(
            "M0-STABILIZER-WEIGHT",
            "M0",
            "full W33 graph-state stabilizer weight",
            FULL_STABILIZER_WEIGHT,
            "K+1=13=Phi3",
            "W33 graph-state stabilizer measurements",
            "every stabilizer support should have size 13",
            "support size differs from 13",
        ),
        ObservableDictionaryEntry(
            "M0-CRITICAL-STABILIZER",
            "M0",
            "critical percolated stabilizer mean weight",
            str(CRITICAL_STABILIZER_WEIGHT),
            "1+pK=7=Phi6 with p=lambda/mu=1/2",
            "specified independent edge-retention/fusion model",
            "estimate mean support at p=1/2",
            "mean incompatible with 7 under model uncertainties",
        ),
        ObservableDictionaryEntry(
            "M0-FUSION-TRIALS",
            "M0",
            "expected full W33 fusion trials",
            str(EXPECTED_FUSION_TRIALS),
            "E/p=240/(1/2)=480",
            "specified independent Type-II fusion model",
            "estimate mean trials over repeated runs",
            "mean incompatible with 480 under model uncertainties",
        ),
        ObservableDictionaryEntry(
            "M1-WEAK-MIXING-GUT",
            "M1",
            "GUT-boundary weak mixing angle",
            str(TARGET_SIN2_THETA_W_GUT),
            "sin^2(theta_W)=3/8",
            "unification scale, normalization convention, RG equations",
            "run to measured electroweak scale and compare residual",
            "fixed-map residual exceeds declared tolerance",
        ),
        ObservableDictionaryEntry(
            "M1-KOIDE",
            "M1",
            "charged-lepton Koide ratio",
            str(TARGET_KOIDE),
            "Q=2/3",
            "mass scheme, scale, uncertainty model",
            "compute Q from measured lepton masses in fixed scheme",
            "Q incompatible with 2/3 beyond declared tolerance",
        ),
        ObservableDictionaryEntry(
            "M1-MARKOV-CONTRACTION",
            "M1",
            "random-walk nontrivial contraction",
            str(TARGET_MARKOV_CONTRACTION),
            "SLEM=1/q=1/3",
            "finite W33 Markov emulator or physical process mapped to A/K",
            "measure contraction/mixing rate",
            "rate incompatible with 1/3",
        ),
        ObservableDictionaryEntry(
            "M1-NONREVERSE-PROBABILITY",
            "M1",
            "ordinary-to-nonbacktracking transition probability",
            str(TARGET_NONREVERSE_PROB),
            "(K-1)/K=11/12",
            "finite W33 walk emulator",
            "sample next-step nonreverse rate after oriented edge",
            "rate incompatible with 11/12",
        ),
        ObservableDictionaryEntry(
            "M2-DIMENSIONFUL-MAP",
            "M2",
            "absolute masses/lengths/times",
            "not fixed in v1",
            "requires action, speed, and one scale anchor",
            "; ".join(REQUIRED_DIMENSIONFUL_ANCHORS),
            "after anchors are fixed, compute absolute predictions without new fits",
            "post-anchor residuals exceed declared tolerance",
        ),
    ]


def scale_map_rules() -> List[ScaleMapRule]:
    return [
        ScaleMapRule(
            "NO_REFIT",
            "After anchors and RG/continuum rules are fixed, no observable-specific refitting is allowed.",
            "Otherwise the framework can fit anything and predicts nothing.",
        ),
        ScaleMapRule(
            "DIMENSIONLESS_FIRST",
            "Dimensionless ratios must be tested before dimensionful absolute quantities.",
            "Dimensionful claims can hide arbitrary unit choices; dimensionless claims cannot.",
        ),
        ScaleMapRule(
            "ANCHOR_ACCOUNTING",
            "Every fitted anchor consumes one degree of freedom and must be listed separately from predictions.",
            "Predictions are only the quantities not used as anchors.",
        ),
        ScaleMapRule(
            "RG_LOCK",
            "The RG or continuum rule must be specified before comparing with data.",
            "Changing the flow after seeing residuals is refitting.",
        ),
        ScaleMapRule(
            "ERROR_BANDS",
            "Each empirical claim must include measurement uncertainty and theory uncertainty.",
            "A target without tolerance is not a falsifiable prediction.",
        ),
    ]


def scale_map_v1_audit() -> Dict[str, object]:
    checks = {
        "w33_atoms": (q, lam, mu, V, K, E, DIRECTED) == (3, 2, 4, 40, 12, 240, 480),
        "cyclotomic_atoms": (Phi3, Phi4, Phi6, J, J_inv, H1, ALBERT) == (13, 10, 7, 5, 8, 81, 27),
        "projective_observables": PROJECTIVE_OBSERVABLES == V == 40,
        "full_stabilizer_weight": FULL_STABILIZER_WEIGHT == Phi3 == 13,
        "critical_fusion": CRITICAL_FUSION_P == Fraction(1, 2),
        "critical_edge_half": CRITICAL_EDGE_HALF == 120,
        "critical_mean_degree": CRITICAL_MEAN_DEGREE == 2 * q == 6,
        "critical_degree_variance": CRITICAL_DEGREE_VARIANCE == q == 3,
        "critical_stabilizer_weight": CRITICAL_STABILIZER_WEIGHT == Phi6 == 7,
        "expected_fusion_trials": EXPECTED_FUSION_TRIALS == DIRECTED == 480,
        "resource_ladder": RESOURCE_LADDER == [120, 240, 480, 960],
        "clifford_quotients": CLIFFORD_QUOTIENTS == [432, 216, 108, 54],
        "sin2_target": TARGET_SIN2_THETA_W_GUT == Fraction(3, 8),
        "koide_target": TARGET_KOIDE == Fraction(2, 3),
        "fusion_target": TARGET_FUSION == Fraction(1, 2),
        "klm_target": TARGET_KLM == Fraction(1, 4),
        "markov_modes": TARGET_MARKOV_POSITIVE_MODE == Fraction(1, 6) and TARGET_MARKOV_NEGATIVE_MODE == Fraction(-1, 3),
        "nonreverse_return": TARGET_NONREVERSE_PROB == Fraction(11, 12) and TARGET_RETURN_PROB == Fraction(1, 12),
        "dictionary_entries": len(observable_dictionary()) == 10,
        "scale_rules": len(scale_map_rules()) == 5,
        "dimensionful_anchors": len(REQUIRED_DIMENSIONFUL_ANCHORS) == 3,
        "threshold_carrier_inverse": (J * J_inv) % Phi3 == 1,
        "phi6_carrier_step": Phi6 + 1 == J_inv,
    }
    assert all(checks.values())

    return {
        "module": "PART_CCCXX_OBSERVABLE_DICTIONARY_SCALE_MAP_V1",
        "status": "first concrete empirical scale-map candidate with locked dictionary and no-refit rules",
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
        "scale_levels": {
            "M0": "no-scale finite predictions",
            "M1": "dimensionless physical predictions with fixed scale/scheme/RG prescription",
            "M2": "dimensionful predictions after action/speed/energy-or-length anchors",
        },
        "observable_dictionary": [asdict(entry) for entry in observable_dictionary()],
        "scale_map_rules": [asdict(rule) for rule in scale_map_rules()],
        "required_dimensionful_anchors": REQUIRED_DIMENSIONFUL_ANCHORS,
        "exact_targets": {
            "sin2_theta_W_GUT": "3/8",
            "Koide": "2/3",
            "fusion": "1/2",
            "KLM": "1/4",
            "Markov_contraction": "1/3",
            "nonreverse_probability": "11/12",
            "return_probability": "1/12",
        },
        "checks": checks,
        "theorem_statement": (
            "Scale Map v1 turns the W33 finite theorem into an empirical framework by separating no-scale finite predictions, dimensionless "
            "physical predictions, and dimensionful predictions.  It locks an observable dictionary and no-refit rules: after anchors, schemes, "
            "and RG/continuum flow are fixed, all residuals must be evaluated without moving the map."
        ),
        "honesty_boundary": (
            "This is a candidate empirical dictionary, not a completed data fit.  It defines what must be compared and how it can fail. "
            "Measured constants should be supplied by a separate versioned data file before numerical residuals are claimed."
        ),
    }


def main() -> int:
    audit = scale_map_v1_audit()
    out = ROOT / "PART_CCCXX_observable_dictionary_scale_map_v1_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
