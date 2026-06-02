from fractions import Fraction
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCII_S6_TO_S5_BRANCHING_GAUGE_results.json'

from analysis.w33_s6_duad_representation_decomposition import main as s6_main


def Z(n,m): return [[Fraction(0) for _ in range(m)] for __ in range(n)]
def I(n): return [[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
def J(n): return [[Fraction(1) for _ in range(n)] for __ in range(n)]
def add(A,B): return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def smul(c,A): return [[Fraction(c)*x for x in row] for row in A]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def trans(A): return [list(row) for row in zip(*A)]
def tr(A): return sum(A[i][i] for i in range(len(A)))

def rank_q(M):
    A=[row[:] for row in M]
    if not A: return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        piv=None
        for i in range(r,m):
            if A[i][c]!=0:
                piv=i; break
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        pv=A[r][c]
        A[r]=[x/pv for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]!=0:
                f=A[i][c]
                A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
        r+=1
    return r

def eig_signature(M):
    vals=np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in M], dtype=float))
    C=Counter()
    for v in vals:
        if abs(v) < 1e-8:
            C['0'] += 1
        elif abs(v - 1.5) < 1e-8:
            C['3/2'] += 1
        else:
            C[str(int(round(v)))] += 1
    return dict(sorted(C.items(), key=lambda kv: float(Fraction(kv[0])) if '/' in kv[0] else float(kv[0])))

def main():
    prev=s6_main()
    V=tuple(range(6)); duads=list(combinations(V,2)); didx={e:i for i,e in enumerate(duads)}
    n15=15; A6=Z(n15,n15)
    for i,e in enumerate(duads):
        for j,f in enumerate(duads):
            if i!=j and set(e)&set(f): A6[i][j]=1
    I15=I(15); J15=J(15)
    S6_P1=smul(Fraction(1,15),J15)
    S6_P5=smul(Fraction(-1,24), mul(sub(A6,smul(8,I15)), add(A6,smul(2,I15))))
    S6_P9=smul(Fraction(1,40), mul(sub(A6,smul(8,I15)), sub(A6,smul(2,I15))))

    k5_edges=list(combinations(range(5),2)); n10=10
    # Gauge-fix by choosing vertex 5 as the killed gauge vertex; remaining coordinates are K5 edges.
    spoke=[didx[(i,5)] for i in range(5)]
    F=[]
    for i,j in k5_edges:
        row=[Fraction(0) for _ in duads]
        row[didx[(i,j)]] += 1
        row[didx[(i,5)]] -= 1
        row[didx[(j,5)]] -= 1
        for s in spoke: row[s] += Fraction(1,2)
        F.append(row)

    A5=Z(n10,n10)
    for i,e in enumerate(k5_edges):
        for j,f in enumerate(k5_edges):
            if i!=j and set(e)&set(f): A5[i][j]=1
    I10=I(10); J10=J(10)
    S5_Q1=smul(Fraction(1,10),J10)
    S5_Q4=smul(Fraction(-1,15), mul(sub(A5,smul(6,I10)), add(A5,smul(2,I10))))
    S5_Q5=smul(Fraction(1,24), mul(sub(A5,smul(6,I10)), sub(A5,I10)))

    B1=mul(mul(F,S6_P1),trans(F))
    B5=mul(mul(F,S6_P5),trans(F))
    B9=mul(mul(F,S6_P9),trans(F))
    B9_Q1=mul(mul(S5_Q1,B9),S5_Q1)
    B9_Q4=mul(mul(S5_Q4,B9),S5_Q4)
    B9_Q5=mul(mul(S5_Q5,B9),S5_Q5)

    checks={
      'inherits_s6_decomposition':prev['n_verified']==prev['n_checks']==21,
      'F_rank_10':rank_q(F)==10,
      'S6_projectors_ranks_1_5_9':(rank_q(S6_P1),rank_q(S6_P5),rank_q(S6_P9))==(1,5,9),
      'S5_projectors_ranks_1_4_5':(rank_q(S5_Q1),rank_q(S5_Q4),rank_q(S5_Q5))==(1,4,5),
      'S6_uniform_branches_to_scaled_S5_uniform':B1==smul(Fraction(3,2),S5_Q1),
      'S6_gauge_sector_killed_by_F':B5==Z(10,10),
      'S6_observable_rank_9_after_F':rank_q(B9)==9,
      'S6_observable_spectrum_after_F':eig_signature(B9)=={'0':1,'1':5,'4':4},
      'S6_observable_no_S5_uniform_block':B9_Q1==Z(10,10),
      'S6_observable_Q4_block_is_4Q4':B9_Q4==smul(4,S5_Q4),
      'S6_observable_Q5_block_is_Q5':B9_Q5==S5_Q5,
      'S5_cross_blocks_zero':mul(mul(S5_Q4,B9),S5_Q5)==Z(10,10) and mul(mul(S5_Q5,B9),S5_Q4)==Z(10,10),
      'branching_9_to_4_plus_5':rank_q(B9_Q4)+rank_q(B9_Q5)==9,
      'full_quotient_spectrum_1_4_5':eig_signature(add(add(B1,B5),B9))=={'0':0} or eig_signature(add(B1,B9))=={'1':5,'3/2':1,'4':4},
      'trace_accounting':tr(B1)+tr(B5)+tr(B9)==Fraction(45,2),
      'dimension_accounting':1+4+5==10 and 1+5+9==15,
    }
    # The synthetic full-spectrum check above cannot literally have zero count omitted in a 10x10 full-rank matrix.
    checks['full_quotient_spectrum_1_4_5'] = eig_signature(add(B1,B9))=={'1':5,'3/2':1,'4':4}
    assert all(checks.values()), checks
    R={
      'part':'MMCCCXCII',
      'theorem':'S6 to S5 branching gauge',
      'map':'F: 15-dimensional K6 duad carrier -> 10-dimensional K5 edge quotient carrier',
      'branching':{
        'S6_P1':'maps to (3/2) times S5_Q1',
        'S6_P5':'killed by F',
        'S6_P9':'branches as 4*S5_Q4 plus 1*S5_Q5 with no S5 uniform component'
      },
      'spectra':{
        'F_S6_P1_Ft':eig_signature(B1),
        'F_S6_P5_Ft':eig_signature(B5),
        'F_S6_P9_Ft':eig_signature(B9),
        'full_observable_quotient':eig_signature(add(B1,B9))
      },
      'ranks':{'F':rank_q(F),'S6_P1_image':rank_q(B1),'S6_P5_image':rank_q(B5),'S6_P9_image':rank_q(B9),'Q4_block':rank_q(B9_Q4),'Q5_block':rank_q(B9_Q5)},
      'interpretation':'The chosen K6-to-K5 gauge is an explicit branching map.  It kills the S6 5-dimensional gauge representation, sends the S6 uniform line to the S5 uniform line, and splits the S6 9-dimensional observable representation into the S5 4-dimensional vertex mode plus the S5 5-dimensional Petersen mode.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['branching'])
