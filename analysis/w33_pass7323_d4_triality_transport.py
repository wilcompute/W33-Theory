#!/usr/bin/env python3
"""Pass7323: test whether relation-(0,4) E8 charts canonically transport D4 triality frames."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import w33_pass7163_7170_e8_hexagonal_lift as b
import w33_pass7182_d4_glue_spread_code as d

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7323_D4_TRIALITY_TRANSPORT.json'

def compose(p,q):return tuple(p[q[i]] for i in range(3))
def invp(p):
    z=[0]*3
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def pclass(p):
    if p==(0,1,2):return 'identity'
    fixed=sum(p[i]==i for i in range(3))
    return 'transposition' if fixed==1 else '3-cycle'

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,partner=d.cqs(adj);ri={r:i for i,r in enumerate(R)}
    neg={i:ri[tuple(-x for x in R[i])] for i in range(240)}
    frames=[]
    for q in Q:
        roots=sorted({v for f in q for v in fib[f]});lines=sorted({min(v,neg[v]) for v in roots});assert len(lines)==12
        F=[]
        for C in itertools.combinations(lines,4):
            if all(b.dot(R[x],R[y])==0 for x,y in itertools.combinations(C,2)):F.append(tuple(C))
        F=sorted(set(F));assert len(F)==3 and set().union(*map(set,F))==set(lines) and sum(map(len,F))==12
        frames.append(F)
    opt_hist=Counter();matrix_hist=Counter();unique_transport={};relation_hist=Counter()
    for a,c in itertools.combinations(range(90),2):
        rel=d.relation(Q,adj,a,c);relation_hist[rel]+=1
        if rel!=(0,4):continue
        M=[]
        for F in frames[a]:
            row=[]
            for G in frames[c]:
                row.append(sum(abs(b.dot(R[x],R[y]))==4 for x in F for y in G))
            M.append(tuple(row))
        M=tuple(M);matrix_hist[M]+=1
        vals=[]
        for p in itertools.permutations(range(3)):vals.append((sum(M[i][p[i]] for i in range(3)),p))
        best=max(x for x,p in vals);opts=[p for x,p in vals if x==best];opt_hist[len(opts)]+=1
        if len(opts)==1:unique_transport[(a,c)]=opts[0];unique_transport[(c,a)]=invp(opts[0])
    # If the cross-incidence invariant gives unique transports, compute triangle holonomy.
    hol=Counter();triangles=0
    Gnbr={i:set() for i in range(90)}
    for a,c in itertools.combinations(range(90),2):
        if d.relation(Q,adj,a,c)==(0,4):Gnbr[a].add(c);Gnbr[c].add(a)
    if opt_hist and set(opt_hist)=={1}:
        for a,c,e in itertools.combinations(range(90),3):
            if c in Gnbr[a] and e in Gnbr[c] and a in Gnbr[e]:
                p=compose(unique_transport[(e,a)],compose(unique_transport[(c,e)],unique_transport[(a,c)]));hol[pclass(p)]+=1;triangles+=1
    out={'schema':'w33.pass7323.d4_triality_transport.v1','status':'PASS','selected_D4':90,'triality_frames_per_D4':3,
      'relation_histogram':{str(k):v for k,v in sorted(relation_hist.items(),key=lambda z:str(z[0]))},
      'cross4_frame_score_definition':'3x3 entry counts nonorthogonal antipodal-root-line pairs between the two D4 triality frames',
      'distinct_cross4_score_matrices':len(matrix_hist),'cross4_score_matrix_multiplicities':{str(k):v for k,v in matrix_hist.items()},
      'number_of_optimal_matchings_histogram':{str(k):v for k,v in sorted(opt_hist.items())},
      'unique_triality_transport_on_every_cross4_edge':bool(opt_hist and set(opt_hist)=={1}),
      'triangle_holonomy':{k:v for k,v in hol.items()},'triangles_tested':triangles,
      'theorem_or_obstruction':('The root-line cross-incidence canonically transports the three D4 triality frames, and the displayed S3 triangle holonomy is gauge-invariant up to conjugacy.' if opt_hist and set(opt_hist)=={1} else 'The natural root-line cross-incidence does not select a unique S3 matching on every unimodular D4 chart edge. Thus ordinary E8 chart data plus this intrinsic incidence still leave a genuine triality torsor; no nontrivial S3 holonomy is manufactured.'),
      'firewall':'A transport is promoted only if the optimizer is unique on all 1080 relation-(0,4) edges.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','optimizers':out['number_of_optimal_matchings_histogram'],'unique':out['unique_triality_transport_on_every_cross4_edge'],'hol':out['triangle_holonomy']}))
if __name__=='__main__':main()
