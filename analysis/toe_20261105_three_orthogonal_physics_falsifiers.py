#!/usr/bin/env python3
"""Three independent falsifiers outside the main five TOE programme fronts.

(1) Laplacian-isospectral, geometrically different connected 6-vertex graphs.
(2) Critical-vs-gapped Z3 clock chain, relevant to a 2026 SU3 plaquette paper.
(3) Finite Markov nonreversibility vs stationary distribution/entropy.
Established subjects; independently calculated repo-local comparisons.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import networkx as nx
import sympy as sp
from scipy.linalg import expm
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261105_three_orthogonal_physics_falsifiers.json"

def cospectral():
    e1=[(0,2),(1,2),(1,3),(1,4),(2,5),(3,5),(4,5)]
    e2=[(0,2),(0,5),(1,3),(1,4),(2,3),(3,4),(3,5)]
    graphs=[]; Ls=[]
    for edges in (e1,e2):
        g=nx.Graph();g.add_nodes_from(range(6));g.add_edges_from(edges)
        assert nx.is_connected(g)
        graphs.append(g)
        A=nx.to_numpy_array(g,dtype=int)
        L=np.diag(A.sum(axis=1))-A
        Ls.append(L)
    assert not nx.is_isomorphic(*graphs)
    x=sp.symbols("x")
    polys=[str(sp.factor(sp.Matrix(L).charpoly(x).as_expr())) for L in Ls]
    assert polys[0]==polys[1]
    assert polys[0]==str(x*(x-3)**2*(x-2)*(x*x-6*x+4))
    assert sorted(dict(graphs[0].degree()).values())!=sorted(dict(graphs[1].degree()).values())
    records=[]
    for t in (.3,1,2):
        heat=[expm(-t*L) for L in Ls]
        global_traces=[float(np.trace(v)) for v in heat]
        assert abs(global_traces[0]-global_traces[1])<1e-12
        local=[sorted(np.diag(v).tolist()) for v in heat]
        delta=float(np.linalg.norm(np.array(local[0])-np.array(local[1])))
        assert delta>1e-5
        records.append(dict(time=t,common_global_heat_trace=global_traces[0],
                            sorted_local_heat_diagonal_distance=delta,
                            sorted_local_heat_first=local[0],
                            sorted_local_heat_second=local[1]))
    return dict(status="PASS_EXACT_LAPLACIAN_COSPECTRAL_GRAPH_NONIDENTIFICATION",
       graph_vertices=6,edges_first=e1,edges_second=e2,
       first_degree_sequence=sorted(dict(graphs[0].degree()).values()),
       second_degree_sequence=sorted(dict(graphs[1].degree()).values()),
       exact_laplacian_characteristic_polynomial=polys[0],
       isomorphic=False,records=records,
       boundary="Identical Laplacian eigenvalues and heat traces do not fix local geometry, topology, metric, causal structure, or unique quantum substrate. Isospectral graphs are established mathematics.")

def potts_spectrum(n,g):
    count=3**n
    ids=np.arange(count)
    powers=3**np.arange(n)
    digits=((ids[:,None]//powers[None,:])%3)
    diag=-2*np.cos(2*np.pi*(digits-np.roll(digits,-1,axis=1))/3).sum(axis=1)
    rows=[ids];cols=[ids];data=[diag]
    for j,pow3 in enumerate(powers):
        old=digits[:,j]
        for sign in (1,-1):
            target=ids+(((old+sign)%3)-old)*pow3
            rows.append(ids);cols.append(target);data.append(np.full(count,-g))
    h=coo_matrix((np.concatenate(data),(np.concatenate(rows),np.concatenate(cols))),
                 shape=(count,count)).tocsr()
    assert abs((h-h.T).data).max(initial=0)<1e-12
    vals=np.sort(eigsh(h,k=3,which="SA",return_eigenvectors=False,
                       tol=1e-9,maxiter=100000))
    return vals
def z3_chain():
    records=[]
    for n in (3,4,5,6,7):
        gcrit=potts_spectrum(n,1)
        gapped=potts_spectrum(n,1.8)
        cgap=float(gcrit[1]-gcrit[0])
        dgap=float(gapped[1]-gapped[0])
        records.append(dict(sites=n,qudit_hilbert=3**n,
                            critical_coupling=1,critical_gap=cgap,
                            critical_n_times_gap=n*cgap,
                            disordered_coupling=1.8,disordered_gap=dgap,
                            disordered_n_times_gap=n*dgap))
    assert all(a["critical_gap"]>b["critical_gap"] for a,b in zip(records[:-1],records[1:]))
    assert abs(records[-1]["critical_n_times_gap"]-records[0]["critical_n_times_gap"])<.1
    assert abs(records[-1]["disordered_gap"]-records[2]["disordered_gap"])<.1
    return dict(status="PASS_Z3_PARAFERMION_CRITICAL_VS_MASSIVE_FINITE_SIZE_SCALING",
                model="Periodic 3-state quantum Potts chain H=-sum(Zi Z_i+1^dagger+h.c.)-g sum(Xi+Xi^dagger)",
                records=records,
                notable_prior_art="R. X. Siew, S. Chandrasekharan, T. Bhattacharya, Phys. Rev. D 114 L071504 (2026-10-29): SU3 qubit-regularized plaquette-chain continuum maps to Z3 clock/parafermion criticality.",
                nonidentification="A qutrit spectral clock or a 27-dimensional three-site Hilbert space is not automatically the Z3 parafermion field theory; one needs an explicit local Hamiltonian, critical tuning, and scaling observables.")

def entropy_production():
    n=4
    def chain(pf,pb):
        stay=1-pf-pb
        P=np.zeros((n,n))
        for i in range(n):
            P[i,(i+1)%n]=pf;P[i,(i-1)%n]=pb;P[i,i]=stay
        pi=np.ones(n)/n
        assert np.max(abs(pi@P-pi))<1e-14
        val=0
        for i in range(n):
            for j in range(n):
                if i!=j and P[i,j]>0:
                    val+=pi[i]*P[i,j]*math.log((pi[i]*P[i,j])/(pi[j]*P[j,i]))
        predicted=(pf-pb)*math.log(pf/pb)
        assert abs(val-predicted)<1e-12
        return dict(forward=pf,backward=pb,stay=stay,entropy_production=val,
                    stationary_probability=pi.tolist(),
                    stationary_shannon_entropy=math.log(n),
                    clockwise_net_current=(pf-pb)/n,
                    detailed_balance=abs(pf-pb)<1e-12)
    balanced=chain(.45,.45)
    asymmetric=chain(.7,.2)
    reverse=chain(.2,.7)
    assert balanced["entropy_production"]==0
    assert asymmetric["entropy_production"]>.6
    assert abs(asymmetric["entropy_production"]-reverse["entropy_production"])<1e-12
    assert asymmetric["clockwise_net_current"]==-reverse["clockwise_net_current"]
    return dict(status="PASS_STATIONARY_ENTROPY_NOT_DETERMINING_TIME_ARROW",
                equilibrium=balanced,clockwise=asymmetric,
                counterclockwise=reverse,
                boundary="Identical four-state geometry and uniform stationary Shannon entropy coexist with equilibrium and two opposite nonequilibrium currents. An exchange counter alone does not derive time reversal breaking; microscopic rates and constraints are required.")

def main():
    r={"isospectral_geometry":cospectral(),
       "z3_criticality":z3_chain(),
       "entropy_arrow":entropy_production()}
    out=dict(status="PASS_THREE_ORTHOGONAL_THEORY_CONTROLS",results=r)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for key,v in r.items():print("PASS",key,v["status"],flush=True)
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
