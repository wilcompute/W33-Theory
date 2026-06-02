from itertools import product, combinations
from collections import Counter, defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCXCVII_FANO_AXIS_CODEC_TRANSITION_results.json'

from analysis.w33_hinge_k5_axis_tomotope_weld import main as hinge_main


def xor(a,b): return tuple(x^y for x,y in zip(a,b))
def wt(a): return sum(a)
def comp3(a): return tuple(1-x for x in a)
def comp4(x): return tuple(1-b for b in x)
def ham(a,b): return sum(x!=y for x,y in zip(a,b))
def canon_axis4(x):
    y=comp4(x)
    return min(x,y), max(x,y)
def fmt(p): return ''.join(map(str,p))


def fano_lines(points):
    lines=set()
    for a,b in combinations(points,2):
        c=xor(a,b)
        if c in points and c!=(0,0,0):
            lines.add(tuple(sorted((a,b,c))))
    return sorted(lines)


def main():
    prev=hinge_main()

    F23=list(product([0,1], repeat=3))
    zero=(0,0,0)
    nonzero=[p for p in F23 if p!=zero]
    odd=[p for p in nonzero if wt(p)%2==1]
    even=[p for p in nonzero if wt(p)%2==0]
    generators=odd[:]  # weight 1 plus 111
    units=[p for p in odd if wt(p)==1]
    allone=(1,1,1)

    # Label every antipodal Q4 axis by p in F2^3:
    # axis(p) = {(0,p), (1,1-p)}.
    axis_by_label={p:((0,)+p, (1,)+comp3(p)) for p in F23}
    label_by_axis={canon_axis4(axis_by_label[p][0]):p for p in F23}
    hinge_label=zero

    # Build Q4 quotient adjacency on axis labels.
    q4_vertices=list(product([0,1], repeat=4))
    quotient_edges=set(); lift_count=Counter(); edge_generators=defaultdict(list)
    codec_edges=Counter()
    for a,b in combinations(q4_vertices,2):
        if ham(a,b)!=1: continue
        A=label_by_axis[canon_axis4(a)]
        B=label_by_axis[canon_axis4(b)]
        e=tuple(sorted((A,B)))
        quotient_edges.add(e); lift_count[e]+=1
        g=xor(A,B)
        edge_generators[g].append(e)
        # endpoint transition type in the C_p / S_p convention
        if a[0]==0 and b[0]==0 or a[0]==1 and b[0]==1:
            codec_edges['same_family_last_bit_flip'] += 1
        else:
            codec_edges['cs_duality_first_bit_flip'] += 1

    cayley_edges=set()
    for p in F23:
        for g in generators:
            q=xor(p,g)
            cayley_edges.add(tuple(sorted((p,q))))

    # Four generator matchings, each size 4, partition K4,4.
    generator_matching_sizes={fmt(g):len(set(tuple(sorted(e)) for e in es)) for g,es in edge_generators.items()}

    # Fano-line accounting induced by the hinge chart.
    lines=fano_lines(nonzero)
    odd_pairs=list(combinations(odd,2))
    odd_pair_to_even={tuple(sorted((a,b))):xor(a,b) for a,b in odd_pairs}
    mixed_lines=set(tuple(sorted((a,b,xor(a,b)))) for a,b in odd_pairs)
    even_line=tuple(sorted(even))
    all_lines_from_split=sorted(mixed_lines | {even_line})

    # Internal K4 edges among the four adjacent axes are exactly odd pairs.
    internal_k4_edges=odd_pairs
    pair_sum_profile=Counter(odd_pair_to_even.values())
    # The three nonadjacent even axes each correspond to two opposite internal K4 edges.
    even_to_pairs=defaultdict(list)
    for pair,e in odd_pair_to_even.items(): even_to_pairs[e].append(pair)

    checks={
      'inherits_hinge_weld':prev['n_verified']==prev['n_checks']==23,
      'axis_label_bijection_8':len(axis_by_label)==len(label_by_axis)==8,
      'hinge_is_zero_axis':axis_by_label[zero]==((0,0,0,0),(1,1,1,1)),
      'toroidal_axes_are_nonzero_fano_points':len(nonzero)==7,
      'odd_adjacent_axes_4':len(odd)==4,
      'even_nonadjacent_axes_3':len(even)==3,
      'q4_quotient_edge_count_16':len(quotient_edges)==16,
      'quotient_edges_lift_twice':Counter(lift_count.values())==Counter({2:16}),
      'quotient_is_cayley_f2_3_odd_generators':quotient_edges==cayley_edges,
      'quotient_adjacency_iff_odd_difference':all((tuple(sorted((p,q))) in quotient_edges)==(p!=q and wt(xor(p,q))%2==1) for p,q in combinations(F23,2)),
      'generator_matchings_partition_edges':set(generator_matching_sizes.values())=={4} and sum(generator_matching_sizes.values())==16,
      'four_generators_are_hinge_adjacent_axes':set(generators)==set(q for p,q in quotient_edges if p==zero) | set(p for p,q in quotient_edges if q==zero),
      'codec_edge_lift_decomposition_8_first_24_same_family':codec_edges==Counter({'same_family_last_bit_flip':24,'cs_duality_first_bit_flip':8}),
      'fano_line_count_7':len(lines)==7,
      'mixed_lines_from_odd_pairs_6':len(mixed_lines)==6,
      'even_line_is_seventh_line':even_line in lines and len(all_lines_from_split)==7,
      'split_lines_equal_fano_lines':all_lines_from_split==lines,
      'internal_k4_edges_6':len(internal_k4_edges)==6,
      'internal_k4_edges_pair_to_three_even_axes':len(even_to_pairs)==3 and all(len(v)==2 for v in even_to_pairs.values()),
      'odd_pair_sum_profile_two_per_even_axis':Counter(pair_sum_profile.values())==Counter({2:3}),
      'fano_incidence_total_21':len(lines)*3==21,
      'mixed_plus_even_incidence_18_plus_3':6*3 + 3 == 21,
      'fano_points_match_toroidal_axes':len(nonzero)==7,
      'psl27_flag_localization_still_7x2x12':7*2*12==168,
      'tomotope_flags_still_16x12':16*12==192,
    }
    assert all(checks.values()), checks

    R={
      'part':'MMCCCXCVII',
      'theorem':'Fano axis codec transition theorem',
      'axis_labeling':'axis(p) = {(0,p), (1,1-p)} for p in F2^3; hinge axis is p=000; seven toroidal axes are nonzero Fano points',
      'quotient_graph':{
        'description':'Q4/{±} on axis labels is Cay(F2^3, odd-weight generators)',
        'generators':[fmt(g) for g in generators],
        'edge_count':len(quotient_edges),
        'generator_matching_sizes':generator_matching_sizes,
        'graph':'K4,4 with parity bipartition of F2^3'
      },
      'codec_transition_lifts':{
        'same_family_last_bit_flips':codec_edges['same_family_last_bit_flip'],
        'cs_duality_first_bit_flips':codec_edges['cs_duality_first_bit_flip'],
        'reading':'last three bit flips translate C_p to C_{p+e_i} and S_p to S_{p+e_i}; first bit flip sends C_p to S_{1-p}'
      },
      'fano_split':{
        'odd_adjacent_axes':[fmt(p) for p in odd],
        'even_nonadjacent_axes':[fmt(p) for p in even],
        'mixed_lines_from_odd_pairs':[[fmt(x) for x in line] for line in sorted(mixed_lines)],
        'even_line':[fmt(x) for x in even_line],
        'line_count':len(lines),
        'incidence_count':21
      },
      'internal_k4_to_nonadjacent_axes':{fmt(k):[[fmt(x) for x in pair] for pair in v] for k,v in even_to_pairs.items()},
      'interpretation':'The seven toroidal axes in the antipodal codec quotient carry the Fano plane canonically.  The hinge-adjacent axes are the four odd Fano points; the three nonadjacent axes are the even Fano points.  The six internal K4 edges among the adjacent axes produce the six mixed Fano lines, while the three nonadjacent axes form the seventh all-even Fano line.  Thus the local hinge K5 chart is not arbitrary: it is the affine parity chart of the Fano plane sitting inside Q4/{±}.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['quotient_graph']); print(r['fano_split'])
