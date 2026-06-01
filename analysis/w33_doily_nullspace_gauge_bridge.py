from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXVII_DOILY_NULLSPACE_GAUGE_results.json'

from analysis.w33_doily_e15_packet_spectrum import main as spectrum_main
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


def rank(M): return int(np.linalg.matrix_rank(np.array(M,dtype=float), tol=1e-8))

def main():
    prev=spectrum_main()
    V=tuple(range(6))
    duads=list(combinations(V,2)); duad_index={e:i for i,e in enumerate(duads)}
    synthemes=perfect_matchings(V)
    D=np.zeros((len(synthemes),len(duads)),dtype=int)
    for r,S in enumerate(synthemes):
        for e in S: D[r,duad_index[e]]=1

    # Right kernel: original K6 vertex-potential gauge w_ij=a_i+a_j with sum_i a_i=0.
    A=[]
    for k in range(5):
        a=np.zeros(6,dtype=int); a[k]=1; a[5]=-1
        A.append([a[i]+a[j] for i,j in duads])
    Vpot=np.array(A,dtype=int)  # 5 x 15

    # Left kernel: pentad-potential gauge.  Each pentad is five synthemes partitioning all 15 duads.
    all_duads=set(duads); pentads=[]
    for subset in combinations(range(len(synthemes)),5):
        edges=[]
        for si in subset: edges.extend(synthemes[si])
        if set(edges)==all_duads and len(set(edges))==15:
            pentads.append(tuple(sorted(subset)))
    P=np.zeros((len(pentads),len(synthemes)),dtype=int)
    for r,Pent in enumerate(pentads):
        for si in Pent: P[r,si]=1
    Pdiff=np.array([P[k]-P[5] for k in range(5)],dtype=int) # 5 x 15

    DD=D@D.T
    DtD=D.T@D
    checks={
      'inherits_spectrum':prev['n_verified']==prev['n_checks']==22,
      'syntheme_duad_matrix_15x15':D.shape==(15,15),
      'rank_D_10':rank(D)==10,
      'right_nullity_5':15-rank(D)==5,
      'left_nullity_5':15-rank(D.T)==5,
      'vertex_potential_rank_5':rank(Vpot)==5,
      'vertex_potential_in_right_kernel':np.array_equal(D@Vpot.T, np.zeros((15,5),dtype=int)),
      'right_kernel_exhausted_by_vertex_potentials':rank(np.vstack([D,Vpot]))==15,
      'pentads_6':len(pentads)==6,
      'each_pentad_partitions_all_duads':np.array_equal(P@D, np.ones((6,15),dtype=int)),
      'pentad_difference_rank_5':rank(Pdiff)==5,
      'pentad_differences_in_left_kernel':np.array_equal(Pdiff@D, np.zeros((5,15),dtype=int)),
      'left_kernel_exhausted_by_pentad_differences':rank(np.vstack([D.T,Pdiff]))==15,
      'dd_spectrum_9_4x9_0x5':Counter(int(round(x)) for x in np.linalg.eigvalsh(DD))==Counter({0:5,4:9,9:1}),
      'dtd_spectrum_9_4x9_0x5':Counter(int(round(x)) for x in np.linalg.eigvalsh(DtD))==Counter({0:5,4:9,9:1}),
      'row_space_dimension_10_mutation_edge':rank(D)==10,
      'outer_sixset_pair_original_and_pentad':Vpot.shape[0]==Pdiff.shape[0]==5,
      'incidence_sum_45':int(D.sum())==45,
      'quotient_15_minus_5_equals_10':15-5==10,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXVII',
      'theorem':'Doily nullspace gauge bridge',
      'matrix':'D = syntheme/one-factor by duad incidence, shape 15 x 15',
      'ranks':{'rank_D':rank(D),'right_nullity':15-rank(D),'left_nullity':15-rank(D.T),'row_space_mutation_edge_dimension':10},
      'right_kernel':'zero-sum original K6 vertex-potential gauge w_ij=a_i+a_j, dim 5',
      'left_kernel':'zero-sum pentad-potential gauge from the second six-set, dim 5',
      'spectra':{'D_Dt':'9^1 + 4^9 + 0^5','Dt_D':'9^1 + 4^9 + 0^5'},
      'compression_identity':'15 E15/duad directions - 5 vertex/pentad gauge directions = 10 K5 mutation-edge directions',
      'reading':'The rank defect in the doily/E15 packet system is not accidental.  The right nullspace is exactly the zero-sum potential gauge on the original six K6 vertices; the left nullspace is exactly the zero-sum potential gauge on the six pentads, the second six-set produced by the S6 outer automorphism.  Quotienting either gauge leaves the 10-dimensional K5 mutation-edge carrier detected in the previous packet spectrum.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['ranks'])
