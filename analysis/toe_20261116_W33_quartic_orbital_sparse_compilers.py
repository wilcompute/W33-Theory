#!/usr/bin/env python3
"""Enumerate ALL 164 equivariant Sym4(C40)->C27 orbital operators.

The 27-line stabilizer H<=PSp4(3) has order960. By the orbit-stabilizer
correspondence, G-orbits on (quartic boson occupation, output line)
are H-orbits on the 123,410 unordered 40-mode quartets.

Every H-orbit defines a 0/1 incidence map E with identical support in
each of the 27 output rows. Exact Schläfli rank formula reveals
sparsest single-orbit full-rank quartic operators (if any), and ideal
heralding probability for the uniform coherent product input.
No optical implementation is inferred.
"""
from itertools import combinations_with_replacement
from collections import Counter,defaultdict,deque
import math,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_W33_symmetry_minimal_fourcopy import build_geometry,generators
OUT=ROOT/"data"/"toe_20261116_W33_quartic_164_orbital_sparse_compilers.json"

def compose(p,q):return tuple(p[x] for x in q)
def inverse(p):
    v=[0]*len(p)
    for i,x in enumerate(p):v[x]=i
    return tuple(v)
def closure(gens,cap=1000):
    identity=tuple(range(40))
    visited={identity};todo=deque([identity])
    while todo:
        w=todo.popleft()
        for g in gens:
            z=compose(g,w)
            if z not in visited:
                visited.add(z);todo.append(z)
                if len(visited)>cap:raise ValueError("stabilizer closure unexpectedly large")
    return visited

def run():
    geom=build_geometry();A=geom[6]
    gens=generators(geom)
    reps={0:(tuple(range(40)),tuple(range(27)))}
    todo=deque([0])
    while todo:
        i=todo.popleft();p,l=reps[i]
        for gp,gl in gens:
            new=(compose(gp,p),compose(gl,l))
            j=new[1][0]
            if j not in reps:reps[j]=new;todo.append(j)
    assert len(reps)==27
    h_candidates=set()
    for i,(p,l) in reps.items():
        for gp,gl in gens:
            j=gl[i]
            q,m=reps[j]
            hp=compose(inverse(q),compose(gp,p))
            hl=compose(inverse(m),compose(gl,l))
            assert hl[0]==0
            if hp!=tuple(range(40)):h_candidates.add(hp)
    h_gen=[]
    subgroup={tuple(range(40))}
    for g in sorted(h_candidates):
        if g in subgroup:continue
        h_gen.append(g)
        subgroup=closure(h_gen)
        if len(subgroup)==960:break
    assert len(subgroup)==960
    quads=list(combinations_with_replacement(range(40),4))
    assert len(quads)==math.comb(43,4)==123410
    qi={q:i for i,q in enumerate(quads)}
    N=len(quads);parent=list(range(N));sz=[1]*N
    def find(i):
        while i!=parent[i]:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    def union(i,j):
        i=find(i);j=find(j)
        if i==j:return
        if sz[i]<sz[j]:i,j=j,i
        parent[j]=i;sz[i]+=sz[j]
    for g in h_gen:
        for i,q in enumerate(quads):
            union(i,qi[tuple(sorted(g[x] for x in q))])
    orbits=defaultdict(list)
    for i in range(N):orbits[find(i)].append(i)
    assert len(orbits)==164
    adj_id=next(i for i in range(1,27) if A[0][i])
    nonadj_id=next(i for i in range(1,27) if not A[0][i])
    pA=reps[adj_id][0];pB=reps[nonadj_id][0]
    records=[]
    for ids in orbits.values():
        d=len(ids);O=set(ids)
        a=sum(qi[tuple(sorted(pA[x] for x in quads[i]))] in O for i in ids)
        b=sum(qi[tuple(sorted(pB[x] for x in quads[i]))] in O for i in ids)
        e1=d+10*a+16*b
        e20=d+a-2*b
        e6=d-5*a+4*b
        assert min(e1,e20,e6)>=0
        rank=1+(20 if e20 else 0)+(6 if e6 else 0)
        m=1
        for val in Counter(quads[ids[0]]).values():m*=math.factorial(val)
        product_occupation_amplitude_squared=math.factorial(4)/(40**4*m)
        p_coherent=27*d*d*product_occupation_amplitude_squared/e1
        assert 0<=p_coherent<=1+1e-9
        records.append(dict(representative_four_rails=list(quads[ids[0]]),
            occupation_multiplicities=sorted(Counter(quads[ids[0]]).values(),reverse=True),
            support_per_output=d,adjacent_overlap=a,nonadjacent_overlap=b,
            gram_eigenvalues_1_20_6=[e1,e20,e6],output_rank=rank,
            exact_optimal_K_scale="1/sqrt("+str(e1)+")",
            uniform_identical_fourcopy_heralding_probability=p_coherent))
    hist=Counter(r["output_rank"] for r in records)
    full=sorted((r for r in records if r["output_rank"]==27),
                key=lambda r:(r["support_per_output"],-r["uniform_identical_fourcopy_heralding_probability"]))
    assert full
    maximal=max(full,key=lambda r:r["uniform_identical_fourcopy_heralding_probability"])
    minimal=full[0]
    # Independent exact 27x27 Gram verification for BOTH preferred maps.
    for chosen in (minimal,maximal):
        target=next(v for v in orbits.values() if list(quads[v[0]])==chosen["representative_four_rails"])
        rows=[]
        for j in range(27):
            gj=reps[j][0]
            rows.append({qi[tuple(sorted(gj[x] for x in quads[i]))] for i in target})
        assert all(len(x)==chosen["support_per_output"] for x in rows)
        for i in range(27):
            for j in range(i,27):
                t=len(rows[i]&rows[j])
                expected=chosen["support_per_output"] if i==j else (
                    chosen["adjacent_overlap"] if A[i][j] else chosen["nonadjacent_overlap"])
                assert t==expected
    assert minimal["support_per_output"]==60
    assert minimal["gram_eigenvalues_1_20_6"]==[60,60,60]
    assert maximal["support_per_output"]==960
    assert maximal["gram_eigenvalues_1_20_6"]==[960,960,960]
    assert abs(maximal["uniform_identical_fourcopy_heralding_probability"]-.243)<1e-14
    result={
      "status":"EXACT_PSP43_QUARTIC_ORBITAL_SPARSE_COMPILER_CENSUS",
      "PSp4_order":25920,"output_stabilizer_order":960,
      "independent_stabilizer_generators":len(h_gen),
      "full_sym4_input_dimension":N,
      "total_output_line_orbits":len(orbits),
      "orbital_rank_histogram":{str(k):v for k,v in sorted(hist.items())},
      "full_rank_27_orbit_count":len(full),
      "sparsest_full_rank_orbital":minimal,
      "best_uniform_product_heralding_orbital":maximal,
      "sparsest_and_best_uniform_exact_27x27_Gram_verified":True,
      "sparsest_uniform_product_success_exact":"243/16000",
      "best_uniform_product_success_exact":"243/1000",
      "both_preferred_orbitals_are_coisometries":True,
      "top_20_sparsest_full_rank_orbitals":full[:20],
      "all_164_orbital_summaries":records,
      "orbit_completeness_check":"For transitive output action, Hom_G(Sym4 V,C27) dimension equals number of stabilizer H-orbits on Sym4 input; exact Molien independently found 164.",
      "scope":"Full-rank equivariant integer/binary orbital Kraus maps, canonically rescaled by exact top singular value. No compact quantum circuit or physical 4-photon success implementation inferred. Uniform-product probabilities are ideal normalized abstract Kraus success probabilities."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    d=run()
    print("PASS",d["status"],"full_rank",d["full_rank_27_orbit_count"],
          "sparsest",d["sparsest_full_rank_orbital"]["support_per_output"],
          "p_uniform",d["sparsest_full_rank_orbital"]["uniform_identical_fourcopy_heralding_probability"],flush=True)
