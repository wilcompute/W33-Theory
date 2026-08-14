#!/usr/bin/env python3
"""Pass5140 (bonkers): all-q triple chamber-star law and q=5 cubic closure of leader 18.

Three chambers can lie in one apartment only in five dihedral C8 distance
patterns.  For W(3,q), common-apartment counts are q^2,q,1 accordingly.  The
complete rooted census is verified at q=2,3,4,5, including GF(4).

At q=5 this exact cubic coefficient closes the m=18 shell that Pass5134 proved
was inaccessible to pairwise Bonferroni/Delsarte.  For an 18-edge cut-minimal
leader with N1 adjacent chamber pairs, the selected three-edge-path count
P3=sum_{uv}(d_u-1)(d_v-1) obeys P3>=max(0,4(N1-18)).  Each such path has
signature (1,1,2), hence contributes 25 to the triple-overlap sum.  Combining
this with the parity minorant 1_{r odd} >= r-2*C(r,2)+(6/17)*C(r,3) and exact
Delsarte pair-overlap maxima for each N1<=27 gives wt>=638 in the worst shell.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5140_ALLQ_TRIPLE_CHAMBER_STAR_LAW.json'

def dist_from_inter(q,w):
    for d in range(1,5):
        if w==q**(4-d):return d
    raise AssertionError((q,w))

def predicted(q,sig):
    return {(1,1,2):q*q,(1,2,3):q,(1,3,4):1,(2,2,4):1,(2,3,3):1}.get(sig,0)

def anchor(q):
    G=build_W(q);S=chamber_stars(G);n=len(S);base=S[0]
    d0=[0]*n
    for i in range(1,n):d0[i]=dist_from_inter(q,(base&S[i]).bit_count())
    hist=Counter();by_sig=defaultdict(Counter)
    for i,j in itertools.combinations(range(1,n),2):
        dij=dist_from_inter(q,(S[i]&S[j]).bit_count())
        sig=tuple(sorted((d0[i],d0[j],dij)))
        t=(base&S[i]&S[j]).bit_count();hist[t]+=1;by_sig[sig][t]+=1
        assert t==predicted(q,sig),(q,sig,t,predicted(q,sig))
    assert all(len(H)==1 for H in by_sig.values())
    return {'q':q,'chambers':n,'fixed_base_triples':sum(hist.values()),
      'triple_intersection_histogram':{str(k):v for k,v in sorted(hist.items())},
      'distance_signatures':{str(sig):{'intersection':next(iter(H)),'count':sum(H.values())} for sig,H in sorted(by_sig.items())}}

def delsarte_ok(m,n1,n2,n3,n4):
    if 625*m-250*n1+50*n2-10*n3+2*n4<0:return False
    if 25*m+20*n1-10*n2-4*n3+2*n4<0:return False
    R=25*m+20*n1+4*n3-2*n4;C=5*n1+4*n2-n3
    return R>=0 and R*R>=10*C*C

def max_pair_overlap_exact_n1(m,n1):
    total=math.comb(m,2);rem=total-n1;best=(-1,None)
    for n2 in range(rem+1):
      for n3 in range(rem-n2+1):
        n4=rem-n2-n3
        if not delsarte_ok(m,n1,n2,n3,n4):continue
        ov=125*n1+25*n2+5*n3+n4
        if ov>best[0]:best=(ov,(n1,n2,n3,n4))
    return best

def parity_minorant_check():
    c=Fraction(6,17)
    rows=[]
    for r in range(19):
        rhs=Fraction(r)-2*math.comb(r,2)+c*math.comb(r,3)
        assert rhs<=r%2
        rows.append({'r':r,'rhs_num':rhs.numerator,'rhs_den':rhs.denominator})
    return rows

def q5_m18_cubic_closure():
    # For an edge uv of the selected Levi subgraph set x=d(u)-1,y=d(v)-1 in {0,1,2}.
    # xy >= 2x+2y-4. Summing gives P3 >= 4 N1 - 4m because
    # sum_{edge ends}(d(v)-1)=sum_v d(v)(d(v)-1)=2N1.
    m=18;rows=[];worst=None
    for n1 in range(28): # Pass5134's sharp N1<=27 cap
        ov,dist=max_pair_overlap_exact_n1(m,n1)
        assert ov>=0
        p3=max(0,4*(n1-m))
        triple_lb=25*p3
        # 17 wt >= 17(m*625-2*pair_overlap)+6*triple_overlap.
        num=17*(m*625-2*ov)+6*triple_lb
        ceil_lb=(num+16)//17
        row={'N1':n1,'pair_overlap_max':ov,'distance_counts':list(dist),
             'three_edge_paths_lower_bound':p3,'triple_overlap_lower_bound':triple_lb,
             'seventeen_times_weight_lower_bound':num,'integer_weight_lower_bound':ceil_lb}
        rows.append(row)
        if worst is None or Fraction(num,17)<Fraction(worst['seventeen_times_weight_lower_bound'],17):worst=row
    assert worst['N1']==27
    assert worst['pair_overlap_max']==5465 and worst['distance_counts']==[27,73,53,0]
    assert worst['three_edge_paths_lower_bound']==36 and worst['triple_overlap_lower_bound']==900
    assert worst['seventeen_times_weight_lower_bound']==10840
    assert worst['integer_weight_lower_bound']==638
    return {'leader_size':18,'adjacent_pair_cap_from_pass5134':27,
            'path_inequality':'P3=sum_edges(d(u)-1)(d(v)-1) >= max(0,4(N1-18))',
            'parity_minorant':'1_{r odd} >= r-2*C(r,2)+(6/17)C(r,3) for 0<=r<=18',
            'rows':rows,'worst_shell':worst,
            'conclusion':'Every cut-minimal q5 leader of size 18 produces apartment-code weight at least 638. Therefore any q5 word of weight below 625 has minimum chamber leader at least 19.'}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    minor=parity_minorant_check();closure=q5_m18_cubic_closure()
    out={'pass':5140,'status':'THEOREM_ALL_Q_TRIPLE_LAW_AND_Q5_COUNTEREXAMPLE_LEADER_AT_LEAST_19',
      'law':{'(1,1,2)':'q^2','(1,2,3)':'q','(1,3,4)':'1','(2,2,4)':'1','(2,3,3)':'1','all_other_sorted_distance_signatures':'0'},
      'geometric_proof':'An apartment is an induced 8-cycle in the Levi graph. Up to dihedral symmetry, three distinct cycle edges have exactly the five displayed gallery-distance signatures. Conversely each displayed chamber hull embeds in an apartment. Completing the hull to an 8-cycle leaves respectively two, one, or zero independent generalized-quadrangle projection choices, each with q possibilities, giving q^2,q,1. Any other distance triangle cannot embed in C8 and has intersection zero.',
      'anchors':A,'q5_histogram_expected':{'0':428320,'1':7500,'5':750,'25':75},
      'parity_minorant_rows':minor,'q5_m18_cubic_closure':closure,
      'connection':'Pass5134 proves the pair-only lower bound collapses to 320 at m=18. The exact (1,1,2) triple coefficient q^2=25 plus the three-edge-path lower bound raises the true cubic minorant to wt>=638 and closes that shell.',
      'boundary':'The strict q5 counterexample wall is now leader>=19. The full q5/all-q distance theorem remains open for leaders >=19; fourth and higher intersection information may be needed there.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
