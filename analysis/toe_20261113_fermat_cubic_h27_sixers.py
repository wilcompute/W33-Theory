#!/usr/bin/env python3
"""Independent exact Fermat cubic line geometry (not a lookup of 18/54).

Construct all 27 Fermat x0^3+x1^3+x2^3+x3^3=0 lines as three
coordinate pairings times omega phases (3x3), test intersections via
integer Z[omega] 4x4 determinants, identify with canonical E6 45-term
tritangent graph, enumerate sixers and their 648-element Fermat
automorphism action (diagonal 3^3 semidirect S4).
"""
from pathlib import Path
from collections import Counter
from itertools import product,permutations,combinations
import json
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_fermat_cubic_h27_sixers.json"
PAIRINGS=(((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))
OMEGA=((1,0),(0,1),(-1,-1))
Z=(0,0)
ONE=(1,0)
def add(u,v):return (u[0]+v[0],u[1]+v[1])
def mul(u,v):return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0]-u[1]*v[1])
def neg(u):return (-u[0],-u[1])
def det4(A):
    ans=Z
    for p in permutations(range(4)):
        sign=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        val=ONE
        for i in range(4):
            val=mul(val,A[i][p[i]])
            if val==Z:break
        if sign==-1:val=neg(val)
        ans=add(ans,val)
    return ans
def line_rows(b,p,q):
    rows=[]
    for (i,j),exp in zip(PAIRINGS[b],(p,q)):
        v=[Z]*4
        v[i]=ONE;v[j]=OMEGA[exp]
        rows.append(tuple(v))
    return rows
def identifier(b,p,q):return 9*b+3*p+q
def decompose(i):return i//9,(i%9)//3,i%3
def geometry():
    Fermat=nx.Graph()
    Fermat.add_nodes_from(range(27))
    for a,b in combinations(range(27),2):
        am=line_rows(*decompose(a));bm=line_rows(*decompose(b))
        if det4(am+bm)==Z:Fermat.add_edge(a,b)
    assert Fermat.number_of_edges()==135
    assert set(dict(Fermat.degree()).values())=={10}
    for a,b in combinations(range(27),2):
        both=len(set(Fermat.neighbors(a))&set(Fermat.neighbors(b)))
        assert both==(1 if Fermat.has_edge(a,b) else 5)
    return Fermat

def original():
    can=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text(encoding="utf-8"))
    bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text(encoding="utf-8"))
    eh={int(i):tuple(map(int,v)) for i,v in bridge["maps"]["e6id_to_current_H27_address"].items()}
    triples=[tuple(sorted(map(int,v["triple"]))) for v in can["solution"]["d_triples"]]
    assert len(triples)==45
    C=nx.Graph()
    C.add_nodes_from(range(27))
    for x in triples:C.add_edges_from(combinations(x,2))
    assert C.number_of_edges()==135
    return C,eh,triples

def permute_line(line,sigma):
    b,p,q=decompose(line)
    transformed={}
    for pair,phase in zip(PAIRINGS[b],(p,q)):
        i,j=pair
        x,y=sigma[i],sigma[j]
        if x<y:transformed[(x,y)]=phase
        else:transformed[(y,x)]=(-phase)%3
    key=frozenset(transformed)
    target=next(k for k,arr in enumerate(PAIRINGS) if frozenset(arr)==key)
    pnew,qnew=[transformed[pair] for pair in PAIRINGS[target]]
    return identifier(target,pnew,qnew)
def phase_shift(line,diagonal):
    b,p,q=decompose(line)
    (i,j),(k,l)=PAIRINGS[b]
    return identifier(b,(p+diagonal[i]-diagonal[j])%3,
                      (q+diagonal[k]-diagonal[l])%3)
def automorphisms(Fermat):
    line_perms={}
    # All (Z3)^3 x S4: apply diagonal first then permute coordinates
    for d1,d2,d3 in product(range(3),repeat=3):
        diag=(0,d1,d2,d3)
        for sigma in permutations(range(4)):
            perm=tuple(permute_line(phase_shift(i,diag),sigma) for i in range(27))
            assert len(set(perm))==27
            # Strong independent automorphism control, actual intersections.
            assert all(Fermat.has_edge(i,j)==Fermat.has_edge(perm[i],perm[j])
                       for i,j in combinations(range(27),2))
            line_perms[perm]=1
    assert len(line_perms)==648,len(line_perms)
    return list(line_perms)

def section_orbits(sections,perms):
    seq=[frozenset(x) for x in sections]
    ids={s:i for i,s in enumerate(seq)}
    assert len(ids)==72
    remaining=set(range(72))
    parts=[]
    while remaining:
        i=min(remaining)
        orb={ids[frozenset(perm[x] for x in seq[i])] for perm in perms}
        assert orb<=remaining
        remaining-=orb
        parts.append(sorted(orb))
    parts=sorted(parts,key=len)
    assert [len(v) for v in parts]==[18,54],[len(v) for v in parts]
    return parts

def main():
    F=geometry()
    C,eh,tri=original()
    def colors(a,b):return a["b"]==b["b"]
    for i in F.nodes():F.nodes[i]["b"]=i//9
    for i in C.nodes():C.nodes[i]["b"]=eh[i][1]
    iso=nx.algorithms.isomorphism.GraphMatcher(C,F,node_match=colors)
    assert iso.is_isomorphic(),"Not compatible preserving H27 b-sector decomposition"
    mapping=next(iso.isomorphisms_iter())
    assert all(mapping[i]//9==eh[i][1] for i in range(27))
    fer_tris={tuple(sorted(mapping[i] for i in tr)) for tr in tri}
    assert len(fer_tris)==45
    assert all(all(F.has_edge(i,j) for i,j in combinations(tr,2)) for tr in fer_tris)
    assert len({tuple(sorted(c)) for c in nx.enumerate_all_cliques(F) if len(c)==3})==45
    sections=sorted(tuple(sorted(c)) for c in nx.find_cliques(nx.complement(F)) if len(c)==6)
    assert len(sections)==72
    perms=automorphisms(F)
    parts=section_orbits(sections,perms)
    profile=Counter(tuple(sorted(sum(i//9==b for i in sec) for b in range(3))) for sec in sections)
    assert profile==Counter({(0,3,3):18,(2,2,2):54})
    orbit_profile=Counter()
    for orb in parts:
        ps={tuple(sorted(sum(i//9==b for i in sections[t]) for b in range(3))) for t in orb}
        assert len(ps)==1,ps
        orbit_profile[tuple([len(orb),next(iter(ps))])]+=1
    assert orbit_profile==Counter({(18,(0,3,3)):1,(54,(2,2,2)):1}),orbit_profile
    result={
      "schema":"toe.fermat.cubic.h27_27_lines_72_sixers.v1",
      "status":"PASS_EXACT_FERMAT_LINE_MODEL_AND_H27_SIXER_ORBIT_ALIGNMENT",
      "fermat_equation":"x0^3+x1^3+x2^3+x3^3=0",
      "line_description":"Three disjoint pairings of four homogeneous coordinates; each paired equation x_i+omega^p x_j=0; p,q in F3",
      "line_count":27,
      "intersection_test":"determinant of 4x4 stacked plane constraints exactly zero in Z[omega]",
      "intersection_graph":"SRG(27,10,1,5)",
      "canonical_E6_45_triple_graph_isomorphic":True,
      "iso_preserves_three_b_sectors":True,
      "E6_index_to_Fermat_line_id":{str(i):int(mapping[i]) for i in range(27)},
      "E6_index_to_Fermat_bpq":{str(i):list(decompose(mapping[i])) for i in range(27)},
      "all_45_tritangent_triangles_identified":True,
      "fermat_linear_automorphism_group_order":len(perms),
      "fermat_automorphism_generators":"27 distinct diagonal omega-scalings fixing d0=0 times all 24 coordinate permutations",
      "sixers_count":len(sections),
      "sixer_orbit_sizes":[len(x) for x in parts],
      "orbit_alignment_with_b_populations":{str(k):v for k,v in sorted(orbit_profile.items())},
      "sixers_all_27_line_ids":[list(c) for c in sections],
      "sixer_orbits_indices":parts,
      "literature":"Favacchio-Malara 2026 arXiv:2608.23716 independently finds the 18+54 Fermat sixer orbit split. Current calculation obtains this by exact 27 line equations and all 648 explicit automorphisms.",
      "scope":"Exact finite cubic-surface geometry and unsigned 45-triple incidence isomorphism. Does NOT mean the H27 right translation representation is the Fermat surface automorphism group or that the 27 spacetime physical coordinates of ExFT are given by these lines."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:result[k] for k in ["status","fermat_linear_automorphism_group_order","sixer_orbit_sizes","orbit_alignment_with_b_populations"]},indent=2),flush=True)
    return result
if __name__=="__main__":main()
