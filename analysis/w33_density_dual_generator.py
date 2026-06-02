from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCCCLXXV_DENSITY_DUAL_GENERATOR_results.json'


def main():
    q = 3
    r = 2
    chi = 4
    phi6 = 7
    f = 24
    mu = 28
    g2_pos = 6
    k = 12
    dim_g2 = 14
    phi3 = 13
    psl = 168
    dim_f4 = 52
    aut_k44 = 1152
    heegner6 = 19
    big_gap = 192
    residual_gap = 152

    checks = {
        'f_is_24': f == 24,
        'mu_is_28': mu == chi * phi6 == 28,
        'g2_pos_is_6': g2_pos == 6,
        'g2_total_roots_are_k': 2 * g2_pos == k,
        'dim_g2_is_14': dim_g2 == r * phi6 == 14,
        'psl_from_f_phi6': f * phi6 == psl,
        'psl_from_mu_g2_pos': mu * g2_pos == psl,
        'dual_generators_match': f * phi6 == mu * g2_pos,
        'f_plus_mu_is_f4': f + mu == dim_f4,
        'mu_minus_f_is_chi': mu - f == chi,
        'f_times_mu_is_chi_psl': f * mu == chi * psl,
        'f4_is_chi_phi3': dim_f4 == chi * phi3,
        'psl_is_k_dim_g2': psl == k * dim_g2,
        'aut_k44_is_two_f_squared': aut_k44 == r * f * f,
        'aut_k44_is_six_big_gaps': aut_k44 == g2_pos * big_gap,
        'big_gap_is_psl_plus_f': big_gap == psl + f,
        'residual_is_2q_heegner6': residual_gap == r**q * heegner6,
        'f4_plus_residual_is_big_gap': dim_f4 + residual_gap == big_gap,
        'psl_f4_residual_is_two_big_gaps': psl + dim_f4 + residual_gap == 2 * big_gap,
        'product_is_four_psl': f * mu == 4 * psl,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCCCLXXV',
        'theorem': 'Density dual generator theorem',
        'counts': {
            'f': f,
            'mu': mu,
            'phi6': phi6,
            'positive_G2_roots': g2_pos,
            'PSL27': psl,
            'F4_horizon': dim_f4,
            'Aut_K44': aut_k44,
            'packet_big_gap': big_gap,
            'packet_residual_gap': residual_gap
        },
        'identities': {
            'dual_PSL': '24*7 = 28*6 = 168',
            'F4_horizon': '24+28 = 52',
            'Euler_gap': '28-24 = 4',
            'product': '24*28 = 672 = 4*168',
            'packet_bridge': '52+152 = 192 and 168+52+152 = 384',
            'K44_bridge': '1152 = 6*192 = 2*24^2'
        },
        'reading': 'BT47 singles out 24 as the deepest density peak and BT46 singles out 28 as a sevenfold coincidence. Together they form a dual generator: 24 times the seven Fano points equals 28 times the six positive G2 roots. Their sum is the F4 horizon, their gap is chi, and their product is chi times 168.',
        'claim_boundary': 'This proves the exact integer bridge, not a pointwise map between all individual interpretations.',
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
