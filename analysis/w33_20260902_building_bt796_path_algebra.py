#!/usr/bin/env python3
"""Compose both building cycle spaces through the 1080 <-> 2160 router.

Upstream exact certificates provide:
  * three primitive St_81 channels and three primitive St_64 channels in the
    1080 obstruction carrier;
  * explicit chain injections from H1(W33) (81) and H1(GQ(4,2)) (64) into
    those six channels;
  * a complete 113-dimensional Hom_G(1080,2160) incidence family whose
    two-step cross-Grams span M3(Q) on both multiplicity-three blocks.

This script closes the composition gap in two complementary senses.

(1) DIRECT CYCLE ROUTING.  It reconstructs the same six chain injections and,
for each primitive channel, chooses an actual 0/1 1080-to-2160 incidence
relation that remains injective on that copy.  Choices are made greedily so the
three 81 images have combined rank 243, the three 64 images rank 192, and all
six images together rank 435 (checked modulo two good primes).  Thus concrete
building cycles, not only abstract multiplicity spaces, are embedded into the
2160 BT796/packet48 carrier.

(2) FULL TWO-STEP PATH ALGEBRA.  For each of the 81 and 64 isotypic blocks it
constructs exact rational matrix units e_ij in End_G(St^3)=M3(Q), then solves
each e_ij as an exact rational linear combination of source-side cross-Grams
R_a R_b^T through the 2160 carrier.  All 18 matrix-unit identities are thereby
realized by explicit two-step incidence paths.

No physical channel interpretation is assumed; this is finite equivariant
linear algebra and building homology.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from functools import lru_cache
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260901_packet48_bt796_crossid as cross
import w33_20260901_obstruction_wedderburn_steinberg_projectors as obs
import w33_20260901_double_steinberg_64_81 as dual
from w33_20260901_steinberg_frame_common import build as build_frame, proportional_scalar
from w33_20260831_c5_wedderburn_kernel import center_equations, generic_center, mulvec
from w33_20260901_building_chain_injections import integer_cycle_basis, rank_mod, lcm_den

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_BUILDING_BT796_PATH_ALGEBRA.json'
PRIMES=(1000003,1000033)


def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))


def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m)));G={I};Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in G:G.add(z);Q.append(z)
    assert len(G)==25920
    return list(G)


def projector_integer(P,rel):
    den=lcm_den(P); coeff=np.array([int(den*q) for q in P],dtype=np.int64)
    return coeff[np.asarray(rel,dtype=np.int64)],den,coeff


def make_matrix_units(frame,E,T,rel,reps):
    zero=sp.zeros(len(E),1)
    tr=[]
    for seed in reps:
        a,b=divmod(seed,1080);tr.append(int(rel[b,a]))
    def sym_orb(k):
        v=sp.zeros(len(E),1);v[k]=1
        if tr[k]!=k:v[tr[k]]+=1
        return mulvec(E,v,T)
    def sandwich(A,B,C):return mulvec(A,mulvec(B,C,T),T)
    def connector(i,j):
        Pi,Pj=frame[i],frame[j]
        for k in range(len(reps)):
            B=sym_orb(k)
            if B==zero:continue
            X=sandwich(Pi,B,Pj);Y=sandwich(Pj,B,Pi)
            if X==zero or Y==zero:continue
            XY=mulvec(X,Y,T);YX=mulvec(Y,X,T)
            a=proportional_scalar(XY,Pi);b=proportional_scalar(YX,Pj)
            if a is not None and b is not None and a==b and a!=0:
                return k,tr[k],X,Y,sp.factor(a)
        raise AssertionError((i,j))
    k01,t01,X01,Y10,a01=connector(0,1)
    k02,t02,X02,Y20,a02=connector(0,2)
    u={(0,0):frame[0],(1,1):frame[1],(2,2):frame[2],
       (0,1):X01,(1,0):Y10/a01,(0,2):X02,(2,0):Y20/a02}
    u[(1,2)]=mulvec(u[(1,0)],u[(0,2)],T)
    u[(2,1)]=mulvec(u[(2,0)],u[(0,1)],T)
    for i,j,k,l in itertools.product(range(3),repeat=4):
        got=mulvec(u[(i,j)],u[(k,l)],T)
        want=u[(i,l)] if j==k else zero
        assert got==want,(i,j,k,l)
    return u,{'01':[k01,t01,str(a01)],'02':[k02,t02,str(a02)]}


def main():
    F=build_frame();acts,rel,reps,T,diag=F['acts'],F['rel'],F['reps'],F['T'],F['diag']
    E81=F['E'];frame81=list(F['frame'])

    # Recover/split St64^3 in the same orbital algebra.
    Zc=center_equations(T).nullspace();one=sp.zeros(59,1);one[diag]=1
    z,_L,_cp,factors,_coeff=generic_center(Zc,T)
    records,idempotents=obs.central_records(z,factors,T,one,diag)
    i64=next(i for i,r in enumerate(records) if r['complexIrrepDegree']==64)
    E64=idempotents[i64]
    split64_label,split64_vals,frame64,_left64=dual.split_three_copies(E64,rel,reps,T,64,diag)

    units81,connect81=make_matrix_units(frame81,E81,T,rel,reps)
    units64,connect64=make_matrix_units(frame64,E64,T,rel,reps)

    D=cross.build();G=D['G'];wlines=D['wlines'];charts=D['charts'];slots=D['slots']
    sli={x:i for i,x in enumerate(slots)};li={frozenset(L):i for i,L in enumerate(wlines)}
    line_sets=[set(L) for L in wlines]
    skew=[(i,j) for i,j in itertools.combinations(range(40),2) if not(line_sets[i]&line_sets[j])]
    skidx={frozenset(x):i for i,x in enumerate(skew)}
    def line_perm(p):return tuple(li[frozenset(p[x] for x in L)] for L in wlines)
    def slot_perm(p):
        lp=line_perm(p);out=[]
        for s,t in slots:
            a,b=skew[s];ns=skidx[frozenset((lp[a],lp[b]))]
            out.append(sli[(ns,lp[t])])
        return tuple(out)
    target_gens=[slot_perm(p) for p in D['g40']]
    source_line=[tuple(acts[k][ell]%40 for ell in range(40)) for k in range(4)]
    assert source_line==[line_perm(p) for p in D['g40']]
    PG=paired_closure(acts,target_gens,1080,2160)
    H=[z for z in PG if z[0][0]==0];assert len(H)==24
    unseen=set(range(2160));orbits=[]
    while unseen:
        o=min(unseen);O={gt[o] for _gs,gt in H};unseen-=O;orbits.append(sorted(O))
    orbits=sorted(orbits,key=lambda O:(len(O),O[0]));assert len(orbits)==113
    trans=[None]*1080
    for gs,gt in PG:
        y=gs[0]
        if trans[y] is None:trans[y]=gt
    assert all(x is not None for x in trans)

    @lru_cache(maxsize=None)
    def raw_cross(i,j):
        Oi=set(orbits[i]);Oj=orbits[j];row=[]
        for y in range(1080):row.append(sum(1 for x in Oj if trans[y][x] in Oi))
        oval=[None]*59
        for y,v in enumerate(row):
            r=int(rel[0,y])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        return sp.Matrix(oval)
    def project(E,V):return mulvec(E,mulvec(V,E,T),T)

    fixed_pairs={
      81:[(0,0),(0,4),(0,5),(0,7),(0,25),(0,45),(1,1),(1,2),(1,5)],
      64:[(0,0),(0,1),(0,4),(1,0),(1,1),(1,2),(1,5),(1,8),(1,9)]}

    path_formulas={}
    for degree,E,units in ((81,E81,units81),(64,E64,units64)):
        vecs=[project(E,raw_cross(a,b)) for a,b in fixed_pairs[degree]]
        B=sp.Matrix.hstack(*vecs);assert B.rank()==9
        formulas={}
        for i,j in itertools.product(range(3),repeat=2):
            sol,_=B.gauss_jordan_solve(units[(i,j)]);assert B*sol==units[(i,j)]
            terms=[]
            for q,c in enumerate(sol):
                if c:
                    terms.append({'crossOrbitPair':list(fixed_pairs[degree][q]),'coefficient':str(sp.factor(c))})
            formulas[f'e{i}{j}']=terms
        path_formulas[str(degree)]={'basisPairs':[list(x) for x in fixed_pairs[degree]],'matrixUnits':formulas}

    # Reconstruct the same chamber->1080 primitive chain injections.
    @lru_cache(maxsize=None)
    def g_line_perm(gi):return line_perm(G[gi][0])
    def target_one(gi,y):
        c,ell=divmod(y,40);return G[gi][2][c]*40+g_line_perm(gi)[ell]
    gen_indices=[]
    for k,a in enumerate(acts):
        # cross.build uses the same four deterministic generators.
        p40=D['g40'][k];p27=D['g27'][k]
        hit=next(i for i,zg in enumerate(G) if zg[0]==p40 and zg[2]==p27)
        assert all(target_one(hit,y)==a[y] for y in range(1080));gen_indices.append(hit)

    wch=[(p,ell) for ell,L in enumerate(wlines) for p in L]
    fch=[(packet,c) for c,C in enumerate(charts) for packet in C]
    wi={x:i for i,x in enumerate(wch)};fi={x:i for i,x in enumerate(fch)}
    def wsrc_one(gi,s):
        p,ell=wch[s];return wi[(G[gi][0][p],g_line_perm(gi)[ell])]
    def fsrc_one(gi,s):
        p,c=fch[s];return fi[(G[gi][1][p],G[gi][2][c])]
    Z81,Z81den=integer_cycle_basis(40,40,wch);Z64,Z64den=integer_cycle_basis(45,27,fch)
    assert Z81den==Z64den==1

    def source_orbit_data(source_n,source_one):
        transport=[None]*source_n;HH=[]
        for gi in range(len(G)):
            s=source_one(gi,0)
            if transport[s] is None:transport[s]=gi
            if s==0:HH.append(gi)
        assert all(x is not None for x in transport)
        unseen=set(range(1080));OO=[]
        while unseen:
            y=min(unseen);O={target_one(gi,y) for gi in HH};unseen-=O;OO.append(tuple(sorted(O)))
        OO.sort(key=lambda O:(len(O),O[0]));return transport,OO
    def columns_for_orbit(transport,O):
        return [tuple(sorted(target_one(transport[s],y) for y in O)) for s in range(len(transport))]
    def selfgram_orbital(columns):
        row=np.zeros(1080,dtype=np.int64)
        for C in columns:
            if 0 in C:row[list(C)]+=1
        oval=[None]*59
        for y,v in enumerate(row.tolist()):
            r=int(rel[0,y])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        return sp.Matrix(oval)
    def source_perm(source_n,source_one,gi):return np.array([source_one(gi,s) for s in range(source_n)],dtype=np.int64)

    def primitive_chain_maps(source_n,source_one,cycle,frame):
        transport,OO=source_orbit_data(source_n,source_one);zero=sp.zeros(59,1);out=[]
        for k,P in enumerate(frame):
            chosen=None
            for oi,O in enumerate(OO):
                cols=columns_for_orbit(transport,O);V=selfgram_orbital(cols)
                if mulvec(P,mulvec(V,P,T),T)!=zero:
                    chosen=(oi,O,cols);break
            assert chosen is not None
            oi,O,cols=chosen;Pnum,Pden,_coeff=projector_integer(P,rel)
            A=np.zeros((1080,source_n),dtype=np.int64)
            for s,C in enumerate(cols):A[:,s]=Pnum[:,list(C)].sum(axis=1)
            Y=A@cycle
            assert all(rank_mod(Y,p)==cycle.shape[1] for p in PRIMES if Pden%p)
            out.append({'primitive':k,'sourceOrbit':oi,'A':A,'Y':Y,'den':Pden})
        return out

    chain81=primitive_chain_maps(160,wsrc_one,Z81,frame81)
    chain64=primitive_chain_maps(135,fsrc_one,Z64,frame64)

    # Apply an actual source->2160 relation R_o^T. Choose relations so target
    # images of the three copies are simultaneously independent.
    def apply_relation(oi,A):
        O=orbits[oi];B=np.zeros((2160,A.shape[1]),dtype=np.int64)
        for y in range(1080):
            row=A[y]
            if not np.any(row):continue
            for t in O:B[trans[y][t]]+=row
        return B

    def choose_target_maps(degree,frame,chains,source_n,source_one,cycle):
        chosen=[];stack_by_p={p:None for p in PRIMES}
        records=[]
        for k,(P,ch) in enumerate(zip(frame,chains)):
            hit=None
            for oi in range(113):
                if project(P,raw_cross(oi,oi))==sp.zeros(59,1):continue
                B=apply_relation(oi,ch['A']);Yt=B@cycle
                if not all(rank_mod(Yt,p)==degree for p in PRIMES):continue
                good=True
                for p in PRIMES:
                    C=Yt if stack_by_p[p] is None else np.concatenate([stack_by_p[p],Yt],axis=1)
                    if rank_mod(C,p)!=(k+1)*degree:good=False;break
                if not good:continue
                # Verify chain-level equivariance through both carriers.
                for gi,gt in zip(gen_indices,target_gens):
                    gs=source_perm(source_n,source_one,gi)
                    if not np.array_equal(B[np.ix_(np.array(gt,dtype=np.int64),gs)],B):
                        raise AssertionError(('target-equivariance',degree,k,oi))
                hit=(oi,B,Yt);break
            assert hit is not None,(degree,k)
            oi,B,Yt=hit
            for p in PRIMES:
                stack_by_p[p]=Yt if stack_by_p[p] is None else np.concatenate([stack_by_p[p],Yt],axis=1)
            records.append({'primitiveIndex':k,'sourcePrimitiveOrbit':ch['sourceOrbit'],'bt796RelationOrbit':oi,
                            'rationalDenominator':int(ch['den']),'targetCycleShape':list(Yt.shape),
                            'targetCycleRankModuloGoodPrimes':{str(p):rank_mod(Yt,p) for p in PRIMES},
                            'targetCycleSHA256Int64LE':hashlib.sha256(np.asarray(Yt,dtype='<i8').tobytes()).hexdigest(),
                            'chainLevelGeneratorEquivarianceVerified':True})
            chosen.append(Yt)
        final={str(p):rank_mod(np.concatenate(chosen,axis=1),p) for p in PRIMES}
        assert set(final.values())=={3*degree}
        return records,chosen,final

    rec81,tgt81,rank81=choose_target_maps(81,frame81,chain81,160,wsrc_one,Z81)
    rec64,tgt64,rank64=choose_target_maps(64,frame64,chain64,135,fsrc_one,Z64)
    all_images=np.concatenate(tgt81+tgt64,axis=1)
    allrank={str(p):rank_mod(all_images,p) for p in PRIMES}
    assert set(allrank.values())=={3*81+3*64}

    out={
      'schema':'w33.20260902.building-bt796-path-algebra.v1','status':'PASS','groupOrder':25920,
      'carriers':{'sourceObstruction':1080,'routerBT796':2160,'equivariantHomDimension':113},
      'St81':{'building':'H1(W33)','degree':81,'primitiveTargetRoutes':rec81,'combinedTargetRankModuloGoodPrimes':rank81,
              'twoStepPathAlgebra':path_formulas['81'],'matrixUnitConnectors':connect81},
      'St64':{'building':'H1(GQ(4,2))','degree':64,'primitiveTargetRoutes':rec64,'combinedTargetRankModuloGoodPrimes':rank64,
              'twoStepPathAlgebra':path_formulas['64'],'matrixUnitConnectors':connect64,
              'splitOperator':split64_label,'splitEigenvalues':[str(x) for x in split64_vals]},
      'allSixTargetImagesCombinedRankModuloGoodPrimes':allrank,
      'allSixCombinedDimension':435,
      'theorem':(
        'The explicit W33 and GQ(4,2) building cycle spaces route through all six primitive obstruction channels into the same 2160 BT796/packet48 carrier with independent target dimensions 243 and 192, total 435. On each multiplicity-three block, all nine rational matrix units are exact linear combinations of two-step 1080->2160->1080 incidence cross-Grams. Hence the BT796 carrier realizes an explicit M3(Q) direct-sum M3(Q) path algebra tied to concrete building cycles.'),
      'boundary':(
        'This is a finite equivariant path algebra. The words route/channel are algebraic: no optical transfer efficiency, Hamiltonian, physical time evolution, or particle-generation interpretation is inferred.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','rank81':rank81,'rank64':rank64,'all':allrank,
                      'routes81':[x['bt796RelationOrbit'] for x in rec81],
                      'routes64':[x['bt796RelationOrbit'] for x in rec64]},sort_keys=True))


if __name__=='__main__':main()
