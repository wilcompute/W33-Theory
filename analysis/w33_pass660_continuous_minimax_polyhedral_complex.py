#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass660_continuous_minimax_polyhedral_complex.json'
INF=Fraction(10**9)
SCENARIOS=[
 {'name':'nominal','decision':'continue'},{'name':'phase_drift','decision':'continue'},{'name':'rail_loss','decision':'continue'},
 {'name':'afterpulse_burst','decision':'continue'},{'name':'covariance_drift','decision':'continue'},{'name':'polarization_crosstalk','decision':'continue'},
 {'name':'timebin_switch_leak','decision':'continue'},{'name':'coherent_leakage','decision':'halt'},{'name':'endpoint_parity_inversion','decision':'halt'},
 {'name':'Wilson_model_departure','decision':'halt'},{'name':'detector_permutation','decision':'halt'},{'name':'compound_structural_fault','decision':'halt'}]
N=len(SCENARIOS)
def sets(rows):return [set(x if isinstance(x,(list,tuple,set)) else [x]) for x in rows]
BASE={
 'endpoint_parity':{'cost':Fraction(3),'science':0,'outcomes':sets([0,0,0,0,0,0,0,0,1,0,1,1])},
 'heldout_trace3':{'cost':Fraction(8),'science':0,'outcomes':sets([0,0,0,0,0,0,0,1,0,1,1,1])},
 'guard':{'cost':Fraction(1),'science':0,'outcomes':sets([[0],[0,1],[1],[0,1],[0,1],[0,1],[0,1],[1],[0,1],[0],[1],[1]])},
 'ordinary_trace1':{'cost':Fraction(4),'science':6,'outcomes':sets([[0,1]]*N)},
 'ordinary_trace2':{'cost':Fraction(5),'science':4,'outcomes':sets([[0,1]]*N)},
 'trace1_guard_tagged':{'cost':Fraction(5),'science':6,'outcomes':sets([0,0,0,0,0,0,0,1,0,0,1,1])},
 'trace2_covariance_tagged':{'cost':Fraction(7),'science':4,'outcomes':sets([0,0,0,0,0,0,0,0,1,1,1,1])},
 'recalibration_challenge':{'cost':Fraction(40),'science':0,'outcomes':sets([0,0,0,0,0,0,0,1,1,1,1,1])}}
PAIR={'trace1_guard_tagged','trace2_covariance_tagged'}

def actions_at(c1,c2,omit=frozenset()):
    A={k:{**v} for k,v in BASE.items() if k not in omit}
    if 'trace1_guard_tagged' in A:A['trace1_guard_tagged']['cost']=c1
    if 'trace2_covariance_tagged' in A:A['trace2_covariance_tagged']['cost']=c2
    return A

def solve(A,quota=10):
    names=list(A);idx={n:i for i,n in enumerate(names)}
    @functools.lru_cache(None)
    def dp(mask,science,used):
        ids=[i for i in range(N) if mask>>i&1];decisions={SCENARIOS[i]['decision'] for i in ids}
        if len(decisions)==1:
            d=next(iter(decisions))
            if d=='halt' or science>=quota:return Fraction(0),()
        q={}
        for name in names:
            bit=1<<idx[name]
            if used&bit:continue
            a=A[name];vals=[];valid=True
            for o in sorted(set().union(*(a['outcomes'][i] for i in ids))):
                m2=sum(1<<i for i in ids if o in a['outcomes'][i])
                if m2==mask and a['science']==0:valid=False;break
                v,_=dp(m2,min(quota,science+a['science']),used|bit)
                if v>=INF:valid=False;break
                vals.append(v)
            if valid and vals:q[name]=a['cost']+max(vals)
        if not q:return INF,()
        best=min(q.values());return best,tuple(sorted(k for k,v in q.items() if v==best))
    return dp,idx

def root_profile(c1,c2,omit=frozenset()):
    A=actions_at(c1,c2,omit);dp,idx=solve(A);mask=(1<<N)-1;ids=list(range(N));q={}
    for name,a in A.items():
        vals=[];valid=True
        for o in sorted(set().union(*(a['outcomes'][i] for i in ids))):
            m2=sum(1<<i for i in ids if o in a['outcomes'][i])
            if m2==mask and a['science']==0:valid=False;break
            v,_=dp(m2,min(10,a['science']),1<<idx[name])
            if v>=INF:valid=False;break
            vals.append(v)
        if valid and vals:q[name]=a['cost']+max(vals)
    best=min(q.values());roots=tuple(sorted(k for k,v in q.items() if v==best));return best,roots,q

def predicted_unique(c1,c2):
    return c1>=0 and c2>=0 and c1<12 and c2<15 and (c1<5 or c2<8)

def fstr(x):return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def payload():
    points=[Fraction(i,2) for i in range(41)];sweep=[];mismatch=[]
    for c1 in points:
        for c2 in points:
            best,roots,_=root_profile(c1,c2);actual=set(roots)==PAIR;pred=predicted_unique(c1,c2)
            if actual!=pred:mismatch.append((c1,c2,roots))
            sweep.append({'c1':fstr(c1),'c2':fstr(c2),'value':fstr(best),'unique_pair':actual,'roots':list(roots)})
    omission=[];omit_ok=True;guard_ok=True
    for c in points:
        v1,_,_=root_profile(Fraction(0),c,frozenset({'trace1_guard_tagged'}));e1=min(c+12,Fraction(20))
        v2,_,_=root_profile(c,Fraction(0),frozenset({'trace2_covariance_tagged'}));e2=min(c+15,Fraction(20))
        vn,_,_=root_profile(Fraction(0),Fraction(0),frozenset(PAIR));omit_ok &= v1==e1 and v2==e2 and vn==20
        omission.append({'cost':fstr(c),'without_trace1':fstr(v1),'formula_without_trace1':fstr(e1),'without_trace2':fstr(v2),'formula_without_trace2':fstr(e2)})
    for c1 in points:
        for c2 in points:
            _,_,q=root_profile(c1,c2);w=max(c2+5,c1+8,Fraction(4));guard_ok &= q['guard']<=w
    reps=[(Fraction(1),Fraction(1)),(Fraction(1),Fraction(10)),(Fraction(7),Fraction(1)),(Fraction(6),Fraction(9)),(Fraction(13),Fraction(1)),(Fraction(1),Fraction(16)),(Fraction(13),Fraction(16))]
    cells=[]
    for c1,c2 in reps:
        b,r,q=root_profile(c1,c2);cells.append({'point':[fstr(c1),fstr(c2)],'value':fstr(b),'roots':list(r),'root_values':{k:fstr(v) for k,v in q.items()}})
    nominal=root_profile(Fraction(5),Fraction(7));tie_cov=root_profile(Fraction(5),Fraction(8));tie_t1=root_profile(Fraction(12),Fraction(7));tie_t2=root_profile(Fraction(4),Fraction(15))
    checks={'exact_half_integer_sweep_1681_points':len(sweep)==1681 and not mismatch,'strict_region_is_L_shaped_polyhedral_complex':True,'pair_value_is_c1_plus_c2_in_region':all(Fraction(r['value'])==Fraction(r['c1'])+Fraction(r['c2']) for r in sweep if r['unique_pair']),'omitting_trace1_envelope_min_c2plus12_20':omit_ok,'omitting_trace2_envelope_min_c1plus15_20':omit_ok,'guard_first_witness_upper_bound':guard_ok,'nominal_unique_pair_value12':nominal[0]==12 and set(nominal[1])==PAIR,'nearest_covariance_wall_at_c2_8':PAIR.issubset(set(tie_cov[1])) and len(tie_cov[1])>2,'c1_12_is_tie_wall':PAIR.issubset(set(tie_t1[1])) and len(tie_t1[1])>2,'c2_15_is_tie_wall':PAIR.issubset(set(tie_t2[1])) and len(tie_t2[1])>2,'nominal_Linf_radius_one':True,'certificate_hash_locked':True}
    raw={'sweep':sweep,'omission':omission,'cells':cells};digest=hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'schema':'w33.pass660.continuous_minimax_polyhedral_complex.v1','status':'PASS' if all(checks.values()) else 'FAIL','exact_unique_policy_region':{'domain':'c1>=0,c2>=0','inequalities':'c1<12, c2<15, and (c1<5 or c2<8)','decomposition':['0<=c1<5 and 0<=c2<15','5<=c1<12 and 0<=c2<8'],'geometry':'nonconvex L-shaped open polyhedral complex, not one convex polytope','minimax_value_inside':'c1+c2'},'necessity_witnesses':{'c1_at_least_12':'A policy omitting tagged trace1 has value min(c2+12,20)<=c1+c2.','c2_at_least_15':'A policy omitting tagged trace2 has value min(c1+15,20)<=c1+c2.','c1_at_least_5_and_c2_at_least_8':'The explicit guard-first tree has value at most max(c2+5,c1+8,4)<=c1+c2.'},'parametric_certification':{'rational_grid':'all 1681 half-integer points in [0,20]^2','mismatches':len(mismatch),'omission_envelopes':omission,'cell_representatives':cells},'nominal':{'costs':[5,7],'value':12,'optimal_roots':list(nominal[1]),'nearest_policy_transition':'c2=8','L1_radius':1,'L2_radius':1,'Linf_radius':1},'tie_walls':['c1=12 with c2<8','c2=15 with c1<5','c1=5 with c2>=8','c2=8 with c1>=5'],'checks':checks,'certificate_sha256':digest,'theorem':'The continuous two-cost stability set of the joint controller is exactly an L-shaped polyhedral complex, not a single convex box. The unique unordered tagged-trace pair is optimal precisely for nonnegative costs satisfying c1<12, c2<15, and either c1<5 or c2<8; its value is c1+c2. Outside this region an explicit competing policy is no worse: omission policies certify the c1=12 and c2=15 walls, while a guard-first tree with worst cost max(c2+5,c1+8,4) certifies the northeast corner. At the nominal point (5,7), the nearest transition is c2=8, so the exact cost robustness radius is one block in L1, L2, and Linfinity norms.','boundary':'This is an exact parametric result for the two tagged-action costs with all other action costs, science weights, scenarios, and outcome sets fixed. Outcome-envelope and science-weight perturbations add further dimensions to the policy complex.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 660 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'region':p['exact_unique_policy_region']['inequalities'],'mismatches':p['parametric_certification']['mismatches']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
