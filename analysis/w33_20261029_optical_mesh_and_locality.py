#!/usr/bin/env python3
"""Reproducible 40-mode one-photon W33 walk, optical mesh, loss, and locality.

Not a [[40,8,6]] physical CSS implementation. A single photon across
40 modes has Hilbert dimension 40, insufficient for eight logical qubits.
Models a passive spatial-mode quantum walk in the ordinary Born framework.
"""
from __future__ import annotations
from collections import deque
from pathlib import Path
import json
import math
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_incidence_even_line_resolution_20261029 import make_geometry
OUT=ROOT/"data/w33_20261029_optical_mesh_and_locality.json"

def adjacency():
    points,lines,line_masks,rows,incidence,norm,omega=make_geometry(3)
    matrix=np.array([[((rows[i]>>j)&1) for j in range(40)]
                     for i in range(40)],dtype=float)
    generators=[]
    index={x:i for i,x in enumerate(points)}
    ulist=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
           (1,0,1,0),(0,1,0,1),(1,0,0,1))
    for u in ulist:
        g=tuple(index[norm(tuple((x[k]+omega(x,u)*u[k])%3
                                   for k in range(4)))] for x in points)
        assert len(set(g))==40
        generators.append(g)
    return matrix,generators

def pair_orbits(generators):
    unvisited=set(range(1600))
    results={}
    while unvisited:
        first=min(unvisited)
        seen={first}
        queue=deque([first])
        while queue:
            a,b=divmod(queue.popleft(),40)
            for g in generators:
                z=40*g[a]+g[b]
                if z not in seen:
                    seen.add(z);queue.append(z)
        a,b=divmod(first,40)
        label="diagonal" if a==b else "adjacent" if ADJ[a,b] else "nonadjacent"
        results[label]=len(seen)
        unvisited.difference_update(seen)
    assert results=={"diagonal":40,"nonadjacent":1080,"adjacent":480}
    return results

def walk(A,t,nonlocal_shift=0):
    n=40
    I=np.eye(n);J=np.ones((n,n))
    P12=J/40
    P2=(2/3)*I+(1/6)*A-(1/15)*J
    Pminus=I-P12-P2
    assert np.max(abs(A@P2-2*P2))<1e-12
    return (np.exp(-1j*(12+nonlocal_shift)*t)*P12+
            np.exp(-2j*t)*P2+np.exp(4j*t)*Pminus)

def triangular_mesh(U):
    # Givens eliminate below-diagonal entries; all gates act on ADJACENT
    # mode pairs. Each 2x2 unitary has a beam-splitter + phase realization.
    R=U.copy()
    n=R.shape[0]
    gates=[]
    for column in range(n-1):
        for lower in range(n-1,column,-1):
            a,b=R[lower-1,column],R[lower,column]
            length=np.hypot(abs(a),abs(b))
            if length<1e-13:
                continue
            G=np.array([[a.conjugate(),b.conjugate()],[-b,a]],
                       dtype=complex)/length
            R[lower-1:lower+1,:]=G@R[lower-1:lower+1,:]
            gates.append((lower-1,G.conj().T))
    assert np.max(abs(R-np.diag(np.diag(R))))<1e-12
    phases=np.diag(R).copy()
    assert np.max(abs(abs(phases)-1))<1e-12
    result=np.diag(phases)
    for row,Gdag in reversed(gates):
        result[row:row+2,:]=Gdag@result[row:row+2,:]
    err=float(np.max(abs(result-U)))
    assert err<5e-12
    return gates,phases,err

def lossy_map(gates,phases,per_active_element_eta):
    # Each component attenuates BOTH participating modes; no loss is
    # assigned to modes untouched by that component.
    T=np.diag(phases.astype(complex))
    for i,G in reversed(gates):
        T[i:i+2,:]=(per_active_element_eta**0.5)*G@T[i:i+2,:]
    return T

def main():
    global ADJ
    ADJ,generators=adjacency()
    I=np.eye(40);J=np.ones((40,40))
    assert np.max(abs(ADJ@ADJ-(8*I-2*ADJ+4*J)))==0
    orbits=pair_orbits(generators)
    U=walk(ADJ,math.pi/2)
    assert np.max(abs(U@U.conj().T-I))<1e-12
    distribution=abs(U[:,0])**2
    counts={"self":1,"neighbors":int(sum(ADJ[0])),
            "nonneighbors":int(39-sum(ADJ[0]))}
    assert counts=={"self":1,"neighbors":12,"nonneighbors":27}
    assert abs(distribution[0]-1/25)<1e-12
    assert all(abs(distribution[j]-(1/25 if ADJ[0,j] else 4/225))<1e-12
               for j in range(1,40))
    gates,phases,error=triangular_mesh(U)
    assert len(gates)<=780
    K=lossy_map(gates,phases,0.999)
    eigenvalues=np.linalg.eigvalsh(K.conj().T@K)
    survival=float(np.sum(abs(K[:,0])**2))
    assert -1e-10<=eigenvalues.min()<=eigenvalues.max()<=1+1e-10
    U1=walk(ADJ,math.pi)
    U2=walk(ADJ,math.pi,nonlocal_shift=1)
    assert np.max(abs(U1-I))<1e-12
    P=abs(U2[:,0])**2
    assert abs(P[0]-361/400)<1e-12
    assert all(abs(p-1/400)<1e-12 for p in P[1:])
    result={
     "checks":"PASS","point_pair_orbits":orbits,
     "G_invariant_commutant_dimension":3,
     "invariant_H":"a I + b A + c(J-I-A)",
     "strict_nearest_neighbor_H":"a I + b A (up to energy shift and scale)",
     "one_photon_modes":40,"full_eight_qubit_css_not_implemented":True,
     "quarter_cycle_probabilities":{"self":"1/25","each_neighbor":"1/25",
                                     "each_nonneighbor":"4/225"},
     "beam_splitter_SU2_elements":len(gates),"max_40_mode_elements":780,
     "phase_shifters":40,"reconstruction_max_abs_error":error,
     "illustrative_per_element_transmission":0.999,
     "illustrative_input_zero_survival":survival,
     "survival_eigenvalues":[float(eigenvalues.min()),float(eigenvalues.max())],
     "nonlocal_countermodel_pi_probability":{"self":"361/400",
                                             "each_offsite":"1/400"},
     "falsification_boundary":"Site-only quantum-walk intensities depend on SRG parameters, not uniquely W33. To distinguish geometry, use labeled multichannel coherent phase-sensitive tomography.",
     "no_new_physics_claim":"This is ordinary finite-dimensional quantum optics; an observed deviation requires a separately specified nonstandard law."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS:",len(gates),"Givens elements; onsite",survival,
          "orbit classes",orbits)
if __name__=="__main__":
    main()
