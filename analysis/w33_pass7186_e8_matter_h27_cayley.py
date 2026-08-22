#!/usr/bin/env python3
"""Pass7186: the E8/W33 27-fibre matter graph is the repo's H27 Heisenberg Cayley graph.

Pass7183 identifies the nine-class C3 voltage with the alternating determinant
cocycle on AG(2,3).  Choosing the sign matching the repo's existing H27 model,
this pass proves the resulting 27-vertex graph is Cay(H27,{(u,0):u!=0}), computes
its full automorphism group, and verifies distance transitivity.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import w33_pass7183_c3_affine_area_cocycle as a

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7186_E8_MATTER_H27_CAYLEY.json'
F=[(x,y) for x in range(3) for y in range(3)]

def add(u,v):return ((u[0]+v[0])%3,(u[1]+v[1])%3)
def neg(u):return ((-u[0])%3,(-u[1])%3)
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
# Existing repo H27 cocycle: u2*v1 + 2*u1*v2 = -det(u,v).
def coc(u,v):return (-det(u,v))%3

def star(x,y):
    u,z=x;v,w=y
    return (add(u,v),(z+w+coc(u,v))%3)
def inv(x):
    u,z=x;return (neg(u),(-z)%3)

def gl2():
    out=[]
    for a,b,c,d in itertools.product(range(3),repeat=4):
        D=(a*d-b*c)%3
        if D:out.append(((a,b,c,d),D))
    assert len(out)==48;return out
def actA(A,u):
    a,b,c,d=A;return ((a*u[0]+b*u[1])%3,(c*u[0]+d*u[1])%3)

def main():
    C,sh,hol,hist=a.build_voltage();pts=F
    # Recover all affine-plane relabellings fixing the gauge origin, and choose one
    # whose sign is -det so it agrees literally with tools/h27_heisenberg_model.py.
    zero={frozenset(t) for t,h in hol.items() if h==0};canon=set()
    for tri in itertools.combinations(range(9),3):
        u,v,w=[pts[i] for i in tri]
        if (det(u,v)+det(v,w)+det(w,u))%3==0:canon.add(frozenset(tri))
    matches=[]
    for rest in itertools.permutations(range(1,9)):
        p=(0,)+rest
        if {frozenset(p[i] for i in L) for L in zero}!=canon:continue
        for eps in (1,2):
            if all(sh[i,j]==eps*det(pts[p[i]],pts[p[j]])%3 for i in range(9) for j in range(9) if i!=j):matches.append((p,eps))
    p,eps=next(z for z in matches if z[1]==2);assert eps==2
    # Voltage graph in canonical H27 coordinates.
    V=[(u,z) for u in F for z in range(3)];G=nx.Graph();G.add_nodes_from(V)
    for x,y in itertools.combinations(V,2):
        u,z=x;v,w=y
        if u!=v and w==(z+coc(u,v))%3:G.add_edge(x,y)
    assert G.number_of_edges()==108 and set(dict(G.degree()).values())=={8}
    # Exact Cayley law: x~y iff x^-1*y=(t,0), t!=0.
    S={(u,0) for u in F if u!=(0,0)}
    for x,y in itertools.permutations(V,2):
        assert G.has_edge(x,y)==(star(inv(x),y) in S)
    # Exhaust group axioms and Heisenberg structure.
    e=((0,0),0)
    assert all(star(e,x)==x and star(x,e)==x and star(x,inv(x))==e and star(inv(x),x)==e for x in V)
    assert all(star(star(x,y),z)==star(x,star(y,z)) for x,y,z in itertools.product(V,repeat=3))
    center=[x for x in V if all(star(x,y)==star(y,x) for y in V)];assert center==[((0,0),z) for z in range(3)]
    assert any(star(x,y)!=star(y,x) for x,y in itertools.product(V,repeat=2))
    # Distance-regular intersection array.
    arrays=set();dist_spheres=None
    for x in V:
        dx=nx.single_source_shortest_path_length(G,x);assert max(dx.values())==3
        if dist_spheres is None:dist_spheres=Counter(dx.values())
        for y in V:
            i=dx[y]
            cnum=sum(1 for z in G[y] if dx[z]==i-1) if i else 0
            anum=sum(1 for z in G[y] if dx[z]==i)
            bnum=sum(1 for z in G[y] if dx[z]==i+1) if i<3 else 0
            arrays.add((i,cnum,anum,bnum))
    by={i:(c,aa,bb) for i,c,aa,bb in arrays};assert len(by)==4
    assert by[0]==(0,0,8) and by[1]==(1,1,6) and by[2]==(3,4,1) and by[3]==(8,0,0)
    # Explicit H27 : GL(2,3) automorphisms.
    explicit=set()
    for h in V:
      for A,D in gl2():
        perm=[]
        for x in V:
            u,z=x;ax=(actA(A,u),(D*z)%3);perm.append(V.index(star(h,ax)))
        explicit.add(tuple(perm))
    assert len(explicit)==1296
    for pp in explicit:
        assert all(G.has_edge(V[i],V[j])==G.has_edge(V[pp[i]],V[pp[j]]) for i,j in itertools.combinations(range(27),2))
    # Independent full automorphism census.
    autos=list(nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter());assert len(autos)==1296
    v0=e;stab=[m for m in autos if m[v0]==v0];assert len(stab)==48
    dist=nx.single_source_shortest_path_length(G,v0);orb={}
    for d0 in (1,2,3):
        w=next(x for x in V if dist[x]==d0);orb[d0]=len({m[w] for m in stab})
    assert orb=={1:8,2:16,3:2}
    out={
      'schema':'w33.pass7186.e8_matter_h27_cayley.v1','status':'PASS',
      'vertices':27,'degree':8,'edges':108,'diameter':3,'distance_spheres_from_vertex':{str(k):v for k,v in sorted(dist_spheres.items())},
      'intersection_array':'{8,6,1;1,3,8}','spectrum':'8^1 + 2^12 + (-1)^8 + (-4)^6',
      'heisenberg_law':'(u,z)*(v,w)=(u+v,z+w-det(u,v)) over F3','center_order':3,
      'Cayley_connection':'{(u,0): u in F3^2, u != 0}','cayley_adjacency_verified_all_ordered_pairs':True,
      'full_automorphism_order':1296,'automorphism_structure':'H27 : GL(2,3)','explicit_semidirect_subgroup_order':1296,
      'vertex_stabilizer_order':48,'stabilizer_sphere_orbits':{str(k):v for k,v in orb.items()},'distance_transitive':True,
      'E8_bridge':'The 27 W33 distance-two fibres produced by the E8 C6/A2 matter decomposition carry exactly this H27 Cayley graph after the Pass7183 AG(2,3) gauge.',
      'repo_prior_art':'tools/h27_heisenberg_model.py already proves the same Cayley rule for the local W33 H27 object. The new result is the object-level identification of the E8-derived matter-fibre cover with that existing H27 model.',
      'literature_classification':'With the displayed intersection array and distance transitivity, this is the distance-transitive member of the two GQ(2,4)-minus-spread graphs on 27 vertices.',
      'physics_firewall':'H27 is the finite qutrit Heisenberg group already used by the repo; this graph identification is finite algebra/geometry and is not by itself a particle or dynamical claim.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','graph':'Cay(H27,8 horizontal generators)','Aut':1296,'distance_transitive':True}))
if __name__=='__main__':main()
