#!/usr/bin/env python3
"""Exact 27/12/1 Witting phase sites and POVM normalization obstruction.

The 27 universal sites span rank 15 out of the 16D operator space, but
the missing Q has nonzero trace. Thus they ARE informationally complete
for trace-normalized states when measured separately. They cannot by
themselves sum to an identity-normalized rank-one POVM; the 12 blocked
sites repair this and yield an exact 39-effect IC POVM.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import toe_20261122_witting_one_phase_three_fixed as W
import toe_20261122_witting_minimal_lie_control as L
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_control_observation_duality.json'
PRIMES=L.PRIMES

def projectors(p):
    mats=[]
    for v,vc in L.all_witting_rays(p):
        norm=sum(int(x)*int(y) for x,y in zip(v,vc))%p
        assert norm!=0
        P=np.array(L.outer(v,vc,p),dtype=np.int64).reshape(4,4)*pow(norm,-1,p)%p
        assert np.array_equal(P@P%p,P)
        assert np.trace(P)%p==1
        mats.append(P)
    return mats

def verify():
    perms=W.permutations()
    O27=sorted(W.orbit_and_paths(perms))
    O12=sorted(set(range(40))-set(O27)-{25})
    assert len(O27)==27 and len(O12)==12
    cert=[]
    for p in PRIMES:
        mats=projectors(p)
        I=np.eye(4,dtype=np.int64)
        Lline=mats[25]
        Q=(3*Lline-I)%p
        s27=sum((mats[i] for i in O27),np.zeros((4,4),dtype=np.int64))%p
        s12=sum((mats[i] for i in O12),np.zeros((4,4),dtype=np.int64))%p
        assert np.array_equal(s27,(6*I+3*Lline)%p)
        assert np.array_equal(s12,4*(I-Lline)%p)
        assert all(int(np.trace(Q@mats[i])%p)==0 for i in O27)
        assert all(int(np.trace(Q@mats[i])%p)==p-1 for i in O12)
        assert np.array_equal((s27*pow(9,-1,p)+s12*pow(12,-1,p))%p,I%p)
        r27=L.modular_rank([mats[i].reshape(16).tolist() for i in O27],p)
        r39=L.modular_rank([mats[i].reshape(16).tolist() for i in O27+O12],p)
        assert r27==15 and r39==16
        assert L.modular_rank([mats[i].reshape(16).tolist() for i in O27]+[I.reshape(16).tolist()],p)==16
        assert int(np.trace(Q)%p)==(p-1)
        for j in O12:
            assert L.modular_rank([mats[i].reshape(16).tolist() for i in O27+[j]],p)==16
        cert.append(dict(prime=p,universal_27_span_rank=r27,union_39_span_rank=r39,
          each_blocked_ray_repairs_linear_observation=True,
          tight_POVM_in_normalized_field=True))
    # Physical complex-number independent state/control sample.
    roots=W.all_rays(); cv=lambda z:complex(float(z[0])-float(z[1])/2,float(z[1])*np.sqrt(3)/2)
    v=np.array([cv(z) for z in roots[25]]);v=v/np.linalg.norm(v)
    Lline=np.outer(v,v.conj());Q=3*Lline-np.eye(4)
    rp=np.eye(4)/4+Q/16;rm=np.eye(4)/4-Q/16
    assert np.min(np.linalg.eigvalsh(rp))>0 and np.min(np.linalg.eigvalsh(rm))>0
    assert abs(np.linalg.norm(rp-rm,ord='nuc')/2-5/16)<1e-12
    assert abs(np.trace(rp).real-15/16)<1e-12
    assert abs(np.trace(rm).real-17/16)<1e-12
    # These are UNNORMALIZED positive operators, NOT density matrices.
    # Normalizing by trace makes the two states distinguishable.
    rho_p=rp/np.trace(rp);rho_m=rm/np.trace(rm)
    ps=[]
    for j in range(40):
        u=np.array([cv(z) for z in roots[j]]);u/=np.linalg.norm(u)
        ps.append(np.outer(u,u.conj()))
    assert all(abs(np.trace((rp-rm)@ps[j]))<1e-12 for j in O27)
    assert any(abs(np.trace((rho_p-rho_m)@ps[j]))>1e-3 for j in O27)
    assert all(abs(np.trace((rp-rm)@ps[j])+1/8)<1e-12 for j in O12)
    assert np.linalg.norm(sum((ps[j]/9 for j in O27),np.zeros((4,4),dtype=complex))+
                          sum((ps[j]/12 for j in O12),np.zeros((4,4),dtype=complex))-np.eye(4))<1e-12
    return dict(status='PASS_WITTING_UNIVERSAL_SITE_POVM_NORMALIZATION_COMPLEMENTARITY',date='2026-11-22',
      fixed_ray=25,universal_phase_sites=O27,nonuniversal_orthogonal_sites=O12,
      dimensions={'complex_matrix_operator_space':16,'universal_orbit_span':15,'all39_span':16,'universal_orbit_plus_trace_span':16},
      universal_orbit_sum='sum_O27 P = 6 I + 3 P25',
      blocked_orbit_sum='sum_O12 P = 4 (I - P25)',
      exact_tight_POVM='E_j=P_j/9 (27 orbit) and E_j=P_j/12 (12 orbit); sum E_j=I4',
      missing_observable='Q=3P25-I4, Hilbert-Schmidt orthogonal to all 27 orbit projectors but Tr(Q)=-1; trace-normalized states are still fully distinguishable',
      two_positive_UNNORMALIZED_operators='A,B=I/4 +/- (3P25-I)/16; traces(A,B)=(15/16,17/16); same raw 27-site intensities but NOT normalized quantum states',
      unnormalized_operators_half_trace_norm_distance=5/16,
      affine_state_tomography_with_known_trace_is_complete=True,
      blocked_projector_probing_probability_difference=-1/8,
      modular_certificates=cert,
      physical_limit='27 separate yes/no projective settings plus trace normalization are already informationally complete for physical density states. But 27 rank-one effects alone cannot sum to I; a 39-effect weighted POVM is mathematically complete. Joint unknown photon flux remains unidentifiable with 27 raw rates. Actual Naimark/measurement hardware and SPAM remain open.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(d,indent=2)+'\n');print(d['status'])
if __name__=='__main__':main()
