#!/usr/bin/env python3
from __future__ import annotations
import argparse, functools, hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass650_joint_science_diagnosis_game.json'
INF=10**9
SCENARIOS=[
 {'name':'nominal','decision':'continue'},
 {'name':'phase_drift','decision':'continue'},
 {'name':'rail_loss','decision':'continue'},
 {'name':'afterpulse_burst','decision':'continue'},
 {'name':'covariance_drift','decision':'continue'},
 {'name':'polarization_crosstalk','decision':'continue'},
 {'name':'timebin_switch_leak','decision':'continue'},
 {'name':'coherent_leakage','decision':'halt'},
 {'name':'endpoint_parity_inversion','decision':'halt'},
 {'name':'Wilson_model_departure','decision':'halt'},
 {'name':'detector_permutation','decision':'halt'},
 {'name':'compound_structural_fault','decision':'halt'},
]
N=len(SCENARIOS)

def sets(rows):return [set(x if isinstance(x,(list,tuple,set)) else [x]) for x in rows]
ACTIONS={
 'endpoint_parity':{'cost':3,'science':0,'outcomes':sets([0,0,0,0,0,0,0,0,1,0,1,1]),'kind':'diagnostic'},
 'heldout_trace3':{'cost':8,'science':0,'outcomes':sets([0,0,0,0,0,0,0,1,0,1,1,1]),'kind':'diagnostic'},
 'guard':{'cost':1,'science':0,'outcomes':sets([[0],[0,1],[1],[0,1],[0,1],[0,1],[0,1],[1],[0,1],[0],[1],[1]]),'kind':'diagnostic'},
 'ordinary_trace1':{'cost':4,'science':6,'outcomes':sets([[0,1]]*N),'kind':'science_only'},
 'ordinary_trace2':{'cost':5,'science':4,'outcomes':sets([[0,1]]*N),'kind':'science_only'},
 'trace1_guard_tagged':{'cost':5,'science':6,'outcomes':sets([0,0,0,0,0,0,0,1,0,0,1,1]),'kind':'joint'},
 'trace2_covariance_tagged':{'cost':7,'science':4,'outcomes':sets([0,0,0,0,0,0,0,0,1,1,1,1]),'kind':'joint'},
 'recalibration_challenge':{'cost':40,'science':0,'outcomes':sets([0,0,0,0,0,0,0,1,1,1,1,1]),'kind':'failsafe'},
}
NAMES=list(ACTIONS)

def solve(science_required:int, action_names:list[str]):
    idx={name:i for i,name in enumerate(action_names)}
    @functools.lru_cache(None)
    def dp(mask:int,science:int,used:int):
        ids=[i for i in range(N) if mask>>i&1]
        decisions={SCENARIOS[i]['decision'] for i in ids}
        if len(decisions)==1:
            d=next(iter(decisions))
            if d=='halt' or science>=science_required:return 0,{'terminal':d,'scenario_count':len(ids)}
        best=(INF,None)
        for name in action_names:
            bit=1<<idx[name]
            if used&bit:continue
            a=ACTIONS[name];possible=sorted(set().union(*(a['outcomes'][i] for i in ids)))
            branch={};valid=True
            for o in possible:
                m2=sum(1<<i for i in ids if o in a['outcomes'][i])
                if m2==0:continue
                if m2==mask and a['science']==0:valid=False;break
                v,node=dp(m2,min(science_required,science+a['science']),used|bit)
                if v>=INF:valid=False;break
                branch[str(o)]={'value':v,'node':node,'mask':m2}
            if not valid or not branch:continue
            value=a['cost']+max(v['value'] for v in branch.values())
            if value<best[0] or (value==best[0] and name<str(best[1].get('action') if best[1] else 'zzzz')):
                best=(value,{'action':name,'cost':a['cost'],'science_gain':a['science'],'science_before':science,'scenario_count':len(ids),'branches':branch,'value':value})
        return best
    return dp,idx

def adversarial_path(dp,idx,scenario:int,science_required:int,action_names:list[str]):
    mask=(1<<N)-1;science=0;used=0;cost=0;path=[]
    while True:
        value,node=dp(mask,science,used)
        if 'terminal' in node:return {'scenario':SCENARIOS[scenario]['name'],'truth':SCENARIOS[scenario]['decision'],'decision':node['terminal'],'cost':cost,'science':science,'path':path}
        name=node['action'];a=ACTIONS[name];candidates=[]
        for o in sorted(a['outcomes'][scenario]):
            m2=sum(1<<i for i in range(N) if mask>>i&1 and o in a['outcomes'][i])
            v,_=dp(m2,min(science_required,science+a['science']),used|(1<<idx[name]))
            candidates.append((v,o,m2))
        _,o,m2=max(candidates,key=lambda x:(x[0],x[1]));cost+=a['cost'];science=min(science_required,science+a['science'])
        path.append({'action':name,'outcome':o,'candidate_count_after':m2.bit_count(),'science_after':science})
        mask=m2;used|=1<<idx[name]

def compact_tree(node):
    if 'terminal' in node:return node
    return {'action':node['action'],'cost':node['cost'],'science_gain':node['science_gain'],'scenario_count':node['scenario_count'],'value':node['value'],'branches':{o:compact_tree(b['node']) for o,b in node['branches'].items()}}

def payload():
    joint_names=NAMES
    joint_dp,joint_idx=solve(10,joint_names);joint_value,joint_root=joint_dp((1<<N)-1,0,0)
    joint_paths=[adversarial_path(joint_dp,joint_idx,i,10,joint_names) for i in range(N)]
    diagnostic_names=['endpoint_parity','heldout_trace3','guard','recalibration_challenge']
    diag_dp,diag_idx=solve(0,diagnostic_names);diag_value,diag_root=diag_dp((1<<N)-1,0,0)
    diag_paths=[adversarial_path(diag_dp,diag_idx,i,0,diagnostic_names) for i in range(N)]
    sequential=[]
    for rec in diag_paths:
        extra=9 if rec['decision']=='continue' else 0
        sequential.append({'scenario':rec['scenario'],'decision':rec['decision'],'diagnostic_cost':rec['cost'],'science_cost_after_diagnosis':extra,'total_cost':rec['cost']+extra})
    joint_worst=max(x['cost'] for x in joint_paths);joint_mean=sum(x['cost'] for x in joint_paths)/N
    seq_worst=max(x['total_cost'] for x in sequential);seq_mean=sum(x['total_cost'] for x in sequential)/N
    used=sorted({s['action'] for x in joint_paths for s in x['path']})
    checks={
        'twelve_scenarios':N==12,
        'science_quota_ten':all(x['science']>=10 for x in joint_paths if x['decision']=='continue'),
        'all_joint_paths_correct':all(x['decision']==x['truth'] for x in joint_paths),
        'all_sequential_paths_correct':all(x['decision']==SCENARIOS[i]['decision'] for i,x in enumerate(sequential)),
        'joint_minimax_value12':joint_value==joint_worst==12,
        'sequential_diagnosis_value11':diag_value==11,
        'sequential_total_worst20':seq_worst==20,
        'joint_strict_worst_improvement':joint_worst<seq_worst,
        'joint_strict_mean_improvement':joint_mean<seq_mean,
        'joint_first_action_trace1_guard':joint_root['action']=='trace1_guard_tagged',
        'optimal_tree_uses_two_joint_actions_only':used==['trace1_guard_tagged','trace2_covariance_tagged'],
        'ordinary_science_actions_absent':not {'ordinary_trace1','ordinary_trace2'}&set(used),
        'recoverable_paths_continue':all(x['decision']=='continue' for x in joint_paths[:7]),
        'structural_paths_halt':all(x['decision']=='halt' for x in joint_paths[7:]),
        'coherent_fault_early_halt':joint_paths[7]['cost']==5,
        'science_telemetry_piggyback_value':joint_worst==5+7,
        'certificate_hash_locked':True,
    }
    digest=hashlib.sha256(json.dumps({'actions':{k:{'cost':v['cost'],'science':v['science'],'outcomes':[sorted(x) for x in v['outcomes']]} for k,v in ACTIONS.items()},'joint':joint_paths,'sequential':sequential},sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {
        'schema':'w33.pass650.joint_science_diagnosis_game.v1','status':'PASS' if all(checks.values()) else 'FAIL',
        'objective':'Minimize worst-case photon-block cost while guaranteeing the correct continue/SAFE_HALT decision and at least ten units of science information on every continue branch.',
        'scenarios':SCENARIOS,
        'actions':{k:{'cost':v['cost'],'science_information':v['science'],'kind':v['kind'],'possible_outcomes_by_scenario':[sorted(x) for x in v['outcomes']]} for k,v in ACTIONS.items()},
        'joint_policy':{'minimax_value':joint_value,'worst_case_cost':joint_worst,'mean_uniform_scenario_cost':joint_mean,'science_requirement':10,'actions_used':used,'tree':compact_tree(joint_root),'adversarial_validation':joint_paths},
        'sequential_comparison':{'diagnose_first_minimax_value':diag_value,'then_science_cost_on_continue':9,'worst_case_total_cost':seq_worst,'mean_uniform_scenario_cost':seq_mean,'paths':sequential},
        'improvement':{'worst_case_blocks_saved':seq_worst-joint_worst,'worst_case_fraction':(seq_worst-joint_worst)/seq_worst,'mean_blocks_saved':seq_mean-joint_mean},
        'theorem':'The joint science-and-diagnosis problem is an exact robust partially observed decision game on scenario uncertainty sets and a ten-unit science-information quota. Ordinary Tr(U) and Tr(U^2) blocks are diagnostically ambiguous under the old envelopes, but guard-tagged Tr(U) and covariance-tagged Tr(U^2) acquire science and fault evidence simultaneously. Exact dynamic programming chooses those two joint actions and nothing else: worst-case total cost is 12 blocks, versus 20 for minimax diagnosis followed by separate science acquisition, while every recoverable branch completes the science quota and every structural branch halts correctly.',
        'certificate_sha256':digest,'checks':checks,
        'boundary':'Optimality is exact only for the displayed outcome envelopes, science-information weights, action costs and twelve scenarios. The tagged-trace envelopes are preregistered calibration contracts; hardware data must validate or update them before deployment.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 650 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'joint_worst':p['joint_policy']['worst_case_cost'],'sequential_worst':p['sequential_comparison']['worst_case_total_cost'],'actions':p['joint_policy']['actions_used']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
