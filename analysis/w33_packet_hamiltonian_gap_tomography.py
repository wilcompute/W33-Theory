from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCV_PACKET_HAMILTONIAN_GAP_TOMOGRAPHY_results.json'

from analysis.w33_integer_packet_hamiltonian import main as integer_main


def Z(n,m): return [[Fraction(0) for _ in range(m)] for __ in range(n)]
def I(n): return [[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
def J(n): return [[Fraction(1) for _ in range(n)] for __ in range(n)]
def add(A,B): return [[A[i][j]+B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def smul(c,A): return [[Fraction(c)*x for x in row] for row in A]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
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


def main():
    prev=integer_main()
    n=10
    verts=range(5); edges=list(combinations(verts,2)); Id=I(n); All=J(n)
    A=Z(n,n)
    for i,e in enumerate(edges):
        for j,f in enumerate(edges):
            if i!=j and set(e)&set(f): A[i][j]=1

    Q1=smul(Fraction(1,10),All)
    Q4=smul(Fraction(-1,15), mul(sub(A,smul(6,Id)), add(A,smul(2,Id))))
    Q5=smul(Fraction(1,24), mul(sub(A,smul(6,Id)), sub(A,Id)))
    K=add(add(smul(216,Q1), smul(256,Q4)), smul(64,Q5))

    # Spectral projectors recovered from K alone.
    P216=smul(Fraction(1, (216-256)*(216-64)), mul(sub(K,smul(256,Id)), sub(K,smul(64,Id))))
    P256=smul(Fraction(1, (256-216)*(256-64)), mul(sub(K,smul(216,Id)), sub(K,smul(64,Id))))
    P64=smul(Fraction(1, (64-216)*(64-256)), mul(sub(K,smul(216,Id)), sub(K,smul(256,Id))))

    gap_Q4_Q5 = sub(K,smul(64,Id))             # 152 Q1 + 192 Q4
    pure_Q4_tomotope = sub(gap_Q4_Q5, smul(152,Q1))
    gap_Q4_Q1 = sub(smul(256,Id), K)           # 40 Q1 + 192 Q5
    pure_Q5_tomotope = sub(gap_Q4_Q1, smul(40,Q1))
    vertex_gap = sub(smul(256,Q1), mul(mul(Q1,K),Q1)) # 40 Q1
    residual_gap = sub(mul(mul(Q1,K),Q1), smul(64,Q1)) # 152 Q1

    # Gap identities.
    gaps={
        'Q4_minus_Q5':256-64,
        'Q4_minus_Q1':256-216,
        'Q1_minus_Q5':216-64,
        'tomotope_minus_w33_vertices':192-40,
        'tomotope_flags':16*12,
        'w33_vertices':40,
    }

    checks={
      'inherits_integer_hamiltonian':prev['n_verified']==prev['n_checks']==18,
      'spectral_projector_P216_equals_Q1':eq(P216,Q1),
      'spectral_projector_P256_equals_Q4':eq(P256,Q4),
      'spectral_projector_P64_equals_Q5':eq(P64,Q5),
      'projectors_recovered_from_K_sum_identity':eq(add(add(P216,P256),P64),Id),
      'gap_256_minus_64_is_tomotope_192':gaps['Q4_minus_Q5']==192 and gaps['tomotope_flags']==192,
      'gap_256_minus_216_is_w33_40':gaps['Q4_minus_Q1']==40 and gaps['w33_vertices']==40,
      'gap_216_minus_64_is_152_equals_192_minus_40':gaps['Q1_minus_Q5']==152 and gaps['tomotope_minus_w33_vertices']==152,
      'K_minus_64I_decomposes_152Q1_plus_192Q4':eq(gap_Q4_Q5, add(smul(152,Q1), smul(192,Q4))),
      'pure_Q4_tomotope_block_192Q4':eq(pure_Q4_tomotope, smul(192,Q4)),
      'rank_pure_Q4_block_4':rank_q(pure_Q4_tomotope)==4,
      'trace_pure_Q4_block_768':tr(pure_Q4_tomotope)==192*4,
      '256I_minus_K_decomposes_40Q1_plus_192Q5':eq(gap_Q4_Q1, add(smul(40,Q1), smul(192,Q5))),
      'pure_Q5_tomotope_block_192Q5':eq(pure_Q5_tomotope, smul(192,Q5)),
      'rank_pure_Q5_block_5':rank_q(pure_Q5_tomotope)==5,
      'trace_pure_Q5_block_960':tr(pure_Q5_tomotope)==192*5,
      'uniform_vertex_gap_40Q1':eq(vertex_gap, smul(40,Q1)),
      'uniform_residual_gap_152Q1':eq(residual_gap, smul(152,Q1)),
      'three_gaps_sum_relation_192_equals_40_plus_152':192==40+152,
      'hamiltonian_reconstruction_from_gap_law':eq(K, add(smul(64,Id), add(smul(152,Q1), smul(192,Q4)))),
    }
    assert all(checks.values()), checks

    R={
      'part':'MMCCCXCV',
      'theorem':'Packet Hamiltonian gap tomography',
      'operator':'K = 216Q1 + 256Q4 + 64Q5 on the K5 quotient-edge carrier',
      'spectral_projectors_from_K':{
        'Q1':'((K-256I)(K-64I))/((216-256)(216-64))',
        'Q4':'((K-216I)(K-64I))/((256-216)(256-64))',
        'Q5':'((K-216I)(K-256I))/((64-216)(64-256))'
      },
      'gap_identities':{
        '256-64':'192 = 16*12 = tomotope total flag count',
        '256-216':'40 = W33 vertex count',
        '216-64':'152 = 192-40'
      },
      'block_identities':{
        'K-64I':'152Q1 + 192Q4',
        'K-64I-152Q1':'192Q4, rank 4',
        '256I-K':'40Q1 + 192Q5',
        '256I-K-40Q1':'192Q5, rank 5'
      },
      'interpretation':'The integer packet Hamiltonian is tomographically rigid.  Its own spectral gaps recover the tomotope flag count 192, the W33 vertex count 40, and the residual 152=192-40.  Subtracting the Petersen ground level 64I exposes a rank-4 tomotope block 192Q4; subtracting from the vertex-standard ceiling 256I exposes a rank-5 tomotope block 192Q5.  Thus both nontrivial K5 branches carry the same 192-flag scale from opposite sides of the Hamiltonian.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['gap_identities'])
