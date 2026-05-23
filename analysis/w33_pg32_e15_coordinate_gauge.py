#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; P=3

def cn(v):
    v=tuple(int(x)%P for x in v)
    if v==(0,0,0,0): raise ValueError
    for x in v:
        if x: return tuple(((1 if x==1 else 2)*y)%P for y in v)
def sp(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P
def build_w33():
    pts=[]; seen=set()
    for raw in product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        z=cn(raw)
        if z not in seen: seen.add(z); pts.append(z)
    A=np.zeros((40,40),dtype=int)
    for i,j in combinations(range(40),2):
        if sp(pts[i],pts[j])==0: A[i,j]=A[j,i]=1
    return A
def pg32():
    pts=[v for v in product((0,1), repeat=4) if any(v)]
    planes=[]; affines=[]
    for f in pts:
        planes.append(tuple(i for i,v in enumerate(pts) if sum(f[k]*v[k] for k in range(4))%2==0))
        affines.append(tuple(i for i,v in enumerate(pts) if sum(f[k]*v[k] for k in range(4))%2==1))
    N=np.zeros((15,15),dtype=int); H=np.zeros((15,15),dtype=int)
    for j,pl in enumerate(planes):
        for i in pl: N[i,j]=1
    for j,ah in enumerate(affines):
        for i in ah: H[i,j]=1
    return pts,planes,affines,N,H
def main():
    A=build_w33(); I=np.eye(40); J=np.ones((40,40)); E15n=8*I+J-4*A
    # E15n has eigenvalue 24 on the 15-dimensional E15 sector.
    vals,vecs=np.linalg.eigh(E15n)
    idx=np.argsort(vals)[-15:]
    U=vecs[:,idx]
    # Fix signs deterministically for stable output.
    for k in range(U.shape[1]):
        m=np.argmax(np.abs(U[:,k]))
        if U[m,k]<0: U[:,k]*=-1
    # Build a PG(3,2)-derived orthogonal gauge from point-plane incidence whitening.
    pgpts,planes,affines,N,H=pg32()
    G=N.T@N
    ev,Q=np.linalg.eigh(G.astype(float))
    Gminushalf=Q@np.diag(1/np.sqrt(ev))@Q.T
    O=N@Gminushalf
    # Columns of X are indexed by the 15 PG(3,2) points/directions.
    X=U*np.sqrt(24)@O.T
    gram=X@X.T; colgram=X.T@X
    # Affine half-space packets: each nonzero functional selects 8 PG directions.
    packet_sums=[]
    for ah in affines:
        packet_sums.append(X[:,list(ah)].sum(axis=1))
    Pmat=np.stack(packet_sums,axis=1)
    Pgram=Pmat.T@Pmat
    plane_sums=[]
    for pl in planes:
        plane_sums.append(X[:,list(pl)].sum(axis=1))
    Lmat=np.stack(plane_sums,axis=1)
    Lgram=Lmat.T@Lmat
    checks={
        'E15_coordinate_realization':np.allclose(gram,E15n,atol=1e-8),
        'orthogonal_pg32_columns':np.allclose(colgram,24*np.eye(15),atol=1e-8),
        'pg32_plane_counts':Counter(N.sum(axis=0))==Counter({7:15}) and Counter(N.sum(axis=1))==Counter({7:15}),
        'pg32_affine_counts':Counter(H.sum(axis=0))==Counter({8:15}) and Counter(H.sum(axis=1))==Counter({8:15}),
        'plane_intersections':Counter(int(N[:,i]@N[:,j]) for i,j in combinations(range(15),2))==Counter({3:105}),
        'affine_intersections':Counter(int(H[:,i]@H[:,j]) for i,j in combinations(range(15),2))==Counter({4:105}),
        'affine_packet_norm_192':Counter(int(round(Pgram[i,i])) for i in range(15))==Counter({192:15}),
        'affine_packet_overlap_96':Counter(int(round(Pgram[i,j])) for i,j in combinations(range(15),2))==Counter({96:105}),
        'plane_packet_norm_168':Counter(int(round(Lgram[i,i])) for i in range(15))==Counter({168:15}),
        'plane_packet_overlap_72':Counter(int(round(Lgram[i,j])) for i,j in combinations(range(15),2))==Counter({72:105}),
    }
    out={
        'theorem_name':'PG(3,2) E15 Coordinate Gauge and 192 Affine-Packet Theorem',
        'all_checks_passed':all(checks.values()),
        'summary':{
            'PG32_directions':15,
            'E15_rank':15,
            'coordinate_identity':'X X^T = 24 E15 = 8I + J - 4A',
            'column_gram':'X^T X = 24 I_15',
            'affine_halfspace_size':8,
            'affine_packet_norm_squared':192,
            'affine_packet_overlap':96,
            'plane_size':7,
            'plane_packet_norm_squared':168,
            'plane_packet_overlap':72,
        },
        'checks':checks,
        'identities':{
            'PG32_planes':'15 projective planes, each size 7, pairwise intersection size 3',
            'PG32_affine_halfspaces':'15 complements of planes / affine half-spaces, each size 8, pairwise intersection size 4',
            'E15_coordinate_gauge':'columns indexed by PG(3,2) directions, with X^T X = 24 I',
            'tomotope_packet':'each affine 8-packet has squared norm 8*24 = 192',
            'packet_gram':'affine packet Gram = 96 I_15 + 96 J_15',
        },
        'interpretation':'The rank-15 W33 curvature-active sector admits a PG(3,2)-indexed coordinate gauge. In this gauge, each PG(3,2) affine half-space of 8 directions carries squared norm 192, matching the tomotope flag-carrier scale. This upgrades the relation from a cardinality match to a coordinate-packet theorem.',
        'boundary':'The orthogonal basis inside E15 is unique only up to O(15); the PG(3,2) incidence matrix fixes a natural PG-labeled gauge, but not yet a canonical automorphism-equivariant identification of W33 E15 coordinates with PG(3,2) directions.'
    }
    path=ROOT/'data'/'w33_pg32_e15_coordinate_gauge.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if out['all_checks_passed'] else 1
if __name__=='__main__': raise SystemExit(main())
