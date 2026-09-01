#!/usr/bin/env python3
"""Full PSp-equivariant Hom scan from the 1080 obstruction carrier to BT796-2160.

The packet48/BT796 cross-identification gives a transitive 2160-point target
G-set.  The 1080 obstruction carrier contains three Steinberg copies with the
exact primitive frame P,R,S, where S is the K3,3-dark 81-space.

For a transitive source G/H, every equivariant incidence map to a target
permutation module is determined by one H-orbit on the target.  We therefore:
  * compute every source-stabilizer orbit on the 2160 BT796 slots;
  * test each orbital incidence Gram A_i A_i^T against P,R,S and St^3;
  * scan cross-Grams A_i A_j^T until their Steinberg projections span the full
    nine-dimensional End_G(St_81^3) ~= M3(Q), if they do;
  * solve exactly for the dark projector S as a rational combination of an
    independent cross-Gram basis.

This is a complete linear-equivariant search on this target carrier, not a
hand-picked relation.
"""
from __future__ import annotations

import json
from collections import deque
from pathlib import Path

import sympy as sp

from w33_20260901_steinberg_frame_common import build as build_frame, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import mulvec
import w33_20260901_packet48_bt796_crossid as cross

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_BT796_STEINBERG_HOM_SCAN.json'


def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))


def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    assert len(S)==25920
    return list(S)


def main():
    F=build_frame(); D=cross.build()
    acts=F['acts']; rel=F['rel']; T=F['T']; E=F['E']; P,R,S=F['frame']; Q=F['Qvec']; diag=F['diag']
    slots=D['slots']; sli={x:i for i,x in enumerate(slots)}; wlines=D['wlines']
    li={frozenset(L):i for i,L in enumerate(wlines)}
    line_sets=[set(L) for L in wlines]
    skew=[(i,j) for i,j in __import__('itertools').combinations(range(40),2) if not (line_sets[i]&line_sets[j])]
    skidx={frozenset(x):i for i,x in enumerate(skew)}

    def line_perm(p):return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def slot_perm(p):
        lp=line_perm(p); out=[]
        for s,t in slots:
            a,b=skew[s]; ns=skidx[frozenset((lp[a],lp[b]))]
            out.append(sli[(ns,lp[t])])
        return tuple(out)

    target_gens=[slot_perm(p) for p in D['g40']]
    # Fail closed if the independently-built source action is not using these
    # same four W33-line generators in the same order.
    src_line=[tuple(acts[k][ell]%40 for ell in range(40)) for k in range(4)]
    assert src_line==[line_perm(p) for p in D['g40']]
    G=paired_closure(acts,target_gens,1080,2160)
    H=[z for z in G if z[0][0]==0];assert len(H)==24

    # H-orbits on target = basis of Hom_G(Q[1080],Q[2160]).
    unseen=set(range(2160));orbits=[]
    while unseen:
        o=min(unseen);O={gt[o] for _gs,gt in H};unseen-=O;orbits.append(sorted(O))
    orbits=sorted(orbits,key=lambda O:(len(O),O[0]))

    # One well-defined target transporter for each source point.
    tr=[None]*1080
    for gs,gt in G:
        y=gs[0]
        if tr[y] is None:tr[y]=gt
    assert all(x is not None for x in tr)

    zero=sp.zeros(59,1)
    def cross_operator(i,j):
        Oi=set(orbits[i]);Oj=orbits[j]
        row=[]
        for y in range(1080):
            row.append(sum(1 for x in Oj if tr[y][x] in Oi))
        oval=[None]*59
        for y,v in enumerate(row):
            r=int(rel[0,y])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        v=sp.Matrix(oval)
        return mulvec(E,mulvec(v,E,T),T)

    def sandwich(A,B,C):return mulvec(A,mulvec(B,C,T),T)
    records=[];dark_single=[]
    for i,O in enumerate(orbits):
        X=cross_operator(i,i)
        LM=F['left_matrix'](X)
        rr=LM.rank();assert rr%3==0
        scal={}
        for name,Z in [('P',P),('R',R),('S',S),('Q',Q)]:
            scal[name]=proportional_scalar(sandwich(Z,X,Z),Z)
        rec={'orbit':i,'targetOrbitSize':len(O),'steinbergRegularRank':int(rr),
             'steinbergActualRank':int(rr//3*81),
             'primitiveSandwichScalars':{k:(None if v is None else str(sp.factor(v))) for k,v in scal.items()}}
        records.append(rec)
        if scal['S'] not in (None,0):dark_single.append(i)

    # Scan cross-Grams and retain only rank-increasing Steinberg operators.
    indep=[];basis=sp.zeros(59,0);rank=0
    for i in range(len(orbits)):
        if rank==9:break
        for j in range(len(orbits)):
            X=cross_operator(i,j)
            if X==zero:continue
            C=sp.Matrix.hstack(basis,X)
            r=C.rank()
            if r>rank:
                indep.append((i,j,X));basis=C;rank=r
                if rank==9:break

    solutions={}
    if rank==9:
        for name,Z in [('P',P),('R',R),('S_dark',S),('Q_K33',Q),('E_St3',E)]:
            sol,_=basis.gauss_jordan_solve(Z);assert basis*sol==Z
            terms=[]
            for k,c in enumerate(sol):
                if c!=0:
                    terms.append({'crossOrbitPair':[indep[k][0],indep[k][1]],'coefficient':str(sp.factor(c))})
            solutions[name]=terms

    out={'schema':'w33.20260901.bt796-steinberg-hom-scan.v1','status':'PASS',
      'sourceCarrier':1080,'targetCarrier':2160,'groupOrder':25920,'sourceStabilizerOrder':24,
      'equivariantHomDimension':len(orbits),'targetOrbitSizes':[len(O) for O in orbits],
      'singleOrbitalGrams':records,'singleOrbitDarkHits':dark_single,
      'crossGramSteinbergSpanDimension':rank,
      'independentCrossOrbitPairs':[[i,j] for i,j,_X in indep],
      'exactProjectorExpansions':solutions,
      'fullM3RealizedByTargetCrossGrams':bool(rank==9),
      'theorem':('The complete PSp-equivariant incidence Hom space from the 1080 obstruction carrier to the BT796/packet48 2160 carrier is enumerated by source-stabilizer orbits. Its orbital Grams are tested copy-by-copy against P,R,S. If the cross-Gram Steinberg span has dimension nine, this single 2160 carrier realizes the full M3(Q) multiplicity algebra and the recorded rational expansion gives an explicit linear construction of the dark S projector from target intertwiners.'),
      'boundary':('This is finite characteristic-zero representation theory. A nonzero or exact dark-projector coupling does not identify a physical dark sector, particle species, field, energy, or experimental observable.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','HomDim':len(orbits),'darkSingle':dark_single,
                      'crossSpan':rank,'fullM3':rank==9},sort_keys=True))

if __name__=='__main__':main()
