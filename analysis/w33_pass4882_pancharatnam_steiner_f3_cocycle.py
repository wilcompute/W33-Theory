#!/usr/bin/env python3
"""Pass4882 — historical Pancharatnam/Steiner conjecture, now superseded.

This file used to promote a parameter-only match between the 40 Steiner fibers
and the 40 Witting rays. Pass4954 proved the Steiner fiber quotient is the
Q(4,3)=W33-line action, while Pass4963 proved the Witting orthogonality graph is
the nonisomorphic standard W(3,3) POINT action. Therefore the old proposed
Steiner/Witting identification is withdrawn.

Running this legacy entry point now writes only a supersession certificate; the
authoritative executable phase analysis is Pass4963 (and outer-character
refinement Pass4966).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4882_PANCHARATNAM_STEINER_COCYCLE.json'

def main()->int:
    newer=ROOT/'data/PART_W33_PASS4963_WITTING_PANCHARATNAM_W33_REAUDIT.json'
    if not newer.exists():
        raise RuntimeError('Pass4963 authoritative certificate is required')
    audit=json.loads(newer.read_text())
    assert audit['witting_carrier']['orthogonality_graph']=='isomorphic to standard W(3,3) point graph'
    assert audit['witting_carrier']['isomorphic_to_Q43_Steiner_line_graph'] is False
    out={
      'pass':4882,
      'status':'WITHDRAWN_SUPERSEDED_BY_PASS4963',
      'withdrawn_claim':'40 Steiner fibers/Q(4,3) are the same 40-ray carrier as the Witting orthogonality geometry, and E6 Steiner signing can therefore be identified directly with Witting Pancharatnam phase.',
      'reason':'Pass4954 separates the two degree-40 actions: Steiner fibers are W33 lines/Q(4,3). Pass4963 independently proves the 40 Witting rays carry the standard W33 point graph and are not isomorphic to Q(4,3). Parameter equality SRG(40,12,2,4) was insufficient.',
      'authoritative_replacement':{
        'Pass4963':'Witting rays = W33 point action; exact phase detects 1-center versus 4-center W33 point triads',
        'Pass4966':'oriented Witting phase is PSp-invariant and outer-PGSp odd'},
      'boundary':'The old Steiner/Pancharatnam equality is withdrawn, not merely left open.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
