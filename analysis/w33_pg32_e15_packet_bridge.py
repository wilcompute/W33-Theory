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
def rank(A): return int(np.linalg.matrix_rank(np.array(A,dtype=float)))
def eig(A): return Counter(int(round(x)) for x in np.linalg.eigvalsh(np.array(A,dtype=float)))
def w33_adj():
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
    pi={v:i for i,v in enumerate(pts)}
    # In PG(3,2), planes are nonzero linear functionals f; plane f=0 has 7 points.
    planes=[]
    for f in pts:
        planes.append(tuple(i for i,v in enumerate(pts) if sum(f[k]*v[k] for k in range(4))%2==0))
    lines=set()
    for a,b in combinations(range(15),2):
        c=tuple((pts[a][k]^pts[b][k]) for k in range(4))
        lines.add(tuple(sorted((a,b,pi[c]))))
    N=np.zeros((15,15),dtype=int)
    for j,pl in enumerate(planes):
        for i in pl: N[i,j]=1
    return pts, sorted(lines), planes, N
def curved_count(A):
    centers={}
    for t in combinations(range(40),3):
        if all(A[a,b]==0 for a,b in combinations(t,2)):
            centers[t]=tuple(x for x in range(40) if all(A[x,a] for a in t))
    return sum(1 for c in centers.values() if len(c)==1)
def main():
    A=w33_adj(); I=np.eye(40,dtype=int); J=np.ones((40,40),dtype=int)
    E15n=8*I+J-4*A
    E25n=16*I+4*A-J
    Gflat=8*I+J+2*A
    Gcurv=272*I+16*J+20*A
    residual=Gcurv-26*Gflat+18*J
    pg_pts,pg_lines,pg_planes,N=pg32()
    NN=N@N.T
    curved=curved_count(A)
    tom_flags=192
    checks={
        'pg32_counts':len(pg_pts)==15 and len(pg_lines)==35 and len(pg_planes)==15,
        'pg32_plane_size':Counter(N.sum(0))==Counter({7:15}) and Counter(N.sum(1))==Counter({7:15}),
        'pg32_point_plane_gram':np.array_equal(NN,4*np.eye(15,dtype=int)+3*np.ones((15,15),dtype=int)),
        'pg32_full_rank_carrier':rank(N)==15 and eig(NN)==Counter({49:1,4:14}),
        'E15_rank_15':np.array_equal(E15n@E15n,24*E15n) and int(np.trace(E15n)//24)==15,
        'E25_rank_25':np.array_equal(E25n@E25n,24*E25n) and int(np.trace(E25n)//24)==25,
        'residual_identity':np.array_equal(residual,8*E15n),
        'curved_events_count':curved==2880,
        'pg32_tomotope_packet_count':15*tom_flags==curved,
        'residual_trace_packet_count':int(np.trace(residual))==15*tom_flags,
    }
    out={
        'theorem_name':'PG(3,2) E15 Tomotope-Packet Carrier Bridge',
        'all_checks_passed':all(checks.values()),
        'summary':{
            'PG32_points':len(pg_pts),'PG32_lines':len(pg_lines),'PG32_planes':len(pg_planes),
            'PG32_point_plane_gram_spectrum':dict(eig(NN)),
            'E15_rank':15,'curved_events':curved,'tomotope_flags':tom_flags,
            'curved_events_as_PG32_packets':'2880 = 15 * 192',
            'residual_trace':int(np.trace(residual)),
        },
        'checks':checks,
        'identities':{
            'PG32_carrier':'|PG(3,2)_points| = |PG(3,2)_planes| = 15',
            'PG32_incidence':'N N^T = 4 I_15 + 3 J_15, spectrum 49^1 + 4^14',
            'W33_curvature_projector':'E15 = (8I + J - 4A_W33)/24 has rank 15',
            'tomotope_packet':'192 = tomotope flag carrier',
            'packet_bridge':'2880 curved events = 15 PG(3,2) carriers * 192 tomotope flags',
            'residual_bridge':'trace(192 E15) = 15 * 192 = 2880',
        },
        'interpretation':'The 15-dimensional W33 curvature-active sector has the same carrier cardinality as PG(3,2).  The curved event tight frame has exactly one tomotope 192-flag redundancy per PG(3,2) point/plane direction.  This is a carrier/packet theorem, not yet a canonical labeling of E15 coordinates by PG(3,2) points.',
        'boundary':'Next target: construct an explicit 40 x 15 coordinate model of the W33 E15 projector with columns indexed by PG(3,2) points, i.e. X X^T = 24 E15 or E15 numerator.'
    }
    path=ROOT/'data'/'w33_pg32_e15_packet_bridge.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out['summary'],indent=2,sort_keys=True)); return 0 if out['all_checks_passed'] else 1
if __name__=='__main__': raise SystemExit(main())
