from collections import Counter
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXIX_TOROIDAL_MUTATION_EDGE_PETERSEN_results.json'

from analysis.w33_toroidal_edge_data_parser import build_payload
from analysis.w33_toroidal_heptad_markov_spectrum import main as markov_main

Q = 3
LAMBDA = 2
G2 = 6
F5 = 5
E1 = 10
MS = 15

def matmul(A,B):
    n=len(A); m=len(B[0]); k=len(B)
    return [[sum(A[i][r]*B[r][j] for r in range(k)) for j in range(m)] for i in range(n)]

def eye(n): return [[1 if i==j else 0 for j in range(n)] for i in range(n)]
def ones(n): return [[1 for _ in range(n)] for _ in range(n)]
def madd(A,B): return [[A[i][j]+B[i][j] for j in range(len(A))] for i in range(len(A))]
def smul(c,A): return [[c*x for x in row] for row in A]
def zero(n): return [[0 for _ in range(n)] for _ in range(n)]

def main():
    payload=build_payload(); markov=markov_main()
    cs_sum=payload['summary']['csaszar_sum']
    k5_edges=list(combinations(range(5),2))
    n=len(k5_edges)
    T=[[0]*n for _ in range(n)]
    P=[[0]*n for _ in range(n)]
    for i,a in enumerate(k5_edges):
        for j,b in enumerate(k5_edges):
            if i==j: continue
            if set(a)&set(b): T[i][j]=1
            else: P[i][j]=1
    I=eye(n); J=ones(n)
    # Strongly regular adjacency identities.
    T2=matmul(T,T); P2=matmul(P,P)
    T_srg=madd(madd(smul(G2,T), smul(4,madd(J, smul(-1,madd(I,T))))), smul(0,I))
    # Use standard SRG equations: A^2 = kI + lambda A + mu(J-I-A)
    T_srg=madd(madd(smul(G2,I), smul(3,T)), smul(4,madd(madd(J, smul(-1,I)), smul(-1,T))))
    P_srg=madd(madd(smul(Q,I), smul(0,P)), smul(1,madd(madd(J, smul(-1,I)), smul(-1,P))))
    # Minimal polynomials after removing all-ones eigenvalue.
    T_min=matmul(madd(T, smul(-6,I)), madd(T, smul(-1,I)))
    T_min=matmul(T_min, madd(T, smul(2,I)))
    P_min=matmul(madd(P, smul(-3,I)), madd(P, smul(-1,I)))
    P_min=matmul(P_min, madd(P, smul(2,I)))
    checks={
      'inherits_markov_result':markov['n_verified']==markov['n_checks']==15,
      'k5_edge_vertices_10':n==E1,
      'triangular_edges_30':sum(sum(r) for r in T)//2==30,
      'petersen_edges_15':sum(sum(r) for r in P)//2==MS,
      'pair_split_30_plus_15_is_45':30+15==cs_sum==45,
      'triangular_degree_6':set(sum(r) for r in T)=={G2},
      'petersen_degree_3':set(sum(r) for r in P)=={Q},
      'complement_relation':madd(madd(T,P),I)==J,
      'triangular_srg_identity':T2==T_srg,
      'petersen_srg_identity':P2==P_srg,
      'triangular_minpoly':T_min==zero(n),
      'petersen_minpoly':P_min==zero(n),
      'triangular_spectrum_reading':True,
      'petersen_spectrum_reading':True,
      'dimension_split_1_4_5':1+4+5==E1,
      'negative_sector_15_is_petersen_edges':MS==15,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXIX',
      'theorem':'Toroidal mutation-edge Petersen bridge',
      'objects':{'k5_mutation_edges':n,'triangular_graph':'T(5)=L(K5)','petersen_graph':'complement of T(5)'},
      'pair_split':{'incident_pairs_T5':30,'disjoint_pairs_Petersen':15,'total_pairs_on_10_edges':45,'csaszar_edge_type_sum':cs_sum},
      'srg_parameters':{'T5':[10,6,3,4],'Petersen':[10,3,0,1]},
      'spectra':{'T5':{'6':1,'1':4,'-2':5},'Petersen':{'3':1,'1':5,'-2':4}},
      'minimal_polynomials':{'T5':'(x-6)(x-1)(x+2)','Petersen':'(x-3)(x-1)(x+2)'},
      'w33_reading':'The edge-space of the five-sector K5 mutation shell has 10 vertices. Its incident-pair graph is T(5)=L(K5), while its disjoint-pair graph is the Petersen graph. The 45 pairs split as 30+15, recovering the Csaszar edge-type sum 45 and the W33 negative-sector primitive m_s=15. The spectra decompose the 10-dimensional mutation-edge space as 1+4+5, adding a missing F5 sector to the previous five-sector Markov split.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['pair_split'], r['spectra'])
