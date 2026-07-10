#!/usr/bin/env python3
"""Shared exact substrate for the five v3 W33 closures."""
from __future__ import annotations

from collections import deque
from itertools import combinations, product
from dataclasses import dataclass
from typing import Iterable

import numpy as np


def canon(v: Iterable[int]) -> tuple[int, int, int, int]:
    v = tuple(int(x) % 3 for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise ValueError("zero has no projective representative")


def symp(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


@dataclass(frozen=True)
class W33:
    points: tuple[tuple[int, int, int, int], ...]
    lines: tuple[frozenset[int], ...]
    incidence: np.ndarray
    adjacency: np.ndarray
    line_adjacency: np.ndarray


def build_w33() -> W33:
    points = tuple(sorted({canon(v) for v in product(range(3), repeat=4) if any(v)}))
    pindex = {p:i for i,p in enumerate(points)}
    adjacency = np.zeros((40,40), dtype=np.int64)
    line_set: set[frozenset[int]] = set()
    for i,j in combinations(range(40),2):
        if symp(points[i], points[j]) != 0:
            continue
        adjacency[i,j] = adjacency[j,i] = 1
        x,y = points[i],points[j]
        line = frozenset(
            pindex[canon(tuple((a*x[k] + b*y[k]) % 3 for k in range(4)))]
            for a,b in product(range(3),repeat=2) if a or b
        )
        line_set.add(line)
    lines = tuple(sorted(line_set, key=lambda s: tuple(sorted(s))))
    assert len(lines)==40 and all(len(l)==4 for l in lines)
    incidence = np.zeros((40,40), dtype=np.int64)
    for r,line in enumerate(lines):
        for p in line: incidence[r,p]=1
    line_adj = (incidence @ incidence.T > 0).astype(np.int64) - np.eye(40,dtype=np.int64)
    return W33(points, lines, incidence, adjacency, line_adj)


def point_transvection_perm(points, v) -> tuple[int,...]:
    idx={p:i for i,p in enumerate(points)}
    out=[]
    for x in points:
        b=symp(x,v)
        y=canon(tuple((x[k]+b*v[k])%3 for k in range(4)))
        out.append(idx[y])
    return tuple(out)


def point_outer_perm(points) -> tuple[int,...]:
    idx={p:i for i,p in enumerate(points)}
    out=[]
    for x in points:
        y=canon((x[0],x[1],2*x[2],2*x[3]))
        out.append(idx[y])
    return tuple(out)


def line_perm_from_point_perm(lines, perm) -> tuple[int,...]:
    idx={line:i for i,line in enumerate(lines)}
    return tuple(idx[frozenset(perm[p] for p in line)] for line in lines)


def compose_perm(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    """a after b."""
    return tuple(a[b[i]] for i in range(len(a)))


def invert_perm(p: tuple[int,...]) -> tuple[int,...]:
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)


def group_closure_perms(gens: list[tuple[int,...]], max_size: int|None=None) -> set[tuple[int,...]]:
    n=len(gens[0]); e=tuple(range(n)); seen={e}; q=deque([e])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose_perm(g,x)
            if y not in seen:
                seen.add(y); q.append(y)
                if max_size and len(seen)>max_size:
                    raise RuntimeError("group exceeded expected size")
    return seen


def permute_mask(mask:int, perm:tuple[int,...]) -> int:
    out=0
    while mask:
        b=mask & -mask; i=b.bit_length()-1; out |= 1<<perm[i]; mask ^= b
    return out


def gf2_rank(rows: Iterable[int]) -> int:
    basis={}
    for row in rows:
        x=int(row)
        while x:
            p=x.bit_length()-1
            if p in basis: x ^= basis[p]
            else: basis[p]=x; break
    return len(basis)


def gf2_row_basis(rows: Iterable[int]) -> list[int]:
    basis={}
    for row in rows:
        x=int(row)
        while x:
            p=x.bit_length()-1
            if p in basis: x ^= basis[p]
            else: basis[p]=x; break
    return [basis[p] for p in sorted(basis, reverse=True)]


def gf2_nullspace(rows: Iterable[int], width:int) -> list[int]:
    work=[int(x) for x in rows]; piv=[]; r=0
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


def tagged_basis(vectors:list[int]) -> dict[int,tuple[int,int]]:
    basis={}
    for i,v in enumerate(vectors):
        x=int(v); tag=1<<i
        for p in sorted(basis,reverse=True):
            if (x>>p)&1:
                row,t=basis[p]; x^=row; tag^=t
        if x: basis[x.bit_length()-1]=(x,tag)
    return basis


def coordinates(v:int, basis:dict[int,tuple[int,int]]) -> tuple[int,int]:
    x=int(v); tag=0
    for p in sorted(basis,reverse=True):
        if (x>>p)&1:
            row,t=basis[p]; x^=row; tag^=t
    return x,tag


def quotient_basis(kernel:list[int], image:list[int]) -> list[int]:
    span=gf2_row_basis(image); out=[]
    for v in kernel:
        tagged=tagged_basis(span)
        rem,_=coordinates(v,tagged)
        if rem:
            out.append(v); span=gf2_row_basis(span+[v])
    return out


def matrix_rows_to_masks(a: np.ndarray) -> list[int]:
    rows=[]
    for r in range(a.shape[0]):
        mask=0
        for c in range(a.shape[1]):
            if int(a[r,c])&1: mask|=1<<c
        rows.append(mask)
    return rows


def gf2_apply(rows:list[int], v:int) -> int:
    out=0
    for i,row in enumerate(rows):
        if ((row&v).bit_count()&1): out|=1<<i
    return out


def homology_action(differential: np.ndarray, perms: list[tuple[int,...]]):
    rows=matrix_rows_to_masks(differential%2)
    image=gf2_row_basis(rows)
    kernel=gf2_nullspace(rows, differential.shape[1])
    hom=quotient_basis(kernel,image)
    tagged=tagged_basis(image+hom)
    gens=[]
    for perm in perms:
        cols=[]
        for rep in hom:
            moved=permute_mask(rep,perm)
            rem,tag=coordinates(moved,tagged)
            assert rem==0
            cols.append(tag>>len(image))
        gens.append(tuple(cols))
    return image,hom,gens


def apply_cols(cols:tuple[int,...], v:int) -> int:
    out=0
    while v:
        b=v&-v; out ^= cols[b.bit_length()-1]; v^=b
    return out


def invariant_span(seed:int, gens:list[tuple[int,...]]) -> tuple[list[int],int]:
    orbit={seed}; q=deque([seed])
    while q:
        x=q.popleft()
        for g in gens:
            y=apply_cols(g,x)
            if y not in orbit: orbit.add(y); q.append(y)
    return gf2_row_basis(orbit),len(orbit)


def restrict_action(gens:list[tuple[int,...]], basis:list[int]) -> list[tuple[int,...]]:
    tagged=tagged_basis(basis); out=[]
    for g in gens:
        cols=[]
        for v in basis:
            rem,tag=coordinates(apply_cols(g,v),tagged); assert rem==0; cols.append(tag)
        out.append(tuple(cols))
    return out


def weight_q(mask:int) -> int:
    return (mask.bit_count()//2)&1


def dot2(a:int,b:int)->int:
    return (a&b).bit_count()&1


def orbit_sizes(perms:list[tuple[int,...]], n:int)->list[int]:
    seen=bytearray(n); out=[]
    for s in range(n):
        if seen[s]: continue
        seen[s]=1; q=deque([s]); count=0
        while q:
            x=q.popleft(); count+=1
            for p in perms:
                y=p[x]
                if not seen[y]: seen[y]=1; q.append(y)
        out.append(count)
    return sorted(out)


def sha256_json(obj) -> str:
    import hashlib,json
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def invariant_linear_span(seed:int, gens:list[tuple[int,...]]) -> list[int]:
    """Small MeatAxe primitive: close the F2 span of seed under generators."""
    basis: dict[int,int]={}
    queue=deque()
    def add(v:int)->bool:
        x=v
        for p in sorted(basis,reverse=True):
            if (x>>p)&1: x^=basis[p]
        if not x: return False
        p=x.bit_length()-1
        for q in list(basis):
            if (basis[q]>>p)&1: basis[q]^=x
        basis[p]=x; queue.append(x); return True
    add(seed)
    while queue:
        v=queue.popleft()
        for g in gens: add(apply_cols(g,v))
    return [basis[p] for p in sorted(basis,reverse=True)]


def compose_cols(a:tuple[int,...], b:tuple[int,...]) -> tuple[int,...]:
    return tuple(apply_cols(a,c) for c in b)


def group_closure_cols(gens:list[tuple[int,...]], dim:int, max_size:int|None=None)->set[tuple[int,...]]:
    e=tuple(1<<i for i in range(dim)); seen={e}; q=deque([e])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose_cols(g,x)
            if y not in seen:
                seen.add(y); q.append(y)
                if max_size and len(seen)>max_size: raise RuntimeError('linear group exceeded bound')
    return seen
