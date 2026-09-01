#!/usr/bin/env python3
"""Shared exact construction for the 2026-09-01 Steinberg follow-ups.

Returns the 59-dimensional orbital algebra of the transitive 1080 obstruction
carrier, its central Steinberg idempotent E (actual rank 243), and the exact
primitive frame P,R,S plus the K3,3-selected primitive projector Q.

The construction is intentionally replayed from frozen certificates rather
than reading generated JSON.  Downstream attacks therefore fail closed if any
upstream objectwise dictionary changes.
"""
from __future__ import annotations

import itertools
import networkx as nx
import numpy as np
import sympy as sp

import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_k33_steinberg_router as router
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import orbital_mult, center_equations, generic_center, mulvec


def proportional_scalar(A: sp.Matrix, B: sp.Matrix):
    q = None
    for i in range(A.rows):
        for j in range(A.cols):
            a,b=A[i,j],B[i,j]
            if b==0:
                if a!=0:return None
            else:
                z=sp.factor(a/b)
                if q is None:q=z
                elif z!=q:return None
    return sp.Integer(0) if q is None else q


def build():
    acts,charts,wlines=obs.build_action()
    rel,reps,_sizes=orbit_ids(acts,acts,1080,1080); assert len(reps)==59
    T=orbital_mult(rel,reps)
    Z=center_equations(T).nullspace(); assert len(Z)==15
    diag=int(rel[0,0]); one=sp.zeros(59,1); one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Z,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    si=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==81)
    E=idempotents[si]; assert 1080*E[diag]==243

    cols=[]
    for j in range(59):
        q=sp.zeros(59,1); q[j]=1; cols.append(mulvec(E,q,T))
    B=sp.Matrix.hstack(*cols); _r,piv=B.rref(); piv=list(piv); assert len(piv)==9
    U=sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr,rowp=U.T.rref(); rowp=list(rowp); assert len(rowp)==9
    Uinv=U[rowp,:].inv()
    coord=lambda v:Uinv*v[rowp,:]
    def left_matrix(v):
        M=sp.zeros(9,9)
        for k in range(9):M[:,k]=coord(mulvec(v,U[:,k],T))
        return M

    cubic,G27,q4,q0,phi,mp=router.bridge(acts,charts)

    K33=[]
    for SS in itertools.combinations(range(27),6):
        H=G27.subgraph(SS)
        if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
            A,C=nx.algorithms.bipartite.sets(H)
            if len(A)==len(C)==3:K33.append(frozenset(SS))
    assert len(K33)==360
    kof=[set() for _ in range(1080)]
    for j,SS in enumerate(K33):
        for i,C in enumerate(q4):
            if C<=SS:kof[i].add(j)
    assert {len(s) for s in kof}=={3}
    baseK=kof[q0]
    row=[len(baseK & kof[phi[j]]) for j in range(1080)]
    kval=[None]*59
    for j,v in enumerate(row):
        r=int(rel[0,j])
        if kval[r] is None:kval[r]=v
        else:assert kval[r]==v
    Kvec=sp.Matrix(kval)
    KE=mulvec(E,Kvec,T)
    assert mulvec(KE,KE,T)==8*KE
    Qvec=KE/8; assert mulvec(Qvec,Qvec,T)==Qvec and 1080*Qvec[diag]==81

    A27=nx.to_numpy_array(nx.Graph([(a,b) for a,b in itertools.combinations(range(27),2)
                                    if set(charts[a])&set(charts[b])]),nodelist=range(27),dtype=int)
    A40=np.zeros((40,40),dtype=int)
    for a,b in itertools.combinations(range(40),2):
        if set(wlines[a])&set(wlines[b]):A40[a,b]=A40[b,a]=1
    P20=router.projector(A27,1,[10,1,-5])
    P15=router.projector(A40,-4,[12,2,-4])
    P24=router.projector(A40,2,[12,2,-4])
    def tensor_orbital_vector(Pc,Pl):
        vals=[Pc[0,j//40]*Pl[0,j%40] for j in range(1080)]
        out=[None]*59
        for j,v in enumerate(vals):
            r=int(rel[0,j])
            if out[r] is None:out[r]=sp.factor(v)
            else:assert out[r]==v
        return sp.Matrix(out)
    Pvec=mulvec(E,tensor_orbital_vector(P20,P15),T)
    Cvec=mulvec(E,tensor_orbital_vector(P20,P24),T)
    assert Pvec+Cvec==E
    Rvec=sp.Rational(3,2)*mulvec(Cvec,mulvec(Qvec,Cvec,T),T)
    Svec=Cvec-Rvec
    frame=[Pvec,Rvec,Svec]
    assert all(mulvec(v,v,T)==v and 1080*v[diag]==81 for v in frame)
    assert all(mulvec(frame[i],frame[j],T)==sp.zeros(59,1) and
               mulvec(frame[j],frame[i],T)==sp.zeros(59,1)
               for i,j in itertools.combinations(range(3),2))
    assert sum(frame,sp.zeros(59,1))==E
    assert mulvec(Svec,Qvec,T)==sp.zeros(59,1)==mulvec(Qvec,Svec,T)

    return dict(acts=acts,charts=charts,wlines=wlines,rel=rel,reps=reps,T=T,diag=diag,
                E=E,left_matrix=left_matrix,cubic=cubic,G27=G27,q4=q4,q0=q0,phi=phi,mp=mp,
                K33=K33,kof=kof,Kvec=Kvec,Qvec=Qvec,Pvec=Pvec,Rvec=Rvec,Svec=Svec,
                frame=frame)
