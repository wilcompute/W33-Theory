#!/usr/bin/env python3
"""Pass 1508: operational contextual-fraction falsifier.

A finite deficit is not an empirical model.  This module accepts complete
context/outcome probability tables, verifies normalization and no-disturbance,
and computes the contextual fraction by the defining linear program.
"""
from __future__ import annotations
import argparse, importlib.util, itertools, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'analysis'/'w33_pass1416_cokernel_signed_turn_intertwiner.py'
OUT=ROOT/'data'/'w33_pass1508_contextuality_protocol.json'
TEMPLATE=ROOT/'data'/'w33_contextuality_empirical_model_template.json'

def load_base():
 s=importlib.util.spec_from_file_location('p1416',BASE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def validate_model(model,tol=1e-9):
 if 'measurements' not in model or 'contexts' not in model:raise ValueError('An empirical model requires measurements and contexts, not a deficit count.')
 outcomes={m['id']:tuple(m['outcomes']) for m in model['measurements']}
 if not outcomes or any(not x for x in outcomes.values()):raise ValueError('Every measurement requires a nonempty outcome set.')
 tables={}
 for ctx in model['contexts']:
  mids=tuple(ctx['measurements'])
  if any(m not in outcomes for m in mids):raise ValueError(f'Unknown measurement in {ctx.get("id",mids)}')
  if 'probabilities' not in ctx:raise ValueError(f'Context {ctx.get("id",mids)} has no empirical probability table.')
  tab={tuple(x['outcome']):float(x['p']) for x in ctx['probabilities']}
  expected=set(itertools.product(*(outcomes[m] for m in mids)))
  if set(tab)!=expected:raise ValueError(f'Context {ctx.get("id",mids)} does not contain the complete outcome table.')
  if any(p < -tol for p in tab.values()) or abs(sum(tab.values())-1)>tol:raise ValueError(f'Context {ctx.get("id",mids)} is not a normalized probability distribution.')
  tables[ctx['id']]=(mids,tab)
 max_gap=0.0
 vals=list(tables.values())
 for i,(m1,t1) in enumerate(vals):
  for m2,t2 in vals[i+1:]:
   shared=tuple(m for m in m1 if m in m2)
   if not shared:continue
   idx1=[m1.index(m) for m in shared];idx2=[m2.index(m) for m in shared]
   marg1={o:0.0 for o in itertools.product(*(outcomes[m] for m in shared))};marg2=dict(marg1)
   for o,p in t1.items():marg1[tuple(o[j] for j in idx1)]+=p
   for o,p in t2.items():marg2[tuple(o[j] for j in idx2)]+=p
   max_gap=max(max_gap,max(abs(marg1[o]-marg2[o]) for o in marg1))
 if max_gap>tol:raise ValueError(f'No-disturbance/compatibility failed; maximum marginal gap {max_gap}.')
 return outcomes,tables,max_gap

def incidence_and_vector(model):
 outcomes,tables,gap=validate_model(model);mids=tuple(outcomes);globals_=list(itertools.product(*(outcomes[m] for m in mids)));gidx={m:i for i,m in enumerate(mids)}
 rows=[];emp=[];labels=[]
 for cid,(ctx,tab) in tables.items():
  idx=[gidx[m] for m in ctx]
  for out,p in sorted(tab.items(),key=lambda x:x[0]):
   rows.append([1 if tuple(g[j] for j in idx)==out else 0 for g in globals_]);emp.append(p);labels.append((cid,out))
 return np.array(rows,dtype=float),np.array(emp,dtype=float),globals_,labels,gap

def contextual_fraction(model):
 M,e,globals_,labels,gap=incidence_and_vector(model)
 res=linprog(-np.ones(M.shape[1]),A_ub=M,b_ub=e,bounds=(0,None),method='highs')
 if not res.success:raise RuntimeError(res.message)
 ncf=max(0.0,min(1.0,float(-res.fun)));return {'contextual_fraction':1.0-ncf,'noncontextual_fraction':ncf,'global_assignments':len(globals_),'event_rows':len(labels),'max_no_disturbance_gap':gap}

def chsh(kind):
 ms=[{'id':x,'outcomes':[0,1]} for x in ('A0','A1','B0','B1')];contexts=[]
 for x,y in itertools.product((0,1),repeat=2):
  probs=[]
  for a,b in itertools.product((0,1),repeat=2):
   if kind=='pr':p=.5 if (a^b)==(x&y) else 0.0
   elif kind=='uniform':p=.25
   elif kind=='deterministic':p=1.0 if (a,b)==(0,0) else 0.0
   probs.append({'outcome':[a,b],'p':p})
  contexts.append({'id':f'A{x}B{y}','measurements':[f'A{x}',f'B{y}'],'probabilities':probs})
 return {'measurements':ms,'contexts':contexts}

def w33_template():
 b=load_base();points,edges,lines,frames,G,M,A,N,d,K=b.build_geometry()
 return {
  'schema':'w33.contextuality.empirical_model.template.v1','status':'AWAITING_EMPIRICAL_DATA',
  'measurements':[{'id':f'p{i}','projective_point':list(map(int,p)),'outcomes':'SPECIFY_EIGENVALUE_LABELS_AND_PHASE_CONVENTION'} for i,p in enumerate(points)],
  'contexts':[{'id':f'L{i}','measurements':[f'p{j}' for j in sorted(L)],'probabilities':'SUPPLY_COMPLETE_JOINT_COUNTS_OR_PROBABILITIES'} for i,L in enumerate(lines)],
  'required_metadata':{'state_preparation':'SPECIFY','observable_operators_and_phases':'SPECIFY','source_heralding':'SPECIFY','detector_model':'SPECIFY','loss_and_postselection_rule':'SPECIFY','compatibility_calibration':'SPECIFY','feed_forward_and_timing':'SPECIFY'},
  'rejected_shortcut':{'bad_contexts':4,'total_contexts':40,'ratio':0.1,'reason':'A 4/40 combinatorial deficit is not a table of empirical outcome probabilities and therefore is not an input to the contextual-fraction LP.'}
 }

def certificate():
 tests={k:contextual_fraction(chsh(k)) for k in ('uniform','deterministic','pr')};template=w33_template()
 rejected=False
 try:contextual_fraction({'bad_contexts':4,'total_contexts':40})
 except ValueError:rejected=True
 checks={
  'uniform_CHSH_CF_zero':abs(tests['uniform']['contextual_fraction'])<1e-9,
  'deterministic_CHSH_CF_zero':abs(tests['deterministic']['contextual_fraction'])<1e-9,
  'PR_box_CF_one':abs(tests['pr']['contextual_fraction']-1)<1e-9,
  'self_tests_no_disturbance':all(x['max_no_disturbance_gap']<1e-9 for x in tests.values()),
  'deficit_only_input_rejected':rejected,
  'W33_template_40_measurements':len(template['measurements'])==40,
  'W33_template_40_contexts':len(template['contexts'])==40,
  'each_W33_context_has_four_measurements':all(len(x['measurements'])==4 for x in template['contexts']),
 }
 checks={k:bool(v) for k,v in checks.items()}
 return {
  'schema':'w33.pass1508.contextuality_protocol.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'theorem':('The contextual fraction is computable only from a complete empirical probability model. The defining LP and no-disturbance gate pass exact CHSH self-tests (uniform and deterministic models have CF 0; the PR box has CF 1). The W33 4/40 deficit is rejected as insufficient input, and a 40-context acquisition template is emitted.'),
  'self_tests':tests,'checks':checks,
  'claim_falsifier':{'claim':'operational contextual fraction equals 1/10','pass_condition':'A completed W33 empirical table passes normalization and compatibility gates and the contextual-fraction LP returns 0.1 within a predeclared statistical confidence region.','automatic_fail_conditions':['only the combinatorial ratio 4/40 is supplied','outcome tables are incomplete or unnormalized','overlap marginals violate the predeclared compatibility tolerance','loss/postselection rules are changed after observing the result','the physical measurement operators or phase conventions are unspecified']},
  'optical_resource_ledger':['heralded state/source specification','implemented commuting-context measurements','detector efficiency and dark-count model','loss and postselection convention','active feed-forward/timing model if universality is claimed','raw counts for every context and outcome','compatibility/no-disturbance calibration','predeclared LP and uncertainty analysis'],
  'primary_references':[{'id':'arXiv:1705.07918','role':'contextual-fraction definition and LP'},{'id':'arXiv:1401.4174','role':'contextuality as magic in the specified odd-prime stabilizer framework'},{'id':'arXiv:quant-ph/0006088','role':'linear-optical universality resource model and feed-forward'}],
  'boundary':'This pass supplies the operational calculation and falsification protocol. It does not manufacture experimental probabilities from finite geometry and therefore does not assert CF=1/10.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--template',type=Path,default=TEMPLATE);ap.add_argument('--check',action='store_true');ap.add_argument('--model',type=Path);a=ap.parse_args()
 if a.model:print(json.dumps(contextual_fraction(json.loads(a.model.read_text())),sort_keys=True));return 0
 p=certificate();template=w33_template();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n';t=json.dumps(template,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s or not a.template.exists() or a.template.read_text()!=t:raise SystemExit('Pass 1508 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s);a.template.write_text(t)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'self_tests':{k:v['contextual_fraction'] for k,v in p['self_tests'].items()}}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
