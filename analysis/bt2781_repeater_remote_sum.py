#!/usr/bin/env python3
"""Pass 2781: exact qutrit Bell purification and nested remote-SUM repeater model."""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];U=1/9;BOUNDARY=1/3
def isotropic_distribution(F):
 q=(1-F)/8;return {(a,b):(F if (a,b)==(0,0) else q) for a in range(3) for b in range(3)}
def bilateral_sum_purification(dist):
 raw={(a,b):0.0 for a in range(3) for b in range(3)};acc=0.0
 for a in range(3):
  for b in range(3):
   for d in range(3):
    w=dist[a,b]*dist[(-a)%3,d];acc+=w;raw[a,(b-d)%3]+=w
 return acc,{k:v/acc for k,v in raw.items()}
def isotropic_purification(F):
 den=27*F*F-6*F+11;acc=den/32;out=(33*F*F-2*F+1)/den;a,d=bilateral_sum_purification(isotropic_distribution(F));assert abs(a-acc)<1e-12 and abs(d[0,0]-out)<1e-12;return acc,out
def swap(F1,F2):return F1*F2+(1-F1)*(1-F2)/8
def contract(F,v):return U+v*(F-U)
def memory(F,t,T):return contract(F,math.exp(-max(t,0)/T))
def purify(F,rounds):
 factor=1.0;trace=[]
 for r in range(rounds):
  a,n=isotropic_purification(F);factor*=2/a;trace.append({'round':r+1,'input_fidelity':F,'acceptance_probability':a,'output_fidelity':n,'cumulative_raw_pair_factor':factor});F=n
 return F,factor,trace
def evaluate(distance,segments,elementary_rounds,swap_rounds,attempt_rate=1e6,source_fidelity=.806,alpha=.2,node_eff=.55,Tmem=10.0,swap_visibility=.92**2,c_km_s=200000.0):
 if segments<1 or segments&(segments-1):raise ValueError
 levels=int(math.log2(segments));seg=distance/segments;p_link=10**(-alpha*seg/10)*node_eff;rate=attempt_rate*p_link;F,factor,etrace=purify(source_fidelity,elementary_rounds);time=factor/rate;raw=factor;strace=[]
 for level in range(levels):
  span=seg*2**(level+1);lat=span/c_km_s;time=1.5*time+lat;fb=memory(F,time,Tmem);ideal=swap(fb,fb);F=contract(ideal,swap_visibility);raw*=2;ptr=[]
  for r in range(swap_rounds):
   a,n=isotropic_purification(F);time=(2/a)*time+lat;raw*=2/a;ptr.append({'round':r+1,'input_fidelity':F,'acceptance_probability':a,'output_fidelity':n});F=n
  strace.append({'level':level+1,'span_km':span,'memory_degraded_input_fidelity':fb,'ideal_swapped_fidelity':ideal,'level_output_fidelity':F,'post_swap_purification':ptr,'estimated_pair_time_s':time})
 latency=distance/c_km_s;return {'distance_km':distance,'segments':segments,'nesting_levels':levels,'segment_km':seg,'elementary_purification_rounds':elementary_rounds,'swap_purification_rounds':swap_rounds,'elementary_link_probability':p_link,'elementary_link_rate_hz':rate,'raw_pair_factor':raw,'estimated_pair_time_s':time,'classical_latency_s':latency,'remote_sum_rate_hz':1/(time+latency),'final_pair_fidelity':F,'distillable':F>BOUNDARY,'elementary_purification_trace':etrace,'swap_trace':strace}
def pareto(rows):return sorted([r for r in rows if not any(o['final_pair_fidelity']>=r['final_pair_fidelity'] and o['remote_sum_rate_hz']>=r['remote_sum_rate_hz'] and (o['final_pair_fidelity']>r['final_pair_fidelity'] or o['remote_sum_rate_hz']>r['remote_sum_rate_hz']) for o in rows)],key=lambda r:(r['final_pair_fidelity'],r['remote_sum_rate_hz']))
def build():
 fixed=[]
 for F in (U,BOUNDARY,1.0):a,n=isotropic_purification(F);assert abs(n-F)<1e-12;fixed.append({'fidelity':F,'acceptance_probability':a})
 for i in range(1,1000):
  F=i/1000;_,n=isotropic_purification(F)
  if F>BOUNDARY:assert n>F-1e-14
  elif U<F<BOUNDARY:assert n<F+1e-14
 scenarios={}
 for distance in (60,320,640,1280):
  rows=[evaluate(distance,s,e,p) for s in (1,2,4,8,16,32,64) for e in range(4) for p in range(3)];feasible=[r for r in rows if r['distillable']];scenarios[str(distance)]={'best_distillable_rate':max(feasible,key=lambda r:r['remote_sum_rate_hz']) if feasible else None,'best_fidelity':max(rows,key=lambda r:r['final_pair_fidelity']),'pareto_front':pareto(rows)}
 return {'schema':'w33.pass2781.repeater_remote_sum.v1','status':'EXACT_BELL_DIAGONAL_PROTOCOL_WITH_EXPLICIT_ENGINEERING_SCENARIOS','bell_label_transition':{'accept_condition':'target shift c=-a mod 3','retained_label':'(a,b-d mod 3)','accepted_measurement_outcomes':3},'isotropic_recurrence':{'acceptance_probability':'(27 F^2 - 6 F + 11)/32','output_fidelity':'(33 F^2 - 2 F + 1)/(27 F^2 - 6 F + 11)','fixed_points':[U,BOUNDARY,1.0],'fixed_point_checks':fixed,'improvement_region':'F > 1/3'},'swap_recurrence':'F_swap=F1*F2+(1-F1)*(1-F2)/8 before local-operation noise','memory_model':'F(t)=1/9+(F(0)-1/9) exp(-t/T_mem)','scenario_assumptions':{'attempt_rate_hz':1e6,'source_fidelity':.806,'fiber_loss_db_per_km':.2,'combined_elementary_node_efficiency':.55,'memory_coherence_s':10.0,'swap_visibility':.92**2,'classical_speed_km_s':200000.0,'synchronization_model':'(3/2)^nesting_levels first-order waiting overhead'},'scenarios':scenarios,'hardware_contract':{'faults':['link_erasure','memory_timeout','purification_reject','swap_fault','stale_frame'],'success_condition':'one heralded end-to-end qutrit Bell pair above configured fidelity floor','remote_sum_cost_after_pair_ready':'one pair, two trits, all LOCC measurement branches accepted'},'boundary':'The Bell-label recurrences are exact for isotropic qutrit pairs and the stated idealized operations. Rates are explicit engineering scenarios, not measurements. The model does not claim a full fault-tolerance threshold or include correlated hardware noise.'}
def main():
 out=build();p=ROOT/'data/PART_BT2781_REPEATER_REMOTE_SUM.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');s={k:out[k] for k in ('schema','status','bell_label_transition','isotropic_recurrence','swap_recurrence','memory_model','scenario_assumptions','hardware_contract','boundary')};s['scenario_summary']={d:{'best_distillable_rate':x['best_distillable_rate'],'best_fidelity':x['best_fidelity']} for d,x in out['scenarios'].items()};(ROOT/'data/PART_BT2781_REPEATER_REMOTE_SUM_summary.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');print('wrote',p)
if __name__=='__main__':main()
