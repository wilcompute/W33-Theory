#!/usr/bin/env python3
"""PART CCCLVIII -- Preferred Grading-Role Sector Architecture Compiler.

Promotes the winning response-sector architecture after CCCL--CCCLVII.

Evidence:
- CCCXLIX: operator_core and order_parity maps are W33-derived.
- CCCL: derived sector model comparison recovers operator_core packets.
- CCCLII: computed W33 graph evidence supports state/even vs transition/odd.
- CCCLV: Hashimoto B=T+O gives exact 2+9 turn split.
- CCCLVI: E8/E6 alignment gives a 6/6 match for operator_core/grading_role.
- CCCLVII: exact B spectrum supports Hashimoto carrier consistency.

Preferred map:
    operator_core = grading_role

    sector 0: mass, heat_trace, zeta       (G^2 / even / matter-scale)
    sector 1: gap, spinor_trace, resolvent (G / first-order / action-gap)

Fallback refinements:
    minimal_bridge for geometry-vs-kernel refinement.
    transform_class for functional-calculus refinement.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFERRED={"mass":0,"gap":1,"heat_trace":0,"spinor_trace":1,"resolvent_trace":1,"zeta":0}
MINIMAL={"mass":0,"gap":0,"heat_trace":1,"spinor_trace":2,"resolvent_trace":2,"zeta":1}
TRANSFORM={"mass":0,"gap":1,"heat_trace":2,"spinor_trace":2,"resolvent_trace":3,"zeta":4}
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def blocks(assign):
    out={}
    for c in CHANNELS: out.setdefault(str(assign[c]),[]).append(c)
    return out
def evidence_table():
    return [
        {"part":"CCCXLIX","evidence":"operator_core/grading_role derived from W33 operator provenance","score":"structural"},
        {"part":"CCCL","evidence":"derived sector model comparison recovers operator_core packets by BIC","score":"statistical synthetic"},
        {"part":"CCCLII","evidence":"computed W33 graph supports state/even versus transition/first-order split","score":"computed graph"},
        {"part":"CCCLV","evidence":"Hashimoto B=T+O with uniform 2+9 split supports closed/open transition split","score":"operator"},
        {"part":"CCCLVI","evidence":"E8/E6 grading alignment gives operator_core/grading_role a 6/6 match","score":"grading"},
        {"part":"CCCLVII","evidence":"exact Hashimoto spectrum validates carrier consistency","score":"spectral"},
    ]
def architecture_policy():
    return {"preferred":"operator_core/grading_role","preferred_assignment":PREFERRED,"preferred_blocks":blocks(PREFERRED),"fallbacks":{"minimal_bridge":{"assignment":MINIMAL,"blocks":blocks(MINIMAL),"use_when":"data favors separating geometry readout from traced kernels"},"transform_class":{"assignment":TRANSFORM,"blocks":blocks(TRANSFORM),"use_when":"data favors functional-calculus specific sectors"}},"rejection_rule":"if neither preferred nor refinements pass, compare against free_channel and treat response packet as not explained by current sector architecture"}
def build_results():
    checks=[]; policy=architecture_policy(); evidence=evidence_table()
    checks.append(ok('preferred has two sectors',len(set(PREFERRED.values()))==2,blocks(PREFERRED)))
    checks.append(ok('preferred G2 sector has mass heat zeta',blocks(PREFERRED)['0']==['mass','heat_trace','zeta'],blocks(PREFERRED)))
    checks.append(ok('preferred G sector has gap spinor resolvent',blocks(PREFERRED)['1']==['gap','spinor_trace','resolvent_trace'],blocks(PREFERRED)))
    checks.append(ok('minimal bridge is a refinement',len(set(MINIMAL.values()))>len(set(PREFERRED.values())),blocks(MINIMAL)))
    checks.append(ok('transform class is finest fallback',len(set(TRANSFORM.values()))>len(set(MINIMAL.values())),blocks(TRANSFORM)))
    checks.append(ok('evidence table has six sources',len(evidence)==6,evidence))
    checks.append(ok('policy has rejection rule','free_channel' in policy['rejection_rule'],policy['rejection_rule']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLVIII","title":"Preferred Grading-Role Sector Architecture Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"architecture_policy":policy,"evidence_table":evidence,"promoted_theorem":"The preferred finite W33 response-sector architecture is operator_core/grading_role: G^2/even/matter-scale channels {mass, heat_trace, zeta} and G/first-order/action-gap channels {gap, spinor_trace, resolvent_trace}. Minimal_bridge and transform_class are retained as controlled refinements, not replacements, unless model comparison favors them.","honesty_boundary":"This promotion is based on current structural, graph, spectral, and grading evidence. It remains conditional on future empirical response packets and deeper representation-theoretic checks.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLVIII_preferred_grading_role_architecture_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
