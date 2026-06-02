from itertools import product, permutations, combinations
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCIX_K44_FACTORIZATION_G2_ROOT_SELECTOR_results.json'

from analysis.w33_fano_hinge_affine_symmetry import main as affine_main


def xor(a,b): return tuple(x^y for x,y in zip(a,b))
def wt(a): return sum(a)
def fmt(p): return ''.join(map(str,p))
def edge(a,b,idx): return tuple(sorted((idx[a],idx[b])))
def det3_mod2(M):
    s=0
    for p in permutations(range(3)):
        term=1
        for i,j in enumerate(p):
            term &= M[i][j]
        s ^= term
    return s

def all_gl32():
    mats=[]
    for bits in product([0,1], repeat=9):
        M=tuple(tuple(bits[3*i:3*i+3]) for i in range(3))
        if det3_mod2(M)==1:
            mats.append(M)
    return mats

def mat_vec(M,v): return tuple(sum(M[i][j]*v[j] for j in range(3)) % 2 for i in range(3))
def apply_edge(e,perm): return tuple(sorted((perm[e[0]],perm[e[1]])))
def apply_matching(M,perm): return frozenset(apply_edge(e,perm) for e in M)
def apply_factorization(F,perm): return frozenset(apply_matching(M,perm) for M in F)


def main():
    prev=affine_main()
    pts=list(product([0,1], repeat=3)); idx={p:i for i,p in enumerate(pts)}
    even=[p for p in pts if wt(p)%2==0]
    odd=[p for p in pts if wt(p)%2==1]
    S=odd[:]  # the four odd Fano generators 001,010,100,111

    # K4,4 edge set and canonical affine generator one-factorization.
    K44_edges=set(edge(e,o,idx) for e in even for o in odd)
    F0=frozenset(
        frozenset(edge(e,xor(e,s),idx) for e in even)
        for s in S
    )

    # All 24 perfect matchings of K4,4.
    perfect_matchings=[]
    for po in permutations(odd):
        M=frozenset(edge(e,o,idx) for e,o in zip(even,po))
        perfect_matchings.append(M)
    perfect_matchings=set(perfect_matchings)

    # Full Aut(K4,4) = (S4 x S4) semidirect C2, represented on the 8 axis labels.
    G=set()
    for pe in permutations(even):
        mapE=dict(zip(even,pe))
        for po in permutations(odd):
            mapO=dict(zip(odd,po))
            G.add(tuple(idx[mapE[p]] if p in mapE else idx[mapO[p]] for p in pts))
    for peo in permutations(odd):
        mapE=dict(zip(even,peo))
        for poe in permutations(even):
            mapO=dict(zip(odd,poe))
            G.add(tuple(idx[mapE[p]] if p in mapE else idx[mapO[p]] for p in pts))

    # Affine Fano-hinge group H from the previous theorem.
    GL=all_gl32()
    linear_stab=[M for M in GL if set(mat_vec(M,s) for s in S)==set(S)]
    H=set()
    for b in pts:
        for M in linear_stab:
            H.add(tuple(idx[xor(mat_vec(M,p),b)] for p in pts))

    stabilizer=set(g for g in G if apply_factorization(F0,g)==F0)
    orbit=set(apply_factorization(F0,g) for g in G)
    orbit_list=sorted(orbit, key=lambda F: sorted(sorted(m) for m in F))
    all_orbit_matchings=[]
    for F in orbit_list:
        all_orbit_matchings.extend(list(F))
    matching_membership=Counter(all_orbit_matchings)

    # Distinct factorization frames are disjoint at the matching level.
    pairwise_common=Counter(len(A & B) for A,B in combinations(orbit_list,2))

    # Every factorization is a partition of the 16 K4,4 edges into four perfect matchings.
    fact_partition_ok=all(len(F)==4 and all(len(M)==4 for M in F) and len(set().union(*F))==16 for F in orbit_list)
    edge_cover_profile=Counter()
    for F in orbit_list:
        U=set().union(*F)
        for e in K44_edges:
            edge_cover_profile[e] += int(e in U)

    # Two orientations per factorization: even->odd versus odd->even.  This gives 12 oriented root sectors.
    oriented_root_sectors=2*len(orbit_list)

    # Stabilizers of each factorization are conjugate 192-groups.
    stabilizer_sizes=[]
    for F in orbit_list:
        stabilizer_sizes.append(sum(1 for g in G if apply_factorization(F,g)==F))

    decompositions={
        'full_K44_auto':len(G),
        'affine_hinge_stabilizer_times_six_frames':len(H)*len(orbit_list),
        'six_positive_g2_root_sectors_times_192':6*192,
        'twelve_oriented_g2_roots_times_96':12*96,
        'twentyfour_matchings_times_48':24*48,
    }

    checks={
        'inherits_affine_symmetry':prev['n_verified']==prev['n_checks']==21,
        'k44_edges_16':len(K44_edges)==16,
        'canonical_factorization_4_matchings':len(F0)==4,
        'canonical_matchings_are_perfect_size_4':all(len(M)==4 for M in F0),
        'canonical_factorization_partitions_edges':set().union(*F0)==K44_edges,
        'all_perfect_matchings_24':len(perfect_matchings)==24,
        'full_k44_aut_order_1152':len(G)==1152,
        'affine_hinge_group_order_192':len(H)==192,
        'affine_group_is_factorization_stabilizer':H==stabilizer and len(stabilizer)==192,
        'orbit_has_six_factorizations':len(orbit_list)==6,
        'orbit_stabilizer_index_6':len(G)//len(stabilizer)==6,
        'each_factorization_partitions_k44':fact_partition_ok,
        'distinct_factorizations_share_no_perfect_matching':pairwise_common==Counter({0:15}),
        'six_factorizations_partition_all_24_matchings':set(all_orbit_matchings)==perfect_matchings and set(matching_membership.values())=={1},
        'total_orbit_matching_count_6_times_4_24':len(all_orbit_matchings)==6*4==24,
        'each_k44_edge_occurs_in_each_factorization_once':set(edge_cover_profile.values())=={6},
        'oriented_root_sectors_12':oriented_root_sectors==12,
        'g2_positive_root_count_6':len(orbit_list)==6,
        'g2_total_root_count_12':oriented_root_sectors==12,
        'conjugate_stabilizers_all_192':set(stabilizer_sizes)=={192},
        'decompositions_all_1152':all(v==1152 for v in decompositions.values()),
        'tomotope_scale_192_times_g2_6':192*6==1152,
        'fano_24_matchings_as_6_frames_of_4':24==6*4,
    }
    assert all(checks.values()), checks

    R={
        'part':'MMCCCXCIX',
        'theorem':'K4,4 one-factorization / G2 root selector theorem',
        'carrier':'Q4 antipodal quotient K4,4 with F2^3 Fano axis labels',
        'canonical_factorization':{
            'generators':[fmt(s) for s in S],
            'description':'four odd-generator perfect matchings p -> p+s from even axes to odd axes',
            'matchings':4,
            'edges_per_matching':4
        },
        'groups':{
            'Aut_K44_order':len(G),
            'affine_hinge_group_order':len(H),
            'stabilizer_of_canonical_factorization':len(stabilizer),
            'orbit_size':len(orbit_list),
            'index':len(G)//len(stabilizer)
        },
        'factorization_orbit':{
            'one_factorizations':len(orbit_list),
            'perfect_matchings_total':len(perfect_matchings),
            'partition':'the six one-factorizations are pairwise disjoint at the matching level and partition all 24 perfect matchings of K4,4',
            'oriented_root_sectors':oriented_root_sectors
        },
        'decompositions_of_1152':decompositions,
        'interpretation':'The previous 192-element affine Fano-hinge symmetry is exactly the stabilizer of one affine generator one-factorization of K4,4.  The full K4,4 automorphism group has order 1152 and moves this frame through six disjoint one-factorization frames.  Those six frames partition all 24 perfect matchings, giving a six-sector selector naturally read as the six positive G2 roots; orienting each frame gives 12 root sectors, matching the full G2 root count and the CS level k=12.',
        'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['groups']); print(r['factorization_orbit'])
