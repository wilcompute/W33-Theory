#!/usr/bin/env python3
"""Foundry-targeted self-calibrating compiler for the 16-mode Levi-to-E8 mesh."""
from __future__ import annotations
from functools import lru_cache

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from w33_levi_next5_v4_common import ACTIVE, sha256_json


def psd_sqrt(H):
    vals, vecs = eigh((H + H.T.conj()) / 2)
    vals = np.clip(vals, 0, None)
    return (vecs * np.sqrt(vals)) @ vecs.T.conj()


def halmos(A):
    s = np.linalg.svd(A, compute_uv=False)[0]
    C = A / s
    I = np.eye(8)
    L = psd_sqrt(I - C @ C.T)
    R = psd_sqrt(I - C.T @ C)
    U = np.block([[C, L], [R, -C.T]]).astype(complex)
    return s, C, U


def givens_decompose(U):
    A = U.copy()
    rots = []
    n = A.shape[0]
    for col in range(n):
        for row in range(n - 1, col, -1):
            i, j = row - 1, row
            a, b = A[i, col], A[j, col]
            r = math.sqrt(abs(a) ** 2 + abs(b) ** 2)
            if r < 1e-15:
                c, s = 1 + 0j, 0 + 0j
            else:
                c, s = np.conj(a) / r, np.conj(b) / r
            G = np.array([[c, s], [-np.conj(s), np.conj(c)]], complex)
            A[[i, j], :] = G @ A[[i, j], :]
            theta = math.atan2(abs(s), abs(c))
            phi = float(np.angle(s) - np.angle(c))
            alpha = float(np.angle(c))
            rots.append((i, j, theta, phi, alpha))
    phases = np.angle(np.diag(A))
    return rots, phases


def build_rotation(theta, phi, alpha):
    c = math.cos(theta) * np.exp(1j * alpha)
    s = math.sin(theta) * np.exp(1j * (alpha + phi))
    return np.array([[c, s], [-np.conj(s), np.conj(c)]], complex)


def synthesize(rot_pairs, theta, phi, alpha, output_phase):
    A = np.diag(np.exp(1j * output_phase))
    for k in reversed(range(len(rot_pairs))):
        i, j = rot_pairs[k]
        G = build_rotation(theta[k], phi[k], alpha[k])
        A[[i, j], :] = G.conj().T @ A[[i, j], :]
    return A


def wrap(x):
    return (x + math.pi) % (2 * math.pi) - math.pi


def quantize(x, bits, span=2 * math.pi):
    step = span / (2**bits - 1)
    return np.round(x / step) * step


def crosstalk_matrix(n, nearest=0.065, length=1.7):
    idx = np.arange(n)
    distance = np.abs(idx[:, None] - idx[None, :])
    K = np.exp(-distance / length)
    np.fill_diagonal(K, 0.0)
    K *= nearest / math.exp(-1 / length)
    C = np.eye(n) + K
    return C


def process_fidelity(U, V):
    n = U.shape[0]
    return float(abs(np.trace(U.conj().T @ V)) ** 2 / (n * n))


def calibrate(target, C, Cinv, bias, bits, rng, iterations=12):
    command = quantize(target, bits)
    history = []
    for _ in range(iterations):
        command = quantize(command, bits)
        measured = C @ command + bias + rng.normal(0, 1.5e-4, len(target))
        error = target - measured
        command += 0.92 * (Cinv @ error)
        history.append(float(np.linalg.norm(error) / math.sqrt(len(error))))
    command = quantize(command, bits)
    effective = C @ command + bias
    return command, effective, history


@lru_cache(maxsize=1)
def analyze(seed=20260710):
    rng = np.random.default_rng(seed)
    _scale, _C8, target_U = halmos(ACTIVE)
    rotations, out_phase = givens_decompose(target_U)
    pairs = [(i, j) for i, j, *_ in rotations]
    theta = np.array([r[2] for r in rotations])
    phi = np.array([r[3] for r in rotations])
    alpha = np.array([r[4] for r in rotations])
    target = np.concatenate([theta, phi, alpha, out_phase])
    n = len(target)

    stack = {
        "platform": "800-nm-class foundry-compatible Si3N4 passive core with thermo-optic metal heaters",
        "design_wavelength_nm": 1550.0,
        "wavelength_band_nm": [1530.0, 1565.0],
        "propagation_loss_db_per_m": 2.6,
        "heater_pi_power_mw": 24.0,
        "phase_dac_bits": 14,
        "nearest_neighbor_thermal_crosstalk": 0.065,
        "thermal_correlation_length_cells": 1.7,
        "mzi_excess_loss_db": 0.018,
        "phase_section_length_mm": 1.2,
        "fiber_coupling_db_per_facet": 2.5,
        "assumption_boundary": "Passive loss is anchored to foundry-manufactured thick SiN; heater efficiency, excess loss, and layout lengths are explicit design assumptions pending a chosen PDK corner deck.",
    }

    Cx = crosstalk_matrix(n, stack["nearest_neighbor_thermal_crosstalk"], stack["thermal_correlation_length_cells"])
    bias = np.concatenate([
        rng.normal(0, 0.010, len(theta)),
        rng.normal(0, 0.022, len(phi)),
        rng.normal(0, 0.018, len(alpha)),
        rng.normal(0, 0.015, len(out_phase)),
    ])

    zero_cmd = quantize(target, stack["phase_dac_bits"])
    uncal_eff = Cx @ zero_cmd + bias
    Cinv = np.linalg.inv(Cx + 1e-8 * np.eye(n))
    command, calibrated, history = calibrate(target, Cx, Cinv, bias, stack["phase_dac_bits"], rng)

    def unitary_from_vector(vec, wavelength_nm=1550.0, dynamic=None):
        m = len(theta)
        t = vec[:m].copy()
        p = vec[m:2*m].copy()
        a = vec[2*m:3*m].copy()
        o = vec[3*m:].copy()
        ratio = stack["design_wavelength_nm"] / wavelength_nm
        t *= 1 + 0.035 * (ratio - 1)
        p *= ratio
        a *= ratio
        o *= ratio
        if dynamic is not None:
            t += dynamic[:m]
            p += dynamic[m:2*m]
            a += dynamic[2*m:3*m]
            o += dynamic[3*m:]
        return synthesize(pairs, t, p, a, o)

    U_uncal = unitary_from_vector(uncal_eff)
    U_cal = unitary_from_vector(calibrated)
    nominal = {
        "uncalibrated_fidelity": process_fidelity(target_U, U_uncal),
        "calibrated_fidelity": process_fidelity(target_U, U_cal),
        "calibration_rms_history": history,
        "final_phase_rms_rad": float(np.linalg.norm(target - calibrated) / math.sqrt(n)),
    }

    wavelengths = np.linspace(1530.0, 1565.0, 15)
    wavelength_fidelity = {f"{w:.1f}": process_fidelity(target_U, unitary_from_vector(calibrated, float(w))) for w in wavelengths}

    drift = np.zeros(n)
    tracked = []
    open_loop = []
    tracked_command = command.copy()
    for epoch in range(64):
        common = rng.normal(0, 0.0012)
        drift += rng.normal(0, 0.00045, n) + common * np.exp(-np.arange(n) / 180)
        open_eff = Cx @ command + bias + drift
        open_loop.append(process_fidelity(target_U, unitary_from_vector(open_eff)))
        measured = Cx @ tracked_command + bias + drift + rng.normal(0, 1.8e-4, n)
        error = target - measured
        tracked_command = quantize(tracked_command + 0.90 * (Cinv @ error), stack["phase_dac_bits"])
        tracked_eff = Cx @ tracked_command + bias + drift
        tracked.append(process_fidelity(target_U, unitary_from_vector(tracked_eff)))

    die_fidelities = []
    for _ in range(96):
        die_bias = bias + rng.normal(0, 0.004, n)
        _cmd, eff, _hist = calibrate(target, Cx, Cinv, die_bias, stack["phase_dac_bits"], rng, iterations=6)
        dyn = rng.normal(0, 0.0008, n)
        die_fidelities.append(process_fidelity(target_U, unitary_from_vector(eff, 1550.0, dyn)))
    arr = np.array(die_fidelities)

    path_length_m = 16 * stack["phase_section_length_mm"] / 1000
    passive_loss = path_length_m * stack["propagation_loss_db_per_m"]
    mesh_loss = 16 * stack["mzi_excess_loss_db"]
    on_chip_loss = passive_loss + mesh_loss
    total_insertion = on_chip_loss + 2 * stack["fiber_coupling_db_per_facet"]
    phase_mod = np.mod(command, 2 * math.pi)
    heater_power = float(np.sum(phase_mod) / math.pi * stack["heater_pi_power_mw"])

    checks = {
        "mesh_exact_before_foundry_model": np.linalg.norm(target_U.conj().T @ target_U - np.eye(16)) < 1e-10,
        "closed_loop_converges": history[-1] < history[0] / 20,
        "calibrated_nominal_above_0_999": nominal["calibrated_fidelity"] > 0.999,
        "wavelength_band_p05_above_0_995": np.quantile(list(wavelength_fidelity.values()), 0.05) > 0.995,
        "foundry_corner_p05_above_0_995": float(np.quantile(arr, 0.05)) > 0.995,
        "tracking_beats_open_loop": float(np.mean(tracked)) > float(np.mean(open_loop)),
        "tracked_min_above_0_995": min(tracked) > 0.995,
        "phase_controls_quantized": np.allclose(command, quantize(command, stack["phase_dac_bits"])),
    }
    checks = {k: bool(v) for k, v in checks.items()}

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "foundry_stack": stack,
        "compiler": {
            "modes": 16, "mzi_elements": 120, "output_phases": 16,
            "control_parameters": n, "netlist_digest": sha256_json(rotations),
            "quantized_command_digest": sha256_json([round(float(x), 12) for x in command]),
        },
        "calibration": nominal,
        "wavelength_fidelity": wavelength_fidelity,
        "foundry_corners": {
            "dies": len(arr), "mean": float(arr.mean()), "p05": float(np.quantile(arr, 0.05)),
            "min": float(arr.min()), "max": float(arr.max()),
        },
        "drift_tracking": {
            "epochs": len(tracked), "open_loop_mean": float(np.mean(open_loop)),
            "tracked_mean": float(np.mean(tracked)), "tracked_min": float(min(tracked)),
            "tracked_digest": sha256_json([round(x, 12) for x in tracked]),
        },
        "budget": {
            "path_length_m": path_length_m, "passive_propagation_loss_db": passive_loss,
            "mesh_excess_loss_db": mesh_loss, "on_chip_loss_db": on_chip_loss,
            "fiber_to_fiber_loss_db": total_insertion, "estimated_total_heater_power_mw": heater_power,
        },
        "theorem": (
            "A 14-bit closed-loop inverse-crosstalk calibration of the 16-mode, 120-MZI Levi-to-E8 mesh "
            "maintains >0.995 fifth-percentile process fidelity across the modeled foundry corners and 1530-1565 nm band, "
            "while online drift correction dominates open-loop operation."
        ),
    }


def main():
    out = analyze()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
