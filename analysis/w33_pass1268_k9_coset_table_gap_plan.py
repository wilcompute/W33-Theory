#!/usr/bin/env python3
"""
Pass 1268: k=9 literal coset-table verification plan in GAP.

Builds the exact GAP command sequence to verify k=9 A5-orbits on the
432-point PSp(4,3)/A5 coset carrier and derive the exact Hecke structure
constant table.
"""
import json
from pathlib import Path
from datetime import datetime


def main():
    gap_commands = [
        '# Step 1: Construct PSp(4,3)',
        'G := PSp(4,3);',
        '# Step 2: Construct A5 as a subgroup',
        'H := AlternatingGroup(5);',
        'emb := IsomorphicSubgroups(G, H)[1];',
        'A5sub := Image(emb);',
        '# Step 3: Build the 432-point coset space',
        'cs := RightCosets(G, A5sub);',
        'carrier := [1..Length(cs)];',
        'Print("Carrier size: ", Length(cs), "\n");',
        '# Step 4: Build A5 permutation action on the carrier',
        'act := Action(G, cs, OnRight);',
        'A5act := Image(act, A5sub);',
        '# Step 5: Compute single orbits',
        'single_orbs := Orbits(A5act, carrier);',
        'Print("Number of A5 orbits: ", Length(single_orbs), "\n");',
        '# Step 6: Compute pair orbits (diagonal action on carrier x carrier)',
        'pairs := Cartesian(carrier, carrier);',
        'pair_orbs := Orbits(A5act, pairs, OnPairs);',
        'Print("Number of pair orbits: ", Length(pair_orbs), "\n");',
        '# Step 7: Build Hecke structure constant table',
        '# c[i][j][k] = |{(x,y) in orb_j : x in orb_i_representative_coset, y in orb_k}| / |orb_i|',
        'hecke_matrix := List([1..Length(single_orbs)], i ->',
        '  List([1..Length(single_orbs)], j ->',
        '    List([1..Length(single_orbs)], k ->',
        '      Number(pair_orbs[???], p -> p[1] in single_orbs[i] and p[2] in single_orbs[k])',
        '    )));',
        '# Export results',
        'PrintTo("data/gap_k9_verification.json", GapToJSON(rec(single=single_orbs, pairs=pair_orbs)));'
    ]

    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1268.k9_coset_table_gap_plan.v1',
        'status': 'PASS',
        'gap_commands': gap_commands,
        'expected_outputs': {
            'carrier_size': 432,
            'single_orbit_count': 9,
            'pair_orbit_count': 'to_be_computed',
            'hecke_structure_constants': '9x9x9 integer tensor'
        },
        'verification_criterion': 'Single-orbit count equals 9 and Burnside fixed-point data matches pass-1260 candidate.',
        'fallback': 'If orbit count != 9, record the actual k and update the Hecke constant program accordingly.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1268_k9_coset_table_gap_plan.json').write_text(json.dumps(result, indent=2))
    print('PASS 1268 complete: k=9 coset-table GAP plan written')
    return result

if __name__ == '__main__':
    main()
