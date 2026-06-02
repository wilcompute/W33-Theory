from __future__ import annotations

import json
from pathlib import Path

from analysis.w33_ga7_toroidal_realization_bridge import main as bridge_main
from analysis.w33_ga7_calibration_class_counts import main as class_main

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'PART_MMCDIV_GA7_HEPTAD_CALIBRATION_LIFT_results.json'


def main():
    bridge = bridge_main()
    classes = class_main()

    # W33 / toroidal constants.
    q, r, k, v = 3, 2, 12, 40
    E1, g1, g2, phi6 = 10, 21, 6, 7
    chi, f5, dim_g2, psl27 = 4, 5, 14, 168
    m_s, e6_x_min_supports = 15, 160

    # Wilmot / GA7 counts from the classification verifier.
    primaries = classes['counts']['primaries']
    signings = classes['counts']['signings_per_primary']
    signed_per_carrier = classes['counts']['total']
    oct_per_carrier = classes['class_distribution']['28']
    pseudo_per_carrier = signed_per_carrier - oct_per_carrier

    # Seven toroidal realizations: 5 Csaszar + 2 Szilassi.
    heptad = bridge['counts']['realizations']
    edges_per_realization = bridge['counts']['edges_per_realization']

    heptad_primary_overlays = heptad * primaries
    heptad_line_overlays = heptad * primaries * phi6
    heptad_edge_line_incidences = heptad_line_overlays * 3
    heptad_signed = heptad * signed_per_carrier
    heptad_oct = heptad * oct_per_carrier
    heptad_pseudo = heptad * pseudo_per_carrier

    ratios = {
        'heptad_signed_over_psl27': heptad_signed // psl27,
        'heptad_oct_over_psl27': heptad_oct // psl27,
        'heptad_pseudo_over_psl27': heptad_pseudo // psl27,
        'heptad_signed_over_primary_overlays': heptad_signed // heptad_primary_overlays,
        'heptad_oct_over_primary_overlays': heptad_oct // heptad_primary_overlays,
        'heptad_pseudo_over_primary_overlays': heptad_pseudo // heptad_primary_overlays,
    }

    checks = {
        'inherits_bridge_theorem': bridge['n_verified'] == bridge['n_checks'] == 20,
        'inherits_ga7_class_counts': classes['n_verified'] == classes['n_checks'] == 19,
        'heptad_realizations_7': heptad == phi6 == 7,
        'edges_per_realization_21': edges_per_realization == g1 == 21,
        'primary_count_30': primaries == 30,
        'signings_128': signings == 2**phi6 == 128,
        'signed_per_carrier_3840': signed_per_carrier == primaries * signings == 3840,
        'oct_per_carrier_480': oct_per_carrier == 480,
        'pseudo_per_carrier_3360': pseudo_per_carrier == 3360,
        'heptad_primary_overlays_210': heptad_primary_overlays == 210,
        'heptad_primary_overlays_E1_g1': heptad_primary_overlays == E1 * g1,
        'heptad_primary_overlays_ms_dimG2': heptad_primary_overlays == m_s * dim_g2,
        'heptad_line_overlays_1470': heptad_line_overlays == phi6 * E1 * g1 == 1470,
        'heptad_edge_line_incidences_4410': heptad_edge_line_incidences == heptad * primaries * edges_per_realization == 4410,
        'heptad_signed_26880': heptad_signed == 26880,
        'heptad_signed_equals_160_times_168': heptad_signed == e6_x_min_supports * psl27,
        'heptad_signed_equals_128_times_210': heptad_signed == signings * heptad_primary_overlays,
        'heptad_oct_3360': heptad_oct == 3360,
        'heptad_oct_equals_single_carrier_pseudo': heptad_oct == pseudo_per_carrier,
        'heptad_oct_equals_20_times_168': heptad_oct == 20 * psl27,
        'heptad_oct_equals_16_times_210': heptad_oct == 16 * heptad_primary_overlays,
        'heptad_pseudo_23520': heptad_pseudo == 23520,
        'heptad_pseudo_equals_140_times_168': heptad_pseudo == 140 * psl27,
        'heptad_pseudo_equals_112_times_210': heptad_pseudo == 112 * heptad_primary_overlays,
        'octonion_pseudo_exchange_ratio_7_to_1': heptad_oct == pseudo_per_carrier,
        'signed_ratio_is_minimal_x_supports': ratios['heptad_signed_over_psl27'] == e6_x_min_supports,
        'g2_root_law': k == 2 * g2,
        'spin7_dimension_law': g1 == phi6 + dim_g2,
        'redundancy_law_28': v - k == chi * phi6 == 28,
    }
    assert all(checks.values()), checks

    result = {
        'part': 'MMCDIV',
        'theorem': 'GA7 heptad calibration lift theorem',
        'counts': {
            'toroidal_realizations': heptad,
            'edges_per_realization': edges_per_realization,
            'ga7_primaries_per_carrier': primaries,
            'signings_per_primary': signings,
            'signed_forms_per_carrier': signed_per_carrier,
            'octonions_per_carrier': oct_per_carrier,
            'pseudo_per_carrier': pseudo_per_carrier,
            'heptad_primary_overlays': heptad_primary_overlays,
            'heptad_line_overlays': heptad_line_overlays,
            'heptad_edge_line_incidences': heptad_edge_line_incidences,
            'heptad_signed_forms': heptad_signed,
            'heptad_octonions': heptad_oct,
            'heptad_pseudo': heptad_pseudo,
        },
        'identities': {
            'heptad_primary_overlays': '7*30 = 210 = E1*g1 = 10*21 = m_s*dimG2 = 15*14',
            'heptad_signed_forms': '7*3840 = 26880 = 160*168 = |X_min_supports|*|PSL(2,7)|',
            'heptad_octonions': '7*480 = 3360 = pseudo-octonions of one GA7 carrier = 20*168',
            'heptad_pseudo': '7*3360 = 23520 = 140*168',
            'line_overlay': '7 realizations * 30 primaries * 7 Fano lines = 1470 = 7*10*21',
        },
        'ratios': ratios,
        'interpretation': 'The full seven-realization toroidal heptad lifts one GA7 carrier into a 26880-form signed calibration packet.  This packet is exactly 160 copies of the Fano symmetry group PSL(2,7), matching the 160 minimal X-supports from the W33 edge CSS code.  In parallel, the 480 octonions per carrier lift to 3360 octonions across the heptad, exactly equal to the pseudo-octonion count of a single carrier.  Thus the heptad turns Wilmot’s one-carrier O/P split into a cross-carrier octonion/pseudo exchange law.',
        'honesty_boundary': 'This theorem proves calibration-count identities and their match to existing W33 constants.  It does not yet assign a specific Wilmot primary or signing to a specific metric edge class of a particular Csaszar/Szilassi realization.',
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
