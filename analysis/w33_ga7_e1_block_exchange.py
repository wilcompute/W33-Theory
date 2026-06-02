from __future__ import annotations

import json
from pathlib import Path

from analysis.w33_ga7_heptad_calibration_lift import main as lift_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCDV_GA7_E1_BLOCK_EXCHANGE_results.json'


def main():
    lift = lift_main()

    # W33 constants.
    q, r, k, v = 3, 2, 12, 40
    E1, E2, g1, g2, phi6 = 10, 16, 21, 6, 7
    chi, dim_g2, psl27 = 4, 14, 168
    x_min_supports = 160

    counts = lift['counts']
    heptad_primary_overlays = counts['heptad_primary_overlays']
    heptad_signed = counts['heptad_signed_forms']
    heptad_oct = counts['heptad_octonions']
    heptad_pseudo = counts['heptad_pseudo']
    signings = counts['signings_per_primary']

    # E1-block decomposition.
    block_count = E1
    primaries_per_block = heptad_primary_overlays // block_count
    signed_per_block = heptad_signed // block_count
    oct_per_block = heptad_oct // block_count
    pseudo_per_block = heptad_pseudo // block_count
    x_supports_per_block = x_min_supports // block_count

    # The block-level PSL decomposition.
    psl_copies_signed_per_block = signed_per_block // psl27
    psl_copies_oct_per_block = oct_per_block // psl27
    psl_copies_pseudo_per_block = pseudo_per_block // psl27

    # Interpretable block vector.
    block_vector = {
        'octonion_psl_copies': psl_copies_oct_per_block,
        'pseudo_psl_copies': psl_copies_pseudo_per_block,
        'total_psl_copies': psl_copies_signed_per_block,
    }

    checks = {
        'inherits_heptad_lift': lift['n_verified'] == lift['n_checks'] == 29,
        'e1_block_count_10': block_count == 10,
        'primary_overlays_factor_as_E1_g1': heptad_primary_overlays == E1 * g1 == 210,
        'primaries_per_block_g1': primaries_per_block == g1 == 21,
        'signed_per_block_2688': signed_per_block == 2688,
        'signed_per_block_g1_times_128': signed_per_block == g1 * signings,
        'signed_per_block_E2_times_PSL27': signed_per_block == E2 * psl27,
        'heptad_signed_E1_E2_PSL27': heptad_signed == E1 * E2 * psl27,
        'heptad_signed_E1_g1_128': heptad_signed == E1 * g1 * signings,
        'x_supports_factor_as_E1_E2': x_min_supports == E1 * E2,
        'x_supports_per_block_E2': x_supports_per_block == E2 == 16,
        'oct_per_block_336': oct_per_block == 336,
        'oct_per_block_r_times_PSL27': oct_per_block == r * psl27,
        'pseudo_per_block_2352': pseudo_per_block == 2352,
        'pseudo_per_block_dimG2_times_PSL27': pseudo_per_block == dim_g2 * psl27,
        'sector_split_r_plus_dimG2_equals_E2': r + dim_g2 == E2,
        'block_psl_split_2_plus_14_equals_16': psl_copies_oct_per_block + psl_copies_pseudo_per_block == psl_copies_signed_per_block == E2,
        'global_oct_E1_r_PSL27': heptad_oct == E1 * r * psl27,
        'global_pseudo_E1_dimG2_PSL27': heptad_pseudo == E1 * dim_g2 * psl27,
        'global_signed_E1_r_plus_dimG2_PSL27': heptad_signed == E1 * (r + dim_g2) * psl27,
        'g2_root_law_k_equals_2g2': k == 2 * g2,
        'spin7_law_g1_equals_phi6_plus_dimG2': g1 == phi6 + dim_g2,
        'redundancy_law_v_minus_k': v - k == chi * phi6 == 28,
        'psl27_factorization': psl27 == phi6 * 24 == k * dim_g2,
        'block_vector_exact': block_vector == {'octonion_psl_copies': 2, 'pseudo_psl_copies': 14, 'total_psl_copies': 16},
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCDV',
        'theorem': 'GA7 E1 block exchange theorem',
        'counts': {
            'E1_blocks': block_count,
            'primaries_per_block': primaries_per_block,
            'signed_forms_per_block': signed_per_block,
            'octonions_per_block': oct_per_block,
            'pseudo_per_block': pseudo_per_block,
            'x_supports_per_block': x_supports_per_block,
            'global_signed_forms': heptad_signed,
            'global_octonions': heptad_oct,
            'global_pseudo': heptad_pseudo,
        },
        'block_identities': {
            'primary_block': '21 primary overlays per E1 block = g1',
            'signed_block': '21*128 = 2688 = 16*168 = E2*PSL27',
            'octonion_block': '336 = 2*168 = r*PSL27',
            'pseudo_block': '2352 = 14*168 = dimG2*PSL27',
            'sector_split': '2 + 14 = 16 = E2',
            'global_lift': '26880 = 10*16*168 = E1*E2*PSL27',
        },
        'block_vector': block_vector,
        'interpretation': 'The heptad GA7 lift decomposes into E1=10 identical exchange blocks.  Each block contains g1=21 primary overlays and 2688 signed calibrations.  The same block is also E2=16 copies of the Fano symmetry group PSL(2,7).  Inside each block, the octonion sector contributes r=2 PSL copies and the pseudo-octonion sector contributes dim(G2)=14 PSL copies, so the local sector split is r + dim(G2) = E2.  Globally this yields 26880 = E1*E2*PSL(2,7), aligning the Wilmot GA7 heptad with the 160 minimal X-supports as 10 blocks of 16 supports.',
        'honesty_boundary': 'This is a block-level count theorem.  It does not yet choose a canonical bijection between individual signed calibrations and individual minimal logical X-support/Fano-group elements.',
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
