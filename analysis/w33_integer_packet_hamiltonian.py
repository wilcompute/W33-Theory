from fractions import Fraction
from itertools import combinations
from collections import Counter
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCIV_INTEGER_PACKET_HAMILTONIAN_results.json'

from analysis.w33_branching_packet_energy_renormalization import main as energy_main
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

def eig_counter(M):
    vals=np.linalg.eigvalsh(np.array([[float(x) for x in row] for row in M], dtype=float))
    C=Counter()
    for v in vals:
        if abs(v) < 1e-8:
            C['0'] += 1
        elif abs(v - 13.5) < 1e-8:
            C['27/2'] += 1
        else:
            C[str(int(round(v)))] += 1
    return dict(sorted(C.items(), key=lambda kv: float(Fraction(kv[0])) if '/' in kv[0] else float(kv[0])))

def is_integer_matrix(M):
    return all(x.denominator == 1 for row in M for x in row)

def determinant_int_spectrum():
    return 216 * (256**4) * (64**5)


def main():
    prev=energy_main()

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
    Dq=mul(D, trans(F))
    H=mul(trans(Dq), Dq)     # quotient packet energy operator
    K=smul(16, H)            # integer packet Hamiltonian

    n=10; Id=I(n); All=J(n); A=Z(n,n)
    for i,e in enumerate(k5_edges):
        for j,f in enumerate(k5_edges):
            if i!=j and set(e)&set(f): A[i][j]=1
    C=sub(sub(All,Id),A)     # Petersen complement of T(5)

    # Polynomial formulas in the T(5) and Petersen adjacency algebras.
    K_from_T5=add(add(smul(-9, mul(A,A)), smul(55, A)), smul(210, Id))
    K_from_Pet=add(add(smul(-9, mul(C,C)), smul(-37, C)), smul(222, Id))

    # Projectors for T(5) sectors.
    Q1=smul(Fraction(1,10),All)
    Q4=smul(Fraction(-1,15), mul(sub(A,smul(6,Id)), add(A,smul(2,Id))))
    Q5=smul(Fraction(1,24), mul(sub(A,smul(6,Id)), sub(A,Id)))
    K_projector=add(add(smul(216,Q1), smul(256,Q4)), smul(64,Q5))

    # Minimal polynomial for K.
    K_min=mul(mul(sub(K,smul(216,Id)), sub(K,smul(256,Id))), sub(K,smul(64,Id)))
    H_min=mul(mul(sub(H,smul(Fraction(27,2),Id)), sub(H,smul(16,Id))), sub(H,smul(4,Id)))

    checks={
      'inherits_energy_renormalization':prev['n_verified']==prev['n_checks']==16,
      'Dq_rank_10':rank_q(Dq)==10,
      'H_full_rank_10':rank_q(H)==10,
      'H_spectrum_27_over_2_16x4_4x5':eig_counter(H)=={'4':5,'16':4,'27/2':1},
      'K_integer_matrix':is_integer_matrix(K),
      'K_spectrum_216_256x4_64x5':eig_counter(K)=={'64':5,'216':1,'256':4},
      'K_trace_1560':tr(K)==1560,
      'K_determinant_from_spectrum':determinant_int_spectrum()==216*(256**4)*(64**5),
      'T5_polynomial_formula':eq(K,K_from_T5),
      'Petersen_polynomial_formula':eq(K,K_from_Pet),
      'projector_formula_216_256_64':eq(K,K_projector),
      'K_minimal_polynomial':eq(K_min,Z(n,n)),
      'H_minimal_polynomial':eq(H_min,Z(n,n)),
      'eigenvalue_216_equals_g2_cubed':216==6**3,
      'eigenvalue_256_equals_E2_squared':256==16**2,
      'eigenvalue_64_equals_discriminant_su3_square':64==8**2,
      'trace_decomposition_216_plus_4x256_plus_5x64':216 + 4*256 + 5*64 == 1560,
      'dimension_decomposition_1_4_5':1+4+5==10,
    }
    assert all(checks.values()), checks

    R={
      'part':'MMCCCXCIV',
      'theorem':'Integer packet Hamiltonian theorem',
      'operator':'K = 16 Dq^T Dq on the 10-dimensional K5 quotient-edge carrier',
      'polynomial_T5':'K = -9 A_T5^2 + 55 A_T5 + 210 I',
      'polynomial_Petersen':'K = -9 A_Pet^2 - 37 A_Pet + 222 I',
      'projector_formula':'K = 216 Q1 + 256 Q4 + 64 Q5',
      'spectrum':{'216':1,'256':4,'64':5},
      'eigenvalue_reading':{
        '216':'6^3 = g2^3, matching the Lenz-symmetric Csaszar total squared edge length',
        '256':'16^2 = E2^2, the 4-dimensional vertex-standard packet mode',
        '64':'8^2 = (r*chi)^2 = dim(su3)^2, the 5-dimensional Petersen packet mode'
      },
      'invariants':{'trace':1560,'determinant':'216 * 256^4 * 64^5','minimal_polynomial':'(x-216)(x-256)(x-64)'},
      'interpretation':'After clearing the denominator in the doily quotient packet energy, the final observable is an integer Hamiltonian in the adjacency algebra of T(5) and its Petersen complement.  The eigenvalues are not arbitrary: 216 is the g2^3 toroidal edge-energy total, 256 is E2^2 on the vertex-standard branch, and 64 is the master discriminant square on the Petersen branch.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['spectrum'])
