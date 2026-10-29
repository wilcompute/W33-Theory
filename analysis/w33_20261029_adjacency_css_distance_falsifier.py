#!/usr/bin/env python3
"""Deterministic exact minimum-distance certificates for odd-q adjacency CSS codes.
Finite geometry is reconstructed; 64-bit projection is a *linear* map, not a
probabilistic assertion: absence of collisions proves absence of real collisions.
q=5 examines all C(156,4)=23,738,715 quartets; q=7 all C(400,3)=10,586,800 triples.
"""
from __future__ import annotations
import hashlib, json
from itertools import combinations
from math import comb
from pathlib import Path
import numpy as np

from w33_incidence_even_line_resolution_20261029 import make_geometry, rank_basis, reduce_row

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261029_adjacency_css_distance_falsifier.json"
SEED="W33-20261029-FIXED-LINEAR-PROJECTION-v1"

def projected_columns(rows):
    n=len(rows)
    basis=[int.from_bytes(hashlib.sha256(f"{SEED}:{i}".encode()).digest()[:8],"little")
           for i in range(n)]
    masks=[]
    for row in rows:
        v=0
        while row:
            low=row & -row
            v ^= basis[low.bit_length()-1]
            row ^= low
        masks.append(v)
    return np.array(masks,dtype=np.uint64)

def enumerate_projected_sums(h, degree):
    n=len(h)
    size=comb(n,degree)
    out=np.empty(size,dtype=np.uint64)
    pos=0
    if degree==3:
        for i in range(n-2):
            for j in range(i+1,n-1):
                length=n-j-1
                out[pos:pos+length]=h[i]^h[j]^h[j+1:]
                pos+=length
    elif degree==4:
        for i in range(n-3):
            for j in range(i+1,n-2):
                v=h[i]^h[j]
                for k in range(j+1,n-1):
                    length=n-k-1
                    out[pos:pos+length]=v^h[k]^h[k+1:]
                    pos+=length
    else:
        raise ValueError("degree must be 3 or 4")
    assert pos==size
    out.sort()
    collision_indices=np.flatnonzero(out[1:]==out[:-1])
    collisions=int(collision_indices.size)
    # A deterministic replay fingerprint: sorted little-endian 64-bit array.
    digest=hashlib.sha256(out.astype("<u8",copy=False).tobytes()).hexdigest()
    return {"degree":degree,"combinations":size,"projected_collisions":collisions,
            "sorted_projection_sha256":digest,"linear_projection_seed":SEED}

def witness(q,lines,A):
    B=rank_basis(A)
    masks=[sum(1<<i for i in line) for line in lines]
    for i,x in enumerate(masks):
        for y in masks[i+1:]:
            if (x&y).bit_count()==1:
                z=x^y
                assert z.bit_count()==2*q
                assert reduce_row(z,B)!=0
                return {"weight":z.bit_count(),"support":list(i for i in range(len(A)) if (z>>i)&1),
                        "not_a_stabilizer":True}
    raise AssertionError("no intersecting lines")

def compute(q,degree):
    pts,lines,lm,A,N,*_=make_geometry(q)
    h=projected_columns(A)
    c=enumerate_projected_sums(h,degree)
    assert c["projected_collisions"]==0, "unexpected collision; inspect exact support"
    # Key lemma: for every even-weight kernel S with 0<|S|<=2d,
    # take d-set T meeting S in |S|/2. Then |T|=|T xor S|=d
    # and their full, hence projected, syndromes agree.
    # Thus collision freedom EXCLUDES any such kernel word.
    assert all((a.bit_count()&1)==0 for a in rank_basis(A).values())
    w=witness(q,lines,A)
    lower=2*degree+2
    out={"q":q,"n":len(A),"rank_A":len(rank_basis(A)),
         "k":len(A)-2*len(rank_basis(A)), "weight_exclusion_through":2*degree,
         "distance_lower_bound":lower,"distance_upper_bound":w["weight"],
         "witness":w,"collision_certificate":c}
    if lower==w["weight"]:
        out["distance_exact"]=lower
    return out

def main():
    results=[compute(5,4),compute(7,3)]
    assert results[0]["distance_exact"]==10
    assert results[1]["distance_lower_bound"]==8
    OUT.write_text(json.dumps({"proof":"Injective fixed 64-bit linear projection on all d-element adjacency column sums certifies no even kernel word of weight <=2d; even parity follows from 1 in im A. Intersecting line differences certify nonstabilizer upper bound.","results":results},indent=2)+"\n",encoding="utf8")
    for result in results:
        print("q",result["q"],"distance",result.get("distance_exact",f'[{result["distance_lower_bound"]},{result["distance_upper_bound"]}]'),
              "checked tuples",result["collision_certificate"]["combinations"],
              "hash",result["collision_certificate"]["sorted_projection_sha256"])
    print("PASS: exact q=5 CSS distance; certified q=7 distance interval")
if __name__=="__main__":main()
