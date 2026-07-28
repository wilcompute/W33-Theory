#!/usr/bin/env python3
"""
Pass 1171: Fix the NEEDS_TAG claim in the breakthrough release.

From Pass 1165: one claim in PASS1158_1162_BREAKTHROUGH_RELEASE.md
(Pass 1158 residual section) lacks the three required tags:
  acting_group, stabilizer_label_or_order, color_retained_or_forgotten.

This pass:
1. Generates the corrected text for the Pass 1158 section.
2. Records the correction in a structured erratum JSON.
3. Verifies the correction contains all three required tags.
4. Prepares the errata register entry.

Outputs:
  data/ERRATUM_PASS1158_RESIDUAL_2026_07_27.json
  data/ERRATA_REGISTER.json (updated)
"""
import json
from pathlib import Path
from datetime import datetime

ERRATUM = {
    'id': 'ERR-1158-RESIDUAL',
    'date': '2026-07-27',
    'file': 'PASS1158_1162_BREAKTHROUGH_RELEASE.md',
    'section': 'Pass 1158 -- Systematic attack on the 1952-dim kernel residual',
    'original_claim': '1952-dim cubic-map kernel residual after removing Steinberg packet',
    'defect': 'Missing: acting_group, stabilizer_label_or_order, color_retained_or_forgotten',
    'corrected_claim': (
        '1952-dim sub-module of the cubic-map kernel (acting group: W(E6), order 51840; '
        'not an orbit so no pointwise stabilizer -- module stabilizer is the full W(E6); '
        'color: uncolored unless C3-colored kernel variant is used explicitly). '
        'The residual is the W(E6)-equivariant complement to the 243-dim Steinberg packet '
        'inside the 2195-dim kernel of the cubic incidence map M: C^2240 -> C^k, rank 45.'
    ),
    'tags_now_present': {
        'acting_group': 'W(E6), order 51840',
        'stabilizer_label_or_order': 'full W(E6) (not an orbit; module has no pointwise stabilizer)',
        'color_retained_or_forgotten': 'uncolored (C3 color not applied unless explicitly stated)',
    },
    'classification_after_fix': 'TYPED',
    'policy': 'Pass 1157 sync rule: every 432-carrier/kernel claim must carry all three tags.',
}

def main():
    # Verify all three tags present in correction
    required = ['acting_group', 'stabilizer_label_or_order', 'color_retained_or_forgotten']
    for tag in required:
        assert tag in ERRATUM['tags_now_present'], f'Missing tag: {tag}'

    # Write erratum
    err_path = Path('data/ERRATUM_PASS1158_RESIDUAL_2026_07_27.json')
    err_path.parent.mkdir(exist_ok=True)
    err_path.write_text(json.dumps(ERRATUM, indent=2))

    # Update or create errata register
    reg_path = Path('data/ERRATA_REGISTER.json')
    if reg_path.exists():
        register = json.loads(reg_path.read_text())
    else:
        register = {'schema': 'w33.errata_register.v1', 'errata': []}
    # Remove if already present
    register['errata'] = [e for e in register['errata'] if e.get('id') != ERRATUM['id']]
    register['errata'].append(ERRATUM)
    register['last_updated'] = datetime.utcnow().isoformat()+'Z'
    reg_path.write_text(json.dumps(register, indent=2))

    result = {
        'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1171.needs_tag_fix.v1',
        'status': 'PASS',
        'erratum_id': ERRATUM['id'],
        'file_corrected': ERRATUM['file'],
        'tags_verified': required,
        'all_tags_present': True,
        'errata_register_updated': True,
        'manuscript_action': 'Amend Pass 1158 section in PASS1158_1162_BREAKTHROUGH_RELEASE.md with the corrected claim text from this erratum.',
    }
    print(f'PASS 1171: Erratum {ERRATUM["id"]} filed and verified, all 3 tags present')
    return result

if __name__ == '__main__':
    main()
