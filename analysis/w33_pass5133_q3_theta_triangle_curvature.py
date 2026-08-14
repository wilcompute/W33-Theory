#!/usr/bin/env python3
"""Pass5133 (bonkers): q=3 triangle curvature escapes first-order theta blindness.

Pass5127 shows every codeword support has identical first-order theta degree,
boundary, and Rayleigh data.  Here we count induced theta-point-graph
triangles.  Code parity forbids any complete theta-check triangle, so every
fully selected triangle is a common-root/Tanner-six-cycle triangle.  The
count varies across chamber-star XOR words and therefore supplies a genuine
higher-order invariant unavailable to first-order expansion.
"""
from __future__ import annotations
import itertools,json
from collections import deque,Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5133_Q3_THETA_TRIANGLE_CURVATURE.json'

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
    def support(z):return {i for i in range(N) if (z>>i)&1}
    def profile(z):
        S=support(z);edges=sum(len(nbr[v]&S) for v in S)//2;T=set()
        for v in S:
            for a in nbr[v]&S:
                if a<=v:continue
                for b in nbr[v]&nbr[a]&S:
                    if b>a:T.add((v,a,b))
        theta_full=sum(t in checks for t in T)
        assert theta_full==0
        return (len(S),edges,len(T),theta_full)
    # Chamber gallery graph = line graph of the q=3 Levi incidence graph.
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
    single=profile(stars[0]);assert single==(81,324,108,0)
    bydist={}
    for d in range(1,5):
        vals={profile(stars[0]^stars[j]) for j in range(1,F) if dist[j]==d}
        assert len(vals)==1;bydist[str(d)]=list(next(iter(vals)))
    assert bydist=={'1':[108,432,108,0],'2':[144,576,168,0],'3':[156,624,196,0],'4':[160,640,208,0]}
    # First-order edge count remains exactly 4|S| for q=3 in every row.
    assert single[1]==4*single[0] and all(v[1]==4*v[0] for v in bydist.values())
    out={'pass':5133,'status':'THEOREM_Q3_HIGHER_ORDER_THETA_CURVATURE','q':3,
      'theta_graph':{'vertices':1620,'degree':16,'theta_checks':4320},
      'single_chamber_star':{'weight':81,'induced_edges':324,'selected_triangles':108,'fully_selected_theta_checks':0},
      'two_star_xor_by_gallery_distance':{d:{'weight':v[0],'induced_edges':v[1],'selected_triangles':v[2],'fully_selected_theta_checks':v[3]} for d,v in bydist.items()},
      'first_order_rigidity':'Every listed support has induced_edges=4*weight, the q=3 instance of Pass5127.',
      'higher_order_signal':'Selected triangle count varies although first-order Rayleigh/escape data is fixed. Since a codeword cannot contain all three vertices of a theta parity check, these triangles are the common-root/Tanner-six-cycle triangles classified in Pass5079.',
      'boundary':'This identifies a nonconstant higher-order invariant and a candidate curvature statistic for distance proofs. It does not yet prove a general triangle inequality or q=5/all-q minimum distance.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
