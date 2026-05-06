#!/usr/bin/env python3
"""PART CCCL -- W33-Derived Sector Model Comparison Compiler.

Uses the sector maps derived in CCCXLIX as actual model hypotheses, then applies
the CCCXLVII multi-sector GLS comparison logic.  This replaces synthetic sector
choices with W33 operator-provenance maps:

    one_sector, operator_core, order_parity, trace_flag, minimal_bridge,
    transform_class, free_channel.

Synthetic packets are generated from each derived map and the compiler verifies
that BIC selects the generating map when the signal is structured and not too
fine-grained, while free_channel saturates deliberately unstructured data.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Any, Dict, List
ROOT=Path(__file__).resolve().parents[1]
Q=3; K=12; V=40; PHI3=Q*Q+Q+1; PHI6=Q*Q-Q+1; B=2*V-PHI3; A0=(V//2)*PHI6; DELTA=B*B+4*A0; M2_DIMLESS=DELTA/4.0
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def inv(M):
    n=len(M); A=[row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(M)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]; piv=A[c][c]
        if abs(piv)<1e-30: raise ValueError('singular')
        A[c]=[x/piv for x in A[c]]
        for r in range(n):
            if r==c: continue
            f=A[r][c]; A[r]=[A[r][j]-f*A[c][j] for j in range(2*n)]
    return [row[n:] for row in A]
def T(M): return [list(row) for row in zip(*M)]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A,v): return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cov(sig=0.02,rho=0.10):
    n=len(CHANNELS); return [[(1.0 if i==j else rho)*sig*sig for j in range(n)] for i in range(n)]
def canonical(labels):
    order=[]; out={}
    for c in CHANNELS:
        lab=labels[c]
        if lab not in order: order.append(lab)
        out[c]=order.index(lab)
    return out
def derived_maps():
    return {
        "one_sector": {c:0 for c in CHANNELS},
        "operator_core": {"mass":0,"gap":1,"heat_trace":0,"spinor_trace":1,"resolvent_trace":1,"zeta":0},
        "order_parity": {"mass":0,"gap":1,"heat_trace":0,"spinor_trace":1,"resolvent_trace":1,"zeta":0},
        "trace_flag": {"mass":0,"gap":0,"heat_trace":1,"spinor_trace":1,"resolvent_trace":1,"zeta":1},
        "minimal_bridge": {"mass":0,"gap":0,"heat_trace":1,"spinor_trace":2,"resolvent_trace":2,"zeta":1},
        "transform_class": {"mass":0,"gap":1,"heat_trace":2,"spinor_trace":2,"resolvent_trace":3,"zeta":4},
        "free_channel": {c:i for i,c in enumerate(CHANNELS)},
    }
def assignment_list(assignment): return [assignment[c] for c in CHANNELS]
def design(assign):
    sectors=sorted(set(assign)); return [[1.0 if assign[i]==s else 0.0 for s in sectors] for i in range(len(assign))],sectors
def fit(x,C,assignment):
    assign=assignment_list(assignment) if isinstance(assignment,dict) else assignment
    A,sectors=design(assign); At=T(A); Ci=inv(C); N=mm(mm(At,Ci),A); Ni=inv(N); beta=mv(Ni,mv(mm(At,Ci),x)); yhat=mv(A,beta); res=[xi-yi for xi,yi in zip(x,yhat)]; chi2=dot(res,mv(Ci,res)); n=len(x); k=len(beta); dof=n-k
    return {"sectors":sectors,"sector_scales":beta,"k":k,"chi_square":chi2,"degrees_of_freedom":dof,"reduced_chi_square":chi2/dof if dof else 0.0,"aic":chi2+2*k,"bic":chi2+k*math.log(n),"residuals":res}
def compare_all(x,C):
    maps=derived_maps(); models={name:fit(x,C,assignment) for name,assignment in maps.items()}
    return {"models":models,"best_aic":min(models,key=lambda m:models[m]['aic']),"best_bic":min(models,key=lambda m:models[m]['bic'])}
def packet_from_map(map_name,base=6872.25,step=35.0):
    assignment=derived_maps()[map_name]; vals=[]
    for c in CHANNELS:
        vals.append(base + step*assignment[c])
    return vals
def block_signature(assignment):
    blocks={}
    for c in CHANNELS: blocks.setdefault(str(assignment[c]),[]).append(c)
    return blocks
def build_results():
    checks=[]; C=cov(sig=0.02,rho=0.10); maps=derived_maps()
    packets={name:packet_from_map(name) for name in ["one_sector","operator_core","trace_flag","minimal_bridge","transform_class"]}
    comparisons={name:compare_all(x,C) for name,x in packets.items()}
    unstructured=[6872.25,6900.1,6888.7,6942.3,6860.4,6921.2]; unstructured_cmp=compare_all(unstructured,C)
    checks.append(ok('dimensionless W33 M2=5049/4',abs(M2_DIMLESS-5049/4)<1e-15,M2_DIMLESS))
    checks.append(ok('operator_core data selects operator_core by BIC',comparisons['operator_core']['best_bic']=='operator_core',comparisons['operator_core']['best_bic']))
    checks.append(ok('trace_flag data selects trace_flag by BIC',comparisons['trace_flag']['best_bic']=='trace_flag',comparisons['trace_flag']['best_bic']))
    checks.append(ok('minimal_bridge data selects minimal_bridge by BIC',comparisons['minimal_bridge']['best_bic']=='minimal_bridge',comparisons['minimal_bridge']['best_bic']))
    checks.append(ok('transform_class data selects transform_class by BIC',comparisons['transform_class']['best_bic']=='transform_class',comparisons['transform_class']['best_bic']))
    checks.append(ok('one_sector data selects one_sector by BIC',comparisons['one_sector']['best_bic']=='one_sector',comparisons['one_sector']['best_bic']))
    checks.append(ok('unstructured data selects free_channel by AIC',unstructured_cmp['best_aic']=='free_channel',unstructured_cmp['best_aic']))
    checks.append(ok('operator_core and order_parity maps agree',maps['operator_core']==maps['order_parity'],maps['operator_core']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCL","title":"W33-Derived Sector Model Comparison Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"derived_maps":{name:{"assignment":assignment,"blocks":block_signature(assignment),"sector_count":len(set(assignment.values()))} for name,assignment in maps.items()},"synthetic_packets":packets,"comparisons":comparisons,"unstructured_comparison":unstructured_cmp,"architecture_upgrade":"CCCXLIX derived sector maps from W33 operator provenance. CCCL uses those maps as actual GLS/BIC model hypotheses and verifies that generated sector structure is selected over one-sector and free-channel alternatives.","theorem":"W33-derived sector maps can be treated as statistical model hypotheses. If response scales are generated by one of the provenance-derived maps, GLS/BIC recovers that map; if the packet is unstructured, the free-channel alternative is selected instead.","honesty_boundary":"The packets here are synthetic. Real use requires measured response scales or response scales derived from deeper W33 operator data.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCL_derived_sector_model_comparison_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
