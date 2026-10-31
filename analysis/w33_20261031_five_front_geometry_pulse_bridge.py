#!/usr/bin/env python3
"""Five finite W33 fronts: exact tritter pulse, q9 icosa orbit, chirality, clock and continuum firewall.

Original cross-checks use frozen prior witnesses; this does not claim a theory of everything.
"""
from __future__ import annotations
from collections import Counter
import argparse, itertools, json, math, sys
from pathlib import Path
import networkx as nx
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
from analysis.w33_pass11062_single_foliation_finite54_transducer import factorize
from analysis.w33_20261031_plaquette_strict_duality_gap import geometry as w33_geometry
from symmetric_fast import fast_build

OUT=ROOT/"data/w33_20261031_five_front_geometry_pulse_bridge.json"

def q9_icosa():
    q=9
    frozen=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())
    points,lines=fast_build(q)
    assert len(points)==len(lines)==820
    chosen=frozen["results"][0]["chosen"]
    assert len(chosen)==48 and len(set(chosen))==48
    S=[set(lines[j]) for j in chosen]
    cov=Counter(p for L in S for p in L)
    assert set(cov.values())=={2} and len(cov)==240
    G=nx.Graph();G.add_nodes_from(range(48))
    G.add_edges_from((i,j) for i in range(48) for j in range(i+1,48) if S[i]&S[j])
    assert G.number_of_edges()==240 and all(d==10 for _,d in G.degree())
    assert nx.is_connected(G) and nx.is_bipartite(G)
    color=nx.bipartite.color(G)
    assert Counter(color.values())=={0:24,1:24}
    assert sum(nx.triangles(G).values())==0
    A=nx.to_numpy_array(G,dtype=np.int64)
    tr4=int(np.trace(A@A@A@A))
    c4=(tr4-48*10*19)//8
    assert c4==1680
    eigen=np.linalg.eigvalsh(A.astype(float))
    expected=[-10]+[-math.sqrt(10)]*12+[-2]*5+[0]*12+[2]*5+[math.sqrt(10)]*12+[10]
    assert max(abs(x-y) for x,y in zip(eigen,expected))<1e-8
    left=sorted(i for i,c in color.items() if c==0)
    right=sorted(i for i,c in color.items() if c==1)
    B=np.array([[int(G.has_edge(i,j)) for j in right] for i in left],dtype=np.int64)
    assert B.shape==(24,24)
    def rank_mod(M,p):
        m=np.asarray(M,dtype=np.int64).copy()%p; rank=0
        for col in range(m.shape[1]):
            piv=next((r for r in range(rank,m.shape[0]) if m[r,col]),None)
            if piv is None:continue
            m[[rank,piv]]=m[[piv,rank]]
            m[rank]=(m[rank]*pow(int(m[rank,col]),-1,p))%p
            for r in range(m.shape[0]):
                if r!=rank and m[r,col]:m[r]=(m[r]-m[r,col]*m[rank])%p
            rank+=1
        return rank
    field_ranks={str(p):rank_mod(B,p) for p in (2,3,5,7,11)}
    assert field_ranks=={"2":18,"3":18,"5":11,"7":18,"11":18}
    sq_per_edge=Counter(sum(1 for x in G.neighbors(u) if x!=v
                          for y in G.neighbors(v) if y!=u if G.has_edge(x,y))
                          for u,v in G.edges())
    assert sq_per_edge=={28:240}
    C=B@B.T;I24=np.eye(24,dtype=np.int64)
    assert np.array_equal(C@(C-4*I24)@(C-10*I24)@(C-100*I24),np.zeros((24,24),dtype=np.int64))
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    smith=smith_normal_form(Matrix(B.tolist()),domain=ZZ)
    invariants=[abs(int(smith[j,j])) for j in range(24)]
    assert invariants==[1]*11+[5]*7+[0]*6
    return {"q":9,"line_set":48,"covered_points_twice":240,
        "intersection_graph":{"n":48,"edges":240,"degree":10,"bipartition":[24,24],
        "connected":True,"triangles":0,"four_cycles":1680,
        "square_cycles_per_edge":28,
        "spectrum":{"-10":1,"-sqrt(10)":12,"-2":5,"0":12,"2":5,"sqrt(10)":12,"10":1}},
        "24x24_biadjacency":{"rank_over_fields":field_ranks,
           "smith_normal_form":{"one":11,"five":7,"zero":6},
           "integral_cokernel":"Z^6 direct_sum (Z/5Z)^7",
           "BBt_minimal_annihilator":"C(C-4I)(C-10I)(C-100I)=0",
           "BBt_spectrum":{"100":1,"10":12,"4":5,"0":6}},
        "source":"Pass 12501 orbit witness, analysis/search_drivers_12466/icosa_even_q9.json",
        "novelty_boundary":"Source already identifies A5 orbit and graph spectrum; this checks incidence, field ranks and exact 4-cycles."}

def exact_pulse():
    orientations={}
    for which,ix in (("plus",7),("minus",6)):
        coords,pairs,factors=factorize(which)
        F=factors[ix].astype(np.int64)
        assert np.array_equal(F.T,-F)
        assert np.array_equal(F@F@F,-14*F)
        n=81; I=np.eye(n,dtype=np.int64)
        # All of these are exact integral checks; no floating expm is needed.
        D=F@F
        W=7*I+D
        assert np.array_equal(W@W,49*I) # (I+F^2/7)^2=I
        assert np.array_equal(D@D,-14*D) # P=-F^2/14 projector
        assert np.linalg.matrix_rank(F)==54
        assert np.linalg.matrix_rank(D)==54
        assert np.linalg.matrix_rank(W-7*I)==54
        seen=set(); histogram=Counter()
        for i in range(81):
            if i in seen: continue
            neigh={j for j in range(81) if F[i,j]!=0}
            C=sorted({i}|neigh)
            assert len(C)==3
            seen.update(C)
            weights=tuple(sorted(abs(int(F[a,b])) for a in C for b in C if a<b))
            histogram[weights]+=1
        assert len(seen)==81 and histogram=={(1,2,3):27}
        cert=json.loads((ROOT/"data/w33_pass11062_single_foliation_finite54_transducer.json").read_text())
        assert ix in [p["factor"] for p in cert["perfect_single_factors"][which]]
        orientations[which]={"factor":ix,"edge_weight_histogram":{"1,2,3":27},
          "triangle_count":27,"raw_rank":54,"quotient_rank_previous_certificate":54,
          "all_triangles_F_cubed_equals_minus14F":True,
          "exact_81x81_involution_certified":True,"integer_involution_identity":"(7I+F^2)^2=49I"}
    return {"orientations":orientations,
      "common_pulse":"P=-F^2/14, H_real=pi*P, exp(-i*H_real)=I+F^2/7",
      "eigenvalues_H_real":"0 on 27 dims; pi on 54 dims",
      "directed_pulse":"exp(+-pi*F/(2sqrt(14)))=I+F^2/14+-F/sqrt(14)",
      "orientation_loss":"Real-symmetric involution depends on F^2 and cannot see F -> -F",
      "orientation_resource":"Directed pulse depends on F; H=iF has imaginary gauge-invariant triangle hopping product",
      "implementation_status":"Exact ideal 81-mode Hamiltonian with 27 parallel three-mode blocks; no actual device, calibration, error threshold or chirality selection."}

def clock_ensemble():
    critical=math.log(3)/math.log(4)
    finite={}
    for N in (8,16,32,64,128,256):
        ln_mult=math.lgamma(N+1)-4*math.lgamma(N//4+1)
        finite[str(N)]=N*math.log(3)/ln_mult
    assert finite["256"]<finite["8"] and finite["256"]>critical
    return {"prior_thermodynamic_threshold_N_over_M":critical,
        "finite_N_equal_four_label_critical_ratios":finite,
        "derivation":"single event yields log3 per quantum copy; four compatible ticks yield log4 per classical label asymptotically",
        "boundary":"Combinatorial finite-size entropy control; assumes prior annealed all-to-all rate ensemble, not a local clock action or physical real-form choice."}

def chiral_w33():
    pts,lines=w33_geometry()
    G=nx.Graph();G.add_nodes_from(range(len(pts)))
    for L in lines:
        G.add_edges_from(itertools.combinations(L,2))
    assert len(pts)==40 and G.number_of_edges()==240 and all(d==12 for _,d in G.degree())
    cut,partition=nx.stoer_wagner(G)
    assert cut==12
    return {"edge_graph":"W(3,3) 40-vertex collinearity graph",
       "min_edge_cut":cut,"cut_partition_sizes":[len(c) for c in partition],
       "projected_O_squared":"9/32","minimum_nontrivial_flip_excitation_energy_over_J":"27/4",
       "ground_sign_sectors":2,
       "firewall":"Source-free projected edge Ising model already in Oct23 Round9; cut cost is finite, K-conjugate signs remain unbiased at finite volume and an external field or infinite-volume limit is needed for selection."}

def scalar_continuum():
    rows={}
    for q in (2,3,5,7,11,19):
        v=(q+1)*(q*q+1); k=q*(q+1)
        f=((q+1)*(v-1)-k)//(2*q);g=v-1-f
        assert k+(q-1)*f-(q+1)*g==0
        rows[str(q)]={"v":v,"degree":k,"eigenvalues":[k,q-1,-q-1],
                      "multiplicities":[1,f,g],
                      "normalized_positive_gap":1-(q-1)/k}
    return {"rank_three_commutant":"PSp(4,q)-invariant scalar point kernels are aI+bA+cJ",
        "all_q_obstruction":"At most 3 distinct eigenvalues at each q, for any q-dependent a,b,c. This rank-three invariant scalar sector cannot yield the unbounded ladder of distinct eigenvalues of a positive-dimensional compact-manifold Laplacian via eigenvalue convergence.",
        "numerical_families":rows,
        "previous_prior_art":"2026-10-29 symmetry/dynamics no chirality; 2026-10-23 round7 positive gap no-go; 2026-10-09 Levi heat no-go; 2026-10-23 round9 periodic Euclidean acoustic control.",
        "boundary":"This rejects the full-PSp-invariant one-body scalar sector, not matrix-valued modes, growing periodic covers, broken symmetries, interactions or continuum gravity in general."}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,default=OUT)
    a=ap.parse_args()
    result={"schema":"w33.20261031.five_front_geometry_pulse_bridge.v1",
       "status":"PASS","checks":{"q9_incidence_spectral_four_cycle":True,
       "two_exact_81_mode_reflection_pulses":True,
       "clock_entropy_finite_size":True,"w33_chiral_edge_cut":True,
       "rank_three_continuum_firewall":True},
       "geometry_A5_q9":q9_icosa(),"transducer_pulse":exact_pulse(),
       "clock_selection":clock_ensemble(),"source_free_chirality":chiral_w33(),
       "continuum":scalar_continuum(),
       "scientific_scope":"Exact finite mathematics and conditional toy Hamiltonians; not a physical TOE.",
       "upstream_head_at_start":"7949488538a96670bdd11740a77474cd51a5f758"}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"fronts":5,
      "q9_C4":result["geometry_A5_q9"]["intersection_graph"]["four_cycles"],
      "plus_factor":7,"minus_factor":6,
      "mincut":result["source_free_chirality"]["min_edge_cut"],
      "output":str(a.output)},sort_keys=True))
if __name__=="__main__":
    main()
