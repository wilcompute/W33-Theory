#!/usr/bin/env python3
"""Pass5172: exact all-q incidence formula for gallery-distance-two pairs.

Let Y be any selected chamber set in W(3,q), viewed as an edge set of the
point-line Levi graph.  Write x_p and y_l for its selected degrees on points and
lines, m=|Y|, and N1 for adjacent selected chamber pairs.  If N is the point-line
incidence matrix, then

    x^T N y = m + 2 N1 + N2,

where N2 is the number of selected chamber pairs at gallery distance two.
Indeed a diagonal selected chamber contributes once, an adjacent pair contributes
in both orientations through its selected host chamber, and a distance-two pair
contributes once through its unique cross-incidence.  Girth eight forbids a
second cross-incidence.

For W(3,q), NN^T=(q+1)I+A, where A is the point graph.  Its eigenvalues are
(q+1)^2, 2q, 0, so the second singular value of N is sqrt(2q).  Writing W_P,W_L
for point- and line-centered adjacent-pair counts, W_P+W_L=N1, gives

 N2 <= m^2/(q^2+1)
       + sqrt(2q (m+2W_P-m^2/v)(m+2W_L-m^2/v))
       - (m+2N1),

v=(q+1)(q^2+1).  This couples the Delsarte N2 coordinate to the actual Levi
degree split.  The executable arithmetic below freezes the exact integer floors
for the current q=5,m=30 dense frontier.
"""
from __future__ import annotations
import json,math
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5172_ALLQ_INCIDENCE_N2_SPECTRAL_BRIDGE.json'


def floor_base_sqrt(base:Fraction,rad:Fraction):
    n=math.floor(float(base)+math.sqrt(float(rad)))
    def le(k):
        t=Fraction(k)-base
        return t<=0 or t*t<=rad
    while le(n+1):n+=1
    while not le(n):n-=1
    return n


def n2_spectral_upper(q,m,WP,WL):
    v=(q+1)*(q*q+1);W=WP+WL
    base=Fraction(m*m,q*q+1)-Fraction(m+2*W)
    a=Fraction(m+2*WP)-Fraction(m*m,v)
    b=Fraction(m+2*WL)-Fraction(m*m,v)
    assert a>=0 and b>=0
    rad=Fraction(2*q)*a*b
    return floor_base_sqrt(base,rad),base,rad


def side_profiles(m):
    out=[]
    for n3 in range(m//3+1):
      for n2 in range((m-3*n3)//2+1):
        n1=m-3*n3-2*n2
        W=n2+3*n3
        out.append({'degrees':(n1,n2,n3),'wedges':W,'vertices':n1+n2+n3})
    return out


def dense_table(q,m,W):
    rows=[]
    S=side_profiles(m)
    for L in S:
      for R in S:
        if L['wedges']+R['wedges']!=W:continue
        ub,base,rad=n2_spectral_upper(q,m,L['wedges'],R['wedges'])
        rows.append({'WP':L['wedges'],'WL':R['wedges'],'N2_upper':ub,
          'left_degree_counts':list(L['degrees']),'right_degree_counts':list(R['degrees']),
          'base_num':base.numerator,'base_den':base.denominator,
          'sqrt_rad_num':rad.numerator,'sqrt_rad_den':rad.denominator})
    return rows


def main():
    # Pure spectral checks: the incidence singular values follow from the GQ point
    # graph eigenvalues k=q(q+1), r=q-1, s=-(q+1).
    spec={}
    for q in (2,3,4,5,7,9):
        vals=((q+1)**2,2*q,0)
        assert vals==(q+1+q*(q+1),q+1+q-1,q+1-(q+1))
        spec[str(q)]={'NNt_eigenvalues':list(vals),'second_singular_squared':2*q}

    t51=dense_table(5,30,51);t52=dense_table(5,30,52)
    shell51=sorted(set((r['WP'],r['WL'],r['N2_upper']) for r in t51))
    shell52=sorted(set((r['WP'],r['WL'],r['N2_upper']) for r in t52))
    assert shell51==[(21,30,138),(23,28,139),(24,27,140),(25,26,140),
                     (26,25,140),(27,24,140),(28,23,139),(30,21,138)]
    assert shell52==[(22,30,140),(24,28,141),(25,27,141),(26,26,141),
                     (27,25,141),(28,24,141),(30,22,140)]

    out={'pass':5172,'status':'THEOREM_ALL_Q_LEVI_INCIDENCE_N2_SPECTRAL_BRIDGE',
      'exact_identity':'N2 = x^T N y - (m+2 N1)',
      'proof':'Expand x^TNy over Levi incidences. A selected chamber contributes once; each adjacent selected pair contributes twice, once for each orientation through a selected endpoint chamber; each gallery-distance-two pair contributes once through its unique cross-incidence. A second cross-incidence would make a Levi 4-cycle, impossible in a generalized quadrangle.',
      'incidence_spectrum':'NN^T=(q+1)I+A_point has eigenvalues (q+1)^2, 2q, 0, hence sigma_2(N)=sqrt(2q).',
      'spectral_upper':'N2 <= m^2/(q^2+1) + sqrt(2q (m+2WP-m^2/v)(m+2WL-m^2/v)) - (m+2N1), v=(q+1)(q^2+1).',
      'spectral_anchors':spec,
      'q5_m30_N1_51_split_bounds':[list(x) for x in shell51],
      'q5_m30_N1_52_split_bounds':[list(x) for x in shell52],
      'connection':'This removes N2 as a free association-scheme coordinate once the point/line adjacent-pair split is known. It is the first exact matrix bridge between the Levi degree profile and the chamber Delsarte program.',
      'boundary':'The identity and spectral inequality are exact for every selected chamber set in W(3,q). By themselves they do not close q5 leader 30; the current N1=51,52 sectors still need additional coupled path/fourth-order information.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main()
