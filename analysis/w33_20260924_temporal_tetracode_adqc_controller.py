#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260924_temporal_tetracode_adqc_controller.json"
RTL=ROOT/"rtl/w33_temporal_tetracode_adqc_controller.v"
TB=ROOT/"tests/rtl/tb_w33_temporal_tetracode_adqc_controller.v"

from analysis.w33_affine_tetracode_e8_glue_bridge import (
    STANDARD_TETRACODE_GENERATORS,
)
from analysis.w33_20260924_single_photon_adqc_qutrit_universality import (
    build_operators, single_register_kraus,
)

TOL=2e-12
C3_PERM=(0,2,3,1)

def mod3(x):
    return int(x)%3

def history(n):
    n0,n1,n2,n3=map(int,n)
    return (
        mod3(n1+n2+n3),
        mod3(n2+2*n3),
        mod3(n0+n2+n3),
    )

def syndrome(n):
    n0,n1,n2,n3=map(int,n)
    return mod3(n0+n2+2*n3)
def plane(n):
    return history(n)[0]==0

def gauge_shift(n):
    s=syndrome(n)
    return (-s)%3

def add_common(n,g):
    return tuple((int(x)+g)%3 for x in n)

def c3(n):
    return tuple(int(n[C3_PERM[i]]) for i in range(4))

def span(gens):
    out=set()
    for a,b in itertools.product(range(3),repeat=2):
        v=(a*np.array(gens[0])+b*np.array(gens[1]))%3
        out.add(tuple(map(int,v)))
    return out

def analyzer_certificate():
    omega,F,X,Z,CZ,E,plus=build_operators()
    programs={
      "F_ID":[0.0,0.0,0.0],
      "PW_FORWARD_Z":[0.0,2*math.pi/3,4*math.pi/3],
      "PW_REVERSE_ZINV":[0.0,4*math.pi/3,2*math.pi/3],
      "UNIVERSAL_T_MU9":[0.0,2*math.pi/9,16*math.pi/9],
    }
    rows={}
    for name,phases in programs.items():
        basis,branches=single_register_kraus(F,X,E,plus,phases)
        berr=float(np.linalg.norm(basis.conj().T@basis-np.eye(3)))
        errs=[float(np.linalg.norm(K-target)) for _,K,target in branches]
        probs=[float(np.linalg.norm(K.conj().T@K-np.eye(3)/3)) for _,K,_ in branches]
        assert max([berr]+errs+probs)<TOL
        rows[name]={
          "phases_rad":phases,
          "basis_unitarity_error":berr,
          "max_branch_error":max(errs),
          "max_probability_error":max(probs),
        }
    return rows
def main():
    T=span(STANDARD_TETRACODE_GENERATORS)
    assert len(T)==9
    all_words=list(itertools.product(range(3),repeat=4))

    rows=[]
    plane_words=0
    fixed_words=set()
    hist_fibres=Counter()
    for n in all_words:
        h=history(n)
        hist_fibres[h]+=1
        is_plane=plane(n)
        if is_plane:
            plane_words+=1
            g=gauge_shift(n)
            nf=add_common(n,g)
            assert history(nf)==h
            assert syndrome(nf)==0
            assert nf in T
            fixed_words.add(nf)
            # C3 leaves the quotient plane and the chosen tetracode gauge intact.
            nc=c3(n)
            assert plane(nc)
            assert syndrome(nc)==syndrome(n)
            assert c3(nf) in T
        rows.append({
          "counter_word":list(n),
          "history":list(h),
          "tetracode_plane":is_plane,
          "gauge_syndrome":syndrome(n),
          "common_mode_correction":gauge_shift(n) if is_plane else None,
        })

    assert set(hist_fibres.values())=={3} and len(hist_fibres)==27
    assert plane_words==27
    assert fixed_words==T

    # Each of the nine program histories has exactly three common-mode gauges.
    plane_hist=Counter(tuple(r["history"]) for r in rows if r["tetracode_plane"])
    assert len(plane_hist)==9 and set(plane_hist.values())=={3}

    analyzers=analyzer_certificate()
    # Existing Page-Wootters certificate supplies the exact c+/-p phase support.
    pw=json.loads(
        (ROOT/"data/w33_20260924_page_wootters_diagonal_weld.json").read_text()
    )
    assert pw["page_wootters"]["forward_equals_plus_zero_set"] is True
    assert pw["page_wootters"]["reverse_equals_minus_zero_set"] is True

    # Existing universality certificate keeps the non-Clifford resource in analyzer programming.
    adqc=json.loads(
        (ROOT/"data/w33_20260924_single_photon_adqc_qutrit_universality.json").read_text()
    )
    assert adqc["status"]=="PASS_FIXED_INTERACTION_ADAPTIVE_MEASUREMENT_QUTRIT_UNIVERSALITY"
    assert "measurement" in adqc["non_clifford_gate"]["analyzer_resource_statement"]

    # Parallel Pass 10941 lowers the same ideal T analyzer into the seven-qutrit VM.
    vm_bridge=json.loads(
        (ROOT/"data/w33_pass10941_qutrit_universal_instruction_bridge.json").read_text()
    )
    assert vm_bridge["status"]=="PASS_SEVEN_QUTRIT_CLIFFORD_T_ABI_WITH_RESOURCE_CONSERVATION"
    lowering=vm_bridge["seven_qutrit_clifford_lowering"]
    analyzer=vm_bridge["nonclifford_resource_equivalence"]["programmed_analyzer"]
    assert lowering["all_25_vm_generators_lowered_exactly_mod3"] is True
    assert lowering["maximum_clifford_macro_length"]==7
    assert [r["zeta9_exponents"] for r in analyzer["analyzer_vectors"]]==[
        [0,8,1],[0,5,4],[0,2,7]
    ]

    # Truth-table checksum is a hardware/compiler ABI lock.
    payload=";".join(
        f"{''.join(map(str,n))}:{''.join(map(str,history(n)))}:{int(plane(n))}:{syndrome(n)}:{gauge_shift(n) if plane(n) else 9}"
        for n in all_words
    )
    truth_hash=hashlib.sha256(payload.encode()).hexdigest()
    assert RTL.exists(),f"missing RTL: {RTL}"
    assert TB.exists(),f"missing RTL testbench: {TB}"
    rtl_hash=hashlib.sha256(RTL.read_bytes()).hexdigest()
    tb_hash=hashlib.sha256(TB.read_bytes()).hexdigest()

    out={
      "schema":"w33.20260924.temporal_tetracode_adqc_controller.v1",
      "status":"PASS_TETRACODE_RELATIVE_MODE_COMPILED_TO_PHOTONIC_ADQC_CONTROLLER",
      "four_channel_abi":{
        "channel_order":["infinity","zero","plus","minus"],
        "counter_domain":"F3^4",
        "history_map":[
          "a=n_zero+n_plus+n_minus",
          "b=n_plus+2*n_minus",
          "c=n_infinity+n_plus+n_minus",
        ],
        "common_mode_kernel":"<1111>",
        "histories":27,
        "representatives_per_history":3,
      },
      "tetracode_program_plane":{
        "quotient_condition":"history a=0",
        "program_histories":len(plane_hist),
        "counter_words_over_plane":plane_words,
        "gauge_syndrome":"sigma=n_infinity+n_plus+2*n_minus",
        "gauge_fix":"add -sigma to all four counters; history unchanged",
        "unique_tetracode_representatives":len(fixed_words),
        "all_standard_tetracode_words_recovered":fixed_words==T,
        "C3_channel_permutation":[0,2,3,1],
        "C3_preserves_plane_and_gauge":True,
      },
      "analyzer_programs":{
        "0_F_ID":analyzers["F_ID"],
        "1_PW_FORWARD_Z":analyzers["PW_FORWARD_Z"],
        "2_PW_REVERSE_ZINV":analyzers["PW_REVERSE_ZINV"],
        "3_UNIVERSAL_T_MU9":analyzers["UNIVERSAL_T_MU9"],
        "program_id_width":2,
        "Page_Wootters_forward":"R=Z implements the + orientation finite clock program",
        "Page_Wootters_reverse":"R=Z^-1 implements the reversed finite clock program",
        "universality_boundary":(
          "the tetracode/mu12 sector organizes finite clock and Clifford control; "
          "approximate universality still requires the separate mu9 T analyzer program"
        ),
      },
      "parallel_pass10941_vm_bridge":{
        "status":vm_bridge["status"],
        "target":lowering["target"],
        "all_25_vm_generators_lowered_exactly_mod3":True,
        "maximum_clifford_macro_length":7,
        "same_T_analyzer_Z_orbit":True,
        "resource_boundary":vm_bridge["nonclifford_resource_equivalence"]["consequence"],
      },
      "rtl":{
        "path":"rtl/w33_temporal_tetracode_adqc_controller.v",
        "testbench":"tests/rtl/tb_w33_temporal_tetracode_adqc_controller.v",
        "exhaustive_software_truth_table_cases":len(all_words),
        "truth_table_sha256":truth_hash,
        "rtl_source_sha256":rtl_hash,
        "testbench_source_sha256":tb_hash,
        "external_verilog_simulator_available":False,
        "simulation_status":"testbench supplied; no external Verilog simulator was available for this certification",
      },
      "rows":rows,
      "theorem":(
        "The four null/Hesse/A2 counters compile directly to a hardware-friendly "
        "three-trit history address with common mode <1111> removed. The temporal "
        "tetracode program sector is exactly the nine quotient histories satisfying "
        "a=0. Every one of their three counter gauges has a unique common-mode "
        "correction into the standard tetracode, and the tetracode-selected C3 "
        "preserves both the plane and that gauge syndrome. The same fixed ADQC "
        "interaction realizes F, Page-Wootters Z/Z^-1, and the independent mu9 T "
        "program solely by changing the three-outcome analyzer basis."
      ),
      "boundary":(
        "This is a verified controller/compiler ABI plus exact finite-dimensional "
        "ADQC gate identities, not a fabricated photonic device. Loss, detector "
        "efficiency, analog phase fidelity, memory-photon coupling and fault-"
        "tolerance thresholds remain physical engineering requirements."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "plane_histories":len(plane_hist),
      "truth_hash":truth_hash,
      "analyzer_max_error":max(
        v["max_branch_error"] for v in analyzers.values()
      ),
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
