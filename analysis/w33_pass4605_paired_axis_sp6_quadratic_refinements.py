#!/usr/bin/env python3
"""Pass 4605 -- forget the 27|36 color and the paired axes enlarge to Sp(6,2).

Pass4592 identifies the paired coordinate set with all 63 nonzero vectors of
F2^6. Keep the alternating polar form B but forget which points are singular or
anisotropic for the chosen minus quadratic q. Joining x,y when B(x,y)=1 gives
SRG(63,32,16,16), the standard symplectic graph Sp(6,2). Its natural linear
symmetry group has order 1,451,520. The subgroup preserving q is O^-(6,2) of
order 51,840, index 28; this is exactly the PGSp(4,3) symmetry retained by the
27|36 cubic coloring.

The index 28 has an intrinsic quadratic meaning. All quadratic refinements of B
are q_v(x)=q(x)+B(v,x), v in F2^6. Relative to a minus q, the 28 vectors with
q(v)=0 (including zero) give the 28 minus refinements; the 36 anisotropic v give
36 plus refinements. Thus the same 27+36 coordinate split can also be read as
"the other 27 minus refinements + the 36 plus refinements" relative to the base
minus form. This is an exact affine geometry of quadratic refinements, not a
count-only sporadic-group identification.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4605_PAIRED_AXIS_SP6_QUADRATIC_REFINEMENTS.json'

def q(x):
    # three anisotropic binary planes = parity of nonzero F4 coordinates
    return sum(((x>>(2*i))&3)!=0 for i in range(3))&1
def B(x,y):return q(x^y)^q(x)^q(y)
def main():
    V=list(range(1,64));A=np.zeros((63,63),dtype=np.uint8)
    for i,j in itertools.combinations(range(63),2):
        if B(V[i],V[j]):A[i,j]=A[j,i]=1
    deg=A.sum(1);assert set(map(int,deg))=={32}
    lam=set();mu=set()
    for i,j in itertools.combinations(range(63),2):
        c=int(np.dot(A[i].astype(int),A[j].astype(int)))
        (lam if A[i,j] else mu).add(c)
    assert lam==mu=={16}
    sing=[v for v in range(64) if q(v)==0];anis=[v for v in range(64) if q(v)==1]
    assert (len(sing),len(anis))==(28,36)
    # equitable 27|36 coloring on nonzero points
    S=[v for v in V if q(v)==0];T=[v for v in V if q(v)==1]
    def nbr_counts(v):return (sum(B(v,w) for w in S),sum(B(v,w) for w in T))
    assert {nbr_counts(v) for v in S}=={(16,16)}
    assert {nbr_counts(v) for v in T}=={(12,20)}
    sp6=2**9*(2**2-1)*(2**4-1)*(2**6-1);ominus=51840
    assert sp6==1451520 and sp6//ominus==28
    # q_v types via zero counts.
    types=[]
    for v in range(64):
        z=sum((q(x)^B(v,x))==0 for x in range(64))
        types.append(z)
    assert sum(z==28 for z in types)==28 and sum(z==36 for z in types)==36
    out={'pass':4605,'uncolored_graph':{'vertices':63,'adjacency':'B(x,y)=1','srg':[63,32,16,16],'name':'symplectic graph Sp(6,2)','natural_group_order':sp6},'quadratic_coloring':{'minus_nonzero_singular':27,'anisotropic':36,'equitable_quotient':[[16,16],[12,20]],'color_preserving_group':'O^-(6,2)=PGSp(4,3)','order':ominus,'index_in_Sp6':28},'quadratic_refinements':{'total':64,'minus_type':28,'plus_type':36,'formula':'q_v(x)=q(x)+B(v,x)','relative_split':'base q plus 27 other minus refinements and 36 plus refinements'},'boundary':'Exact finite symplectic/quadratic geometry. The 28/36 refinement counts are not identified with an external sporadic or algebraic-geometric carrier without a separate intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
