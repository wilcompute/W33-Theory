#!/usr/bin/env python3
"""Pass5146: actual W(3,5) census of sharp 18-chamber / 27-adjacency leaders.

Pass5134's abstract subcubic girth-eight cap n1=27 is genuinely attained inside
the W(3,5) Levi graph.  We materialize two natural sharp carriers.  The first
uses two disjoint GQ lines, three matched transversal pairs, and one pendant
flag at each of the six selected points.  It has 4^6=4096 pendant gauges and is
fully censused.  A second explicit carrier is a K_{3,3} point-collinearity grid.

These are geometry witnesses/diagnostics, not a classification of every sharp
leader.  Their apartment-code words are all far above 625.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5146_Q5_SHARP_LEADER18_EMBEDDED_CENSUS.json'
Q=5
PAIR_INTER_TO_DIST={125:1,25:2,5:3,1:4}


def xor_stars(S,ids):
    z=0
    for i in ids:z^=S[i]
    return z


def pair_distance_hist(S,ids):
    h=Counter()
    for a,b in itertools.combinations(ids,2):
        w=(S[a]&S[b]).bit_count()
        assert w in PAIR_INTER_TO_DIST,(a,b,w)
        h[PAIR_INTER_TO_DIST[w]]+=1
    assert sum(h.values())==len(ids)*(len(ids)-1)//2
    return tuple(h[d] for d in range(1,5))


def selected_levi_wedges(G,ids):
    deg={}
    for fi in ids:
        p,l=G['flags'][fi]
        deg[('p',p)]=deg.get(('p',p),0)+1
        deg[('l',l)]=deg.get(('l',l),0)+1
    w=sum(d*(d-1)//2 for d in deg.values())
    return w,Counter(deg.values())


def main():
    G=build_W(Q);S=chamber_stars(G);fidx={f:i for i,f in enumerate(G['flags'])}
    pair_line={}
    point_lines=[[] for _ in G['pts']]
    for li,L in enumerate(G['lines']):
        for p in L:point_lines[p].append(li)
        for a,b in itertools.combinations(sorted(L),2):pair_line[(a,b)]=li
    def line_of(a,b):return pair_line.get(tuple(sorted((a,b))))

    # Carrier A: two disjoint lines with the canonical GQ matching.
    l0=0;L0=sorted(G['lines'][l0])
    l1=next(li for li,L in enumerate(G['lines']) if li!=l0 and not (G['lines'][l0]&L))
    L1=sorted(G['lines'][l1])
    matching=[]
    for p in L0:
        qs=[q for q in L1 if line_of(p,q) is not None]
        assert len(qs)==1
        matching.append((p,qs[0],line_of(p,qs[0])))
    assert len({q for _,q,_ in matching})==6
    chosen=matching[:3]
    points=[x for p,q,_ in chosen for x in (p,q)]
    fixed=[];pendant_options=[]
    for p,q,t in chosen:
        fixed.extend([fidx[(p,l0)],fidx[(q,l1)],fidx[(p,t)],fidx[(q,t)]])
        for x,base in ((p,l0),(q,l1)):
            used={base,t};opts=[fidx[(x,l)] for l in point_lines[x] if l not in used]
            assert len(opts)==4;pendant_options.append(opts)
    assert len(fixed)==12 and len(pendant_options)==6

    weights=Counter();profiles=Counter();joint=Counter()
    min_word=None
    for choice in itertools.product(range(4),repeat=6):
        ids=fixed+[pendant_options[i][choice[i]] for i in range(6)]
        assert len(set(ids))==18
        n1,degs=selected_levi_wedges(G,ids);assert n1==27
        assert degs==Counter({3:8,2:3,1:6})
        w=xor_stars(S,ids).bit_count();ph=pair_distance_hist(S,ids)
        weights[w]+=1;profiles[ph]+=1;joint[(w,ph)]+=1
        if min_word is None or w<min_word[0]:min_word=(w,ids,ph)
    expected_weights={5832:4,5848:180,5856:480,5864:1260,5872:1440,5880:732}
    expected_profiles={
        (27,36,54,36):4,(27,36,52,38):180,(27,36,51,39):480,
        (27,36,50,40):1260,(27,36,49,41):1440,(27,36,48,42):732}
    assert dict(weights)==expected_weights and dict(profiles)==expected_profiles
    assert sum(weights.values())==4096 and min_word[0]==5832

    # Carrier B: an explicit K3,3 point-collinearity grid in the same canonical labeling.
    A=(0,6,7);B=(1,31,36)
    assert all(line_of(a,a2) is None for a,a2 in itertools.combinations(A,2))
    assert all(line_of(b,b2) is None for b,b2 in itertools.combinations(B,2))
    grid_lines=[line_of(a,b) for a in A for b in B];assert all(x is not None for x in grid_lines)
    assert len(set(grid_lines))==9
    grid_ids=[]
    for a in A:
        for b in B:
            l=line_of(a,b);grid_ids.extend([fidx[(a,l)],fidx[(b,l)]])
    assert len(set(grid_ids))==18
    gn1,gdeg=selected_levi_wedges(G,grid_ids);assert gn1==27
    assert gdeg==Counter({3:6,2:9})
    grid_w=xor_stars(S,grid_ids).bit_count();grid_ph=pair_distance_hist(S,grid_ids)
    assert grid_w==5832 and grid_ph==(27,36,54,36)

    out={
      'pass':5146,'status':'THEOREM_Q5_SHARP_LEADER18_EMBEDDED_WITNESS_CENSUS',
      'q':5,'abstract_sharp_adjacent_pairs':27,
      'opposite_line_carrier':{
        'base_lines':[l0,l1],'three_matching_pairs':[[p,q,t] for p,q,t in chosen],
        'pendant_gauges':4096,
        'selected_levi_degree_histogram':{'3':8,'2':3,'1':6},
        'weight_histogram':{str(k):v for k,v in sorted(weights.items())},
        'pair_distance_histogram_family':{str(k):v for k,v in sorted(profiles.items())},
        'minimum_weight_in_family':min(weights)},
      'k33_grid_carrier':{
        'A_points':list(A),'B_points':list(B),'selected_levi_degree_histogram':{'3':6,'2':9},
        'apartment_word_weight':grid_w,'pair_distance_histogram':list(grid_ph)},
      'conclusion':'The Pass5134 n1=27 extremum is not an artifact of the abstract girth-eight relaxation: distinct sharp carriers occur in actual W(3,5). Nevertheless these explicit sharp families have apartment weights at least 5832, far above the 625 target.',
      'boundary':'This is not an orbit-complete classification of all 18-chamber n1=27 embeddings and cannot replace the universal Pass5142 cubic proof.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
