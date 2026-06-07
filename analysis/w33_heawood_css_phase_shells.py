#!/usr/bin/env python3
"""BT497: Heawood CSS Phase-Shell Theorem.

Connects three existing repo threads:
  * CSS-genus hinge: d_X=3, d_Z=4, d_X+d_Z=7, d_X d_Z=12.
  * Genus-one Fano/Heawood phase lock: phase superperiod 28 and Euler drift 56.
  * Corrected Szilassi carrier: Heawood graph.

The new executable statement:
For every vertex of the Heawood graph, distance-shell sizes are
    d0,d1,d2,d3 = 1,3,6,4.
Thus the Heawood local shell itself contains the CSS roots 3 and 4,
the G2 positive-root shell 6, and the Fano/toroidal shell 7=3+4.
Globally the unordered distance pair counts are
    21,42,28,
and the oriented distance-3 count is
    14*4=56,
matching the 28/56 phase-superperiod/Euler-drift pair.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx


def main() -> dict:
    H = nx.heawood_graph()
    assert H.number_of_nodes() == 14
    assert H.number_of_edges() == 21
    assert nx.is_bipartite(H)
    assert nx.diameter(H) == 3
    assert sorted(dict(H.degree()).values()) == [3] * 14

    local_profiles = {}
    for v in H.nodes():
        lengths = nx.single_source_shortest_path_length(H, v)
        profile = Counter(lengths.values())
        assert profile == Counter({0: 1, 1: 3, 2: 6, 3: 4})
        local_profiles[str(v)] = {str(k): profile[k] for k in sorted(profile)}

    pair_profile = Counter()
    for u, v in combinations(H.nodes(), 2):
        pair_profile[nx.shortest_path_length(H, u, v)] += 1
    assert pair_profile == Counter({1: 21, 2: 42, 3: 28})

    dX = local_profiles['0']['1']
    g2_plus = local_profiles['0']['2']
    dZ = local_profiles['0']['3']
    assert (dX, g2_plus, dZ) == (3, 6, 4)
    assert dX + dZ == 7
    assert dX * dZ == 12
    assert 1 + dX + g2_plus + dZ == 14
    assert dX + g2_plus + dZ == 13

    oriented_d3 = 14 * dZ
    unordered_d3 = pair_profile[3]
    assert unordered_d3 == 28
    assert oriented_d3 == 56
    assert oriented_d3 == 2 * unordered_d3

    # The global pair profile follows from local shells by divide-by-two.
    assert pair_profile[1] == 14 * dX // 2
    assert pair_profile[2] == 14 * g2_plus // 2
    assert pair_profile[3] == 14 * dZ // 2

    # Percolation thresholds from the CSS-genus hinge are literally visible
    # as nested shell activations in Heawood.
    nested_shell_sums = {
        'center_only': 1,
        'through_d1': 1 + dX,
        'through_d2': 1 + dX + g2_plus,
        'through_d3_full': 1 + dX + g2_plus + dZ,
        'off_center_total': dX + g2_plus + dZ,
    }
    assert nested_shell_sums == {
        'center_only': 1,
        'through_d1': 4,
        'through_d2': 10,
        'through_d3_full': 14,
        'off_center_total': 13,
    }

    results = {
        'theorem': 'BT497 Heawood CSS Phase-Shell Theorem',
        'graph': 'Heawood graph = corrected Szilassi carrier',
        'local_distance_shell_profile': {'d0': 1, 'd1': 3, 'd2': 6, 'd3': 4},
        'global_unordered_distance_pair_profile': {str(k): pair_profile[k] for k in sorted(pair_profile)},
        'css_genus_hinge_recovery': {
            'd_X': dX,
            'd_Z': dZ,
            'd_X_plus_d_Z': dX + dZ,
            'd_X_times_d_Z': dX * dZ,
            'G2_positive_shell': g2_plus,
            'Phi3_off_center_shell': dX + g2_plus + dZ,
        },
        'phase_superperiod_recovery': {
            'unordered_distance3_pairs': unordered_d3,
            'oriented_distance3_pairs': oriented_d3,
            'phase_superperiod': 28,
            'euler_drift_magnitude': 56,
            'identity': 'oriented distance-3 pairs = 2 * unordered distance-3 pairs = 56',
        },
        'nested_shell_sums': nested_shell_sums,
        'percolation_reading': {
            'p_X_shell': 'first Heawood shell has size 3=d_X',
            'p_Z_shell': 'outer Heawood shell has size 4=d_Z',
            'p_T_shell': 'inner+outer shell 3+4=7 is Fano/toroidal threshold',
            'p_C_clock': '3*4=12 is local codec/genus denominator',
            'p_full_local': 'full local Heawood ball has 14 vertices = dim(G2)',
        },
    }
    out = Path('data/PART_BT497_HEAWOOD_CSS_PHASE_SHELLS_results.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
    return results

if __name__ == '__main__':
    main()
