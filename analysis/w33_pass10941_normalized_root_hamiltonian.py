#!/usr/bin/env python3
"""Pass 10941 front 5: normalized compact-E8 pulse law and falsifier.

The exact algebraic scheduler supplies eight compact root-plane generators and
six commuting microframes.  This producer adds only declared laboratory scale:
one reference angle theta_0=pi/2.  Every tolerance below is derived from that
choice and is labelled as a design requirement rather than a measurement.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_pass10941_normalized_root_hamiltonian.json"

sparse = json.loads((ROOT / "data/w33_20260923_compact_e8_sparse8.json").read_text())
schedule = json.loads((ROOT / "data/w33_pass409_sparse8_holonet_schedule.json").read_text())

support = sparse["support"]
amplitudes = sparse["amplitudes"]
assert support == schedule["support"] and len(support) == len(amplitudes) == 8
assert sum(amplitudes) == 14 and sum(a * a for a in amplitudes) == 30
assert schedule["microframes_per_AB_cycle"] == 6
assert schedule["ticks_per_microframe"] == 72

# For a Chevalley root pair in E8, B(e_alpha,e_-alpha)=60 in the repo gauge.
# The compact real generators X=e_alpha-sigma(e_alpha) and
# Y=i(e_alpha+sigma(e_alpha)) consequently have -B(X,X)=-B(Y,Y)=120.
killing_norm = 120
theta0 = math.pi / 2
operator_error_target = 0.01
survival_target = 0.90

frames = []
for lane in ("A", "B"):
    for batch in schedule["schedules"][lane]["batches"]:
        ids = batch["atom_ids"]
        weights = [amplitudes[i] for i in ids]
        frames.append(
            {
                "microframe": len(frames),
                "lane": lane,
                "atom_ids": ids,
                "sources": [support[i] for i in ids],
                "integer_weights": weights,
                "l1_weight": sum(weights),
                "pulse_areas_rad": [a * theta0 for a in weights],
                "hamiltonian": (
                    "H_k(t)/hbar = Omega_0(t) * sum_{j in batch(k)} "
                    "a_j Ghat_j, with integral Omega_0 dt = theta_0"
                ),
                "normalized_generators": (
                    "Ghat_j=X_j/sqrt(120) for A; Ghat_j=Y_j/sqrt(120) for B"
                ),
            }
        )

weights_per_frame = [f["l1_weight"] for f in frames]
assert weights_per_frame == [4, 5, 5, 4, 5, 5]
total_l1_angle = sum(weights_per_frame) * theta0
assert math.isclose(total_l1_angle, 28 * theta0)

# If each implemented Hamiltonian differs by at most rho times the ideal
# weighted generator norm, Duhamel's inequality gives exp(E)-1 with
# E <= rho * total_l1_angle.  Invert it for the declared one-percent target.
rho_max = math.log1p(operator_error_target) / total_l1_angle
duhamel_at_threshold = math.expm1(total_l1_angle * rho_max)
assert math.isclose(duhamel_at_threshold, operator_error_target, rel_tol=0, abs_tol=1e-15)

per_frame_survival = survival_target ** (1 / 6)
cycle_loss_db = -10 * math.log10(survival_target)
per_frame_loss_db = cycle_loss_db / 6
assert math.isclose(per_frame_survival**6, survival_target)

out = {
    "schema": "w33.pass10941.normalized_root_hamiltonian.v1",
    "status": "PASS_NORMALIZED_EIGHT_ROOT_HAMILTONIAN_AND_END_TO_END_FALSIFIER",
    "algebraic_normalization": {
        "compact_root_plane_killing_norm": killing_norm,
        "basis": "Ghat_j=G_j/sqrt(120), so -B(Ghat_j,Ghat_j)=1",
        "support": support,
        "integer_amplitudes": amplitudes,
        "sum_abs_amplitudes": 14,
        "sum_squared_amplitudes": 30,
    },
    "declared_reference_pulse": {
        "theta_0_rad": theta0,
        "meaning": "integral Omega_0(t) dt for a unit-weight root-plane pulse",
        "ticks_per_microframe": 72,
        "maximum_single_atom_Rabi_per_tick_time": "pi/(48*tau_tick)",
        "maximum_batch_norm_bound_per_tick_time": "5*pi/(144*tau_tick)",
        "boundary": "theta_0 and tau_tick are engineering controls, not predictions",
    },
    "six_microframes": frames,
    "cycle": {
        "frame_l1_weights": weights_per_frame,
        "total_l1_angle_rad": total_l1_angle,
        "ticks": schedule["ticks_per_AB_cycle"],
    },
    "coherent_error_falsifier": {
        "model": "||Delta H_k(t)|| <= rho ||H_k(t)|| in the Killing-normalized control norm",
        "bound": "||U_meas-U_ideal|| <= exp(28*theta_0*rho)-1",
        "declared_operator_error_target": operator_error_target,
        "maximum_relative_integrated_error_rho": rho_max,
        "bound_at_threshold": duhamel_at_threshold,
        "acceptance": "tomography must give operator-norm deviation <= 0.01",
    },
    "loss_falsifier": {
        "declared_AB_cycle_survival_target": survival_target,
        "minimum_survival_per_microframe_if_equal": per_frame_survival,
        "maximum_AB_cycle_loss_db": cycle_loss_db,
        "maximum_loss_per_microframe_db_if_equal": per_frame_loss_db,
        "acceptance": "measured unconditional survival must be >= 0.90 and reported separately from conditional coherent fidelity",
    },
    "end_to_end_protocol": [
        "calibrate each of the sixteen compact root-plane quadratures in the Killing-normalized convention",
        "execute the frozen A0,A1,A2,B0,B1,B2 commuting schedule with 72 ticks per microframe",
        "reconstruct the implemented cycle on the addressed control subspace by process tomography",
        "reject if operator-norm deviation exceeds 0.01 or unconditional survival is below 0.90",
        "repeat with each microframe omitted and each root-plane sign reversed to localize crosstalk and phase faults",
    ],
    "parents": [
        "data/w33_20260923_compact_e8_sparse8.json",
        "data/w33_pass409_sparse8_holonet_schedule.json",
        "data/w33_hesse36_photonic_process_calibration_theorem.json",
    ],
    "boundary": (
        "This is a normalized control law and a falsifiable device specification. "
        "No physical pulse duration, optical loss, crosstalk level, or successful "
        "laboratory realization is inferred from the E8 algebra."
    ),
}

OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "status": out["status"],
            "frame_weights": weights_per_frame,
            "rho_max": rho_max,
            "cycle_loss_db": cycle_loss_db,
        },
        indent=2,
    )
)
