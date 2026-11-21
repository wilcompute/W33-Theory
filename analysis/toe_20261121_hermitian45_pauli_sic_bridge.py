"""Exact GF(4) Hermitian/Witting -> F3 two-qutrit frame bridge.

Source: Vlasov arXiv:2503.18431; Marcelis' PG(3,4)/Witting pages.
Reuses established 40-ray/40-line graph equivalence and 45 frame count.
This module explicitly tests the 45-point incidence correspondence and dual
SIC/PVM measurement decomposition without claiming physical qutrit encoding.
"""
from __future__ import annotations
from collections import Counter
from itertools import product, combinations
import json
from pathlib import Path
import networkx as nx
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/toe_20261121_hermitian45_witting_pauli_sic.json"
P4 = (1, 2, 3)
EXP = {1: 0, 2: 1, 3: 2}

def mul4(a, b):
    return 0 if a == 0 or b == 0 else P4[(EXP[a] + EXP[b]) % 3]

def norm4(v):
    a = next(x for x in v if x)
    return tuple(mul4(x, P4[(-EXP[a]) % 3]) for x in v)

def herm4(u, v):
    h = 0
    for a, b in zip(u, v):
        h ^= mul4(mul4(a, a), b)
    return h

def canonical3(u):
    a = next(x for x in u if x)
    return tuple((a * x) % 3 for x in u)

def symp3(u, v):
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % 3

def witting_rays():
    omega = np.exp(2j * np.pi / 3)
    c = []
    f = []
    for j in range(4):
        z = [0]*4
        z[j] = 1
        c.append(np.array(z, dtype=complex))
        f.append(tuple(z))
    for mu, nu in product(range(3), repeat=2):
        a, b = omega**mu, omega**nu
        x, y = P4[mu], P4[nu]
        for v, q in (
            ((0,1,-a,b), (0,1,x,y)),
            ((1,0,-a,-b), (1,0,x,y)),
            ((1,-a,0,b), (1,x,0,y)),
            ((1,a,b,0), (1,x,y,0)),
        ):
            c.append(np.array(v, dtype=complex)/np.sqrt(3))
            f.append(q)
    assert len(c)==len(f)==40
    return np.array(c), f

def analyze():
    rays, wf4 = witting_rays()
    all4 = sorted({norm4(q) for q in product(range(4),repeat=4) if any(q)})
    iso = [q for q in all4 if herm4(q,q)==0]
    aniso = [q for q in all4 if herm4(q,q)]
    assert (len(all4),len(iso),len(aniso))==(85,45,40)
    assert set(wf4)==set(aniso)
    overlap = abs(rays.conj() @ rays.T)**2
    Aw = (overlap < 1e-9).astype(int)
    np.fill_diagonal(Aw,0)
    Af4 = np.array([[int(i!=j and herm4(u,v)==0)
                     for j,v in enumerate(wf4)] for i,u in enumerate(wf4)])
    assert np.array_equal(Aw,Af4)
    assert set(Aw.sum(axis=1))=={12}
    X = sorted({canonical3(q) for q in product(range(3),repeat=4) if any(q)})
    xi={q:i for i,q in enumerate(X)}
    A3=np.array([[int(i!=j and symp3(u,v)==0)
                  for j,v in enumerate(X)] for i,u in enumerate(X)])
    mapping=next(nx.algorithms.isomorphism.GraphMatcher(
        nx.from_numpy_array(Aw),nx.from_numpy_array(A3)).isomorphisms_iter())
    assert len(mapping)==40
    lines=sorted({tuple(sorted({xi[canonical3(tuple((a*u[k]+b*v[k])%3
                      for k in range(4)))] for a,b in product(range(3),repeat=2)
                      if a or b})) for u,v in combinations(X,2) if symp3(u,v)==0})
    assert len(lines)==40 and all(len(t)==4 for t in lines), (len(lines),Counter(map(len,lines)))
    N=np.zeros((40,40),dtype=int)
    for k,L in enumerate(lines):
        N[list(L),k]=1
    assert np.array_equal(N@N.T,4*np.eye(40,dtype=int)+A3)
    diag=smith_normal_form(Matrix(N),domain=ZZ)
    snf=Counter(abs(int(diag[i,i])) for i in range(40))
    assert snf=={1:25,0:15}

    planes=set()
    for u,v in combinations(X,2):
        if symp3(u,v):
            pl=frozenset(xi[canonical3(tuple((a*u[k]+b*v[k])%3
                    for k in range(4)))] for a,b in product(range(3),repeat=2)
                    if a or b)
            assert len(pl)==4
            planes.add(pl)
    assert len(planes)==90
    frames=set()
    for pl in planes:
        perp=frozenset(i for i,w in enumerate(X)
                       if all(symp3(w,X[k])==0 for k in pl))
        assert len(perp)==4 and not (pl & perp)
        frames.add(frozenset(pl|perp))
    assert len(frames)==45

    polar_sets=[]
    K=np.zeros((45,40),dtype=int)
    max_povm_error=max_sic_error=0.0
    side_rank=Counter()
    for j,o in enumerate(iso):
        ids=[i for i,u in enumerate(wf4) if herm4(o,u)==0]
        assert len(ids)==8
        induced=nx.from_numpy_array(Aw[np.ix_(ids,ids)])
        assert nx.is_bipartite(induced)
        l,r=nx.bipartite.sets(induced)
        assert len(l)==len(r)==4
        assert induced.number_of_edges()==16
        assert set(dict(induced.degree()).values())=={4}
        for part in (l,r):
            members=rays[[ids[k] for k in sorted(part)]]
            side_rank[int(np.linalg.matrix_rank(members,tol=1e-9))]+=1
            assert side_rank[2]>=1
            for i,k in combinations(range(4),2):
                max_sic_error=max(max_sic_error,
                         abs(abs(np.vdot(members[i],members[k]))**2-1/3))
        P=sum(np.outer(rays[i],rays[i].conj()) for i in ids)
        max_povm_error=max(max_povm_error,float(np.max(abs(P-2*np.eye(4)))))
        mapped=frozenset(mapping[i] for i in ids)
        polar_sets.append(mapped)
        K[j,list(mapped)]=1
    assert set(polar_sets)==frames and len(set(polar_sets))==45
    assert side_rank=={2:90}
    assert max_povm_error<1e-11 and max_sic_error<1e-11
    assert np.all(K.sum(axis=0)==9)
    assert np.all(K.sum(axis=1)==8)
    assert np.array_equal(K.T@K,8*np.eye(40,dtype=int)+2*A3+
                          np.ones((40,40),dtype=int))
    polar_pairs=Counter(len(polar_sets[i]&polar_sets[j])
                   for i,j in combinations(range(45),2))
    assert polar_pairs=={2:720,0:270}
    frame_spectrum=Counter(np.rint(np.linalg.eigvalsh(K.T@K)).astype(int))
    assert frame_spectrum=={72:1,12:24,0:15}
    projector_gram=(overlap+overlap.T)/2
    spectral_gram=(2*np.eye(40)+np.ones((40,40))-Aw)/3
    assert np.max(abs(projector_gram-spectral_gram))<1e-11
    gram_spectrum=Counter(np.rint(np.linalg.eigvalsh(projector_gram)).astype(int))
    assert gram_spectrum=={10:1,2:15,0:24}
    # For a fixed sample density matrix, the two measurement schedules
    # induce the same 40-outcome marginal E_i=P_i/10.
    rho=np.outer(rays[17],rays[17].conj())
    p=np.array([np.vdot(r,rho@r).real for r in rays])
    basis_marginal=np.array([np.sum(N[mapping[i],:])/40*p[i] for i in range(40)])
    chart_marginal=np.array([np.sum(K[:,mapping[i]])/90*p[i] for i in range(40)])
    assert np.max(abs(basis_marginal-chart_marginal))<1e-12
    assert abs(sum(basis_marginal)-1)<1e-12
    # Every individual 45-chart setting has total probability one.
    assert max(abs(sum(p[i]/2 for i,u in enumerate(wf4)
               if herm4(o,u)==0)-1) for o in iso)<1e-11
    return {
      "status":"PASS",
      "PG34_points":85,"Hermitian_isotropic_points":45,
      "Hermitian_anisotropic_Witting_points":40,
      "GF4_complex_orthogonality_exact_match":True,
      "two_qutrit_W33_points":40,"Pauli_commuting_lines":40,
      "two_qutrit_nondegenerate_planes":90,"Pauli_tensor_charts":45,
      "isotropic_polar_supports_identical_to_all_45_Pauli_charts":True,
      "Hermitian_chart_points":8,"Witting_ray_charts_per_point":9,
      "each_induced_chart_graph":"K4,4",
      "each_chart_two_orthogonal_qubit_tetrahedral_SICs":True,
      "qubit_SIC_subspace_rank_counter":dict(side_rank),
      "max_SIC_overlap_residual":max_sic_error,
      "max_8ray_sum_minus_2I_residual":max_povm_error,
      "chart_pair_intersections":dict(polar_pairs),
      "chart_incidence_Gram":"K^T K = 8I + 2A + J",
      "chart_incidence_spectrum":{int(k):int(v) for k,v in frame_spectrum.items()},
      "Witting_projector_Gram_spectrum":{int(k):int(v) for k,v in gram_spectrum.items()},
      "W33_point_line_incidence_smith_normal_form":dict(snf),
      "dual_POVM_marginals":"40 uniform 4-outcome orthogonal bases = 45 uniform 8-outcome double-SIC charts = {P_i/10}_i",
      "max_dual_POVM_marginal_residual":float(np.max(abs(basis_marginal-chart_marginal))),
      "ray_index_to_F3_projective_point_index":{str(k):int(v) for k,v in mapping.items()},
      "isotropic_GF4_point_to_Pauli_chart_support":[
          {"isotropic_point":list(o),"Pauli_indices":sorted(polar_sets[j])}
          for j,o in enumerate(iso)],
      "scope":"Finite projective/quantum POVM identity, not an isometric 4D-to-9D ququart/qutrit quantum encoding or proven QKD secrecy."
    }

def main():
    result=analyze()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 85=45+40 GF4; 45 exact Pauli charts; 90 qubit SIC blocks; dual POVM", flush=True)
    print("CERTIFICATE",OUT)
    return result

if __name__=="__main__":
    main()
