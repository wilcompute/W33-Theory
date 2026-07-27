#!/usr/bin/env python3
"""Pass 1135: exact W(E6)-module decomposition of the 2195-dimensional cubic-map kernel.

The 25 irreducible rows and the 2240-carrier multiplicities are the independently
reconstructed class-algebra data from the clean PR-162 branch. This pass rebuilds
the 45 cubic-support permutation character on the same ATLAS class ordering,
decomposes it, and subtracts it from the 2240 carrier.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1135_cubic_kernel_decomposition.json"

ATLAS = [
 ('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),
 ('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),
 ('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),
 ('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),
 ('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),
 ('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),
 ('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),
 ('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),
 ('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)
]
CLASS_SIZES = np.array([51840 // x[3] for x in ATLAS], dtype=np.int64)
DOMAIN_PERM = np.array([2240,32,160,26,242,8,32,12,20,2,32,2,10,2,2,672,40,8,80,42,6,4,8,2,8], dtype=np.int64)

IRR = [
(1,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],0,'sign'),
(1,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],14,'1'),
(6,[6,-2,2,-3,3,0,2,0,1,1,1,-2,-1,0,-1,-4,0,2,-2,-1,2,0,0,1,-1],0,'6_outer_negative'),
(6,[6,-2,2,-3,3,0,2,0,1,1,1,-2,-1,0,-1,4,0,-2,2,1,-2,0,0,-1,1],16,'6'),
(10,[10,-6,2,1,-2,4,2,-2,0,-3,0,0,2,1,-1,0,0,0,0,0,0,0,0,0,0],0,'10'),
(15,[15,-1,-1,6,3,0,3,-1,0,2,-1,2,-1,0,0,-5,3,-1,-1,1,-2,0,1,0,-1],0,'15_outer_negative'),
(15,[15,-1,-1,6,3,0,3,-1,0,2,-1,2,-1,0,0,5,-3,1,1,-1,2,0,-1,0,1],5,'15'),
(15,[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,-5,-1,-3,1,-2,1,-1,1,0,0],0,'15a_outer_negative'),
(15,[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,5,1,3,-1,2,-1,1,-1,0,0],4,'15a'),
(20,[20,4,-4,-7,2,2,4,0,0,1,-2,-2,2,-1,1,0,0,0,0,0,0,0,0,0,0],0,'20_zero'),
(20,[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,-10,-2,-2,-2,-1,-1,1,0,0,1],0,'20_outer_negative'),
(20,[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1],22,'20'),
(24,[24,8,0,6,0,3,0,0,-1,2,2,-1,0,0,0,-4,-4,0,0,2,-1,-1,0,1,0],0,'24_outer_negative'),
(24,[24,8,0,6,0,3,0,0,-1,2,2,-1,0,0,0,4,4,0,0,-2,1,1,0,-1,0],3,'24'),
(30,[30,-10,2,3,3,3,-2,0,0,-1,-1,-1,-1,0,1,-10,2,4,0,-1,-1,-1,0,0,1],0,'30_outer_negative'),
(30,[30,-10,2,3,3,3,-2,0,0,-1,-1,-1,-1,0,1,10,-2,-4,0,1,1,1,0,0,-1],9,'30'),
(60,[60,-4,4,6,-3,-3,0,0,0,2,-1,-1,1,0,0,-10,-2,2,2,-1,-1,1,0,0,-1],0,'60_outer_negative'),
(60,[60,-4,4,6,-3,-3,0,0,0,2,-1,-1,1,0,0,10,2,-2,-2,1,1,-1,0,0,1],4,'60a'),
(60,[60,12,4,-3,-6,0,4,0,0,-3,0,0,-2,0,1,0,0,0,0,0,0,0,0,0,0],0,'60b'),
(64,[64,0,0,-8,4,-2,0,0,-1,0,0,0,0,1,0,-16,0,0,0,2,2,0,0,-1,0],0,'64_outer_negative'),
(64,[64,0,0,-8,4,-2,0,0,-1,0,0,0,0,1,0,16,0,0,0,-2,-2,0,0,1,0],10,'64'),
(80,[80,-16,0,-10,-4,2,0,0,0,2,2,2,0,-1,0,0,0,0,0,0,0,0,0,0,0],0,'80'),
(81,[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0],0,'81_plus'),
(81,[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0],3,'81_minus'),
(90,[90,-6,-6,9,0,0,2,2,0,-3,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0],1,'90'),
]


def roots_e8():
    roots=[]
    for i in range(8):
        for j in range(i+1,8):
            for si in (1,-1):
                for sj in (1,-1):
                    v=[0]*8;v[i]=2*si;v[j]=2*sj;roots.append(tuple(v))
    for m in range(256):
        v=tuple(-1 if (m>>k)&1 else 1 for k in range(8))
        if sum(x==-1 for x in v)%2==0: roots.append(v)
    assert len(roots)==240
    return roots


def compose(a,b): return a[b]
def invperm(p):
    q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q

def reflection_perm(r,roots,idx):
    out=[]
    for x in roots:
        q=sum(a*b for a,b in zip(x,r))//4
        out.append(idx[tuple(a-q*b for a,b in zip(x,r))])
    return np.array(out,dtype=np.uint8)

def order(p):
    seen=np.zeros(len(p),bool);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=True;j=int(p[j]);l+=1
            o=math.lcm(o,l)
    return o

def enum_group(gens):
    I=np.arange(len(gens[0]),dtype=np.uint8);keys={I.tobytes():0};els=[I];par=[0];q=deque([0])
    while q:
        i=q.popleft();x=els[i]
        for g in gens:
            y=compose(g,x);k=y.tobytes()
            if k not in keys:keys[k]=len(els);els.append(y.copy());par.append(par[i]^1);q.append(len(els)-1)
    return np.stack(els),keys,np.array(par,dtype=np.uint8)
def classes(arr,index,gens):
    trs=[]
    for g in gens:
        gi=invperm(g);C=gi[arr[:,g]];trs.append(np.array([index[row.tobytes()] for row in C],dtype=np.int32))
    unseen=np.ones(len(arr),bool);out=[];co=np.empty(len(arr),dtype=np.int16)
    for seed in range(len(arr)):
        if not unseen[seed]:continue
        unseen[seed]=False;q=deque([seed]);orb=[]
        while q:
            x=q.popleft();orb.append(x)
            for tr in trs:
                y=int(tr[x])
                if unseen[y]:unseen[y]=False;q.append(y)
        co[orb]=len(out);out.append(orb)
    return out,co
def ppower(p,n):
    r=np.arange(len(p),dtype=p.dtype);b=p
    while n:
        if n&1:r=compose(r,b)
        b=compose(b,b);n//=2
    return r
def eval_word(expr,c,d):
    if expr.startswith('('):w,n=expr[1:].split(')^');n=int(n)
    else:w=expr;n=1
    r=np.arange(len(c),dtype=c.dtype)
    for ch in w:r=compose(r,c if ch=='c' else d)
    return ppower(r,n)
def gen_size(gens):
    I=np.arange(len(gens[0]),dtype=np.uint8);seen={I.tobytes()};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x);k=y.tobytes()
            if k not in seen:seen.add(k);q.append(y)
    return len(seen)

def root_orbits(gens,degree=240):
    unseen=set(range(degree));out=[]
    while unseen:
        s=min(unseen);orb={s};q=deque([s])
        while q:
            x=q.popleft()
            for g in gens:
                y=int(g[x])
                if y not in orb:orb.add(y);q.append(y)
        unseen-=orb;out.append(sorted(orb))
    return sorted(out,key=lambda x:(len(x),x[0]))


def main():
    roots=roots_e8();idx={r:i for i,r in enumerate(roots)}
    simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
    gens=[reflection_perm(r,roots,idx) for r in simples]
    G,index,par=enum_group(gens);assert len(G)==51840
    cls,co=classes(G,index,gens);assert len(cls)==25
    rec=[]
    for ci,x in enumerate(cls):
        rep=G[x[0]];rec.append({'ci':ci,'size':len(x),'centralizer':51840//len(x),'order':order(rep),'inner':not bool(par[x[0]])})
    cci=next(r['ci'] for r in rec if not r['inner'] and r['order']==2 and r['centralizer']==1440)
    dci=next(r['ci'] for r in rec if r['inner'] and r['order']==9 and r['centralizer']==9)
    c=G[cls[cci][0]];d=None
    for ii in cls[dci]:
        z=G[ii]
        if order(compose(c,z))==10 and gen_size([c,z])==51840:d=z;break
    assert d is not None
    reps=[];mapping=[]
    for _,word,o,cent in ATLAS:
        x=eval_word(word,c,d);ci=int(co[index[x.tobytes()]]);rr=rec[ci]
        assert rr['order']==o and rr['centralizer']==cent
        reps.append(x);mapping.append(ci)
    assert all(len(cls[mapping[i]])==CLASS_SIZES[i] for i in range(25))

    ro=root_orbits(gens)
    assert [len(x) for x in ro]==[1,1,1,1,1,1,27,27,27,27,27,27,72]
    shell=next(x for x in ro if len(x)==27)
    sum_buckets={}
    for triple in combinations(shell,3):
        total=tuple(sum(roots[i][k] for i in triple) for k in range(8))
        sum_buckets.setdefault(total,[]).append(tuple(sorted(triple)))
    constant,supports=max(sum_buckets.items(),key=lambda kv:len(kv[1]))
    supports=tuple(sorted(supports));assert len(supports)==45
    support_set=set(supports)
    assert all(tuple(sorted(int(g[x]) for x in t)) in support_set for g in gens for t in supports)

    perm45=[]
    for rep in reps:
        fixed=sum(tuple(sorted(int(rep[x]) for x in t))==t for t in supports)
        perm45.append(fixed)
    perm45=np.array(perm45,dtype=np.int64)
    assert perm45[0]==45

    image_mult=[]
    for degree,chi,domain_mult,name in IRR:
        m=int(np.dot(CLASS_SIZES*perm45,np.array(chi,dtype=np.int64))//51840)
        image_mult.append(m)
    assert all(x>=0 for x in image_mult)
    assert sum(IRR[i][0]*image_mult[i] for i in range(25))==45
    image_nonzero=[(IRR[i][3],IRR[i][0],image_mult[i]) for i in range(25) if image_mult[i]]
    assert image_nonzero==[('1',1,1),('20',20,1),('24',24,1)],image_nonzero

    kernel=[]
    for i,(degree,chi,domain_mult,name) in enumerate(IRR):
        km=domain_mult-image_mult[i]
        assert km>=0
        if km:
            kernel.append({'name':name,'degree':degree,'multiplicity':km,'character_sha256':hashlib.sha256(json.dumps(chi,separators=(',',':')).encode()).hexdigest()})
    assert sum(x['degree']*x['multiplicity'] for x in kernel)==2195
    steinberg=next(x for x in kernel if x['name']=='81_minus')
    assert steinberg['multiplicity']==3

    A=np.zeros((45,45),dtype=np.int64)
    for i,s in enumerate(supports):
        ss=set(s)
        for j,t in enumerate(supports):
            if i!=j and ss.isdisjoint(t):A[i,j]=1
    assert np.all(A.sum(axis=1)==32)
    assert np.array_equal(A@A,8*np.eye(45,dtype=np.int64)-2*A+24*np.ones((45,45),dtype=np.int64))
    eig=Counter(np.rint(np.linalg.eigvalsh(A)).astype(int).tolist())
    assert eig==Counter({32:1,2:24,-4:20})

    result={
      'schema':'w33.pass1135.cubic_kernel_decomposition.v1','status':'PASS',
      'headline':'The surjective 2240-to-45 cubic-lift map removes exactly 1+20+24 from the A2 carrier; its kernel is 2195-dimensional and retains all three 81_minus copies.',
      'atlas_class_order':[x[0] for x in ATLAS],
      'cubic_support_constant_sum':list(constant),
      'cubic_permutation_character':perm45.tolist(),
      'cubic_module_decomposition':[{'name':n,'degree':d,'multiplicity':m} for n,d,m in image_nonzero],
      'cubic_support_graph':{'parameters':[45,32,22,24],'spectrum':{'32':1,'2':24,'-4':20}},
      'kernel_dimension':2195,'kernel_decomposition':kernel,
      'kernel_compact':'13*1 + 16*6 + 5*15 + 4*15a + 21*20 + 2*24 + 9*30 + 4*60a + 10*64 + 3*81_minus + 1*90',
      'steinberg_obstruction':{'multiplicity_in_domain':3,'multiplicity_in_cubic_image':0,'multiplicity_in_kernel':3,'statement':'3*81_minus is a direct summand of ker(L_cubic).'},
      'checks':{'we6_order_51840':len(G)==51840,'classes_25':len(cls)==25,'cubic_supports_45':len(supports)==45,'cubic_image_dimension_45':sum(IRR[i][0]*image_mult[i] for i in range(25))==45,'image_is_1_plus_20_plus_24':image_nonzero==[('1',1,1),('20',20,1),('24',24,1)],'kernel_dimension_2195':sum(x['degree']*x['multiplicity'] for x in kernel)==2195,'steinberg_three_in_kernel':steinberg['multiplicity']==3,'cubic_graph_srg':eig==Counter({32:1,2:24,-4:20})},
      'scope':'Exact E8-root/W(E6) permutation computation and exact character inner products. The nine-term firewall restriction is not treated as a W(E6)-submodule.'
    }
    assert all(result['checks'].values())
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','image':image_nonzero,'kernel_dimension':2195,'steinberg':3},indent=2))

if __name__=='__main__':main()
