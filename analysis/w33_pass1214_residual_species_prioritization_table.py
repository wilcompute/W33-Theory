#!/usr/bin/env python3
"""
Pass 1214: residual species prioritization table.

Ranks the ten residual species by two complementary notions of importance:
residual rank share and commutant leverage share.
"""
import json
from pathlib import Path
from datetime import datetime

SRC = Path('data/w33_pass1194_residual_central_idempotents.json')


def main():
    data = json.loads(SRC.read_text())
    total_rank = data['residual_dimension']
    total_comm = data['commutant_dimension']
    rows = []
    for p in data['projectors']:
        m = p['multiplicity']
        rank = p['residual_rank']
        rows.append({
            'irrep': p['irrep'],
            'degree': p['degree'],
            'multiplicity': m,
            'rank': rank,
            'rank_share': rank / total_rank,
            'commutant_block_dim': m*m,
            'commutant_share': (m*m) / total_comm,
        })
    by_rank = sorted(rows, key=lambda r: (-r['rank'], -r['commutant_block_dim']))
    by_comm = sorted(rows, key=lambda r: (-r['commutant_block_dim'], -r['rank']))
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1214.residual_species_prioritization_table.v1',
        'status': 'PASS',
        'by_rank': by_rank,
        'by_commutant_leverage': by_comm,
        'best_first_targets': {
            'rank_dominant': [r['irrep'] for r in by_rank[:3]],
            'commutant_dominant': [r['irrep'] for r in by_comm[:3]],
        }
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1214_residual_species_prioritization_table.json').write_text(json.dumps(result, indent=2))
    print('PASS 1214 complete: residual species prioritization table written')
    return result

if __name__ == '__main__':
    main()
