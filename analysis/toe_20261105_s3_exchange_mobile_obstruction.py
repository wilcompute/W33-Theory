#!/usr/bin/env python3
"""S3 27-history operator-level obstruction and minimal mobile-matter extension.

Base model: toe_20261105_s3_nonabelian_matter_gauge.py.
The exact 17+10 exchange-parity split obstructs identifying its specific
E,M,C operator algebra with a full irreducible 27-dimensional Weyl algebra.
It does NOT forbid abstract Hilbert isomorphisms or an unrelated H27 action.
The gauge-fixed two-vertex, three-parallel-link one-particle model has 18,
not 27, invariant states, despite two independent holonomy loops.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
from toe_20261105_s3_nonabelian_matter_gauge import PERMS, INDEX, TRANS, mul, inv, irrep
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_s3_27_exchange_mobile_no_go.json"

def matrix_family(color_kind):
    """Color: tensor 2x2 if fixed two species, direct sum 2+2 if mobile."""
    rep=irrep()
    n=144
    gauge=[]
    for h in PERMS:
        u=np.zeros((n,n))
        hi=inv(h)
        color=(np.kron(rep[INDEX[h]],rep[INDEX[h]]) if color_kind=="tensor"
               else np.kron(np.eye(2),rep[INDEX[h]]))
        for i,g in enumerate(PERMS):
            a=INDEX[mul(mul(h,g),hi)]
            for j,k in enumerate(PERMS):
                b=INDEX[mul(mul(h,k),hi)]
                u[4*(6*a+b):4*(6*a+b)+4,4*(6*i+j):4*(6*i+j)+4]=color
        gauge.append(u)
    P=sum(gauge)/6
    assert np.max(abs(P@P-P))<2e-13
    E=np.zeros((n,n));M=np.zeros((n,n));C=np.zeros((n,n))
    for i,g in enumerate(PERMS):
        for j,k in enumerate(PERMS):
            q=6*i+j; sl=slice(4*q,4*q+4)
            for t in TRANS:
                a=INDEX[mul(t,g)]; b=INDEX[mul(t,k)]
                E[sl,slice(4*(6*a+j),4*(6*a+j)+4)]-=np.eye(4)/3
                E[sl,slice(4*(6*i+b),4*(6*i+b)+4)]-=np.eye(4)/3
            c=mul(mul(mul(g,k),inv(g)),inv(k))
            M[sl,sl]=-(np.trace(rep[INDEX[c]])/2)*np.eye(4)
            if color_kind=="tensor":
                Rg=(rep[i]+rep[i].T)/2;Rk=(rep[j]+rep[j].T)/2
                C[sl,sl]=-.5*(np.kron(Rg,np.eye(2))+
                               np.kron(np.eye(2),Rk))
            else:
                # Site-U to site-V transport on two loop edges, with one
                # chosen spanning-tree edge gauge fixed to the identity.
                hop=(rep[i]+rep[j]+np.eye(2))/3
                C[sl,sl]= -np.block([[np.zeros((2,2)),hop],
                                      [hop.T,np.zeros((2,2))]])
    for X in (E,M,C):
        assert np.max(abs(X-X.T))<5e-13
        assert max(np.max(abs(X@u-u@X)) for u in gauge)<5e-13
    eig,V=np.linalg.eigh(P)
    F=V[:,eig>.5]
    assert np.max(abs(F.T@F-np.eye(F.shape[1])))<2e-12
    return rep,gauge,P,(E,M,C),F

def exchange_obstruction():
    rep,gauge,P,operators,F=matrix_family("tensor")
    n=144
    S=np.zeros((n,n))
    for i in range(6):
        for j in range(6):
            for a in range(2):
                for b in range(2):
                    before=4*(6*i+j)+2*a+b
                    after=4*(6*j+i)+2*b+a
                    S[after,before]=1
    assert np.array_equal(S@S,np.eye(n))
    assert max(np.max(abs(S@u-u@S)) for u in gauge)<1e-13
    assert max(np.max(abs(S@X-X@S)) for X in operators)<1e-13
    B=F.T@S@F
    assert np.max(abs(B@B-np.eye(27)))<3e-12
    rank_plus=int(round((27+np.trace(B))/2))
    rank_minus=27-rank_plus
    assert abs(np.trace(P@S)-7)<3e-12
    assert rank_plus==17 and rank_minus==10
    # Analytic Burnside trace: |C(h²)|*chi_2(h²).
    traces=[]
    for h in PERMS:
        h2=mul(h,h)
        cent=sum(mul(h2,g)==mul(g,h2) for g in PERMS)
        term=cent*np.trace(rep[INDEX[h2]])
        traces.append(int(round(term)))
    assert sorted(traces)==[-3,-3,12,12,12,12] and sum(traces)==42
    H=0.6*operators[0]+0.8*operators[1]+.4*operators[2]
    Hp=F.T@H@F
    vals=np.linalg.eigvalsh(Hp)
    blocks=[]
    for sign,dim in ((1,17),(-1,10)):
        w,U=np.linalg.eigh(B)
        Q=U[:,w*sign>.5]
        assert Q.shape[1]==dim
        evals=np.linalg.eigvalsh(Q.T@Hp@Q)
        blocks.append({"exchange_eigenvalue":sign,"dimension":dim,
                       "lowest_four_energies":evals[:4].tolist()})
    assert np.max(abs(B@Hp-Hp@B))<3e-12
    # Gauge-invariant difference between the two electric loop couplings
    # is exchange-ODD. This removes the *specific* parity obstruction,
    # without proving the enlarged generators form Mat_27(C).
    delta=np.zeros((144,144))
    for i,g in enumerate(PERMS):
        for j,k in enumerate(PERMS):
            sl=slice(4*(6*i+j),4*(6*i+j)+4)
            for t in TRANS:
                a=INDEX[mul(t,g)];b=INDEX[mul(t,k)]
                delta[sl,slice(4*(6*a+j),4*(6*a+j)+4)]-=np.eye(4)/3
                delta[sl,slice(4*(6*i+b),4*(6*i+b)+4)]+=np.eye(4)/3
    assert max(np.max(abs(delta@u-u@delta)) for u in gauge)<1e-13
    assert np.max(abs(S@delta@S+delta))<1e-13
    D=F.T@delta@F
    even=(np.eye(27)+B)/2;odd=(np.eye(27)-B)/2
    mixing=float(np.linalg.norm(even@D@odd))
    assert mixing>1
    assert np.linalg.norm(B@D-D@B)>2
    return {
       "rank_physical":27,"exchange_trace_physical":7,
       "gauge_invariant_loop_imbalance_breaks_exchange":True,
       "interparity_mixing_frobenius":mixing,
       "exchange_even":17,"exchange_odd":10,
       "burnside_trace_census":sorted(traces),
       "exchange_is_nontrivial_commutant_of_E_M_C":True,
       "sample_H_ground_energy":float(vals[0]),"sample_H_parity_blocks":blocks,
       "claim_boundary":"For this exchange-symmetric E/M/C generating set, a non-scalar commuting operator prevents its generated associative algebra from being full Mat_27(C). No claim that a distinct H27 address action or an abstract 27D Hilbert isomorphism is impossible."}

def mobile_two_vertex():
    _,gauge,P,operators,F=matrix_family("mobile")
    assert F.shape==(144,18)
    assert abs(np.trace(P)-18)<3e-12
    tr=[int(round(np.trace(u))) for u in gauge]
    assert sorted(tr)==[-18,-18,0,0,0,144]
    E,M,T=operators
    assert np.linalg.norm(E@T-T@E)>1
    scans=[]
    for j,k,t in ((1.,0,0),(.5,1,.3),(1.,.5,.7),(.1,1,1.)):
        H=F.T@(j*E+k*M+t*T)@F
        values,vec=np.linalg.eigh(H)
        state=F@vec[:,0]
        assert max(np.linalg.norm((u-np.eye(144))@state) for u in gauge)<1e-11
        scans.append({"J":j,"K":k,"matter_transport":t,
                      "ground_energy":float(values[0]),
                      "spectral_gap":float(values[1]-values[0]),
                      "gauss_max_residual":float(max(
                         np.linalg.norm((u-np.eye(144))@state) for u in gauge))})
    return {"gauge_fixed_graph":"two vertices joined by three parallel directed links, one spanning tree edge fixed",
        "independent_loops":2,"matter_model":"one mobile color-doublet excitation at either of two sites (2+2 direct sum)",
        "raw_reduced_dimension":144,"projected_dimension":18,
        "Burnside_traces_sorted":sorted(tr),
        "full_unfixed_raw_dimension":6**3*4,
        "full_unfixed_2vertex_projected_dimension_from_character":18,
        "transport_covariant_and_noncommuting_with_electric":True,"scans":scans,
        "boundary":"A minimal two-vertex graph with mobile matter, not a continuum propagating field. Replacing a tensor-product two-species Hilbert space by one mobile excitation changes the physical rank from 27 to 18."}

def main():
    out={"status":"PASS_S3_PARITY_17_10_OBSTRUCTION_AND_MOBILE_18_SECTOR",
         "27_exchange_obstruction":exchange_obstruction(),
         "mobile_two_vertex":mobile_two_vertex(),
         "known_prior_art":"Burnside's lemma, finite-group Gauss projection, and gauge-fixed link transport; novel here is a direct model-to-model obstruction/falsifier calculation."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 27=17+10, mobile gauge rank 18; certificate",OUT)
    return out
if __name__=="__main__":main()
