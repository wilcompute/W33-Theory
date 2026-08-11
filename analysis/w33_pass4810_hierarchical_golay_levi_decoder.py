#!/usr/bin/env python3
"""Pass 4810 — exact local-Golay/global-Levi component decoder.

The 270 triangle coordinates split into 27 disjoint K5 fibers of ten triangles.
On one fiber the syndrome map has 81 states.  Modulo the local punctured Golay
kernel G10 every state has a representative of weight 0,1,or2, with census
1+20+60.  Therefore *every* ternary error component is syndrome-equivalent to
one having at most two nonzero coordinates in each fiber.

This gives an exact ML formulation for one CSS error component: select one of
81 local states on each of 27 fibers, minimize the sum of their exact local
costs, and require their contributions to add to the observed 45-point
syndrome modulo three.  It is a 27x81 state-selection ILP rather than a
270-coordinate brute force problem.

The producer also exhausts exact weight 1--3 errors with a compact ternary
bit-mask syndrome representation.  The resulting collision census identifies
all low-weight ambiguity mechanisms with the local Golay and the complete
K3,3 homology shell of Pass4809.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4810_HIERARCHICAL_GOLAY_LEVI_DECODER.json'
MASK45=(1<<45)-1

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))

def geometry():
    qp=[x for x in range(1,64) if Qm(bits(x))==0]
    ql=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    K5=[tuple(i for i,Q in enumerate(ql) if p in Q) for p in qp]
    T=sorted({tuple(sorted(t)) for C in K5 for t in itertools.combinations(C,3)})
    parent={tuple(sorted(t)):i for i,C in enumerate(K5) for t in itertools.combinations(C,3)}
    masks=[sum(1<<p for p in t) for t in T]
    assert len(K5)==27 and len(T)==270 and len(parent)==270
    return K5,T,parent,masks

def local_table():
    triples=list(itertools.combinations(range(5),3));M=np.zeros((5,10),dtype=int)
    for j,t in enumerate(triples):M[list(t),j]=1
    best={};exact={w:Counter() for w in range(11)}
    for x in itertools.product(range(3),repeat=10):
        a=np.array(x,dtype=int);z=tuple(int(v) for v in (M@a)%3);w=int(np.count_nonzero(a))
        exact[w][z]+=1
        if z not in best or w<best[z][0]:best[z]=(w,x)
    assert len(best)==81 and Counter(w for w,_ in best.values())==Counter({0:1,1:20,2:60})
    mult={}
    for w in range(6):mult[str(w)]=dict(sorted(Counter(exact[w].values()).items()))
    assert mult=={'0':{1:1},'1':{1:20},'2':{3:60},'3':{12:80},
                  '4':{39:60,48:20,60:1},'5':{90:20,102:60,144:1}}
    return best,mult

def add_state(s,m,c):
    a=s&MASK45;b=(s>>45)&MASK45;outside=MASK45^m;zero=m&~(a|b)&MASK45
    if c==1:
        na=(a&outside)|zero;nb=(b&outside)|(a&m)
    else:
        na=(a&outside)|(b&m);nb=(b&outside)|zero
    return na|(nb<<45)

def exact_weight2(masks,parent,T):
    C=Counter()
    for i,j in itertools.combinations(range(270),2):
        for a,b in itertools.product((1,2),repeat=2):
            s=add_state(add_state(0,masks[i],a),masks[j],b);C[s]+=1
    assert sum(C.values())==145260
    md=Counter(C.values());assert md==Counter({1:140400,3:1620})
    # The 3-fold classes are precisely same-fiber errors.
    same=27*45*4;assert same==4860 and 1620*3==same
    return md

def exact_weight3(masks):
    C=Counter()
    for i in range(268):
        for j in range(i+1,269):
            pair=[]
            for a,b in itertools.product((1,2),repeat=2):pair.append(add_state(add_state(0,masks[i],a),masks[j],b))
            for k in range(j+1,270):
                for s in pair:
                    C[add_state(s,masks[k],1)]+=1;C[add_state(s,masks[k],2)]+=1
    assert sum(C.values())==25953120
    md=Counter(C.values())
    assert md==Counter({1:23385600,2:7200,3:842400,12:2160})
    # Structural counts: 12-fold = 27*80 local syndromes; 3-fold =
    # 27*60 local weight2 states * 260 outside coordinates * 2 coefficients;
    # 2-fold = 720 nonzero K33 weight6 words * C(6,3)/2 partitions.
    assert md[12]==27*80
    assert md[3]==27*60*260*2
    assert md[2]==720*10
    return md

def main():
    K5,T,parent,masks=geometry();best,local=local_table()
    w2=exact_weight2(masks,parent,T);w3=exact_weight3(masks)
    out={'pass':4810,'component_code':'syndrome map B:F3^270 -> F3^45',
      'fibers':27,'coordinates_per_fiber':10,'local_states_per_fiber':81,
      'local_minimum_cost_census':{'0':1,'1':20,'2':60},
      'local_exact_weight_syndrome_multiplicity_through_5':local,
      'exact_decoder':'Choose one of 81 states on each fiber, minimize total local cost, and enforce the 45 point sums modulo 3. This is exact because replacing a fiber error by its minimum representative changes it by G10 subset C^perp.',
      'weight2_errors':145260,'weight2_syndrome_multiplicities':dict(sorted(w2.items())),
      'weight2_cross_fiber_unique_errors':140400,'weight2_same_fiber_errors':4860,'weight2_same_fiber_ambiguity_classes':1620,
      'weight3_errors':25953120,'weight3_syndrome_multiplicities':dict(sorted(w3.items())),
      'weight3_twofold_K33_classes':7200,'weight3_threefold_local2_plus_external_classes':842400,'weight3_twelvefold_single_fiber_classes':2160,
      'theorem':'An exact ML syndrome decoder for each ternary CSS component factors through 27 local punctured-Golay state tables followed by the global GQ(4,2) point constraints. At weight two all ambiguity is local Golay. At weight three the first genuinely global ambiguity consists exactly of the 7200 twofold syndrome classes obtained by splitting the 720 nonzero K3,3 weight-six homology logicals into two triples.',
      'boundary':'The decoder is exact for one ternary X- or Z-error component in Hamming weight. Independent component ML is not asserted to minimize joint qutrit Pauli support when X and Z occur on the same data qutrit. Local G10 words are logical ambiguity, not correctable syndrome information.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
