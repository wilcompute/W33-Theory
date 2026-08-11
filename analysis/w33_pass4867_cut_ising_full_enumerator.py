#!/usr/bin/env python3
"""Pass4867 — exact ordinary cut-space Ising enumerator and full K enumerator.

Use the marked-double-six K6 subset chart (independently certified in Pass4869).
Fixing the marked vertex on one side of each cut leaves 15 duad bits and 20
triad bits. The 15 duad bits are arbitrary labeled graphs on six vertices.
Instead of enumerating all 2^15 duad choices, quotient them by S6: there are
exactly 156 unlabeled graphs on six vertices. For each orbit representative,
enumerate all 2^20 triad subsets and weight by the labeled-graph orbit size.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS4867_CUT_ISING_FULL_CODE_ENUMERATOR.json"
COS=ROOT/"data/PART_W33_PASS4859_SWITCHING_ENUMERATOR_RADIUS.json"

def kraw(j,i,n=360):
    return sum((-1)**s*math.comb(i,s)*math.comb(n-i,j-s)
               for s in range(max(0,j-(n-i)),min(j,i)+1))

def main()->int:
    duads=list(itertools.combinations(range(6),2));triads=list(itertools.combinations(range(6),3))
    di={d:i for i,d in enumerate(duads)}
    DD=nx.Graph();DD.add_nodes_from(range(15))
    for i,j in itertools.combinations(range(15),2):
        if len(set(duads[i])&set(duads[j]))==1:DD.add_edge(i,j)
    TT=nx.Graph();TT.add_nodes_from(range(20))
    for i,j in itertools.combinations(range(20),2):
        if len(set(triads[i])&set(triads[j])) in (0,2):TT.add_edge(i,j)
    cross=np.zeros((15,20),dtype=np.int8)
    for i,d in enumerate(duads):
        for j,t in enumerate(triads):
            if len(set(d)&set(t))==1:cross[i,j]=1
    assert DD.number_of_edges()==60 and TT.number_of_edges()==100 and int(cross.sum())==180

    reps=[g.copy() for g in nx.graph_atlas_g() if g.number_of_nodes()==6]
    assert len(reps)==156
    repdata=[]
    for g in reps:
        aut=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g,g).isomorphisms_iter())
        orbit=math.factorial(6)//aut
        mask=0
        for a,b in g.edges():mask|=1<<di[tuple(sorted((a,b)))]
        sel={i for i in range(15) if mask>>i&1}
        cutD=sum(((i in sel)!=(j in sel)) for i,j in DD.edges())
        nG=np.array([sum(int(cross[i,j]) for i in sel) for j in range(20)],dtype=np.int16)
        repdata.append((orbit,mask,len(sel),cutD,nG,aut))
    assert sum(x[0] for x in repdata)==2**15

    N=1<<20
    hsize=np.zeros(N,dtype=np.int8);cutT=np.zeros(N,dtype=np.int16)
    nbr=[]
    for i in range(20):
        m=0
        for j in TT.neighbors(i):m|=1<<j
        nbr.append(m)
    for m in range(1,N):
        lb=m&-m;i=lb.bit_length()-1;prev=m^lb
        hsize[m]=hsize[prev]+1
        cutT[m]=cutT[prev]+10-2*((prev&nbr[i]).bit_count())
    masks=np.arange(N,dtype=np.uint32)
    bits=((masks[:,None]>>np.arange(20,dtype=np.uint32))&1).astype(np.int8)

    hist=np.zeros(361,dtype=object);max_contrib=[]
    for idx,(orbit,mask,gs,cd,ng,aut) in enumerate(repdata):
        dot=bits@ng
        w=cd+12*gs+cutT.astype(np.int32)+10*hsize.astype(np.int32)-2*dot.astype(np.int32)
        h=np.bincount(w,minlength=361)
        for k,val in enumerate(h):
            if val:hist[k]+=int(orbit)*int(val)
        if h[216]:max_contrib.append((idx,orbit,gs,cd,aut,int(h[216]),int(orbit)*int(h[216])))
    assert sum(hist)==2**35
    cut={str(i):int(c) for i,c in enumerate(hist) if c}
    assert cut["0"]==1 and cut["20"]==36 and cut["216"]==120
    assert len(cut)==82 and max_contrib==[(52,60,6,36,12,2,120)]
    assert nx.is_isomorphic(reps[52],nx.cycle_graph(6))

    prior=json.loads(COS.read_text())
    cos={int(k):int(v) for k,v in prior["nontrivial_switching_coset"]["complete_weight_enumerator"].items()}
    assert sum(cos.values())==2**35
    full={i:int(hist[i])+cos.get(i,0) for i in range(361) if int(hist[i]) or cos.get(i,0)}
    assert sum(full.values())==2**36 and min(i for i in full if i>0)==20 and max(full)==216
    dual={}
    for j in range(8):
        num=sum(A*kraw(j,i) for i,A in full.items())
        assert num%(2**36)==0
        dual[j]=num//(2**36)
    assert [dual[i] for i in range(4)]==[1,0,0,1080]

    out={
      "pass":4867,
      "cut_space":{"dimension":35,"size":2**35,"weight_levels":len(cut),"minimum_nonzero":20,
        "maximum":216,"maximum_count":120,"complete_weight_enumerator":cut},
      "orbit_reduction":{"marked_chart":"15 duads + 20 triads","duad_labeled_states":2**15,
        "duad_S6_orbits_unlabeled_graphs":156,"triad_states_per_representative":2**20,
        "effective_pair_evaluations":156*(2**20),"brute_force_cut_words":2**35,
        "maximum_cut_duad_orbit":"C6","maximum_cut_duad_orbit_size":60,
        "triad_completions_per_C6_representative":2},
      "full_code":{"code":"K=[360,36,20]_2","size":2**36,"weight_levels":len(full),
        "minimum":20,"maximum":216,"complete_weight_enumerator":{str(k):v for k,v in full.items()}},
      "MacWilliams_dual_check":{"A0_to_A7":{str(k):v for k,v in dual.items()},
        "confirms_dual_minimum_3":True,"A3_dual_1080_even_triangle_checks":True},
      "theorem":"The ordinary 35-dimensional cut-space Ising polynomial is now exact. A marked-double-six K6 chart reduces the computation from 2^35 cut words to 156 unlabeled six-vertex graph representatives times 2^20 triad states, with exact S6 orbit weights. The cut enumerator has 82 nonzero weight levels, minimum 20, maximum 216, and exactly 120 maximum cuts. Combining it with the frozen Pass4859 non-cut switching coset gives the complete 2^36-word enumerator of K=[360,36,20]_2. A MacWilliams cross-check recovers dual coefficients A1=A2=0 and A3=1080.",
      "boundary":"This closes the complete weight enumerator, not the covering radius. The equality '120 maximum cuts = 120 Steiner triangles' is not promoted to an identification without a stabilizer-compatible map."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"pass":4867,"cut_levels":len(cut),"full_levels":len(full),"max_cut_count":120,"dual":dual},indent=2))
    return 0
if __name__=="__main__":raise SystemExit(main())
