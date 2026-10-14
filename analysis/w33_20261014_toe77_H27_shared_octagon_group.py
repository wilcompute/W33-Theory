"""TOE77: prove/refute exact H27 group inside the 216-element pair
stabilizer acting transitively on 27 shared native W33 octagons.

Group calculations are on explicit permutation tuples, no group-name
guessing. If a 27-Sylow regular subgroup has center order 3,
exponent 3 and commutator order 3, it is extraspecial H_27.
The 216 / 27 = 8 quotient action is checked separately; a
Q8 semidirect product will only be asserted if a complement
and quaternion relations are EXPLICITLY verified.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_embedded_theta_exterior_flux import build
from w33_20261014_toe77_twentyseven_octagons import compose,inverse
from w33_pass1081_1086_core import (
 build_w33,transvection_perm,outer_similitude_perm,line_perm)

def subgroup(generators,identity,limit=250):
    have={identity};queue=collections.deque([identity])
    while queue:
        x=queue.popleft()
        for s in generators:
            y=compose(s,x)
            if y not in have:
                have.add(y)
                if len(have)>limit:return None
                queue.append(y)
    return have

def order_of(g,e):
    x=e
    for n in range(1,300):
        x=compose(g,x)
        if x==e:return n
    raise AssertionError("finite permutation order exceeds bound")

def certificate():
    edges,cycles,p,chords=build()
    native_common=sorted(set(i for i,c in enumerate(cycles) if chords[0] in c)&
                         set(i for i,c in enumerate(cycles) if chords[1] in c))
    assert len(native_common)==27
    base=tuple(sorted(chords))
    points,pidx,lines,lidx,_,_,_,flags,flagidx=build_w33()
    def on_flags(perm):
        line=line_perm(perm,lines,lidx)
        return tuple(flagidx[(perm[a],line[b])] for a,b in flags)
    G=[on_flags(transvection_perm(points[i],points,pidx)) for i in (0,1,2,4,8,15)]
    G.append(on_flags(outer_similitude_perm(points,pidx)))
    I160=tuple(range(160))
    reps={base:I160};q=collections.deque([base])
    hset=set()
    while q:
        x=q.popleft();rep=reps[x]
        for g in G:
            y=tuple(sorted((g[x[0]],g[x[1]])))
            if y not in reps:
                reps[y]=compose(g,rep);q.append(y)
            else:
                h=compose(inverse(reps[y]),compose(g,rep))
                if h!=I160:hset.add(h)
    assert len(reps)==240 and 51840//len(reps)==216
    cycle_lookup={frozenset(c):i for i,c in enumerate(cycles)}
    index={cy:i for i,cy in enumerate(native_common)}
    perms27=set()
    for h in hset:
        perm=tuple(index[cycle_lookup[frozenset(h[e] for e in cycles[cy])]]
                    for cy in native_common)
        perms27.add(perm)
    I=tuple(range(27));perms27.discard(I)
    full=subgroup(perms27,I,limit=216)
    assert full is not None and 216%len(full)==0
    assert all(sorted(g)==list(range(27)) for g in full)
    # The 27 shared octagons are one transitive orbit under the pair
    # stabilizer; quotient image cannot be larger than 216.
    orbit={g[0] for g in full}
    assert len(orbit)==27
    hist=collections.Counter(order_of(g,I) for g in full)
    three=[g for g in full if order_of(g,I)==3]
    H=None
    for a in three:
        if H:break
        for b in three:
            if a==b:continue
            candidate=subgroup((a,b),I,limit=27)
            if candidate is not None and len(candidate)==27:
                H=candidate
                break
    sylow_found=H is not None
    res={
      "status":"PASS_TOE77_NATIVE_27_OCTAGON_EXPLICIT_GROUP_STRUCTURE",
      "pair_stabilizer_order_in_PGSp":216,
      "pair_orbit_size":240,
      "induced_faithful_permutation_group_order":len(full),
      "group_order_histogram":dict(sorted(hist.items())),
      "transitive_on_27_shared_octagons":True,
      "Sylow_3_order_27_subgroup_exhibited":sylow_found,
      "native_common_octagons":27,
      "Schreier_generators_native_160":len(hset),
      "distinct_induced_generators_27":len(perms27),
      "classification_guard":"Numerical order 27 does not prove an E6 representation or equivalence with the previously constructed regular/Payne and trinification H27; only explicit group operations on the shared 27 octagons establish an abstract isomorphism."
    }
    if H is not None:
        center=[x for x in H if all(compose(x,y)==compose(y,x) for y in H)]
        Hhist=collections.Counter(order_of(x,I) for x in H)
        regular=len({x[0] for x in H})==27
        normal=all(compose(compose(g,h),inverse(g)) in H for g in full for h in H)
        nonabelian=len(center)<27
        extraspecial=len(center)==3 and Hhist.get(3,0)==26 and nonabelian
        res.update({
          "selected_Sylow27_element_order_histogram":dict(sorted(Hhist.items())),
          "selected_Sylow27_center_order":len(center),
          "selected_Sylow27_regular_on_27_octagons":regular,
          "selected_Sylow27_normal_in_pair_stabilizer":normal,
          "selected_Sylow27_nonabelian":nonabelian,
          "selected_Sylow27_is_extraspecial_Heisenberg_H27":extraspecial,
          "explicit_regular_address_action":(
             "For fixed shared octagon C0, H27 -> shared cycles via h|->h(C0) "
             "is a bijection" if extraspecial and regular else "Not established")
        })
    if H is not None:
        # Schur-Zassenhaus is not assumed: exhibit an actual Sylow-2
        # complement of order 8 in the explicit 216-element group.
        two=[g for g in full if order_of(g,I) in (2,4,8)]
        Q=None
        for a in two:
            if Q:break
            for b in two:
                guess=subgroup((a,b),I,limit=8)
                if guess is not None and len(guess)==8:
                    Q=guess
                    break
        assert Q is not None
        qhist=collections.Counter(order_of(q,I) for q in Q)
        assert not (Q& H-{I})
        assert len(H)*len(Q)==len(full)==216
        dihedral=(qhist.get(1,0)==1 and qhist.get(2,0)==5 and
                  qhist.get(4,0)==2)
        quaternion=(qhist.get(1,0)==1 and qhist.get(2,0)==1 and
                    qhist.get(4,0)==6)
        # The center Z(H) has order 3 for extraspecial H27.
        central=set(x for x in H if all(compose(x,y)==compose(y,x) for y in H))
        assert len(central)==3
        classes={frozenset(compose(x,z) for z in central) for x in H}
        assert len(classes)==9
        trivial=frozenset(central)
        nontriv=next(x for x in classes if x!=trivial)
        phase_orbit={frozenset(compose(compose(q,x),inverse(q))
                               for x in nontriv) for q in Q}
        assert phase_orbit<=classes
        phase_remaining=classes-{trivial}
        phase_orbit_sizes=[]
        while phase_remaining:
            seedclass=next(iter(phase_remaining))
            orb={frozenset(compose(compose(q,x),inverse(q))
                           for x in seedclass) for q in Q}
            assert orb<=phase_remaining
            phase_remaining-=orb
            phase_orbit_sizes.append(len(orb))
        central_fixed=all(compose(compose(q,z),inverse(q))==z
                          for q in Q for z in central)
        full_center=[g for g in full
                       if all(compose(g,h)==compose(h,g) for h in full)]
        # Exact action on unordered pairs of the 27 shared octagons.
        # This tests whether the native 216-group can preserve the
        # cubic-surface GQ(2,4) adjacency with degree 10, rather than
        # simply sharing its 27 point count.
        all_pairs=set(itertools.combinations(range(27),2))
        pair_orbits=[]
        while all_pairs:
            pair=min(all_pairs)
            orb={tuple(sorted((g[pair[0]],g[pair[1]]))) for g in full}
            assert orb<=all_pairs
            all_pairs-=orb
            assert 2*len(orb)%27==0
            pair_orbits.append(orb)
        pair_orbits.sort(key=lambda orb:(len(orb),min(orb)))
        degrees=[2*len(orb)//27 for orb in pair_orbits]
        assert sum(degrees)==26
        matching=[]
        # SRG(27,10,1,5) is the cubic-surface intersection graph.
        # Invariant graphs are unions of entire unordered pair orbitals.
        for flags in itertools.product((0,1),repeat=len(pair_orbits)):
            if sum(d for d,choose in zip(degrees,flags) if choose)!=10:
                continue
            adj=[set() for _ in range(27)]
            for orb,include in zip(pair_orbits,flags):
                if include:
                    for u,v in orb:
                        adj[u].add(v);adj[v].add(u)
            assert all(len(x)==10 for x in adj)
            common_adj=set()
            common_non=set()
            tri=0
            for u in range(27):
                for v in range(u+1,27):
                    x=len(adj[u]&adj[v])
                    (common_adj if v in adj[u] else common_non).add(x)
                    if v in adj[u]:tri+=x
            if common_adj=={1} and common_non=={5}:
                triangles=tri//3
                assert triangles==45
                matching.append({
                    "selected_pair_orbit_indices":[j for j,v in enumerate(flags) if v],
                    "triangle_tritangent_count":triangles,
                    "srg_parameters":[27,10,1,5]
                })
        assert sum(len(o) for o in pair_orbits)==351
        z_nontrivial=[z for z in central if z!=I]
        assert len(z_nontrivial)==2
        inverted=0
        for q in Q:
            cz=compose(compose(q,z_nontrivial[0]),inverse(q))
            assert cz in central
            if cz!=z_nontrivial[0]:
                assert cz==z_nontrivial[1]
                inverted+=1
        # TOE78: native 27-octagon GQ(2,4) line geometry.
        assert len(matching)==1
        idx=matching[0]["selected_pair_orbit_indices"]
        graph=[set() for _ in range(27)]
        for j in idx:
            for a,b in pair_orbits[j]:
                graph[a].add(b);graph[b].add(a)
        tri={frozenset((a,b,c)) for a in range(27)
             for b in graph[a] if b>a
             for c in graph[a]&graph[b] if c>b}
        assert len(tri)==45
        assert all(sum(x in L for L in tri)==5 for x in range(27))
        assert all(sum(v in graph[x] for v in L)==1
                   for x in range(27) for L in tri if x not in L)
        # Native H27 right cosets, independent of cubic-frame labels.
        through=[L for L in tri if 0 in L]
        directions=set()
        for L in through:
            subdirs={frozenset((I,h,compose(h,h))) for h in H
                     if h!=I and order_of(h,I)==3
                     and frozenset((I[0],h[0],compose(h,h)[0]))==L}
            assert len(subdirs)==1
            directions.update(subdirs)
        assert len(directions)==5
        native_cosets={frozenset(compose(g,d)[0] for d in D)
                       for D in directions for g in H}
        assert native_cosets==tri
        Q0={g for g in full if g[0]==0}
        assert len(Q0)==8
        unseen=set(through);dorbits=[]
        while unseen:
            L=next(iter(unseen))
            orb={frozenset(q[x] for x in L) for q in Q0}
            assert orb<=unseen
            unseen-=orb;dorbits.append(orb)
        direction_sizes=sorted(map(len,dorbits))
        line_sizes=sorted(len({frozenset(h[x] for x in L)
                               for h in H for L in orb}) for orb in dorbits)
        assert line_sizes==[9,18,18]
        z=next(h for h in central if h!=I)
        preserving=[q for q in Q0
                    if compose(compose(q,z),inverse(q))==z]
        assert len(preserving)==4
        # TOE78 cross-repo test: enumerate ALL choices of H27 generating
        # pairs, and compare each induced regular H27 torsor to the
        # original frozen cubic-surface 5-direction right-coset system.
        # This checks H27-equivariance, not merely abstract SRG isomorphism.
        def abstract_mul(g,h):
            a,b,c=g;A,B,C=h
            return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
        tuples=list(itertools.product(range(3),repeat=3))
        zero=(0,0,0)
        standard_directions=((0,0,1),(0,1,1),(1,0,1),
                             (1,1,0),(1,2,2))
        standard_lines={
            frozenset(abstract_mul(g,p)
                      for p in (zero,d,abstract_mul(d,d)))
            for d in standard_directions for g in tuples}
        assert len(standard_lines)==45
        noncentral=sorted(h for h in H if h not in central)
        gauges=[]
        variants=set()
        tested=0
        for xx in noncentral:
            xp=(I,xx,compose(xx,xx))
            for yy in noncentral:
                if subgroup((xx,yy),I,limit=27) is None:
                    continue
                # An exponent-3 group generated by xx,yy is H27.
                zz=compose(compose(compose(xx,yy),inverse(xx)),inverse(yy))
                if zz==I:continue
                yp=(I,yy,compose(yy,yy))
                zp=(I,zz,compose(zz,zz))
                normal={
                    (a,b,c):compose(compose(xp[a],yp[b]),zp[c])
                    for a,b,c in tuples}
                assert len(set(normal.values()))==27
                tested+=1
                index={v:normal[v][0] for v in tuples}
                transformed={frozenset(index[h] for h in L)
                             for L in standard_lines}
                variants.add(frozenset(transformed))
                if transformed==tri:
                    gauges.append([index[v] for v in tuples])
        assert tested==432
        assert len(variants)==9
        assert len(gauges)==48
        res["original_H27_432_aut_basis_distinct_cubic_direction_geometries"]=len(variants)
        res["original_H27_cubic_line_geometry_aut_stabilizer_order"]=len(gauges)
        res["original_5_coset_directions_abstract_H27_generator_pairs_tested"]=tested
        res["original_address_H27_to_native_octagon_equivariant_gauge_count"]=len(gauges)
        res["example_original_H27_address_to_octagon_bijection"]=(gauges[0] if gauges else None)
        ordered={tuple(w) for L in tri for w in itertools.permutations(L)}
        assert len(ordered)==270
        leftovers=set(ordered)
        oriented_orbit_sizes=[]
        while leftovers:
            w=min(leftovers)
            orb={tuple(g[v] for v in w) for g in full}
            assert orb<=leftovers
            leftovers-=orb
            oriented_orbit_sizes.append(len(orb))
        oriented_orbit_sizes.sort()
        assert oriented_orbit_sizes==[54,108,108]
        res["native_216_orbits_on_270_based_oriented_triangle_cubics"]=oriented_orbit_sizes
        res["native_270_directed_triangle_instruction_bijection"]=True
        res["native_GQ24_line_count"]=len(tri)
        res["native_GQ24_each_point_lines"]=5
        res["native_GQ24_exact_right_cosets_of_five_H27_C3_directions"]=True
        res["native_GQ24_tritangent_lines"]=[sorted(L) for L in sorted(tri,key=lambda t:sorted(t))]
        res["native_D8_direction_orbit_sizes"]=direction_sizes
        res["native_216_tritangent_orbit_sizes"]=line_sizes
        res["center_preserving_order4_subgroup_size"]=len(preserving)
        res["center_inverting_order8_coset_size"]=len(Q0)-len(preserving)
        res.update({
          "unordered_pair_orbit_lengths":[len(x) for x in pair_orbits],
          "unordered_pair_orbit_edges":[[list(pair) for pair in sorted(orb)] for orb in pair_orbits],
          "normal_H27_center_generator_27":list(z),
          "unordered_pair_orbit_valencies":degrees,
          "invariant_degree10_graph_candidate_subsets_tested":
            sum(1 for flags in itertools.product((0,1),repeat=len(degrees))
                if sum(d for d,v in zip(degrees,flags) if v)==10),
          "native_216_invariant_cubic_surface_intersection_srg_candidates":matching,
          "native_216_invariant_cubic_surface_intersection_srg_count":len(matching),
          "dihedral_reflections_inverting_Heisenberg_center":inverted,
          "dihedral_elements_preserving_Heisenberg_center":8-inverted,
          "projective_Clifford_warning":
            "The normal H27 subgroup and D8 quotient distinguish this 216-group from the ordinary projective one-qutrit Clifford F3^2 semidirect SL2(3). An anti-symplectic operation inverts the scalar Heisenberg center and cannot act by unitary conjugation on a fixed nontrivial central character."
        })
        res.update({
          "explicit_order8_complement_found":True,
          "order8_complement_element_orders":dict(sorted(qhist.items())),
          "order8_complement_is_quaternion_Q8":quaternion,
          "order8_complement_is_dihedral_D8":dihedral,
          "pair_stabilizer_is_semidirect_H27_by_D8":bool(normal and extraspecial and dihedral),
          "pair_stabilizer_is_semidirect_H27_by_Q8":
              bool(normal and extraspecial and quaternion),
          "H27_center_fixed_pointwise_under_order8":central_fixed,
          "D8_orbit_sizes_on_eight_nonzero_H27_mod_center_classes":sorted(phase_orbit_sizes),
          "order8_orbit_size_on_eight_nonzero_H27_mod_center_classes":
              len(phase_orbit),
          "full_216_group_center_order":len(full_center),
          "comparison_warning":"Even if G is H27 semidirect Q8 of order216, it must NOT be identified with the ordinary projective single-qutrit Clifford group ASp(2,3) solely by its order 216. Compare group center and natural 9-point/27-point actions before any Clifford claim."
        })
    return res
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe77_H27_shared_octagon_group.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],"order",c["induced_faithful_permutation_group_order"])
    print("ORBITALS",c.get("unordered_pair_orbit_valencies"),"SRG",c.get("native_216_invariant_cubic_surface_intersection_srg_count"),"CENTER_INVERSION",c.get("dihedral_reflections_inverting_Heisenberg_center"))
    print("GEOMETRIES",c.get("original_H27_432_aut_basis_distinct_cubic_direction_geometries"),"GAUGES",c.get("original_address_H27_to_native_octagon_equivariant_gauge_count"),"INSTRUCTION_ORBITS",c.get("native_216_orbits_on_270_based_oriented_triangle_cubics"))
    print("D8",c.get("order8_complement_is_dihedral_D8"),"semidirect",c.get("pair_stabilizer_is_semidirect_H27_by_D8"),"orders",c.get("order8_complement_element_orders"),"orbits",c.get("D8_orbit_sizes_on_eight_nonzero_H27_mod_center_classes"))
    print("Q8",c.get("order8_complement_is_quaternion_Q8"), "semidirect",c.get("pair_stabilizer_is_semidirect_H27_by_Q8"), "center",c.get("full_216_group_center_order"),"phase_orbit",c.get("order8_orbit_size_on_eight_nonzero_H27_mod_center_classes"))
    print("H27",c.get("selected_Sylow27_is_extraspecial_Heisenberg_H27"),
          "center",c.get("selected_Sylow27_center_order"),
          "regular",c.get("selected_Sylow27_regular_on_27_octagons"),
          "normal",c.get("selected_Sylow27_normal_in_pair_stabilizer"))
