#!/usr/bin/env python3
"""Numerical routed-exposure noise experiment for the W33 [[20,7,2]]_3 adapter.

This is deliberately a pseudothreshold experiment, not a physical FT threshold.
The topological route compiler supplies an exact local-operation exposure count
E_i for each of the first twenty input qutrits.  A stated phenomenological model
then assigns independent nontrivial qutrit-Pauli probability

    p_i = 1 - (1-p_gate)^E_i

to external coordinate i, uniformly over the eight nonidentity X^a Z^b Paulis.

For every p_gate on a deterministic grid we evaluate weight 0 and 1 exactly,
and exhaustively classify all C(20,2)*8^2 = 12160 weight-2 Pauli patterns by the
mapped [[20,7,2]]_3 syndrome and logical quotient.  The entire probability mass
of weight >=3 is retained as an adversarial uncertainty envelope.  Therefore,
inside this explicit independent-exposure model, the reported lower/upper
logical-error interval does not hide unenumerated higher-weight faults.

The experiment can demonstrate whether the CURRENT non-FT routed encoder has a
pseudothreshold under this model.  It cannot establish a hardware threshold:
correlated optical faults, loss, ancilla/readout noise, leakage, decoder timing,
and fault spread are not calibrated here.
"""
from __future__ import annotations

import json
import math

import numpy as np

import w33_qutrit_20_7_2_packet_decoder as dec
import w33_qutrit_20_7_2_w33_route_compiler as route

P_GRID = [
    1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6,
    1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2,
]


def pair_classification(Hx, Hz):
    pairs = {}
    total = 0
    malignant_total = 0
    benign_total = 0
    for i in range(20):
        for j in range(i + 1, 20):
            malignant = benign = detected = 0
            for ai in range(3):
                for bi in range(3):
                    if ai == 0 and bi == 0:
                        continue
                    for aj in range(3):
                        for bj in range(3):
                            if aj == 0 and bj == 0:
                                continue
                            x = np.zeros(20, dtype=np.int64); z = np.zeros(20, dtype=np.int64)
                            x[i] = ai; z[i] = bi; x[j] = aj; z[j] = bj
                            s = dec.syndrome(Hx, Hz, x, z)
                            if any(s):
                                detected += 1
                            elif dec.logical_trivial(Hx, Hz, x, z):
                                benign += 1
                            else:
                                malignant += 1
            if malignant + benign + detected != 64:
                raise RuntimeError("weight-2 classification lost Pauli cases")
            pairs[(i, j)] = {"malignant": malignant, "benign_zero": benign, "detected": detected}
            total += 64
            malignant_total += malignant
            benign_total += benign
    if total != math.comb(20, 2) * 64:
        raise RuntimeError("did not enumerate all weight-2 Pauli patterns")
    return pairs, malignant_total, benign_total


def exact_weight012_bounds(p_gate, exposures, pairs):
    p = [1.0 - (1.0 - float(p_gate)) ** int(max(1, e)) for e in exposures]
    q = [1.0 - x for x in p]
    P0 = math.prod(q)
    P1 = 0.0
    for i in range(20):
        rest = math.prod(q[k] for k in range(20) if k != i)
        P1 += p[i] * rest
    P2 = 0.0
    malignant2 = 0.0
    benign2 = 0.0
    detected2 = 0.0
    for (i, j), cls in pairs.items():
        rest = math.prod(q[k] for k in range(20) if k != i and k != j)
        pair_mass = p[i] * p[j] * rest
        P2 += pair_mass
        malignant2 += pair_mass * cls["malignant"] / 64.0
        benign2 += pair_mass * cls["benign_zero"] / 64.0
        detected2 += pair_mass * cls["detected"] / 64.0
    Pge3 = max(0.0, min(1.0, 1.0 - P0 - P1 - P2))
    accepted_known = P0 + malignant2 + benign2
    logical_lower = malignant2
    logical_upper = min(1.0, malignant2 + Pge3)
    acceptance_lower = accepted_known
    acceptance_upper = min(1.0, accepted_known + Pge3)
    cond_lower = logical_lower / acceptance_upper if acceptance_upper > 0 else 1.0
    cond_upper = logical_upper / acceptance_lower if acceptance_lower > 0 else 1.0
    per_logical_lower = cond_lower / 7.0
    per_logical_upper = min(1.0, cond_upper / 7.0)
    return {
        "p_gate": float(p_gate),
        "max_effective_coordinate_p": float(max(p)),
        "mean_effective_coordinate_p": float(sum(p) / len(p)),
        "weight0": float(P0), "weight1": float(P1), "weight2": float(P2), "weight_ge3": float(Pge3),
        "weight2_detected": float(detected2), "weight2_benign_zero": float(benign2), "weight2_logical": float(malignant2),
        "acceptance_lower": float(acceptance_lower), "acceptance_upper": float(acceptance_upper),
        "conditional_logical_lower": float(cond_lower), "conditional_logical_upper": float(cond_upper),
        "per_logical_qutrit_lower": float(per_logical_lower), "per_logical_qutrit_upper": float(per_logical_upper),
        "certified_below_bare_p": bool(per_logical_upper < float(p_gate)),
    }


def asymptotic_coefficient(exposures, pairs):
    # p_i = E_i p + O(p^2).  Weight-2 malignant mass therefore has coefficient
    # sum E_i E_j malignant_ij/64 at order p^2.
    C = 0.0
    for (i, j), cls in pairs.items():
        C += max(1, exposures[i]) * max(1, exposures[j]) * cls["malignant"] / 64.0
    per_logical_C = C / 7.0
    pstar = (1.0 / per_logical_C) if per_logical_C > 0 else None
    return float(C), float(per_logical_C), (float(pstar) if pstar is not None else None)


def verify(candidate_count=route.multi.DEFAULT_CANDIDATES):
    H, Hx, Hz = dec.code_matrices()
    routed = route.compile_routes(int(candidate_count))
    exposures = [max(1, int(x)) for x in routed["metrics"]["logical_input_exposure_first20"]]
    pairs, malignant_patterns, benign_patterns = pair_classification(Hx, Hz)
    grid = [exact_weight012_bounds(p, exposures, pairs) for p in P_GRID]
    C, C7, pstar = asymptotic_coefficient(exposures, pairs)

    certified = [x["p_gate"] for x in grid if x["certified_below_bare_p"]]
    uncertified = [x["p_gate"] for x in grid if not x["certified_below_bare_p"]]
    bracket = None
    if certified and uncertified:
        low_candidates = [x for x in certified if x < min(uncertified)]
        if low_candidates:
            lo = max(low_candidates)
            hi = min(x for x in uncertified if x > lo)
            bracket = [float(lo), float(hi)]
    elif certified:
        bracket = [float(max(certified)), None]
    else:
        bracket = [None, float(min(uncertified))] if uncertified else None

    checks = {
        "route_exposure_has_20_inputs": len(exposures) == 20 and all(x >= 1 for x in exposures),
        "all_12160_weight2_paulis_enumerated": sum(sum(v.values()) for v in pairs.values()) == math.comb(20, 2) * 64,
        "distance2_has_malignant_weight2_patterns": malignant_patterns > 0,
        "weight1_is_detected_by_decoder_certificate": dec.verify(int(candidate_count))["checks"]["all_160_nontrivial_single_paulis_detected"],
        "probability_bounds_are_ordered": all(0 <= x["conditional_logical_lower"] <= x["conditional_logical_upper"] <= 1 for x in grid),
        "higher_weight_mass_is_never_dropped": all(x["weight0"] + x["weight1"] + x["weight2"] + x["weight_ge3"] >= 1 - 1e-12 for x in grid),
    }
    checks = {k: bool(v) for k, v in checks.items()}
    return {
        "schema": "w33.qutrit-20-7-2-routed-exposure-pseudothreshold.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "noise_model": {
            "type": "independent external qutrit depolarizing exposure derived from routed local-op counts",
            "coordinate_rule": "p_i=1-(1-p_gate)^E_i; nonidentity X^a Z^b uniform over 8 choices",
            "logical_input_exposure_first20": exposures,
            "measurement_noise": "not included",
            "correlations": "not included",
        },
        "weight2_exact": {
            "patterns": math.comb(20, 2) * 64,
            "malignant_logical_patterns": int(malignant_patterns),
            "benign_zero_syndrome_patterns": int(benign_patterns),
            "malignant_fraction": float(malignant_patterns / (math.comb(20, 2) * 64)),
        },
        "asymptotic": {
            "block_logical_p2_coefficient": C,
            "per_logical_qutrit_p2_coefficient": C7,
            "leading_order_pseudothreshold_estimate": pstar,
        },
        "grid": grid,
        "certified_grid_crossing_bracket": bracket,
        "interpretation": "Within the stated independent exposure model, weight-0/1/2 behavior is exact and all weight>=3 probability is adversarially retained. A grid point is called certified-below-bare-p only when even the worst-case higher-weight upper bound lies below p_gate per logical qutrit.",
        "boundary": "This is a numerical pseudothreshold experiment tied to the topological routed circuit, not a physical fault-tolerance threshold. It omits correlated optical errors, loss/leakage, syndrome measurement faults, calibrated gate infidelity, and decoder latency; those omissions prevent FT admission.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
