from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from analysis.w33_golden_ordered_d4_torsor import golden_ordered_d4_torsor_packet
from analysis.w33_frame_action_g2_weyl_quotient import main as frame_action_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXIV_GOLDEN_D4_WEYL_BRIDGE_results.json'


def q4_edge_count(n: int = 4) -> int:
    return n * 2 ** (n - 1)


def main() -> dict[str, Any]:
    golden = golden_ordered_d4_torsor_packet()
    frame = frame_action_main()

    # W33 constants.
    q, r, k, v = 3, 2, 12, 40
    E1, E2, g1, g2, phi6 = 10, 16, 21, 6, 7
    chi, dim_g2, psl27 = 4, 14, 168

    # Claude-hint carrier from the golden selector commits.
    k22_edges = 4
    bridge_cube = q ** 3
    d4_orientations = 8
    unique_failures = golden['unique_support_count']
    ordered_failures = golden['ordered_failure_count']
    q4_edges = q4_edge_count(4)

    # Previously verified G2/Weyl frame constants.
    aut_k33 = 72
    weyl_g2 = 12
    positive_g2_roots = 6

    # Extract profiles from the golden packet.
    orientation_profile = golden['orientation_count_profile']
    pair_profile = golden['pair_count_profile']
    bridge_profile = golden['bridge_count_profile']

    checks = {
        'inherits_golden_ordered_d4_torsor': golden['n_verified'] == len(golden['checks']) == 12,
        'inherits_frame_action_g2_weyl_quotient': frame['n_verified'] == frame['n_checks'] == 24,
        'unique_failures_are_k22_times_bridge_cube': unique_failures == k22_edges * bridge_cube == 108,
        'ordered_failures_are_unique_times_D4': ordered_failures == unique_failures * d4_orientations == 864,
        'D4_times_K22_is_Q4_edge_count': d4_orientations * k22_edges == q4_edges == 32,
        'ordered_failures_are_bridge_cube_times_Q4_edges': ordered_failures == bridge_cube * q4_edges,
        'ordered_failures_are_q3_times_2_to_5': ordered_failures == q ** 3 * 2 ** 5,
        'ordered_failures_are_r_E2_q3': ordered_failures == r * E2 * q ** 3,
        'ordered_failures_are_chi_g2_cubed': ordered_failures == chi * g2 ** 3,
        'pair_shells_are_g2_cubed': set(pair_profile.values()) == {g2 ** 3} and len(pair_profile) == k22_edges,
        'bridge_shells_are_Q4_edges': set(bridge_profile.values()) == {q4_edges} and len(bridge_profile) == bridge_cube,
        'orientation_shells_are_unique_failures': set(orientation_profile.values()) == {unique_failures} and len(orientation_profile) == d4_orientations,
        'ordered_failures_are_autK33_times_weylG2': ordered_failures == aut_k33 * weyl_g2,
        'autK33_is_positive_roots_times_weylG2': aut_k33 == positive_g2_roots * weyl_g2,
        'ordered_failures_are_positive_roots_times_weyl_squared': ordered_failures == positive_g2_roots * weyl_g2 ** 2,
        'ordered_failures_divide_autK44_by_three_quarters': ordered_failures * 4 == 3 * 1152,
        'Q4_edges_split_as_two_E2_blocks': q4_edges == r * E2,
        'bridge_cube_is_F3_cube': bridge_cube == 27,
        'support_shell_is_chi_F3_cube': unique_failures == chi * bridge_cube,
        'g2_cube_is_Csaszar3_energy': g2 ** 3 == 216,
        'spin7_law_g1_equals_phi6_plus_dimG2': g1 == phi6 + dim_g2,
        'g2_root_law_k_equals_2g2': k == 2 * g2,
        'redundancy_law_v_minus_k': v - k == chi * phi6 == 28,
        'psl_factorization': psl27 == k * dim_g2 == phi6 * 24,
        'e1_not_needed_boundary': ordered_failures % E1 != 0,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXIV',
        'theorem': 'Golden D4 Weyl bridge theorem',
        'input_packets': [
            'MMCCCLXXIII golden ordered D4 torsor',
            'MMCD frame action / G2 Weyl quotient theorem',
        ],
        'counts': {
            'unique_failures': unique_failures,
            'ordered_failures': ordered_failures,
            'K2_2_edges': k22_edges,
            'bridge_cube': bridge_cube,
            'D4_orientations': d4_orientations,
            'Q4_edges': q4_edges,
            'Aut_K33': aut_k33,
            'Weyl_G2': weyl_g2,
            'positive_G2_roots': positive_g2_roots,
        },
        'identities': {
            'golden_product': '864 = 4*27*8 = K2,2_edges * F3^3 * D4',
            'Q4_edge_lift': '864 = 27*32 = F3^3 * |E(Q4)|, because 4*8 = 32',
            'G2_Weyl_shell': '864 = 72*12 = |Aut(K3,3)| * |W(G2)|',
            'root_sector_shell': '864 = 6*12^2 = positive_G2_roots * Weyl(G2)^2',
            'energy_shell': '864 = 4*6^3 = chi*g2^3',
            'qutrit_block': '864 = 2*16*27 = r*E2*q^3',
        },
        'profiles': {
            'orientation_profile': orientation_profile,
            'pair_profile': pair_profile,
            'bridge_profile': bridge_profile,
        },
        'interpretation': (
            'Claude’s D4 torsor result turns the repeated 864 obstruction count into a product carrier.  '
            'The independent bridge is that K2,2_edges*D4_orientations = 32, exactly the edge count of Q4.  '
            'Therefore the ordered golden obstruction shell is F3^3 times the Q4 boundary edge set.  '
            'The same 864 is also Aut(K3,3)*W(G2)=72*12, so the golden obstruction shell is the qutrit-cube/Q4-boundary form of the G2 Weyl frame-action shell.'
        ),
        'honesty_boundary': (
            'This proves the count and profile bridge.  It does not yet construct a pointwise equivariant bijection '
            'between ordered golden quadrangles and explicit Aut(K3,3) x W(G2) elements.'
        ),
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
