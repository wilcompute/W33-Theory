#!/usr/bin/env python3
"""Pass 1525: exact frame +4 eigenspace to harmonic signed-edge bridge.

This script rebuilds W(3,3), PSp(4,3), the clique-chain complex, the frame graph,
and an integral Reynolds intertwiner. It verifies over the integers that the
projected 240 x 540 map has rank 81 and lands exactly in ker(d1) cap ker(d2^T).
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, itertools, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_frame_hoffman_resolution_theorem.py'

def load_base():
    spec=importlib.util.spec_from_file_location('frame_hoffman',BASE)
    mod=importlib.util.module_from_spec(spec);assert spec.loader is not None;spec.loader.exec_module(mod)
    return mod

def certificate()->dict:
    w=load_base();g=w.build_geometry()
    pts=g['points'];A=g['point_adjacency'];lines=g['lines'];edges=g['edges'];frames=g['frames'];H=g['frame_graph']
    pidx={p:i for i,p in enumerate(pts)}
    lidx={tuple(sorted(L)):i for i,L in enumerate(lines)}
    fidx={tuple(sorted(f)):i for i,f in enumerate(frames)}
    eidx={e:i for i,e in enumerate(edges)}
    def trans(v):
        v=w.normalize(v);out=[]
        for x in pts:
            c=w.symplectic(x,v);y=tuple((x[i]+c*v[i])%3 for i in range(4));out.append(pidx[w.normalize(y)])
        return tuple(out)
    def comp(p,q):return tuple(q[p[i]] for i in range(40))
    ident=tuple(range(40))
    gens=[trans(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0)]]
    group=[ident];seen={ident};queue=collections.deque([ident])
    while queue:
        a=queue.popleft()
        for gen in gens:
            b=comp(a,gen)
            if b not in seen:seen.add(b);group.append(b);queue.append(b)
    assert len(group)==25920
    def line_perm(p):return tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines)
    def edge_image(p,k):
        a,b=edges[k];aa,bb=p[a],p[b]
        return (eidx[(aa,bb)],1) if aa<bb else (eidx[(bb,aa)],-1)
    d1=np.zeros((40,240),dtype=np.int64)
    for j,(a,b) in enumerate(edges):d1[a,j]=-1;d1[b,j]=1
    triangles=[t for L in lines for t in itertools.combinations(sorted(L),3)]
    d2=np.zeros((240,160),dtype=np.int64)
    for j,(a,b,c) in enumerate(triangles):
        d2[eidx[(b,c)],j]=1;d2[eidx[(a,c)],j]=-1;d2[eidx[(a,b)],j]=1
    P4=np.eye(540,dtype=np.int64);I=np.eye(540,dtype=np.int64)
    for lam in (32,14,8,2,-4):P4=P4@(H-lam*I)
    scalar=-17920
    seed_frame=0;seed_edge=4;T=np.zeros((240,540),dtype=np.int64)
    a0,b0=frames[seed_frame]
    for p in group:
        lp=line_perm(p);f=fidx[tuple(sorted((lp[a0],lp[b0])))]
        e,s=edge_image(p,seed_edge);T[e,f]+=s
    B=T@P4
    checks={
      'group_order_25920':len(group)==25920,
      'chain_complex':not np.any(d1@d2),
      'rank_d1_39':np.linalg.matrix_rank(d1.astype(float))==39,
      'rank_d2_120':np.linalg.matrix_rank(d2.astype(float))==120,
      'betti_h1_81':240-39-120==81,
      'P4_eigenidentity':not np.any(H@P4-4*P4),
      'P4_rank_81':np.linalg.matrix_rank(P4.astype(float))==81,
      'bridge_rank_81':np.linalg.matrix_rank(B.astype(float),tol=1e-7)==81,
      'bridge_closed':not np.any(d1@B),
      'bridge_coclosed':not np.any(d2.T@B),
      'bridge_domain_eigenvalue_4':not np.any(B@H-4*B),
    }
    def signed_edge_matrix(p):
        S=np.zeros((240,240),dtype=np.int64)
        for k in range(240):e,s=edge_image(p,k);S[e,k]=s
        return S
    def frame_matrix(p):
        lp=line_perm(p);R=np.zeros((540,540),dtype=np.int64)
        for k,(a,b) in enumerate(frames):R[fidx[tuple(sorted((lp[a],lp[b])))],k]=1
        return R
    for i,p in enumerate(gens,1):
        S=signed_edge_matrix(p);R=frame_matrix(p)
        checks[f'equivariant_generator_{i}']=not np.any(S@T-T@R)
        checks[f'projected_equivariant_generator_{i}']=not np.any(S@B-B@R)
    checks={k:bool(v) for k,v in checks.items()};assert all(checks.values())
    sha=lambda X:hashlib.sha256(np.ascontiguousarray(X).tobytes()).hexdigest()
    return {
      'schema':'w33.pass1525.frame_harmonic_bridge.v1','status':'PASS',
      'theorem':'The +4 frame eigenspace is PSp(4,3)-equivariantly isomorphic to the 81-dimensional harmonic signed-edge sector.',
      'construction':{'seed_frame':seed_frame,'seed_edge':seed_edge,'T_shape':[240,540],'B_shape':[240,540],
        'projector_polynomial':'(H-32I)(H-14I)(H-8I)(H-2I)(H+4I)','projector_scalar_on_E4':scalar},
      'ranks':{'d1':39,'d2':120,'harmonic':81,'P4':81,'bridge':81},
      'integer_ranges':{'T':[int(T.min()),int(T.max())],'B':[int(B.min()),int(B.max())]},
      'hashes':{'T_int64_sha256':sha(T),'P4_int64_sha256':sha(P4),'B_int64_sha256':sha(B)},
      'checks':checks,
      'boundary':'An exact finite-module identification only; no Hodge star, action functional, or continuum dynamics is inferred.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--check',action='store_true');a=ap.parse_args()
    result=certificate();text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(text,encoding='utf-8')
    if not a.check or not a.output:print(text,end='')
if __name__=='__main__':main()
