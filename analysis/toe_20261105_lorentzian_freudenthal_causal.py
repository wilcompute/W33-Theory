#!/usr/bin/env python3
"""Lorentzian 4D Freudenthal refinement and explicit causal-orientation firewall.

Exact triangulation of [0,N]^4 by 24 Freudenthal 4-simplices/hypercube.
Check 4-simplex Gram inertia (-+++), integrated 4-volume, Euler chi=1,
time direction, and timelike-edge propagation. Show S4 chi=2 obstruction
to globally nonsingular Lorentzian metric, and a one-way causal skeleton
from a fixed oriented simplicial subdivision even in flat spacetime.
No Regge curvature/constraint algebra is claimed.
"""
from __future__ import annotations
from itertools import product,permutations,combinations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_lorentzian_refinement_causal_firewall.json"

def triangulation(n):
    vertex=set();facets=[set() for _ in range(5)]
    for base in product(range(n),repeat=4):
        for perm in permutations(range(4)):
            s=[tuple(base)]
            x=np.array(base,dtype=int)
            for k in perm:
                x=x.copy();x[k]+=1
                s.append(tuple(map(int,x)))
            vertex.update(s)
            for k in range(1,6):
                facets[k-1].update(combinations(s,k))
    # subsets in simplex are already globally sorted due monotone coords
    f=[len(a) for a in facets]
    assert f[0]==len(vertex)
    assert sum((-1)**k*f[k] for k in range(5))==1
    return vertex,facets,f

def causal_and_signature(n,time_step):
    vertex,faces,f=triangulation(n)
    # Eigenvalue signs are simplex-permutation dependent in value, not inertia.
    metric=np.diag([-time_step**2,1,1,1])
    total4=0; signatures=set();samples=[]
    for base in product(range(n),repeat=4):
        for p in permutations(range(4)):
            pts=[np.array(base,dtype=float)]
            point=np.array(base,dtype=float)
            for k in p:
                point=point.copy();point[k]+=1;pts.append(point)
            J=np.array(pts[1:])-pts[0]
            G=J@metric@J.T
            ev=np.linalg.eigvalsh(G)
            signature=(int(sum(ev< -1e-9)),int(sum(ev>1e-9)))
            assert signature==(1,3),ev
            signatures.add(signature)
            det=float(np.linalg.det(G))
            vol=math.sqrt(abs(det))/24
            assert abs(vol-time_step/24)<1e-11
            total4+=vol
    assert abs(total4-time_step*n**4)<1e-9
    directed=0;spatial=0;positive=0;negative=0;timelike_edges=0
    for a,b in faces[1]:
        if a[0]==b[0]:continue
        future,past=(b,a) if b[0]>a[0] else (a,b)
        delta=np.array(future)-np.array(past)
        ds2=time_step*time_step*delta[0]**2-np.sum(delta[1:]**2)
        if ds2>1e-12:
            timelike_edges+=1;directed+=1
            if np.any(delta[1:]!=0):
                spatial+=1
                if np.any(delta[1:]>0):positive+=1
                if np.any(delta[1:]<0):negative+=1
    assert negative==0
    if time_step<1:assert spatial==0
    if time_step>1:assert spatial>0 and positive>0
    return dict(n=n,metric_timestep=time_step,
        f_vector=f,euler_characteristic=sum((-1)**k*f[k] for k in range(5)),
        four_simplices=f[4],four_volume=total4,
        metric_signatures=[list(s) for s in signatures],
        future_directed_timelike_edges=directed,
        timelike_edges_with_spatial_transport=spatial,
        positive_spatial_future_steps=positive,
        negative_spatial_future_steps=negative,
        parity_asymmetric_timelike_1_skeleton=(spatial>0 and negative==0))

def scalar_fem_action(n):
    """Massless Lorentzian scalar kinetic action for a sampled smooth field."""
    total=0.
    for base in product(range(n),repeat=4):
        for perm in permutations(range(4)):
            pts=[np.array(base,dtype=float)/n]
            q=np.array(base,dtype=float)
            for k in perm:
                q=q.copy();q[k]+=1
                pts.append(q/n)
            pts=np.asarray(pts)
            field=np.prod(np.sin(np.pi*pts),axis=1)
            J=pts[1:]-pts[0]
            gradient=np.linalg.solve(J,field[1:]-field[0])
            volume=abs(float(np.linalg.det(J)))/24
            total+=.5*volume*(-gradient[0]**2+sum(gradient[1:]**2))
    return float(total)

def main():
    rows=[causal_and_signature(n,t) for n in (1,2,3) for t in (.37,1.2)]
    assert all(z["euler_characteristic"]==1 for z in rows)
    assert all(z["metric_signatures"]==[[1,3]] for z in rows)
    s4_f=[6,15,20,15,6]
    chi_s4=sum((-1)**k*v for k,v in enumerate(s4_f))
    assert chi_s4==2
    continuum_scalar_action=math.pi**2/16
    fem=[{"n":n,"Lorentzian_FEM_action":scalar_fem_action(n)} for n in (2,3,4,5)]
    for row in fem:
        row["absolute_error"]=abs(row["Lorentzian_FEM_action"]-continuum_scalar_action)
    assert all(a["absolute_error"]>b["absolute_error"] for a,b in zip(fem[:-1],fem[1:]))
    assert fem[-1]["absolute_error"]<.021
    # On compact boundaryless even-dimensional M, existence of a
    # globally nonsingular Lorentz metric forces chi(M)=0.
    out={"status":"PASS_4D_LORENTZIAN_GRID_REFINEMENT_AND_CAUSAL_ARTIFACT",
         "spatial_lattice_step":1,
         "vertex_ordering":"Freudenthal simplices formed by cumulative +coordinate increments",
         "rows":rows,
         "massless_scalar_FEM_continuum_action":continuum_scalar_action,
         "massless_scalar_FEM_refinement":fem,
         "scalar_action_model":"S=1/2 integral(-dt(phi)^2+dx(phi)^2+dy(phi)^2+dz(phi)^2), phi=product sin(pi*x_mu) on unit box",
         "curved_regge_S4_closed_f_vector":s4_f,
         "curved_regge_S4_euler_characteristic":chi_s4,
         "S4_lorentzian_no_go":"The closed compact 4-sphere chi=2 cannot support a global nonsingular Lorentz metric. An open time-slab chi=1 is not obstructed by this closed-manifold theorem.",
         "new_discretization_control":"With timestep .37, the timelike 1-skeleton cannot change spatial coordinates; with timestep 1.2 it allows spatial movement only in +coordinate directions under this Freudenthal ordering. Neither behavior follows from continuum Minkowski lightcones; they are mesh artefacts.",
         "physical_boundary":"Signature and causal link counts are kinematic only; no Lorentzian Regge deficit angles, constraints, quantum amplitudes or continuum convergence proof."}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for row in rows:print("PASS LORENTZ",row["n"],row["metric_timestep"],row["f_vector"],row["timelike_edges_with_spatial_transport"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
