#!/usr/bin/env python3
"""Actual 4-mode measurement-basis interferometer compilation for:
 (i) all sixteen published critical 18-ray, nine-tetrad Peres/Reye
 Kochen-Specker configurations; and
 (ii) forty Witting ququart orthogonal tetrad contexts.

Givens triangularization of 4x4 normalized projector basis; minimize
coupler count under free reordering of output labels. Verify complete
unitary reconstruction and all projector effects. Cabello 9-vs-7
noncontextual parity inequality checked exactly, with *conditional*
independent dichotomic readout sign-flip noise threshold.

This is a finite closed-system photonic circuit design, NOT a live
hardware run, device-independent loophole-free KS demonstration,
or a finite-key cryptographic security theorem.
"""
from __future__ import annotations
import itertools,json,math,sys
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
OUT=ROOT/"data"/"toe_20261104_ks18_witting_interferometer_compiler.json"
from analysis.toe_20261104_reye_peres_critical_ks import RAYS,run as ks_reconstruct
from exploration.w33_witting_srg_bridge import construct_witting_rays,witting_orthogonal_tetrads

def givens_unitary(B):
    """B columns are orthonormal; left-adjacent Givens to diagonal phases."""
    n=4
    A=np.array(B,dtype=complex).copy()
    assert A.shape==(4,4) and np.max(abs(A.conj().T@A-np.eye(4)))<1e-11
    blocks=[]
    cumulative=np.eye(n,dtype=complex)
    for j in range(4):
        for row in range(3,j,-1):
            a=A[row-1,j];b=A[row,j]
            if abs(b)<1e-10:continue
            r=math.sqrt(abs(a)**2+abs(b)**2)
            assert r>1e-10
            G=np.eye(n,dtype=complex)
            G[row-1,row-1]=a.conjugate()/r
            G[row-1,row]=b.conjugate()/r
            G[row,row-1]=-b/r
            G[row,row]=a/r
            assert np.max(abs(G.conj().T@G-np.eye(n)))<1e-12
            A=G@A
            cumulative=G@cumulative
            local=G[np.ix_([row-1,row],[row-1,row])]
            blocks.append(dict(modes=[row-1,row],
                amplitudes_before=[float(abs(a)),float(abs(b))],
                mixing_angle_rad=float(math.atan2(abs(b),abs(a))),
                relative_phase_rad=float(np.angle(b)-np.angle(a)),
                exact_Givens_block_real=[[float(z.real) for z in rr] for rr in local],
                exact_Givens_block_imag=[[float(z.imag) for z in rr] for rr in local]))
    assert np.max(abs(A-np.diag(np.diag(A))))<1e-10
    assert np.max(abs(np.abs(np.diag(A))-1))<1e-10
    diagonal=np.diag(A)
    reconstructed=cumulative.conj().T@np.diag(diagonal)
    assert np.max(abs(reconstructed-B))<1e-10
    return blocks,np.angle(diagonal).tolist(),float(np.max(abs(reconstructed-B)))

def optimize_basis(B):
    best=None
    for perm in itertools.permutations(range(4)):
        ordered=B[:,perm]
        blocks,phase,resid=givens_unitary(ordered)
        weighted=(len(blocks),sum(min(x["mixing_angle_rad"],abs(math.pi-x["mixing_angle_rad"]))
                        for x in blocks),perm)
        if best is None or weighted<best["weight"]:
            best=dict(weight=weighted,permutation=list(perm),blocks=blocks,
                phases=phase,max_unitary_residual=resid)
    best.pop("weight")
    best["couplers"]=len(best["blocks"])
    best["phase_shifters_max4"]=sum(abs(x)>1e-8 for x in best["phases"])
    return best

def ks_contexts():
    cert=ks_reconstruct()
    results=[]
    for witness_id,w in enumerate(cert["certificate_rows"]):
        rows=[]
        for tet in w["nine_full_orthogonal_tetrads"]:
            cols=[np.array(RAYS[i-1],dtype=float) for i in tet]
            B=np.column_stack([v/np.linalg.norm(v) for v in cols])
            record=optimize_basis(B)
            record["rays"]=tet
            rows.append(record)
        total=sum(x["couplers"] for x in rows)
        results.append(dict(witness_id=witness_id,
            excluded_six_rays=w["missing_first_12_ray_line"]+w["missing_second_12_ray_line"],
            distinct_rays=18,measurement_contexts=9,
            couplers_per_context=[x["couplers"] for x in rows],
            total_couplers_for_nine_contexts=total,
            worst_case_per_context=max(x["couplers"] for x in rows),
            phase_shifters_total=sum(x["phase_shifters_max4"] for x in rows),
            contexts=rows))
    best=min(results,key=lambda x:(x["total_couplers_for_nine_contexts"],x["worst_case_per_context"],x["witness_id"]))
    return results,best

def witting_contexts():
    W=construct_witting_rays()
    contexts=witting_orthogonal_tetrads()
    assert len(contexts)==40
    rows=[]
    for i,quad in enumerate(contexts):
        B=np.column_stack([W[j] for j in quad])
        record=optimize_basis(B)
        record["basis_index"]=i
        record["ray_labels"]=list(quad)
        rows.append(record)
    return rows

def classical_bound(tetrads):
    # E_r=2|r><r|-I (dichotomic) occurs in exactly two contexts.
    # Each basis product C_j = prod_{r in basis} v_r.
    # Since every ray occurs twice, prod C_j =1, so number C_j=-1
    # is even <=8 among nine: beta=-sum C_j<=7; quantum C_j=-I -> beta=9.
    ids=sorted({r for tet in tetrads for r in tet})
    assert len(ids)==18
    incidence=Counter(r for tet in tetrads for r in tet)
    assert set(incidence.values())=={2}
    assert len(tetrads)==9 and all(len(t)==4 for t in tetrads)
    # Verify tightness with exhaustive 2^18 configurations by XOR parity.
    n=1<<18
    choices=np.arange(n,dtype=np.uint32)
    renumber={v:i for i,v in enumerate(ids)}
    odd_count=np.zeros(n,dtype=np.int8)
    for t in tetrads:
        parity=np.zeros(n,dtype=np.uint32)
        for r in t:parity^=(choices>>renumber[r])&1
        odd_count+=parity.astype(np.int8)
    maxodd=int(odd_count.max())
    assert maxodd==8
    ncmax=2*maxodd-9
    assert ncmax==7
    return ncmax

def main():
    KS,best=ks_contexts()
    W=witting_contexts()
    bound=classical_bound([x["rays"] for x in best["contexts"]])
    wcount=[x["couplers"] for x in W]
    kcount=[x["couplers"] for x in best["contexts"]]
    assert bound==7
    eps=(1-(7/9)**.25)/2
    assert 9*(1-2*eps)**4==7 or abs(9*(1-2*eps)**4-7)<1e-12
    output=dict(status="PASS_KS18_AND_WITTING_4MODE_INTERFEROMETER_COMPILATION",
      theorem_owner="Cabello et al 18 rays/nine contexts; Aravind 2000 sixteen critical Reye constructions (prior art)",
      contextuality_noncontextual_classical_bound=7,
      ideal_quantum_context_product_sum=9,
      context_product_operator="for orthogonal tetrad, prod_r (2P_r-I)=-I4; beta=-sum_context product",
      one_witness_exhaustive_binary_assignments=1<<18,
      conditional_independent_binary_readout_flip_model="Each of four dichotomic observables in one context has independent symmetric sign flip epsilon, so context correlator scaled by (1-2epsilon)^4. NOT the same as 4-port single-click photon readout.",
      independent_sign_flip_epsilon_strictly_below_to_violate=eps,
      nominal_hardware_gate_survival_model="A physical beam splitter per Givens rotation; local phases not costed; all 9 bases executed separately; one photon per context; different contexts require calibration of same ray effect.",
      num_published_critical_18_ray_sets=len(KS),
      best_parity_configuration_id=best["witness_id"],
      best_18ray_nine_contexts_couplers=best["total_couplers_for_nine_contexts"],
      best_18ray_nine_contexts_max_per_context=best["worst_case_per_context"],
      best_18ray_context_gate_counts=kcount,
      best_18ray_contexts=best["contexts"],
      all_16_critical_set_compiled_resource_summary=[{
        k:v for k,v in row.items() if k!="contexts"} for row in KS],
      Witting_40_tetrad_basis_count=len(W),
      Witting_fourmode_couplers_per_context=wcount,
      Witting_total_couplers_for_40_contexts=sum(wcount),
      Witting_average_couplers_per_context=sum(wcount)/len(wcount),
      Witting_all_40_contexts=W,
      maximal_unitary_reconstruction_residual=max(x["max_unitary_residual"] for x in
        best["contexts"]+W),
      phase_gate_warning="Hadamard or internal phase controls and swaps are not fully device-native gate-compiled. This only counts abstract adjacent two-mode Givens mixing blocks; compare per-context not just total across different number of contexts.",
      experimental_boundary="Neither a noise-tolerant generalized contextuality inequality nor a loophole-free experiment is derived. Detection efficiency, postselection bias, contextual equivalence, interferometer cross-talk, source count rate and finite shot significance require explicit calibration.",
      predecessor_files=["analysis/toe_20261104_reye_peres_critical_ks.py",
          "analysis/2026-10-15_toe90_vlasov_witting_research.md",
          "analysis/toe_20261104_tomotope_reye_flux_invariants.py"])
    OUT.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(output["status"],"KS couplers",output["best_18ray_nine_contexts_couplers"],
         "Witting40 total",output["Witting_total_couplers_for_40_contexts"],
         "flip threshold",eps,flush=True)
    return output
if __name__=="__main__":main()
