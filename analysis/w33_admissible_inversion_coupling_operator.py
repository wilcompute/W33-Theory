#!/usr/bin/env python3
"""BT516: Admissible Inversion Coupling Operator Theorem.

This executes Next Idea 1 from BT515.

Local part:
  The Richter octahedron O has vertices ±(2/5)e_i.  Radial inversion sends
  them to the polar cube face centers ±(5/2)e_i.  At the graph level this is
  the identity on the six K4-edge channels, i.e. the admissible inversion
  operator preserves the L(K4) octahedral carrier.

Global W33 test:
  Rebuild the BT514 even/odd signed-Xmin matrices Q+ and Q-.  Their coupling
  C=Q+Q-^T has rank 24.  This script proves that the nonzero left singular
  space of C is exactly the lift of the 24-dimensional +2 eigenspace of the
  W33 collinearity graph to the 160 projective Xmin-pair space.

Thus the radial-dual inversion/coupling channel is not arbitrary: it is the
W33 24-sector lifted through local octahedral projective pairs.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

P_FIELD=3
Vec=tuple[int,int,int,int]

def canonical(v)->Vec:
    vv=tuple(int(x)%P_FIELD for x in v)
    if vv==(0,0,0,0): raise ValueError('zero')
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P_FIELD for y in vv)  # type: ignore[return-value]
    raise AssertionError

def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P_FIELD

def build_geometry():
    points=[]; seen=set()
    for raw in itertools.product(range(P_FIELD), repeat=4):
        if raw==(0,0,0,0): continue
        c=canonical(raw)
        if c not in seen:
            seen.add(c); points.append(c)
    pidx={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in itertools.combinations(range(len(points)),2) if omega(points[i],points[j])==0]
    adj=np.zeros((40,40),dtype=int)
    for i,j in edges: adj[i,j]=adj[j,i]=1
    lines=set()
    for i,j in edges:
        u,v=points[i],points[j]
        line=set()
        for a,b in itertools.product(range(P_FIELD), repeat=2):
            if a==0 and b==0: continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines)
    point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))]=li
    return points,edges,adj,lines,point_lines,edge_to_line

def ordinary_quadrangles(adj):
    quads=[]; seen=set(); n=len(adj)
    for a,b in itertools.combinations(range(n),2):
        if adj[a,b]: continue
        common=[x for x in range(n) if adj[a,x] and adj[b,x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen:
                seen.add(cyc); quads.append(cyc)
    return quads

def local_signed_faces(p:int,Ls:list[int]):
    Ls=sorted(Ls); faces=[]; v2f=defaultdict(list)
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=tuple(sorted(tuple(sorted((L,M))) for M in others))
        opp=tuple(sorted(tuple(sorted(pair)) for pair in itertools.combinations(others,2)))
        fs=(p,L,+1); fo=(p,L,-1)
        faces.extend([fs,fo])
        for v in star: v2f[(p,v)].append(fs)
        for v in opp: v2f[(p,v)].append(fo)
    return faces,v2f

def orth(A:np.ndarray, tol:float=1e-8)->np.ndarray:
    Q,R=np.linalg.qr(A)
    if R.size==0: return Q[:,[]]
    keep=np.abs(np.diag(R))>tol
    return Q[:,keep]

def main()->dict:
    # Local admissible inversion certificate.
    r=sp.Rational(2,5); h=sp.Rational(5,2)
    oct_vertices=[(r,0,0),(-r,0,0),(0,r,0),(0,-r,0),(0,0,r),(0,0,-r)]
    inv=[tuple(sp.simplify(x/(r*r)) for x in v) for v in oct_vertices]
    assert set(inv)=={(h,0,0),(-h,0,0),(0,h,0),(0,-h,0),(0,0,h),(0,0,-h)}

    points,edges,adj,lines,point_lines,edge_to_line=build_geometry()
    quads=ordinary_quadrangles(adj)
    signed_faces=[]; local_vertex_to_faces={}
    for p in range(40):
        faces,v2f=local_signed_faces(p,point_lines[p])
        signed_faces.extend(faces); local_vertex_to_faces.update(v2f)
    signed_faces=sorted(signed_faces)
    pairs=sorted({(p,L) for p,L,s in signed_faces})
    sf_idx={f:i for i,f in enumerate(signed_faces)}
    pair_idx={pair:i for i,pair in enumerate(pairs)}

    M=np.zeros((320,len(quads)),dtype=np.int16)
    for qi,cyc in enumerate(quads):
        inc=defaultdict(list)
        for u,v in cyc:
            inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            for f in local_vertex_to_faces[(p,lpair)]: M[sf_idx[f],qi]+=1
    Qp=np.zeros((160,len(quads)),dtype=np.int16); Qm=np.zeros((160,len(quads)),dtype=np.int16)
    for p,L in pairs:
        i=pair_idx[(p,L)]
        Qp[i]=M[sf_idx[(p,L,+1)]]+M[sf_idx[(p,L,-1)]]
        Qm[i]=M[sf_idx[(p,L,+1)]]-M[sf_idx[(p,L,-1)]]
    C=Qp@Qm.T
    CC=C@C.T
    assert np.linalg.matrix_rank(C.astype(float))==24
    evals,evecs=np.linalg.eigh(CC.astype(float))
    U=orth(evecs[:,np.isclose(evals,77760)])
    assert U.shape==(160,24)

    # Lift the W33 +2 eigenspace from point-space to projective-pair space.
    w,V=np.linalg.eigh(adj.astype(float))
    assert Counter(np.round(w,6))==Counter({12.0:1,2.0:24,-4.0:15})
    V2=V[:,np.isclose(w,2)]
    S=np.zeros((160,40))
    for i,(p,L) in enumerate(pairs): S[i,p]=1
    lifted=orth(S@V2)
    assert lifted.shape==(160,24)
    projector_error=float(np.linalg.norm(U@U.T - lifted@lifted.T))
    assert projector_error < 1e-10

    results={
        'theorem':'BT516 Admissible Inversion Coupling Operator Theorem',
        'local_radial_inversion':{'octahedron_radius':'2/5','polar_face_center_radius':'5/2','operator':'x -> x/(x·x)','preserves_channel_graph':'L(K4)'},
        'global_coupling':{'C':'Qplus Qminus^T','rank':24,'CCt_spectrum':{'77760':24,'0':136},'singular_value':'72*sqrt(15)'},
        'eigenspace_match':{'W33_collinearity_eigenspace':'lambda=2 multiplicity 24','lift':'projective pair space via (p,L)->p','projector_error':projector_error,'match':True},
        'substrate_reading':{'24':'radial-dual even/odd coupling is exactly the lifted W33 +2 sector','40':'base W33 point carrier','160':'projective Xmin pair space','77760':'72^2*15 coupling-square eigenvalue'}
    }
    out=Path('data/PART_BT516_ADMISSIBLE_INVERSION_COUPLING_OPERATOR_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))
    return results

if __name__=='__main__': main()
