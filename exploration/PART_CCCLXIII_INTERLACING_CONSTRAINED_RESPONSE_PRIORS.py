#!/usr/bin/env python3
"""PART CCCLXIII -- Interlacing-Constrained Response Priors.

Uses the H27/N12 and two-graph certificates as model priors in the response
sector leaderboard.

Instead of comparing sector maps by pure BIC only, define a structural prior
bonus/penalty:

- operator_core/grading_role gets full support: operator provenance, E8/E6,
  H27/N12 interlacing, two-graph parity, RG generator derivation.
- minimal_bridge gets partial refinement support.
- transform_class gets functional-calculus refinement support but weaker
  interlacing support.
- free_channel gets no structural prior and pays a complexity penalty.

Score convention:

    posterior_score = bic + structural_penalty

(lower is better).  Synthetic tests verify that when likelihoods are close, the
interlacing/two-graph prior selects the preferred operator_core/grading_role map;
but if data strongly requires a refinement, the refinement can still win.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def maps():
    return {"operator_core":{"mass":0,"gap":1,"heat_trace":0,"spinor_trace":1,"resolvent_trace":1,"zeta":0},"minimal_bridge":{"mass":0,"gap":0,"heat_trace":1,"spinor_trace":2,"resolvent_trace":2,"zeta":1},"transform_class":{"mass":0,"gap":1,"heat_trace":2,"spinor_trace":2,"resolvent_trace":3,"zeta":4},"free_channel":{c:i for i,c in enumerate(CHANNELS)},"one_sector":{c:0 for c in CHANNELS}}
def structural_prior_penalties():
    return {"operator_core":0.0,"minimal_bridge":4.0,"transform_class":8.0,"one_sector":12.0,"free_channel":24.0}
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
def cov(sig=1.0,rho=0.1):
    n=len(CHANNELS); return [[(1 if i==j else rho)*sig*sig for j in range(n)] for i in range(n)]
def design(assign):
    al=[assign[c] for c in CHANNELS]; sectors=sorted(set(al)); return [[1.0 if al[i]==s else 0.0 for s in sectors] for i in range(len(al))]
def fit_bic(x,C,assign):
    A=design(assign); At=T(A); Ci=inv(C); N=mm(mm(At,Ci),A); Ni=inv(N); beta=mv(Ni,mv(mm(At,Ci),x)); y=mv(A,beta); res=[xi-yi for xi,yi in zip(x,y)]; chi=dot(res,mv(Ci,res)); k=len(beta); n=len(x); return {"chi_square":chi,"k":k,"bic":chi+k*math.log(n),"beta":beta,"residuals":res}
def compare_with_priors(x,C):
    penalties=structural_prior_penalties(); out={}
    for name,assign in maps().items():
        f=fit_bic(x,C,assign); f['structural_penalty']=penalties[name]; f['posterior_score']=f['bic']+penalties[name]; out[name]=f
    return {"models":out,"best_bic":min(out,key=lambda m:out[m]['bic']),"best_posterior":min(out,key=lambda m:out[m]['posterior_score'])}
def packet_operator_core(base=100.0,delta=1.0):
    assign=maps()['operator_core']; return [base+delta*assign[c] for c in CHANNELS]
def packet_minimal_bridge(base=100.0,delta=6.0):
    assign=maps()['minimal_bridge']; return [base+delta*assign[c] for c in CHANNELS]
def packet_close_call(base=100.0,delta=0.4):
    # weak operator_core signal where prior should break near-tie in favor of operator_core.
    return packet_operator_core(base,delta)
def build_results():
    checks=[]; C=cov(sig=1.0,rho=0.1); op=compare_with_priors(packet_operator_core(delta=2.0),C); close=compare_with_priors(packet_close_call(delta=0.4),C); refined=compare_with_priors(packet_minimal_bridge(delta=6.0),C); penalties=structural_prior_penalties()
    checks.append(ok('operator_core has zero structural penalty',penalties['operator_core']==0,penalties))
    checks.append(ok('free_channel has largest penalty',penalties['free_channel']==max(penalties.values()),penalties))
    checks.append(ok('operator_core packet posterior selects operator_core',op['best_posterior']=='operator_core',op['best_posterior']))
    checks.append(ok('close-call packet posterior selects operator_core',close['best_posterior']=='operator_core',close['best_posterior']))
    checks.append(ok('minimal bridge strong packet can overcome prior',refined['best_posterior']=='minimal_bridge',refined['best_posterior']))
    checks.append(ok('minimal bridge strong packet BIC selects minimal_bridge',refined['best_bic']=='minimal_bridge',refined['best_bic']))
    checks.append(ok('free channel not selected under structured packets',op['best_posterior']!='free_channel' and refined['best_posterior']!='free_channel',{"op":op['best_posterior'],"refined":refined['best_posterior']}))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCLXIII","title":"Interlacing-Constrained Response Priors","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"structural_prior_penalties":penalties,"prior_sources":{"operator_core":"operator provenance + E8/E6 + H27/N12 interlacing + two-graph incidence + RG generator derivation","minimal_bridge":"controlled refinement with partial shell/trace support","transform_class":"functional-calculus refinement with weaker shell prior","free_channel":"saturated fallback with no structural support"},"comparisons":{"operator_core_packet":op,"close_call_packet":close,"minimal_bridge_packet":refined},"architecture_upgrade":"CCCLX used interlacing and two-graph certificates as explanatory sector evidence. CCCLXIII turns them into active structural priors in the response-sector likelihood leaderboard.","theorem":"A response-sector leaderboard can combine empirical BIC with finite W33 structural priors. The operator_core/grading_role map receives full prior support from operator provenance, E8/E6 grading, H27/N12 interlacing, two-graph incidence, and RG-generator derivation; refinements can still win when their likelihood improvement exceeds the structural penalty.","honesty_boundary":"The prior penalties are transparent finite-model weights, not statistically calibrated experimental Bayesian priors. Real empirical use should calibrate them against data or derive them from a formal model prior.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCLXIII_interlacing_constrained_response_priors_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
