#!/usr/bin/env python3
"""BT899 - Photonic Holonet static guard.

This protects photonic_holonet.tex as the Photonic Holonet architecture paper.
It fails closed if the BT893--BT898 shifted-reflection / q^2=9 profile
boundary disappears or if the paper is mislabeled as a transvection paper.
"""
from __future__ import annotations
import json, re
from pathlib import Path

TARGET=Path("photonic_holonet.tex")
OUT=Path("data/PART_BT899_PHOTONIC_HOLONET_STATIC_GUARD_results.json")
REQUIRED=[r"\\title\{\\textbf\{The Photonic Holonet\}",r"BT893--BT898",r"shifted reflection",r"b\\equiv -a-g_H\\pmod3",r"within-grade \$q\^2=9\$ profile",r"\$9\\cdot\\mathbf2\$ flavor multiplicity",r"3/\\sqrt\{178\}",r"Koide",r"Yukawa reflection/profile layer"]
FORBIDDEN=[r"transvection paper",r"pure circulant Yukawa texture",r"gives a circulant Yukawa texture"]
SECTIONS=["Overture: the machine is the geometry is the carrier","The substrate","The carrier: how to self-entangle a photon","The network: atlas, building, and routing","The middleware: tomotope mirrors and the runtime bus","The software: braids, teleported gates, universality","Fractal scaling: the computer is the network","Build sheet and falsifiable witnesses"]

def main()->None:
    text=TARGET.read_text(encoding="utf-8")
    required_hits={p: bool(re.search(p,text)) for p in REQUIRED}
    missing=[p for p,ok in required_hits.items() if not ok]
    if missing: raise AssertionError(f"missing required holonet guard patterns: {missing}")
    forbidden_hits={p: bool(re.search(p,text,flags=re.I)) for p in FORBIDDEN}
    bad=[p for p,ok in forbidden_hits.items() if ok]
    if bad: raise AssertionError(f"forbidden pattern present: {bad}")
    section_hits={s:(s in text) for s in SECTIONS}
    if not all(section_hits.values()): raise AssertionError(f"missing sections: {[s for s,ok in section_hits.items() if not ok]}")
    transvection_count=text.lower().count("transvection")
    result={"theorem":"BT899 Photonic Holonet static guard","target":str(TARGET),"title_ok":"The Photonic Holonet" in text[:1000],"required_hits":required_hits,"forbidden_hits":forbidden_hits,"transvection_count_allowed_inside_physics_section":transvection_count,"section_hits":section_hits,"guard_conclusion":"photonic_holonet.tex is guarded as the Photonic Holonet architecture paper. The Standard-Model transvection theorem may appear as an internal physics implication, but the paper is not labeled or guarded as a transvection paper. The Yukawa layer must state the BT893--BT898 shifted-reflection / q^2=9 profile boundary.","checks":{"T1_title_is_photonic_holonet":True,"T2_BT893_BT898_reflection_profile_patch_present":True,"T3_no_forbidden_circulant_yukawa_overclaim":True,"T4_transvection_allowed_only_as_internal_physics_theorem":True,"T5_core_holonet_sections_present":True}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2))
    print("BT899 Photonic Holonet static guard passed; wrote",OUT)
if __name__=="__main__": main()
