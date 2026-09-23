#!/usr/bin/env python3
"""Derive a coherent calibration theorem for the 36-channel 9+3 F3 retimer.

Design target (explicitly chosen, not measured):
    F_target = 0.99
for the normalized 36x36 coherent transfer matrix.

Model:
  * every logical path contains one phase-referenced balanced tritter;
  * every path contains one matched HOLD;
  * common insertion loss is factored out (it affects success probability,
    not normalized coherent process overlap);
  * residual hold phases obey |delta_phi_j| <= phi_max after removing one
    common phase;
  * differential HOLD power-loss offsets obey |delta_L_j| <= L_max dB around
    the calibrated common loss;
  * the tritter coherent process factor is at least F_TRI.

For a diagonal phase error, normalized coherent overlap is >= cos^2(phi_max).
For positive amplitude gains a_j in [e^-s,e^s], the Kantorovich bound gives
    (sum a_j)^2/(d sum a_j^2) >= sech^2(s),
with s=(ln 10/20)L_max.

Under the phase-referenced multiplicative budget
    F_model >= F_TRI * cos^2(phi_max) * sech^2(s),
an equal three-way allocation uses f = F_target^(1/3), so it suffices that
    F_TRI >= f,
    phi_max <= acos(sqrt(f)),
    L_max <= (20/ln 10) acosh(1/sqrt(f)) dB.

The final experimental acceptance test is not the factorized model: measure
the ONE device's complete 36x36 complex transfer matrix M and require
    F_HS = |Tr(U_ideal^dag M)|^2 / (36 Tr(M^dag M)) >= 0.99,
together with the existing visibility and radial-leakage falsifiers.
"""
from __future__ import annotations
import json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_hesse36_photonic_process_calibration_theorem.json"

def main(write=True):
    ret=json.loads((ROOT/"data/w33_hesse36_photonic_coherent_retiming.json").read_text())
    assert ret["schedule"]["channels"]==36
    assert ret["schedule"]["F3_traversals_per_channel"]==1
    assert ret["schedule"]["HOLD_traversals_per_channel"]==1

    F=0.99
    f=F**(1/3)
    phi=math.acos(math.sqrt(f))
    phi_deg=phi*180/math.pi
    s=math.acosh(1/math.sqrt(f))
    L=20/math.log(10)*s
    inf=1-f
    # Numerical closure of the sufficient bound.
    bound=f*(math.cos(phi)**2)*(1/(math.cosh(s)**2))
    assert abs(bound-F)<1e-12

    vals={
      "F_target":round(F,12),
      "per_factor_min":round(f,12),
      "tritter_process_infidelity_max":round(inf,12),
      "hold_phase_rad_max":round(phi,12),
      "hold_phase_deg_max":round(phi_deg,12),
      "hold_differential_power_loss_abs_db_max":round(L,12),
      "hold_differential_power_loss_peak_to_peak_db_max":round(2*L,12),
      "sufficient_product_bound":round(bound,12)
    }
    assert vals=={
      "F_target":0.99,
      "per_factor_min":0.996655493413,
      "tritter_process_infidelity_max":0.003344506587,
      "hold_phase_rad_max":0.057863994222,
      "hold_phase_deg_max":3.31536265468,
      "hold_differential_power_loss_abs_db_max":0.502880974035,
      "hold_differential_power_loss_peak_to_peak_db_max":1.00576194807,
      "sufficient_product_bound":0.99
    }

    out={
      "schema":"w33.hesse36_photonic_process_calibration_theorem.v1",
      "status":"PASS_SYMBOLIC_36_CHANNEL_PROCESS_FIDELITY_BUDGET_AND_SINGLE_DEVICE_CALIBRATION_PROTOCOL",
      "headline":"For the coherent 9+3 retimer, a declared 99% normalized 36-channel process target admits an exact sufficient three-factor budget. Equal allocation requires phase-referenced tritter process fidelity at least 0.996655493413, residual matched-HOLD phase magnitude at most 0.057863994222 rad (3.31536 deg), and differential HOLD power-loss offset at most +/-0.502880974035 dB about the calibrated common loss. The final acceptance criterion is direct tomography of one device's full 36x36 complex transfer matrix, not transplantation of literature efficiencies.",
      "model":{
        "dimension":36,
        "ideal":"12 independent normalized F3 blocks with the coherent 9+3 retiming permutation",
        "conditional_process_fidelity":"F_HS(M)=|Tr(U_ideal^dag M)|^2/(36 Tr(M^dag M)); invariant under a common complex gain",
        "sufficient_bound":"F_model >= F_TRI * cos^2(phi_max) * sech^2((ln10/20)L_max_dB)",
        "amplitude_bound_source":"Kantorovich inequality for positive gains in [exp(-s),exp(s)]",
        "common_loss":"does not enter normalized F_HS; it must be budgeted separately as success/detection probability"
      },
      "design_target":vals,
      "existing_repo_falsifiers":{
        "visibility":ret["coherent_optical_budget"]["visibility_acceptance"],
        "radial_leakage":ret["coherent_optical_budget"]["radial_leakage_acceptance"]
      },
      "single_device_protocol":[
        "phase-reference all nine physical tritters to one optical clock and characterize each 3x3 complex transfer block; absorb block-global phase into the HOLD phase ledger",
        "calibrate the matched HOLD network on all 36 logical paths; subtract common loss/phase and record per-path delta_L and delta_phi",
        "verify F_TRI >= 0.996655493413, |delta_phi| <= 3.315362654680 deg, and |delta_L| <= 0.502880974035 dB as sufficient component gates",
        "run the complete coherent 9+3 schedule on the same hardware stack and reconstruct one 36x36 complex transfer matrix M",
        "accept only if normalized F_HS(M) >= 0.99 AND the existing |delta V(F3)|<=0.05 and radial-leakage<=0.10 falsifiers pass",
        "report absolute common insertion loss, source efficiency and detector efficiency separately; never convert them into conditional process fidelity"
      ],
      "prior_art_boundary":"Published balanced frequency-bin tritters demonstrate that high-fidelity 3x3 mixing is feasible, but their reported fidelity is not assigned to this device. This theorem specifies what the W33/Holonet device itself must measure.",
      "boundary":"The 0.99 target is an engineering design choice, not a prediction. The multiplicative factor budget is a sufficient model under the stated phase-referenced independent-error assumptions; the decisive experimental test is the directly reconstructed full transfer matrix. No physical device measurement is claimed.",
      "parents":["data/w33_hesse36_photonic_coherent_retiming.json"],
      "checks":{
        "one_F3_and_one_HOLD_per_channel":True,
        "target_declared_not_measured":True,
        "equal_factor_budget_closes_exactly":True,
        "phase_bound_derived":True,
        "differential_loss_bound_derived":True,
        "common_loss_separated_from_conditional_fidelity":True,
        "single_device_full_matrix_acceptance_defined":True,
        "existing_falsifiers_retained":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
