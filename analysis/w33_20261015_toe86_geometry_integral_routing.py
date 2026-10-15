"""TOE86 tracks I, IV, V: 468-pair census, integral SNF, Clifford routing.

Exactly reconstructs the TOE83 native H27/Schlaefli geometry. Runs in a clean
Git worktree; does not touch other agents' scratch files or dirty master.
"""
from __future__ import annotations
import collections, itertools, json
from collections import Counter
from itertools import product, combinations
from pathlib import Path
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
from analysis.w33_20261015_toe85_h2_relation_module import geometry, rank_and_basis, ROOT

D=((0,0,1),(0,1,1),(1,0,1),(1,1,0),(1,2,2))
H=list(product(range(3),repeat=3))
IDX={h:i for i,h in enumerate(H)}
IDENTITY=(0,0,0)

def mul(x,y):
    a,b,c=x; A,B,C=y
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)

def pow3(x,n):
    out=IDENTITY
    for _ in range(n): out=mul(out,x)
    return out

def native():
    tri=sorted({tuple(sorted(IDX[mul(g,t)] for t in (IDENTITY,d,mul(d,d))))
                for g in H for d in D})
    edges=sorted({tuple(sorted(e)) for f in tri for e in combinations(f,2)})
    ei={e:i for i,e in enumerate(edges)}
    adj=[set() for _ in H]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    sq=set()
    for u,v in combinations(range(27),2):
        if v in adj[u]:continue
        for a,b in combinations(sorted(adj[u]&adj[v]),2):
            sq.add(tuple(sorted(ei[tuple(sorted(e))] for e in
                            ((u,a),(a,v),(v,b),(b,u)))))
    assert len(tri)==45 and len(edges)==135 and len(sq)==1080
    perms=[[IDX[mul(g,h)] for h in H] for g in H]
    unseen=set(sq); orbits=[]
    while unseen:
        s=min(unseen)
        orbit={tuple(sorted(ei[tuple(sorted((p[edges[i][0]],p[edges[i][1]])))]
                            for i in s)) for p in perms}
        unseen-=orbit
        orbits.append(sorted(orbit))
    orbits.sort(key=lambda o:(len(o),o[0]))
    assert len(orbits)==40 and all(len(o)==27 for o in orbits)
    return tri, edges, ei, perms, orbits

def rank2(rows):
    piv={}
    for row in rows:
        while row:
            k=row.bit_length()-1
            if k in piv:row^=piv[k]
            else:piv[k]=row;break
    return len(piv)

def automorphisms():
    axes={frozenset((IDENTITY,d,mul(d,d))) for d in D}
    autos=set()
    for x in H:
        for y in H:
            det=(x[0]*y[1]-x[1]*y[0])%3
            if not det:continue
            z=(0,0,det)
            phi=tuple(IDX[mul(mul(pow3(x,a),pow3(y,b)),pow3(z,c))]
                      for a,b,c in H)
            mapped={frozenset(phi[IDX[t]] for t in axis) for axis in axes}
            if mapped == {frozenset(IDX[t] for t in axis) for axis in axes}:
                autos.add(phi)
    return sorted(autos)

def pair_census():
    triangles,edges,ei,perms,orbits=native()
    masks=[[sum(1<<i for i in s) for s in orb] for orb in orbits]
    face_masks=[sum(1<<ei[tuple(sorted(e))] for e in combinations(f,2))
                for f in triangles]
    pairs=[]
    for f in triangles:
        ids=[ei[tuple(sorted(e))] for e in combinations(f,2)]
        pairs.extend(sum(1<<i for i in t) for t in combinations(ids,2))
    assert len(pairs)==135
    cover=[]
    for rows in masks:
        cover.append(sum(1<<j for j,p in enumerate(pairs)
                         if any((p&s).bit_count()%2 for s in rows)))
    full=(1<<135)-1
    solutions={}
    for i,j in combinations(range(40),2):
        if (cover[i]|cover[j])!=full:continue
        r=rank2(face_masks+masks[i]+masks[j])
        solutions[(i,j)]=r
    assert len(solutions)==468 and solutions[(0,10)]==83
    autos=automorphisms()
    # The full subgroup-direction preserving H27 automorphism stabilizer
    # has 48 elements, not merely the earlier 8-element restricted subgroup.
    assert len(autos)==48, ("unexpected direction normalizer",len(autos))
    representative_to_orbit={orb[0]:i for i,orb in enumerate(orbits)}
    maps=[]
    for perm in autos:
        transform=[]
        for orb in orbits:
            image=tuple(sorted(ei[tuple(sorted((perm[edges[k][0]],perm[edges[k][1]])))]
                               for k in orb[0]))
            # A square can lie anywhere within its target orbit.
            target=next((j for j,O in enumerate(orbits) if image in set(O)),None)
            assert target is not None
            transform.append(target)
        assert sorted(transform)==list(range(40))
        maps.append(transform)
    pending=set(solutions)
    classes=[]
    while pending:
        pair=min(pending)
        eq={tuple(sorted((m[pair[0]],m[pair[1]]))) for m in maps}
        assert eq<=set(solutions)
        ranks={solutions[x] for x in eq}
        assert len(ranks)==1
        pending-=eq
        classes.append({"representative":list(pair),"size":len(eq),"face_rank_F2":next(iter(ranks)),
                        "logical_dimension_F2":109-next(iter(ranks)),
                        "members":[list(x) for x in sorted(eq)]})
    return {"all_pairs_tested":780,"covering_admissible_pair_count":len(solutions),
            "native_H27_order":27,"native_normalizer_point_stabilizer_order":len(autos),
            "total_normalizer_order":27*len(autos),
            "equivalence_class_count":len(classes),
            "class_sizes":dict(Counter(str(c["size"]) for c in classes)),
            "all_pair_face_rank_F2_distribution":dict(Counter(str(r) for r in solutions.values())),
            "classes":classes}

def chain_snf():
    _, rows, _=geometry()
    M=Matrix(rows).T
    S=smith_normal_form(M,domain=ZZ)
    diagonal=[abs(int(S[i,i])) for i in range(min(S.shape)) if S[i,i]]
    assert len(diagonal)==83
    assert all(diagonal[i+1]%diagonal[i]==0 for i in range(82))
    torsion=[d for d in diagonal if d>1]
    # Compare reductions to exact F2 and F3 modules.
    r2=len(rank_and_basis(rows,2))
    r3=len(rank_and_basis(rows,3))
    assert r2==r3==83
    assert all(d%2 and d%3 for d in diagonal)
    return {"matrix_shape":[135,99],"rank_over_Q":len(diagonal),
            "unit_invariant_factor_count":len(diagonal)-len(torsion),
            "torsion_invariant_factors":torsion,
            "H2_integral_free_rank":99-len(diagonal),
            "H1_integral_free_rank":135-26-len(diagonal),
            "H1_integral_torsion_invariants":torsion,
            "ranks_F2_F3":[r2,r3]}

def perm_cycles(q):
    seen=set(); cycles=[]
    for i in range(len(q)):
        if i in seen:continue
        cyc=[];j=i
        while j not in seen:
            seen.add(j);cyc.append(j);j=q[j]
        assert j==i
        cycles.append(cyc)
    return cycles

def odd_even_schedule(q):
    n=len(q)
    tokens=list(range(n))
    schedule=[]
    for step in range(n):
        ops=[]
        for j in range(step%2,n-1,2):
            if q[tokens[j]] > q[tokens[j+1]]:
                tokens[j],tokens[j+1]=tokens[j+1],tokens[j]
                ops.append(j)
        schedule.append(ops)
        if all(q[tokens[i]]==i for i in range(n)):break
    assert all(q[tokens[i]]==i for i in range(n))
    return schedule

def gate_compiler():
    H2,face_rows,face_actions=geometry()
    assert H2==H
    triangles, edges, ei, perms, _=native()
    results=[]
    for g in ((1,0,0),(0,1,0),(0,0,1)):
        p=perms[IDX[g]]
        q=[ei[tuple(sorted((p[u],p[v])))] for u,v in edges]
        sign=[1 if p[u]<p[v] else -1 for u,v in edges]
        assert sorted(q)==list(range(135))
        cycles=perm_cycles(q)
        layers=odd_even_schedule(q)
        inversion=sum(x==-1 for x in sign)
        min_swaps=135-len(cycles)
        adjacent_swaps=sum(len(x) for x in layers)
        inv_count=sum(q[i]>q[j] for i in range(135) for j in range(i+1,135))
        assert adjacent_swaps==inv_count
        def compose(a,b): # map first b, then a
            return [(a[0][b[0][i]],a[1][b[0][i]]*b[1][i]) for i in range(135)]
        # Verify signed action has order three, including center.
        current=(list(range(135)),[1]*135)
        for _ in range(3):
            temp=compose((q,sign),current)
            current=([e for e,s in temp],[s for e,s in temp])
        assert current==(list(range(135)),[1]*135)
        # The H27 action on all 99 oriented checks was independently verified
        # by geometry(); assert the matching face permutation lies in the set.
        dest,face_sign=face_actions[g]
        assert sorted(dest)==list(range(99))
        results.append({"generator":list(g),"physical_qutrits":135,
                        "permutation_cycle_count":len(cycles),
                        "unrestricted_SWAP_count_optimal":min_swaps,
                        "linear_nearest_neighbor_SWAP_count_optimal":adjacent_swaps,
                        "linear_odd_even_SWAP_layers":len(layers),
                        "local_qutrit_inversion_count":inversion,
                        "face_stabilizers_mapped":99,
                        "signed_order_three_verified":True,
                        "edge_destination":q,"edge_orientation_sign":sign,
                        "nearest_neighbor_layers_start_positions":layers})
    return {"geometry":"135 edge qudits / 99 oriented face checks",
            "physical_model":"ideal qutrit wire permutations and local j->-j inversions",
            "topology_assumption":"linear nearest-neighbor array; SWAPs idealized",
            "compiled_generators":results,
            "limits":"No gate noise, syndrome extraction, error propagation, threshold, or optical device modeled."}

def certificate():
    result={"provenance":"native TOE83/TOE85 frozen H27 chain data",
            "orbit_pair_census":pair_census(),
            "integral_smith":chain_snf(),
            "encoded_clifford_permutation_compiler":gate_compiler()}
    return result

if __name__=="__main__":
    out=certificate()
    p=ROOT/"data/w33_20261015_toe86_geometry_integral_routing.json"
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("pair classes",out["orbit_pair_census"]["equivalence_class_count"])
    print("face rank distribution",out["orbit_pair_census"]["all_pair_face_rank_F2_distribution"])
    print("smith",out["integral_smith"])
    print("gates",[{k:v for k,v in x.items() if k not in
                   ("edge_destination","edge_orientation_sign","nearest_neighbor_layers_start_positions")}
                  for x in out["encoded_clifford_permutation_compiler"]["compiled_generators"]])
    print("WROTE",p)
