#!/usr/bin/env python3
"""Pass 391: out-of-sample physics prediction registry.

The registry makes retrospective numerology ineligible for prospective credit,
requires a frozen selection rule and uncertainty model, and demands an explicit
null-comparator family before any future data are opened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_ENTRY_FIELDS = {
    "id",
    "claim",
    "status",
    "eligibility",
    "observable",
    "selection_rule",
    "data_freeze",
    "uncertainty_propagation",
    "null_comparator_family",
    "multiplicity_control",
    "tuning_policy",
    "decision_rule",
}


def sha256_payload(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_registry() -> dict[str, Any]:
    entries: list[dict[str, Any]] = [
        {
            "id": "PHOTONIC-CHOI-001",
            "claim": "A calibrated single-qutrit gate module yields Choi fringe visibilities V(I)=1, V(X)=0, V(Z)=0, V(F3)=1/3.",
            "status": "preregistered_not_physically_run",
            "eligibility": "prospective",
            "observable": {
                "vector": ["V(I)", "V(X)", "V(Z)", "V(F3)"],
                "target": [1.0, 0.0, 0.0, 1.0 / 3.0],
                "units": "dimensionless",
            },
            "selection_rule": (
                "Use the four named gates and four phase settings fixed in "
                "analysis/w33_pass390_blinded_choi_visibility_dry_run.py; no gate "
                "may be dropped after counts are opened."
            ),
            "data_freeze": (
                "The first timestamped laboratory raw-count export produced after "
                "this registry commit, with its separately timestamped blind key "
                "and calibration run."
            ),
            "uncertainty_propagation": (
                "Replicate-level signed cosine visibility, calibration dilution "
                "propagated multiplicatively, 95% interval from independent "
                "replicate standard error; publish raw counts and calibration."
            ),
            "null_comparator_family": (
                "Gate-independent visibility; unconstrained four-visibility model; "
                "depolarizing channel with one fitted strength; phase-drift model."
            ),
            "multiplicity_control": (
                "One four-component family; simultaneous Holm correction for the "
                "four target residual tests."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "Pass only if every target is inside its corrected 95% interval "
                "and the preregistered residual tolerances are met; otherwise fail."
            ),
            "observed_value": None,
            "notes": (
                "Pass 390 is only a synthetic pipeline dry run and supplies no "
                "physical evidence."
            ),
        },
        {
            "id": "ALPHA-STATIC-001",
            "claim": "The finite-geometry expression reproduces alpha^{-1}(0) near 137.036.",
            "status": "retrospective_target_used",
            "eligibility": "ineligible_for_out_of_sample_credit",
            "observable": {
                "name": "inverse fine-structure constant at zero momentum",
                "target_source": "already known before formula selection",
            },
            "selection_rule": (
                "No retrospective version is eligible. A future test must freeze "
                "an independently derived running prescription and predict alpha(Q) "
                "at named Q values not used anywhere in construction."
            ),
            "data_freeze": (
                "A future precision release at preregistered momentum-transfer "
                "points, selected before inspecting the release."
            ),
            "uncertainty_propagation": (
                "Full experimental covariance plus theory uncertainty from the "
                "fixed running map and threshold inputs."
            ),
            "null_comparator_family": (
                "Standard QED/SM running; low-complexity rational approximants with "
                "the same number of fitted constants; constant-offset model."
            ),
            "multiplicity_control": (
                "All momentum points treated as one correlated vector; no choosing "
                "the best Q after release."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "Only a prediction fixed before the holdout release can receive "
                "prospective status; the alpha(0) match remains retrospective."
            ),
            "observed_value": "known_target_contaminated",
        },
        {
            "id": "WEAK-GUT-001",
            "claim": "sin^2(theta_W)=3/8 at a unification boundary.",
            "status": "conditional_benchmark_not_unique_prediction",
            "eligibility": "prospective_only_after_scale_and_threshold_freeze",
            "observable": {
                "name": "running weak mixing angle",
                "target": 3.0 / 8.0,
                "scale": "must be fixed numerically before data comparison",
            },
            "selection_rule": (
                "Freeze the renormalization scheme, unification scale, particle "
                "content, and threshold corrections before evaluating the target."
            ),
            "data_freeze": (
                "The next designated global electroweak-coupling fit after all "
                "model ingredients and the scale are committed."
            ),
            "uncertainty_propagation": (
                "Run the published covariance of gauge couplings through the fixed "
                "RG equations and frozen threshold model."
            ),
            "null_comparator_family": (
                "SU(5)-type 3/8 boundary; generic one-scale unification; no-unification "
                "SM running; threshold-expanded alternatives with equal parameter count."
            ),
            "multiplicity_control": (
                "Count every tried scale, threshold spectrum, and normalization as "
                "a separate model in the family."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "The value 3/8 alone is not discriminating; support requires a "
                "pre-frozen scale and thresholds outperforming the null family."
            ),
            "observed_value": None,
        },
        {
            "id": "WEAK-EW-001",
            "claim": "sin^2(theta_W)=3/13 at an electroweak reference scale.",
            "status": "retrospective_empirical_formula",
            "eligibility": "ineligible_until_scale_is_frozen_prospectively",
            "observable": {
                "name": "scheme-specific weak mixing angle",
                "target": 3.0 / 13.0,
            },
            "selection_rule": (
                "Freeze one named renormalization scheme and one numerical scale; "
                "do not choose the scale where the running curve crosses 3/13."
            ),
            "data_freeze": (
                "The next independent electroweak global fit after scheme and scale "
                "are committed."
            ),
            "uncertainty_propagation": (
                "Use the fit covariance and fixed RG transport; include scheme and "
                "threshold uncertainties without refitting the target."
            ),
            "null_comparator_family": (
                "All reduced rationals a/b with 1<=a<b<=20, plus standard SM running "
                "without a rational target."
            ),
            "multiplicity_control": (
                "Correct over the complete rational family and every previously "
                "considered scale."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "A crossing located after looking at the running curve is a fit, "
                "not a prediction."
            ),
            "observed_value": "previously_compared",
        },
        {
            "id": "MIXING-ANGLES-001",
            "claim": "The proposed CKM/PMNS rational-radical angle formulas predict future global-fit central values.",
            "status": "retrospective_formula_family",
            "eligibility": "future_holdout_only",
            "observable": {
                "vector": [
                    "|V_us|",
                    "sin^2(theta12)",
                    "sin^2(theta23)",
                    "sin^2(theta13)",
                ],
                "targets": [
                    "3/sqrt(178)",
                    "4/13",
                    "7/13",
                    "2/91",
                ],
            },
            "selection_rule": (
                "Freeze this exact four-component vector, parameter conventions, "
                "mass ordering, and octant; no component replacement after release."
            ),
            "data_freeze": (
                "One named future CKM/PMNS global-fit release not used in deriving "
                "or selecting any formula."
            ),
            "uncertainty_propagation": (
                "Use the published full covariance matrix; compare the complete "
                "residual vector with a chi-square or likelihood ratio."
            ),
            "null_comparator_family": (
                "Independent free angles; low-denominator rational/radical formulas "
                "enumerated before the release; previous-fit persistence model."
            ),
            "multiplicity_control": (
                "Familywise correction across every formula present in the repository "
                "before the freeze, not only the four retained formulas."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "Evaluate the full vector. A subset match or post-release octant "
                "choice is a failure."
            ),
            "observed_value": "historical_data_influenced_selection",
        },
        {
            "id": "MASS-KOIDE-001",
            "claim": "Mass relations retained in the papers predict future renormalized mass updates.",
            "status": "retrospective_relation",
            "eligibility": "future_holdout_only",
            "observable": {
                "name": "frozen vector of named running masses and derived ratios",
                "renormalization_scheme": "must be fixed before release",
            },
            "selection_rule": (
                "List every included particle, scale, scheme, and exact algebraic "
                "relation before the holdout update."
            ),
            "data_freeze": (
                "The next designated independent mass evaluation after the registry "
                "entry is fully specified."
            ),
            "uncertainty_propagation": (
                "Monte Carlo or linear covariance propagation from the published "
                "mass covariance, with scale and scheme uncertainties included."
            ),
            "null_comparator_family": (
                "No-relation free masses; generic symmetric quadratic relations; "
                "all low-complexity relations searched in the historical corpus."
            ),
            "multiplicity_control": (
                "Description-length or explicit familywise correction over the full "
                "searched relation class."
            ),
            "tuning_policy": "none_after_freeze",
            "decision_rule": (
                "No credit for a relation chosen after inspecting the same mass table."
            ),
            "observed_value": "historical_data_influenced_selection",
        },
    ]

    registry: dict[str, Any] = {
        "pass": 391,
        "title": "W33 out-of-sample physics prediction registry",
        "version": 1,
        "frozen_date": "2026-07-17",
        "rules": {
            "selection_before_data": True,
            "raw_data_and_covariance_required": True,
            "null_family_required": True,
            "all_tried_formulas_count_toward_multiplicity": True,
            "no_post_hoc_formula_tuning": True,
            "retrospective_matches_receive_no_prospective_credit": True,
        },
        "entries": entries,
    }
    registry["registry_sha256"] = sha256_payload(registry)
    return registry


def validate_registry(registry: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    ids: set[str] = set()
    for entry in registry.get("entries", []):
        missing = REQUIRED_ENTRY_FIELDS.difference(entry)
        if missing:
            errors.append(f"{entry.get('id', '<unknown>')}: missing {sorted(missing)}")
        entry_id = entry.get("id")
        if entry_id in ids:
            errors.append(f"duplicate id: {entry_id}")
        ids.add(entry_id)
        if entry.get("tuning_policy") != "none_after_freeze":
            errors.append(f"{entry_id}: tuning policy is not frozen")
        if not entry.get("null_comparator_family"):
            errors.append(f"{entry_id}: missing null family")
        if entry.get("eligibility") == "prospective" and entry.get("observed_value") is not None:
            errors.append(f"{entry_id}: prospective entry contains an observed value")
        if entry.get("status") == "preregistered_not_physically_run" and entry.get("observed_value") is not None:
            errors.append(f"{entry_id}: preregistered entry is contaminated")
    return {
        "verified": not errors,
        "entry_count": len(registry.get("entries", [])),
        "prospective_entry_count": sum(
            entry.get("eligibility") == "prospective"
            for entry in registry.get("entries", [])
        ),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/w33_prediction_registry_v1.json"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    registry = build_registry()
    validation = validate_registry(registry)
    registry["validation"] = validation
    text = json.dumps(registry, indent=2, sort_keys=True) + "\n"

    if not validation["verified"]:
        raise SystemExit("\n".join(validation["errors"]))
    if args.check:
        if json.loads(args.output.read_text(encoding="utf-8")) != registry:
            raise SystemExit("Pass 391 registry drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")

    print(json.dumps(validation, sort_keys=True))


if __name__ == "__main__":
    main()
