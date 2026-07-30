#!/usr/bin/env python3
"""
Pass 1215: projector fingerprint atlas.

Creates compact projector fingerprints from the denominator-cleared class-sum
numerators so species can be compared quickly before any matrix-unit refinement.
"""
import json, hashlib
from pathlib import Path
from datetime import datetime

SRC = Path('data/w33_pass1194_residual_central_idempotents.json')


def main():
    data = json.loads(SRC.read_text())
    atlas = []
    for p in data['projectors']:
        nums = p['denominator_cleared']['numerators_in_atlas_order']
        support = sum(1 for x in nums if x != 0)
        l1 = sum(abs(int(x)) for x in nums)
        l2sq = sum(int(x) * int(x) for x in nums)
        sign_pattern = ''.join('+' if x > 0 else '-' if x < 0 else '0' for x in nums)
        atlas.append({
            'irrep': p['irrep'],
            'support_size': support,
            'l1_norm': l1,
            'l2_norm_squared': l2sq,
            'sign_pattern_sha256': hashlib.sha256(sign_pattern.encode()).hexdigest(),
            'coefficient_sha256': p['denominator_cleared']['sha256'],
        })
    atlas.sort(key=lambda r: (-r['support_size'], -r['l1_norm']))
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1215.projector_fingerprint_atlas.v1',
        'status': 'PASS',
        'atlas_order': data['atlas_class_order'],
        'fingerprints': atlas,
        'purpose': 'Fast comparison of residual species before explicit basis-level matrix-unit work.'
    }
    Path('data').mkdir(exist_ok=True)
    Path('data/w33_pass1215_projector_fingerprint_atlas.json').write_text(json.dumps(result, indent=2))
    print('PASS 1215 complete: projector fingerprint atlas written')
    return result

if __name__ == '__main__':
    main()
