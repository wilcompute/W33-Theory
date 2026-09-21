#!/usr/bin/env python3
"""Unify the certified E8 Z2/Z3/Z4/Z6/Z12 gradings as reductions of Qpsi.

The repository already proves separately that:
  * the Kummer Z4 charge restricts to Qpsi mod 4 on the E6 channels;
  * the CE2 E6+A2 grading has channels g0,g1,g2;
  * Qpsi mod 2 is matter parity;
  * the physical FI projection realizes the CE2 Z3 grading.

The source-locked exact E8 Qpsi channel histogram is strong enough to close the
remaining logical gap: every charge in g0 is 0 mod 3, every charge in g1 is
1 mod 3, and every charge in g2 is 2 mod 3.  Hence CE2/FI grade = Qpsi mod 3.
Together with Kummer grade = Qpsi mod 4, CRT says the old common Z12 grading is
literally Qpsi mod 12.  Its Z6 quotient is Qpsi mod 6 and its Z2 quotient is
matter parity.

This is a charge/grading theorem.  It does not identify the E8 Z12 with the
independent photonic mu_12 scalar phase group.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_qpsi_mod12_unification.json"

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def residue_dims(hist: Counter, n: int):
    out = [0] * n
    for q, mult in hist.items():
        out[q % n] += mult
    return out

def main(write=True):
    qmod = load(
        ROOT / "analysis/w33_qpsi_matter_parity_e8_d8_bridge.py",
        "w33_qpsi_source",
    )
    old = json.loads(
        (ROOT / "data/PART_W33_PASS7081_7096_E8_Z3_Z4_Z12_COMMON_REFINEMENT.json").read_text()
    )
    fi = json.loads(
        (ROOT / "data/w33_physical_fi_e6_a2_z3_grading.json").read_text()
    )
    z6 = json.loads(
        (ROOT / "data/w33_physical_fi_matter_parity_z6_quotient.json").read_text()
    )
    kac = json.loads(
        (ROOT / "data/w33_e8_order6_kac_classification.json").read_text()
    )

    grade = {"g0_e6": 0, "g0_a2": 0, "g1": 1, "g2": 2}
    for channel, hist in qmod.ROOT_QPSI.items():
        assert all(q % 3 == grade[channel] for q in hist), (channel, hist)

    # Aggregate all 240 roots, then add the eight Cartan generators at Qpsi=0.
    hist = Counter()
    for h in qmod.ROOT_QPSI.values():
        hist.update(h)
    assert sum(hist.values()) == 240
    hist[0] += 8
    assert sum(hist.values()) == 248
    assert hist == Counter({0:54, 1:48, -1:48, -2:30, 2:30,
                            -3:16, 3:16, 4:3, -4:3})

    d2 = residue_dims(hist, 2)
    d3 = residue_dims(hist, 3)
    d4 = residue_dims(hist, 4)
    d6 = residue_dims(hist, 6)
    d12 = residue_dims(hist, 12)

    assert d2 == [120, 128]
    assert d3 == [86, 81, 81]
    assert d4 == [60, 64, 60, 64]
    assert d6 == [54, 48, 33, 32, 33, 48]
    assert d12 == [54,48,30,16,3,0,0,0,3,16,30,48]

    # Match every previously frozen layer.
    assert d3 == old["z3_ce2_grading"]["grade_dimensions"]
    assert d4 == old["z4_kummer_spinor_grading"]["grade_dimensions"]
    assert d12 == old["z12_crt_grading_dimensions"]
    assert fi["status"] == "PASS_PHYSICAL_FI_REALIZES_E6_A2_Z3_GRADING"
    assert list(map(int, fi["E8"]["root_grades"].keys())) == [0]
    assert fi["E8"]["fixed_dimension"] == d3[0] == 86
    assert d6 == z6["Z6"]["dimensions"]
    assert kac["structural_FI_x_matter_parity_Z6"]["eigendimensions"] == d6
    assert kac["structural_FI_x_matter_parity_Z6"]["unique_kac_coordinates"] == [2,0,0,0,1,0,0,0,0]

    # Channel-wise object statement for the Z3 factor.
    channel_mod3 = {
        channel: {
            "grade": grade[channel],
            "charges": {str(q): n for q, n in sorted(charges.items())},
            "all_charges_match_grade_mod3": all(q % 3 == grade[channel] for q in charges),
        }
        for channel, charges in qmod.ROOT_QPSI.items()
    }

    out = {
        "schema": "w33.qpsi_mod12_unification.v1",
        "status": "PASS_SINGLE_INTEGER_QPSI_UNIFIES_E8_Z2_Z3_Z4_Z6_Z12",
        "Qpsi_adjoint_histogram": {str(q): n for q, n in sorted(hist.items())},
        "channel_mod3_certificate": channel_mod3,
        "residue_dimensions": {
            "mod2_matter_parity": d2,
            "mod3_CE2_and_physical_FI": d3,
            "mod4_Kummer": d4,
            "mod6_FI_x_matter_parity": d6,
            "mod12_common_refinement": d12,
        },
        "single_charge_law": {
            "Z2": "Qpsi mod 2",
            "Z3": "Qpsi mod 3",
            "Z4": "Qpsi mod 4",
            "Z6": "Qpsi mod 6",
            "Z12": "Qpsi mod 12",
            "order6_generator": "exp(2*pi*i*Qpsi/6)",
            "order12_generator": "exp(2*pi*i*Qpsi/12)",
        },
        "interpretation": "The FI/family Z3 and matter-parity Z2 are not independent discrete labels on the certified E8 channels: they are the mod-3 and mod-2 shadows of one integral Qpsi charge. The older Kummer Z4 and common Z12 grading are the corresponding mod-4 and mod-12 shadows.",
        "literature_crosscheck": "The standard E8 -> SO(10) x SU(3) x U(1) adjoint branching carries charges 0, +/-1, +/-2, +/-3, +/-4 with exactly the representation dimensions used here.",
        "boundary": "This unifies the E8 Lie/representation gradings. It does not identify the E8 Z12 with the independent photonic mu_12 scalar phase group, and it does not prove a matter-parity-preserving D/F-flat heterotic vacuum.",
        "checks": {
            "CE2_grade_equals_Qpsi_mod3_channelwise": True,
            "mod2_matches_matter_parity": True,
            "mod4_matches_Kummer": True,
            "mod6_matches_structural_Z6": True,
            "mod12_matches_common_refinement": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out

if __name__ == "__main__":
    main(True)
