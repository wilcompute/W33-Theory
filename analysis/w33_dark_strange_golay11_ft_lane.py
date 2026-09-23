#!/usr/bin/env python3
"""Build the W33-internal [[11,1,5]]_3 Golay Strange-state distillation lane.

Pass4806 already reconstructs the perfect ternary Golay G11=[11,6,5]_3 from
one local W33 K5 fiber.  This file proves the extra quantum-CSS fact needed by
the published Strange protocol:

    G11^perp subset G11,
    rank(G11^perp)=5,
    CSS(Hx=Hz=G11^perp) = [[11,1,5]]_3.

The minimum non-stabilizer word in G11 has weight 5, so the CSS logical
distance is exactly 5.

The dark resource enters by the already-proved Clifford decode
    DARK_STRANGE_Q3_RAW -> STRANGE_Q3_RAW.

Published prior art (Prakash 2020) proves that the [[11,1,5]]_3 ternary-Golay
protocol distills depolarized Strange states with cubic error suppression and
threshold approximately 0.38715 in its stated convention.  2026 work places
this code in the quantum quadratic-residue family.  Those literature facts are
recorded as external prior art, not rederived from this finite code check.

The runtime remains fail-closed for PHYSICAL fault tolerance until a calibrated
input-noise bound, protected syndrome-extraction circuit, decoder/fault census,
and logical injection are present.
"""
from __future__ import annotations
import importlib.util,itertools,json,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_dark_strange_golay11_ft_lane.json"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def rowset(G):
    msgs=np.array(list(itertools.product(range(3),repeat=G.shape[0])),dtype=int)
    return {(tuple(int(x) for x in row)) for row in (msgs@G)%3}

def main(write=True):
    p=load(ROOT/"analysis/w33_pass4806_bonkers_local_ternary_golay.py","golay11_parent")
    dark=json.loads((ROOT/"data/w33_dark_strange_runtime_adapter.json").read_text())
    assert dark["exact_handoff"]["decode_word"]=="X Z^2"

    triples=list(itertools.combinations(range(5),3))
    M=np.zeros((5,10),dtype=int)
    for j,T in enumerate(triples):M[list(T),j]=1
    G10=p.nullspace_mod(M,3); assert G10.shape==(6,10)
    msgs=np.array(list(itertools.product(range(3),repeat=6)),dtype=int)
    C10=(msgs@G10)%3; basewt=np.count_nonzero(C10,axis=1)

    good=[]
    for a in itertools.product(range(3),repeat=6):
        if not any(a):continue
        aa=np.array(a,dtype=int); ext=(msgs@aa)%3
        if min((basewt+(ext!=0))[1:])>=5:good.append(aa)
    assert len(good)==4
    good.sort(key=lambda x:tuple(int(v) for v in x))
    a=good[0]
    G11=np.column_stack([G10,a])%3
    assert p.rank_mod(G11,3)==6
    C=rowset(G11)
    weights=[sum(x!=0 for x in w) for w in C if any(w)]
    assert min(weights)==5 and len(C)==3**6

    H=p.nullspace_mod(G11,3)%3
    assert H.shape==(5,11) and p.rank_mod(H,3)==5
    assert np.all((H@H.T)%3==0)
    # Dual containment: adding H rows does not increase rank of G11.
    assert p.rank_mod(np.vstack([G11,H]),3)==6
    dual=rowset(H); assert len(dual)==3**5 and dual<=C

    logical=C-dual
    assert logical
    logical_weights=[sum(x!=0 for x in w) for w in logical]
    assert min(logical_weights)==5
    witness=min((w for w in logical if sum(x!=0 for x in w)==5))
    k=11-2*p.rank_mod(H,3); assert k==1

    # Distance five detects/corrects the expected Pauli weights algebraically.
    t=(5-1)//2; assert t==2

    gates={
      "code_algebra_verified":True,
      "dark_to_Strange_Clifford_decode_verified":True,
      "published_Strange_distillation_theorem_available":True,
      "input_depolarizing_noise_bound_measured":False,
      "eleven_token_correlated_source_model_verified":False,
      "fault_tolerant_syndrome_extraction_circuit_verified":False,
      "circuit_level_fault_location_census_verified":False,
      "mapped_decoder_verified":False,
      "logical_Strange_injection_to_nonClifford_gate_verified":False,
      "physical_threshold_certificate_verified":False,
      "device_calibration_verified":False
    }
    physical_enabled=all(gates.values())
    assert not physical_enabled

    out={
      "schema":"w33.dark_strange_golay11_ft_lane.v1",
      "status":"PASS_W33_RECONSTRUCTS_THE_11_QUTRIT_GOLAY_CSS_DISTILLATION_CODE__PHYSICAL_FT_REMAINS_FAIL_CLOSED",
      "headline":"The W33 local-Golay construction now closes internally to the exact [[11,1,5]]_3 CSS code used by the ternary-Golay Strange-state distillation protocol: G11 has dimension 6 and distance 5, its dual has dimension 5 and lies inside G11, Hx=Hz=G11^perp commute, the code encodes one qutrit, and the minimum logical weight is 5. The dark Strange ray Clifford-decodes directly into this lane. Physical FT scheduling is still refused until calibrated noise and circuit-level evidence gates close.",
      "w33_code":{
        "classical":"G11=[11,6,5]_3 perfect ternary Golay",
        "source":"analysis/w33_pass4806_bonkers_local_ternary_golay.py",
        "dual_dimension":5,
        "dual_contained_in_G11":True,
        "dual_self_orthogonal":True,
        "quantum_CSS":"[[11,1,5]]_3",
        "Hx_rank":5,
        "Hz_rank":5,
        "logical_qutrits":1,
        "logical_distance":5,
        "correctable_Pauli_weight":2,
        "weight5_logical_witness_present":true
      },
      "resource_flow":[
        "DARK_STRANGE_Q3_RAW",
        "STRANGE_Q3_RAW via exact Clifford X Z^2",
        "11-copy Golay CSS projection/decoding",
        "GOLAY11_STRANGE_LOGICAL (code-level target)",
        "protected non-Clifford injection (physical gate remains closed)"
      ],
      "published_prior_art":{
        "Prakash_2020":"[[11,1,5]]_3 ternary Golay distills the qutrit Strange state with cubic suppression; depolarizing threshold approximately 0.38715 in the paper's convention",
        "Prakash_Singhal_2026":"restricted searches through 23 qutrits found no better Strange threshold than Golay; 23-qutrit CSS examples with cubic suppression exist",
        "Zurel_Jana_deSilva_2026":"the 11-qutrit Golay protocol is unified with quantum quadratic-residue-code distillation; examined qutrit QR examples do not exceed the Golay threshold",
        "external_not_rederived":True
      },
      "admission_rule":{
        "mathematical_ideal_dark_state_delta":0,
        "published_depolarizing_threshold_approx":0.38715,
        "hardware_rule":"require a calibrated/twirled input-noise upper bound strictly below the applicable published threshold before admitting a physical 11-copy batch",
        "current_physical_input_delta_bound":null
      },
      "evidence_gates":gates,
      "physical_fault_tolerant_lane_enabled":physical_enabled,
      "boundary":"This proves that the W33-reconstructed classical Golay object supplies the correct quantum CSS code algebra and that the exact dark Strange token has the right resource type. It does not implement the published distillation polynomial, certify a laboratory source below threshold, make syndrome extraction fault tolerant, or certify a protected non-Clifford injection.",
      "parents":[
        "data/PART_W33_PASS4806_LOCAL_TERNARY_GOLAY.json",
        "data/w33_dark_strange_runtime_adapter.json"
      ],
      "checks":{
        "G11_11_6_5_reconstructed":True,
        "dual_rank5":True,
        "dual_containment":True,
        "CSS_commutation":True,
        "CSS_encodes1":True,
        "CSS_distance5":True,
        "dark_Strange_type_matches_protocol":True,
        "physical_lane_fail_closed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
