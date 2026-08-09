#!/usr/bin/env python3
"""Pass 4548 -- C7/C8 higher-body tomography of the W33 building.

Pass 4523 proved that the degree-two primitive-C6 Walsh layer reconstructs the
line graph of every thick generalized quadrangle.  This pass asks the next
question on W33: do the first genuinely higher-body layers recover more than
pair adjacency?

Using the exact primitive nonbacktracking Walsh machinery of Pass 4514:

C7, degree three:
  * the 4320 triples inducing exactly one line-graph edge have coefficient 48;
  * the 2160 induced P3 triples have coefficient 204;
  * independent triples and line-graph triangles have coefficient zero.
Thus C7^((3)) is an exact ternary incidence observable, with the P3 support
species singled out by coefficient 204.

C8, degree four:
  ten PSp support orbits occur.  Most importantly, the unique coefficient-712
  orbit has size 1620 and consists exactly of the induced C4 apartments.  Hence
the primitive length-eight degree-four Walsh tensor reconstructs the apartment
set directly.

C8 also refines the induced four-vertex line graph: P3+isolated supports split
between coefficients 56 and 80, while 2K2 supports split between 64 and 156.
The split is visible in ambient point-union collinearity statistics.  Therefore
C8^((4)) is not a function only of the induced line graph on the four support
vertices; it sees their embedding in the surrounding generalized quadrangle.
"""
from __future__ import annotations

import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

import w33_pass4511_4514_dual_even_prism_ihara as p4514
from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4548_C7_C8_HIGHER_BODY_TOMOGRAPHY.json'


def point_union_inv(mask,lines,Apoint):
    ls=[i for i in range(40) if (mask>>i)&1]
    U=set().union(*(set(lines[i]) for i in ls))
    pe=sum(int(Apoint[x,y]) for x,y in itertools.combinations(sorted(U),2))
    pt=sum(1 for t in itertools.combinations(sorted(U),3)
           if all(Apoint[x,y] for x,y in itertools.combinations(t,2)))
    full=sum(1 for L in lines if set(L)<=U)
    return {'point_union_size':len(U),'point_union_edges':pe,'point_union_triangles':pt,'full_GQ_lines_in_union':full}


def compute_prime_orbits(n,pts,pidx,lines,Astar,selected):
    line_gens=[x[1] for x in selected]
    Apoint,edge_line=p4514.point_graph(lines)
    adj=[list(np.flatnonzero(Apoint[i])) for i in range(40)]
    dedges=[];didx={}
    for u in range(40):
        for v in adj[u]:didx[(u,int(v))]=len(dedges);dedges.append((u,int(v)))
    nexts=[[] for _ in dedges];state_line=[]
    for u,v in dedges:state_line.append(edge_line[(min(u,v),max(u,v))])
    for i,(u,v) in enumerate(dedges):
        for w in adj[v]:
            if int(w)!=u:
                j=didx[(v,int(w))];nexts[i].append((j,state_line[j]))
    rev=[[] for _ in dedges]
    for i,lst in enumerate(nexts):
        for j,_ in lst:rev[j].append((i,state_line[j]))
    base=p4514.diagonal_nb_poly(0,n,dedges,nexts,rev)
    rows=p4514.global_orbit_coeffs(base,line_gens)
    out=[]
    for orb,cg in rows:
        rep=next(iter(orb));val=cg
        if n==8 and rep==0:val-=13920
        assert val%n==0
        c=val//n
        if c:out.append((orb,c,rep))
    return out,Apoint


def main()->int:
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry();apset=set(apmasks)
    selected,psp,outer,pgsp=p4514.build_groups(pts,pidx,lines)
    p7,Apoint=compute_prime_orbits(7,pts,pidx,lines,Astar,selected)
    p8,_=compute_prime_orbits(8,pts,pidx,lines,Astar,selected)

    # C7 degree-three layer.
    c7=[]
    for orb,c,rep in p7:
        inv=p4514.graph_inv(rep,Astar)
        if inv['support_size']==3:
            c7.append({'orbit_size':len(orb),'coefficient':c,'induced_edges':inv['induced_edges'],
                       'degree_sequence':inv['degree_sequence'],'triangles':inv['triangles']})
    c7=sorted(c7,key=lambda x:(x['induced_edges'],x['coefficient']))
    assert c7==[
      {'orbit_size':4320,'coefficient':48,'induced_edges':1,'degree_sequence':[0,1,1],'triangles':0},
      {'orbit_size':2160,'coefficient':204,'induced_edges':2,'degree_sequence':[1,1,2],'triangles':0}]

    # C8 degree-four layer, including ambient point-union refinements.
    c8=[]
    for orb,c,rep in p8:
        inv=p4514.graph_inv(rep,Astar)
        if inv['support_size']!=4:continue
        row={'orbit_size':len(orb),'coefficient':c,'induced_edges':inv['induced_edges'],
             'degree_sequence':inv['degree_sequence'],'triangles':inv['triangles'],
             'is_apartment':rep in apset,**point_union_inv(rep,lines,Apoint)}
        c8.append(row)
    c8=sorted(c8,key=lambda x:(x['coefficient'],x['orbit_size']))
    assert len(c8)==10
    apartments712=[x for x in c8 if x['coefficient']==712]
    assert len(apartments712)==1 and apartments712[0]['orbit_size']==1620 and apartments712[0]['is_apartment']
    assert sum(x['orbit_size'] for x in c8 if x['is_apartment'])==1620

    # Same induced line graph, different C8 coefficient: ambient embedding is detected.
    p3iso=[x for x in c8 if x['degree_sequence']==[0,1,1,2]]
    assert {x['coefficient'] for x in p3iso}=={56,80}
    assert {x['point_union_triangles'] for x in p3iso}=={16,18}
    twok2=[x for x in c8 if x['degree_sequence']==[1,1,1,1]]
    assert {x['coefficient'] for x in twok2}=={64,156}
    assert {x['point_union_edges'] for x in twok2}=={36,37}

    # Freeze compact species table, merging only literally identical invariant rows.
    agg=Counter()
    for x in c8:
        key=(x['orbit_size'],x['coefficient'],x['induced_edges'],tuple(x['degree_sequence']),x['triangles'],
             x['is_apartment'],x['point_union_size'],x['point_union_edges'],x['point_union_triangles'],x['full_GQ_lines_in_union'])
        agg[key]+=1
    table=[]
    for k,mult in sorted(agg.items(),key=lambda kv:(kv[0][1],kv[0][0])):
        os,c,e,deg,tr,ap,pu,pe,pt,fl=k
        table.append({'PSp_orbits_with_same_record':mult,'orbit_size_each':os,'coefficient':c,
                      'induced_edges':e,'degree_sequence':list(deg),'triangles':tr,'is_apartment':ap,
                      'point_union_size':pu,'point_union_edges':pe,'point_union_triangles':pt,
                      'full_GQ_lines_in_union':fl})

    out={
      'pass':4548,
      'C7_degree3':{'nonzero_support_orbits':c7,
        'zero_species':'independent triples and line-graph triangles',
        'theorem':'coefficient 204 singles out exactly the 2160 induced P3 line triples; one-edge triples have coefficient 48'},
      'C8_degree4':{'PSp_orbits':10,'species_table':table,
        'apartment_theorem':'coefficient 712 occurs on exactly one orbit of size 1620, equal to the apartment C4 set',
        'ambient_refinement':['P3+isolated splits 56 versus 80','2K2 splits 64 versus 156'],
        'conclusion':'C8 degree four reconstructs apartments and is not determined solely by the induced four-vertex line graph'},
      'boundary':'Exact W33 primitive-prime/Walsh theorem using the already-certified Pass4514 nonbacktracking engine. This is a finite building-tomography statement, not a physical observable claim.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
