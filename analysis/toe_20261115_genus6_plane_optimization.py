#!/usr/bin/env python3
"""Deterministic seeded 36-variable 12-plane genus-six dual face-simplicity search.

Necessary condition ONLY: individual eleven-gon face boundary polygons simple
in their own planes. Does not test global intersection or realizability.
"""
import ast, itertools, json, math, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_genus6_12plane_optimized_necessary.json"

def facets():
    src=ast.parse((ROOT/"analysis"/"w33_genus_six_execution.py").read_text(encoding="utf8"))
    faces=next(ast.literal_eval(v.value) for v in src.body if isinstance(v,ast.Assign)
               and any(isinstance(x,ast.Name) and x.id=="FACETS_ONE" for x in v.targets))
    faces=sorted(tuple(sorted(x-1 for x in f)) for f in faces)
    lookup={f:i for i,f in enumerate(faces)}
    bounds=[]
    for v in range(12):
        n={}
        for f in faces:
            if v not in f:continue
            a,b=[x for x in f if x!=v]
            n.setdefault(a,set()).add(b);n.setdefault(b,set()).add(a)
        q=[min(n),min(n[min(n)])]
        while len(q)<11:q.append(next(iter(n[q[-1]]-{q[-2]})))
        assert q[0] in n[q[-1]]
        bounds.append([lookup[tuple(sorted((v,q[k],q[(k+1)%11])))] for k in range(11)])
    return np.array(faces),np.array(bounds)
F,B=facets()
pairs=np.array([(i,j) for i,j in itertools.combinations(range(11),2)
                if j!=i+1 and not (i==0 and j==10)],dtype=np.int32)
assert len(pairs)==44
u,v=pairs[:,0],pairs[:,1]
v1=(u+1)%11;v2=(v+1)%11
def cross(x,y):
    return x[...,0]*y[...,1]-x[...,1]*y[...,0]

def score(z):
    co=z.reshape(12,3)
    normals=np.column_stack((-co[:,:2],np.ones(12)))
    linear=normals[F]
    determinants=np.linalg.det(linear)
    if np.min(np.abs(determinants))<.005:return 1000,None
    pts=np.linalg.solve(linear,co[F,2][...,None])[...,0]
    if not np.isfinite(pts).all() or np.max(abs(pts))>1e4:return 1000,None
    poly=pts[B,:2]
    a,b,c,d=poly[:,u,:],poly[:,v1,:],poly[:,v,:],poly[:,v2,:]
    o1=cross(b-a,c-a);o2=cross(b-a,d-a)
    o3=cross(d-c,a-c);o4=cross(d-c,b-c)
    crosses=(o1*o2<0)&(o3*o4<0)
    count=int(crosses.sum())
    # Float orientation is only used to find candidates. For the saved
    # best, the exact crossing signs are replayed with rationals on
    # decimal coordinate inputs in a separate validator.
    return count,pts

def run(steps=90000,seed=913):
    rng=np.random.default_rng(seed)
    prev=json.loads(OUT.read_text()) if OUT.exists() else None
    best=(int(prev['best_total_face_self_crossings']),np.array(prev['parameters']).ravel()) if prev else (1000,None)
    total=0; starts=0; improvements=0
    for runid in range(6):
        for trial in range(200):
            if prev:
                z=np.array(prev['parameters']).ravel()+rng.normal(0,.18+runid*.10,36)
                if runid==0 and trial==0:z=np.array(prev['parameters']).ravel().copy()
            else:z=rng.uniform(-1.8,1.8,36)
            val,pts=score(z)
            if val<1000:break
        starts+=1
        curr=z.copy();cost=val
        if val<best[0]:best=(val,z.copy())
        for k in range(steps//6):
            total+=1
            T=max(.20,2.5*(1-k/(steps//6))**1.3)
            scale=.025+.35*T/2.5
            proposal=curr.copy()
            j=rng.integers(0,12)
            prop_count=rng.choice([1,2,3,6,12],p=[.46,.23,.18,.10,.03])
            indexes=rng.choice(12,prop_count,replace=False)
            proposal.reshape(12,3)[indexes,:]+=rng.normal(0,scale,size=(prop_count,3))
            prop,points=score(proposal)
            if prop<best[0]:
                best=(prop,proposal.copy());improvements+=1
                print("BEST",best[0],"run",runid,"iter",k,"trials",total,flush=True)
            if prop<=cost or rng.random()<math.exp(min(0,(cost-prop)/T)):
                curr,cost=proposal,prop
            if best[0]==0:break
        if best[0]==0:break
    best_count,co=best
    ev,pts=score(co)
    assert ev==best_count
    # Verify against original previous results without mutating them.
    result={"status":"GENUS6_12_PLANE_LOCAL_SELF_CROSSING_OPTIMIZATION",
      "source_facets":"analysis/w33_genus_six_execution.py FACETS_ONE",
      "dual_abstract_VEF":[44,66,12],"each_face_length":11,
      "seeds":seed,"local_trials":total,"restarts":starts,"improvements":improvements,
      "best_total_face_self_crossings":best_count,
      "prior_random_search_best_total_face_self_crossings":41,
      "necessary_local_facet_simplicity_passed":best_count==0,
      "parameters":co.reshape(12,3).tolist(),
      "max_vertex_distance_from_origin":float(np.max(np.linalg.norm(pts,axis=1))),
      "minimum_absolute_triple_plane_normal_determinant":float(np.min(np.abs(np.linalg.det(np.column_stack((-co.reshape(12,3)[:,:2],np.ones(12)))[F])))),
      "scope":"Only self-crossings of 12 individual planar face polygons. A zero would still NOT be a 3D embedded genus-six polyhedron; must test all nonincident triangle/edge/face intersections and orientation. A nonzero numerical minimum is not a proof of impossibility."}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    return result
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
