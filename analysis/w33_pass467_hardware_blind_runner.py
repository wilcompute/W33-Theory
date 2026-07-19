#!/usr/bin/env python3
"""Pass 467: fail-closed hardware ingestion and frozen blind-classifier runner.

This closes the software/lab handoff, not the physical experiment.  The runner
accepts an exact 16x16 integer transfer matrix, a label-free sealed count table,
and (only after predictions are committed) an optional reveal.  The classifier,
abstention threshold, and endpoint are inherited unchanged from Pass 451.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS451 = ROOT / "data" / "w33_pass451_device_ready_blind_packet.json"
OUT = ROOT / "data" / "w33_pass467_hardware_blind_runner.json"
HARDWARE = ROOT / "hardware" / "pass467"
PHASES = 16
SCALE = 1_000_000
SHOTS = 16384
THRESHOLD = Fraction(1, 100)
SYNTHETIC_SALT = "pass467-schema-rehearsal-not-a-hardware-secret"


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def digest(obj) -> str:
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def round_fraction(value: Fraction) -> int:
    if value >= 0:
        return (value.numerator + value.denominator // 2) // value.denominator
    return -round_fraction(-value)


def base_templates() -> dict[str, list[int]]:
    field = []
    ring = []
    for n in range(PHASES):
        cf = (72 * math.cos(2 * math.pi * n / 8) + 288 * math.cos(2 * math.pi * n / 16)) / 360
        cr = (6 * math.cos(math.pi * n) + 60 * math.cos(2 * math.pi * n / 8) + 216 * math.cos(2 * math.pi * n / 16)) / 282
        field.append(round(cf * SCALE))
        ring.append(round(cr * SCALE))
    return {"field": field, "ring": ring}


def circulant_matrix(kernel: list[int]) -> tuple[list[list[int]], list[int]]:
    denominator = sum(kernel)
    rows = []
    denoms = []
    for n in range(PHASES):
        rows.append([kernel[(n - j) % PHASES] for j in range(PHASES)])
        denoms.append(denominator)
    return rows, denoms


def apply_transfer(template: list[int], matrix: list[list[int]], denominators: list[int]) -> list[int]:
    if len(matrix) != PHASES or len(denominators) != PHASES:
        raise ValueError("transfer matrix must have 16 rows")
    out = []
    for row, denominator in zip(matrix, denominators):
        if len(row) != PHASES or denominator <= 0:
            raise ValueError("each transfer row must have 16 integer weights and a positive denominator")
        out.append(round_fraction(Fraction(sum(w * x for w, x in zip(row, template)), denominator)))
    return out


def residual(counts: list[int], template: list[int]) -> Fraction:
    if len(counts) != PHASES:
        raise ValueError("each sample must contain 16 counts")
    n = len(counts)
    sy = sum(counts)
    st = sum(template)
    yc = [n * y - sy for y in counts]
    tc = [n * t - st for t in template]
    sst = sum(v * v for v in yc)
    var = sum(v * v for v in tc)
    cov = sum(a * b for a, b in zip(yc, tc))
    if var == 0:
        raise ValueError("constant transferred template")
    return Fraction(sst * var - cov * cov, var)


def predict(counts: list[int], templates: dict[str, list[int]]) -> dict:
    rf = residual(counts, templates["field"])
    rr = residual(counts, templates["ring"])
    winner = "field" if rf < rr else "ring"
    best = min(rf, rr)
    worst = max(rf, rr)
    margin = Fraction(worst - best, worst if worst else 1)
    abstain = margin < THRESHOLD
    return {
        "prediction": "abstain" if abstain else winner,
        "field_residual": [rf.numerator, rf.denominator],
        "ring_residual": [rr.numerator, rr.denominator],
        "margin": [margin.numerator, margin.denominator],
    }


def read_calibration(path: Path) -> tuple[list[list[int]], list[int]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != PHASES:
        raise ValueError("calibration CSV must contain exactly 16 data rows")
    matrix = []
    denominators = []
    for expected, row in enumerate(rows):
        if int(row["output_phase"]) != expected:
            raise ValueError("output_phase rows must be ordered 0..15")
        matrix.append([int(row[f"w{j}"]) for j in range(PHASES)])
        denominators.append(int(row["denominator"]))
    return matrix, denominators


def read_sealed(path: Path, shots_per_phase: int) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        forbidden = {"label", "truth", "class", "target"}
        if reader.fieldnames is None or forbidden.intersection(x.lower() for x in reader.fieldnames):
            raise ValueError("sealed CSV contains a forbidden truth-like column")
        required = {"sample_id", "commitment", *{f"count_{j}" for j in range(PHASES)}}
        if not required.issubset(reader.fieldnames):
            raise ValueError("sealed CSV is missing required columns")
        rows = []
        seen = set()
        for raw in reader:
            sample_id = int(raw["sample_id"])
            if sample_id in seen:
                raise ValueError("duplicate sample_id")
            seen.add(sample_id)
            counts = [int(raw[f"count_{j}"]) for j in range(PHASES)]
            if any(c < 0 or c > shots_per_phase for c in counts):
                raise ValueError("count outside [0,shots_per_phase]")
            commitment_value = raw["commitment"].strip()
            if len(commitment_value) != 64 or any(c not in "0123456789abcdef" for c in commitment_value):
                raise ValueError("commitment must be lowercase SHA256 hex")
            rows.append({"sample_id": sample_id, "commitment": commitment_value, "counts": counts})
    if not rows:
        raise ValueError("sealed CSV has no samples")
    return sorted(rows, key=lambda r: r["sample_id"])


def commitment(salt: str, sample_id: int, label: str) -> str:
    return hashlib.sha256(f"{salt}|{sample_id}|{label}".encode()).hexdigest()


def read_reveal(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"salt", "truth", "prediction_sha256"}:
        raise ValueError("reveal JSON must contain exactly salt, truth, prediction_sha256")
    truth = data["truth"]
    if not isinstance(truth, list) or any(set(row) != {"sample_id", "label"} for row in truth):
        raise ValueError("bad reveal truth rows")
    if any(row["label"] not in ("field", "ring") for row in truth):
        raise ValueError("bad reveal label")
    return data


def run_blind(
    matrix: list[list[int]],
    denominators: list[int],
    sealed: list[dict],
    protocol_parent_sha256: str,
) -> tuple[dict, dict[str, list[int]]]:
    templates = {name: apply_transfer(values, matrix, denominators) for name, values in base_templates().items()}
    calibration = {
        "parent_pass451_protocol_sha256": protocol_parent_sha256,
        "matrix_integer_rows": matrix,
        "row_denominators": denominators,
        "transferred_templates": templates,
    }
    challenge = {"calibration_sha256": digest(calibration), "samples": sealed}
    predictions = []
    for row in sealed:
        result = predict(row["counts"], templates)
        result["sample_id"] = row["sample_id"]
        predictions.append(result)
    prediction_file = {"sealed_challenge_sha256": digest(challenge), "predictions": predictions}
    return prediction_file, templates


def score_prediction_file(sealed: list[dict], prediction_file: dict, reveal: dict) -> dict:
    if reveal["prediction_sha256"] != digest(prediction_file):
        raise ValueError("reveal is not bound to this prediction file")
    truth = {int(row["sample_id"]): row["label"] for row in reveal["truth"]}
    if set(truth) != {row["sample_id"] for row in sealed}:
        raise ValueError("reveal sample IDs do not match sealed challenge")
    if any(row["commitment"] != commitment(reveal["salt"], row["sample_id"], truth[row["sample_id"]]) for row in sealed):
        raise ValueError("commitment verification failed")
    predictions = {row["sample_id"]: row["prediction"] for row in prediction_file["predictions"]}
    decided = [i for i in truth if predictions[i] != "abstain"]
    correct = sum(predictions[i] == truth[i] for i in decided)
    recalls = []
    for label in ("field", "ring"):
        ids = [i for i, value in truth.items() if value == label]
        recalls.append(Fraction(sum(predictions[i] == label for i in ids), len(ids)))
    balanced = sum(recalls, Fraction(0)) / 2
    return {
        "samples": len(truth),
        "decided": len(decided),
        "abstained": len(truth) - len(decided),
        "correct_decided": correct,
        "balanced_accuracy": [balanced.numerator, balanced.denominator],
    }


def deterministic_noise(sample_id: int, phase: int, window: int = 20) -> int:
    raw = hashlib.sha256(f"pass451|{sample_id}|{phase}".encode()).digest()
    return int.from_bytes(raw[:4], "big") % (2 * window + 1) - window


def synthetic_fixture(templates: dict[str, list[int]], samples: int = 96) -> tuple[list[dict], dict]:
    sealed = []
    truth = []
    for sample_id in range(samples):
        label = "ring" if (hashlib.sha256(f"truth|{sample_id}".encode()).digest()[0] & 1) else "field"
        visibility = [700_000, 775_000, 850_000, 925_000, 1_000_000][sample_id % 5]
        contrast = 550_000
        baseline = 500_000 + [-18_000, -8_000, 0, 9_000, 17_000][(sample_id // 5) % 5]
        imbalance = [-500, 0, 500][(sample_id // 25) % 3]
        counts = []
        for phase, value in enumerate(templates[label]):
            delta = round_fraction(Fraction(visibility * contrast * value, SCALE * SCALE))
            probability = max(20_000, min(980_000, baseline + delta + (imbalance if phase % 2 == 0 else -imbalance)))
            expected = round_fraction(Fraction(SHOTS * probability, SCALE))
            counts.append(max(0, min(SHOTS, expected + deterministic_noise(sample_id, phase))))
        sealed.append({
            "sample_id": sample_id,
            "commitment": commitment(SYNTHETIC_SALT, sample_id, label),
            "counts": counts,
        })
        truth.append({"sample_id": sample_id, "label": label})
    return sealed, {"salt": SYNTHETIC_SALT, "truth": truth}


def measured_inputs_present() -> bool:
    return all((HARDWARE / name).exists() for name in (
        "measured_manifest.json", "measured_calibration_matrix.csv", "measured_sealed_observations.csv"
    ))


def build_payload() -> dict:
    parent = json.loads(PASS451.read_text(encoding="utf-8"))
    protocol = parent["protocol"]
    kernel = protocol["kernel_integer_weights"]
    matrix, denominators = circulant_matrix(kernel)
    transferred = {name: apply_transfer(values, matrix, denominators) for name, values in base_templates().items()}
    sealed, reveal_without_hash = synthetic_fixture(transferred)
    prediction_file, runner_templates = run_blind(matrix, denominators, sealed, digest(protocol))
    reveal = {**reveal_without_hash, "prediction_sha256": digest(prediction_file)}
    score = score_prediction_file(sealed, prediction_file, reveal)

    template_calibration = HARDWARE / "calibration_matrix_template.csv"
    template_sealed = HARDWARE / "sealed_observations_template.csv"
    template_manifest = HARDWARE / "measurement_manifest_template.json"
    template_reveal = HARDWARE / "reveal_template.json"
    parsed_matrix, parsed_denominators = read_calibration(template_calibration)

    checks = {
        "parent_pass451_status_pass": parent["status"] == "PASS",
        "classifier_is_frozen_exact_residual": protocol["classifier"] == "minimum exact affine-fit residual to fixed-point transferred templates",
        "threshold_frozen_one_percent": protocol["abstention_margin"] == "1/100",
        "endpoint_frozen_balanced_accuracy": protocol["primary_endpoint"] == "balanced accuracy after commitment reveal",
        "template_calibration_parses": parsed_matrix == matrix and parsed_denominators == denominators,
        "template_sealed_has_required_header": template_sealed.read_text(encoding="utf-8").splitlines()[0].startswith("sample_id,commitment,count_0"),
        "manifest_template_declares_measured_false": json.loads(template_manifest.read_text())["measured"] is False,
        "reveal_template_contains_no_real_truth": json.loads(template_reveal.read_text())["truth"] == [],
        "matrix_reproduces_pass451_transferred_templates": transferred == protocol["transferred_templates"] == runner_templates,
        "synthetic_rehearsal_commitments_score": score["samples"] == 96 and score["decided"] == 96,
        "synthetic_rehearsal_balanced_accuracy_one": score["balanced_accuracy"] == [1, 1],
        "synthetic_fixture_not_misreported_as_measured": not measured_inputs_present(),
    }
    return {
        "schema": "w33.pass467.hardware_blind_runner.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "software_gate": "CLOSED",
        "hardware_gate": "OPEN_NO_MEASURED_INPUT" if not measured_inputs_present() else "MEASURED_INPUT_PRESENT_REQUIRES_EXPLICIT_RUN",
        "frozen_parent_protocol_sha256": digest(protocol),
        "runner_contract": {
            "calibration": "16x16 integer matrix with one positive denominator per row",
            "sealed_observations": "label-free CSV with SHA256 commitment and 16 count columns",
            "prediction": "minimum exact affine-fit residual; abstain below margin 1/100",
            "reveal": "accepted only after prediction hash binding and commitment verification",
            "endpoint": "balanced accuracy after reveal",
        },
        "template_files": [
            str(template_calibration.relative_to(ROOT)),
            str(template_sealed.relative_to(ROOT)),
            str(template_manifest.relative_to(ROOT)),
            str(template_reveal.relative_to(ROOT)),
        ],
        "synthetic_schema_rehearsal": {
            "measured": False,
            "score": score,
            "prediction_sha256": digest(prediction_file),
            "minimum_margin": min(row["margin"] for row in prediction_file["predictions"]),
        },
        "hardware_boundary": (
            "No measured optical transfer matrix or sealed hardware holdout is present in the repository package. "
            "This pass closes parsing, hashing, prediction, reveal, and scoring software and deliberately leaves the "
            "physical gate open. A future measured run must replace only calibration and observations."
        ),
        "checks": checks,
    }


def run_external(args: argparse.Namespace) -> int:
    parent = json.loads(PASS451.read_text(encoding="utf-8"))
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if manifest.get("measured") is not True:
        raise SystemExit("external execution requires manifest.measured=true")
    required_meta = ["acquisition_id", "device_id", "operator", "timestamp_utc", "shots_per_phase"]
    if any(not manifest.get(k) for k in required_meta):
        raise SystemExit("measured manifest missing required acquisition metadata")
    matrix, denominators = read_calibration(args.calibration)
    sealed = read_sealed(args.sealed, int(manifest["shots_per_phase"]))
    prediction_file, _templates = run_blind(matrix, denominators, sealed, digest(parent["protocol"]))
    args.predictions.write_text(canonical(prediction_file) + "\n", encoding="utf-8")
    result = {"prediction_sha256": digest(prediction_file), "samples": len(sealed), "scored": False}
    if args.reveal:
        reveal = read_reveal(args.reveal)
        result["score"] = score_prediction_file(sealed, prediction_file, reveal)
        result["scored"] = True
    print(json.dumps(result, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--calibration", type=Path)
    parser.add_argument("--sealed", type=Path)
    parser.add_argument("--predictions", type=Path)
    parser.add_argument("--reveal", type=Path)
    args = parser.parse_args()
    external = any((args.manifest, args.calibration, args.sealed, args.predictions, args.reveal))
    if external:
        if not all((args.manifest, args.calibration, args.sealed, args.predictions)):
            parser.error("external run requires --manifest --calibration --sealed --predictions")
        return run_external(args)
    payload = build_payload()
    text = canonical(payload) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Pass 467 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"]), "hardware_gate": payload["hardware_gate"]}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
