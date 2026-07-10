#!/usr/bin/env python3
"""Exact native W(E6) runtime map to 27 lines, 45 tritangents, 72 roots, and 540 pair fibers."""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json

import networkx as nx

from w33_levi_next5_v3_common import (
    apply_cols, build_w33, compose_cols, compose_perm, dot2, group_closure_cols,
    homology_action, invariant_linear_span, line_perm_from_point_perm,
    point_outer_perm, point_transvection_perm, restrict_action,
    sha256_json, weight_q,
)

SEEDS=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
       (1,1,0,0),(1,0,1,0),(0,1,0,1),(1,1,1,1)]


def classical_lines():
    labels=[f"E{i}" for i in range(6)]
    labels += [f"L{i}{j}" for i,j in combinations(range(6),2)]
    labels += [f"Q{i}" for i in range(6)]
    def kind(s): return s[0]
    def ints(a,b):
        if a==b:return False
        ka,kb=kind(a),kind(b)
        if ka=='E' and kb=='E':return False
        if ka=='Q' and kb=='Q':return False
        if ka=='E' and kb=='L': return int(a[1]) in {int(b[1]),int(b[2])}
        if ka=='L' and kb=='E': return ints(b,a)
        if ka=='E' and kb=='Q': return int(a[1]) != int(b[1])
        if ka=='Q' and kb=='E': return ints(b,a)
        if ka=='L' and kb=='L':
            return not ({int(a[1]),int(a[2])} & {int(b[1]),int(b[2])})
        if ka=='L' and kb=='Q': return int(b[1]) in {int(a[1]),int(a[2])}
        if ka=='Q' and kb=='L': return ints(b,a)
        raise AssertionError((a,b))
    G=nx.Graph(); G.add_nodes_from(range(27))
    for i,j in combinations(range(27),2):
        if ints(labels[i],labels[j]):G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={10}
    return labels,G


def build_module():
    geom=build_w33()
    pgens=[point_transvection_perm(geom.points,v) for v in SEEDS]
    outerp=point_outer_perm(geom.points)
    lgens=[line_perm_from_point_perm(geom.lines,p) for p in pgens]
    outerl=line_perm_from_point_perm(geom.lines,outerp)
    _,hom,acts=homology_action(geom.line_adjacency,lgens+[outerl])
    u6=invariant_linear_span(0x3D7,acts[:-1])
    assert len(u6)==6
    racts=restrict_action(acts,u6)
    def ambient_h(c):
        out=0
        for i,rep in enumerate(hom):
            if (c>>i)&1:out^=rep
        return out
    def ambient6(v):
        c=0
        for i,b in enumerate(u6):
            if (v>>i)&1:c^=b
        return ambient_h(c)
    singular=[v for v in range(1,64) if weight_q(ambient6(v))==0]
    assert len(singular)==27
    sindex={v:i for i,v in enumerate(singular)}
    line_perms=[tuple(sindex[apply_cols(a,v)] for v in singular) for a in racts]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in combinations(range(27),2):
        if dot2(ambient6(singular[i]),ambient6(singular[j]))==0:G.add_edge(i,j)
    assert set(dict(G.degree()).values())=={10}
    labels,CG=classical_lines()
    matcher=nx.algorithms.isomorphism.GraphMatcher(G,CG)
    mapping=next(matcher.isomorphisms_iter())
    named=[None]*27
    for s,c in mapping.items():named[s]=labels[c]
    return geom,pgens,outerp,racts,line_perms,G,named,singular


def object_sets(G):
    triangles=[tuple(c) for c in combinations(range(27),3) if G.has_edge(c[0],c[1]) and G.has_edge(c[0],c[2]) and G.has_edge(c[1],c[2])]
    assert len(triangles)==45
    sixes=[tuple(c) for c in combinations(range(27),6) if all(not G.has_edge(i,j) for i,j in combinations(c,2))]
    assert len(sixes)==72
    antipode={}
    for i,S in enumerate(sixes):
        Sset=set(S); candidates=[]
        for j,T in enumerate(sixes):
            if i==j or Sset & set(T):continue
            degrees=[sum(G.has_edge(x,y) for y in T) for x in S]
            degrees2=[sum(G.has_edge(x,y) for x in S) for y in T]
            if degrees==[5]*6 and degrees2==[5]*6:candidates.append(j)
        assert len(candidates)==1
        antipode[i]=candidates[0]
    assert all(antipode[antipode[i]]==i for i in antipode)
    return triangles,sixes,antipode


def set_action_perm(lineperm, objects):
    idx={frozenset(x):i for i,x in enumerate(objects)}
    return tuple(idx[frozenset(lineperm[x] for x in obj)] for obj in objects)


def paired_psp_closure(pgens,m6gens):
    e6=tuple(1<<i for i in range(6)); ep=tuple(range(40))
    seen={e6:ep};q=deque([(e6,ep)])
    while q:
        a,p=q.popleft()
        for ga,gp in zip(m6gens,pgens):
            na=compose_cols(ga,a);np=compose_perm(gp,p)
            if na not in seen:
                seen[na]=np;q.append((na,np))
            else: assert seen[na]==np
    assert len(seen)==25920
    return seen


def analyze():
    geom,pgens,outerp,racts,lineperms,G,names,singular=build_module()
    m6gens=racts[:-1]; outer6=racts[-1]
    assert len(group_closure_cols(m6gens,6,25920))==25920
    assert len(group_closure_cols(racts,6,51840))==51840
    triangles,sixes,antipode=object_sets(G)
    tri_perms=[set_action_perm(p,triangles) for p in lineperms]
    six_perms=[set_action_perm(p,sixes) for p in lineperms]
    paired=paired_psp_closure(pgens,m6gens)
    pair_objects=[(i,j) for i,j in combinations(range(40),2) if not geom.adjacency[i,j]]
    assert len(pair_objects)==540
    pair_idx={frozenset(x):i for i,x in enumerate(pair_objects)}
    base_line=0;base_tri=0;base_six=0;base_pair=pair_objects[0]
    line_count=Counter();tri_count=Counter();root_count=Counter();pair_count=Counter();sheet_pair=Counter()
    runtime_digest=[]
    tri_index={frozenset(x):i for i,x in enumerate(triangles)}
    six_index={frozenset(x):i for i,x in enumerate(sixes)}
    singular_index={v:i for i,v in enumerate(singular)}
    for chirality in (0,1):
        for a,p in paired.items():
            aa=compose_cols(outer6,a) if chirality else a
            pp=compose_perm(outerp,p) if chirality else p
            lp=tuple(singular_index[apply_cols(aa,v)] for v in singular)
            li=lp[base_line]
            ti=tri_index[frozenset(lp[x] for x in triangles[base_tri])]
            ri=six_index[frozenset(lp[x] for x in sixes[base_six])]
            pi=pair_idx[frozenset(pp[x] for x in base_pair)]
            line_count[li]+=1;tri_count[ti]+=1;root_count[ri]+=1;pair_count[pi]+=1;sheet_pair[(chirality,pi)]+=1
            runtime_digest.append((chirality,li,ti,ri,pi))
    checks={
      'classical_labeling':len(set(names))==27,
      'tritangents_45':len(triangles)==45,
      'oriented_double_sixes_roots_72':len(sixes)==72 and len(set(antipode.values()))==72,
      'native_group_51840':len(group_closure_cols(racts,6))==51840,
      'line_fibers_1920':set(line_count.values())=={1920},
      'tritangent_fibers_1152':set(tri_count.values())=={1152},
      'root_fibers_720':set(root_count.values())=={720},
      'pair_fibers_96':set(pair_count.values())=={96},
      'middleware_48_per_chirality':set(sheet_pair.values())=={48},
    }
    return {
      'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'group':{'PSp43':25920,'WE6':51840,'degree27_image':51840},
      'objects':{'lines':27,'tritangent_planes':45,'oriented_double_sixes_E6_roots':72,'double_sixes':36,'noncollinear_W33_pairs':540},
      'fiber_sizes':{'runtime_to_line':1920,'runtime_to_tritangent':1152,'runtime_to_root':720,'runtime_to_pair':96,'chirality_pair_to_middleware':48},
      'classical_labels_by_singular_index':names,
      'root_antipode_pairs':sorted({tuple(sorted((i,j))) for i,j in antipode.items()}),
      'generator_digests':{'line27':sha256_json(lineperms),'tritangent45':sha256_json(tri_perms),'root72':sha256_json(six_perms)},
      'runtime_coordinate_digest':sha256_json(runtime_digest),
      'theorem':'The same native generators act on U6- singular vectors as W(E6) on the 27 cubic-surface lines; regular runtime states map equivariantly to 27,45,72,540 with fibers 1920,1152,720,96 and chirality-resolved middleware fibers 48.'
    }


def main():
    out=analyze(); print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
