#!/usr/bin/env python3
"""Resolve the Suzuki Steiner-twin 120 cover against the classical Steiner cover.

The twin cover found inside the U5(2) local 165 has the same four pair-orbit
sizes and 40x3 block system as the classical 120 Steiner trihedral-pair cover,
but its 40-block quotient is the standard W(3,3) point graph.  Pass4870/4954
prove that the classical Steiner quotient is instead the W(3,3) line-
intersection graph, i.e. Q(4,3).

This file identifies the exact difference module.  Point and line permutation
modules both have rational decomposition 1 + 24 + 15.  The literal 40x40
point-line incidence matrix Z obeys

    ZZ^T = 4I + A_point,   Z^T Z = 4I + A_line,

so it has rank 25 and transmits the common 1+24 sector while annihilating the
two distinct 15-dimensional -4 eigenspaces.  Those dual dark 15-spaces, not a
new 4-dimensional module, are the characteristic-zero distinction.  The
mod-3 separator rank(A+I)=11 versus 15 is a modular-extension effect.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_steiner_twin_point_line_dark_module.json'

def canon(v):
    for x in v:
        if x%3:
            z=1 if x%3==1 else 2
            return tuple((z*y)%3 for y in v)
    raise ValueError

def sp(a,b):return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3

def rankp(A,p=3):
    A=np.asarray(A,dtype=np.int64).copy()%p;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r

def main(write=True):
    twin=json.loads((ROOT/'data'/'w33_u52_165_e6_45_120_split.json').read_text())
    old=json.loads((ROOT/'data'/'PART_W33_PASS4952_DUAL_GQ_INCIDENCE_SINGULAR_FILTER.json').read_text())
    assert twin['status']=='PASS' and twin['orbit120']['quotient_rank_F3_A_plus_I']==11
    assert old['rank']==25 and old['left_kernel_dimension']==old['right_kernel_dimension']==15
    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    Ap=np.zeros((40,40),dtype=int)
    for i,j in itertools.combinations(range(40),2):
        if sp(P[i],P[j])==0:Ap[i,j]=Ap[j,i]=1
    lines=[]
    for c in itertools.combinations(range(40),4):
        if all(Ap[i,j] for i,j in itertools.combinations(c,2)):lines.append(c)
    assert len(lines)==40
    Al=np.zeros((40,40),dtype=int);Z=np.zeros((40,40),dtype=int)
    for j,L in enumerate(lines):Z[list(L),j]=1
    for i,j in itertools.combinations(range(40),2):
        if set(lines[i])&set(lines[j]):Al[i,j]=Al[j,i]=1
    assert np.array_equal(Z@Z.T,4*np.eye(40,dtype=int)+Ap)
    assert np.array_equal(Z.T@Z,4*np.eye(40,dtype=int)+Al)
    assert np.linalg.matrix_rank(Z.astype(float))==25 and rankp(Z,3)==25
    rp=rankp(Ap+np.eye(40,dtype=int),3);rl=rankp(Al+np.eye(40,dtype=int),3)
    assert (rp,rl)==(11,15)
    out={
      'schema':'w33.steiner_twin_point_line_dark_module.v1','status':'PASS',
      'headline':'The Suzuki 120 Steiner-twin cover lies over W33 points, while the classical Steiner cover lies over W33 lines/Q(4,3). Their degree-40 rational permutation modules share 1+24+15, and literal point-line incidence transmits exactly 1+24 while annihilating the two distinct 15-dimensional dark sectors. The mod-3 ranks 11 versus 15 are a modular-extension separator, not a new 4D characteristic-zero module.',
      'covers':{'Suzuki_twin_120':{'blocks':40,'quotient':'W33 point graph','rank_F3_A_plus_I':rp},'classical_Steiner_120':{'blocks':40,'quotient':'W33 line graph = Q(4,3)','rank_F3_A_plus_I':rl}},
      'point_line_incidence':{'shape':[40,40],'rank_Q':25,'rank_F3':25,'ZZt':'4I+A_point','ZtZ':'4I+A_line','singular_sector_dimensions':[1,24,15]},
      'difference_module':{'common_transmitted':'1 + 24','point_dark_dimension':15,'line_dark_dimension':15,'interpretation':'dual -4 eigenspaces killed on the left/right by incidence'},
      'modular_boundary':'The numerical rank gap 15-11=4 in A+I over F3 is not by itself a 4-dimensional characteristic-zero representation; the exact rational separator is the pair of dark 15-spaces.',
      'checks':{'twin_rank11':True,'Steiner_rank15':True,'incidence_rank25':True,'Gram_identities':True,'dual_dark15':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
