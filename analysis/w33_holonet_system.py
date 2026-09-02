#!/usr/bin/env python3
"""Current Holonet/W33 machine datasheet with corrected QEC boundaries.

This file replaces an older synthesis that identified the explicit
[[66,8,3]]_3 protected store with the standard genus-6 K12 edge surface code.
The current executable frontier separates those objects:

* PROCESSOR / ROUTER: W33 qutrit packet architecture and exact finite compiler;
* PROTECTED STORE: Pass79's explicit block-plus-ancilla [[66,8,3]]_3 stabilizer;
* K12 COMPILER SURFACE: V=12,E=66,F=44,g=6; its standard closed orientable
  homological edge code has k=12 over GF(3), not k=8;
* PHYSICAL FT: still fail-closed pending measured optical calibration and a
  hardware-calibrated physical threshold.

The logical von Neumann self-reproduction analogy remains an architecture-level
comparison only.  It is not a claim of biological self-reproduction or a
completed physical fault-tolerant machine.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    datasheet=[
        {
            "subsystem":"processor",
            "spec":"balanced-ternary/qutrit finite processor; exact Clifford packet layer plus explicit non-Clifford logical T port",
            "substrate":"W33/Sp(4,3) finite architecture",
            "evidence":"exact finite/software",
        },
        {
            "subsystem":"interconnect",
            "spec":"W(3,3)=SRG(40,12,2,4), 240 edge carriers, diameter-2 point graph; routed two-qutrit primitives use shared-point locality",
            "substrate":"W33 point/edge geometry",
            "evidence":"exact finite/software",
        },
        {
            "subsystem":"protected store",
            "spec":"explicit [[66,8,3]]_3 stabilizer: eight cyclic [[5,1,3]]_3 blocks plus 26 frozen Z ancillas",
            "substrate":"Pass79 noncanonical block-plus-ancilla witness",
            "evidence":"exact finite stabilizer witness",
        },
        {
            "subsystem":"K12 compiler surface",
            "spec":"V=12,E=66,F=44,g=6 oriented triangular compiler surface; standard GF(3) edge surface code encodes k=12",
            "substrate":"Reye-K12 orientable completion",
            "evidence":"exact chain-complex parameter audit",
        },
        {
            "subsystem":"clock / tape",
            "spec":"Boerdijk-Coxeter / quasicrystal compiler and Rule-110/UTM software constructions retained as finite architecture layers",
            "substrate":"Holonet compiler/tape work",
            "evidence":"software/combinatorial",
        },
        {
            "subsystem":"physical fault tolerance",
            "spec":"REFUSED until hardware-backed optical primitive calibration and a hardware-calibrated threshold certificate exist",
            "substrate":"optical candidate compiler + circuit-level noise census",
            "evidence":"open physical gate",
        },
    ]
    von_neumann={
        "universal computer":"finite/software universal-computation constructions in the corpus",
        "universal constructor":"gate/compiler/network architecture candidate; physical construction not certified",
        "error-corrected description":"explicit Pass79 [[66,8,3]]_3 store; physical code-switch path remains open",
    }
    three_selves={
        "self-correcting":"logical error-correction architecture",
        "self-replicating":"von Neumann architecture analogy at the logical/software level",
        "self-similar":"quasicrystal/lattice recursive structure",
    }
    correction={
        "old_identification":"[[66,8,3]]_3 = standard genus-6 K12 surface code",
        "status":"RETRACTED_AS_STANDARD_SURFACE_CODE_IDENTIFICATION",
        "reason":"For the committed K12 completion over GF(3), rank(d1)=11 and rank(d2)=43, so k=66-11-43=12=2g. A K12-native k=8 construction would require four additional independent constraints.",
        "replacement":"Keep the explicit Pass79 [[66,8,3]]_3 protected store distinct from the 66-edge K12 compiler surface.",
    }
    out={
        "schema":"w33.holonet-system-datasheet.v2",
        "status":"PASS_WITH_PHYSICAL_FT_OPEN",
        "datasheet":datasheet,
        "von_neumann":von_neumann,
        "three_selves":three_selves,
        "qec_correction":correction,
        "summary":"The current machine stack has exact finite/software processor, W33 routing, optical candidate compilation, mapped decoding, an explicit noncanonical [[66,8,3]]_3 protected store, and a separate genus-6 K12 compiler surface whose standard surface-code k is 12. Physical fault tolerance remains fail-closed pending measured calibration and a physical threshold.",
        "sources":[
            "w33_pass79_full_closure.py",
            "analysis/w33_reye_k12_orientable_horizon_completion.py",
            "analysis/w33_qutrit_20_7_2_to_66_bridge.py",
            "analysis/w33_qutrit_20_7_2_adapter_attack.py",
        ],
    }
    path=ROOT/"data/w33_holonet_system.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
