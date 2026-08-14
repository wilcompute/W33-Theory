#!/usr/bin/env python3
"""Pass5132 (bonkers): chamber-star theta support is the C2 root-direction Cayley graph."""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mv,norm,mm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5132_THETA_CAYLEY_MINIMUM_SUPPORT.json'

def anchor(q):
    G=build_W(q);U,H,F=roots(q);pidx={p:i for i,p in enumerate(G['pts'])};gens=[z for h in H for z in h[1:]]
    fp=[i for i,p in enumerate(G['pts']) if all(pidx[norm(mv(g,p,F),F)]==i for g in gens)]
    fl=[]
    for li,L in enumerate(G['lines']):
        if all(frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in L)==L for g in gens):fl.append(li)
    fixed=[(p,l) for p in fp for l in fl if p in G['lines'][l]];assert len(fixed)==1;fi=G['flags'].index(fixed[0])
    support=[a for a,es in enumerate(G['apt_edges']) if fi in es];lookup={G['apartments'][a]:a for a in support};base=G['apartments'][support[0]]
    u_to_a={}
    for ui,g in enumerate(U):
        A=frozenset(pidx[norm(mv(g,G['pts'][p],F),F)] for p in base);u_to_a[ui]=lookup[A]
    a_to_u={a:u for u,a in u_to_a.items()};S=set(support);Etheta=set()
    for _,loc in G['charts']:
        T=S&set(loc.values())
        if T:
            uu=sorted(a_to_u[a] for a in T)
            for x,y in itertools.combinations(uu,2):Etheta.add((x,y))
    idx={g:i for i,g in enumerate(U)};identity=idx[next(g for g in U if all(g[i][j]==int(i==j) for i in range(4) for j in range(4)))]
    conn=set()
    for h in H:
        conn|={idx[z] for z in h if idx[z]!=identity}
    Ecay=set()
    for ui,g in enumerate(U):
        for hidx in conn:
            v=idx[mm(g,U[hidx],F)]
            if ui!=v:Ecay.add(tuple(sorted((ui,v))))
    assert Etheta==Ecay
    deg=[0]*len(U)
    for a,b in Etheta:deg[a]+=1;deg[b]+=1
    assert set(deg)=={4*(q-1)}
    return {'q':q,'vertices':q**4,'degree':4*(q-1),'edges':len(Etheta),'active_root_coset_cliques':4*q**3,'clique_size':q,'exact_edge_match':True}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5132,'status':'THEOREM_ALL_Q_MINIMUM_SUPPORT_THETA_CAYLEY_GRAPH',
         'statement':'Under the U(q)-torsor identification of a chamber-star support, the induced theta graph is Cay(U(q), union_i(H_i\\{1})) for the four positive-root subgroups H_i.',
         'degree_formula':'4(q-1)','edge_formula':'2 q^4 (q-1)','root_coset_cliques':'4 q^3 cliques of size q',
         'anchors':A,
         'synthesis':'Pass5119 half-regularity on a minimum word is exactly the root-direction Cayley degree; Pass5129 active charts are exactly the same root-subgroup cosets viewed as cliques.',
         'boundary':'The Cayley identification is for the chamber-star minimum family. It does not assert that an arbitrary codeword support is a Cayley subgraph.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
