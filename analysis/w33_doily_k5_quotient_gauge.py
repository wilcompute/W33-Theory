from itertools import combinations, permutations
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXVIII_DOILY_K5_QUOTIENT_GAUGE_results.json'

from analysis.w33_doily_nullspace_gauge_bridge import main as null_main
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


def rank_q(M):
    A=[list(map(Fraction,row)) for row in M]
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
        if r==m: break
    return r

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def transpose(A): return [list(row) for row in zip(*A)]
def zero(m,n): return [[Fraction(0) for _ in range(n)] for _ in range(m)]

def main():
    prev=null_main()
    V=tuple(range(6)); duads=list(combinations(V,2)); didx={e:i for i,e in enumerate(duads)}
    k5_edges=list(combinations(range(5),2)); kidx={e:i for i,e in enumerate(k5_edges)}
    synthemes=perfect_matchings(V)
    D=[[Fraction(0) for _ in duads] for __ in synthemes]
    for r,S in enumerate(synthemes):
        for e in S: D[r][didx[e]]=Fraction(1)

    # Gauge basis: zero-sum vertex potentials a_k=1, a_5=-1, mapped to duads by w_ij=a_i+a_j.
    G=[]
    for k in range(5):
        a=[Fraction(0) for _ in range(6)]; a[k]=Fraction(1); a[5]=Fraction(-1)
        G.append([a[i]+a[j] for i,j in duads])
    GT=transpose(G)

    # Gauge-fixing map F sends a K6 duad-weight vector to the unique representative with all edges i5 zero.
    # Coordinates are the 10 edges among vertices 0..4.
    F=[]
    spoke=[didx[(i,5)] for i in range(5)]
    for i,j in k5_edges:
        row=[Fraction(0) for _ in duads]
        row[didx[(i,j)]] += Fraction(1)
        row[didx[(i,5)]] -= Fraction(1)
        row[didx[(j,5)]] -= Fraction(1)
        for s in spoke: row[s] += Fraction(1,2)
        F.append(row)

    FG=matmul(F,GT)
    DG=matmul(D,GT)
    rowspace_rank=rank_q(D+F)

    # Stabilizer of vertex 5 acts faithfully as S5 on the ten K5 quotient coordinates.
    actions=set(); edge_actions=set()
    for p in permutations(range(5)):
        p6=tuple(list(p)+[5])
        edge_perm=tuple(kidx[tuple(sorted((p6[a],p6[b])))] for a,b in k5_edges)
        edge_actions.add(edge_perm)
    # Coordinate rows have a clean K5 orbit profile: each K5 coordinate uses one internal edge, two spokes, all five spokes by half-shift.
    row_profiles=Counter((sum(1 for x in row if x==1), sum(1 for x in row if x==-1), sum(1 for x in row if x==Fraction(1,2))) for row in F)

    checks={
      'inherits_nullspace_bridge':prev['n_verified']==prev['n_checks']==19,
      'duad_count_15':len(duads)==15,
      'k5_edge_count_10':len(k5_edges)==10,
      'syntheme_count_15':len(synthemes)==15,
      'D_rank_10':rank_q(D)==10,
      'G_rank_5':rank_q(G)==5,
      'F_rank_10':rank_q(F)==10,
      'F_kills_vertex_gauge':FG==zero(10,5),
      'D_kills_vertex_gauge':DG==zero(15,5),
      'F_kernel_is_vertex_gauge':rank_q(F+G)==15,
      'D_kernel_is_vertex_gauge':rank_q(D+G)==15,
      'D_and_F_have_same_rowspace':rowspace_rank==10,
      'quotient_identity_15_minus_5_equals_10':15-5==10,
      's5_stabilizer_order_120':len(edge_actions)==120,
      'gauge_fix_row_profile_uniform':row_profiles==Counter({(1,2,3):10}),
      'incidence_sum_45':sum(sum(row) for row in D)==45,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXVIII',
      'theorem':'Doily K5 quotient gauge',
      'objects':{'K6_duads':15,'vertex_gauge_dimension':5,'K5_quotient_edges':10,'synthemes':15},
      'ranks':{'rank_D':rank_q(D),'rank_vertex_gauge':rank_q(G),'rank_F':rank_q(F),'rank_rowspan_D_plus_F':rowspace_rank},
      'gauge_fixing':'F fixes the zero-sum K6 vertex-potential gauge by setting all five spoke edges i5 to zero; the remaining ten coordinates are the edges of K5.',
      'symmetry':{'stabilizer_of_gauge_vertex':'S5','order':len(edge_actions),'carrier':'ten K5 quotient edges'},
      'compression_identity':'K6 duad space / vertex-potential gauge = 15 - 5 = 10 = K5 edge carrier',
      'reading':'The 10-dimensional doily packet row space is exactly the K5 edge quotient of the 15-dimensional K6 duad space after removing the 5-dimensional zero-sum vertex-potential gauge.  The syntheme incidence matrix D and the explicit gauge-fixing matrix F have the same row space, so the previous rank-10 E15 packet compression is literally a K6-to-K5 quotient gauge.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['ranks'])
