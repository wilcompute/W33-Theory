#!/usr/bin/env python3
"""Compile the 40 Witting "quantum cards" to a single-photon four-mode protocol.

The carrier is a single photon in four orthogonal modes, read physically as
path x polarization by the convention
    0=aH, 1=aV, 2=bH, 3=bV.

For every Witting tetrad B=(r0,r1,r2,r3), the analyzer U_B has row j equal
to <r_j|. Therefore
    U_B |r_j> = |j>
and, conversely,
    U_B^dagger |j> = |r_j>.
So the same 40 sparse analyzer unitaries also give 160 exact preparation
programs (40 contexts x 4 slots). Every ray has four preparation programs
because every ray lies in four tetrads.

The finite protocol layer is exact. The loss/visibility rows are a simple
depolarizing four-mode component model, not a QKD security proof.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_witting_card_single_photon_protocol.json"


def rays40():
    w = np.exp(2j * np.pi / 3)
    s3 = np.sqrt(3)
    rays = []
    for i in range(4):
        e = np.zeros(4, dtype=complex)
        e[i] = 1
        rays.append(e)
    for mu, nu in product(range(3), repeat=2):
        rays.append(np.array([0, 1, -(w**mu), w**nu]) / s3)
        rays.append(np.array([1, 0, -(w**mu), -(w**nu)]) / s3)
        rays.append(np.array([1, -(w**mu), 0, w**nu]) / s3)
        rays.append(np.array([1, w**mu, w**nu, 0]) / s3)
    return rays


def tetrads(rays):
    orth = np.abs(np.array(rays).conj() @ np.array(rays).T) < 1e-9
    out = []
    for T in combinations(range(40), 4):
        if all(orth[i, j] for i, j in combinations(T, 2)):
            out.append(T)
    return out, orth


def analyzer(rays, T):
    return np.vstack([np.conjugate(rays[i]) for i in T])


def support_weight(ray):
    return int(np.count_nonzero(np.abs(ray) > 1e-9))


def family(profile):
    p = sorted(profile)
    if p == [1, 1, 1, 1]:
        return "COMPUTATIONAL_DIRECT_RAILS"
    if p == [1, 3, 3, 3]:
        return "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER"
    if p == [3, 3, 3, 3]:
        return "FOUR_THREE_RAIL_WITTING_ROWS"
    raise AssertionError(p)


def component_model(name, eta, visibility):
    """Four-dimensional depolarizing click model for an in-basis card."""
    if not (0 <= eta <= 1 and 0 <= visibility <= 1):
        raise ValueError("eta and visibility must lie in [0,1]")
    p_correct_given_click = (1 + 3 * visibility) / 4
    p_wrong_given_click = 1 - p_correct_given_click
    accepted = 13 / 40
    return {
        "name": name,
        "total_detection_efficiency_eta": eta,
        "depolarizing_visibility": visibility,
        "correct_slot_given_click": p_correct_given_click,
        "wrong_slot_given_click": p_wrong_given_click,
        "compatible_query_acceptance": accepted,
        "accepted_correct_click_per_emitted_photon":
            accepted * eta * p_correct_given_click,
        "accepted_wrong_click_per_emitted_photon":
            accepted * eta * p_wrong_given_click,
    }


def main():
    rays = rays40()
    bases, orth = tetrads(rays)
    I = np.eye(4, dtype=complex)
    prep = []
    memberships = Counter()
    fam = Counter()
    max_analyzer_error = 0.0
    max_prepare_error = 0.0

    for basis_id, T in enumerate(bases):
        U = analyzer(rays, T)
        max_analyzer_error = max(
            max_analyzer_error,
            float(np.max(np.abs(U @ U.conj().T - I))),
        )
        fam[family([support_weight(rays[r]) for r in T])] += 1
        for slot, ray_id in enumerate(T):
            memberships[ray_id] += 1
            rail = I[:, slot]
            prepared = U.conj().T @ rail
            # Projective state error, allowing a global phase.
            phase = np.vdot(rays[ray_id], prepared)
            if abs(phase) > 1e-12:
                prepared = prepared * np.exp(-1j * np.angle(phase))
            err = float(np.max(np.abs(prepared - rays[ray_id])))
            max_prepare_error = max(max_prepare_error, err)
            prep.append({
                "ray": ray_id,
                "basis_id": basis_id,
                "slot": slot,
                "program": "prepare = U_basis^dagger |slot>",
            })

    same = 40
    # Orthogonality excludes the diagonal because <r|r>=1, so this is exactly
    # the 480 ordered distinct orthogonal pairs.
    compatible_distinct = int(orth.sum())
    incompatible = 1600 - same - compatible_distinct

    scenarios = [
        component_model("ideal", 1.00, 1.00),
        component_model("high_visibility", 0.80, 0.99),
        component_model("moderate", 0.50, 0.95),
        component_model("stress", 0.25, 0.90),
    ]

    checks = {
        "forty_rays": len(rays) == 40,
        "forty_tetrads": len(bases) == 40,
        "all_analyzers_unitary": max_analyzer_error < 1e-10,
        "one_hundred_sixty_preparation_programs": len(prep) == 160,
        "every_ray_has_four_preparation_routes":
            set(memberships.values()) == {4} and len(memberships) == 40,
        "all_preparations_recover_target_ray": max_prepare_error < 1e-10,
        "analyzer_family_split_is_1_12_27": dict(fam) == {
            "COMPUTATIONAL_DIRECT_RAILS": 1,
            "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
            "FOUR_THREE_RAIL_WITTING_ROWS": 27,
        },
        "ordered_pair_shell_is_40_480_1080":
            (same, compatible_distinct, incompatible) == (40, 480, 1080),
        "accepted_query_rate_is_13_over_40":
            same + compatible_distinct == 520,
    }

    out = {
        "schema": "w33.witting-card-single-photon-protocol.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "carrier": {
            "hilbert_space": "C^4 = C^2_path tensor C^2_polarization",
            "rail_convention": {
                "0": "|a,H>",
                "1": "|a,V>",
                "2": "|b,H>",
                "3": "|b,V>",
            },
            "boundary": (
                "The rail labeling is a physical convention. The exact theorem is "
                "the four-mode single-photon realization; other two-factor encodings "
                "such as path x OAM are possible implementation choices."
            ),
        },
        "exact_compiler": {
            "rays": 40,
            "tetrads": 40,
            "preparation_programs": 160,
            "preparation_rule": "U_B^dagger |slot> = |Witting ray>",
            "analyzer_rule": "U_B |Witting ray in B> = |detector slot>",
            "analyzer_family_histogram": dict(fam),
            "max_analyzer_unitarity_error": max_analyzer_error,
            "max_preparation_projective_error": max_prepare_error,
            "sample_preparation_programs": prep[:12],
            "all_preparation_programs": prep,
        },
        "vlasov_desk": {
            "ordered_pairs": 1600,
            "same": same,
            "compatible_distinct": compatible_distinct,
            "incompatible": incompatible,
            "accepted_same_or_orthogonal": same + compatible_distinct,
            "accepted_fraction": "13/40",
            "rejected_fraction": "27/40",
        },
        "component_model": {
            "model": (
                "For an in-basis card, rho -> V rho + (1-V) I/4, followed by "
                "a basis-independent total detection efficiency eta."
            ),
            "scenarios": scenarios,
            "what_it_measures": (
                "Correct/wrong accepted click opportunities per emitted photon. "
                "These are component-level rates, not secret-key rates."
            ),
        },
        "prior_art_boundary": {
            "vlasov": (
                "Vlasov 2025 supplies the 40-card delayed-query communication "
                "architecture; the repo supplies the exact 40-ray/tetrad compiler."
            ),
            "hybrid_single_photon_ququart": (
                "Single-photon hybrid-ququart contextuality experiments using two "
                "internal degrees of freedom establish an implementation class, "
                "not a validation of this complete Holonet protocol."
            ),
        },
        "security_boundary": (
            "No eavesdropper model, finite-key analysis, detector-side-channel "
            "model, composable secrecy parameter, or quantum-side-information "
            "min-entropy bound is supplied. The 13/40 rate is a geometric admission "
            "rate, not a secret-key rate."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": out["status"],
        "prep_programs": len(prep),
        "families": dict(fam),
        "accepted_fraction": "13/40",
        "scenarios": scenarios,
    }, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
