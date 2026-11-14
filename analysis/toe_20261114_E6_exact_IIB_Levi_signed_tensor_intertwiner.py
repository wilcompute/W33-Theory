#!/usr/bin/env python3
"""Exact native signed E6 cubic -> IIB GL(5)xSL(2) Levi intertwiner.

Not a discovered exceptional Lie algebra: this proves a fully explicit
signed unimodular basis dictionary to the established type-IIB branching,
including all 45 cubic monomials and the full 28D Levi action.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as G
OUT=ROOT/"data/toe_20261114_E6_native_signed_IIB_GL5_SL2_intertwiner.json"

def perm_sign(seq):
    return -1 if sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2 else 1

def rank_mod(matrix,p=101):
    A=np.asarray(matrix,dtype=np.int64).copy()%p
    rr=0
    for c in range(A.shape[1]):
        nz=np.flatnonzero(A[rr:,c])
        if not len(nz):continue
        k=rr+int(nz[0])
        A[[rr,k],:]=A[[k,rr],:]
        A[rr,:]=A[rr,:]*pow(int(A[rr,c]),-1,p)%p
        for j in range(rr+1,A.shape[0]):
            if A[j,c]:A[j,:]=(A[j,:]-A[j,c]*A[rr,:])%p
        rr+=1
        if rr==A.shape[0]:break
    return rr

def exterior_square(A):
    pairs=list(combinations(range(5),2))
    W=np.zeros((10,10),dtype=np.int64)
    for row,(i,j) in enumerate(pairs):
        for col,(k,l) in enumerate(pairs):
            W[row,col]=(int(A[i,k])*(j==l)+int(A[j,l])*(i==k)
                        -int(A[i,l])*(j==k)-int(A[j,k])*(i==l))
    return W

def main():
    cert,terms,_,_,roots=G.load()
    assert len(terms)==45 and len(roots)==72
    native={tuple(sorted(t)):int(s) for t,s in terms.items()}
    V=tuple(range(5))
    W0=(17,8,7,6,5)
    W1=(18,12,11,10,9)
    Zset=set((13,14,15,16,19,20,21,22,23,24))
    S=(25,26)
    pairs=list(combinations(range(5),2))
    def coeff(*coords):
        return native[tuple(sorted(coords))]
    v_sign={i:coeff(i,W0[i],S[1]) for i in V}
    assert all(coeff(i,W1[i],S[0])==-v_sign[i] for i in V)
    z_index={}; z_sign={}
    for i,j in pairs:
        matches=[z for z in Zset if tuple(sorted((W0[i],W1[j],z))) in native]
        assert len(matches)==1
        z=matches[0]
        z_index[(i,j)]=z
        z_sign[(i,j)]=coeff(W0[i],W1[j],z)
        assert coeff(W1[i],W0[j],z)==-z_sign[(i,j)]
    assert set(z_index.values())==Zset

    # Each signed source term is reproduced from the canonical
    # invariant V(W0 S1-W1 S0)+Z(W0 W1-W1 W0)
    #   -epsilon_ijklm V_i Z_jk Z_lm.
    model={}
    def insert(coords,s):
        key=tuple(sorted(coords))
        assert key not in model and len(set(key))==3 and int(s) in (-1,1)
        model[key]=int(s)
    for i in V:
        insert((i,W0[i],S[1]),v_sign[i])
        insert((i,W1[i],S[0]),-v_sign[i])
    for i,j in pairs:
        z=z_index[(i,j)]
        insert((z,W0[i],W1[j]),z_sign[(i,j)])
        insert((z,W1[i],W0[j]),-z_sign[(i,j)])
    vzz=0
    for i in V:
        other=[j for j in V if j!=i]
        for ab in combinations(other,2):
            cd=tuple(sorted(set(other)-set(ab)))
            if ab[0]>cd[0]:continue
            insert((i,z_index[ab],z_index[cd]),
                   -perm_sign((i,*ab,*cd))*v_sign[i]*z_sign[ab]*z_sign[cd])
            vzz+=1
    assert vzz==15 and len(model)==45 and model==native
    assert set(v_sign.values())=={-1,1}

    # Canonical order: 5 V, 5 W0, 5 W1, 10 Z, 2 S.
    original=list(V)+list(W0)+list(W1)+[z_index[p] for p in pairs]+list(S)
    signs=[v_sign[i] for i in V]+[1]*10+[z_sign[p] for p in pairs]+[1,1]
    assert sorted(original)==list(range(27)) and len(original)==27
    Q=np.zeros((27,27),dtype=np.int64)
    for i,(old,s) in enumerate(zip(original,signs)):
        Q[i,old]=s
    I=np.eye(27,dtype=np.int64)
    assert np.array_equal(Q@Q.T,I) and np.array_equal(Q.T@Q,I)

    grade=np.array([4]*5+[1]*10+[-2]*10+[-5]*2,dtype=np.int64)
    nativegrade=Q.T@np.diag(grade)@Q
    assert np.array_equal(nativegrade,np.diag(np.diag(nativegrade)))
    G.inf_check(nativegrade,terms)
    grades={}
    for n,R in enumerate(roots):
        nonzero=np.argwhere(R)
        g={int(nativegrade[i,i]-nativegrade[j,j]) for i,j in nonzero}
        assert len(g)==1
        deg=g.pop()
        grades.setdefault(deg,[]).append((n,R))
        assert np.array_equal(nativegrade@R-R@nativegrade,deg*R)
    assert {k:len(v) for k,v in grades.items()}=={0:22,3:20,-3:20,6:5,-6:5}

    E_candidates=[(i,R) for i,R in grades[0] if R[25,26]]
    F_candidates=[(i,R) for i,R in grades[0] if R[26,25]]
    assert len(E_candidates)==len(F_candidates)==1
    Ei,E=E_candidates[0];Fi,F=F_candidates[0]
    assert (Ei,Fi)==(55,71)
    H=E@F-F@E
    assert np.array_equal(H@E-E@H,2*E)
    assert np.array_equal(H@F-F@H,-2*F)
    assert not np.any(nativegrade@E-E@nativegrade)
    assert not np.any(nativegrade@F-F@nativegrade)
    Enew=Q@E@Q.T;Fnew=Q@F@Q.T;Hnew=Q@H@Q.T
    Eexpected=np.zeros((27,27),dtype=np.int64)
    Eexpected[5:10,10:15]=np.eye(5,dtype=np.int64)
    Eexpected[25,26]=1
    assert np.array_equal(Enew,Eexpected)
    assert np.array_equal(Fnew,Eexpected.T)
    assert np.array_equal(Hnew,Eexpected@Eexpected.T-Eexpected.T@Eexpected)

    # The remaining 20 zero-grade roots act as the 20 elementary
    # E_ij (i != j) on V; their commutators yield the four Cartans.
    sl5roots={};root_indices={}
    for i,R in grades[0]:
        if i in (Ei,Fi):continue
        m=Q@R@Q.T
        loc=np.argwhere(m[:5,:5])
        assert loc.shape==(1,2)
        a,b=map(int,loc[0])
        assert a!=b and abs(int(m[a,b]))==1
        assert (a,b) not in sl5roots
        sl5roots[(a,b)]=R
        root_indices[(a,b)]=i
    assert len(sl5roots)==20
    sl5H=[]
    for i in range(4):
        hi=sl5roots[(i,4)]@sl5roots[(4,i)]-sl5roots[(4,i)]@sl5roots[(i,4)]
        m=Q@hi@Q.T
        A=m[:5,:5]
        assert set(np.flatnonzero(np.diag(A)))=={i,4}
        assert abs(A[i,i])==1 and A[i,i]==-A[4,4]
        assert not np.any(A-np.diag(np.diag(A)))
        sl5H.append(hi)
    sl5=list(sl5roots.values())+sl5H
    levi=sl5+[E,F,H,nativegrade]
    assert len(sl5)==24 and len(levi)==28
    assert rank_mod([R.reshape(-1) for R in sl5])==24
    assert rank_mod([R.reshape(-1) for R in levi])==28

    # Constructive block-by-block IIB intertwining of ALL 24 sl5
    # generators: fundamental V, contragredient W0/W1, exterior² Z,
    # and SL2 singlet S.
    for M in sl5:
        A=Q@M@Q.T
        A5=A[:5,:5]
        expected=np.zeros((27,27),dtype=np.int64)
        expected[:5,:5]=A5
        expected[5:10,5:10]=-A5.T
        expected[10:15,10:15]=-A5.T
        expected[15:25,15:25]=exterior_square(A5)
        assert np.array_equal(A,expected)
        assert int(np.trace(A5))==0
        assert not np.any(M@E-E@M)
        assert not np.any(M@F-F@M)
        assert not np.any(M@H-H@M)
        assert not np.any(M@nativegrade-nativegrade@M)
    # Exact bracket closure of 24 sl5 basis elements, reconstructing
    # their full 27x27 commutators from the faithful 5x5 block.
    bracket_checks=0
    for M in sl5:
        for N in sl5:
            C=M@N-N@M
            c=Q@C@Q.T
            A=c[:5,:5]
            reconstructed=np.zeros((27,27),dtype=np.int64)
            for (i,j),B in sl5roots.items():
                B0=(Q@B@Q.T)[i,j]
                reconstructed+=(int(A[i,j])//int(B0))*B
            for i,hi in enumerate(sl5H):
                h0=(Q@hi@Q.T)[i,i]
                reconstructed+=(int(A[i,i])//int(h0))*hi
            assert np.array_equal(C,reconstructed)
            bracket_checks+=1
    assert bracket_checks==24*24

    result=dict(
       status="PASS_EXACT_NATIVE_SIGNED_E6_CUBIC_IIB_28D_LEVI_INTERTWINER",
       native_signed_terms_verified=45,
       native_to_canonical_signed_permutation_is_unimodular=True,
       canonical_cubic="sum_i V_i(W_i0 S1-W_i1 S0) + sum_{i<j} Z_ij(W_i0 W_j1-W_i1 W_j0) - sum_i sum_pair_partitions epsilon_ijklm V_i Z_jk Z_lm",
       native_coordinate_order_by_canonical_5_5_5_10_2=original,
       native_coordinate_sign_by_canonical_5_5_5_10_2=signs,
       type_IIB_branching={"(5,1)_4":5,"(5bar,2)_1":10,"(10,1)_minus2":10,"(1,2)_minus5":2},
       type_IIB_native_V=list(V),type_IIB_native_W0=list(W0),
       type_IIB_native_W1=list(W1),
       type_IIB_native_Z_ij=[{"pair":list(p),"native_index":z_index[p],"sign":z_sign[p]} for p in pairs],
       type_IIB_native_S=list(S),
       native_cubic_type_count={"VZZ":15,"WWZ":20,"VWS":10},
       GL1_fundamental_weights=[4,1,-2,-5],
       roots_by_GL1_grade={str(k):len(v) for k,v in sorted(grades.items())},
       explicit_SL2_raising_root_index=Ei,explicit_SL2_lowering_root_index=Fi,
       explicit_SL2_doublets=6,sl2_exact_brackets_verified=True,
       sl5_root_matrix_unit_count=20,
       sl5_root_indices_by_5x5_pair=[{"pair":[i,j],"root_index":root_indices[(i,j)]}
                                       for i,j in sorted(root_indices)],
       sl5_diagonal_Cartan_count=4,
       exact_sl5_block_action_on_V_W_W_Z_S=True,
       exact_sl5_bracket_reconstruction_checks=bracket_checks,
       Levi_sl5_sl2_gl1_dimension=28,
       Levi_exact_commutation_and_block_decomposition=True,
       scope="Complete exact native signed cubic and 28D Levi-generator intertwiner to known IIB GL5xSL2 representation. Does not yet identify the dynamical fields, solve GSS twist equations beyond local flux, establish a physical duality transform, select a section, or derive a theory of everything.",
       literature="E6(6) ExFT IIB branching, Eur.Phys.J.C 84 (2024) 13402-4, Hohm/Samtleben 1312.0614"
    )
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in (
       "status","native_signed_terms_verified","native_cubic_type_count",
       "roots_by_GL1_grade","explicit_SL2_raising_root_index",
       "exact_sl5_bracket_reconstruction_checks","Levi_sl5_sl2_gl1_dimension")},indent=2),flush=True)
    return result
if __name__=="__main__":main()
