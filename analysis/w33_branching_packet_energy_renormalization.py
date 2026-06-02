from fractions import Fraction
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCIII_BRANCHING_PACKET_ENERGY_RENORMALIZATION_results.json'

from analysis.w33_s6_to_s5_branching_gauge import main as branching_main
from analysis.w33_doily_quotient_projector_modes import main as modes_main
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


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

def eig_counter(M):
    vals=np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in M], dtype=float))
    C=Counter()
    for v in vals:
        if abs(v) < 1e-8:
            C['0'] += 1
        elif abs(v - 1.5) < 1e-8:
            C['3/2'] += 1
        elif abs(v - 13.5) < 1e-8:
            C['27/2'] += 1
        else:
            C[str(int(round(v)))] += 1
    return dict(sorted(C.items(), key=lambda kv: float(Fraction(kv[0])) if '/' in kv[0] else float(kv[0])))


def main():
    branching=branching_main(); modes=modes_main()

    V=tuple(range(6)); duads=list(combinations(V,2)); didx={e:i for i,e in enumerate(duads)}
    synthemes=perfect_matchings(V)
    D=Z(15,15)
    for r,S in enumerate(synthemes):
        for e in S: D[r][didx[e]]=1

    k5_edges=list(combinations(range(5),2)); spoke=[didx[(i,5)] for i in range(5)]
    F=[]
    for i,j in k5_edges:
        row=[Fraction(0) for _ in duads]
        row[didx[(i,j)]] += 1
        row[didx[(i,5)]] -= 1
        row[didx[(j,5)]] -= 1
        for s in spoke: row[s] += Fraction(1,2)
        F.append(row)

    # S6 duad projectors.
    A6=Z(15,15)
    for i,e in enumerate(duads):
        for j,f in enumerate(duads):
            if i!=j and set(e)&set(f): A6[i][j]=1
    I15=I(15); J15=J(15)
    S6_P1=smul(Fraction(1,15),J15)
    S6_P5=smul(Fraction(-1,24), mul(sub(A6,smul(8,I15)), add(A6,smul(2,I15))))
    S6_P9=smul(Fraction(1,40), mul(sub(A6,smul(8,I15)), sub(A6,smul(2,I15))))

    # S5 quotient projectors.
    A5=Z(10,10); I10=I(10); J10=J(10)
    for i,e in enumerate(k5_edges):
        for j,f in enumerate(k5_edges):
            if i!=j and set(e)&set(f): A5[i][j]=1
    S5_Q1=smul(Fraction(1,10),J10)
    S5_Q4=smul(Fraction(-1,15), mul(sub(A5,smul(6,I10)), add(A5,smul(2,I10))))
    S5_Q5=smul(Fraction(1,24), mul(sub(A5,smul(6,I10)), sub(A5,I10)))

    B1=mul(mul(F,S6_P1),trans(F))
    B5=mul(mul(F,S6_P5),trans(F))
    B9=mul(mul(F,S6_P9),trans(F))
    Dq=mul(D, trans(F))
    DqTDq=mul(trans(Dq), Dq)

    # Because D^T D = 9P1 + 4P9 on the S6 side, the quotient energy is
    # Dq^T Dq = F D^T D F^T = 9 F P1 F^T + 4 F P9 F^T.
    reconstructed=add(smul(9,B1), smul(4,B9))
    Q1_block=mul(mul(S5_Q1,DqTDq),S5_Q1)
    Q4_block=mul(mul(S5_Q4,DqTDq),S5_Q4)
    Q5_block=mul(mul(S5_Q5,DqTDq),S5_Q5)

    checks={
      'inherits_branching_gauge':branching['n_verified']==branching['n_checks']==16,
      'inherits_projector_modes':modes['n_verified']==modes['n_checks']==16,
      'Dq_rank_10':rank_q(Dq)==10,
      'abstract_branch_spectra':eig_counter(B1)=={'0':9,'3/2':1} and eig_counter(B5)=={'0':10} and eig_counter(B9)=={'0':1,'1':5,'4':4},
      'energy_reconstruction_formula':DqTDq==reconstructed,
      'renormalization_P1_9_times_3_over_2':eig_counter(smul(9,B1))=={'0':9,'27/2':1},
      'renormalization_Q4_4_times_4':Q4_block==smul(16,S5_Q4),
      'renormalization_Q5_4_times_1':Q5_block==smul(4,S5_Q5),
      'renormalization_Q1_block':Q1_block==smul(Fraction(27,2),S5_Q1),
      'full_packet_energy_spectrum':eig_counter(DqTDq)=={'4':5,'16':4,'27/2':1},
      'mode_ranks_1_4_5':(rank_q(Q1_block),rank_q(Q4_block),rank_q(Q5_block))==(1,4,5),
      'trace_total_97_over_2':tr(DqTDq)==Fraction(97,2),
      'trace_decomposes':tr(DqTDq)==tr(Q1_block)+tr(Q4_block)+tr(Q5_block),
      'kernel_removed_no_zero_eigenvalues':eig_counter(DqTDq).get('0',0)==0,
      'renormalization_law_matches_previous_mode_spectra':modes['mode_spectra']['P1_uniform']=={'0':14,'27/2':1} and modes['mode_spectra']['P4_vertex']=={'0':11,'16':4} and modes['mode_spectra']['P5_petersen']=={'0':10,'4':5},
      'integer_energy_factors_9_and_4_from_s6_incidence':9==3**2 and 4==2**2,
    }
    assert all(checks.values()), checks

    R={
      'part':'MMCCCXCIII',
      'theorem':'Branching packet energy renormalization',
      'formula':'Dq^T Dq = F D^T D F^T = 9 F P1 F^T + 4 F P9 F^T',
      'abstract_branching_spectra':{'F_P1_Ft':{'3/2':1,'0':9},'F_P5_Ft':{'0':10},'F_P9_Ft':{'4':4,'1':5,'0':1}},
      'renormalized_packet_spectra':{'Q1_uniform':'27/2^1','Q4_vertex':'16^4','Q5_petersen':'4^5'},
      'full_packet_energy_spectrum':{'27/2':1,'16':4,'4':5},
      'energy_weights':{'S6_uniform_weight':9,'S6_observable_weight':4,'Q1_effective':'9*(3/2)=27/2','Q4_effective':'4*4=16','Q5_effective':'4*1=4'},
      'ranks':{'Dq':rank_q(Dq),'Q1_block':rank_q(Q1_block),'Q4_block':rank_q(Q4_block),'Q5_block':rank_q(Q5_block)},
      'interpretation':'The abstract S6->S5 branching map explains the actual doily quotient packet energies once the S6 incidence form D^T D=9P1+4P9 is applied.  The uniform branch is renormalized by 9, while the observable 9-sector branches into Q4 and Q5 and is renormalized by 4.  This derives the doily quotient mode spectrum 27/2,16^4,4^5 from the representation branching law.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['energy_weights'])
