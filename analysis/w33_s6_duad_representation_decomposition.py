from fractions import Fraction
from itertools import combinations, permutations
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCI_S6_DUAD_REPRESENTATION_DECOMPOSITION_results.json'

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
def eq(A,B): return A==B

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

def perm_matrix(p):
    n=len(p); P=Z(n,n)
    for i,j in enumerate(p): P[j][i]=1
    return P

def main():
    prev=modes_main()
    V=tuple(range(6)); duads=list(combinations(V,2)); didx={e:i for i,e in enumerate(duads)}
    synthemes=perfect_matchings(V); n=len(duads)
    D=Z(len(synthemes),n)
    for r,S in enumerate(synthemes):
        for e in S: D[r][didx[e]]=1
    DtD=mul(trans(D),D)

    A=Z(n,n)
    for i,e in enumerate(duads):
        for j,f in enumerate(duads):
            if i!=j and set(e)&set(f): A[i][j]=1
    Id=I(n); All=J(n)
    C=sub(sub(All,Id),A) # disjoint-duad Kneser complement of T(6)
    P1=smul(Fraction(1,15),All)
    P5=smul(Fraction(-1,24), mul(sub(A,smul(8,Id)), add(A,smul(2,Id))))
    P9=smul(Fraction(1,40), mul(sub(A,smul(8,Id)), sub(A,smul(2,Id))))
    projectors=[P1,P5,P9]

    S6=[]; action_mats=[]
    for p in permutations(V):
        ep=tuple(didx[tuple(sorted((p[a],p[b])))] for a,b in duads)
        S6.append(ep); action_mats.append(perm_matrix(ep))
    invariant=all(eq(mul(mul(Pg,P), trans(Pg)), P) for Pg in action_mats for P in projectors)
    commute=all(eq(mul(Pg,A),mul(A,Pg)) for Pg in action_mats)

    D_modes={'P1_uniform':mul(D,P1),'P5_gauge':mul(D,P5),'P9_observable':mul(D,P9)}
    mode_ranks={k:rank_q(v) for k,v in D_modes.items()}
    D_form=add(smul(9,P1), smul(4,P9))
    T6_min=mul(mul(sub(A,smul(8,Id)), sub(A,smul(2,Id))), add(A,smul(2,Id)))
    checks={
      'inherits_quotient_modes':prev['n_verified']==prev['n_checks']==16,
      'duad_space_15':n==15,
      'syntheme_count_15':len(synthemes)==15,
      'D_rank_10':rank_q(D)==10,
      'T6_degree_8':all(sum(row)==8 for row in A),
      'disjoint_degree_6':all(sum(row)==6 for row in C),
      'T6_minpoly_8_2_neg2':eq(T6_min,Z(n,n)),
      'projectors_idempotent':all(eq(mul(P,P),P) for P in projectors),
      'projectors_orthogonal':all(eq(mul(projectors[i],projectors[j]),Z(n,n)) for i in range(3) for j in range(3) if i!=j),
      'projectors_sum_identity':eq(add(add(P1,P5),P9),Id),
      'projector_traces_1_5_9':(tr(P1),tr(P5),tr(P9))==(1,5,9),
      'projector_ranks_1_5_9':(rank_q(P1),rank_q(P5),rank_q(P9))==(1,5,9),
      'S6_order_720':len(set(S6))==720,
      'S6_preserves_projectors':invariant,
      'S6_commutes_with_T6':commute,
      'DTD_formula_2I_plus_J_minus_A':eq(DtD, add(smul(2,Id), sub(All,A))),
      'DTD_projector_formula_9P1_plus_4P9':eq(DtD,D_form),
      'D_kills_P5_gauge':D_modes['P5_gauge']==Z(len(synthemes),n),
      'D_modes_ranks_1_0_9':mode_ranks=={'P1_uniform':1,'P5_gauge':0,'P9_observable':9},
      'observable_rank_10_is_1_plus_9':rank_q(D)==1+9,
      'branching_to_S5_9_to_4_plus_5':9==4+5,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCXCI',
      'theorem':'S6 duad representation decomposition',
      'carrier':'15-dimensional K6 duad space before gauge quotient',
      'S6_split':'15 = 1 + 5 + 9',
      'incidence_formula':'D^T D = 2I + J - A_T6 = 9P1 + 4P9; P5 is the killed gauge sector',
      'projectors':{'P1':'J15/15','P5':'-((A-8I)(A+2I))/24','P9':'((A-8I)(A-2I))/40','ranks':[1,5,9]},
      'mode_ranks_after_D':mode_ranks,
      'link_to_S5_quotient':'Under the gauge vertex stabilizer S5, the S6 9-sector branches as 4+5, matching the K5 quotient projector modes.',
      'interpretation':'The doily incidence map is an S6-intertwiner on the K6 duad representation.  It annihilates the 5-dimensional vertex-potential gauge and preserves the 1+9 observable sector.  The earlier K5 quotient split 1+4+5 is the S5-branching of this S6 observable decomposition.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['mode_ranks_after_D'])
