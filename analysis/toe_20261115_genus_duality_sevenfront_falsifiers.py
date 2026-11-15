#!/usr/bin/env python3
"""Six-front independent audit: Csaszar/Szilassi genus, Fano doubling,
N12 genus-six dual obstruction, W33 native frame kernel, driven-local H27,
flux-compensated KK vectors, photonic calibration cost, F8 bound gaps.

Source datasets read by AST from existing tracked repo scripts, never rewritten.
The abstract R3 non-realizability theorem is external (Schewe), not claimed
to follow from numerical face checks.
"""
from __future__ import annotations
import ast
import json
import math
from collections import Counter,defaultdict,deque
from fractions import Fraction
from itertools import combinations,product
from pathlib import Path
import numpy as np
import networkx as nx
from scipy.linalg import expm
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_sixfront_genus_duality_native_tests.json"

def repo_literal(file,name):
    source=ast.parse((ROOT/"analysis"/file).read_text(encoding="utf-8"))
    for stmt in source.body:
        if isinstance(stmt,ast.Assign):
            if any(isinstance(t,ast.Name) and t.id==name for t in stmt.targets):
                return ast.literal_eval(stmt.value)
    raise AssertionError(f"literal {name} missing in {file}")

def oriented_surface(triangles):
    """Validate full simplicial closed orientable surface and both boundary ranks."""
    triangles=[tuple(sorted(x)) for x in triangles]
    assert len(set(triangles))==len(triangles)
    n=max(max(t) for t in triangles)+1
    assert set(sum((list(t) for t in triangles),[]))==set(range(n))
    ef=defaultdict(list)
    for i,f in enumerate(triangles):
        a,b,c=f
        for x,y in ((a,b),(b,c),(c,a)):
            ef[tuple(sorted((x,y)))].append((i,1 if x<y else -1))
    assert len(ef)==n*(n-1)//2
    assert all(len(z)==2 for z in ef.values())
    adjacent=[[] for _ in triangles]
    for two in ef.values():
        (i,s),(j,t)=two
        adjacent[i].append((j,-s*t))
        adjacent[j].append((i,-s*t))
    signs={0:1};todo=[0]
    while todo:
        i=todo.pop()
        for j,fac in adjacent[i]:
            desired=signs[i]*fac
            if j in signs:assert signs[j]==desired
            else: signs[j]=desired;todo.append(j)
    assert len(signs)==len(triangles)
    links={}
    for v in range(n):
        adj=defaultdict(set)
        for f in triangles:
            if v in f:
                a,b=[u for u in f if u!=v]
                adj[a].add(b);adj[b].add(a)
        assert len(adj)==n-1
        assert all(len(u)==2 for u in adj.values())
        visited={min(adj)};queue=[min(adj)]
        while queue:
            u=queue.pop()
            for w in adj[u]:
                if w not in visited:visited.add(w);queue.append(w)
        assert len(visited)==len(adj)
        links[v]=len(adj)
    edges=sorted(ef)
    edgeset={e:i for i,e in enumerate(edges)}
    def rank2(columns):
        pivots={}
        for bitmask in columns:
            x=bitmask
            while x:
                j=x.bit_length()-1
                if j in pivots:x^=pivots[j]
                else:pivots[j]=x;break
        return len(pivots)
    d1=[(1<<a)|(1<<b) for a,b in edges]
    d2=[sum(1<<edgeset[p] for p in combinations(f,2)) for f in triangles]
    rank1=rank2(d1);rank2_2=rank2(d2)
    assert rank1==n-1 and rank2_2==len(triangles)-1
    e=len(edges);f=len(triangles);chi=n-e+f
    assert (2-chi)%2==0
    genus=(2-chi)//2
    assert (n-3)*(n-4)==12*genus
    assert e*2==3*f
    assert f==n*(n-1)//3
    dual=nx.Graph();dual.add_nodes_from(range(f))
    for two in ef.values():
        dual.add_edge(two[0][0],two[1][0])
    assert dual.number_of_edges()==e
    assert all(deg==3 for _,deg in dual.degree())
    # Dual faces correspond to primal vertices, each degree n-1.
    assert set(links.values())=={n-1}
    return {
       "V":n,"E":e,"F":f,"genus":genus,"Euler":chi,
       "Betti_mod2":[n-rank1,e-rank1-rank2_2,f-rank2_2],
       "triangles":[list(f) for f in triangles],
       "dual_vertices":f,"dual_edges":e,"dual_faces":n,
       "dual_face_degree":n-1,
       "dual_graph_bipartite":nx.is_bipartite(dual),
       "dual_graph_girth":min(nx.shortest_path_length(dual,v,u)+1
          for v,u in [] ) if False else graph_girth(dual),
       "dual_graph_connected":nx.is_connected(dual),
       "_graph":dual
    }

def graph_girth(G):
    best=10**5
    for s in G:
        dist={s:0};parent={s:-1};todo=deque([s])
        while todo:
            v=todo.popleft()
            for u in G[v]:
                if u not in dist:
                    parent[u]=v;dist[u]=dist[v]+1;todo.append(u)
                elif parent[v]!=u and parent[u]!=v:
                    best=min(best,dist[u]+dist[v]+1)
    return best

def two_surface_genus_and_Fano():
    cs=repo_literal("w33_csaszar_concrete_rotation_flag_orientation.py","FACES_UNORIENTED")
    n12=repo_literal("w33_genus_six_execution.py","FACETS_ONE")
    torus=repo_literal("w33_genus_six_execution.py","TORUS_ONE")
    C=oriented_surface(cs)
    T=oriented_surface([[v-1 for v in face] for face in torus])
    N=oriented_surface([[v-1 for v in face] for face in n12])
    assert all((z["V"],z["E"],z["F"],z["genus"])==(7,21,14,1) for z in (C,T))
    assert (N["V"],N["E"],N["F"],N["genus"])==(12,66,44,6)
    assert (C["dual_vertices"],C["dual_edges"],C["dual_faces"],C["dual_face_degree"])==(14,21,7,6)
    assert (N["dual_vertices"],N["dual_edges"],N["dual_faces"],N["dual_face_degree"])==(44,66,12,11)
    assert nx.is_isomorphic(C["_graph"],nx.heawood_graph())
    assert C["dual_graph_bipartite"]
    assert not N["dual_graph_bipartite"]
    def sts(fs):
        pairs=Counter(tuple(sorted(e)) for f in fs for e in combinations(f,2))
        return len(fs)==7 and len(pairs)==21 and set(pairs.values())=={1}
    split=[]
    for ix in combinations(range(14),7):
        a=[cs[i] for i in ix];b=[cs[i] for i in range(14) if i not in ix]
        if sts(a) and sts(b):split.append(ix)
    assert len(split)==2
    cs_parts=[[list(sorted(cs[i])) for i in split[0]],
              [list(sorted(cs[i])) for i in range(14) if i not in split[0]]]
    assert Counter(tuple(sorted(e)) for f in cs for e in combinations(f,2))=={
       e:2 for e in combinations(range(7),2)
    }
    # For an STS(n), each point occurs in (n-1)/2 blocks and
    # the total blocks number n(n-1)/6 must be integer. n=12 fails.
    assert 12*11%6==0 and 11%2==1  # point-degree is nonintegral, not block count
    # In any orientable neighborly triangulation, a bipartite dual would
    # split the F triangles into 2 STS(n); impossible for n=12.
    for S in (C,T,N):S.pop("_graph")
    return {
      "status":"FANO_DOUBLE_SYSTEM_CSASZAR_VS_NONBIPARTITE_GENUS6",
      "source_Cs":"analysis/w33_csaszar_concrete_rotation_flag_orientation.py",
      "source_N12":"analysis/w33_genus_six_execution.py: FACETS_ONE (Frank Lutz catalogue)",
      "Csaszar":C,"alternate_torus":T,"neighborly_genus6":N,
      "Cs_partition_two_STS7":cs_parts,
      "ordered_STS7_partitions":2,"unordered_STS7_partitions":1,
      "genus6_STS12_impossible":"each 12-point vertex must lie in (12-1)/2 = 5.5 triples of any Steiner triple system",
      "topological_Heawood_map_coloring": {"genus1":7,"genus6":12},
      "geometric_status":"Schewe (2008/2010) forbids a 12-vertex straight triangular embedding in R3, not automatically a planar-hendecagon 12-face dual realization"
    }

def genus_ladder_and_prior_claim_audit():
    rows=[]
    for n in range(4,41):
        num=(n-3)*(n-4)
        admissible=(num%12==0)
        genus_exact=Fraction(num,12)
        graph_genus=math.ceil(genus_exact)
        rows.append({
            "n":n,"numerator":num,
            "orientable_triangular_embedding_possible":admissible,
            "triangular_genus":int(genus_exact) if admissible else None,
            "minimum_orientable_graph_genus":graph_genus,
            "complete_graph_edges":n*(n-1)//2})
        assert admissible == (n%12 in (0,3,4,7))
    exact=[x for x in rows if x["orientable_triangular_embedding_possible"]]
    assert [x["n"] for x in exact[:7]]==[4,7,12,15,16,19,24]
    def jr_min(g):
        n=math.ceil((7+math.sqrt(1+48*g))/2)
        return 10 if g==2 else n
    jr={str(g):{"min_vertices":jr_min(g),
                 "min_triangles":2*jr_min(g)+4*g-4}
        for g in range(0,14)}
    assert jr["2"]=={"min_vertices":10,"min_triangles":24}
    assert jr["6"]=={"min_vertices":12,"min_triangles":44}
    return {
       "status":"RINGEL_YOUNGS_VERSUS_JUNGERMAN_RINGEL_EXACT_EQUALITY_AUDIT",
       "admissible_vertex_residues_mod12":[0,3,4,7],
       "rows":rows,"Jungerman_Ringel_minimal_triangulations":jr,
       "not_equivalent":"genus(K_n)=ceil((n-3)(n-4)/12) does not assert triangular embedding or Euclidean realization",
       "1996_vs_2010":"Altshuler et al list 59 abstract genus6 N12; Schewe 2010 proves no polyhedral R3 realization",
       "repo_overclaims_to_qualify":[
         "analysis/W33_Part_DXXXII_Csaszar_Szilassi_Genus_Unification.md calls both polyhedra no-diagonal and says both require 7 vertices; Szilassi has 14 vertices, 7 faces",
         "same report says K12 neighbor graph of each W33 vertex; W33 point neighborhoods are not K12",
         "analysis/w33_pass2017_2021_the_genus_ladder_was_already_ours.md uses the phrase genus-six polyhedron for an abstract K12 triangulation",
         "geometric symmetry C2 of special R3 realizations differs from combinatorial automorphism group order42"
       ]
    }

def native_W33_frame_overlap():
    vecs=list(product(range(3),repeat=4))
    def ray(v):
        j=next(i for i,x in enumerate(v) if x)
        return tuple(v) if v[j]==1 else tuple(2*x%3 for x in v)
    rays=sorted(set(ray(v) for v in vecs if any(v)))
    assert len(rays)==40
    def om(a,b):
        return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
    A=np.zeros((40,40),dtype=np.int16)
    for i in range(40):
        for j in range(i+1,40):
            if om(rays[i],rays[j])==0:
                A[i,j]=A[j,i]=1
    assert set(A.sum(axis=0))=={12}
    A2=A@A
    assert all(int(A2[i,j])==(12 if i==j else 2 if A[i,j] else 4)
               for i in range(40) for j in range(40))
    # Strong negative control of an older repo interpretation:
    # the 12 neighbors of a W33 point are FOUR DISJOINT TRIANGLES,
    # not an induced complete K12.
    neighbors=np.flatnonzero(A[0])
    G_neighborhood=nx.from_numpy_array(A[np.ix_(neighbors,neighbors)])
    assert sorted(len(c) for c in nx.connected_components(G_neighborhood))==[3,3,3,3]
    assert all(nx.is_isomorphic(G_neighborhood.subgraph(c),nx.complete_graph(3))
               for c in nx.connected_components(G_neighborhood))
    frames=[]
    for four in combinations(range(40),4):
        nonperp=[(a,b) for a,b in combinations(range(4),2)
                 if om(rays[four[a]],rays[four[b]])]
        if len(nonperp)==2 and len({z for edge in nonperp for z in edge})==4:
            frames.append(four)
    assert len(frames)==1620
    B=np.zeros((1620,40),dtype=np.int16)
    for i,frame in enumerate(frames):
        for v in frame:B[i,v]=1
    G=B.T@B
    goal=156*np.eye(40,dtype=np.int16)+21*A+6*np.ones((40,40),dtype=np.int16)
    assert np.array_equal(G,goal)
    eig=np.linalg.eigvalsh(G)
    assert np.allclose(eig,np.array([72]*15+[198]*24+[648]),atol=1e-9)
    overlap=B@B[0]
    census=dict(sorted((int(i),int(n)) for i,n in Counter(map(int,overlap)).items()))
    assert sum(census.values())==1620
    assert sum(j*n for j,n in census.items())==648
    assert census[4]==1
    # Native local moves in FRAME space: replace exactly one of four
    # projective rays while preserving the symplectic apartment property.
    K=B@B.T
    assert np.array_equal(np.diag(K),np.full(1620,4,dtype=K.dtype))
    flip=(K==3)
    assert np.array_equal(flip.sum(axis=1),np.full(1620,8))
    GF=nx.from_numpy_array(flip)
    components=list(nx.connected_components(GF))
    n_components=len(components)
    frame_bipartite=nx.is_bipartite(GF)
    component_sizes=Counter(len(comp) for comp in components)
    union_ray_sizes=Counter()
    induced_ray_degrees=Counter()
    memberships=np.zeros(40,dtype=int)
    component_ray_masks=[]
    for comp in components:
        ray_set=np.flatnonzero(B[list(comp)].sum(axis=0))
        union_ray_sizes[len(ray_set)]+=1
        component_ray_masks.append(frozenset(map(int,ray_set)))
        memberships[ray_set]+=1
        sub=A[np.ix_(ray_set,ray_set)]
        induced_ray_degrees[tuple(sorted(set(map(int,sub.sum(axis=1)))))] +=1
        graph8=nx.from_numpy_array(sub)
        assert nx.is_isomorphic(graph8,nx.complete_bipartite_graph(4,4))
        colors=nx.algorithms.bipartite.color(graph8)
        side0={int(ray_set[i]) for i,v in colors.items() if v==0}
        side1={int(ray_set[i]) for i,v in colors.items() if v==1}
        assert len(side0)==len(side1)==4
        observed=set()
        comp_list=sorted(comp)
        for idx in comp_list:
            F=set(frames[idx])
            c0=frozenset(F&side0)
            c1=frozenset(F&side1)
            assert len(c0)==len(c1)==2
            observed.add((c0,c1))
        assert len(observed)==36
        # Adjacent frames differ by one selected ray in exactly one
        # part: J(4,2) square J(4,2). This is checked on *every* pair.
        for idx in comp_list:
            for jdx in comp_list:
                if idx==jdx:continue
                fi=set(frames[idx]);fj=set(frames[jdx])
                ia=len((fi&side0)&(fj&side0))
                ib=len((fi&side1)&(fj&side1))
                expect=(ia==1 and ib==2) or (ia==2 and ib==1)
                assert bool(flip[idx,jdx])==expect
    assert sum(component_sizes.values())==n_components
    assert n_components==45 and component_sizes=={36:45}
    assert union_ray_sizes=={8:45}
    assert len(set(component_ray_masks))==45
    assert set(map(int,memberships))=={9}
    # Two-ray changes are the minimal possible inter-sector moves.
    two_ray=(K==2)
    assert np.array_equal(two_ray.sum(axis=1),np.full(1620,90))
    total_move=nx.from_numpy_array(flip|two_ray)
    two_ray_only=nx.from_numpy_array(two_ray)
    two_ray_only_components=nx.number_connected_components(two_ray_only)
    two_ray_plus_one_components=nx.number_connected_components(total_move)
    component_id=np.zeros(1620,dtype=int)
    for idx,comp in enumerate(components):
        component_id[list(comp)]=idx
    cross_moves=np.sum(two_ray & (component_id[:,None]!=component_id[None,:]),axis=1)
    within_moves=np.sum(two_ray & (component_id[:,None]==component_id[None,:]),axis=1)
    assert set(map(int,cross_moves))=={72}
    assert set(map(int,within_moves))=={18}
    one_component=sorted(components[0])
    ev_comp=np.linalg.eigvalsh(flip[np.ix_(one_component,one_component)].astype(float))
    spectrum_comp={-4:4,-2:12,0:9,2:4,4:6,8:1}
    assert np.allclose(ev_comp,
        np.array([e for e,mult in sorted(spectrum_comp.items())
                  for _ in range(mult)]),atol=1e-8)
    # Positive-semidefinite 1620-frame kernel with rank 40.
    uniform_overlap=Fraction(648,1620)
    assert uniform_overlap==Fraction(2,5)
    # Mean-field free energy for all frames aligned vs uniform.
    # At beta J > 2 log(q)/(4-2/5), the aligned delta has lower
    # free energy than the uniform solution, a sufficient test only.
    q=1620
    beta_sufficient=2*math.log(q)/(4-float(uniform_overlap))
    spinodal=q/198
    assert beta_sufficient<spinodal
    return {
      "status":"NATIVE_W33_1620_FRAME_INTERSECTION_PSD_KERNEL",
      "n_frames":q,"n_rays":40,
      "srg_point_graph":[40,12,2,4],
      "induced_12_vertex_neighborhood":"4 disjoint K3, NOT K12",
      "projective_frame_overlap_census":census,
      "frame_one_ray_move_graph_degree":8,
      "frame_one_ray_move_graph_connected_components":n_components,
      "frame_one_ray_move_graph_bipartite":frame_bipartite,
      "frame_component_size_histogram":dict(component_sizes),
      "frame_component_ray_union_sizes":dict(union_ray_sizes),
      "frame_component_induced_W33_degrees":{str(k):v for k,v in induced_ray_degrees.items()},
      "frame_component_ray_membership_histogram":dict(Counter(map(int,memberships))),
      "frame_component_ray_sets_distinct":len(set(component_ray_masks)),
      "all_45_induced_point_graphs":"K4,4",
      "all_45_frame_transition_graphs":"J(4,2) Cartesian J(4,2)",
      "two_ray_move_graph_degree":90,
      "two_ray_moves_within_K44_sector":18,
      "two_ray_moves_cross_K44_sectors":72,
      "two_ray_only_connected_components":two_ray_only_components,
      "one_or_two_ray_connected_components":two_ray_plus_one_components,
      "one_component_transition_spectrum":{str(e):m for e,m in spectrum_comp.items()},
      "B_gram_identity":"B^T B=156 I+21 A_W33+6 J",
      "B_gram_eigenvalues":{"648":1,"198":24,"72":15},
      "frame_kernel_rank":40,
      "frame_kernel_zero_eigenvalue_multiplicity":1580,
      "uniform_mean_overlap":str(uniform_overlap),
      "overlap_same_frame":4,
      "sufficient_betaJ_aligned_beats_uniform":beta_sufficient,
      "uniform_local_spinodal_betaJ":spinodal,
      "scope":"Canonical combinatorial kernel but postulated attractive interaction -J*|intersection|; finite Gibbs state symmetric, ordered phase only conditional M->infinity."
    }

def h27_driven_local_clock():
    elements=list(product(range(3),repeat=3))
    ix={g:k for k,g in enumerate(elements)}
    def mul(g,h):
        a,b,c=g;u,v,w=h
        return ((a+u)%3,(b+v)%3,(c+w+a*v)%3)
    def mat(g):
        U=np.zeros((27,27),complex)
        for h,i in ix.items():U[ix[mul(g,h)],i]=1
        return U
    X,Y,Z=(1,0,0),(0,1,0),(0,0,1)
    Ux,Uy,Uz=mat(X),mat(Y),mat(Z)
    assert np.array_equal(Ux@Uy@Ux.conj().T@Uy.conj().T,Uz)
    assert np.array_equal(np.linalg.matrix_power(Uz,3),np.eye(27))
    def H(U):
        return 1j*(2*math.pi/(3*math.sqrt(3)))*(U-U.conj().T)
    HX,HY=H(Ux),H(Uy)
    assert np.allclose(HX,HX.conj().T) and np.allclose(HY,HY.conj().T)
    assert np.linalg.norm(expm(-1j*HX)-Ux)<1e-12
    assert np.linalg.norm(expm(-1j*HY)-Uy)<1e-12
    assert np.count_nonzero(abs(HX)>1e-9)==54
    assert np.count_nonzero(abs(HY)>1e-9)==54
    # All H supports are ± generator edges, precisely local in
    # the 4-regular Cayley graph.
    assert all(not(abs(HX[i,j])>1e-9) or
               (abs(Ux[i,j])+abs(Ux[j,i])>0)
               for i in range(27) for j in range(27))
    assert all(not(abs(HY[i,j])>1e-9) or
               (abs(Uy[i,j])+abs(Uy[j,i])>0)
               for i in range(27) for j in range(27))
    pulses=[-HY,-HX,HY,HX] # chronological Y^-1,X^-1,Y,X
    U=np.eye(27,dtype=complex)
    for HP in pulses:U=expm(-1j*HP)@U
    assert np.linalg.norm(U-Uz)<1e-12
    assert np.linalg.norm(np.linalg.matrix_power(U,3)-np.eye(27))<1e-12
    return {
       "status":"EXACT_LOCAL_FOUR_PULSE_H27_FLOQUET_COMMUTATOR",
       "Hilbert_dimension":27,"generator_order":3,
       "graph_degree_union_Xpm_Ypm":4,
       "nonzero_directed_hoppings_each_H":54,
       "H_X":"(2*pi/(3*sqrt(3))) i (U_X-U_X^dagger)",
       "H_Y":"(2*pi/(3*sqrt(3))) i (U_Y-U_Y^dagger)",
       "pulse_chronological":["-H_Y","-H_X","H_Y","H_X"],
       "Floquet_4_pulse_U":"U_Z",
       "recur_after_12_unit_pulses":True,
       "max_matrix_unitary_error":float(np.linalg.norm(U-Uz)),
       "scope":"Explicitly switched time-dependent local Hamiltonian (on H27 Cayley graph); not autonomous and not a universal physical time scale. Escapes isolated 12-cycle logarithm no-go by driving."
    }

def flux_compensated_Killing_vectors():
    theta,phi,f=sp.symbols("theta phi f",real=True)
    S=sp.sin(theta);C=sp.cos(theta)
    generators={
      "K_x":((-sp.sin(phi),-sp.cot(theta)*sp.cos(phi)),f*S*sp.cos(phi)),
      "K_y":((sp.cos(phi),-sp.cot(theta)*sp.sin(phi)),f*S*sp.sin(phi)),
      "K_z":((0,1),f*C)
    }
    verified=[]
    for label,((Kth,Kph),mu) in generators.items():
        components=(-f*S*Kph,f*S*Kth)
        assert all(sp.trigsimp(components[i]-sp.diff(mu,[theta,phi][i]))==0
                   for i in range(2))
        # Lie derivative of F=d (i_K F) because dF=0, and i_KF=dmu.
        d2=sp.simplify(sp.diff(components[1],theta)-sp.diff(components[0],phi))
        assert sp.trigsimp(d2)==0
        verified.append(label)
    return {
      "status":"SIX_FLUX_COMPENSATED_KILLING_VECTORS_PLUS_U1",
      "sphere_Killing_generators":verified,
      "identity":"i_K F=d(mu_K), hence Lie_K F = 0 for each SO3 Killing field",
      "product_sphere_lifted_isometry_algebra":"so(3) + so(3), dimension 6",
      "additional_constant_abelian_zero_mode":1,
      "symmetry_protected_massless_5D_vector_count":7,
      "limits":"Infinitesimal gauge-compensated isometries at classical linear level. Full coupled vector/scalar mass matrices, global bundle subtleties and ExFT embedding uncomputed."
    }

def optical_calibration_resource_falsifier():
    k=16;columns=16
    eps=.002;alpha=.01
    # For each subset A of 16 rail outcomes, Hoeffding:
    # P(|p_hat(A)-p(A)| >= eps/2) <= 2 exp(-n eps²/2).
    # The l1 norm equals 2*max_A|p_hat(A)-p(A)|.
    # Union over 2^k sets and 16 preparation columns.
    n=math.ceil(2/eps**2*math.log(2**(k+1)*columns/alpha))
    assert columns*2**(k+1)*math.exp(-n*eps**2/2)<=alpha*(1+1e-12)
    prior=json.loads((ROOT/"data"/"toe_20261114_fivefronts_late_independent_certificates.json").read_text())
    photo=prior["results"]["photonic_16rail_confusion_calibration"]
    assert photo["assumed_column_l1_calibration_error"]==eps
    signal=photo["nominal_expected_raw_launches"]
    return {
      "status":"FULL_16x16_READOUT_CERTIFICATION_SHOT_COST_UPPER_BOUND",
      "confidence":1-alpha,"L1_column_tolerance":eps,
      "n_independent_preparations_per_input_rail_sufficient":n,
      "n_total_16_input_preparations_sufficient":n*columns,
      "previous_model_expected_signal_launches":signal,
      "calibration_to_signal_shot_ratio":n*columns/signal,
      "proof":"2^(16+1)*16*exp(-n epsilon^2/2)<=0.01 via all-subset union and Bernoulli Hoeffding",
      "limitations":"This bound is conservative and assumes IID samples per known preparation, no drift. Not a lower bound or optimized calibration method. It makes the previous assumed 0.002 column-L1 confidence operationally costly."
    }

def F8_certified_code_space_gap():
    exact=json.loads((ROOT/"data"/"w33_f8_exact_witness.json").read_text())
    cert=json.loads((ROOT/"data"/"w33_f8_codespace_sos6_certificate_249_100.json").read_text())
    prior=json.loads((ROOT/"data"/"toe_20261114_fivefronts_late_independent_certificates.json").read_text())
    value=(47-32*math.cos(2*math.pi/9))/9
    assert exact["equals_closed_form"] and exact["idempotent"]
    assert cert["certified"] and cert["C_cert"]=="249/100"
    assert cert["block1"]["psd_certified"] and cert["block3"]["psd_certified"]
    assert abs(prior["results"]["F8_full_tangent_Hessian"]["c8"]-value)<1e-10
    # Certificate existence / data audited; proof is the certified solver run
    # owned by Pass12673, not re-executed here.
    return {
      "status":"GLOBAL_VERSUS_CODESPACE_F8_LOWER_BOUND_SCOPE_FALSIFIER",
      "exact_witness_upper":value,
      "pass12673_certified_codespace_lower":2.49,
      "upper_minus_codespace_lower":value-2.49,
      "certificate_top_keys":sorted(cert)[:18],
      "previous_fullspace_Hessian_negative_eigenvalues":prior["results"]["F8_full_tangent_Hessian"]["negative_tangent_eigenvalues"],
      "previous_numerical_family_degree8_coefficient_residual_max":max(
        z["degree8_identity_max_absolute_coefficient_residual"]
        for z in prior["results"]["F8_full_tangent_Hessian"]["flat_null_curved_trajectory_controls"]),
      "limitation":"249/100 lower bound pertains only to the selected C8 code-space; no global C64 matching lower. Numerical equal-value families still lack exact algebraic tangent vectors."
    }

FRONTS={
 "topology_duality_Fano_and_genus6":two_surface_genus_and_Fano,
 "Jungerman_Ringel_genus_ladder":genus_ladder_and_prior_claim_audit,
 "W33_native_overlap_frame_selector":native_W33_frame_overlap,
 "H27_driven_local_Hamiltonian":h27_driven_local_clock,
 "D9_compensated_massless_KK_vectors":flux_compensated_Killing_vectors,
 "photonic_16rail_calibration_cost":optical_calibration_resource_falsifier,
 "F8_certified_codespace_gap":F8_certified_code_space_gap
}
def main():
    results={}
    for label,fn in FRONTS.items():
        results[label]=fn()
        print("PASS",label,results[label]["status"],flush=True)
    payload={"status":"SEVEN_ORTHOGONAL_RESEARCH_CONTROLS",
             "main_scope":"Csaszar Szilassi abstract incidence is not Euclidean realization",
             "n_controls":len(results),"results":results}
    OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return payload

if __name__=="__main__":main()
