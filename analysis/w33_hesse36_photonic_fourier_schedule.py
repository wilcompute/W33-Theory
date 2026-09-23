#!/usr/bin/env python3
"""Photonic lowering of the full Clifford648 Hesse36 Fourier compiler.

The exact compiler is twelve independent normalized F3 transforms. The current
Pass409 vendor-neutral demonstrator inventories nine balanced qutrit Fourier
tritters, so the compiler schedules in two waves: 9 fibers then 3 fibers.

This increases scheduler makespan to two tritter waves but does NOT place two
Fourier elements in series on any logical channel: every one of the 36 channels
traverses exactly one F3. Thus the active mixer optical depth per channel is one.

No fabricated insertion-loss or process-fidelity number is introduced. The
existing protocol provides only the falsifier thresholds |delta V(F3)|<=0.05
and radial leakage<=0.10; Pass409 explicitly leaves tritter process fidelity
and insertion loss unspecified. M36 injection remains refused because this
compiler is Clifford-only.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_hesse36_photonic_fourier_schedule.json"

def main(write=True):
    compiler=json.loads((ROOT/"data/w33_hesse36_full_clifford648_fourier_compiler.json").read_text())
    bom=json.loads((ROOT/"data/w33_pass409_vendor_neutral_bom.json").read_text())
    proto=json.loads((ROOT/"data/bt1575_full_protocol_table_for_paper.json").read_text())
    leakage=json.loads((ROOT/"data/bt1581_radial_leakage_pass_fail_simulator.json").read_text())
    hard=json.loads((ROOT/"data/PART_BT2820_BT2824_BLUEPRINT_HARDENING_results.json").read_text())
    assert compiler["compiler"]["fiber_count"]==12
    tri=next(x for x in bom["component_classes"] if x["id"]=="TRI-9")
    assert tri["quantity"]==9
    assert tri["required_specifications"]["unitary_process_fidelity_min"] is None
    assert tri["required_specifications"]["insertion_loss_db_max"] is None
    f3row=next(x for x in proto["rows"] if x["operation"]=="F3")
    assert f3row["threshold"]=="|delta V| <= 0.05"
    assert leakage["thresholds"]=={"radial_leakage":0.1,"visibility_error":0.05}

    fibers=list(range(12))
    waves=[fibers[:9],fibers[9:]]
    assert list(map(len,waves))==[9,3]
    channels=[(fiber,mode) for fiber in fibers for mode in range(3)]
    assert len(channels)==36
    traversals={ch:1 for ch in channels}
    assert set(traversals.values())=={1}

    phase_degrees=[0,120,240]
    amplitude="1/sqrt(3)"
    # Parametric engineering budget; no unmeasured numeric loss is asserted.
    budget={
      "active_F3_elements_per_channel":1,
      "scheduler_tritter_waves":2,
      "wave_occupancy":[{"wave":0,"used":9,"available":9},{"wave":1,"used":3,"available":9}],
      "normalized_F3_amplitude_per_path":amplitude,
      "phase_alphabet_degrees":phase_degrees,
      "per_channel_insertion_loss_db":"L_TRI (one tritter traversal)",
      "second_wave_extra_storage_loss_db":"L_HOLD if a physical delay is required; not measured",
      "worst_path_loss_expression":"L_TRI + L_HOLD for delayed wave; L_TRI for first wave",
      "visibility_acceptance":"|delta V(F3)| <= 0.05",
      "radial_leakage_acceptance":"<= 0.10",
      "process_fidelity_min":None,
      "insertion_loss_db_max":None
    }

    out={
      "schema":"w33.hesse36_photonic_fourier_schedule.v1",
      "status":"PASS_12_F3_COMPILER_FIBERS_SCHEDULE_ON_9_TRITTERS_IN_TWO_WAVES_WITH_ONE_ACTIVE_MIXER_PER_CHANNEL",
      "headline":"The full Clifford648 compiler lowers to twelve balanced qutrit F3 transforms. The existing vendor-neutral demonstrator has nine Fourier tritters, so an exact resource schedule is 9+3 over two waves. Every logical channel traverses one and only one active F3 mixer; the second wave is resource serialization, not a second serial Fourier gate. Existing visibility/leakage falsifiers apply unchanged, while insertion loss and process fidelity remain explicitly unmeasured.",
      "schedule":{"fiber_count":12,"channels":36,"waves":waves,"wave_count":2,
                  "tritter_inventory":9,"active_mixer_depth_per_channel":1,
                  "matrix_nonzeros":compiler["compiler"]["nonzero_entries"]},
      "optical_budget":budget,
      "magic_boundary":{"compiler_is_Clifford_only":True,
                         "M36_injection_enabled":False,
                         "M36_status":"unchanged: RAW resource remains refused for injection until a proved protocol exists",
                         "reason":"an F3/Clifford compiler cannot supply the missing non-Clifford magic-state protocol"},
      "prior_art_note":"The repository cites Imany et al. for a measured 3x3 photonic SUM gate at 0.92+/-0.01; that number is not reassigned to the F3 tritter compiler.",
      "boundary":"Control/resource schedule only. No chip layout, insertion loss, phase-noise distribution, source efficiency, or calibrated W33 device measurement is fabricated.",
      "checks":{"twelve_exact_F3_fibers":True,"nine_tritter_inventory":True,"two_wave_9_plus_3_schedule":True,
                "one_active_F3_per_channel":True,"phase_alphabet_is_mu3":True,
                "existing_visibility_threshold_bound":True,"existing_leakage_threshold_bound":True,
                "loss_and_fidelity_left_unmeasured":True,"M36_still_refused":True}
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out
if __name__=="__main__":print(json.dumps(main(True),indent=2))
