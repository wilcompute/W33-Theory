#!/usr/bin/env python3
"""One-loop inverse gauge-coupling threshold model builder, independent of W33.

Given observed electroweak inputs, solve for a common BSM multiplet mass
and crossing scale with ONE common step-function threshold. Enumerate a
declared shortlist only, respecting vector-like anomaly cancellation.
NO two-loop thresholds, proton decay rates, mass generation, or TOE claim.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import Counter
from itertools import combinations_with_replacement,product
from pathlib import Path
import math,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_inverse_gauge_threshold_witnesses.json"
MZ=91.1876
SM=(F(41,10),F(-19,6),F(-7))

# One Dirac vectorlike fermion contributes 4/3 T(R), times spectator
# dimension. One Weyl fermion in real rep contributes 2/3 T(R).
# A complex scalar contributes 1/3 T(R). U1 T=(3/5)Y^2
# per component, with SU5 hypercharge normalization.
SPECIES={
 "VL_quark_doublet_3_2_1_6":(F(2,15),F(2),F(4,3)),
 "VL_lepton_doublet_1_2_m1_2":(F(2,5),F(2,3),F(0)),
 "VL_down_singlet_3_1_m1_3":(F(4,15),F(0),F(2,3)),
 "VL_up_singlet_3_1_2_3":(F(16,15),F(0),F(2,3)),
 "VL_charged_singlet_1_1_m1":(F(4,5),F(0),F(0)),
 "Majorana_SU2_adjoint_1_3_0":(F(0),F(4,3),F(0)),
 "Majorana_SU3_adjoint_8_1_0":(F(0),F(0),F(2)),
 "complex_scalar_doublet_1_2_1_2":(F(1,10),F(1,6),F(0)),
 "complex_scalar_triplet_3_1_1_3":(F(1,15),F(0),F(1,6))
}

def initial(alpha_em_inv=127.955,sin2=.23122,alpha_s=.118):
    return np.array([.6*(1-sin2)*alpha_em_inv,
                   sin2*alpha_em_inv,1/alpha_s])

def solve(extra,a0=None):
    if a0 is None:a0=initial()
    b=np.asarray(SM,dtype=float)
    e=np.array(extra,dtype=float)
    D=np.array([[b[0]-b[1],e[0]-e[1]],
                [b[1]-b[2],e[1]-e[2]]],float)
    if abs(np.linalg.det(D))<1e-12:return None
    t,s=np.linalg.solve(D,2*math.pi*np.array([a0[0]-a0[1],a0[1]-a0[2]]))
    if not (0<s<t<math.log(1e19/MZ)):return None
    heavy=MZ*math.exp(t-s);unify=MZ*math.exp(t)
    if heavy<1e3:return None
    result=a0-b*t/(2*math.pi)-e*s/(2*math.pi)
    assert np.max(abs(result-result[0]))<2e-12
    return {"new_common_mass_GeV":float(heavy),
           "triple_crossing_mass_GeV":float(unify),
           "alpha_unified_inverse":float(np.mean(result)),
           "inverse_coupling_residual":float(np.max(abs(result-result[0]))),
           "ln_GUT_over_MZ":float(t),
           "ln_GUT_over_new_mass":float(s),
           "is_two_loop_or_proton_safe":False}

def main():
    names=sorted(SPECIES)
    by_size=Counter()
    hits=[]
    for n in range(1,4):
        for combo in combinations_with_replacement(names,n):
            e=tuple(sum((SPECIES[k][j] for k in combo),F(0)) for j in range(3))
            match=solve(e)
            if match is None:continue
            by_size[n]+=1
            hits.append({"new_multiplets":list(combo),
                  "extra_beta_coefficients":[str(z) for z in e],**match})
    single=[x for x in hits if len(x["new_multiplets"])==1]
    assert len(single)==2,single
    desired={
      "VL_quark_doublet_3_2_1_6":(1.438221135e6,2.417922482e15),
      "Majorana_SU2_adjoint_1_3_0":(8.050978055e6,2.432643145e14)}
    for row in single:
        assert row["new_multiplets"][0] in desired
        x,y=desired[row["new_multiplets"][0]]
        assert abs(row["new_common_mass_GeV"]/x-1)<1e-8
        assert abs(row["triple_crossing_mass_GeV"]/y-1)<1e-8
    envelopes=[]
    for row in single:
        e=tuple(F(s) for s in row["extra_beta_coefficients"])
        masses=[];gut=[]
        for da,ds,dq in product((-.01,.01),(-.00006,.00006),(-.0009,.0009)):
            result=solve(e,initial(127.955+da,.23122+ds,.118+dq))
            assert result is not None
            masses.append(result["new_common_mass_GeV"])
            gut.append(result["triple_crossing_mass_GeV"])
        envelopes.append({"multiplet":row["new_multiplets"][0],
             "specified_electroweak_input_uncertainty_corners":8,
             "new_mass_GeV_min":min(masses),"new_mass_GeV_max":max(masses),
             "GUT_scale_GeV_min":min(gut),"GUT_scale_GeV_max":max(gut)})
    out={
       "status":"PASS_SELECTED_ONE_THRESHOLD_INVERSE_UNIFICATION_SCREEN",
       "assumptions":"minimal SM b_i below a single mass; chosen 1-3 extra species all at one shared mass; 1-loop, no two-loop or threshold splitting",
       "betas_SM":[str(v) for v in SM],
       "representations_and_beta_additions":{k:[str(z) for z in v] for k,v in SPECIES.items()},
       "enumerated_declared_representation_count":len(SPECIES),
       "solutions_count_by_added_species":dict(by_size),
       "valid_single_species_witnesses":single,
       "single_species_corner_uncertainty_envelopes":envelopes,
       "max_species_enumerated":3,
       "all_witnesses":sorted(hits,key=lambda x:
           (len(x["new_multiplets"]),x["new_common_mass_GeV"])),
       "epistemic_boundary":"One-loop apparent convergence is neither a UV completion nor a prediction of BSM masses: they are solved for using measured couplings. Proton decay, representation embeddings, thresholds, two-loop RG, neutrino masses and experimental exclusions require independent checks."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("GAUGE_THRESHOLD_PASS",dict(by_size),
       [(x["new_multiplets"][0],round(x["new_common_mass_GeV"]),
          f'{x["triple_crossing_mass_GeV"]:.4e}') for x in single],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return out
if __name__=="__main__":main()
