#!/usr/bin/env python3
"""Exact PSp4(3)-equivariant quantum-map minimal-degree theorem.

For d<=3 enumerate ALL G-orbits in Sym^d(40 point modes) x 27 cubic
line labels. An equivariant complex-linear map is an arbitrary complex
combination of orbit incidence maps. Each annihilates the six-dimensional
Schlafli space. The earlier quartic map has full rank27, so degree4 is
minimal WITHIN THIS EQUIVARIANT SYMMETRIC-POWER ARCHITECTURE.
No scipy/numpy/networkx dependencies.
"""
from collections import defaultdict,deque
from itertools import product,combinations,combinations_with_replacement
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_W33_symmetry_minimal_fourcopy.json"

def norm(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:return tuple(y*(1 if x==1 else 2)%3 for y in v)
    raise ValueError("zero")
def symp(a,b):
    return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3

def build_geometry():
    pts=sorted({norm(v) for v in product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    idx={v:i for i,v in enumerate(pts)}
    adj=[[i!=j and symp(a,b)==0 for j,b in enumerate(pts)]
         for i,a in enumerate(pts)]
    assert all(sum(row)==12 for row in adj)
    octets=set()
    for a in combinations(range(40),4):
        if any(adj[i][j] for i,j in combinations(a,2)):continue
        nbr=[j for j in range(40) if all(adj[i][j] for i in a)]
        if len(nbr)==4 and all(not adj[i][j] for i,j in combinations(nbr,2)):
            octets.add(frozenset((*a,*nbr)))
    S=sorted(octets,key=lambda x:tuple(sorted(x)))
    assert len(S)==45 and all(len(s)==8 for s in S)
    SI={s:i for i,s in enumerate(S)}
    neighbors=[set() for _ in S]
    for i,j in combinations(range(45),2):
        if S[i].isdisjoint(S[j]):
            neighbors[i].add(j);neighbors[j].add(i)
    assert all(len(x)==12 for x in neighbors)
    cliques=[]
    def extend(prefix,remaining):
        if len(prefix)==5:
            cliques.append(tuple(prefix));return
        for k,x in enumerate(remaining):
            extend([*prefix,x],[y for y in remaining[k+1:] if y in neighbors[x]])
    extend([],list(range(45)))
    assert len(cliques)==27 and all(len(x)==5 for x in cliques)
    LI={frozenset(x):i for i,x in enumerate(cliques)}
    A=[[int(i!=j and len(set(a)&set(b))==1) for j,b in enumerate(cliques)]
       for i,a in enumerate(cliques)]
    assert all(sum(row)==10 for row in A)
    return pts,idx,S,SI,cliques,LI,A,adj

def generators(geometry):
    pts,idx,S,SI,cliques,LI,A,adj=geometry
    axes=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]
    gens=[]
    for v in axes:
        pp=tuple(idx[norm(tuple(p[k]+symp(p,v)*v[k] for k in range(4)))]
                 for p in pts)
        assert len(set(pp))==40
        op=tuple(SI[frozenset(pp[k] for k in s)] for s in S)
        assert len(set(op))==45
        lp=tuple(LI[frozenset(op[k] for k in line)] for line in cliques)
        assert len(set(lp))==27
        assert all(A[i][j]==A[lp[i]][lp[j]]
                   for i in range(27) for j in range(27))
        gens.append((pp,lp))
    seen={tuple(range(40))}
    todo=deque(seen)
    while todo:
        p=todo.popleft()
        for pp,lp in gens:
            nxt=tuple(pp[x] for x in p)
            if nxt not in seen:
                seen.add(nxt);todo.append(nxt)
    assert len(seen)==25920
    return gens

def degree_orbits(d,gens,A):
    inputs=list(combinations_with_replacement(range(40),d))
    ix={c:i for i,c in enumerate(inputs)}
    n=27*len(inputs)
    parent=list(range(n));size=[1]*n
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(a,b):
        a=find(a);b=find(b)
        if a==b:return
        if size[a]<size[b]:a,b=b,a
        parent[b]=a;size[a]+=size[b]
    for pp,lp in gens:
        mapping=[ix[tuple(sorted(pp[j] for j in c))] for c in inputs]
        for k,k2 in enumerate(mapping):
            base,other=27*k,27*k2
            for l in range(27):union(base+l,other+lp[l])
    orbits=defaultdict(list)
    for k in range(n):orbits[find(k)].append(k)
    results=[]
    for orb in sorted(orbits.values(),key=len,reverse=True):
        rows=[set() for _ in range(27)]
        for slot in orb:
            k,l=divmod(slot,27);rows[l].add(k)
        diagonal=len(rows[0])
        adjacent=next(len(rows[i]&rows[j]) for i in range(27)
                      for j in range(i+1,27) if A[i][j])
        nonadjacent=next(len(rows[i]&rows[j]) for i in range(27)
                         for j in range(i+1,27) if not A[i][j])
        for i in range(27):
            assert len(rows[i])==diagonal
            for j in range(i+1,27):
                assert len(rows[i]&rows[j])==(adjacent if A[i][j] else nonadjacent)
        eig=(diagonal+10*adjacent+16*nonadjacent,
             diagonal+adjacent-2*nonadjacent,
             diagonal-5*adjacent+4*nonadjacent)
        assert eig[2]==0 and eig[0]>0 and eig[1]>=0
        results.append(dict(orbit_size=len(orb),
                    gram_diagonal=diagonal,gram_adjacent=adjacent,
                    gram_nonadjacent=nonadjacent,
                    eigenvalues_1_20_6=list(eig),
                    rank=(1 if eig[0] else 0)+(20 if eig[1] else 0)))
    assert sum(r["orbit_size"] for r in results)==n
    return dict(degree=d,domain_dimension=len(inputs),joint_pairs=n,
                orbit_count=len(results),max_orbital_rank=max(r["rank"] for r in results),
                orbit_sizes=[r["orbit_size"] for r in results],
                orbit_Gram_certificates=results)

def run():
    g=build_geometry()
    gen=generators(g)
    levels=[degree_orbits(d,gen,g[6]) for d in (1,2,3)]
    assert [(x["orbit_count"],x["max_orbital_rank"]) for x in levels]==[(1,1),(5,21),(19,21)]
    prior=json.loads((ROOT/"data"/"toe_20261115_full_equivariant_fourcopy_quantum_channel.json").read_text())
    assert prior["rank_output"]==27 and prior["all_40_symplectic_transvections_covariant"]
    assert prior["exact_Gram_eigenvalues_mult"]["schlafli_dark_6"]==1560
    result=dict(status="EXACT_PSP4_3_SYMMETRIC_POWER_MINIMAL_DEGREE_FOUR",
         group_order=25920,group_generators=5,
         W33_points=40,W33_induced_K44_octets=45,
         E6_cubic_lines=27,E6_Schlafli_permutation_representation="1+20+6",
         degrees_leq_three=levels,
         zero_six_dimensional_sector_for_all_orbit_matrices=True,
         quartic_witness_rank=prior["rank_output"],
         minimum_copy_number_with_full_27_output=4,
         theorem="All G-equivariant complex-linear maps Sym^d(C40)->C27 for d=0,1,2,3 kill the Schläfli six-sector. Proof: 1/5/19 orbit indicator matrices span Hom_G for d=1/2/3 and each has six-sector eigenvalue zero in MM^T. Existing covariant d=4 map has rank27.",
         scope="The theorem assumes the same finite PSp4(3) action on the 40 point modes and 27 cubic-line modes and symmetric boson tensor powers; non-equivariant, ancilla-extended or different target representations may evade it. It does not establish a physical four-photon circuit.")
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result

if __name__=="__main__":
    d=run()
    print("PASS",d["status"],[(x["degree"],x["orbit_count"]) for x in d["degrees_leq_three"]],flush=True)
