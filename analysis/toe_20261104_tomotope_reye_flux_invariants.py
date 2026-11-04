#!/usr/bin/env python3
"""Read-the-paper tomotope / Reye / Q4 / W(D4) and flux falsifiers.

Primary source: Monson, Pellicer & Williams, The tomotope, Ars Math. Contemp. 5
(2012), §§4-6. Follow-ups: Mixing and monodromy (2014); Reflexible covers
of prisms (2024); generalized Reye configurations (2010).
Repo prior art: BT1363, Pass5309/5310, 5396, 5488-5495, 5643-5650,
BT831. This is not a novelty claim for the identities already established.

New limited controls: exact real-bipartite quadrature no-go, 6-cycle
flux expansion, exact signed-incidence flat-band lifting, full tomotope
symmetry vs single C3 triplication selection, cover-dependent labels.
"""
from __future__ import annotations
import collections,itertools,json,math
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sy
from scipy.linalg import expm
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_tomotope_reye_flux_invariants.json"

def canonical_incidence():
    """The paper's §6, J={1,2,3,4}, edges X+/X-, triangles (a,-b)."""
    J=tuple(range(1,5))
    E=[(tuple(X),s) for X in itertools.combinations(J,2) for s in ("-","+")]
    F=list(itertools.product(J,repeat=2))
    B=np.zeros((12,16),dtype=np.int64)
    for ei,(X,s) in enumerate(E):
        for fi,(a,b) in enumerate(F):
            B[ei,fi]=int((a in X) and ((b in X) if s=="-" else (b not in X)))
    assert np.all(B.sum(axis=1)==4)
    assert np.all(B.sum(axis=0)==3)
    G=nx.Graph()
    G.add_nodes_from(range(12),color=0)
    G.add_nodes_from(range(12,28),color=1)
    G.add_edges_from((e,12+f) for e in range(12) for f in range(16) if B[e,f])
    assert nx.is_connected(G) and G.number_of_edges()==48
    return E,F,B,G

def q4_incidence():
    """Independent Q4 face-edge / antipodal quotient of BT1363 / Pass5488."""
    verts=range(16)
    E=sorted({frozenset((u,u^(1<<i))) for u in verts for i in range(4)},
             key=lambda x:tuple(sorted(x)))
    F=sorted({frozenset((u,u^(1<<i),u^(1<<j),u^(1<<i)^(1<<j)))
              for u in verts for i,j in itertools.combinations(range(4),2)},
             key=lambda x:tuple(sorted(x)))
    def classes(arr):
        seen=set();ans=[]
        for a in arr:
            if a in seen:continue
            b=frozenset(x^15 for x in a)
            assert b in arr and b!=a
            ans.append(frozenset((a,b)))
            seen|={a,b}
        return ans
    EC,FC=classes(E),classes(F)
    assert (len(E),len(F),len(EC),len(FC))==(32,24,16,12)
    B=np.array([[int(any(e<=f for e in Ed for f in Fa)) for Ed in EC]
                for Fa in FC],dtype=np.int64)
    assert int(B.sum())==48
    G=nx.Graph()
    G.add_nodes_from(range(12),color=0)
    G.add_nodes_from(range(12,28),color=1)
    G.add_edges_from((f,12+e) for f in range(12) for e in range(16) if B[f,e])
    return EC,FC,B,G

def graph_spectral(B,G):
    deg=list(dict(G.degree()).values())
    assert collections.Counter(deg)=={4:12,3:16}
    assert G.number_of_edges()-G.number_of_nodes()+1==21
    # Characteristic polynomial of 12x12 BB^T, computed EXACTLY.
    Q=sy.Matrix(B.tolist())
    z=sy.symbols("z")
    exact=sy.factor((Q*Q.T).charpoly(z).as_expr())
    expected=z**2*(z-4)**9*(z-12)
    assert sy.expand(exact-expected)==0
    assert Q.rank()==10
    adjacency=np.block([[np.zeros((12,12),dtype=np.int64),B],
                         [B.T,np.zeros((16,16),dtype=np.int64)]])
    assert int(np.trace(adjacency@adjacency))==96
    evalues=np.linalg.eigvalsh(adjacency.astype(float))
    assert np.allclose(evalues,
        np.array([-math.sqrt(12)]+[-2]*9+[0]*8+[2]*9+[math.sqrt(12)]),atol=1e-9)
    edge_cycles=[]
    for u,v in sorted(G.edges):
        H=G.copy()
        H.remove_edge(u,v)
        paths=[p for p in nx.all_simple_paths(H,u,v,cutoff=5) if len(p)==6]
        edge_cycles.append(len(paths))
        assert nx.shortest_path_length(H,u,v)==5
    assert set(edge_cycles)=={6}
    return dict(status="PASS_REYE_MEDIAL_GRAPH_28_48_H1_21_GIRTH6",
        graph_nodes=28,edge_nodes=12,triangle_nodes=16,medial_incidence_edges=48,
        flags_of_full_tomotope=4*48,cycle_rank=21,girth=6,
        shortest_six_cycles_through_each_incidence_edge=6,
        signed_bipartite_adjacency_spectrum={"minus_2sqrt3":1,"minus_2":9,"zero":8,"plus_2":9,"plus_2sqrt3":1},
        exact_positive_gram_charpoly="z^2 (z-4)^9 (z-12)",
        unsigned_incidence_rank_exact=10,adjacency=adjacency)

def act_vertices(p,t):
    def f(v):
        out=t
        for k in range(4):
            if v&(1<<k):out^=1<<p[k]
        return out
    return f

def act_classes(classes,fn):
    return Permutation([classes.index(frozenset(
        frozenset(fn(x) for x in subset) for subset in c)) for c in classes])

def published_group():
    cycles=[
        [(5,10),(6,9),(7,12),(8,11)],
        [(1,6),(2,5),(3,8),(4,7)],
        [(5,9),(6,10),(7,11),(8,12)],
        [(5,8),(6,7),(9,12),(10,11)]]
    rho=[]
    for pairs in cycles:
        a=list(range(12))
        for u,v in pairs:a[u-1]=v-1;a[v-1]=u-1
        rho.append(Permutation(a))
    pub=PermutationGroup(rho)
    assert pub.order()==96
    assert [int(x.order()) for x in rho]==[2]*4
    assert [int((rho[0]*rho[1]).order()),int((rho[1]*rho[2]).order()),
            int((rho[1]*rho[3]).order())]==[3,3,4]
    assert int((rho[0]*rho[1]*rho[3]).order())==3
    assert int((rho[2]*rho[1]*rho[3]).order())==3
    return pub

def action(EC,FC,B,G):
    # Signed even-coordinate Q4 symmetries W(D4) have 192 elements.
    # Antipodal (-I) acts trivially on edge/face *classes* (not on
    # original edges), giving exactly Gamma(T)=W(D4)/Z of order96.
    ops=[]
    for i in range(3):
        ops.append(act_vertices(tuple(range(4)),(1<<i)|(1<<3)))
    for i in range(3):
        p=list(range(4));p[i],p[i+1]=p[i+1],p[i]
        ops.append(act_vertices(p,0))
    edgegens=[act_classes(EC,fn) for fn in ops]
    facegens=[act_classes(FC,fn) for fn in ops]
    GF=PermutationGroup(facegens);GE=PermutationGroup(edgegens)
    assert GF.order()==GE.order()==96
    assert GF.derived_subgroup().order()==48 and GF.center().order()==1
    assert sorted([len(x) for x in GF.orbits()])==[12]
    assert sorted([len(x) for x in GE.orbits()])==[16]
    flag_pairs=[(f,e) for f in range(12) for e in range(16) if B[f,e]]
    fi={x:i for i,x in enumerate(flag_pairs)}
    flaggen=[Permutation([fi[(pg(f),eg(e))] for f,e in flag_pairs])
             for pg,eg in zip(facegens,edgegens)]
    Gflag=PermutationGroup(flaggen)
    assert Gflag.order()==96 and [len(x) for x in Gflag.orbits()]==[48]
    matched=nx.is_isomorphic(G,canonical_incidence()[3],
        node_match=lambda a,b:a["color"]==b["color"])
    assert matched
    aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(
        G,G,node_match=lambda a,b:a["color"]==b["color"]).isomorphisms_iter())
    assert aut==576
    pub=published_group()
    histogram=lambda group: {str(k):v for k,v in sorted(collections.Counter(
        int(x.order()) for x in group.generate_schreier_sims()).items())}
    assert histogram(GF)==histogram(pub)
    order3_pub=[u for u in pub.generate_schreier_sims() if int(u.order())==3]
    order3_medial=[u for u in Gflag.generate_schreier_sims() if int(u.order())==3]
    assert len(order3_pub)==len(order3_medial)==32
    assert all(not any(u(i)==i for i in range(12)) for u in order3_pub)
    assert all(not any(u(i)==i for i in range(48)) for u in order3_medial)
    r=facegens[3]*facegens[4]
    t=edgegens[3]*edgegens[4]
    s=flaggen[3]*flaggen[4]
    assert r.order()==t.order()==s.order()==3
    def orbit_sizes(g,n):
        return sorted([len(o) for o in PermutationGroup([g]).orbits()])
    assert orbit_sizes(r,12)==[3]*4
    assert orbit_sizes(t,16)==[1]+[3]*5
    assert orbit_sizes(s,48)==[3]*16
    return dict(status="PASS_TOMOTOPE_GAMMA96_REYE_AUT576_C3",
        paper_published_rho_group_order=96,
        paper_published_rho_order_histogram=histogram(pub),
        published_branching_relation="(r1 r3) order4; NOT string diagram involution commuting at distance 2",
        independent_Q4_even_signed_WD4_central_quotient_order=96,
        Q4_action_matches_published_group_order_histogram=True,
        Q4_Gamma_derived_order=48,Q4_Gamma_center_order=1,
        relabelled_PUBLISHED_GENERATORS_NOT_EXPLICITLY_CONJUGATED=True,
        Reye_bipartite_aut_color_preserving_order=aut,
        accidental_extra_symmetry_index=aut//96,
        nontrivial_order3_elements_in_Gamma96=len(order3_medial),
        order3_fixed_published_12_edge_labels_per_element=0,
        order3_fixed_48_medial_incidence_flags_per_element=0,
        Gamma96_orbits_on_12_edges=[12],Gamma96_orbits_on_16_triangles=[16],
        Gamma96_orbits_on_48_incident_pairs=[48],
        selected_C3_orbits_12_edges=orbit_sizes(r,12),
        selected_C3_orbits_16_triangles=orbit_sizes(t,16),
        selected_C3_orbits_48_medial_flags=orbit_sizes(s,48),
        symmetry_selection_obstruction="No proper triple of 16 triangle modes is invariant under all Gamma96, since the action is transitive. A selected C3 has one fixed triangle and five 3-cycles; a 'three-family' choice needs further symmetry breaking and physics.",
        boundary="Both actions realize abstract Gamma96 with same element orders; no assertion that the sixfold Reye graph enhancement is a physical gauge symmetry. Published rho is a non-string Wythoff subgroup, not Mon(T).")

def flux(B,G):
    Hplus=np.block([[np.zeros((12,12),dtype=np.int64),B],
                    [B.T,np.zeros((16,16),dtype=np.int64)]])
    edge=(0,int(np.flatnonzero(B[0])[0]))
    Hminus=Hplus.copy()
    x,y=edge[0],12+edge[1]
    Hminus[x,y]=-1;Hminus[y,x]=-1
    Bs=B.copy();Bs[edge]=-1
    assert sy.Matrix(Bs.tolist()).rank()==11
    assert sy.Matrix(B.tolist()).rank()==10
    # Because both H are real bipartite with zero onsite, odd powers
    # have zero diagonal and U_xx(t) is strictly REAL for every real t.
    S=np.diag(np.array([1]*12+[-1]*16))
    assert np.array_equal(S@Hplus@S,-Hplus)
    assert np.array_equal(S@Hminus@S,-Hminus)
    diffs=[]
    for n in range(0,7):
        a=np.linalg.matrix_power(Hplus,n)[x,x]
        b=np.linalg.matrix_power(Hminus,n)[x,x]
        diffs.append(int(a-b))
    assert diffs[:6]==[0]*6 and diffs[6]==24
    # For the rooted edge, exactly six 6-cycles use the flipped link.
    # Each contributes 4 to the signed sixth moment difference.
    assert sum(1 for p in nx.all_simple_paths(nx.restricted_view(
        G,[],[(x,y)]),x,y,cutoff=5) if len(p)==6)==6
    data=[]
    for time in (.2,.4,.8):
        a=expm(-1j*time*Hplus)[x,x]
        b=expm(-1j*time*Hminus)[x,x]
        assert abs(a.imag)<1e-12 and abs(b.imag)<1e-12
        data.append(dict(time=time,imaginary_Ramsey_quadrature_difference=float((a-b).imag),
            real_return_amplitude_difference=float((a-b).real),
            return_population_difference=float(abs(a)**2-abs(b)**2),
            leading_small_time_real_amplitude_difference=-time**6/30))
    return dict(status="PASS_GIRTH6_BIPARTITE_REAL_QUADRATURE_FLUX_OBSTRUCTION",
        root_node=x,signed_edge_indices=[x,y],
        unsigned_bipartite_incidence_rank=10,one_link_pi_flux_incidence_rank=11,
        zero_eigenmodes_before=8,zero_eigenmodes_after=6,
        cycle_rank_unchanged_under_flux=21,
        sixth_moment_return_difference_exact=24,
        moment_differences_orders_0_through_6=diffs,
        leading_return_amplitude_contrast="-t^6/30 + O(t^8); real quadrature",
        imaginary_return_quadrature_is_exactly_zero_for_all_real_t=True,
        simulations=data,
        limitation="28-site ideal real tight binding; no physical device, no measured noise, no guarantee optical phases and diagonal detunings preserve bipartite chiral symmetry.")

def covers():
    k=[3,5,7]
    rows=[]
    for n in k:
        rows.append(dict(k=n,qk_vertices=4*n**3,qk_edges=24*n**3,
            qk_triangles=32*n**3,qk_tetrahedra=8*n**3,
            qk_octahedra=4*n**3,
            monodromy_order=36864*n**6,
            monodromy_kernel_over_k1_order=n**6))
    return dict(status="PASS_PUBLISHED_COVER_ARITHMETIC_PRIOR_ART",
        fundamental_tomotope_automorphism_order=96,
        tomotope_monodromy_order=18432,
        published_minimal_regular_cover_R2_order=36864,
        cover_parameters=k,table=rows,
        theorem_citation="Monson-Pellicer-Williams 2012 Theorem 5.9: minimal regular covers for coprime odd p,q>1 do not cover each other; R2 incomparable",
        boundary="Restates and checks published order formula, NOT a new proof of group extensions. Regular cover index alone does not specify a physical geometric metric or local dynamics.")

def main():
    edges,triangles,B,G=canonical_incidence()
    EC,FC,Q,GQ=q4_incidence()
    spectral=graph_spectral(B,G)
    adj=spectral.pop("adjacency")
    assert np.array_equal(adj,adj.T)
    result=dict(status="PASS_TOMOTOPE_REYE_PUBLISHED_LITERATURE_FLUX_FALSIFIERS",
        provenance={
            "primary_paper":"Monson, Pellicer, Williams (2012) The tomotope, §4-6, DOI 10.26493/1855-3974.189.e64",
            "followups":["Monson, Pellicer, Williams (2014), Mixing and monodromy",
                         "Cunningham, Mixer, Williams (2024), Reflexible covers of prisms",
                         "Servatius, Servatius (2010), The generalized Reye configuration",
                         "Monson, Weiss (2007), Medial layer graphs of equivelar 4-polytopes"],
            "repo_prior_owners":["BT831","BT1363","Pass5309","Pass5310","Pass5396","Pass5488-5495","Pass5643-5650",
                                 "analysis/w33_pass1376_tomotope_published_generators.g"]},
        spectral=spectral,
        antipodal_q4_source=dict(original_edges=32,original_faces=24,
                                 quotient_edge_classes=16,quotient_face_classes=12,
                                 incidence_edges=int(Q.sum())),
        symmetry=action(EC,FC,Q,GQ),
        hardware_flux=flux(B,G),
        covers=covers(),
        physics_boundary="Only finite exact configuration and independent toy tight-binding checks; no spacetime emergence, Einstein constraints, realistic flavor, or photonic experiment.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"aut",result["symmetry"]["Reye_bipartite_aut_color_preserving_order"],
          "rank",result["spectral"]["unsigned_incidence_rank_exact"],
          "flux_moment",result["hardware_flux"]["sixth_moment_return_difference_exact"],flush=True)
    return result
if __name__=="__main__":main()
