#!/usr/bin/env python3
"""Exact 216-circuit -> right-dark intertwiner, including the nonsplit C3 cover.

The 216 sentinel five-circuits form PSp(4,3)/S5.  Their canonical incidence
matrix C gives an explicit rank-20 map T20=Q20 C^T into the right dark sector.
This audit also reconstructs the central C3 of a W33 point stabilizer and asks
exactly how T20 behaves under its free three-sheet action on the circuits.

The quotient test is representation-theoretically sharp: summing each C3 deck
fibre projects the circuit permutation module to its deck-invariant part, while
within-fibre differences generate the nontrivial deck characters.  The ranks of
those two images say precisely how much of the dark-20 carrier descends to the
72-fibre quotient and how much requires sheet/phase information.
"""
from __future__ import annotations
import itertools,json
from collections import deque,Counter
from pathlib import Path

from w33_20260829_216_clifford_torsor_nogo import (
    geometry,supports_from_N,closure_paired,norm,form,compose,
    deterministic_generators,porder
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_CIRCUIT_DARK_INTERTWINER.json'
P=1000003

def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return [list(x) for x in zip(*A)]
def add(A,B,sa=1,sb=1): return [[sa*A[i][j]+sb*B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def rank_mod(A,p=P):
    if not A or not A[0]: return 0
    M=[[x%p for x in row] for row in A];m=len(M);n=len(M[0]);r=0
    for c in range(n):
        q=next((i for i in range(r,m) if M[i][c]),None)
        if q is None: continue
        M[r],M[q]=M[q],M[r]; inv=pow(M[r][c],p-2,p);M[r]=[(x*inv)%p for x in M[r]]
        for i in range(m):
            if i==r or not M[i][c]: continue
            z=M[i][c];M[i]=[(M[i][j]-z*M[r][j])%p for j in range(n)]
        r+=1
        if r==m: break
    return r

def orbits(H,n,which):
    rem=set(range(n));out=[]
    while rem:
        s=min(rem);O={s};Q=deque([s])
        while Q:
            x=Q.popleft()
            for h in H:
                y=h[which][x]
                if y not in O:O.add(y);Q.append(y)
        out.append(tuple(sorted(O)));rem-=O
    return sorted(out,key=lambda z:(len(z),z))
def indicators(orbs,n):
    return [[int(i in O) for O in orbs] for i in range(n)]
def perm_orbits(p):
    rem=set(range(len(p)));out=[]
    while rem:
        s=min(rem);O=[];x=s
        while x not in O:
            O.append(x);x=p[x]
        out.append(tuple(sorted(O)));rem-=set(O)
    return sorted(out,key=lambda z:(len(z),z))
def set_orbits(perms,n):
    rem=set(range(n));out=[]
    while rem:
        s=min(rem);O={g[s] for g in perms};out.append(tuple(sorted(O)));rem-=O
    return sorted(out,key=lambda z:(-len(z),z))
def select_columns(M,cols):
    return [[row[j] for j in cols] for row in M]

def main():
    pts,idx,lines,N=geometry();supports,masks=supports_from_N(N)
    NtN=mm(tr(N),N);A40=add(NtN,eye(40),1,-4)
    A45=[[0]*45 for _ in range(45)]
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):A45[i][j]=A45[j][i]=1
    assert {sum(r) for r in A40}=={12} and {sum(r) for r in A45}=={12}

    circuits=[]
    for cc in itertools.combinations(range(45),5):
        w=0
        for i in cc:w^=masks[i]
        if w==0:circuits.append(cc)
    assert len(circuits)==216
    cidx={cc:i for i,cc in enumerate(circuits)}
    C=[[int(m in cc) for m in range(45)] for cc in circuits]
    G=mm(tr(C),C)
    Abar=[[int(i!=j)-A45[i][j] for j in range(45)] for i in range(45)]
    assert G==add(eye(45),Abar,24,3) and rank_mod(C)==45

    Q20=mm(add(eye(45),A45,12,-1),add(A45,eye(45),1,3))
    Q15=mm(add(A40,eye(40),1,-12),add(A40,eye(40),1,-2))
    assert rank_mod(Q20)==20 and rank_mod(Q15)==15
    B=[[int(p in supports[m]) for m in range(45)] for p in range(40)]
    T20=mm(Q20,tr(C))
    assert rank_mod(T20)==20 and all(x==0 for row in mm(B,T20) for x in row)
    assert mm(mm(Q20,G),Q20)==[[648*x for x in row] for row in Q20]

    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3
                y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)));p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)};gens45=[]
    for p in gens40:gens45.append(tuple(si[frozenset(p[x] for x in S)] for S in supports))
    chosen=(18,62,77,10)
    Gpaired=closure_paired([gens40[i] for i in chosen],[gens45[i] for i in chosen]);assert len(Gpaired)==25920
    cc0=set(circuits[0])
    H=[g for g in Gpaired if {g[1][x] for x in cc0}==cc0];assert len(H)==120
    o40=orbits(H,40,0);o45=orbits(H,45,1)
    fixed15=rank_mod(mm(Q15,indicators(o40,40)))
    fixed20=rank_mod(mm(Q20,indicators(o45,45)))

    # Central-C3 cover of the 216 circuits.
    K={p45 for p40,p45 in Gpaired if p40[0]==0};assert len(K)==648
    kgens=deterministic_generators(K,45)
    Z=[z for z in K if all(compose(z,g)==compose(g,z) for g in kgens)]
    assert len(Z)==3 and Counter(porder(z) for z in Z)==Counter({1:1,3:2})
    e45=tuple(range(45));z=next(x for x in Z if x!=e45)
    def act_circuit(i,g):return cidx[tuple(sorted(g[x] for x in circuits[i]))]
    zperm=tuple(act_circuit(i,z) for i in range(216))
    zfibres=perm_orbits(zperm);assert len(zfibres)==72 and {len(O) for O in zfibres}=={3}
    fibre_of={x:i for i,O in enumerate(zfibres) for x in O}

    # Fibre summation F is the exact deck-invariant projector up to scalar.
    F=[[0]*72 for _ in range(216)]
    for j,O in enumerate(zfibres):
        for x in O:F[x][j]=1
    Tquot=mm(T20,F);quot_rank=rank_mod(Tquot)

    # Within-fibre differences span the nontrivial C3 sheet characters.
    D=[[0]*(2*72) for _ in range(216)]
    for j,O in enumerate(zfibres):
        a,b,c=O;D[b][2*j]=1;D[a][2*j]=-1;D[c][2*j+1]=1;D[a][2*j+1]=-1
    Tdeck=mm(T20,D);deck_rank=rank_mod(Tdeck)
    assert quot_rank+deck_rank==20

    z45orbs=perm_orbits(z)
    fixed20_z=rank_mod(mm(Q20,indicators(z45orbs,45)))
    assert fixed20_z==quot_rank
    nontrivial20=20-fixed20_z
    assert nontrivial20==deck_rank and nontrivial20%2==0

    # Pointwise descent would require the three T20 columns over every fibre to
    # coincide.  Count this separately from the averaged quotient map.
    cols=[tuple(T20[r][j] for r in range(45)) for j in range(216)]
    constant_fibres=sum(len({cols[x] for x in O})==1 for O in zfibres)

    # K/Z acts faithfully on the 72 fibres and has two 36-orbits.  Measure the
    # dark-sector rank contributed by each quotient orbit after fibre summation.
    def quotient_perm(g):return tuple(fibre_of[act_circuit(O[0],g)] for O in zfibres)
    Q={quotient_perm(g) for g in K};assert len(Q)==216
    qorbits=set_orbits(Q,72);assert [len(O) for O in qorbits]==[36,36]
    orbit_records=[]
    for O in qorbits:
        incidence={sum(0 in supports[j] for j in circuits[zfibres[fi][0]]) for fi in O}
        assert len(incidence)==1;r=next(iter(incidence));assert r in (0,2)
        rr=rank_mod(select_columns(Tquot,O))
        raw=sorted({x for fi in O for x in zfibres[fi]})
        rawrank=rank_mod(select_columns(T20,raw))
        orbit_records.append({'circuitSupportsThroughDistinguishedPoint':r,'fibres':36,'circuitStates':108,
                              'fibreSummedDarkRank':rr,'rawCircuitDarkRank':rawrank})
    orbit_records.sort(key=lambda x:x['circuitSupportsThroughDistinguishedPoint'])

    out={
      'schema':'w33.20260829.circuit-dark-intertwiner.v2','status':'PASS',
      'circuitIncidence':{'shape':[216,45],'rank':45,'gram':'C^T C = 24 I + 3 A_complement(GQ(4,2))',
        'gramEigenvalues':{'trivial':120,'dark20':12,'shared24':30}},
      'rightDark20':{'integerProjector':'Q20=(12I-A45)(A45+3I)=54 P20','rank':20,
        'explicitMap':'T20=Q20 C^T : R^216 -> ker(B) subset R^45','mapRank':20,
        'exactNormIdentity':'Q20 (C^T C) Q20 = 648 Q20'},
      'circuitStabilizer':{'order':120,'structure':'S5','orbitsOnW33Points':[len(x) for x in o40],
        'orbitsOnGQPoints':[len(x) for x in o45],
        'fixedDimensionLeft15':fixed15,'fixedDimensionRight20':fixed20},
      'centralC3Bridge':{
        'deckFibres':72,'fibreSize':3,'centerCycleShapeOn45':{str(k):v for k,v in Counter(len(O) for O in z45orbs).items()},
        'pointwiseConstantFibres':constant_fibres,
        'fibreSummedMapRank':quot_rank,'fixedDarkDimension':fixed20_z,
        'withinFibreDifferenceRank':deck_rank,'nontrivialDeckDarkDimension':nontrivial20,
        'complexNontrivialCharacterMultiplicityEach':nontrivial20//2,
        'quotientOrbitDarkRanks':orbit_records},
      'theorem':'The rank-20 circuit-to-dark intertwiner splits exactly into the C3-invariant image reached by summing the 72 deck fibres and the complementary image reached by within-fibre differences. Thus the 72-state Clifford quotient carries exactly the fixed dark sector; the remaining dark directions require sheet/phase data of the nonsplit three-sheet cover.',
      'boundary':'Exact finite representation/intertwiner statement. Fibre summation is a quotient-level linear observable, not a claim that the nonsplit C3 extension admits a group-theoretic section or that the 216 circuits form a Clifford torsor.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
