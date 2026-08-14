#!/usr/bin/env python3
"""Pass5140: q=3 triangle curvature escapes first-order theta blindness."""
from __future__ import annotations
import itertools,json
from collections import deque,Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5140_Q3_THETA_TRIANGLE_CURVATURE.json'
def main():
    G=build_W(3);N=len(G['apartments']);assert N==1620
    checks=set();nbr=[set() for _ in range(N)]
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(4),3):
            t=tuple(sorted((loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))])))
            checks.add(t)
            for a,b in itertools.combinations(t,2):nbr[a].add(b);nbr[b].add(a)
    assert len(checks)==4320 and {len(x) for x in nbr}=={16}
    stars=chamber_stars(G);assert len(stars)==160 and {z.bit_count() for z in stars}=={81}
    def profile(z):
        S={i for i in range(N) if(z>>i)&1};edges=sum(len(nbr[v]&S) for v in S)//2;T=set()
        for v in S:
            for a in nbr[v]&S:
                if a<=v:continue
                for b in nbr[v]&nbr[a]&S:
                    if b>a:T.add((v,a,b))
        theta_full=sum(t in checks for t in T);assert theta_full==0
        return(len(S),edges,len(T),theta_full)
    flags=G['flags'];F=len(flags);fn=[set() for _ in range(F)]
    for i,(p,l) in enumerate(flags):
        for j in range(i+1,F):
            q,m=flags[j]
            if p==q or l==m:fn[i].add(j);fn[j].add(i)
    dist=[None]*F;dist[0]=0;Q=deque([0])
    while Q:
        a=Q.popleft()
        for b in fn[a]:
            if dist[b] is None:dist[b]=dist[a]+1;Q.append(b)
    assert Counter(dist)==Counter({4:81,3:54,2:18,1:6,0:1})
    single=profile(stars[0]);assert single==(81,324,108,0);by={}
    for d in range(1,5):
        vals={profile(stars[0]^stars[j]) for j in range(1,F) if dist[j]==d};assert len(vals)==1;by[str(d)]=list(next(iter(vals)))
    assert by=={'1':[108,432,108,0],'2':[144,576,168,0],'3':[156,624,196,0],'4':[160,640,208,0]}
    assert single[1]==4*single[0] and all(v[1]==4*v[0] for v in by.values())
    out={'pass':5140,'status':'THEOREM_Q3_HIGHER_ORDER_THETA_CURVATURE','theta_graph':{'vertices':1620,'degree':16,'theta_checks':4320},'single_chamber_star':{'weight':81,'induced_edges':324,'selected_triangles':108,'fully_selected_theta_checks':0},'two_star_xor_by_gallery_distance':{d:{'weight':v[0],'induced_edges':v[1],'selected_triangles':v[2],'fully_selected_theta_checks':v[3]} for d,v in by.items()},'first_order_rigidity':'Every listed support has induced_edges=4*weight.','higher_order_signal':'Selected triangle count varies although first-order degree/Rayleigh data is fixed. Parity forbids fully selected theta-check triangles, so the varying triangles are the common-root/Tanner-six-cycle triangles.','boundary':'Higher-order invariant identified; no general q5/all-q triangle-curvature distance inequality is yet proved.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
