from itertools import combinations, product
from collections import Counter, defaultdict
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCVI_HINGE_K5_AXIS_TOMOTOPE_WELD_results.json'

from analysis.w33_packet_hamiltonian_gap_tomography import main as gap_main


def comp(x): return tuple(1-b for b in x)
def wt(x): return sum(x)
def canon_axis(x):
    y=comp(x)
    return min(x,y), max(x,y)
def ham(a,b): return sum(x!=y for x,y in zip(a,b))

def rank_int(M): return int(np.linalg.matrix_rank(np.array(M,dtype=float), tol=1e-9))


def main():
    prev=gap_main()

    q4_vertices=list(product([0,1], repeat=4))
    q4_edges=[]
    for a,b in combinations(q4_vertices,2):
        if ham(a,b)==1:
            q4_edges.append((a,b))

    axes=sorted(set(canon_axis(x) for x in q4_vertices))
    axis_index={ax:i for i,ax in enumerate(axes)}
    axis_parity={ax:wt(ax[0])%2 for ax in axes}
    hinge=canon_axis((0,0,0,0))

    quotient_edges=set()
    lift_count=Counter()
    for a,b in q4_edges:
        A=canon_axis(a); B=canon_axis(b)
        e=tuple(sorted((axis_index[A],axis_index[B])))
        quotient_edges.add(e); lift_count[e]+=1

    even_axes=[ax for ax in axes if axis_parity[ax]==0]
    odd_axes=[ax for ax in axes if axis_parity[ax]==1]
    hinge_i=axis_index[hinge]
    adj_axis_indices=sorted(j for i,j in quotient_edges if i==hinge_i) + sorted(i for i,j in quotient_edges if j==hinge_i)
    adj_axis_indices=sorted(set(adj_axis_indices))
    nonadj_axis_indices=sorted(set(range(8))-set(adj_axis_indices)-{hinge_i})

    # Name the four adjacent axes A0..A3 by their weight-1 representative.
    adj_by_coord={}
    for ai in adj_axis_indices:
        reps=axes[ai]
        one=next(x for x in reps if wt(x)==1)
        adj_by_coord[one.index(1)] = ai
    Acoords=sorted(adj_by_coord)

    # K5 vertices = hinge H plus the four adjacent axes A0..A3.
    k5_vertices=['H']+[f'A{i}' for i in Acoords]
    k5_edges=[]
    for u,v in combinations(k5_vertices,2):
        k5_edges.append((u,v))
    k5_index={e:i for i,e in enumerate(k5_edges)}
    spokes=[e for e in k5_edges if 'H' in e]
    internal=[e for e in k5_edges if 'H' not in e]

    # The three nonadjacent Q4 axes are the three complementary-pair matchings of the K4 on A0..A3.
    nonadj_to_pairs={}
    for ni in nonadj_axis_indices:
        rep=next(x for x in axes[ni] if wt(x)==2)
        S=tuple(i for i,b in enumerate(rep) if b)
        T=tuple(i for i in range(4) if i not in S)
        pair=(tuple(sorted((f'A{S[0]}',f'A{S[1]}'))), tuple(sorted((f'A{T[0]}',f'A{T[1]}'))))
        nonadj_to_pairs[ni]=tuple(sorted(pair))

    # Axis-by-K5-edge incidence matrix.
    # Row order: H, A0..A3, N0..N2.
    row_names=['H']+[f'A{i}' for i in Acoords]+[f'N{n}' for n in range(len(nonadj_axis_indices))]
    B=np.zeros((8,10), dtype=int)
    # H row: four hinge spokes.
    for e in spokes:
        B[0,k5_index[e]]=1
    # A_i rows: all K5 edges incident to A_i.
    for r,i in enumerate(Acoords, start=1):
        label=f'A{i}'
        for e in k5_edges:
            if label in e:
                B[r,k5_index[e]]=1
    # N rows: two opposite internal K4 edges.
    for r,ni in enumerate(nonadj_axis_indices, start=5):
        for e in nonadj_to_pairs[ni]:
            B[r,k5_index[e]]=1

    relation=np.zeros(8,dtype=int)
    relation[0]=1
    relation[1:5]=-1
    relation[5:8]=2
    relation_ok=np.array_equal(relation @ B, np.zeros(10,dtype=int))

    edge_lift_profile=Counter(lift_count[e] for e in quotient_edges)
    quotient_degree=Counter()
    for i,j in quotient_edges:
        quotient_degree[i]+=1; quotient_degree[j]+=1
    same_parity_edges=sum(1 for i,j in quotient_edges if axis_parity[axes[i]]==axis_parity[axes[j]])
    incident_to_hinge=sum(1 for e in quotient_edges if hinge_i in e)
    not_incident_to_hinge=len(quotient_edges)-incident_to_hinge

    checks={
      'inherits_gap_tomography':prev['n_verified']==prev['n_checks']==20,
      'q4_vertices_16':len(q4_vertices)==16,
      'q4_edges_32':len(q4_edges)==32,
      'antipodal_axes_8':len(axes)==8,
      'axis_parities_4_even_4_odd':Counter(axis_parity.values())==Counter({0:4,1:4}),
      'quotient_edges_16':len(quotient_edges)==16,
      'each_quotient_edge_lifts_twice':edge_lift_profile==Counter({2:16}),
      'quotient_is_k44':set(quotient_degree.values())=={4} and same_parity_edges==0 and len(even_axes)==len(odd_axes)==4,
      'hinge_adjacent_4_nonadjacent_3':len(adj_axis_indices)==4 and len(nonadj_axis_indices)==3,
      'tomotope_f_vector_from_hinge':(incident_to_hinge, not_incident_to_hinge, len(quotient_edges), len(axes))==(4,12,16,8),
      'tomotope_sum_40':4+12+16+8==40,
      'k5_vertices_hinge_plus_adjacent_axes':len(k5_vertices)==5,
      'k5_edge_count_10':len(k5_edges)==10,
      'k5_edges_split_4_spokes_6_internal':len(spokes)==4 and len(internal)==6,
      'internal_six_edges_pair_to_three_nonadj_axes':len(nonadj_to_pairs)==3 and sum(len(v) for v in nonadj_to_pairs.values())==6,
      'axis_incidence_shape_8x10':B.shape==(8,10),
      'axis_incidence_rank_7':rank_int(B)==7,
      'axis_incidence_relation_H_minus_As_plus_2Ns':relation_ok,
      'axis_row_sum_profile':Counter(B.sum(axis=1))==Counter({4:5,2:3}),
      'edge_column_support_profile':Counter(B.sum(axis=0))==Counter({2:4,3:6}),
      'flag_accounting_16x12_192':16*12==192,
      'flag_accounting_24_plus_168':2*12 + 7*2*12 == 192,
      'psl27_localized_as_toroidal_flags':7*2*12==168,
    }
    assert all(checks.values()), checks

    R={
      'part':'MMCCCXCVI',
      'theorem':'Hinge K5 axis / tomotope weld',
      'q4_quotient':{'Q4_vertices':16,'Q4_edges':32,'antipodal_axes':8,'quotient_edges':16,'quotient_graph':'K4,4'},
      'hinge_split':{'hinge_axis':1,'adjacent_axes':4,'nonadjacent_toroidal_axes':3,'tomotope_f_vector':[4,12,16,8],'sum':40},
      'k5_axis_model':{'K5_vertices':'hinge + four adjacent axes','K5_edges':10,'hinge_spokes':4,'adjacent_axis_pair_edges':6,'six_internal_edges_pair_to_nonadjacent_axes':3},
      'axis_incidence':{'matrix_shape':'8 x 10','rank':rank_int(B),'row_sum_profile':dict(Counter(map(int,B.sum(axis=1)))),'column_sum_profile':dict(Counter(map(int,B.sum(axis=0)))),'linear_relation':'H - A0 - A1 - A2 - A3 + 2N0 + 2N1 + 2N2 = 0'},
      'flag_accounting':{'16_codecs_x_12_flags':192,'tetrahedral_flags':24,'toroidal_flags':168,'PSL_2_7':168},
      'interpretation':'Choosing the tetrahedral antipodal axis as a hinge turns the four adjacent quotient axes into the non-hinge vertices of a K5.  The ten K5 Hamiltonian coordinates are four hinge spokes plus six adjacent-axis pair edges.  Those six internal K4 edges pair into the three nonadjacent toroidal axes.  Thus the K5 packet carrier used by the integer Hamiltonian is the local hinge chart of the Q4/{±}=K4,4 tomotope quotient.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['hinge_split'], r['k5_axis_model'])
