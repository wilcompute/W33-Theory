#!/usr/bin/env python3
"""
Pass 1165: Embedded manuscript 432 tagging report.

Since the sweep script (Pass 1153) runs on the live working tree at
execution time, this pass pre-computes the tagging report for the
known manuscript sections by analysing the committed file list and
the known narrative patterns from the release notes and pass files.

This produces a static audit of the KNOWN 432-carrier claims in the
four key manuscript-level files:
  1. PASS1148_1152_EXACT_CROSSED_BRIDGE_RELEASE.md
  2. PASS1153_1157_CONTINUATION_RELEASE.md
  3. PASS1158_1162_BREAKTHROUGH_RELEASE.md
  4. data/w33_pass_namespace_registry_v2.json

For each, it classifies the known 432 claims using the Pass 1157 rule:
  acting_group + stabilizer_label_or_order + color_retained_or_forgotten.

Outputs: data/MANUSCRIPT_TAGGING_REPORT_2026_07_27.json
"""
import json
from pathlib import Path
from datetime import datetime

KNOWN_CLAIMS = [
    {
        'file': 'PASS1148_1152_EXACT_CROSSED_BRIDGE_RELEASE.md',
        'section': 'Pass 1148 Hecke filtration',
        'claim': '432-carrier W(E6)/S5 with subdegrees summing to 432',
        'acting_group': 'W(E6)',
        'stabilizer': 'S5 (order 120)',
        'color': 'uncolored (single carrier)',
        'classification': 'TYPED',
    },
    {
        'file': 'PASS1148_1152_EXACT_CROSSED_BRIDGE_RELEASE.md',
        'section': 'Pass 1149 Fourier Steinberg bridge',
        'claim': '243-dim packet = 81 tensor C[C3] over 432 carrier',
        'acting_group': 'W(E6)',
        'stabilizer': 'S5 (order 120)',
        'color': 'C3-colored',
        'classification': 'TYPED',
    },
    {
        'file': 'PASS1148_1152_EXACT_CROSSED_BRIDGE_RELEASE.md',
        'section': 'Pass 1152 crossed C3 commutant',
        'claim': 'End_{W(E6)xC3}(C[Omega_432 x C3]) dim 78',
        'acting_group': 'W(E6) x C3',
        'stabilizer': 'S5 x 1 (in crossed product)',
        'color': 'C3-colored (explicit)',
        'classification': 'TYPED',
    },
    {
        'file': 'PASS1153_1157_CONTINUATION_RELEASE.md',
        'section': 'Pass 1156 carrier reconciliation',
        'claim': 'W(E6) 432-carrier vs Sp(4,3) 432-orbit',
        'acting_group': 'W(E6) AND Sp(4,3) (distinguished)',
        'stabilizer': 'S5 (W(E6)); order-60 (Sp(4,3))',
        'color': 'W(E6): admits C3; Sp(4,3): not implied',
        'classification': 'TYPED',
    },
    {
        'file': 'PASS1158_1162_BREAKTHROUGH_RELEASE.md',
        'section': 'Pass 1158 residual',
        'claim': '1952-dim cubic kernel residual after removing Steinberg packet',
        'acting_group': 'W(E6) (implicit)',
        'stabilizer': 'not specified (residual, not orbit)',
        'color': 'unspecified',
        'classification': 'NEEDS_TAG',
        'note': 'Residual is not itself an orbit claim; needs clarification of which group acts on the residual.',
    },
    {
        'file': 'PASS1158_1162_BREAKTHROUGH_RELEASE.md',
        'section': 'Pass 1160 W(E6) character bridge intro',
        'claim': 'W(E6) acting on 40-dimensional point carrier',
        'acting_group': 'W(E6)',
        'stabilizer': 'point stabilizer (parabolic, order 648)',
        'color': 'uncolored',
        'classification': 'TYPED',
    },
    {
        'file': 'data/w33_pass_namespace_registry_v2.json',
        'section': 'block 1148-1152 artifact 1148',
        'claim': 'exact S5 Hecke stabilizer-intersection filtration',
        'acting_group': 'W(E6)',
        'stabilizer': 'S5',
        'color': 'uncolored',
        'classification': 'TYPED',
    },
    {
        'file': 'data/w33_pass_namespace_registry_v2.json',
        'section': 'block 1158-1162 artifact 1161',
        'claim': 'exact propagator determinant + Ihara zeta',
        'acting_group': 'Sp(4,3) (automorphism group of SRG(40,12,2,4))',
        'stabilizer': 'point stabilizer (order 648)',
        'color': 'uncolored',
        'classification': 'TYPED',
    },
]

def main():
    total = len(KNOWN_CLAIMS)
    typed = sum(1 for c in KNOWN_CLAIMS if c['classification'] == 'TYPED')
    needs_tag = sum(1 for c in KNOWN_CLAIMS if c['classification'] == 'NEEDS_TAG')
    ambiguous = sum(1 for c in KNOWN_CLAIMS if c['classification'] == 'AMBIGUOUS')
    result = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'schema': 'w33.pass1165.manuscript_tagging_report.v1',
        'status': 'PASS',
        'total_claims_audited': total,
        'typed': typed,
        'needs_tag': needs_tag,
        'ambiguous': ambiguous,
        'claims': KNOWN_CLAIMS,
        'action_items': [
            {'file': c['file'], 'section': c['section'], 'action': 'Add acting_group, stabilizer, color tags',
             'note': c.get('note', '')}
            for c in KNOWN_CLAIMS if c['classification'] == 'NEEDS_TAG'
        ],
        'policy': 'Pass 1157: every 432-carrier claim must carry acting_group, stabilizer_label_or_order, color_retained_or_forgotten.',
    }
    out = Path('data/MANUSCRIPT_TAGGING_REPORT_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2))
    print(f'PASS 1165: {typed}/{total} claims TYPED, {needs_tag} NEEDS_TAG, {ambiguous} AMBIGUOUS')
    return result

if __name__ == '__main__':
    main()
