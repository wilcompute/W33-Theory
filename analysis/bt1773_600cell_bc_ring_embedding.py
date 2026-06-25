#!/usr/bin/env python3
"""BT1773: generate 600-cell facets and find a 30-facet BC-ring candidate."""
from __future__ import annotations
import itertools,json,math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1773_600cell_bc_ring_embedding.json'
def parity(p):
    return sum(1 for i in range(len(p)) for j in range(i+1,len(p)) if p[i]>p[j])%2
def vertices():
    phi=(1+5**0.5)/2; V=[]
    for i in range(4):
        for s in (1,-1):
            v=[0.0]*4; v[i]=s; V.append(tuple(v))
    for signs in itertools.product((0.5,-0.5), repeat=4): V.append(tuple(signs))
    base=[0,0.5,phi/2,1/(2*phi)]
    for perm in itertools.permutations(range(4)):
        if parity(perm)==0:
            arr=[base[i] for i in perm]; nz=[i for i,a in enumerate(arr) if abs(a)>1e-12]
            for signs in itertools.product((1,-1), repeat=3):
                v=list(arr)
                for i,s in zip(nz,signs): v[i]*=s
                V.append(tuple(round(x,12) for x in v))
    return list(dict.fromkeys(V))
def dist2(a,b): return sum((a[i]-b[i])**2 for i in range(4))
def main():
    V=vertices(); n=len(V); ds=sorted(set(round(dist2(V[i],V[j]),10) for i,j in itertools.combinations(range(n),2))); edge=ds[0]
    E={(i,j) for i,j in itertools.combinations(range(n),2) if abs(dist2(V[i],V[j])-edge)<1e-8}
    nbr={i:set() for i in range(n)}
    for i,j in E: nbr[i].add(j); nbr[j].add(i)
    facets=[]
    for a,b,c,d in itertools.combinations(range(n),4):
        if all((min(x,y),max(x,y)) in E for x,y in itertools.combinations((a,b,c,d),2)): facets.append((a,b,c,d))
    face_map=defaultdict(list)
    for fi,f in enumerate(facets):
        for face in itertools.combinations(f,3): face_map[tuple(sorted(face))].append(fi)
    dual={i:set() for i in range(len(facets))}
    for fs in face_map.values():
        if len(fs)==2:
            a,b=fs; dual[a].add(b); dual[b].add(a)
    # deterministic length-30 dual cycle from facet 0
    target=30; path=[0]; seen={0}; cycle=None
    def dfs(v):
        nonlocal cycle
        if cycle is not None: return True
        if len(path)==target:
            if 0 in dual[v]: cycle=path.copy(); return True
            return False
        for w in sorted(dual[v]):
            if w in seen: continue
            seen.add(w); path.append(w)
            if dfs(w): return True
            path.pop(); seen.remove(w)
        return False
    dfs(0)
    checks={'vertices_120':n==120,'edges_720':len(E)==720,'facets_600':len(facets)==600,'dual_4_regular':all(len(v)==4 for v in dual.values()),'found_30_cycle':cycle is not None and len(cycle)==30,'cycle_face_adjacent':cycle is not None and all(cycle[(i+1)%30] in dual[cycle[i]] for i in range(30))}
    payload={'theorem':'BT1773 600-cell BC-Ring Embedding Candidate','verified':all(checks.values()),'summary':'The full standard 600-cell vertex set is generated, its 720 edges and 600 tetrahedral facets are recovered as edge-cliques, and the facet-dual graph is 4-regular. A deterministic 30-cycle of face-adjacent tetrahedral facets is found in the dual graph. This is the first actual 600-cell facet-level BC-ring candidate for the 30 selector completions.', 'counts':{'vertices':n,'edges':len(E),'facets':len(facets),'dual_edges':sum(len(v) for v in dual.values())//2},'facet_cycle_30':cycle,'facet_cycle_vertices':[facets[i] for i in cycle] if cycle else [],'checks':checks,'boundary':'A 30-facet face-adjacent ring is found in the 600-cell. The next check is matching the BT1767 three-strand/triangle-cross-section completion graph to this specific facet cycle, not merely to a 30-cycle.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'counts':payload['counts']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
