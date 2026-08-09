#!/usr/bin/env python3
"""Pass 4559 (outside box) -- protected edges are a canonical double cover of O+(8,2) anisotropic classes.

All 240 edge images have weight 20, so q8=20/4=1 on V8=V9/<j>.  Adding the
fixed vector j complements support and pairs the 240 vectors into 120 quotient
classes.  Geometrically this involution has an exact W33 meaning: an edge is
sent to the opposite edge in the unique K4 pencil of four lines through its
intersection point.  Thus the 120 anisotropic classes are the 120 pairings of
opposite edges in the forty geometric line pencils.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4559_EDGE_ANISOTROPIC_DOUBLE_COVER.json'
COLS=[0,1,2,3,4,5,7,8,10,11]
def vm(v):return sum(int(b)<<i for i,b in enumerate(v) if b)
def srg(A):
    deg=set(map(int,A.sum(1)));aa=set();nn=set()
    for i,j in itertools.combinations(range(len(A)),2):
        c=int(np.dot(A[i],A[j]));(aa if A[i,j] else nn).add(c)
    assert len(deg)==len(aa)==len(nn)==1
    return [len(A),next(iter(deg)),next(iter(aa)),next(iter(nn))]
def main():
    vals=build_geometry();lines=vals[2];A=vals[5]
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];assert len(edges)==240
    edge_by_image={vm(A[:,i]^A[:,j]):(i,j) for i,j in edges};assert len(edge_by_image)==240
    jvec=np.ones(40,dtype=np.uint8);jm=vm(jvec)
    seen=set();classes=[]
    for m,e in sorted(edge_by_image.items()):
        if m in seen:continue
        n=m^jm;assert n in edge_by_image
        f=edge_by_image[n];seen|={m,n};classes.append((m,n,e,f))
        # e and f are the two opposite edges of the unique 4-line pencil.
        assert set(e).isdisjoint(f)
        assert all(A[a,b] for a,b in itertools.combinations(set(e)|set(f),2))
        p=set(lines[e[0]])&set(lines[e[1]]);assert len(p)==1
        pencil={li for li,L in enumerate(lines) if p<=set(L)};assert pencil==set(e)|set(f) and len(pencil)==4
    assert len(classes)==120 and len(seen)==240
    # Canonical protected preimages for the polar form B(A b,A c)=b^T A c.
    M=A[:,COLS];assert rank2(M)==10;pre={}
    for z in range(1<<10):
        b=np.zeros(40,dtype=np.uint8);x=np.zeros(40,dtype=np.uint8)
        for k,c in enumerate(COLS):
            if (z>>k)&1:b[c]=1;x^=A[:,c]
        pre[vm(x)]=b
    reps=[C[0] for C in classes];G=np.zeros((120,120),dtype=np.uint8)
    for i,k in itertools.combinations(range(120),2):
        b=pre[reps[i]];c=pre[reps[k]];B=int((b@(A@c%2))%2)
        if B==0:G[i,k]=G[k,i]=1
    assert srg(G)==[120,63,30,36]
    out={'pass':4559,'edge_images':240,'quotient_classes':120,'quotient_relation':'x~x+j where j is the unique fixed all-ones protected vector',
      'quadratic_type':'Every edge image has weight20, hence q8=20/4=1 and represents an anisotropic class.',
      'geometric_involution':'x->x+j sends each W33 line-graph edge to the opposite edge in the unique K4 pencil through the same geometric point.',
      'pencil_count':40,'opposite_edge_pairs_per_pencil':3,'total_opposite_pairs':120,
      'anisotropic_polar_graph_srg':[120,63,30,36],
      'theorem':'The 240 protected edge carrier is a canonical two-sheeted lift of the 120 anisotropic O+(8,2) classes; the deck involution is opposite-edge complementation inside W33 point pencils.',
      'boundary':'Finite quotient geometry only. The two sheets are not physical particle/antiparticle or time-reversal states.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
