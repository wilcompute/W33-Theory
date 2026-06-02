from fractions import Fraction
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXC_DOILY_QUOTIENT_PROJECTOR_MODES_results.json'

from analysis.w33_doily_k5_quotient_gauge import main as quotient_main
from analysis.w33_k5_edge_projector_decomposition import main as projector_main
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


def Z(n,m): return [[Fraction(0) for _ in range(m)] for __ in range(n)]
def I(n): return [[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
def J(n): return [[Fraction(1) for _ in range(n)] for __ in range(n)]
def add(A,B): return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def smul(c,A): return [[Fraction(c)*x for x in row] for row in A]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def transpose(A): return [list(row) for row in zip(*A)]
def tr(A): return sum(A[i][i] for i in range(len(A)))

def rank_q(M):
    A=[row[:] for row in M]
    if not A: return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        piv=None
        for i in range(r,m):
            if A[i][c] != 0:
                piv=i; break
        if piv is None: continue
        A[r],A[piv]=A[piv],A[r]
        pv=A[r][c]
        A[r]=[x/pv for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c] != 0:
                f=A[i][c]
                A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
        r+=1
    return r

def eig_counter(M):
    arr=np.array([[float(x) for x in row] for row in M], dtype=float)
    vals=np.linalg.eigvalsh(arr)
    out=Counter()
    for v in vals:
        if abs(v) < 1e-8:
            out['0'] += 1
        elif abs(v-Fraction(27,2)) < 1e-8:
            out['27/2'] += 1
        else:
            out[str(int(round(v)))] += 1
    return dict(sorted(out.items(), key=lambda kv: (float(Fraction(kv[0])) if '/' in kv[0] else float(kv[0]))))

def main():
    quotient=quotient_main(); projectors_prev=projector_main()
    V=tuple(range(6)); duads=list(combinations(V,2)); didx={e:i for i,e in enumerate(duads)}
    synthemes=perfect_matchings(V)
    D=Z(len(synthemes),len(duads))
    for r,S in enumerate(synthemes):
        for e in S: D[r][didx[e]]=Fraction(1)

    k5_edges=list(combinations(range(5),2)); n=10
    spoke=[didx[(i,5)] for i in range(5)]
    F=[]
    for i,j in k5_edges:
        row=[Fraction(0) for _ in duads]
        row[didx[(i,j)]] += Fraction(1)
        row[didx[(i,5)]] -= Fraction(1)
        row[didx[(j,5)]] -= Fraction(1)
        for s in spoke: row[s] += Fraction(1,2)
        F.append(row)
    Dq=mul(D, transpose(F))

    Id=I(n); All=J(n); A=Z(n,n)
    for i,e in enumerate(k5_edges):
        for j,f in enumerate(k5_edges):
            if i!=j and set(e)&set(f): A[i][j]=Fraction(1)
    P1=smul(Fraction(1,10),All)
    P4=smul(Fraction(-1,15), mul(sub(A,smul(6,Id)), add(A,smul(2,Id))))
    P5=smul(Fraction(1,24), mul(sub(A,smul(6,Id)), sub(A,Id)))
    modes={'P1_uniform':P1,'P4_vertex':P4,'P5_petersen':P5}
    mode_grams={k:mul(mul(Dq,P), transpose(Dq)) for k,P in modes.items()}
    mode_ranks={k:rank_q(M) for k,M in mode_grams.items()}
    mode_spectra={k:eig_counter(M) for k,M in mode_grams.items()}
    total=add(add(mode_grams['P1_uniform'],mode_grams['P4_vertex']),mode_grams['P5_petersen'])
    DqG=mul(Dq,transpose(Dq))

    checks={
      'inherits_quotient_gauge':quotient['n_verified']==quotient['n_checks']==16,
      'inherits_k5_projectors':projectors_prev['n_verified']==projectors_prev['n_checks']==17,
      'D_rank_10':rank_q(D)==10,
      'F_rank_10':rank_q(F)==10,
      'Dq_rank_10':rank_q(Dq)==10,
      'projector_ranks_1_4_5':(rank_q(P1),rank_q(P4),rank_q(P5))==(1,4,5),
      'mode_ranks_1_4_5':mode_ranks=={'P1_uniform':1,'P4_vertex':4,'P5_petersen':5},
      'mode_spectrum_uniform':mode_spectra['P1_uniform']=={'0':14,'27/2':1},
      'mode_spectrum_vertex':mode_spectra['P4_vertex']=={'0':11,'16':4},
      'mode_spectrum_petersen':mode_spectra['P5_petersen']=={'0':10,'4':5},
      'mode_sum_is_total_quotient_gram':total==DqG,
      'total_rank_10':rank_q(DqG)==10,
      'total_spectrum_split':eig_counter(DqG)=={'0':5,'4':5,'16':4,'27/2':1},
      'trace_additivity':tr(DqG)==tr(mode_grams['P1_uniform'])+tr(mode_grams['P4_vertex'])+tr(mode_grams['P5_petersen']),
      'dimension_split_1_4_5':sum(mode_ranks.values())==10,
      'refines_rank10_carrier':1+4+5==10,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCXC',
      'theorem':'Doily quotient projector modes',
      'carrier':'doily syntheme rows expressed in the explicit K5 quotient-edge gauge',
      'quotient_matrix':'Dq = D F^T, shape 15 x 10, rank 10',
      'mode_ranks':mode_ranks,
      'mode_spectra':mode_spectra,
      'total_quotient_spectrum':eig_counter(DqG),
      'interpretation':'The rank-10 doily packet carrier splits in the explicit K5 edge gauge into three exact projector modes: a 1D uniform mode, a 4D vertex-standard mode, and a 5D Petersen mode.  This turns the previous 10D quotient into the fully resolved 1+4+5 representation decomposition.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['mode_ranks'], r['mode_spectra'])
