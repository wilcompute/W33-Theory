#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, deque
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math

import numpy as np
import sympy as sp

GROUP_ORDER = 51840
ROOT = Path(__file__).resolve().parent

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
CLASS_SIZES = np.array([GROUP_ORDER // x[3] for x in ATLAS], dtype=np.int64)
IRR = [
(1,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],'sign'),
(1,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],'1'),
(6,[6,-2,2,-3,3,0,2,0,1,1,1,-2,-1,0,-1,-4,0,2,-2,-1,2,0,0,1,-1],'6_outer_negative'),
(6,[6,-2,2,-3,3,0,2,0,1,1,1,-2,-1,0,-1,4,0,-2,2,1,-2,0,0,-1,1],'6'),
(10,[10,-6,2,1,-2,4,2,-2,0,-3,0,0,2,1,-1,0,0,0,0,0,0,0,0,0,0],'10'),
(15,[15,-1,-1,6,3,0,3,-1,0,2,-1,2,-1,0,0,-5,3,-1,-1,1,-2,0,1,0,-1],'15_outer_negative'),
(15,[15,-1,-1,6,3,0,3,-1,0,2,-1,2,-1,0,0,5,-3,1,1,-1,2,0,-1,0,1],'15'),
(15,[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,-5,-1,-3,1,-2,1,-1,1,0,0],'15a_outer_negative'),
(15,[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,5,1,3,-1,2,-1,1,-1,0,0],'15a'),
(20,[20,4,-4,-7,2,2,4,0,0,1,-2,-2,2,-1,1,0,0,0,0,0,0,0,0,0,0],'20_zero'),
(20,[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,-10,-2,-2,-2,-1,-1,1,0,0,1],'20_outer_negative'),
(20,[20,4,4,2,5,-1,0,0,0,-2,1,1,1,-1,0,10,2,2,2,1,1,-1,0,0,-1],'20'),
(24,[24,8,0,6,0,3,0,0,-1,2,2,-1,0,0,0,-4,-4,0,0,2,-1,-1,0,1,0],'24_outer_negative'),
(24,[24,8,0,6,0,3,0,0,-1,2,2,-1,0,0,0,4,4,0,0,-2,1,1,0,-1,0],'24'),
(30,[30,-10,2,3,3,3,-2,0,0,-1,-1,-1,-1,0,1,-10,2,4,0,-1,-1,-1,0,0,1],'30_outer_negative'),
(30,[30,-10,2,3,3,3,-2,0,0,-1,-1,-1,-1,0,1,10,-2,-4,0,1,1,1,0,0,-1],'30'),
(60,[60,-4,4,6,-3,-3,0,0,0,2,-1,-1,1,0,0,-10,-2,2,2,-1,-1,1,0,0,-1],'60_outer_negative'),
(60,[60,-4,4,6,-3,-3,0,0,0,2,-1,-1,1,0,0,10,2,-2,-2,1,1,-1,0,0,1],'60a'),
(60,[60,12,4,-3,-6,0,4,0,0,-3,0,0,-2,0,1,0,0,0,0,0,0,0,0,0,0],'60b'),
(64,[64,0,0,-8,4,-2,0,0,-1,0,0,0,0,1,0,-16,0,0,0,2,2,0,0,-1,0],'64_outer_negative'),
(64,[64,0,0,-8,4,-2,0,0,-1,0,0,0,0,1,0,16,0,0,0,-2,-2,0,0,1,0],'64'),
(80,[80,-16,0,-10,-4,2,0,0,0,2,2,2,0,-1,0,0,0,0,0,0,0,0,0,0,0],'80'),
(81,[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0],'81_plus'),
(81,[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0],'81_minus'),
(90,[90,-6,-6,9,0,0,2,2,0,-3,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0],'90'),
]
IRR_BY_NAME = {name: (degree, np.array(chi, dtype=np.int64)) for degree, chi, name in IRR}


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
    return tuple(roots)


def compose(a,b): return a[b]

def invperm(p):
    q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q

def perm_order(p):
    seen=np.zeros(len(p),bool);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=True;j=int(p[j]);l+=1
            o=math.lcm(o,l)
    return o

def reflection_perm(r,roots,idx):
    out=[]
    for x in roots:
        q=sum(a*b for a,b in zip(x,r))//4
        out.append(idx[tuple(a-q*b for a,b in zip(x,r))])
    return np.array(out,dtype=np.uint8)

def enum_group_np(gens, parity_toggles=None):
    I=np.arange(len(gens[0]),dtype=gens[0].dtype);keys={I.tobytes():0};els=[I];par=[0];q=deque([0])
    if parity_toggles is None: parity_toggles=[1]*len(gens)
    while q:
        i=q.popleft();x=els[i]
        for gi,g in enumerate(gens):
            y=compose(g,x);k=y.tobytes();p=par[i]^parity_toggles[gi]
            if k not in keys:keys[k]=len(els);els.append(y.copy());par.append(p);q.append(len(els)-1)
            else: assert par[keys[k]]==p
    return np.stack(els),keys,np.array(par,dtype=np.uint8)

def conjugacy_classes_np(arr,index,gens):
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
        co[orb]=len(out);out.append(tuple(orb))
    return tuple(out),co

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
    I=np.arange(len(gens[0]),dtype=gens[0].dtype);seen={I.tobytes()};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x);k=y.tobytes()
            if k not in seen:seen.add(k);q.append(y)
    return len(seen)

def standard_cd(G,index,par,classes,class_of):
    rec=[]
    for ci,cls in enumerate(classes):
        rep=G[cls[0]];rec.append({'ci':ci,'size':len(cls),'centralizer':GROUP_ORDER//len(cls),'order':perm_order(rep),'inner':not bool(par[cls[0]])})
    cci=next(r['ci'] for r in rec if not r['inner'] and r['order']==2 and r['centralizer']==1440)
    dci=next(r['ci'] for r in rec if r['inner'] and r['order']==9 and r['centralizer']==9)
    c=G[classes[cci][0]];d=None
    for ii in classes[dci]:
        z=G[ii]
        if perm_order(compose(c,z))==10 and gen_size([c,z])==GROUP_ORDER:d=z;break
    assert d is not None
    reps=[];mapping=[]
    for _,word,o,cent in ATLAS:
        x=eval_word(word,c,d);ci=int(class_of[index[x.tobytes()]]);rr=rec[ci]
        assert rr['order']==o and rr['centralizer']==cent
        reps.append(x);mapping.append(ci)
    assert all(len(classes[mapping[i]])==CLASS_SIZES[i] for i in range(25))
    class_to_atlas={ci:i for i,ci in enumerate(mapping)}
    assert len(class_to_atlas)==25
    atlas_of_element=np.array([class_to_atlas(int(class_of[i]))] for i in range(GROUP_ORDER)],dtype=np.int8)
    return c,d,tuple(reps),atlas_of_element


def root_model():
    roots=roots_e8();idx={r:i in enumerate(roots)}
    simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
    gens=tuple(reflection_perm(r,roots,idx) for r in simples)
    G,index,par=enum_group_np(gens)
    assert len(G)==GROUP_ORDER and Counter(par.tolist())==Counter({0:25920,1:25920})
    classes,class_of=conjugacy_classes_np(G,index,gens);assert len(classes)==25
    c,d,reps,atlas_of_element=standard_cd(G,index,par,classes,class_of)
    return roots,idx,gens,G,index,par,classes,class_of,c,d,reps,atlas_of_element


def build_a2(roots,idx,gens):
    triples=set()
    for i,a in enumerate(roots):
        for j in range(i+1,len(roots)):
            b=roots[j]
            if sum(x*y for x,y in zip(a,b))!=-4:continue
            cc=tuple(-x-y for x,y in zip(a,b));triples.add(tuple(sorted((i,j,idx[cc]))))
    triples=tuple(sorted(triples));assert len(triples)==2240
    tri_idx={t:i in enumerate(triples)}
    actions=[]
    for g in gens:
        actions.append(np.array([tri_idx[tuple(sorted(int(g[x]) for x in t))] for t in triples],dtype=np.int16))
    orbits=orbit_partition(actions,2240)
    assert [len(o) for o in orbits]==[1,1,27,27,27,27,27,27,240,270,270,432,432,432]
    return triples,tri_idx,tuple(actions),orbits

def orbit_partition(actions,degree):
    unseen=np.ones(degree,bool);out=[]
    for seed in range(degree):
        if not unseen[seed]:continue
        unseen[seed]=False;o=[seed];q=deque([seed])
        while q:
            x=q.popleft()
            for g in actions:
                y=int(g[x])
                if unseen[y]:unseen[y]=False;o.append(y);q.append(y)
        out.append(tuple(sorted(o)--)
    return tuple(sorted(out,key=lambda x:( len(x),x[0])))

def image_triple(g,t): return tuple(sorted(int(g[x]) for x in t))
def induced_on_orbit(g,orb,triples,tri_idx,local):
    return np.array([local[tri_idx[image_triple(g,triples[x])]] for x in orb],dtype=np.int16)

def char_decomp(character):
    character=np.array(character,dtype=np.int64);out=[]
    for degree,chi,name in IRR:
        m=int(np.dot(CLASS_SIZES*character,np.array(chi,dtype=np.int64))//GROUP_ORDER)
        if m:out.append({'irrep':name,'degree':degree,'multiplicity':m})
    assert sum(x['degree']*x['multiplicity'] for x in out)==int(character[0])
    return out


def hecke_and_432(root):
    roots,idx,gens,G