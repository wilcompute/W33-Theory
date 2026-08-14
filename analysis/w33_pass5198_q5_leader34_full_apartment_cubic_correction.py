#!/usr/bin/env python3
"""Pass5198: close q=5 chamber leader 33 by correcting only full apartments.

Pass5183 closes leader 32 and gives the adjacent-pair cap C_32=57.  Edge
deletion therefore gives the raw m=33 cap floor(57*33/31)=60.  The existing
sharp P5/N3/N4 cubic relaxation closes every layer except N1=56,57,58.

The missing margin comes from using a cubic parity minorant that must remain
valid at apartment occupancy r=8.  On 0<=r<=8 one has the stronger corrected
minorant

  1_{r odd} >= r - 2 C(r,2) + (36/35) C(r,3) - (48/5) C(r,8).

The last term charges only fully selected apartments.  Let A8 be their number
and P5 the total number of selected five-edge Levi paths.  Every full apartment
contains its eight consecutive P5 windows.  Conversely a P5 has opposite outer
chambers and hence a unique apartment (Pass5183).  Thus 8 A8 <= P5.  Counting a
P5 by its central selected edge gives P5<=16m in a subcubic selected Levi graph,
so A8<=2m.

For m=33 this costs at most 66*(48/5), while raising the positive cubic
coefficient from 6/7 to 36/35.  The three formerly open layers N1=56,57,58 now
have uniform integer lower bounds 697,718,739.  Hence every q=5 word below 625
has chamber leader at least 34.
"""
from __future__ import annotations
import json, math
from fractions import Fraction
from pathlib import Path
from analysis.w33_pass5161_q5_cubic_leader23_localtype_dp import (
    p4_relaxed, profiles, ceil_frac)
from analysis.w33_pass5166_q5_cubic_leader25_edgetype_dp import edge_type_n112_floor
from analysis.w33_pass5173_q5_leader31_sharp_p5_extension import p5_sharp
from analysis.w33_pass5183_q5_leader33_p5_n4_coupling import pair_coupled

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5198_Q5_LEADER34_FULL_APARTMENT_CUBIC_CORRECTION.json'


def corrected_parity_rhs(r):
    return (Fraction(r)-2*math.comb(r,2)+Fraction(36,35)*math.comb(r,3)
            -Fraction(48,5)*math.comb(r,8))


def branch(m,W,prev_cap,p):
    minsum=max(2,W-prev_cap+2)
    n112,_=edge_type_n112_floor(*p,minsum)
    p4,_=p4_relaxed(*p,minsum)
    if n112 is None or p4 is None:return None
    p5=p5_sharp(p4,p[0],p[1])
    _,dist,_,pair_lb=pair_coupled(m,W,p4,(p5+1)//2)
    s3=25*n112+10*p4+3*p5
    a8_cap=2*m
    b=(Fraction(pair_lb)+Fraction(36,35)*s3
       -Fraction(48,5)*a8_cap)
    return {'degree_counts':list(p),'N112_lower':n112,'P4_lower':p4,
      'P5_lower':p5,'N3_lower':p4,'N4_lower':(p5+1)//2,
      'conditioned_distance_counts':list(dist),'pair_weight_lower_bound':pair_lb,
      'S3_lower':s3,'full_apartment_upper':a8_cap,
      'corrected_integer_weight_lower_bound':ceil_frac(b)}


def ordinary_branch(m,W,prev_cap,p):
    minsum=max(2,W-prev_cap+2)
    n112,_=edge_type_n112_floor(*p,minsum)
    p4,_=p4_relaxed(*p,minsum)
    if n112 is None or p4 is None:return None
    p5=p5_sharp(p4,p[0],p[1])
    _,dist,_,pair_lb=pair_coupled(m,W,p4,(p5+1)//2)
    s3=25*n112+10*p4+3*p5
    b=Fraction(pair_lb)+Fraction(6,7)*s3
    return ceil_frac(b)


def main():
    # Pointwise certificate for the corrected parity polynomial.
    parity=[]
    for r in range(9):
        z=corrected_parity_rhs(r)
        assert z<=r%2
        parity.append({'r':r,'parity':r%2,'rhs_num':z.numerator,'rhs_den':z.denominator})

    m=33;prev_cap=57
    raw=(prev_cap*m)//(m-2);assert raw==60

    # Pair-only Delsarte is safe through N1=43; N1=44 is already below target.
    _,_,_,pair43=pair_coupled(m,43,0,0);assert pair43==889
    _,_,_,pair44=pair_coupled(m,44,0,0);assert pair44==553

    # Existing sharp cubic + N3/N4 coupling closes all noncritical layers.
    expected_safe={44:1771,45:1587,46:1437,47:1287,48:1103,49:953,
                   50:840,51:780,52:747,53:713,54:680,55:647,
                   59:1475,60:2793}
    safe={}
    for W,E in expected_safe.items():
        vals=[]
        for p in profiles(m,W):
            x=ordinary_branch(m,W,prev_cap,p)
            if x is not None:vals.append(x)
        assert vals and min(vals)==E,(W,min(vals),E)
        safe[str(W)]=E

    expected_critical={56:697,57:718,58:739}
    critical={}
    expected_profiles={
      56:[[2,8,16],[5,5,17],[8,2,18]],
      57:[[0,9,16],[3,6,17],[6,3,18],[9,0,19]],
      58:[[1,7,17],[4,4,18],[7,1,19]],
    }
    for W,E in expected_critical.items():
        rows=[]
        for p in profiles(m,W):
            x=branch(m,W,prev_cap,p)
            if x is not None:rows.append(x)
        assert [r['degree_counts'] for r in rows]==expected_profiles[W]
        lb=min(r['corrected_integer_weight_lower_bound'] for r in rows)
        assert lb==E,(W,lb,E)
        critical[str(W)]={'uniform_lower_bound':lb,'profiles':rows}

    out={'pass':5198,'status':'THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_34',
      'q':5,'leader_size_closed':33,'target_distance':625,
      'previous_adjacent_pair_cap':prev_cap,'raw_deletion_cap':raw,
      'corrected_parity_minorant':'1_{r odd} >= r-2*C(r,2)+(36/35)*C(r,3)-(48/5)*C(r,8), 0<=r<=8',
      'parity_rows':parity,
      'full_apartment_bound':'8*A8 <= P5 <= 16*m, hence A8<=2*m. The first inequality uses unique apartment completion of a five-edge path; the second counts at most 2*2 extensions on each side of its central edge.',
      'pair_only_N1_le_43_lower':pair43,'pair_only_N1_44_lower':pair44,
      'existing_coupled_safe_layers':safe,'critical_corrected_layers':critical,
      'critical_uniform_bounds':{str(k):v for k,v in expected_critical.items()},
      'conclusion':'All m=33 adjacent-pair layers through the raw cap 60 have apartment weight >625. Therefore every q5 apartment-code word of weight <625 has minimum chamber leader at least 34.',
      'connection':'The leader-33 wall was not a failure of the triple law; it was the price paid by the 6/7 cubic coefficient for allowing r=8. Charging only fully occupied apartments raises the cubic coefficient to 36/35 while controlling the correction by the P5 path count.',
      'boundary':'This closes leader 33 only. The q5/all-q minimum-distance theorem and the weight-625 equality shell remain open for leaders >=34.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
