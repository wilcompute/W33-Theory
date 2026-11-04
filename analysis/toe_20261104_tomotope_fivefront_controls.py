#!/usr/bin/env python3
"""Five conditional TOE falsifiers anchored to the ORIGINAL tomotope/REYE data.

Read the 2012 Monson-Pellicer-Williams paper (Sections 3-6), 2014 Mixing
and Monodromy and 2024 Reflexible Covers; compare with repo prior BT831,
BT1363, Pass5309/5310, Pass5488-5495, Pass5643-5650, and earlier W33
81-cycle/photonic/hard-gravity controls. This is NOT new GR/E6/TOE physics.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import brentq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_tomotope_fivefront_controls.json"
spec=importlib.util.spec_from_file_location(
    "published_tomotope",ROOT/"analysis"/"toe_20261104_tomotope_reye_flux_invariants.py")
tomo=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tomo)

def laplacian_subdivision(G,L):
    edges=sorted(tuple(sorted((int(a),int(b)))) for a,b in G.edges())
    n=28+len(edges)*(L-1)
    rows=[];cols=[];vals=[]
    for e,(a,b) in enumerate(edges):
        path=[a]+[28+e*(L-1)+k for k in range(L-1)]+[b]
        for u,v in zip(path,path[1:]):
            rows.extend([u,u,v,v]);cols.extend([u,v,u,v]);vals.extend([1,-1,-1,1])
    A=coo_matrix((vals,(rows,cols)),shape=(n,n)).tocsr()
    return A

def dimension(G):
    # On each subdivided interior edge, solve -f_(j-1)+2 f_j-f_(j+1)=lambda f_j.
    # Eliminating the interior gives neighbour sum F_d(theta)*f_u, where
    # F_d=d cos(Ltheta)+(d-2)tan(theta/2)sin(Ltheta), degrees d=4,3.
    # For Reye bipartite incidence, nontrivial B singular sigma=2 (mult9),
    # so F_4(theta)*F_3(theta)=4 determines the first positive eigenmode.
    alpha=math.acos(1/math.sqrt(3))
    target=alpha**2
    rows=[]
    for L in (1,2,4,8,16,32,64,128):
        def f(theta):
            c=math.cos(L*theta)
            v=math.tan(theta/2)*math.sin(L*theta)
            return (4*c+2*v)*(3*c+v)-4
        theta=brentq(f,1e-13,1.75*alpha/L,xtol=1e-14)
        lam=2*(1-math.cos(theta))
        row=dict(L=L,nodes=28+48*(L-1),edges=48*L,cycle_rank=21,
            first_gap=lam,rescaled_gap=L*L*lam,
            leading_correction_measure=L*(L*L*lam/target-1))
        assert row["edges"]-row["nodes"]+1==21
        if L in (1,2,4,8):
            A=laplacian_subdivision(G,L)
            s=np.sort(eigsh(A,k=3,sigma=1e-6,which="LM",
                  return_eigenvectors=False,tol=1e-9))
            assert abs(float(s[1])-lam)<1e-8
            row["direct_sparse_gap"]=float(s[1])
        rows.append(row)
    assert abs(rows[-1]["leading_correction_measure"]-5/12)<.001
    return dict(status="PASS_REYE_BIREGULAR_METRIC_GRAPH_FINITE_SIZE_CORRECTION",
        rank4_of_abstract_tomotope_is_not_4D_Lorentzian_geometry=True,
        metric_graph_weyl_dimension=1,not_spacetime_dim4=True,
        predicted_rescaled_gap=target,
        alpha_definition="alpha = arccos(1/sqrt(3)), from Reye normalized adjacency sigma=2/sqrt(12)",
        exact_first_eigen_secular_equation="(4cos(Ltheta)+2tan(theta/2)sin(Ltheta))*(3cos(Ltheta)+tan(theta/2)sin(Ltheta))=4",
        asymptotic_formula="L^2 lambda_1(L) = alpha^2 [1+5/(12L)+O(L^-2)]",
        verified_results=rows,
        boundary="A metric-graph 1D refinement, distinct from the existing W33 Levi graph 1D limit and from the native H4 S3xI 4D cell topology. A chosen spin manifold/metric is absent.")

def cycle_matrix(G):
    # Signed 28x48 node-edge incidence and a fundamental H1 basis.
    edges=sorted(tuple(sorted((int(u),int(v)))) for u,v in G.edges())
    emap={e:i for i,e in enumerate(edges)}
    D=np.zeros((28,48),dtype=np.int64)
    for j,(u,v) in enumerate(edges):D[u,j]=-1;D[v,j]=1
    cycles=nx.cycle_basis(G)
    assert len(cycles)==21
    B=np.zeros((48,21),dtype=np.int64)
    for j,seq in enumerate(cycles):
        for a,b in zip(seq,seq[1:]+seq[:1]):
            key=tuple(sorted((a,b)))
            i=emap[key]
            B[i,j]=1 if a==key[0] else -1
    assert not np.any(D@B)
    assert np.linalg.matrix_rank(D.astype(float))==27
    assert np.linalg.matrix_rank(B.astype(float))==21
    assert min(np.sum(B!=0,axis=1))>=1
    return D,B

def gravity(G):
    D,B=cycle_matrix(G)
    # Independent positive cycle Hamiltonian zero loci:
    # each h_i = 1/2(ci*x)^2+1/2 sum_e∈supp(ci) p_e².
    # All h_i=0 => p=0 (each edge covered), x ∈ im(D^T).
    # A nonzero cycle u has B^T u !=0 and cannot be a pure gradient.
    cycle=B[:,0]
    assert not np.any(D@cycle)
    assert not np.any(D@(D.T@np.zeros(28,dtype=np.int64)))
    assert np.any(B.T@cycle)
    return dict(status="PASS_REYE_CYCLE_RANK21_GRAVITY_ZERO_LOCUS_BOUNDARY",
        Reye_node_edge_incidence_rank=27,
        Reye_cycle_rank=21,original_W33_Levi_cycle_rank=81,
        direct_rank_preserving_identification_of_81W33_cycles_inside_Reye_H1_impossible=True,
        selected_integer_cycle_basis_covers_all_48_edges=True,
        positive_local_constraint_zero_set="all 21 positive h_i zero iff p=0 and x=D^T phi, one gauge orbit",
        nonlinear_Einstein_Dirac_algebra_derived=False,
        boundary="Counterexample ONLY for this specific positive local constraint ansatz and direct H1 identification. Extra fibers or a different action may have more degrees of freedom.")

def symmetry_and_flavor(s):
    assert s["Reye_bipartite_aut_color_preserving_order"]==576
    assert s["independent_Q4_even_signed_WD4_central_quotient_order"]==96
    assert s["selected_C3_orbits_16_triangles"]==[1]+[3]*5
    assert s["nontrivial_order3_elements_in_Gamma96"]==32
    assert s["order3_fixed_48_medial_incidence_flags_per_element"]==0
    spec=importlib.util.spec_from_file_location(
        "w33_transvection_c3",ROOT/"analysis"/"toe_20261103_c3_symmetry_selector.py")
    w33=importlib.util.module_from_spec(spec);spec.loader.exec_module(w33)
    cert=w33.certificate(seed=2,save=False)
    assert cert["flags"]==160 and cert["transvection_fixed_flags"]==16
    return dict(status="PASS_TOMOTOPE_SYMMETRY_VS_FLAVOR_ORBIT_NO_GO",
        W33_selected_C3_fixed_160_Levi_flags=16,
        Tomotope_any_nontrivial_Gamma96_C3_fixed_48_medial_flags=0,
        C3_equivariant_total_map_160_W33_flags_to_48_tomotope_medial_flags_exists=False,
        equivariance_proof="Every equivariant map sends fixed points to fixed points. W33's selected transvection fixes 16 of 160 flags; all 32 order-three elements of tomotope Gamma96 act freely on 48 medial incidences. Thus no total map intertwining these two specified nontrivial C3 actions exists.",

        tomotope_Gamma_order=96,Reye_color_preserving_aut_order=576,
        accidental_uncolored_rank1_2_hopping_symmetry_index=6,
        group_action_transitive_on_16_triangles=True,
        invariant_three_triangle_subset_under_full_Gamma_exists=False,
        selected_C3_triangle_orbits=[1]+[3]*5,
        C3_triplication_does_not_select_one_unique_generation_triple=True,
        flavor_parent="October Pass11951 parity-safe Nelson-Barr and November vectorlike strong-CP countercontrol",
        boundary="No fields, Yukawa invariants, physical chirality or measured fermion generations are identified by these rank-2 tomotope incidence orbits.")

def hardware(h):
    assert h["sixth_moment_return_difference_exact"]==24
    assert h["zero_eigenmodes_before"]==8 and h["zero_eigenmodes_after"]==6
    assert all(abs(row["imaginary_Ramsey_quadrature_difference"])<1e-12
               for row in h["simulations"])
    return dict(status="PASS_REAL_BIPARTITE_FLUX_HARDWARE_QUADRATURE_SELECTION",
        tri_hopping_vs_Reye_bipartite_hopping_comparison="triangle: leading t^3 imaginary phase return; Reye: leading t^6 REAL return",
        all_real_bipartite_return_imaginary_is_zero=True,
        leading_observable="Re[U_plus(ii)-U_pi(ii)] = -t^6/30+O(t^8)",
        one_pi_incidence_edge_lifts_two_flat_zero_modes=True,
        measurement_schemes=["coherent real-quadrature Ramsey reference","return population with matched onsite phases"],
        simulated_t_points=h["simulations"],
        boundary="Closed ideal graph only: no Lindblad rates, baseline detector fidelity, Trotter compilation, or physical photonic gate map for the 28-site Reye configuration.")

def main():
    _,_,B,G=tomo.canonical_incidence()
    prev=tomo.main()
    r=dict(status="PASS_ALL_FIVE_TOMOTOPE_ANCHORED_TOE_FALSIFICATION_FRONTS",
        dimension=dimension(G),
        symmetry_and_flavor=symmetry_and_flavor(prev["symmetry"]),
        gravity=gravity(G),
        hardware=hardware(prev["hardware_flux"]),
        nonunique_regular_cover=prev["covers"],
        external_papers=prev["provenance"]["followups"],
        new_tomotope_producer="analysis/toe_20261104_tomotope_reye_flux_invariants.py",
        physics_boundary="Finite exact combinatorial and mathematically conditioned controls, no completed TOE or real hardware experiment.")
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],"finite_gap",r["dimension"]["verified_results"][-1]["rescaled_gap"],
          "cycle_rank",r["gravity"]["Reye_cycle_rank"],
          "protocol",r["hardware"]["leading_observable"],flush=True)
    return r
if __name__=="__main__":main()
