#!/usr/bin/env python3
"""Independent heavy census for the 19-vertex star complements used in the
nonexistence proof of SRG(57,14,1,4).

The enumeration is independent through the 3,720 candidate star complements.
The published all-candidate compatibility-clique histogram is not recomputed by
this file; see Pass 3529's explicit evidence boundary.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

PAIRS=[(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13)]
EXPECTED_STAGE_COUNTS=[22,784,157349]
EXPECTED_SURVIVORS=3720
EXPECTED_SHA="c1e0cb753fbdeab4d8ecf8059896b6ff1eb1fcc75c663022ab7040ceea012219"

def bitperm(x:int,perm:tuple[int,...])->int:
    y=0
    for r,old in enumerate(perm):
        if (x>>old)&1:
            y|=1<<r
    return y

def canon_state(rows:list[frozenset[int]],out_edges:frozenset[tuple[int,int]]):
    t=len(rows)
    best=None
    pats=[sum(((1 if leaf in rows[r] else 0)<<r) for r in range(t)) for leaf in range(14)]
    for perm in itertools.permutations(range(t)):
        pair_desc=[]
        for a,b in PAIRS:
            va=bitperm(pats[a],perm)
            vb=bitperm(pats[b],perm)
            pair_desc.append(tuple(sorted((va,vb))))
        pair_desc=tuple(sorted(pair_desc))
        inv={old:new for new,old in enumerate(perm)}
        edges=tuple(sorted(tuple(sorted((inv[a],inv[b]))) for a,b in out_edges))
        key=(edges,pair_desc)
        if best is None or key<best:
            best=key
    return best

def build_graph(rows:list[frozenset[int]],out_edges:frozenset[tuple[int,int]])->np.ndarray:
    n=1+14+len(rows)
    A=np.zeros((n,n),dtype=np.uint8)
    for leaf in range(14):
        A[0,1+leaf]=A[1+leaf,0]=1
    for a,b in PAIRS:
        A[1+a,1+b]=A[1+b,1+a]=1
    for r,neighbors in enumerate(rows):
        v=15+r
        for leaf in neighbors:
            A[v,1+leaf]=A[1+leaf,v]=1
    for a,b in out_edges:
        A[15+a,15+b]=A[15+b,15+a]=1
    return A

def valid_extension(rows,out_edges,leafset,adjacent_outs):
    new_index=len(rows)
    new_rows=rows+[frozenset(leafset)]
    new_edges=set(out_edges)
    new_edges.update(tuple(sorted((new_index,o))) for o in adjacent_outs)
    new_edges=frozenset(new_edges)
    A=build_graph(new_rows,new_edges)
    common=A@A
    for i in range(len(A)):
        if int(A[i].sum())>14:
            return None
        for j in range(i+1,len(A)):
            bound=1 if A[i,j] else 4
            if int(common[i,j])>bound:
                return None
    return new_rows,new_edges

def extend(states):
    out={}
    for rows,edges in states.values():
        t=len(rows)
        for leafset in itertools.combinations(range(14),4):
            for mask in range(1<<t):
                adjacent=[o for o in range(t) if (mask>>o)&1]
                candidate=valid_extension(rows,edges,leafset,adjacent)
                if candidate is None:
                    continue
                nr,ne=candidate
                out.setdefault(canon_state(nr,ne),(nr,ne))
    return out

def enumerate_candidates(stop_after:int=3):
    base_rows=[frozenset({0,2,4,6})]
    base_edges=frozenset()
    states={canon_state(base_rows,base_edges):(base_rows,base_edges)}
    counts=[]
    for _ in range(stop_after):
        states=extend(states)
        counts.append(len(states))
    return states,counts

def spectral_survivors(states):
    survivors=[]
    for rows,edges in states.values():
        eigenvalues=np.linalg.eigvalsh(build_graph(rows,edges).astype(float))
        if float(eigenvalues[-2]) < 2.0-1e-9:
            survivors.append((rows,edges))
    keys=sorted(canon_state(rows,edges) for rows,edges in survivors)
    digest=hashlib.sha256(json.dumps(keys,separators=(",",":")).encode()).hexdigest()
    return survivors,digest

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--quick",action="store_true",
                        help="verify only the first two extension stages")
    parser.add_argument("--json",type=Path)
    args=parser.parse_args()
    if args.quick:
        _,counts=enumerate_candidates(2)
        assert counts==EXPECTED_STAGE_COUNTS[:2]
        result={"status":"PASS_QUICK_STAR_STAGES","stage_counts":counts}
    else:
        states,counts=enumerate_candidates(3)
        assert counts==EXPECTED_STAGE_COUNTS
        survivors,digest=spectral_survivors(states)
        assert len(survivors)==EXPECTED_SURVIVORS
        assert digest==EXPECTED_SHA
        result={
            "status":"PASS_3720_STAR_COMPLEMENT_CANDIDATES",
            "stage_counts":counts,
            "spectral_survivors":len(survivors),
            "canonical_survivor_sha256":digest,
            "boundary":"Compatibility-clique histogram is not recomputed here.",
        }
    if args.json:
        args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(result["status"],result)

if __name__=="__main__":
    main()
