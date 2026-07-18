#!/usr/bin/env python3
"""Pass 409: vendor-neutral hardware falsifier and sealed nonclaim dry run."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import statistics


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass409_sealed_hardware_falsifier.json"
BOM = ROOT / "data" / "w33_pass409_vendor_neutral_bom.json"
PROTOCOL = ROOT / "data" / "w33_pass409_preregistered_protocol.json"
POWER = ROOT / "data" / "w33_pass409_nonclaim_power_study.json"
RAW = ROOT / "data" / "w33_pass409_nonclaim_raw_counts.json"
CAL = ROOT / "data" / "w33_pass409_nonclaim_calibration.json"
KEY = ROOT / "data" / "w33_pass409_nonclaim_blind_key.json"
PASS404_SCHEDULE = ROOT / "data" / "w33_pass404_photonic_voltage_schedule_q3.json"

PHASES = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
TARGETS = {"I": 1.0, "X": 0.0, "Z": 0.0, "F3": 1.0 / 3.0}
BLIND_MAP = {"A7": "X", "B2": "F3", "C9": "I", "D4": "Z"}


def canonical_sha(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_bom(schedule: dict) -> dict:
    native_layers = schedule["native_layers"]
    return {
        "schema": "w33.pass409.vendor_neutral_bom.v1",
        "scope": "27-mode qutrit Heisenberg bulk demonstrator",
        "component_classes": [
            {"id": "SRC-1", "class": "heralded single-photon source", "quantity": 1, "required_specifications": {"repetition_rate_hz": None, "heralding_efficiency": None, "g2_zero_max": None}},
            {"id": "MODE-27", "class": "phase-stable optical modes", "quantity": 27, "required_specifications": {"relative_phase_stability_rad_rms": None, "path_length_drift_um_per_hour": None}},
            {"id": "SW-12", "class": "reconfigurable two-mode couplers", "quantity": 12, "reuse_model": "reprogrammed across nine native slices", "required_specifications": {"splitting_ratio_error_max": None, "insertion_loss_db_max": None, "switching_time_ns_max": None}},
            {"id": "MAG-9", "class": "oriented three-mode magnetic triangles", "quantity": 9, "equivalent_directed_couplers": 27, "required_specifications": {"coupling_magnitude": "1/sqrt(3)", "directed_phase_rad": "pi/2", "phase_error_rad_max": None}},
            {"id": "TRI-9", "class": "balanced qutrit Fourier tritters", "quantity": 9, "required_specifications": {"unitary_process_fidelity_min": None, "insertion_loss_db_max": None}},
            {"id": "PHASE-27", "class": "independent phase shifters", "quantity": 27, "required_specifications": {"phase_resolution_rad": None, "phase_repeatability_rad_rms": None}},
            {"id": "DELAY-9", "class": "time-slice delay registers", "quantity": 9, "required_specifications": {"slice_delay_ns": None, "jitter_ps_rms": None}},
            {"id": "DET-27", "class": "single-photon detector channels", "quantity": 27, "required_specifications": {"efficiency_min": None, "dark_count_hz_max": None, "timing_jitter_ps_max": None}},
            {"id": "CTRL-1", "class": "deterministic schedule controller", "quantity": 1, "required_specifications": {"native_slices": 9, "calibration_triggers": 10, "blind_code_support": 4}},
        ],
        "compiled_counts": {
            "native_time_slices": len(native_layers),
            "parallel_native_couplers_per_slice": len(native_layers[0]["couplers"]),
            "native_coupler_activations": sum(len(layer["couplers"]) for layer in native_layers),
            "magnetic_directed_couplers": len(schedule["magnetic_control"]["couplers"]),
            "detector_channels": 27,
        },
        "cost_fields": {"currency": None, "unit_costs": None, "total_estimate": None},
        "acceptance_tests": [
            "reconstruct all 108 native edges exactly once",
            "verify zero simultaneous mode conflicts in each native slice",
            "measure magnetic triangle phase circulation before blinded acquisition",
            "hash firmware, schedule, calibration, and blind-key commitments before acquisition",
        ],
    }


def build_protocol() -> dict:
    return {
        "schema": "w33.pass409.preregistered_falsifier.v1",
        "protocol_frozen_at": "2026-07-17T14:00:00-04:00",
        "study_type": "future_physical_lab_protocol_not_yet_run",
        "physical_experiment_completed": False,
        "gates": TARGETS,
        "minimum_design": {"replicates_per_gate": 8, "shots_per_phase": 3000, "phases_radians": PHASES},
        "calibration_requirements": {"visibility_dilution_eta_min": 0.85, "device_id_match_required": True},
        "primary_decision_rule": {
            "all_gate_absolute_visibility_error_max": 0.08,
            "all_gate_absolute_sine_quadrature_max": 0.08,
            "integrity_contract": "Pass 397 seal -> analyze -> unblind with no synthetic production fallback",
            "pass_condition": "all thresholds pass simultaneously; no post-hoc gate-specific relaxation",
        },
        "falsifying_alternatives": {
            "stuck_identity": {"I": 1.0, "X": 1.0, "Z": 1.0, "F3": 1.0},
            "half_control": {"I": 1.0, "X": 0.5, "Z": 0.5, "F3": 2.0 / 3.0},
        },
        "claim_boundary": "A future passing sealed bundle would establish agreement with these process-visibility predictions under the calibrated apparatus model, not universal quantum computation or a fundamental-physics claim.",
    }


def estimate_visibility(rows: list[dict], eta: float) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[int, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[row["blind_gate_code"]][int(row["replicate"])].append(row)
    result = {}
    for code, replicates in grouped.items():
        vis, quad = [], []
        for records in replicates.values():
            ordered = sorted(records, key=lambda r: int(r["phase_index"]))
            y = [2 * int(r["count_port0"]) / int(r["shots"]) - 1 for r in ordered]
            cosine = [1.0, 0.0, -1.0, 0.0]
            sine = [0.0, 1.0, 0.0, -1.0]
            vis.append(sum(a * b for a, b in zip(y, cosine)) / 2.0 / eta)
            quad.append(sum(a * b for a, b in zip(y, sine)) / 2.0 / eta)
        result[code] = {"visibility": round(statistics.fmean(vis), 12), "quadrature": round(statistics.fmean(quad), 12)}
    return result


def pass_rule(estimates_by_gate: dict[str, dict[str, float]], protocol: dict) -> bool:
    threshold_v = protocol["primary_decision_rule"]["all_gate_absolute_visibility_error_max"]
    threshold_q = protocol["primary_decision_rule"]["all_gate_absolute_sine_quadrature_max"]
    return all(
        abs(estimates_by_gate[gate]["visibility"] - TARGETS[gate]) <= threshold_v
        and abs(estimates_by_gate[gate]["quadrature"]) <= threshold_q
        for gate in TARGETS
    )


def hoeffding_visibility_tail(error: float, replicates: int, shots: int, eta: float) -> float:
    """Two-sided Hoeffding bound for the corrected four-phase visibility estimator."""
    return min(1.0, 2.0 * math.exp(-(error**2) * replicates * shots * (eta**2)))


def hoeffding_log10_upper(error: float, replicates: int, shots: int, eta: float, multiplicity: int = 2) -> float:
    """log10 of multiplicity*exp(-error^2*r*N*eta^2), avoiding underflow."""
    return math.log10(multiplicity) - (error**2) * replicates * shots * (eta**2) / math.log(10.0)


def exact_power_bounds(protocol: dict, eta: float = 0.92) -> dict:
    replicates = int(protocol["minimum_design"]["replicates_per_gate"])
    shots = int(protocol["minimum_design"]["shots_per_phase"])
    threshold = float(protocol["primary_decision_rule"]["all_gate_absolute_visibility_error_max"])
    quadrature = float(protocol["primary_decision_rule"]["all_gate_absolute_sine_quadrature_max"])
    # Union bound over four visibility and four quadrature conditions.
    one_v_log10 = hoeffding_log10_upper(threshold, replicates, shots, eta)
    one_q_log10 = hoeffding_log10_upper(quadrature, replicates, shots, eta)
    family_log10 = math.log10(4 * 10**one_v_log10 + 4 * 10**one_q_log10)
    stuck_gap = min(abs(protocol["falsifying_alternatives"]["stuck_identity"][gate] - TARGETS[gate]) for gate in TARGETS if protocol["falsifying_alternatives"]["stuck_identity"][gate] != TARGETS[gate])
    half_gap = min(abs(protocol["falsifying_alternatives"]["half_control"][gate] - TARGETS[gate]) for gate in TARGETS if protocol["falsifying_alternatives"]["half_control"][gate] != TARGETS[gate])
    stuck_log10 = hoeffding_log10_upper(stuck_gap - threshold, replicates, shots, eta)
    half_log10 = hoeffding_log10_upper(half_gap - threshold, replicates, shots, eta)
    return {
        "method": "distribution-free Hoeffding bounds for the preregistered four-phase estimator",
        "eta": eta,
        "ideal_familywise_false_reject_log10_upper_bound": round(family_log10, 9),
        "ideal_protocol_pass_probability_statement": f"at least 1-10^({family_log10:.6f})",
        "stuck_identity_false_pass_log10_upper_bound": round(stuck_log10, 9),
        "half_control_false_pass_log10_upper_bound": round(half_log10, 9),
    }

def make_nonclaim_fixture(eta_overlap: float = 0.96, non_dark: float = 0.96) -> tuple[dict, dict, dict]:
    eta = eta_overlap * non_dark
    rows = []
    for code, gate in BLIND_MAP.items():
        visibility = TARGETS[gate]
        for replicate in range(8):
            for phase_index, phase in enumerate(PHASES):
                shots = 3000
                p0 = (1 + eta * visibility * [1.0, 0.0, -1.0, 0.0][phase_index]) / 2
                count0 = int(round(shots * p0))
                rows.append({"blind_gate_code": code, "replicate": replicate, "phase_index": phase_index, "phase_radians": phase, "shots": shots, "count_port0": count0, "count_port1": shots - count0})
    raw = {
        "schema": "w33.photonic.sealed-lab.v1.raw-counts",
        "study_type": "nonclaim_test_fixture",
        "blinded": True,
        "gate_labels_present": False,
        "acquisition_started_at": "2026-07-17T15:00:00-04:00",
        "acquisition_completed_at": "2026-07-17T15:20:00-04:00",
        "device_id": "PASS409-NONCLAIM-FIXTURE",
        "phases_radians": PHASES,
        "rows": rows,
    }
    calibration = {
        "schema": "w33.photonic.sealed-lab.v1.calibration",
        "study_type": "nonclaim_test_fixture",
        "calibrated_at": "2026-07-17T14:30:00-04:00",
        "device_id": "PASS409-NONCLAIM-FIXTURE",
        "mode_overlap": eta_overlap,
        "non_dark_fraction": non_dark,
        "method": "deterministic nonclaim power-study fixture",
        "operator": "automated-pass409",
    }
    key = {
        "schema": "w33.photonic.sealed-lab.v1.blind-key",
        "study_type": "nonclaim_test_fixture",
        "key_frozen_at": "2026-07-17T14:45:00-04:00",
        "key_revealed_at": "2026-07-17T16:00:00-04:00",
        "mapping": BLIND_MAP,
        "custodian": "automated-pass409-nonclaim",
    }
    return raw, calibration, key


def build_payload() -> tuple[dict, dict, dict, dict, dict, dict, dict]:
    schedule = json.loads(PASS404_SCHEDULE.read_text())
    bom = build_bom(schedule)
    protocol = build_protocol()
    bounds = exact_power_bounds(protocol, eta=0.92)
    power = {
        "schema": "w33.pass409.nonclaim_power_study.v1",
        "study_type": "analytic_power_bound_not_physical_data",
        **bounds,
    }
    raw, calibration, key = make_nonclaim_fixture()
    eta = calibration["mode_overlap"] * calibration["non_dark_fraction"]
    blind = estimate_visibility(raw["rows"], eta)
    unblinded = {gate: blind[code] for code, gate in BLIND_MAP.items()}
    fixture_pass = pass_rule(unblinded, protocol)

    checks = {
        "native_schedule_has_nine_slices": bom["compiled_counts"]["native_time_slices"] == 9,
        "native_schedule_has_108_activations": bom["compiled_counts"]["native_coupler_activations"] == 108,
        "magnetic_layer_has_27_couplers": bom["compiled_counts"]["magnetic_directed_couplers"] == 27,
        "bom_has_27_detector_channels": bom["compiled_counts"]["detector_channels"] == 27,
        "protocol_frozen_before_fixture_acquisition": datetime.fromisoformat(protocol["protocol_frozen_at"]) < datetime.fromisoformat(raw["acquisition_started_at"]),
        "blind_key_frozen_before_fixture_acquisition": datetime.fromisoformat(key["key_frozen_at"]) < datetime.fromisoformat(raw["acquisition_started_at"]),
        "blind_key_revealed_after_fixture_analysis_window": datetime.fromisoformat(key["key_revealed_at"]) > datetime.fromisoformat(raw["acquisition_completed_at"]),
        "raw_fixture_has_four_codes": len({row["blind_gate_code"] for row in raw["rows"]}) == 4,
        "raw_fixture_has_8_replicates_and_4_phases": len(raw["rows"]) == 4 * 8 * 4,
        "raw_counts_conserve_shots": all(row["count_port0"] + row["count_port1"] == row["shots"] for row in raw["rows"]),
        "fixture_remains_blinded": raw["blinded"] is True and raw["gate_labels_present"] is False,
        "nonclaim_fixture_passes_preregistered_rule": fixture_pass,
        "ideal_power_at_least_95_percent": bounds["ideal_familywise_false_reject_log10_upper_bound"] <= math.log10(0.05),
        "stuck_identity_rejected_at_least_99_percent": bounds["stuck_identity_false_pass_log10_upper_bound"] <= math.log10(0.01),
        "half_control_rejected_at_least_95_percent": bounds["half_control_false_pass_log10_upper_bound"] <= math.log10(0.05),
        "physical_experiment_not_completed": protocol["physical_experiment_completed"] is False,
    }

    payload = {
        "schema": "w33.pass409.sealed_hardware_falsifier.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "bom_path": "data/w33_pass409_vendor_neutral_bom.json",
        "protocol_path": "data/w33_pass409_preregistered_protocol.json",
        "power_study_path": "data/w33_pass409_nonclaim_power_study.json",
        "nonclaim_fixture_paths": {
            "raw": "data/w33_pass409_nonclaim_raw_counts.json",
            "calibration": "data/w33_pass409_nonclaim_calibration.json",
            "blind_key": "data/w33_pass409_nonclaim_blind_key.json",
        },
        "fixture_unblinded_estimates": unblinded,
        "production_execution": "not performed; no genuine laboratory counts were supplied",
        "required_next_physical_action": "populate the same sealed schema with externally acquired counts and run Pass 397 without --test-mode",
        "checks": checks,
    }
    for name, artifact in (("bom", bom), ("protocol", protocol), ("power", power), ("raw", raw), ("calibration", calibration), ("key", key)):
        payload[f"{name}_sha256"] = canonical_sha(artifact)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload, bom, protocol, power, raw, calibration, key


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload, bom, protocol, power, raw, calibration, key = build_payload()
    outputs = {
        OUT: payload,
        BOM: bom,
        PROTOCOL: protocol,
        POWER: power,
        RAW: raw,
        CAL: calibration,
        KEY: key,
    }
    for path, artifact in outputs.items():
        text = json.dumps(artifact, indent=2, sort_keys=True) + "\n"
        if args.check:
            if not path.exists() or path.read_text() != text:
                raise SystemExit(f"Pass 409 artifact stale: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
