#!/usr/bin/env python3
"""Pass 4764 -- local geometry of the 36 support-12 minima inside one protected rook grid.

Each of the 45 Pass4762 grids contains exactly 36 thickenings.  The eight maximal
K4s of the rook graph split into two disjoint four-clique families.  The complement
of a thickening inside the 16-line grid is a 2x2 rectangle, hence the 36 minima are
canonically C(4,2) x C(4,2).  The overlap-8 partner is simultaneous complement in
both duad coordinates.

The full PGSp grid stabilizer has order 1152 and PSp stabilizer 576.  Both have a
pointwise kernel C2 on the 16 grid lines, so their induced 36-rectangle actions
have orders 576 and 288 and are transitive.  The canonical partner involution is
not induced by either group but centralizes the PGSp image; adjoining it doubles
the 36-set action to order 1152.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,perm_group,transvection_matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4764_ROOK36_RECTANGLE_PARTNER_ACTION.json'

def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))

def main()->int:
    pts,pidx,lines,lidx,_,A,_,apartments,_=build_geometry();A=np.asarray(A,dtype=np.uint8)
    through=[set() for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:through[p].add(li)
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];eidx={e:k for k,e in enumerate(edges)}
    th=[];em=[]
    for ap in apartments:
        corners=set()
        for i,j in itertools.combinations(ap,2):
            z=lines[i]&lines[j]
            if z:corners|=set(z)
        T=set()
        for p in corners:T|=through[p]
        T=frozenset(T);th.append(T);m=0
        for i,j in itertools.combinations(sorted(T),2):
            if A[i,j]:m|=1<<eidx[(i,j)]
        em.append(m)
    tindex={T:i for i,T in enumerate(th)}
    partner=[None]*1620
    for i in range(1620):
        for j in range(i+1,1620):
            if (em[i]&em[j]).bit_count()==8:partner[i]=j;partner[j]=i
    grids=sorted({frozenset(th[i]|th[partner[i]]) for i in range(1620)},key=lambda U:tuple(sorted(U)));assert len(grids)==45
    G0=grids[0];local=[i for i,T in enumerate(th) if T<=G0];assert len(local)==36
    assert all(partner[i] in local for i in local)

    R=nx.Graph();R.add_nodes_from(G0)
    for a,b in itertools.combinations(G0,2):
        if A[a,b]:R.add_edge(a,b)
    K4=[frozenset(C) for C in nx.find_cliques(R) if len(C)==4];assert len(K4)==8
    H=nx.Graph();H.add_nodes_from(range(8))
    for a,b in itertools.combinations(range(8),2):
        if K4[a].isdisjoint(K4[b]):H.add_edge(a,b)
    fam=[frozenset(C) for C in nx.connected_components(H)];assert sorted(map(len,fam))==[4,4]
    f0=list(fam[0]);f1=list(fam[1])
    rmap={v:next(a for a,c in enumerate(f0) if v in K4[c]) for v in G0}
    cmap={v:next(a for a,c in enumerate(f1) if v in K4[c]) for v in G0}
    coords={}
    for i in local:
        rect=set(G0)-set(th[i]);assert len(rect)==4
        rr=frozenset(rmap[v] for v in rect);cc=frozenset(cmap[v] for v in rect)
        assert len(rr)==len(cc)==2;coords[i]=(rr,cc)
    assert len(set(coords.values()))==36
    all4=frozenset(range(4))
    for i in local:
        r,c=coords[i];j=partner[i]
        assert coords[j]==(all4-r,all4-c)
        assert frozenset(apartments[j])==frozenset(set(G0)-set(th[i]))

    typ=defaultdict(Counter);rowprof=[]
    for i in local:
        c=Counter((em[i]&em[j]).bit_count() for j in local if j!=i);rowprof.append(c)
    assert set(tuple(sorted(c.items())) for c in rowprof)=={((8,1),(12,8),(16,18),(21,8))}
    for ai,i in enumerate(local):
        for j in local[ai+1:]:
            r,c=coords[i];s,d=coords[j];typ[(len(r&s),len(c&d))][(em[i]&em[j]).bit_count()]+=1
    expected={
      (0,0):{8:18},(1,0):{12:72},(0,1):{12:72},
      (1,1):{16:288},(2,0):{16:18},(0,2):{16:18},
      (1,2):{21:72},(2,1):{21:72}}
    assert {k:dict(v) for k,v in typ.items()}==expected

    # Exact PSp/PGSp action on the 40 W33 lines.
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];PSp={tuple(range(40))}
    for p in cand:
        trial=perm_group(gens+[p])
        if len(trial)>len(PSp):gens.append(p);PSp=trial
        if len(PSp)==25920:break
    assert len(PSp)==25920
    outer=build_line_perm(np.diag([1,2,1,2])%3,pts,pidx,lines,lidx);PGSp=perm_group(gens+[outer]);assert len(PGSp)==51840
    stabP=[g for g in PSp if frozenset(g[x] for x in G0)==G0];stabF=[g for g in PGSp if frozenset(g[x] for x in G0)==G0]
    assert (len(stabP),len(stabF))==(576,1152)
    kerP=[g for g in stabP if all(g[x]==x for x in G0)];kerF=[g for g in stabF if all(g[x]==x for x in G0)];assert (len(kerP),len(kerF))==(2,2)
    lpos={i:k for k,i in enumerate(local)}
    def p36(g):return tuple(lpos[tindex[frozenset(g[x] for x in th[i])]] for i in local)
    imP={p36(g) for g in stabP};imF={p36(g) for g in stabF};assert (len(imP),len(imF))==(288,576)
    assert len({p[lpos[local[0]]] for p in imP})==36 and len({p[lpos[local[0]]] for p in imF})==36
    q=tuple(lpos[partner[i]] for i in local)
    assert q not in imF
    assert all(compose(q,p)==compose(p,q) for p in imF)
    ext=imF|{compose(q,p) for p in imF};assert len(ext)==1152

    out={'pass':4764,'local_grid':{'lines':16,'graph':'L_2(4)','support12_minima_inside':36,'coordinate_model':'C(4,2) x C(4,2)','partner_pairs':18,
      'overlap_valencies_per_minimum':{'8':1,'12':8,'16':18,'21':8}},
      'rectangle_rule':{'thickening_complement_is_2x2_rectangle':True,'partner':'simultaneous complement of both 2-subsets','partner_apartment_equals_grid_minus_thickening':True},
      'group_action':{'PGSp_grid_stabilizer':1152,'PSp_grid_stabilizer':576,'pointwise_kernel_on_16_lines':2,'PGSp_image_on_36':576,'PSp_image_on_36':288,'both_transitive':True,
        'partner_in_PGSp_image':False,'partner_centralizes_PGSp_image':True,'generated_extension_order':1152},
      'theorem':'Inside every protected 16-line rook grid, the 36 support-12 minima are exactly the C(4,2)xC(4,2) rectangle states. The overlap-8 partner is simultaneous duad complementation; it is a central extra involution on the 36-set, not a PGSp grid motion.',
      'boundary':'Exact local combinatorics and permutation-group action. The 1152 extension on rectangles is not asserted to be a new subgroup of PGSp.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
