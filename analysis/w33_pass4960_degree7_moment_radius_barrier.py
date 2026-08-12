#!/usr/bin/env python3
"""Pass4960 — degree-7 moment barrier for the K=[360,36,20]_2 covering radius.

Pass4951 used A_3(K^perp)=1080 and a cubic one-sided moment inequality to prove
rho(K)<=173.  This pass asks whether the next frozen dual shells A_4,...,A_7
can lower the ceiling using the standard truncated one-sided moment relaxation.

For a coset y+K set X=wt(c)-180 and
  T_j(y)=sum_{h in K^perp, wt(h)=j} (-1)^(y.h).
MacWilliams/Krawtchouk identities give centered moments through degree seven.
A necessary condition for support X>=-a is positivity of both the ordinary
moment matrix M_3=(m_{i+j}) and the localizing matrix
L_3(a)=(m_{i+j+1}+a m_{i+j}), 0<=i,j<=3.

At a=7 (leader 173) we exhibit exact signed-shell values within every frozen
absolute/parity bound for which both matrices are positive definite.  Hence
no argument that uses only these degree<=7 moment identities, the independent
bounds |T_j|<=A_j, and one-sided support positivity can rule out 173.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4960_DEGREE7_MOMENT_RADIUS_BARRIER.json'

A={3:1080,4:10530,5:127656,6:2329680,7:37193040}
T={3:-1080,4:-1936,5:75316,6:830590,7:-37193040}

def det_fraction(A):
    M=[list(map(Fraction,row)) for row in A]
    n=len(M);det=Fraction(1)
    for c in range(n):
        q=next((r for r in range(c,n) if M[r][c]),None)
        if q is None:return Fraction(0)
        if q!=c:M[c],M[q]=M[q],M[c];det=-det
        p=M[c][c];det*=p
        for j in range(c,n):M[c][j]/=p
        for r in range(c+1,n):
            f=M[r][c]
            if f:
                for j in range(c,n):M[r][j]-=f*M[c][j]
    return det

def leading_minors(M):
    return [det_fraction([row[:k] for row in M[:k]]) for k in range(1,len(M)+1)]

def main()->int:
    for j in range(3,8):
        assert abs(T[j])<=A[j]
        assert (T[j]-A[j])%2==0  # signed sum of A_j many +/-1 characters

    m={0:Fraction(1),1:Fraction(0),2:Fraction(90)}
    m[3]=Fraction(-3,4)*T[3]
    m[4]=Fraction(24255)+Fraction(3,2)*T[4]
    m[5]=Fraction(-2685,4)*T[3]-Fraction(15,4)*T[5]
    m[6]=Fraction(10874340)+2010*T[4]+Fraction(45,4)*T[6]
    m[7]=Fraction(-5037081,8)*T[3]-Fraction(56175,8)*T[5]-Fraction(315,8)*T[7]
    assert m=={0:Fraction(1),1:Fraction(0),2:Fraction(90),3:Fraction(810),
      4:Fraction(21351),5:Fraction(442515),6:Fraction(32654235,2),
      7:Fraction(3231244695,2)}

    M=[[m[i+j] for j in range(4)] for i in range(4)]
    a=7
    L=[[m[i+j+1]+a*m[i+j] for j in range(4)] for i in range(4)]
    md=leading_minors(M);ld=leading_minors(L)
    assert md==[1,90,536490,2855774841174]
    assert ld==[7,1980,79022673,27807585328055790]
    assert all(x>0 for x in md+ld)

    out={
      'pass':4960,
      'code':'K=[360,36,20]_2',
      'frozen_dual_shells':{str(k):v for k,v in A.items()},
      'centered_moment_identities':{
        'm3':'-(3/4)T3',
        'm4':'24255+(3/2)T4',
        'm5':'-(2685/4)T3-(15/4)T5',
        'm6':'10874340+2010T4+(45/4)T6',
        'm7':'-(5037081/8)T3-(56175/8)T5-(315/8)T7'},
      'distance_173_relaxation_witness':{
        'a':a,'delta':173,
        'signed_shell_values':{str(k):v for k,v in T.items()},
        'moments':{str(k):str(v) for k,v in m.items()},
        'ordinary_moment_matrix_leading_minors':[str(x) for x in md],
        'one_sided_localizing_matrix_leading_minors':[str(x) for x in ld],
        'both_positive_definite':True},
      'covering_radius':{'proved_interval_from_Pass4951':[134,173],'improved_here':False},
      'theorem':'The shellwise degree-7 one-sided moment relaxation cannot improve rho(K)<=173. There is an exact feasible truncated moment functional at a=7 satisfying all frozen A3..A7 absolute/parity bounds, with both the ordinary and support-localizing moment matrices positive definite.',
      'consequence':'Any further moment-based improvement must use correlations among the signed shell sums T_j, additional coset identities, or higher structure; independent bounds |T_j|<=A_j through j=7 are insufficient.',
      'boundary':'This is a theorem about the stated truncated relaxation, not an existence proof for an actual distance-173 coset. The exact covering radius remains open.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
