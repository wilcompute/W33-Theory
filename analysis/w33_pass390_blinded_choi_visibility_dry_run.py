#!/usr/bin/env python3
"""Pass 390: blinded photonic Choi-visibility protocol dry run.

This is an executable synthetic dry run, not physical laboratory data.
It freezes V(I)=1, V(X)=0, V(Z)=0, V(F3)=1/3, randomizes hidden gate
labels, emits raw two-port counts, analyzes those counts while labels remain
hidden, and only then applies the separately stored key.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import tempfile
from pathlib import Path

SEED = 390_20260717
TARGETS = {"I": 1.0, "X": 0.0, "Z": 0.0, "F3": 1.0 / 3.0}
PHASES = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0]
REPLICATES = 8
SHOTS = 3000
CALIBRATION = {"mode_overlap": 0.96, "non_dark_fraction": 0.98}
ETA = CALIBRATION["mode_overlap"] * CALIBRATION["non_dark_fraction"]
TOLERANCE = {"I": 0.04, "X": 0.04, "Z": 0.04, "F3": 0.04}


def binomial(rng: random.Random, n: int, probability: float) -> int:
    return sum(rng.random() < probability for _ in range(n))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def make_key(rng: random.Random) -> dict[str, str]:
    codes = ["A7", "B2", "C9", "D4"]
    gates = list(TARGETS)
    rng.shuffle(codes)
    return dict(zip(codes, gates))


def generate_raw_counts(key: dict[str, str]) -> dict:
    rng = random.Random(SEED)
    rows: list[dict] = []
    for code in sorted(key):
        gate = key[code]
        target = TARGETS[gate]
        effective_visibility = ETA * target
        for replicate in range(REPLICATES):
            for phase_index, phase in enumerate(PHASES):
                probability_port0 = 0.5 * (
                    1.0 + effective_visibility * math.cos(phase)
                )
                count0 = binomial(rng, SHOTS, probability_port0)
                rows.append({
                    "blind_gate_code": code,
                    "replicate": replicate,
                    "phase_index": phase_index,
                    "phase_radians": phase,
                    "shots": SHOTS,
                    "count_port0": count0,
                    "count_port1": SHOTS - count0,
                })
    return {
        "pass": 390,
        "study_type": "synthetic_dry_run_not_physical_data",
        "seed": SEED,
        "blinded": True,
        "gate_labels_present": False,
        "phases_radians": PHASES,
        "replicates_per_gate": REPLICATES,
        "shots_per_phase": SHOTS,
        "rows": rows,
    }


def analyze_blinded(raw: dict) -> dict[str, dict]:
    by_code: dict[str, dict[int, list[dict]]] = {}
    for row in raw["rows"]:
        by_code.setdefault(row["blind_gate_code"], {}).setdefault(
            row["replicate"], []
        ).append(row)

    result: dict[str, dict] = {}
    for code, replicate_rows in sorted(by_code.items()):
        estimates: list[float] = []
        quadrature: list[float] = []
        for _, rows in sorted(replicate_rows.items()):
            rows = sorted(rows, key=lambda row: row["phase_index"])
            y = [2.0 * row["count_port0"] / row["shots"] - 1.0 for row in rows]
            cosine = [math.cos(row["phase_radians"]) for row in rows]
            sine = [math.sin(row["phase_radians"]) for row in rows]
            a = sum(value * basis for value, basis in zip(y, cosine)) / sum(
                basis * basis for basis in cosine
            )
            b = sum(value * basis for value, basis in zip(y, sine)) / sum(
                basis * basis for basis in sine
            )
            estimates.append(a / ETA)
            quadrature.append(b / ETA)

        mean = statistics.fmean(estimates)
        standard_error = statistics.stdev(estimates) / math.sqrt(len(estimates))
        q_mean = statistics.fmean(quadrature)
        q_standard_error = statistics.stdev(quadrature) / math.sqrt(len(quadrature))
        result[code] = {
            "visibility_corrected_mean": mean,
            "visibility_standard_error": standard_error,
            "visibility_ci95": [
                mean - 1.96 * standard_error,
                mean + 1.96 * standard_error,
            ],
            "sine_quadrature_mean": q_mean,
            "sine_quadrature_standard_error": q_standard_error,
            "replicate_estimates": estimates,
        }
    return result


def unblind(blinded_analysis: dict[str, dict], key: dict[str, str]) -> dict:
    gates: dict[str, dict] = {}
    checks: dict[str, bool] = {}
    for code, gate in key.items():
        analysis = blinded_analysis[code]
        target = TARGETS[gate]
        estimate = analysis["visibility_corrected_mean"]
        ci_low, ci_high = analysis["visibility_ci95"]
        gate_result = {
            "blind_gate_code": code,
            "target_visibility": target,
            **analysis,
            "absolute_error": abs(estimate - target),
            "target_inside_ci95": ci_low <= target <= ci_high,
            "within_preregistered_tolerance": abs(estimate - target)
            <= TOLERANCE[gate],
        }
        gates[gate] = gate_result
        checks[f"{gate}_within_tolerance"] = gate_result[
            "within_preregistered_tolerance"
        ]
        checks[f"{gate}_phase_quadrature_small"] = (
            abs(gate_result["sine_quadrature_mean"]) <= 0.04
        )

    return {
        "pass": 390,
        "study_type": "synthetic_dry_run_not_physical_data",
        "physical_experiment_completed": False,
        "pre_registration": {
            "targets": TARGETS,
            "tolerances": TOLERANCE,
            "analysis_estimator": (
                "signed cosine coefficient of the four-phase two-port fringe, "
                "divided by independently declared visibility dilution eta"
            ),
            "uncertainty": (
                "normal 95% interval from the standard error across 8 independent "
                "replicate visibility estimates"
            ),
            "no_post_hoc_tuning": True,
        },
        "calibration": {
            **CALIBRATION,
            "visibility_dilution_eta": ETA,
            "source": "synthetic declared constants for pipeline validation only",
        },
        "unblinded_results": gates,
        "checks": checks,
        "verified_dry_run": all(checks.values()),
        "next_required_action": (
            "Freeze this code and replace only the raw count and calibration files "
            "with timestamped laboratory exports; the present counts cannot support "
            "a physical claim."
        ),
    }


def build_bundle(output_dir: Path) -> tuple[dict, dict, dict]:
    key_rng = random.Random(SEED + 1)
    key_map = make_key(key_rng)
    key = {
        "pass": 390,
        "study_type": "synthetic_dry_run_not_physical_data",
        "blind_key": key_map,
        "key_frozen_before_counts": True,
    }
    raw = generate_raw_counts(key_map)
    blinded = analyze_blinded(raw)
    results = unblind(blinded, key_map)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_text = json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n"
    key_text = json.dumps(key, sort_keys=True, separators=(",", ":")) + "\n"
    results["raw_counts_sha256"] = sha256_text(raw_text)
    results["blind_key_sha256"] = sha256_text(key_text)
    results_text = json.dumps(results, sort_keys=True, separators=(",", ":")) + "\n"

    (output_dir / "w33_pass390_choi_visibility_raw_counts.json").write_text(
        raw_text, encoding="utf-8"
    )
    (output_dir / "w33_pass390_choi_visibility_blind_key.json").write_text(
        key_text, encoding="utf-8"
    )
    (output_dir / "w33_pass390_choi_visibility_results.json").write_text(
        results_text, encoding="utf-8"
    )
    return raw, key, results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            _, _, expected = build_bundle(Path(temporary))
            for filename in (
                "w33_pass390_choi_visibility_raw_counts.json",
                "w33_pass390_choi_visibility_blind_key.json",
                "w33_pass390_choi_visibility_results.json",
            ):
                committed = (args.output_dir / filename).read_text(encoding="utf-8")
                generated = (Path(temporary) / filename).read_text(encoding="utf-8")
                if committed != generated:
                    raise SystemExit(f"Pass 390 drift: {filename}")
            results = expected
    else:
        _, _, results = build_bundle(args.output_dir)

    print(json.dumps({
        "verified_dry_run": results["verified_dry_run"],
        "physical_experiment_completed": results["physical_experiment_completed"],
        "estimates": {
            gate: round(values["visibility_corrected_mean"], 6)
            for gate, values in results["unblinded_results"].items()
        },
    }, sort_keys=True))


if __name__ == "__main__":
    main()
