#!/usr/bin/env python3
"""Exact 27 <-> 45 <-> 90-D4 lift of the curved cubic-surface prism.

Pass7364-7366 gives integral matrices

    Z^36 --N--> Z^45 --R--> Z^27,       R N = 3 Q.

The selected E8/D4 carrier replaces every one of the 45 tritangent / packet
coordinates by its two individual D4 halves.  If J:Z^45 -> Z^90 is the pair
injection, then J^T J = 2 I.  After the exact packet<->tritangent and
completion-chart<->cubic-line identifications, define

    N90 = J P^T N,
    R90 = R P J^T,

where P is the 45-coordinate permutation from E8 packets to tritangents.
Then

    R90 N90 = 6 Q.

This has two consequences that were not visible on the 45-coordinate prism:
  * mod 3 the middle homology becomes 45 antisymmetric D4-pair modes plus the
    old logical H1=10 in the symmetric pair sector;
  * mod 2 the doubled prism is also a genuine chain complex.  The first divided
    curvature (R90 N90)/2 = 3Q reduces to Q mod 2 and therefore recovers the
    existing [27,7,11]_2 Schlaefli code.

The characteristic-zero chart->D4 incidence has centered rank 20, giving the
unique PSp(4,3) degree-20 / right-dark sector on the lifted carrier.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from collections import Counter

import numpy as np
import networkx as nx

from w33_pass4992_4999_common import build_base
from w33_pass7225_7232_spread_code_doily_puncture import coordinate_isomorphism

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_D4_PRISM_LIFT.json'


def rankp(A,p):
    A=np.asarray(A,dtype=np.int64).copy()%p;m,n=A.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None: continue
        A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(m):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m: break
    return r


def d4_data(W):
    adj=[set(W.neighbors(i)) for i in range(40)]
    Q=set()
    for a,b,c in itertools.combinations(range(40),3):
        if b in adj[a] or c in adj[a] or c in adj[b]: continue
        X=frozenset(adj[a]&adj[b]&adj[c])
        if len(X)==4: Q.add(X)
    Q=sorted(Q,key=lambda z:tuple(sorted(z))); qi={q:i for i,q in enumerate(Q)}
    partner={}
    for i,q in enumerate(Q):
        partner[i]=qi[frozenset(set.intersection(*(adj[x] for x in q)))]
    pairs=sorted({tuple(sorted((i,j))) for i,j in partner.items()})
    assert len(Q)==90 and len(pairs)==45
    supports=[frozenset(Q[i]|Q[j]) for i,j in pairs]
    packs=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for z in C:
            if U&supports[z]:ok=False;break
            U|=supports[z]
        if ok and len(U)==40:packs.append(C)
    assert len(packs)==27
    return Q,pairs,supports,packs


def main():
    b=build_base(); T=b['tritangents']; DS=b['DS']
    R=np.zeros((27,45),dtype=int)
    for j,t in enumerate(T): R[list(t),j]=1
    N=1-np.asarray(b['M'],dtype=int)
    Qcurv=np.zeros((27,36),dtype=int)
    for i in range(27):
        for j,D in enumerate(DS): Qcurv[i,j]=int(i not in D)
    assert np.array_equal(R@N,3*Qcurv)

    D4,pairs,supports,packs=d4_data(b['W'])
    packet_to_tri=coordinate_isomorphism(supports,T)
    P=np.zeros((45,45),dtype=int)
    for s,t in enumerate(packet_to_tri):P[t,s]=1
    assert np.array_equal(P.T@P,np.eye(45,dtype=int))

    # Each five-packet completion chart maps to the five tritangents through
    # exactly one cubic line, and every cubic line occurs once.
    chart_to_line=[]
    for C in packs:
        common=set(range(27))
        for s in C: common &= set(T[packet_to_tri[s]])
        assert len(common)==1
        chart_to_line.append(next(iter(common)))
    assert sorted(chart_to_line)==list(range(27))

    Mchart=np.zeros((27,45),dtype=int)
    for C,line in zip(packs,chart_to_line): Mchart[line,list(C)]=1
    assert np.array_equal(Mchart,R@P)

    # Pair injection 45 -> 90 D4 halves.
    J=np.zeros((90,45),dtype=int)
    for s,(a,c) in enumerate(pairs):J[a,s]=J[c,s]=1
    assert np.array_equal(J.T@J,2*np.eye(45,dtype=int))
    assert rankp(J,2)==rankp(J,3)==45

    N90=J@P.T@N
    R90=R@P@J.T
    assert np.array_equal(R90@N90,6*Qcurv)

    ranks={str(p):{
      'R90':rankp(R90,p),'N90':rankp(N90,p),'Q':rankp(Qcurv,p)
    } for p in (2,3,5,7)}
    assert ranks['2']=={'R90':21,'N90':21,'Q':7}
    assert ranks['3']=={'R90':21,'N90':14,'Q':21}

    h2_2=36-ranks['2']['N90'];h1_2=(90-ranks['2']['R90'])-ranks['2']['N90'];h0_2=27-ranks['2']['R90']
    h2_3=36-ranks['3']['N90'];h1_3=(90-ranks['3']['R90'])-ranks['3']['N90'];h0_3=27-ranks['3']['R90']
    assert (h2_2,h1_2,h0_2)==(15,48,6)
    assert (h2_3,h1_3,h0_3)==(22,55,6)

    # In characteristic 3, 2 is invertible and the 90-space splits into
    # symmetric and antisymmetric pair sectors.  R90 kills the antisymmetric
    # 45-space; N90 lies in the symmetric 45-space.  The symmetric homology is
    # therefore exactly the old 10-dimensional H1.
    old_h1=(45-rankp(R,3))-rankp(N,3)
    assert old_h1==10 and h1_3==45+old_h1

    # Characteristic zero: line/chart -> D4 incidence L has Gram
    # 2 R R^T = 10 I + 2 A_meet.  Its nonzero sector dimensions are 1+20.
    L=J@P.T@R.T
    G=L.T@L
    Ameet=nx.to_numpy_array(b['G27'],nodelist=range(27),dtype=int)
    assert np.array_equal(G,10*np.eye(27,dtype=int)+2*Ameet)
    evals=np.linalg.eigvalsh(G.astype(float))
    hist=Counter(round(float(x)) for x in evals)
    assert hist==Counter({0:6,12:20,30:1})

    divided2=(R90@N90)//2
    assert np.array_equal(divided2,3*Qcurv)
    assert rankp(divided2,2)==7

    out={
      'schema':'w33.20260901.d4-prism-lift.v1','status':'PASS',
      'integral':{
        'oldCurvature':'R N = 3 Q','pairIdentity':'J^T J = 2 I_45',
        'liftedCurvature':'R90 N90 = 6 Q',
        'matrices':{'R90':'27x90','N90':'90x36','J':'90x45'}},
      'coordinateIdentifications':{
        'packetsToTritangents':45,'completionChartsToCubicLines':27,
        'chartPacketIncidenceEquals':'R P'},
      'characteristicZero':{
        'chartToD4Rank':21,'gramSpectrum':{'30':1,'12':20,'0':6},
        'centeredRank':20,'reading':'unique PSp(4,3) degree-20 / dark sector'},
      'mod2':{
        'flat':True,'homology':{'H2':h2_2,'H1':h1_2,'H0':h0_2},
        'dividedCurvature':'(R90 N90)/2 = 3Q = Q mod 2',
        'dividedCurvatureRank':7,'SchlafliCode':'[27,7,11]_2'},
      'mod3':{
        'flat':True,'homology':{'H2':h2_3,'H1':h1_3,'H0':h0_3},
        'H1Split':'45 antisymmetric D4-pair modes + 10 symmetric old logical modes'},
      'theorem':'The 90-D4 lift multiplies the integral curvature by two. It simultaneously realizes the characteristic-zero 20-sector, preserves the old ternary logical 10 in the symmetric pair half while adding 45 antisymmetric modes, and makes the prism flat mod 2 with the old Schlaefli 7 reappearing as the first divided curvature.',
      'boundary':'The mod-2 divided curvature is Bockstein-like but is not called a standard Bockstein here because the integral composite is 6Q rather than zero. The 48-dimensional binary H1 is a homology dimension, not automatically a D4 or hardware channel count.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','curvature':'6Q','F2':[h2_2,h1_2,h0_2],'F3':[h2_3,h1_3,h0_3],'dark20':20,'binary7':7},sort_keys=True))

if __name__=='__main__':main()
