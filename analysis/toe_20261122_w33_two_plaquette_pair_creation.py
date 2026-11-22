"""A Gauss-exact two-plaquette Z2 quantum-link model embedded into W(3,3).

Select two 4-cycles sharing edge 0-36. Six matter-spin sites and seven
electric X eigenbits yield unconstrained 2**(6+7)=8192 states, reduced by
six Gauss constraints to exactly 2**7=128 physical states. Every electric
link config uniquely determines site occupation parity. Edge flipping
toggles both endpoint matter bits (pair creation/annihilation/hopping).
Plaquette Wilson loops flip 4 X bits and respect every Gauss constraint.
This is a finite graph patch, NOT experimental (2+1)D confinement.
"""
from __future__ import annotations
import json,sys
from collections import deque
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261122_experiment_driven_five_fronts import W33
OUT=ROOT/"data/toe_20261122_w33_two_plaquette_pair_creation.json"

def geometry():
    A=W33();a=(0,36,9,37)
    assert all(A[a[i],a[(i+1)%4]]for i in range(4))
    options=[(0,36,x,y) for x in range(40)for y in range(40)
             if len({0,36,x,y,9,37})==6 and A[36,x]and A[x,y]and A[y,0]]
    assert options
    b=min(options)
    vertices=sorted(set(a+b));d={x:i for i,x in enumerate(vertices)}
    faces=[[d[x]for x in f]for f in (a,b)]
    edges=sorted(set(tuple(sorted((f[i],f[(i+1)%4])))for f in faces for i in range(4)))
    mask=[sum(1<<edges.index(tuple(sorted((f[i],f[(i+1)%4]))))for i in range(4))for f in faces]
    assert len(vertices)==6 and len(edges)==7
    assert (mask[0]&mask[1]).bit_count()==1
    return vertices,faces,edges,mask

def main():
    vertices,faces,edges,masks=geometry()
    nv,ne=6,7;N=1<<ne;bits=np.arange(N)
    occ=np.array([[sum((b>>e)&1 for e,(u,v)in enumerate(edges)if u==i or v==i)%2
                  for i in range(nv)]for b in bits],dtype=int)
    assert np.all(occ.sum(axis=1)%2==0)
    for e,(u,v) in enumerate(edges):
        other=bits^(1<<e)
        for i in range(nv):
            assert np.all((occ[other,i]!=occ[:,i])==(i in (u,v)))
    electric=np.array([ne-2*int(x).bit_count()for x in bits])
    matter=occ.sum(axis=1)
    H_pair=np.zeros((N,N))
    for e in range(ne):H_pair[bits,bits^(1<<e)]-=1
    W=[]
    for mask in masks:
        f=np.zeros((N,N))
        f[bits,bits^mask]=1
        assert np.max(abs(f@f-np.eye(N)))<1e-12
        W.append(f)
    assert np.max(abs(W[0]@W[1]-W[1]@W[0]))<1e-12
    assert np.max(abs(H_pair@W[0]-W[0]@H_pair))<1e-12
    # Every electric bit configuration is a physical Gauss state;
    # fixed charges are specified by the occupation parity vector.
    def fixed_energy(charges,h=1):
        idx=np.flatnonzero((occ==charges).all(axis=1))
        assert len(idx)==4
        return -h*electric[idx].max()
    vac=np.zeros(nv,dtype=int);E0=fixed_energy(vac)
    costs=[]
    adj=[[]for _ in range(nv)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    for a in range(nv):
        for b in range(a+1,nv):
            charge=np.zeros(nv,dtype=int);charge[[a,b]]=1
            delta=fixed_energy(charge)-E0
            Q=deque([(a,0)]);visited={a}
            while Q:
                node,d=Q.popleft()
                if node==b:break
                for v in adj[node]:
                    if v not in visited:visited.add(v);Q.append((v,d+1))
            assert abs(delta-2*d)<1e-12
            costs.append({"pair":[vertices[a],vertices[b]],"distance":d,"electric_energy_over_vacuum":float(delta)})
    rng=[]
    vacuum=np.zeros(N);vacuum[0]=1
    for name,J,h,B,m in (("weak_creation",.15,.6,.2,.7),
                          ("strong_creation",.7,.6,.2,.7),
                          ("large_plaquette",.7,.6,1.2,.7)):
        H=J*H_pair-h*np.diag(electric)-B*(W[0]+W[1])+m*np.diag(matter)
        ev,U=eigh(H)
        for time in (0,.5,1.5,3):
            psi=U@(np.exp(-1j*ev*time)*(U.conj().T@vacuum))
            p=abs(psi)**2
            assert abs(p.sum()-1)<1e-11
            rng.append({"case":name,"t":time,"J":J,"h":h,"B":B,"matter_mass":m,
                  "mean_dynamical_matter_count":float(p@matter),
                  "Wilson_loop_expectations":[float(np.vdot(psi,w@psi).real)for w in W],
                  "mean_electric_link_field":float(p@electric/ne)})
    weak=next(x for x in rng if x["case"]=="weak_creation" and x["t"]==1.5)
    strong=next(x for x in rng if x["case"]=="strong_creation" and x["t"]==1.5)
    assert strong["mean_dynamical_matter_count"]>weak["mean_dynamical_matter_count"]+1
    result={"status":"PASS","date":"2026-11-22",
      "W33_vertices":vertices,"two_four_cycles_as_local_vertex_indices":faces,
      "seven_edges_as_local_indices":edges,"two_Wilson_link_masks":masks,
      "kinematic_matter_link_hilbert_dim":8192,"Gauss_positive_sector_hilbert_dim":128,
      "Gauss_rule":"n_v=parity of adjacent electric X-negative bits; implies even total matter parity",
      "static_B0_h1_energy_by_pair_separation":costs,
      "static_potential":"Delta E=2h * minimum graph shortest-path length on this 2-square patch",
      "dynamical_pair_sweep":rng,
      "limits":"Genuine 128D constrained finite quantum-link model, but graph embedding/charge-pair terms imposed; no thermodynamic string tension, non-Abelian gauge field or physical QCD experiment."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS two W33 plaquettes, six Gauss laws, 128D physical link sector")
    return result
if __name__=="__main__":main()
