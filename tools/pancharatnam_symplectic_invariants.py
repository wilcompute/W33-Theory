#!/usr/bin/env python3
"""Regenerate the corrected Witting/Pancharatnam invariant report.

The legacy implementation attempted to encode Witting rays directly as F3^4
phase-exponent tuples. Pass4963 proves that encoder was non-bijective and that
the correct finite identification is graph-theoretic: Witting orthogonality is
the standard W(3,3) POINT graph, while the Steiner quotient is Q(4,3), the W33
LINE graph.

This public tool now delegates the exact computation to Pass4963 and emits a
short corrected report. It never recreates the withdrawn Pass4882 claim.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis.w33_pass4963_witting_pancharatnam_w33_reaudit import main as audit_main

OUT=ROOT/'docs/pancharatnam_symplectic_invariants.md'
CERT=ROOT/'data/PART_W33_PASS4963_WITTING_PANCHARATNAM_W33_REAUDIT.json'

def main()->int:
    audit_main();d=json.loads(CERT.read_text())
    t=d['exact_pancharatnam_center_table']
    text=f'''# Pancharatnam phase vs. W(3,3) point-triad geometry — corrected Pass4963 report

**Status:** exact finite result; supersedes the old phase-exponent/F3 encoder report.

The 40 Witting rays form an orthogonality graph isomorphic to the standard
`W(3,3)` **point** graph. They are **not** the 40 Steiner fibers: those fibers
form the nonisomorphic dual `Q(4,3)` / W33-line graph.

The retired direct ray→`F3^4` exponent encoder is not a bijection: it maps the
40 rays to only **{d['legacy_encoder_failure']['distinct_F3_tuples_from_40_rays']}** tuples and maps **{d['legacy_encoder_failure']['zero_tuple_multiplicity']}** rays to the zero tuple.

## Exact Bargmann/Pancharatnam phase census

W33 point-triad centers | phase | count
--- | --- | ---:
1 | `+π/6` | {t['one_W33_common_center']['+pi/6']}
1 | `−π/6` | {t['one_W33_common_center']['-pi/6']}
4 | `+π/2` | {t['four_W33_common_centers']['+pi/2']}
4 | `−π/2` | {t['four_W33_common_centers']['-pi/2']}

Total nonorthogonal triples: **{d['nonorthogonal_triples']}**.

Thus phase magnitude detects the exact W33 independent-triad center dichotomy:
`1 center ↔ |phase|=π/6`, `4 centers ↔ |phase|=π/2`.

The old proposed direct equality between the E6 Steiner signing and Witting
Pancharatnam phase is withdrawn because it conflated the two nonisomorphic
40-element point/line actions.
'''
    OUT.write_text(text,encoding='utf-8');print(f'Wrote {OUT}');return 0
if __name__=='__main__':raise SystemExit(main())
