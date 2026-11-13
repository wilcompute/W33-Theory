#!/usr/bin/env python3
"""27-mode single-photon E6-compatible magic pulse -> 3-qutrit
repetition encoded magic through EXPLICIT affine Clifford permutation.

Exact Knill-Laflamme for every single X_j^(1,2) error, detect failure
for a single Z_j phase error, and quantify heralded photon-loss limit.
This is a shift-error *subsystem protection*, not a full quantum-error
correcting code against arbitrary single-qutrit errors.
"""
from pathlib import Path
from itertools import product,combinations
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261113_chiral_null_order3_gate as G
OUT=ROOT/"data/toe_20261113_E6_photonic_magic_qutrit_repetition_KL.json"

def det3(A):
    a,b,c=A[0];d,e,f=A[1];g,h,i=A[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)

def affine_clifford(x,y):
    d=tuple((y[i]-x[i])%3 for i in range(3))
    assert any(d)
    choices=[r for r in product(range(3),repeat=3) if sum(r[k]*d[k] for k in range(3))%3==1]
    A=next((np.asarray(rows,dtype=np.int64) for rows in product(choices,repeat=3)
            if det3(rows)%3!=0),None)
    assert A is not None
    M={}
    for address in G.V:
        M[tuple(address)]=tuple(int(t) for t in ((A@(np.asarray(address)-x))%3))
    assert len(set(M.values()))==27
    assert M[x]==(0,0,0) and M[y]==(1,1,1)
    return A,M

def X_on_site(site,power):
    mat=np.zeros((27,27),dtype=np.complex128)
    for i,a in enumerate(G.V):
        b=list(a);b[site]=(b[site]+power)%3
        mat[G.VID[tuple(b)],i]=1
    return mat

def Z_on_site(site,power):
    v=np.array([np.exp(2j*math.pi/3*power*a[site]) for a in G.V])
    return np.diag(v)

def correctability():
    W=np.zeros((27,3),dtype=np.complex128)
    for a in range(3):
        W[G.VID[(a,a,a)],a]=1
    assert np.max(abs(W.conj().T@W-np.eye(3)))==0
    errors=[np.eye(27,dtype=np.complex128)]
    names=["I"]
    for j in range(3):
        for k in (1,2):
            errors.append(X_on_site(j,k));names.append(f"X{j}^{k}")
    record=[]
    for i,E in enumerate(errors):
        for j,F in enumerate(errors):
            P=W.conj().T@E.conj().T@F@W
            assert np.max(abs(P-(np.eye(3) if i==j else np.zeros((3,3)))))<1e-12,(i,j,P)
            record.append([names[i],names[j],bool(i==j)])
    Z=Z_on_site(0,1)
    logical_Z=W.conj().T@Z@W
    assert not np.allclose(logical_Z,logical_Z[0,0]*np.eye(3))
    # All 27 possible independent shifts (including I) acting on a
    # codeword are split into 9 syndrome classes for 2 parity checks.
    p=.02
    prob_weight_le1=(1-p)**3+3*p*(1-p)**2
    assert .998 < prob_weight_le1 < 1
    return {"all_7_shift_error_Knill_Laflamme_pairs":49,
      "single_shift_errors":[n for n in names if n!="I"],
      "all_49_overlap_matrices_are_delta_ab_I3":True,
      "single_Z_error_correctable":False,
      "logical_Z_matrix_diag":[[float(v.real),float(v.imag)] for v in np.diag(logical_Z)],
      "shift_error_distribution":"Each of 3 qutrits independently has I probability (1-p), X/X² each p/2; code correctly recovers any <=1 shift.",
      "shift_error_rate":p,"probability_guaranteed_correctable_weight_le1":prob_weight_le1,
      "arbitrary_single_qudit_distance":1,
      "shift_X_distance":3,
      "information_loss_heralded_photon_erasure":"A vacuum erasure destroys the sole photon carrying the entire logical state; syndrome correction cannot recover the lost photon."}

def main():
    _,terms,_,mapi,roots=R.load()
    packets,Ks=R.pack_roots(roots)
    i,j,sgn=packets[0][0]
    x=tuple(map(int,G.V[int(mapi[i])]))
    y=tuple(map(int,G.V[int(mapi[j])]))
    A,aff=affine_clifford(x,y)
    chosen=Ks[0]
    U=np.eye(27)+math.sqrt(3)/2*chosen+1.5*(chosen@chosen)
    output=U[:,i]
    support=np.flatnonzero(abs(output)>1e-12).tolist()
    assert sorted(support)==[i,j]
    assert abs(abs(output[i])-.5)<1e-12 and abs(abs(output[j])-math.sqrt(3)/2)<1e-12
    assert tuple(aff[x])==(0,0,0) and tuple(aff[y])==(1,1,1)
    assert det3(A)%3 in (1,2)
    kl=correctability()
    out={
      "status":"PASS_EXPLICIT_CLIFFORD_TO_3QUTRIT_REPETITION_SHIFT_CODE_MAGIC",
      "source_E6_packet":0,
      "source_E6_input_index":i,
      "source_E6_output_indices":[i,j],
      "history_pair_addresses":[list(x),list(y)],
      "GL3_affine_coordinate_matrix_mod3":A.tolist(),
      "affine_shift_negates_input_history":list(x),
      "encoded_output_code_basis":["000","111"],
      "encoded_amplitude_magnitudes":[0.5,math.sqrt(3)/2],
      "affine_permutation_is_a_qutrit_Clifford":True,
      "logical_magic_nonstabilizer":"two-support encoded output and a perfect Clifford decoding recover a one-qutrit nonstabilizer with mana ln(1+1/sqrt3)",
      "Knill_Laflamme_shift_subcode":kl,
      "photonic_scope":"The three qutrits are virtual degrees of freedom of ONE photon in 27 paths, not three spatially separate photons; this repetition encoding corrects restricted mode-shift errors, not phase noise or photon loss, and does not yield fault-tolerant multi-photon gates."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":out["status"],"history_pair":out["history_pair_addresses"],
       "affine_matrix":out["GL3_affine_coordinate_matrix_mod3"],
       "KL_pairs":kl["all_7_shift_error_Knill_Laflamme_pairs"],
       "single_Z_corrected":kl["single_Z_error_correctable"],
       "p_le1":kl["probability_guaranteed_correctable_weight_le1"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
