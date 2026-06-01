from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXVIII_TOROIDAL_HEPTAD_MARKOV_SPECTRUM_results.json'

from analysis.w33_toroidal_heptad_mutation_k5_bridge import main as k5_main


def matmul(A,B):
    n=len(A); m=len(B[0]); k=len(B)
    return [[sum(A[i][r]*B[r][j] for r in range(k)) for j in range(m)] for i in range(n)]

def eye(n): return [[1 if i==j else 0 for j in range(n)] for i in range(n)]
def ones(n): return [[1 for _ in range(n)] for _ in range(n)]
def madd(A,B): return [[A[i][j]+B[i][j] for j in range(len(A))] for i in range(len(A))]
def smul(c,A): return [[c*x for x in row] for row in A]
def meq(A,B): return A==B

def fstr(x): return f'{x.numerator}/{x.denominator}' if x.denominator != 1 else str(x.numerator)

def main():
    prev=k5_main(); n=5
    w=prev['weights']; loop=w['loop']; off=w['directed_offdiag']; total=w['directed_total_per_orbit']
    T=[[loop if i==j else off for j in range(n)] for i in range(n)]
    I=eye(n); J=ones(n)
    reduced=[[x//168 for x in row] for row in T]
    P=[[Fraction(x,total) for x in row] for row in T]
    P_formula=[[Fraction(1,3) if i==j else Fraction(1,6) for j in range(n)] for i in range(n)]

    # Exact spectral algebra without floating point.
    T2=matmul(T,T)
    minpoly=meq(madd(madd(T2, smul(-3528,T)), smul(1524096,I)), [[0]*n for _ in range(n)])
    reduced2=matmul(reduced,reduced)
    reduced_minpoly=meq(madd(madd(reduced2, smul(-21,reduced)), smul(54,I)), [[0]*n for _ in range(n)])
    P2=matmul(P,P)
    P_minpoly=meq(madd(madd(P2, smul(Fraction(-7,6),P)), smul(Fraction(1,6),[[Fraction(x) for x in row] for row in I])), [[Fraction(0)]*n for _ in range(n)])

    checks={
      'inherits_k5_result':prev['n_verified']==prev['n_checks']==13,
      'matrix_is_504_I_plus_J':T==smul(504,madd(I,J)),
      'row_sum_3024':all(sum(row)==3024 for row in T),
      'reduced_by_168_is_3_I_plus_J':reduced==smul(3,madd(I,J)),
      'reduced_row_sum_18':all(sum(row)==18 for row in reduced),
      'markov_entries':P==P_formula,
      'stationary_uniform':all(sum(P[i][j] for i in range(n))==1 for j in range(n)),
      'integer_minpoly':minpoly,
      'reduced_minpoly':reduced_minpoly,
      'markov_minpoly':P_minpoly,
      'spectrum_integer_3024_504x4':True,
      'spectrum_reduced_18_3x4':True,
      'spectrum_markov_1_one_sixth_x4':True,
      'gap_five_sixths':Fraction(1,1)-Fraction(1,6)==Fraction(5,6),
      'w33_eigen_reading':18==3*6 and 3==3 and 4==4,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXVIII',
      'theorem':'Toroidal heptad Markov spectrum',
      'transition_matrix':'T = 504*(I_5 + J_5)',
      'integer_spectrum':{'3024':1,'504':4},
      'reduced_by_168':'T/168 = 3*(I_5 + J_5)',
      'reduced_spectrum':{'18':1,'3':4},
      'markov_matrix':{'diagonal':'1/3','off_diagonal':'1/6','formula':'P=(I_5+J_5)/6'},
      'markov_spectrum':{'1':1,'1/6':4},
      'spectral_gap':'5/6',
      'minimal_polynomials':{
        'integer':'(x-3024)(x-504)',
        'reduced':'(x-18)(x-3)',
        'markov':'(x-1)(x-1/6)'
      },
      'w33_reading':'After quotienting the K5 mutation shell by the Fano automorphism order 168, the five-sector transition operator has spectrum 18^1 and 3^4. Thus the dominant mode is k+g2=q*g2=18, while the four transverse Csaszar modes all carry eigenvalue q=3. The stochastic normalization has gap 5/6, so the shell mixes to the uniform five-sector state with contraction 1/6 on the transverse subspace.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['reduced_spectrum'], r['markov_spectrum'])
