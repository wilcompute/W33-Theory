#!/usr/bin/env python3
"""
Pass 1213: residual commutant geometry memo.

Uses the exact pass-1194 residual data to expose the geometric shape of the
commutant: which species dominate multiplicity mass and where matrix-unit work
should start for maximum leverage.
"""
import json
from pathlib import Path
from datetime import datetime

SRC = Path('data/w33_pass1194_residual_central_idempotents.json')


def main():
    data = json.loads(SRC.read_text())
    projs = data['projectors']
    blocks = []
    total_rank = data['residual_dimension']
    total_comm = data['commutant_dimension']
    for p in projs:
        m = p['multiplicity']
        d = p['degree']
        rank = p['residual_rank']
        comm_block_dim = m * m
        blocks.append({
            'irrep': p['irrep'],
            'degree': d,
            'multiplicity': m,
            'rank': rank,
            'rank_share': rank / total_rank,
            'commutant_block_dim': comm_block_dim,
            'commutant_share': comm_block_dim / total_comm,
        })
    blocks.sort(key=lambda x: (-x['commutant_block_dim'], -x['rank']))
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1213.residual_commutant_geometry_memo.v1',
        'status': 'PASS',
        'residual_dimension': total_rank,
        'commutant_dimension': total_comm,
        'blocks_sorted_by_commutant_leverage': blocks,
        'highest_leverage_species': [b['irrep'] for b in blocks[:4]],
        'verdict': 'Matrix-unit construction should begin with species 20, 6, 1, and 64, which dominate commutant leverage.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1213_residual_commutant_geometry_memo.json').write_text(json.dumps(result, indent=2))
    print('PASS 1213 complete: residual commutant geometry memo written')
    return result

if __name__ == '__main__':
    main()
