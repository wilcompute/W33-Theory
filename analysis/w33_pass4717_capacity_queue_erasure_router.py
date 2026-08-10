#!/usr/bin/env python3
"""Pass 4717 — exact capacity/queue/erasure envelope of the mixed router.

Pass4685 found the complete two-resource all-pairs path frontier for the
selected270 router.  This pass converts that frontier into a finite-capacity
max-concurrent-flow theorem.  PSp symmetry makes load uniform inside the 1620
base-edge orbit and the 405 Petersen-edge orbit, so the problem is two-dimensional.

With base capacity C_b=1 and shortcut/base capacity ratio rho=C_s/C_b, the
maximum uniform all-pairs demand has three exact breakpoints.  Independent edge
erasures enter by replacing capacities with effective service C*q under an
explicit retransmission model.  A symmetric M/M/1 queue model is also evaluated;
it is a modelling layer, not a hardware measurement.
"""
from __future__ import annotations
import json,math
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4717_CAPACITY_QUEUE_ERASURE_ROUTER_REGEN.json'

# Exact aggregate traversal totals over all C(270,2)=36315 unordered pairs.
P=[
 {'name':'P0','B':56700,'S':32265},
 {'name':'P1','B':73980,'S':14985},
 {'name':'P2','B':83700,'S':8505},
 {'name':'P3','B':100710,'S':0},
]
EB,ES=1620,405;PAIRS=36315
for x in P:
    x['b']=Fraction(x['B'],EB);x['s']=Fraction(x['S'],ES)
assert [(x['b'],x['s']) for x in P]==[(Fraction(35),Fraction(239,3)),(Fraction(137,3),Fraction(37)),(Fraction(155,3),Fraction(21)),(Fraction(373,6),Fraction(0))]

def capacity_formula_region(rho:Fraction):
    a=Fraction(63,155);b=Fraction(111,137);c=Fraction(239,105)
    if rho<a:return 'P2-P3',Fraction(3)*(rho+2)/373
    if rho<b:return 'P1-P2',Fraction(3)*(3*rho+8)/1429
    if rho<c:return 'P0-P1',Fraction(3)*(rho+4)/659
    return 'P0',Fraction(1,35)

def maxload(b,s,rho):return max(b,s/rho)

def queue_delay(B,S,b,s,d,Cb=1.0,Cs=1.0):
    # Mean sum of M/M/1 system times along a route under uniform pair demand d.
    lb=d*float(b);ls=d*float(s)
    if lb>=Cb or ls>=Cs:return math.inf
    return (B/PAIRS)/(Cb-lb)+(S/PAIRS)/(Cs-ls)

def main():
    breaks=[Fraction(63,155),Fraction(111,137),Fraction(239,105)]
    # Verify continuity and endpoint policies.
    for rho in breaks:
        left=capacity_formula_region(rho-Fraction(1,10**9))[1]
        right=capacity_formula_region(rho+Fraction(1,10**9))[1]
        assert abs(float(left-right))<1e-8
    samples=[Fraction(1,4),Fraction(1,2),Fraction(1),Fraction(3,2),Fraction(3)]
    table=[]
    for rho in samples:
        region,lam=capacity_formula_region(rho);table.append({'rho':str(rho),'region':region,'lambda_max':str(lam),'lambda_float':float(lam)})

    # Equal capacities: exact P0/P1 mixture balancing the two edge-orbit loads.
    # Let t be the P1 fraction.  t=67/80 leaves P0 fraction 13/80 and gives
    # b=s=659/15, hence lambda_max=15/659.
    t=Fraction(67,80)
    b=(1-t)*P[0]['b']+t*P[1]['b'];s=(1-t)*P[0]['s']+t*P[1]['s']
    B=(1-t)*P[0]['B']+t*P[1]['B'];S=(1-t)*P[0]['S']+t*P[1]['S']
    assert b==s==Fraction(659,15) and B+S==Fraction(88965)
    lam=Fraction(15,659)
    # Under equal M/M/1 service capacities the same balance minimizes queueing
    # for every 0<d<lambda because P0-P1 keeps total hop count fixed and 1620 db
    # is exactly the negative of 405 ds.
    d=float(lam)/2
    D=queue_delay(float(B),float(S),float(b),float(s),d)
    assert math.isfinite(D)

    # Erasure/retransmission model: each attempted service succeeds independently
    # with q_i, so effective throughput capacity is C_i q_i.  The same theorem
    # applies with rho_eff=(C_s q_s)/(C_b q_b).
    erasure_example={'Cb':1.0,'Cs':1.0,'q_b':0.995,'q_s':0.98}
    rhoeff=Fraction(980,995);reg,leff=capacity_formula_region(rhoeff)
    erasure_example.update({'rho_eff':float(rhoeff),'region':reg,'normalized_lambda_per_Cb_qb':float(leff),'lambda_effective':0.995*float(leff)})

    out={'pass':4717,
      'edge_orbits':{'base_edges':EB,'shortcut_edges':ES},
      'policy_edge_loads':{x['name']:{'base':str(x['b']),'shortcut':str(x['s'])} for x in P},
      'capacity':{'normalization':'C_b=1, rho=C_s/C_b','breakpoints':[str(x) for x in breaks],
        'regions':[
          {'rho':'0 < rho < 63/155','mix':'P2-P3','lambda_max':'3(rho+2)/373'},
          {'rho':'63/155 < rho < 111/137','mix':'P1-P2','lambda_max':'3(3rho+8)/1429'},
          {'rho':'111/137 < rho < 239/105','mix':'P0-P1','lambda_max':'3(rho+4)/659'},
          {'rho':'rho >= 239/105','mix':'P0','lambda_max':'1/35'}],
        'sample_checks':table},
      'equal_capacity':{'optimal_mix':{'P0':'13/80','P1':'67/80'},'per_edge_load':'659/15','lambda_max':'15/659','half_capacity_MM1_mean_system_time_per_pair':D},
      'erasure_retransmission_model':erasure_example,
      'queue_model':'Independent symmetric M/M/1 edge servers; D=(mean base hops)/(C_b-d ell_b)+(mean shortcut hops)/(C_s-d ell_s). Queueing diverges at the max-concurrent-flow boundary.',
      'theorem':'For uniform all-pairs traffic, PSp averaging reduces the selected270 multicommodity capacity problem to the exact two-edge-orbit path frontier. The maximum concurrent-flow envelope has breakpoints rho=63/155,111/137,239/105 and the stated closed forms. Equal capacities are optimally balanced by the 13/80 P0 + 67/80 P1 mixture.',
      'boundary':'Exact symmetric routing/capacity theorem plus explicitly assumed M/M/1 and independent-retransmission models; no measured hardware queueing or failure rate is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
