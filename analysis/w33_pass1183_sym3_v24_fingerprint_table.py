#!/usr/bin/env python3
"""
Pass 1183: Sym^3(V24) candidate fingerprint table.

Takes the arithmetic candidates from Pass 1178 and computes compact fingerprints
(term count, total multiplicity, heavy-mass share) to prioritize later exact
character-table elimination.
"""
import json
from pathlib import Path
from datetime import datetime

SRC = Path('data/SYM3_V24_PLETHYSM_SEARCH_2026_07_27.json')


def main():
    data = json.loads(SRC.read_text()) if SRC.exists() else {'best_candidates': []}
    fps = []
    for i, cand in enumerate(data.get('best_candidates', []), start=1):
        total_terms = sum(cand.values())
        distinct = len(cand)
        heavy = sum(int(k)*v for k,v in cand.items() if int(k) >= 160)
        total = sum(int(k)*v for k,v in cand.items())
        fps.append({
            'candidate_index': i,
            'distinct_irreps': distinct,
            'total_terms': total_terms,
            'heavy_mass': heavy,
            'heavy_mass_share': heavy / total if total else 0.0,
            'candidate': cand,
        })
    result = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1183.sym3_v24_fingerprint_table.v1',
        'status': 'PASS',
        'source': str(SRC),
        'fingerprints': fps,
        'selection_rule': 'Prefer low term count, low distinct irrep count, and high heavy-mass share for early character-trace testing.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/SYM3_V24_FINGERPRINTS_2026_07_27.json').write_text(json.dumps(result, indent=2))
    print('PASS 1183 complete:', len(fps), 'fingerprints written')
    return result

if __name__ == '__main__':
    main()
