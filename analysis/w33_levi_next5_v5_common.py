#!/usr/bin/env python3
"""Shared exact substrate for the v5 W33/E6/E8/foundry/runtime witnesses."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Sequence
import hashlib, json, math, struct

import numpy as np


def sha256_json(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canon(v: Iterable[int]) -> tuple[int, int, int, int]:
    v = tuple(int(x) % 3 for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)  # type: ignore[return-value]
    raise ValueError("zero has no projective representative")


def symp(x: Sequence[int], y: Sequence[int]) -> int:
    return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1]) % 3

@dataclass(frozen=True)
class W33:
    points: tuple[tuple[int,int,int,int], ...]
    lines: tuple[frozenset[int], ...]
    incidence: np.ndarray
    adjacency: np.ndarray
    line_adjacency: np.ndarray


def build_w33() -> W33:
    points = tuple(sorted({canon(v) for v in product(range(3), repeat=4) if any(v)}))
    pindex = {p:i for i,p in enumerate(points)}
    adjacency = np.zeros((40,40), dtype=np.uint8)
    line_set:set[frozenset[int]] = set()
    for i,j in combinations(range(40),2):
        if symp(points[i], points[j]):
            continue
        adjacency[i,j]=adjacency[j,i]=1
        x,y=points[i],points[j]
        line=frozenset(
            pindex[canon(tuple((a*x[k]+b*y[k])%3 for k in range(4)))]
            for a,b in product(range(3), repeat=2) if a or b
        )
        line_set.add(line)
    lines=tuple(sorted(line_set,key=lambda s:tuple(sorted(s))))
    assert len(lines)==40 and all(len(x)==4 for x in lines)
    incidence=np.zeros((40,40),dtype=np.uint8)
    for r,line in enumerate(lines):
        for p in line: incidence[r,p]=1
    line_adj=((incidence@incidence.T)>0).astype(np.uint8)^np.eye(40,dtype=np.uint8)
    return W33(points,lines,incidence,adjacency,line_adj)

SEEDS=[
    (1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
    (1,1,0,0),(1,0,1,0),(0,1,0,1),(1,1,1,1),
]


def point_transvection_perm(points,v)->tuple[int,...]:
    idx={p:i for i,p in enumerate(points)}
    return tuple(idx[canon(tuple((x[k]+symp(x,v)*v[k])%3 for k in range(4)))] for x in points)


def point_outer_perm(points)->tuple[int,...]:
    idx={p:i for i,p in enumerate(points)}
    return tuple(idx[canon((x[0],x[1],2*x[2],2*x[3]))] for x in points)


def line_perm_from_point_perm(lines,perm)->tuple[int,...]:
    idx={line:i for i,line in enumerate(lines)}
    return tuple(idx[frozenset(perm[p] for p in line)] for line in lines)


def compose_perm(a,b): return tuple(a[b[i]] for i in range(len(b)))

def invert_perm(p):
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)


def gf2_rank_matrix(a:np.ndarray)->int:
    a=(np.array(a,dtype=np.uint8)&1).copy()
    r=0
    for c in range(a.shape[1]):
        piv=next((i for i in range(r,a.shape[0]) if a[i,c]),None)
        if piv is None: continue
        a[[r,piv]]=a[[piv,r]]
        for i in range(a.shape[0]):
            if i!=r and a[i,c]: a[i]^=a[r]
        r+=1
        if r==a.shape[0]: break
    return r


def gf2_rank(rows:Iterable[int])->int:
    basis={}
    for row in rows:
        x=int(row)
        while x:
            p=x.bit_length()-1
            if p in basis: x^=basis[p]
            else: basis[p]=x; break
    return len(basis)


def gf2_row_basis(rows:Iterable[int])->list[int]:
    basis={}
    for row in rows:
        x=int(row)
        while x:
            p=x.bit_length()-1
            if p in basis: x^=basis[p]
            else: basis[p]=x; break
    return [basis[p] for p in sorted(basis,reverse=True)]


def gf2_nullspace(rows:Iterable[int], width:int)->list[int]:
    work=[int(x) for x in rows]
    piv=[]; r=0
    for c in range(width):
        s=next((i for i in range(r,len(work)) if (work[i]>>c)&1),None)
        if s is None: continue
        work[r],work[s]=work[s],work[r]
        for i in range(len(work)):
            if i!=r and ((work[i]>>c)&1): work[i]^=work[r]
        piv.append(c); r+=1
        if r==len(work): break
    free=[c for c in range(width) if c not in piv]
    out=[]
    for f in free:
        v=1<<f
        for i,p in enumerate(piv):
            if (work[i]>>f)&1: v|=1<<p
        out.append(v)
    return out


def tagged_basis(vectors:list[int])->dict[int,tuple[int,int]]:
    basis={}
    for i,v in enumerate(vectors):
        x=int(v); tag=1<<i
        for p in sorted(basis,reverse=True):
            if (x>>p)&1:
                row,t=basis[p]; x^=row; tag^=t
        if x: basis[x.bit_length()-1]=(x,tag)
    return basis


def coordinates(v:int,basis:dict[int,tuple[int,int]])->tuple[int,int]:
    x=int(v); tag=0
    for p in sorted(basis,reverse=True):
        if (x>>p)&1:
            row,t=basis[p]; x^=row; tag^=t
    return x,tag


def in_span(v:int,basis:list[int])->bool:
    x=v
    for row in gf2_row_basis(basis):
        p=row.bit_length()-1
        if (x>>p)&1: x^=row
    return x==0


def apply_cols(cols:tuple[int,...],v:int)->int:
    out=0
    while v:
        b=v&-v; out^=cols[b.bit_length()-1]; v^=b
    return out


def transpose_mask3(mask:int)->int:
    out=0
    for i in range(3):
        for j in range(3):
            if (mask>>(3*i+j))&1: out|=1<<(3*j+i)
    return out


def matrix_mask3(rows:Sequence[Sequence[int]])->int:
    return sum((int(rows[i][j])&1)<<(3*i+j) for i in range(3) for j in range(3))


def e8_roots():
    roots=[]
    for i,j in combinations(range(8),2):
        for si,sj in product((-2,2),repeat=2):
            v=[0]*8; v[i]=si; v[j]=sj; roots.append(tuple(v))
    for signs in product((-1,1),repeat=8):
        if sum(x<0 for x in signs)%2==0: roots.append(tuple(signs))
    roots=sorted(set(roots)); assert len(roots)==240
    return roots


def ip(a,b):
    val=sum(x*y for x,y in zip(a,b)); assert val%4==0; return val//4


def reflection_perm(roots,alpha):
    idx={r:i for i,r in enumerate(roots)}
    return tuple(idx[tuple(r[i]-ip(r,alpha)*alpha[i] for i in range(8))] for r in roots)


def orbit(seed:int,gens:list[tuple[int,...]])->list[int]:
    seen={seed}; q=deque([seed])
    while q:
        x=q.popleft()
        for g in gens:
            y=g[x]
            if y not in seen: seen.add(y); q.append(y)
    return sorted(seen)


def find_e6_simple_roots(roots72):
    nbr={r:[s for s in roots72 if ip(r,s)==-1] for r in roots72}
    center=roots72[0]
    for a1 in nbr[center]:
      for a0 in nbr[a1]:
       if a0==center or ip(a0,center)!=0: continue
       for a3 in nbr[center]:
        if a3 in {a1,a0} or ip(a3,a1)!=0 or ip(a3,a0)!=0: continue
        for a4 in nbr[a3]:
         if a4 in {center,a1,a0} or any(ip(a4,x)!=0 for x in (center,a1,a0)): continue
         for a5 in nbr[center]:
          if a5 in {a0,a1,a3,a4} or any(ip(a5,x)!=0 for x in (a0,a1,a3,a4)): continue
          simple=[a0,a1,center,a3,a4,a5]
          if np.linalg.matrix_rank(np.array(simple,dtype=float))==6: return simple
    raise RuntimeError('failed E6 simple roots')

ACTIVE=np.array([
[-1,-1,0,2,1,0,1,-3],[-1,-2,-1,4,2,-2,4,-6],[-1,-3,-3,6,2,-2,5,-8],
[-1,-2,-2,4,1,-1,4,-6],[-1,-1,-1,3,0,0,2,-4],[-1,0,0,1,0,0,1,-2],
[0,-1,-1,2,0,0,0,0],[-1,-1,-2,3,1,-1,2,-3]],dtype=float)

# Minimal GDSII writer utilities.
def _gds_real8(value:float)->bytes:
    if value==0: return b'\0'*8
    sign=0x80 if value<0 else 0; value=abs(value); exp=0
    while value>=1: value/=16; exp+=1
    while value<1/16: value*=16; exp-=1
    mant=int(value*(1<<56))
    return bytes([sign|(exp+64)&0x7f])+mant.to_bytes(7,'big')

def _rec(rtype:int,dtype:int,payload:bytes=b'')->bytes:
    n=4+len(payload); return struct.pack('>HBB',n,rtype,dtype)+payload

def gds_library(rects:list[dict],lib='HOLONETV5',cell='TOP')->bytes:
    out=bytearray()
    out+=_rec(0x00,0x02,struct.pack('>H',600))
    out+=_rec(0x01,0x02,b'\0'*24)
    name=lib.encode(); name+=b'\0'*(len(name)%2); out+=_rec(0x02,0x06,name)
    out+=_rec(0x03,0x05,_gds_real8(1e-6)+_gds_real8(1e-9))
    out+=_rec(0x05,0x02,b'\0'*24)
    s=cell.encode(); s+=b'\0'*(len(s)%2); out+=_rec(0x06,0x06,s)
    for r in rects:
        x0,y0,x1,y1=[int(round(1000*r[k])) for k in ('x0','y0','x1','y1')]
        xy=[x0,y0,x1,y0,x1,y1,x0,y1,x0,y0]
        out+=_rec(0x08,0x00)
        out+=_rec(0x0d,0x02,struct.pack('>H',int(r['layer'])))
        out+=_rec(0x0e,0x02,struct.pack('>H',int(r.get('datatype',0))))
        out+=_rec(0x10,0x03,struct.pack('>'+('i'*10),*xy))
        out+=_rec(0x11,0x00)
    out+=_rec(0x07,0x00); out+=_rec(0x04,0x00)
    return bytes(out)
