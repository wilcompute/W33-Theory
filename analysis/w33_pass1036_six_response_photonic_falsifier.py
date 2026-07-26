#!/usr/bin/env python3
"""Pass 1036: six-response photonic C6 holonomy falsifier."""
from __future__ import annotations

import json
import math
import random
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
OUT=DATA/"w33_pass1036_six_response_photonic_falsifier.json"


def crt_label(sign_bit,phase): return next(z for z in range(6) if z%2==sign_bit and z%3==phase)
def phase_quadrature(phase):
    angle=2*math.pi*phase/3
    return (round(math.cos(angle),15),round(math.sin(angle),15))
def centroid(sign_bit,phase):
    i,q=phase_quadrature(phase)
    return (1.0 if sign_bit==0 else -1.0,i,q)
def distance_sq(x,y): return sum((a-b)**2 for a,b in zip(x,y))
def nearest(sample,codebook): return min(codebook,key=lambda key:distance_sq(sample,codebook[key]))
def monte_carlo(codebook,sigma,trials_per_state,seed):
    rng=random.Random(seed);correct=0;confusion=Counter()
    for label,center in codebook.items():
        for _ in range(trials_per_state):
            sample=tuple(v+rng.gauss(0,sigma) for v in center)
            decoded=nearest(sample,codebook)
            correct+=int(decoded==label);confusion[(label,decoded)]+=1
    total=len(codebook)*trials_per_state
    return {"sigma_per_channel":sigma,"trials":total,"accuracy":correct/total,"errors":total-correct,"off_diagonal_confusions":{f"{a}->{b}":n for (a,b),n in sorted(confusion.items()) if a!=b}}
def unique_projection_count(records,projection): return len({projection(r) for r in records})


def main():
    syndrome=json.loads((DATA/"w33_pass1028_primary_obstruction_syndrome.json").read_text())
    no_switch=json.loads((DATA/"w33_pass1029_no_orientation_switch_inside.json").read_text())
    determinant=json.loads((DATA/"w33_pass1031_complex_determinant_phase_detector.json").read_text())
    correction=json.loads((DATA/"w33_pass1034_selector_correction_torsor.json").read_text())
    realification=json.loads((DATA/"w33_pass1035_determinant_to_s3_realification.json").read_text())
    records=[];codebook={}
    for sign_bit in range(2):
        for phase in range(3):
            z6=crt_label(sign_bit,phase);iq=phase_quadrature(phase);center=centroid(sign_bit,phase)
            records.append({"z6_label":z6,"sign_bit":sign_bit,"phase_mod3":phase,"chirality_channel":center[0],"phase_I":iq[0],"phase_Q":iq[1],"phase_intensity":1.0})
            codebook[z6]=center
    records.sort(key=lambda row:row["z6_label"])
    pairwise={};distance_profile=Counter()
    for a in range(6):
        for b in range(a+1,6):
            d2=round(distance_sq(codebook[a],codebook[b]),12);pairwise[f"{a}-{b}"]=d2;distance_profile[d2]+=1
    minimum_d2=min(pairwise.values());guaranteed_radius=math.sqrt(minimum_d2)/2
    projection_counts={
        "full_chirality_I_Q":unique_projection_count(records,lambda r:(r["chirality_channel"],r["phase_I"],r["phase_Q"])),
        "phase_I_Q_only":unique_projection_count(records,lambda r:(r["phase_I"],r["phase_Q"])),
        "chirality_only":unique_projection_count(records,lambda r:r["chirality_channel"]),
        "chirality_plus_phase_intensity":unique_projection_count(records,lambda r:(r["chirality_channel"],r["phase_intensity"])),
        "chirality_plus_real_quadrature":unique_projection_count(records,lambda r:(r["chirality_channel"],r["phase_I"])),
        "phase_intensity_only":unique_projection_count(records,lambda r:r["phase_intensity"]),
    }
    simulations=[monte_carlo(codebook,sigma,2000,103600+i) for i,sigma in enumerate((0.05,0.15,0.30,0.50))]
    checks={
        "all_source_certificates_pass":all(source["status"]=="PASS" for source in (syndrome,no_switch,determinant,correction,realification)),
        "crt_gives_six_unique_labels":sorted(crt_label(s,p) for s in range(2) for p in range(3))==list(range(6)),
        "six_full_centroids_are_distinct":len(set(codebook.values()))==6,
        "phase_detector_is_sign_blind":determinant["detector_table"]["det_C_on_centraliser"]["detects_sign"] is False,
        "chirality_requires_external_channel":no_switch["checks"]["whole_normaliser_is_orientation_preserving"],
        "full_readout_has_six_signatures":projection_counts["full_chirality_I_Q"]==6,
        "ternary_only_has_three_signatures":projection_counts["phase_I_Q_only"]==3,
        "binary_only_has_two_signatures":projection_counts["chirality_only"]==2,
        "intensity_erases_ternary_phase":projection_counts["phase_intensity_only"]==1,
        "sign_plus_intensity_has_only_two_signatures":projection_counts["chirality_plus_phase_intensity"]==2,
        "one_real_quadrature_has_only_four_signatures":projection_counts["chirality_plus_real_quadrature"]==4,
        "minimum_squared_distance_is_three":abs(minimum_d2-3)<1e-12,
        "guaranteed_bounded_noise_radius_is_sqrt3_over2":abs(guaranteed_radius-math.sqrt(3)/2)<1e-12,
        "correction_frame_is_independent_binary_choice":correction["two_binary_characters"]["joint_image"]=="C2 x C2",
        "scalar_s3_phase_detector_is_impossible":realification["s3_completion"]["one_dimensional_extension_exists"] is False,
        "low_noise_simulation_decodes_all_states":simulations[0]["accuracy"]==1.0,
        "accuracy_degrades_with_noise":all(simulations[i]["accuracy"]>=simulations[i+1]["accuracy"] for i in range(len(simulations)-1)),
    }
    if not all(checks.values()): raise AssertionError([k for k,v in checks.items() if not v])
    result={
        "schema":"w33.pass1036.six_response_photonic_falsifier.python.v1","status":"PASS",
        "headline":"A genuine C6 photonic response requires an external binary chirality readout and a two-quadrature ternary determinant-phase readout. Their CRT product gives six distinct centroids; ternary-only, binary-only, intensity-only, and single-quadrature devices give 3, 2, 1/2, and 4 signatures.",
        "response_table":records,"codebook_coordinates":{str(k):list(v) for k,v in sorted(codebook.items())},"projection_falsifiers":projection_counts,
        "distance_certificate":{"pairwise_squared_distances":pairwise,"squared_distance_profile":{str(k):v for k,v in sorted(distance_profile.items())},"minimum_squared_distance":minimum_d2,"guaranteed_l2_noise_radius":guaranteed_radius,"exact_radius":"sqrt(3)/2"},
        "noise_diagnostics":simulations,
        "protocol":{"prepare":"lock one of the two Pass-1034 correction frames","phase_channel":"I/Q measurement of det_C in {1,omega,omega^2}","chirality_channel":"external orientation-sensitive binary controller outside the Eisenstein normaliser","decode":"nearest centroid then CRT","acceptance":["six joint signatures","three without chirality","two without phase quadratures","Q inversion exchanges omega and omega^2","correction-frame switch changes calibration metadata, not C6 labels"]},
        "checks":checks,"check_count":len(checks),
        "boundary":"Finite detector/noise contract only; no claim a specific optical apparatus already realizes the external chirality channel."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Pass1036 PASS",projection_counts)


if __name__=="__main__": main()
