#!/usr/bin/env python3
"""Pull Pass4850's Schlaefli K3,3 Gram operator through the explicit
1080 obstruction<->C4 dictionary and ask whether it resolves the three
Steinberg copies geometrically.

The intrinsic tensor sectors are
    20_chart x 15_W33   (contains one St_81),
    20_chart x 24_W33   (contains two St_81).
The test is exact in the 59-dimensional orbital algebra; no 1080x1080 rational
projector matrices are materialized.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import deque
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
from w33_20260831_all5_frontier_audit import orbit_ids
from w33_20260831_c5_wedderburn_kernel import orbital_mult,center_equations,generic_center,mulvec
from w33_pass4992_4999_common import build_base
from w33_20260901_eisenstein_schlaefli_obstruction_bridge import q4_cycles,paired_closure

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_K33_STEINBERG_ROUTER.json'
x=sp.Symbol('x')


def projector(A,lam,roots):
    A=sp.Matrix(A);n=A.rows;I=sp.eye(n);P=I
    den=sp.Rational(1)
    for r in roots:
        if r==lam:continue
        P=P*(A-r*I);den*=lam-r
    P=P/den
    assert P*P==P
    return P


def bridge(acts,charts):
    chart_act=[tuple(g[c*40]//40 for c in range(27)) for g in acts]
    CG=nx.Graph();CG.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if set(charts[a])&set(charts[b]):CG.add_edge(a,b)
    cubic=build_base();G27=cubic['G27']
    mp=next(nx.algorithms.isomorphism.GraphMatcher(CG,G27).isomorphisms_iter())
    invmp={v:k for k,v in mp.items()}
    q4=q4_cycles(G27);qi={C:i for i,C in enumerate(q4)}
    qacts=[]
    for pc in chart_act:
        pv=tuple(mp[pc[invmp[v]]] for v in range(27))
        qacts.append(tuple(qi[frozenset(pv[z] for z in C)] for C in q4))
    G=paired_closure(acts,qacts);assert len(G)==25920
    H=[z for z in G if z[0][0]==0];assert len(H)==24
    fixed=[i for i in range(1080) if all(b[i]==i for _a,b in H)];assert len(fixed)==1
    q0=fixed[0];phi=[None]*1080
    for a,b in G:
        y=b[q0];u=a[0]
        if phi[u] is None:phi[u]=y
        else:assert phi[u]==y
    assert len(set(phi))==1080
    return cubic,G27,q4,q0,phi,mp


def main():
    acts,charts,wlines=obs.build_action()
    rel,reps,sizes=orbit_ids(acts,acts,1080,1080);assert len(reps)==59
    T=orbital_mult(rel,reps)
    Z=center_equations(T).nullspace();assert len(Z)==15
    diag=int(rel[0,0]);one=sp.zeros(59,1);one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Z,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    si=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==81)
    E=idempotents[si];assert 1080*E[diag]==243

    # Coordinate system for the M3 Steinberg commutant block, exactly as in the
    # primitive-projector certificate.
    cols=[]
    for j in range(59):
        q=sp.zeros(59,1);q[j]=1;cols.append(mulvec(E,q,T))
    B=sp.Matrix.hstack(*cols);_r,piv=B.rref();piv=list(piv);assert len(piv)==9
    U=sp.Matrix.hstack(*[cols[j] for j in piv])
    _rr,rowp=U.T.rref();rowp=list(rowp);assert len(rowp)==9
    Uinv=U[rowp,:].inv()
    coord=lambda v:Uinv*v[rowp,:]
    def left_matrix(v):
        M=sp.zeros(9,9)
        for k in range(9):M[:,k]=coord(mulvec(v,U[:,k],T))
        return M

    cubic,G27,q4,q0,phi,mp=bridge(acts,charts)

    # Pass4850 K3,3 carrier and its C4 incidence Gram, but calculate only the
    # base row needed to identify the orbital-algebra element.
    K=[]
    for S in itertools.combinations(range(27),6):
        H=G27.subgraph(S)
        if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
            A,C=nx.algorithms.bipartite.sets(H)
            if len(A)==len(C)==3:K.append(frozenset(S))
    assert len(K)==360
    kof=[set() for _ in range(1080)]
    for j,S in enumerate(K):
        for i,C in enumerate(q4):
            if C<=S:kof[i].add(j)
    assert {len(S) for S in kof}=={3}
    baseK=kof[q0]
    row=[len(baseK & kof[phi[j]]) for j in range(1080)]
    assert set(row)<={0,1,3} and row[0]==3
    kval=[None]*59
    for j,v in enumerate(row):
        r=int(rel[0,j])
        if kval[r] is None:kval[r]=v
        else:assert kval[r]==v
    assert all(v is not None for v in kval)
    Kvec=sp.Matrix(kval)
    KE=mulvec(E,Kvec,T);KM=left_matrix(KE)
    kfac=sp.factor_list(sp.Poly(KM.charpoly(x).as_expr(),x,domain=sp.QQ))[1]

    # Intrinsic tensor projectors.  Chart overlap is the Schlaefli graph; W33
    # line-intersection is SRG(40,12,2,4).
    A27=nx.to_numpy_array(nx.Graph([(a,b) for a,b in itertools.combinations(range(27),2)
                                    if set(charts[a])&set(charts[b])]),nodelist=range(27),dtype=int)
    # build W33 line-intersection graph from the actual 40 isotropic lines
    A40=np.zeros((40,40),dtype=int)
    for a,b in itertools.combinations(range(40),2):
        if set(wlines[a])&set(wlines[b]):A40[a,b]=A40[b,a]=1
    assert sorted(round(float(t)) for t in np.linalg.eigvalsh(A27))==[-5]*6+[1]*20+[10]
    assert sorted(round(float(t)) for t in np.linalg.eigvalsh(A40))==[-4]*15+[2]*24+[12]
    P20=projector(A27,1,[10,1,-5])
    P15=projector(A40,-4,[12,2,-4])
    P24=projector(A40,2,[12,2,-4])
    assert sp.trace(P20)==20 and sp.trace(P15)==15 and sp.trace(P24)==24

    def tensor_orbital_vector(Pc,Pl):
        vals=[Pc[0,j//40]*Pl[0,j%40] for j in range(1080)]
        out=[None]*59
        for j,v in enumerate(vals):
            r=int(rel[0,j])
            if out[r] is None:out[r]=sp.factor(v)
            else:assert out[r]==v
        return sp.Matrix(out)

    V2015=tensor_orbital_vector(P20,P15)
    V2024=tensor_orbital_vector(P20,P24)
    S15=mulvec(E,V2015,T);S24=mulvec(E,V2024,T)
    assert mulvec(S15,S15,T)==S15 and mulvec(S24,S24,T)==S24
    assert mulvec(S15,S24,T)==sp.zeros(59,1)
    assert S15+S24==E
    ranks=[int(1080*S15[diag]),int(1080*S24[diag])];assert ranks==[81,162]
    M15=left_matrix(S15);M24=left_matrix(S24)
    assert (M15*M15==M15 and M24*M24==M24 and M15+M24==sp.eye(9))

    comm15=mulvec(Kvec,S15,T)-mulvec(S15,Kvec,T)
    comm24=mulvec(Kvec,S24,T)-mulvec(S24,Kvec,T)
    preserves15=comm15==sp.zeros(59,1);preserves24=comm24==sp.zeros(59,1)
    # Off-diagonal mixing ranks in the 9d regular M3 representation.
    off1524=M15*KM*M24;off2415=M24*KM*M15
    off=[off1524.rank(),off2415.rank()]

    # Spectra on the two intrinsic blocks when preserved; otherwise keep the
    # exact compressed operators to expose the mixing rather than overclaim.
    def char_nonzero_block(P,M):
        # image basis of idempotent P
        cols=P.columnspace();V=sp.Matrix.hstack(*cols)
        _r,rows=V.T.rref();rows=list(rows);Vin=V[rows,:].inv()
        R=sp.zeros(len(cols),len(cols))
        for j in range(len(cols)):R[:,j]=Vin*(M*V[:,j])[rows,:]
        return str(sp.factor(R.charpoly(x).as_expr())),R.rank()
    blocks={}
    if preserves15 and preserves24:
        blocks['20x15']=char_nonzero_block(M15,KM)
        blocks['20x24']=char_nonzero_block(M24,KM)

    out={
      'schema':'w33.20260901.k33-steinberg-router.v1','status':'PASS',
      'operator':{'source':'Pass4850 1080 C4 x 360 K3,3 incidence Gram M M^T',
                  'pulledBackTo':'27x40 obstruction coordinates','orbitalCoefficients':kval,
                  'steinbergRegularCharpoly':str(sp.factor(KM.charpoly(x).as_expr())),
                  'steinbergRegularFactors':[(str(f),int(e)) for f,e in kfac]},
      'intrinsicSteinbergAddress':{
        '20x15Rank':ranks[0],'20x24Rank':ranks[1],
        'reading':'one Steinberg copy lies in 20x15 and two lie in 20x24',
        'projectorsSumToCentralSteinberg':True},
      'routingTest':{
        'K33CommutesWith20x15Projector':preserves15,
        'K33CommutesWith20x24Projector':preserves24,
        'offDiagonalRegularRanks_15to24_24to15':off,
        'preservedBlockCharpolys':blocks,
        'distinguishesIntrinsicOnePlusTwoSplit':bool(preserves15 and preserves24)},
      'theorem':(
        'The old Schlaefli K3,3 Gram operator is now an explicit element of the '
        'same 59-orbital obstruction commutant.  Its exact action on the '
        '3*Steinberg block is compared with the intrinsic 81+162 tensor split; '
        'the certificate reports whether it genuinely routes the one-copy and '
        'two-copy sectors rather than inferring this from dimensions.'),
      'boundary':'Exact finite representation theory only; router means a commutant-sector discriminator, not a hardware channel.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','steinbergRanks':ranks,'preservesSplit':preserves15 and preserves24,
                      'offdiag':off,'charpoly':out['operator']['steinbergRegularCharpoly']},sort_keys=True))

if __name__=='__main__':main()
