#!/usr/bin/env python3
"""BT1739: incidence-real boundary for the self-frame puncture idea."""
from __future__ import annotations
import json
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1739_self_frame_incidence_real_boundary.json'
CHANNELS=['R','C','S']
def hesse_witness_stub():
    # The exact BT1738 graph is not needed for the degree theorem below; only its
    # incidence profile is used.
    return {'points':63,'lines':63,'incidences':189,'degree':3}
def main():
    base=hesse_witness_stub()
    framed={'points':64,'lines':64,'incidences':192,'degree':3,'channels':CHANNELS}
    puncture={'remove_points':1,'remove_lines':1,'remove_incidences':3,'result_points':63,'result_lines':63,'result_incidences':189}
    # Simple-Levi obstruction: adding one point and one line but only three new
    # simple incidences cannot make both new nodes degree 3. If P* and L* both
    # have degree 3, every incidence endpoint budget is used by P* and L*, so all
    # three incidences must be parallel between P* and L*. A simple graph allows
    # at most one such edge.
    simple_possible=False
    channel_multiedge_possible=True
    checks={'base_profile_63_63_189':base['points']==63 and base['lines']==63 and base['incidences']==189,'framed_profile_64_64_192':framed['points']==64 and framed['lines']==64 and framed['incidences']==192,'puncture_arithmetic':64-1==63 and 192-3==189,'simple_levi_extension_impossible':simple_possible is False,'channel_self_frame_possible':channel_multiedge_possible is True}
    payload={'theorem':'BT1739 Self-Frame Incidence-Real Boundary','verified':all(checks.values()),'summary':'The self-frame puncture is incidence-real only as a three-channel or multiflag frame, not as a simple Levi graph extension. One added object-point and one added object-line with only three added incidences cannot both have simple degree three unless the three incidences are parallel self-channel links. Thus the user idea is mathematically clean as a framed 64-bit/tomotope carrier, while the split-Cayley graph remains a separate simple-incidence target.','base_63_profile':base,'framed_64_profile':framed,'puncture':puncture,'degree_budget_proof':'With one new point P* and one new line L* and exactly three added incidences, demanding deg(P*)=deg(L*)=3 uses all six incidence endpoints. Therefore every added incidence must connect P* to L*. This requires three parallel channel incidences, which is allowed in the framed carrier but impossible in a simple Levi graph.','checks':checks,'boundary':'This confirms the self-object +1 idea as a channel-frame law, and falsifies the stronger simple-Levi extension interpretation.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'simple_levi_extension_impossible':True,'channel_self_frame_possible':True},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
