#!/usr/bin/env python3
"""Operational graph metric from short-time quantum transport:
distance(i,j)=minimum order k with <j|H^k|i> nonzero for H=A.
Compares two 8-site degree-3 graphs, isolates a hidden scale J*t,
and shows dynamical locality requires supplied interactions.
"""
from __future__ import annotations
import math,json
from pathlib import Path
import networkx as nx,numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_operational_metric_from_dynamics.json'
def rows_for(G,name):
    nodes=sorted(G.nodes());n=len(nodes)
    A=nx.to_numpy_array(G,nodelist=nodes,dtype=int)
    assert np.array_equal(A,A.T)
    assert np.all(np.diag(A)==0)
    powers=[np.eye(n,dtype=np.int64)]
    for k in range(1,n):powers.append(powers[-1]@A)
    D=np.array([[nx.shortest_path_length(G,u,v) for v in nodes] for u in nodes])
    earliest=np.zeros((n,n),int);coeff=np.zeros((n,n),float)
    for i in range(n):
        for j in range(n):
            k=next(t for t in range(n) if powers[t][j,i]!=0)
            earliest[j,i]=k
            coeff[j,i]=int(powers[k][j,i])/math.factorial(k)
            assert k==D[j,i]
            assert powers[k][j,i]>0
    t=.05
    U=expm(-1j*t*A)
    max_relative_err=0.
    for i in range(n):
        for j in range(n):
            if i==j:continue
            lead=(-1j*t)**D[j,i]*coeff[j,i]
            err=abs(U[j,i]-lead)/max(abs(lead),1e-50)
            max_relative_err=max(max_relative_err,err)
    assert max_relative_err<.07,(name,max_relative_err)
    # Reparametrization J->lambda J, physical interaction duration
    # t->t/lambda leaves all predictions unchanged identically.
    for lam in (.4,1.,2.3):
        assert np.max(abs(expm(-1j*(lam*A)*(t/lam))-U))<1e-12
    paircounts={str(k):int(sum(D[i,j]==k for i in range(n) for j in range(i+1,n)))
                for k in sorted(set(D.flatten())) if k>0}
    return {"graph":name,"nodes":n,"edges":G.number_of_edges(),
            "degree_sequence":sorted(dict(G.degree()).values()),
            "pair_distance_census":paircounts,"diameter":int(D.max()),
            "exact_Taylor_order_recovers_all_pair_distances":True,
            "max_small_time_leading_coefficient_relative_error_at_t_005":max_relative_err,
            "unidentifiable_absolute_J_and_t_separately":True}
def run():
    cube=nx.hypercube_graph(3)
    cube=nx.convert_node_labels_to_integers(cube)
    mob=nx.cycle_graph(8)
    mob.add_edges_from((i,i+4) for i in range(4))
    assert sorted(dict(mob.degree()).values())==sorted(dict(cube.degree()).values())==[3]*8
    assert not nx.is_isomorphic(cube,mob)
    rows=[rows_for(cube,"hypercube_Q3"),rows_for(mob,"Mobius_ladder_M8")]
    assert rows[0]["pair_distance_census"]!=rows[1]["pair_distance_census"]
    out={"status":"PASS_LOCAL_HAMILTONIAN_OPERATIONAL_DISTANCE_AND_TIME_SCALE",
       "identity":"For a finite simple connected graph G with A adjacency and H=J A, the transition amplitude U_ji(t)=sum_k (-iJt)^k (A^k)_ji/k!. By walk counting, (A^k)_ji=0 for k<distance(i,j) and (A^distance)_ji>0, hence the first nonzero Taylor order is precisely graph shortest path distance.",
       "same_degree_nonisomorphic_graphs":rows,
       "unitarity":"U(t)=exp(-i Jt A) unitary for real J; a finite-speed suppression in powers of t follows from microscopic adjacency, but no Lorentz symmetry or relativistic Lieb-Robinson theorem is proved.",
       "physical_scale_firewall":"All one-excitation observables depend only on Jt. Without a separately calibrated interaction J or clock t, the dynamical transfer measurements do not determine absolute seconds or propagation speed.",
       "no_geometry_free_claim":"The dynamical interaction graph A is an INPUT. The experiment reconstructs its operational distance from quantum transition amplitudes; it does not derive the interaction graph or emergent 4D locality from an abstract algebra by itself.",
       "sources":["https://doi.org/10.1103/PhysRevLett.28.259"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("OPERATIONAL METRIC",[(r["graph"],r["pair_distance_census"],r["max_small_time_leading_coefficient_relative_error_at_t_005"]) for r in rows])
if __name__=="__main__":run()
