"""TOE87 exact H27 modular modules, Bockstein maps, and three-orbit stress test.

Input: TOE86's 13 equivalence-class representatives for 468 admissible
two-square-orbit CSS complexes, with native oriented 135-edge geometry.
"""
from __future__ import annotations
import collections, json
from itertools import combinations
from pathlib import Path
from analysis.w33_20261015_toe85_h2_relation_module import (
    ROOT, nullspace, rank_and_basis, action_on_kernel, apply
)
from analysis.w33_20261015_toe86_geometry_integral_routing import H, IDX, native
from analysis.w33_20261015_toe86_hom_intertwiners import cycle_basis, independent_ordered

GEN=((1,0,0),(0,1,0))
LINES=((1,0),(0,1),(1,1),(1,2))
CENTER=[(0,0,c) for c in range(3)]

def geometry_data():
    tri,edges,ei,perms,orbits=native()
    cycles=cycle_basis(edges,ei)
    def oriented(walk):
        row=[0]*135
        for u,v in zip(walk,walk[1:]):
            row[ei[tuple(sorted((u,v)))]]+=1 if u<v else -1
        return row
    tri_rows=[oriented([a,b,c,a]) for a,b,c in tri]
    def square_walk(ids):
        ns=collections.defaultdict(set)
        for i in ids:
            u,v=edges[i];ns[u].add(v);ns[v].add(u)
        a=min(ns);walk=[a,min(ns[a])]
        while len(walk)<4:walk.append(next(k for k in ns[walk[-1]] if k!=walk[-2]))
        return walk+[a]
    return tri,edges,ei,perms,orbits,cycles,tri_rows,oriented,square_walk

def geometry_for_orbits(inds,G):
    tri,edges,ei,perms,orbits,cycles,tri_rows,orient,walk=G
    sq=sorted({s for i in inds for s in orbits[i]})
    rows=tri_rows+[orient(walk(s)) for s in sq]
    n=len(rows)
    face_idx={face:i for i,face in enumerate(tri)}
    sq_idx={s:45+i for i,s in enumerate(sq)}
    def action(g):
        perm=perms[IDX[g]]
        edge_dest=[ei[tuple(sorted((perm[u],perm[v])))] for u,v in edges]
        edge_sign=[1 if perm[u]<perm[v] else -1 for u,v in edges]
        fdest=[];fsign=[]
        for j,row in enumerate(rows):
            if j<45:
                destination=face_idx[tuple(sorted(perm[v] for v in tri[j]))]
            else:
                destination=sq_idx[tuple(sorted(ei[tuple(sorted(
                    (perm[edges[k][0]],perm[edges[k][1]])))] for k in sq[j-45]))]
            moved=[0]*135
            for k,x in enumerate(row):
                if x:moved[edge_dest[k]]=x*edge_sign[k]
            if moved==rows[destination]: sgn=1
            else:
                assert moved==[-x for x in rows[destination]]
                sgn=-1
            fdest.append(destination);fsign.append(sgn)
        assert sorted(fdest)==list(range(n))
        return edge_dest,edge_sign,(fdest,fsign)
    return rows, cycles, action, sq

def rank_mod(rows,p):
    return len(rank_and_basis(rows,p))

def independent_with_projection(face_rows,cycles,p):
    """Select an independent ordered basis B1 + H1 of Z1."""
    faces=independent_ordered(face_rows,p)
    r=len(faces)
    chosen=faces[:];logical=[]
    for c in cycles:
        v=[x%p for x in c]
        t=independent_ordered(chosen+[v],p)
        if len(t)>len(chosen):
            chosen.append(v);logical.append(v)
    assert len(chosen)==109 and len(logical)==109-r
    pivot={}
    for i,v in enumerate(chosen):
        w=v[:];co=[int(j==i) for j in range(109)]
        while True:
            k=next((j for j,x in enumerate(w) if x),None)
            if k is None:raise AssertionError("dependent")
            if k in pivot:
                b,c=pivot[k];f=w[k]
                w=[(a-f*z)%p for a,z in zip(w,b)]
                co=[(a-f*z)%p for a,z in zip(co,c)]
            else:
                f=pow(w[k],-1,p)
                pivot[k]=([f*x%p for x in w],[f*x%p for x in co])
                break
    def coords(v):
        w=[x%p for x in v];co=[0]*109
        while True:
            k=next((j for j,x in enumerate(w) if x),None)
            if k is None:break
            assert k in pivot
            b,c=pivot[k];f=w[k]
            w=[(a-f*z)%p for a,z in zip(w,b)]
            co=[(a+f*z)%p for a,z in zip(co,c)]
        return co[r:]
    return logical,coords

def matrix_actions(face_rows,cycles,action,p):
    r=rank_mod(face_rows,p)
    ker,free,rb=nullspace([[face_rows[j][i] for j in range(len(face_rows))]
                           for i in range(135)],p)
    assert r==rb
    logical,coords=independent_with_projection(face_rows,cycles,p)
    mats1={};mats2={}
    for g in H:
        q,sign,fact=action(g)
        def edge_act(x):
            w=[0]*135
            for k,val in enumerate(x):
                if val:w[q[k]]=val*sign[k]%p
            return w
        mats1[g]=[coords(edge_act(c)) for c in logical]
        mats2[g]=action_on_kernel(ker,free,fact,p)
    return mats1,mats2,r

def matrix_rank_minus_identity(M,p):
    return rank_mod([[(x-int(i==j))%p for j,x in enumerate(row)]
                     for i,row in enumerate(M)],p)

def radical_filtration(mats,p):
    assert p==3
    dim=len(next(iter(mats.values())))
    state=[[int(i==j) for j in range(dim)] for i in range(dim)]
    lengths=[dim]
    while state:
        out=[]
        for v in state:
            for g in GEN:
                y=apply(mats[g],v,p)
                out.append([(a-b)%p for a,b in zip(y,v)])
        state=rank_and_basis(out,p)
        assert len(state)<lengths[-1]
        lengths.append(len(state))
        assert len(lengths)<30
    return lengths

def binary_simple_decomposition(mats):
    dim=len(mats[(0,0,0)])
    def projector(subgroup):
        return [[sum(mats[g][i][j] for g in subgroup)%2
                 for j in range(dim)] for i in range(dim)]
    e=projector(H);z=projector(CENTER)
    triv=rank_mod(e,2)
    centerfixed=rank_mod(z,2)
    dirs=[]
    for a,b in LINES:
        line=[((t*a)%3,(t*b)%3,c) for t in range(3) for c in range(3)]
        M=projector(line)
        eig=rank_mod(M,2)
        assert (eig-triv)%2==0
        dirs.append((eig-triv)//2)
    assert (dim-centerfixed)%6==0
    faithful=(dim-centerfixed)//6
    assert triv+2*sum(dirs)+6*faithful==dim
    return {"trivial_multiplicity":triv,
            "four_2D_simple_multiplicities":dirs,
            "faithful_6D_simple_multiplicity":faithful}

def bockstein_rank(rows,p):
    n=len(rows)
    M=[[rows[j][i] for j in range(n)] for i in range(135)]
    ker,free,r=nullspace(M,p)
    images=[]
    for v in ker:
        y=[sum(x*t for x,t in zip(row,v)) for row in M]
        assert all(t%p==0 for t in y)
        images.append([(t//p)%p for t in y])
    rank=rank_mod(rows,p)
    image_rank=rank_mod(rows+images,p)-rank
    return {"free_relations":n-r-image_rank,
            "H2_Fp_dimension":n-r,
            "bockstein_image_dimension":image_rank,
            "H1_Fp_dimension":109-r}

def overlap_histogram(sqpair,G):
    _,_,_,_,orbits,*_=G
    a,b=sqpair
    hist=collections.Counter(len(set(x)&set(y))
                             for x in orbits[a] for y in orbits[b])
    return [hist.get(i,0) for i in range(5)]

def generator_rank_directions(mats,p):
    return [matrix_rank_minus_identity(mats[(a,b,0)],p) for a,b in LINES]

def pair_certificate():
    G=geometry_data()
    census=json.loads((ROOT/"data/w33_20261015_toe86_geometry_integral_routing.json").read_text())["orbit_pair_census"]
    torsion=json.loads((ROOT/"data/w33_20261015_toe86_pair_integral.json").read_text())["classes"]
    torsion_by_pair={tuple(c["representative"]):c for c in torsion}
    results=[]
    for entry in census["classes"]:
        pair=entry["representative"];size=entry["size"]
        rows,cycles,action,squares=geometry_for_orbits(pair,G)
        a3,b3,r3=matrix_actions(rows,cycles,action,3)
        a2,b2,r2=matrix_actions(rows,cycles,action,2)
        t=torsion_by_pair[tuple(pair)]
        assert [r2,r3]==t["ranks_F2_F3"]
        bp2=bockstein_rank(rows,2)
        bp3=bockstein_rank(rows,3)
        assert bp2["bockstein_image_dimension"]==sum(x%2==0 for x in t["nonunit_smith_factors"])
        assert bp3["bockstein_image_dimension"]==sum(x%3==0 for x in t["nonunit_smith_factors"])
        l1=generator_rank_directions(a3,3)
        l2=generator_rank_directions(b3,3)
        min1=[i for i,x in enumerate(l1) if x==min(l1)]
        min2=[i for i,x in enumerate(l2) if x==min(l2)]
        assert min1==min2 and len(min1)==1
        result={"orbit_pair":pair,"equivalence_class_size":size,
                "integral_torsion":t["nonunit_smith_factors"],
                "overlap_edge_histogram":overlap_histogram(pair,G),
                "H1":{},"H2":{},
                "Bockstein_F2":bp2,"Bockstein_F3":bp3,
                "selected_polarization_index":min1[0]}
        for name, A2,A3 in (("H1",a2,a3),("H2",b2,b3)):
            result[name]={
                "F2_semisimple":binary_simple_decomposition(A2),
                "F3_radical_filtration":radical_filtration(A3,3),
                "F3_four_direction_ranks":generator_rank_directions(A3,3),
                "F3_center_rank":matrix_rank_minus_identity(A3[(0,0,1)],3)
            }
        results.append(result)
        print("MODULE",pair,"size",size,"torsion",t["nonunit_smith_factors"],
              "Bockstein",bp2["bockstein_image_dimension"],
              bp3["bockstein_image_dimension"],
              "H1L",result["H1"]["F3_radical_filtration"],
              "H2L",result["H2"]["F3_radical_filtration"],flush=True)
    counts=collections.Counter(str(x["overlap_edge_histogram"]) for x in results)
    group=collections.defaultdict(set)
    for x in results:group[str(x["overlap_edge_histogram"])].add(str(x["integral_torsion"]))
    return {"all_468_pairs_represented":sum(x["equivalence_class_size"] for x in results),
            "classes":results,
            "shared_unique_H1_H2_polarization_class_count":sum(
                x["H1"]["F3_four_direction_ranks"].index(min(x["H1"]["F3_four_direction_ranks"]))==
                x["H2"]["F3_four_direction_ranks"].index(min(x["H2"]["F3_four_direction_ranks"]))
                for x in results),
            "overlap_signatures_ambiguous_for_torsion":{
                key:sorted(value) for key,value in group.items() if len(value)>1},
            "overlap_signature_count":len(counts)}

def triple_stress():
    G=geometry_data()
    cases=[]
    # Expand the original rank-83 two-orbit code along 12 deterministic
    # previously-unused square orbits, not a complete three-orbit census.
    for third in [i for i in range(40) if i not in (0,10)][:12]:
        inds=(0,10,third)
        rows,cycles,action,_=geometry_for_orbits(inds,G)
        a3,b3,r=matrix_actions(rows,cycles,action,3)
        if len(a3[(0,0,0)])==0:continue
        r1=generator_rank_directions(a3,3)
        r2=generator_rank_directions(b3,3)
        match=[i for i,x in enumerate(r1) if x==min(r1)]==[
            i for i,x in enumerate(r2) if x==min(r2)]
        cases.append({"orbit_triple":list(inds),"face_rank_F3":r,
                      "logical_H1_dimension_F3":109-r,
                      "H2_dimension_F3":len(rows)-r,
                      "H1_four_direction_ranks":r1,
                      "H2_four_direction_ranks":r2,
                      "matching_minimizer_sets":match})
        print("TRIPLE",third,r,match,r1,r2,flush=True)
    return {"three_orbit_cases_checked":len(cases),
            "sample_is_exhaustive":False,
            "counterexample_found":any(not x["matching_minimizer_sets"] for x in cases),
            "cases":cases}

def certificate():
    return {"status":"EXACT_MATH", "modular_pair_classification":pair_certificate(),
            "three_orbit_stress":triple_stress(),
            "interpretation":"Exact class representatives and deterministic three-orbit probes. No general cohomological polarization theorem established."}

if __name__=="__main__":
    result=certificate()
    dest=ROOT/"data/w33_20261015_toe87_modular_bockstein_triples.json"
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FROZEN",dest)
