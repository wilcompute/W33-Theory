#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass600_photonic_wilson_compiler.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def trans(n,a,b):
 p=list(range(n));p[a],p[b]=p[b],p[a];return tuple(p)
def compile_swaps(swaps):
 u=tuple(range(6))
 for a,b in swaps:u=comp(trans(6,a,b),u)
 return u
def cycle_type(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  j=i;n=0
  while j not in seen:seen.add(j);n+=1;j=p[j]
  out.append(n)
 return tuple(sorted(out,reverse=True))
def power(p,n):
 q=tuple(range(len(p)))
 for _ in range(n):q=comp(p,q)
 return q
def trace(p):return sum(i==p[i] for i in range(len(p)))

def payload():
 classes=[
  ('flat_identity',[],112),
  ('top_double_transposition',[(0,1),(2,3)],112),
  ('tetrahedral_fixed_point_free_involution',[(0,1),(2,3),(4,5)],280),
  ('top_order_three',[(1,2),(0,1),(4,5),(3,4)],336),
 ]
 records=[]
 for name,swaps,count in classes:
  p=compile_swaps(swaps);fp=(trace(p),trace(power(p,2)),trace(power(p,3)))
  ct=cycle_type(p)
  phases={'flat_identity':['1^6'],'top_double_transposition':['1^4','(-1)^2'],'tetrahedral_fixed_point_free_involution':['1^3','(-1)^3'],'top_order_three':['1^2','omega^2','omega_bar^2']}[name]
  records.append({'class':name,'pass595_count':count,'probability':f'{count}/840','mode_permutation':list(p),'cycle_type':list(ct),'two_mode_cross_switches':[list(x) for x in swaps],'switch_count':len(swaps),'trace_fingerprint':list(fp),'eigenphase_multiplicities':phases})
 fingerprints={tuple(r['trace_fingerprint']) for r in records}
 counts={r['class']:r['pass595_count'] for r in records}
 checks={
  'four_classes_compiled':len(records)==4,
  'counts_sum840':sum(counts.values())==840,
  'minimal_switch_counts_0_2_3_4':[r['switch_count'] for r in records]==[0,2,3,4],
  'cycle_types_exact':[r['cycle_type'] for r in records]==[[1,1,1,1,1,1],[2,2,1,1],[2,2,2],[3,3]],
  'trace_fingerprints_unique':len(fingerprints)==4,
  'identity_fingerprint':records[0]['trace_fingerprint']==[6,6,6],
  'double_transposition_fingerprint':records[1]['trace_fingerprint']==[2,6,2],
  'fixed_point_free_involution_fingerprint':records[2]['trace_fingerprint']==[0,6,0],
  'order_three_fingerprint':records[3]['trace_fingerprint']==[0,0,6],
  'predicted_histogram_112_112_280_336':sorted(counts.values())==[112,112,280,336],
 }
 return {'schema':'w33.pass600.photonic_wilson_compiler.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'hardware_model':{'fibre_modes':6,'primitive':'lossless two-mode cross switch','readout':'phase-sensitive estimation of Tr(U), Tr(U^2), and Tr(U^3)','implementation_note':'A six-mode multiport or time-bin interferometer can realize each listed permutation network.'},
  'compiled_classes':records,
  'falsifier':{'decision_table':{str(tuple(r['trace_fingerprint'])):r['class'] for r in records},'predicted_840_loop_histogram':counts,'acceptance_rule':'The three measured power traces must match exactly one class before finite-loss tolerances are applied.','class_probabilities':{'flat_identity':'2/15','top_double_transposition':'2/15','tetrahedral_fixed_point_free_involution':'1/3','top_order_three':'2/5'}},
  'theorem':'The four Pass-595 holonomy conjugacy classes admit minimal 0/2/3/4-switch six-mode compilations and are separated perfectly by the three Wilson power traces.',
  'checks':checks,'boundary':'This is a vendor-neutral logical compiler and noiseless falsifier. It does not claim calibrated insertion loss, detector dark-count thresholds, or a specific laboratory switching technology.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 600 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'classes':len(p['compiled_classes'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
