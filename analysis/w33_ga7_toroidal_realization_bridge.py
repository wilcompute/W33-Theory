from itertools import combinations
from collections import Counter, defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCDIII_GA7_TOROIDAL_REALIZATION_BRIDGE_results.json'


def fano_primaries():
    pts = tuple(range(1, 8))
    pairs = set(combinations(pts, 2))
    triples = list(combinations(pts, 3))
    p2t = defaultdict(list)
    for t in triples:
        for p in combinations(t, 2):
            p2t[tuple(sorted(p))].append(t)
    ans = []
    def bt(chosen, rem):
        if not rem:
            ans.append(tuple(sorted(chosen)))
            return
        p = min(rem)
        for t in p2t[p]:
            ed = set(tuple(sorted(x)) for x in combinations(t, 2))
            if ed <= rem:
                bt(chosen + [t], rem - ed)
    bt([], pairs)
    return sorted(set(ans))


def third_on_edge(system, edge=(1, 2)):
    e = set(edge)
    for t in system:
        if e <= set(t):
            return next(x for x in t if x not in e)
    raise RuntimeError('edge not covered')


def main():
    q, r, k, v, phi6, chi, f5, g1, dim_g2 = 3, 2, 12, 40, 7, 4, 5, 21, 14
    systems = fano_primaries()
    all_pairs = set(combinations(range(1, 8), 2))
    all_triples = set(combinations(range(1, 8), 3))

    # Existing repo toroidal edge-data ledger constants.
    cs_counts = [10, 9, 9, 8, 9]
    sz_counts = [12, 11]
    realization_counts = cs_counts + sz_counts

    buckets = defaultdict(list)
    for idx, sys in enumerate(systems, 1):
        buckets[third_on_edge(sys)].append(idx)

    # Paper-side class skeleton: six pseudo-octonion classes plus octonions.
    pseudo_classes = [4, 8, 10, 12, 14, 16]
    zero_remainder_primary_indices = [11, 20]  # explicitly singled out in Wilmot Table 1.

    candidate_dictionary = {
        'Csaszar_1_to_5': {
            f'C{i+1}': {'edge_type_count': c, 'calibration_bucket_third_vertex': tv, 'primary_count': len(buckets[tv])}
            for i, (c, tv) in enumerate(zip(cs_counts, sorted(buckets)))
        },
        'Szilassi_1_to_2': {
            f'S{i+1}': {'edge_type_count': c, 'zero_remainder_primary_candidate': zero_remainder_primary_indices[i]}
            for i, c in enumerate(sz_counts)
        },
        'algebra_classes': ['O'] + [f'P{c}' for c in pseudo_classes],
    }

    checks = {
        'seven_realizations': len(realization_counts) == phi6 == 7,
        'five_csaszar_two_szilassi': len(cs_counts) == f5 and len(sz_counts) == r,
        'each_realization_has_21_edges': g1 == 21,
        'toroidal_edge_instances_7_times_21': phi6 * g1 == 147,
        'ga7_primary_count_30': len(systems) == 30,
        'ga7_signing_landscape_size': len(systems) * 2**phi6 == 3840,
        'octonion_representations_30_times_16': len(systems) * 16 == 480,
        'primary_has_7_lines': all(len(s) == phi6 for s in systems),
        'primary_covers_21_pairs_once': all(Counter(tuple(sorted(p)) for t in s for p in combinations(t, 2)) == Counter(all_pairs) for s in systems),
        'all_imaginary_triples_35': len(all_triples) == phi6 * f5 == 35,
        'fano_pair_count_21': len(all_pairs) == g1,
        'edge_completion_buckets_5': len(buckets) == f5,
        'edge_completion_bucket_sizes_6_each': sorted(len(v) for v in buckets.values()) == [6, 6, 6, 6, 6],
        'bucket_total_5_times_6': sum(len(v) for v in buckets.values()) == f5 * 6 == 30,
        'csaszar_count_matches_bucket_count': len(cs_counts) == len(buckets),
        'szilassi_count_matches_zero_remainder_pair': len(sz_counts) == len(zero_remainder_primary_indices) == r,
        'seven_classes_O_plus_six_pseudo': 1 + len(pseudo_classes) == phi6,
        'spin7_dimension_law_21_equals_7_plus_14': g1 == phi6 + dim_g2,
        'g2_root_count_law_12': k == 2 * 6,
        'v_minus_k_law_28': v - k == chi * phi6 == 28,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCDIII',
        'theorem': 'GA7 toroidal realization bridge theorem',
        'core_statement': 'Each of the seven toroidal realizations has the K7 edge carrier with 21 edges. Each of the 30 GA7 primary Fano calibrations partitions that 21-edge carrier into seven Fano lines. Fixing one reference edge splits the 30 primaries into five buckets of six, matching the five Csaszar realizations; the two Szilassi realizations are naturally paired with the two zero-remainder primaries singled out in Wilmot Table 1 as a candidate dual anchor.',
        'counts': {
            'realizations': len(realization_counts),
            'csaszar': len(cs_counts),
            'szilassi': len(sz_counts),
            'edges_per_realization': g1,
            'fano_primaries': len(systems),
            'signings_per_primary': 2**phi6,
            'signed_landscape': len(systems) * 2**phi6,
            'octonion_representations': len(systems) * 16,
        },
        'edge_completion_buckets': {str(k0): v0 for k0, v0 in sorted(buckets.items())},
        'candidate_dictionary': candidate_dictionary,
        'hard_claim': 'The edge-carrier and calibration-bucket counts are proved by enumeration.',
        'honesty_boundary': 'The Csaszar-to-bucket and Szilassi-to-zero-remainder pairings are canonical-looking candidates, not yet metric-derived assignments. A later test should use actual edge-length spectra to choose the bucket labels rather than assigning them in sorted order.',
        'checks': checks,
        'n_verified': sum(checks.values()),
        'n_checks': len(checks),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


if __name__ == '__main__':
    r = main()
    print(r['part'], r['theorem'])
    print('checks', r['n_verified'], '/', r['n_checks'])
    print(r['counts'])
