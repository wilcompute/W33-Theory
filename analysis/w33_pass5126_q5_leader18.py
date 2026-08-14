#!/usr/bin/env python3
"""Pass5126: exact q=5 sub-625 chamber-leader barrier rises to 18.

A cut-minimal chamber representative is an edge set in the 6-regular Levi
incidence graph, hence its selected subgraph is bipartite, max-degree <=3,
and has girth >=8.  For 17 selected edges we exhaust all left/right degree
sequences with wedge count >=26 and all simple bipartite realizations while
forbidding C4/C6.  None exists.  Wedge count 25 is realizable.  Feeding this
exact cap into the q=5 chamber distance-scheme Delsarte inequalities gives a
second-order Bonferroni apartment-weight lower bound exactly 625.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5126_Q5_LEADER18.json'

def degree_sequences(m):
    out=[]
    for n3 in range(m//3+1):
        for n2 in range((m-3*n3)//2+1):
            n1=m-3*n3-2*n2
            if n1<0: continue
            seq=(3,)*n3+(2,)*n2+(1,)*n1
            out.append((seq,3*n3+n2,(n1,n2,n3)))
    return out

def exists_girth8(left_degs,right_degs):
    """Exact prescribed-degree bipartite realization with no C4 or C6."""
    L=tuple(sorted(left_degs,reverse=True)); R=tuple(sorted(right_degs,reverse=True))
    rem=list(R); rows=[]; nodes=0
    def conflicts():
        bad=set()
        # Two rights in one prior row are distance two: reusing both makes a C4.
        for row in rows:
            for a,b in itertools.combinations(row,2): bad.add((min(a,b),max(a,b)))
        # Rights at distance four through two prior rows: reusing both makes a C6.
        for i in range(len(rows)):
            A=set(rows[i])
            for j in range(i+1,len(rows)):
                B=set(rows[j])
                for t in A&B:
                    for a in A-{t}:
                        for b in B-{t}:
                            if a!=b: bad.add((min(a,b),max(a,b)))
        return bad
    def rec(i):
        nonlocal nodes
        nodes+=1
        if i==len(L): return tuple(rows) if all(x==0 for x in rem) else None
        if sum(rem)!=sum(L[i:]): return None
        d=L[i]; avail=[j for j,x in enumerate(rem) if x]
        if len(avail)<d: return None
        bad=conflicts()
        for C in itertools.combinations(avail,d):
            if any((min(a,b),max(a,b)) in bad for a,b in itertools.combinations(C,2)): continue
            for j in C: rem[j]-=1
            if all(x<=len(L)-i-1 for x in rem):
                rows.append(C); z=rec(i+1)
                if z is not None: return z
                rows.pop()
            for j in C: rem[j]+=1
        return None
    witness=rec(0)
    return witness,nodes

def delsarte_ok(m,n1,n2,n3,n4):
    # Exact q=5 chamber-scheme positivity, as in Pass5118.
    if 625*m-250*n1+50*n2-10*n3+2*n4 < 0: return False
    if 25*m+20*n1-10*n2-4*n3+2*n4 < 0: return False
    R=25*m+20*n1+4*n3-2*n4
    C=5*n1+4*n2-n3
    return R>=0 and R*R>=10*C*C

def optimize(m,cap):
    total=math.comb(m,2); best=(-1,None); feasible=0
    for n1 in range(cap+1):
      for n2 in range(total-n1+1):
        for n3 in range(total-n1-n2+1):
          n4=total-n1-n2-n3
          if not delsarte_ok(m,n1,n2,n3,n4): continue
          feasible+=1; overlap=125*n1+25*n2+5*n3+n4
          if overlap>best[0]: best=(overlap,(n1,n2,n3,n4))
    return {'m':m,'N1_cap':cap,'max_pair_overlap':best[0],
            'distance_pair_counts':list(best[1]),'delsarte_integer_points':feasible,
            'bonferroni_weight_lower_bound':m*625-2*best[0]}

def main():
    ds=degree_sequences(17); candidates=[]; seen=set(); rejected=[]; max_nodes=0
    for L,wL,cL in ds:
      for R,wR,cR in ds:
        if wL+wR<26: continue
        key=tuple(sorted((cL,cR)))
        if key in seen: continue
        seen.add(key); candidates.append((wL+wR,cL,cR,L,R))
    for W,cL,cR,L,R in sorted(candidates,reverse=True):
        witness,nodes=exists_girth8(L,R); max_nodes=max(max_nodes,nodes)
        assert witness is None
        rejected.append({'wedge':W,'left_counts':list(cL),'right_counts':list(cR),'search_nodes':nodes})
    # Find an exact wedge-25 witness.
    witness25=None
    for L,wL,cL in ds:
      for R,wR,cR in ds:
        if wL+wR!=25: continue
        z,nodes=exists_girth8(L,R)
        if z is not None:
            witness25={'left_counts':list(cL),'right_counts':list(cR),'rows':[list(x) for x in z],'search_nodes':nodes}; break
      if witness25: break
    assert witness25 is not None
    row=optimize(17,25)
    assert row['distance_pair_counts']==[25,66,45,0]
    assert row['max_pair_overlap']==5000 and row['bonferroni_weight_lower_bound']==625
    out={'pass':5126,'status':'THEOREM_Q5_SUB625_COUNTEREXAMPLE_LEADER_AT_LEAST_18','q':5,
         'selected_edges':17,'universal_girth8_wedge_cap':25,
         'degree_sequence_pairs_rejected_above_cap':len(rejected),'max_backtracking_nodes':max_nodes,
         'wedge25_witness':witness25,'delsarte':row,
         'conclusion':'Pass5118 covers leaders <=16. Every cut-minimal 17-edge representative has apartment weight >=625. Hence any q=5 word of weight <625 has minimum chamber-generator leader >=18.',
         'boundary':'The lower bound at leader 17 is exactly 625. Equality-shell feasibility/classification at leader 17 and all leaders >=18 remain open; q=5 distance 625 is not claimed proved.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
