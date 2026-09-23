#!/usr/bin/env python3
"""Coherence-preserving retiming for the 12-F3 / 9-tritter compiler.

The landed schedule uses 9 tritters for 12 independent qutrit Fourier fibers:
wave0 handles 9 fibers and wave1 handles 3.

For a coherent 36-mode state, simple serialization creates a timing/path-class
asymmetry. A balanced retiming removes it:

  wave0 fibers: F3 at epoch 0, then one matched HOLD;
  wave1 fibers: one matched HOLD, then F3 at epoch 1.

All 36 logical channels therefore experience exactly
  one F3 + one HOLD
and emerge at the same output epoch. The symbolic path loss is uniformly
  L_TRI + L_HOLD,
so deterministic inter-wave attenuation is zero in the matched model.

Measured insertion loss, hold phase noise and tritter process fidelity remain
engineering inputs. The existing visibility/leakage falsifiers are unchanged.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_hesse36_photonic_coherent_retiming.json"

def main(write=True):
    base=json.loads((ROOT/"data/w33_hesse36_photonic_fourier_schedule.json").read_text())
    assert base["schedule"]["fiber_count"]==12
    assert base["schedule"]["tritter_inventory"]==9
    assert [len(x) for x in base["schedule"]["waves"]]==[9,3]

    rows=[]
    for fiber in range(12):
        wave=0 if fiber<9 else 1
        for mode in range(3):
            if wave==0:
                sequence=["F3@epoch0","HOLD@epoch0_to_1","OUT@epoch1"]
                hold_location="post_F3"
            else:
                sequence=["HOLD@epoch0_to_1","F3@epoch1","OUT@epoch1"]
                hold_location="pre_F3"
            rows.append({"fiber":fiber,"mode":mode,"wave":wave,"hold_location":hold_location,"sequence":sequence,
                         "F3_count":1,"HOLD_count":1,"output_epoch":1})
    assert len(rows)==36
    assert {r["F3_count"] for r in rows}=={1}
    assert {r["HOLD_count"] for r in rows}=={1}
    assert {r["output_epoch"] for r in rows}=={1}
    assert sum(r["hold_location"]=="post_F3" for r in rows)==27
    assert sum(r["hold_location"]=="pre_F3" for r in rows)==9

    out={
      "schema":"w33.hesse36_photonic_coherent_retiming.v1",
      "status":"PASS_9_PLUS_3_FOURIER_SCHEDULE_RETIMER_GIVES_UNIFORM_ONE_F3_PLUS_ONE_HOLD_DEPTH",
      "headline":"The 12-F3 compiler can be serialized on nine tritters without creating a deterministic coherent path-depth bias. Hold the 27 wave-0 output channels after their F3 and the 9 wave-1 input channels before their F3. Every logical channel then sees exactly one tritter and one matched storage interval and all 36 outputs emerge at epoch 1.",
      "schedule":{
        "fibers":12,
        "channels":36,
        "tritter_inventory":9,
        "wave_occupancy":[9,3],
        "output_epoch":1,
        "wave0_channels_postheld":27,
        "wave1_channels_preheld":9,
        "F3_traversals_per_channel":1,
        "HOLD_traversals_per_channel":1,
        "active_mixer_depth":1,
        "storage_depth":1
      },
      "coherent_optical_budget":{
        "matched_path_loss_expression":"L_TRI + L_HOLD on every channel",
        "deterministic_interwave_loss_difference_db":"0 in the matched-component model",
        "unmatched_hold_loss_error":"Delta_L_HOLD remains an engineering calibration input",
        "unmatched_hold_phase_error":"Delta_phi_HOLD remains an engineering calibration input",
        "visibility_acceptance":base["optical_budget"]["visibility_acceptance"],
        "radial_leakage_acceptance":base["optical_budget"]["radial_leakage_acceptance"],
        "tritter_process_fidelity_min":None,
        "measured_insertion_loss_db_max":None
      },
      "external_prior_art_boundary":"High-fidelity balanced 3x3 frequency-bin tritters have been demonstrated in the literature, but no external fidelity or loss number is assigned to this W33/Holonet schedule.",
      "magic_boundary":base["magic_boundary"],
      "physics_reading":"The compiler's 9+3 serialization is compatible with coherent superposition across all 36 channels provided the storage stage is treated as part of the interferometer rather than as a classical queue. Retiming is therefore a phase-calibration problem, not an extra Fourier-depth problem.",
      "boundary":"Exact scheduling and symbolic path-depth theorem only. No physical delay-line loss, phase stability, source brightness, detector efficiency, or W33 device process fidelity is claimed.",
      "parents":["data/w33_hesse36_photonic_fourier_schedule.json"],
      "checks":{
        "36_channels":True,
        "9_plus_3_resource_schedule":True,
        "one_F3_each":True,
        "one_HOLD_each":True,
        "common_output_epoch":True,
        "uniform_symbolic_path_loss":True,
        "existing_falsifiers_preserved":True,
        "unmeasured_hardware_numbers_remain_open":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
