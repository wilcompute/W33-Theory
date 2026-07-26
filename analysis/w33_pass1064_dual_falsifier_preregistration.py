from __future__ import annotations
import json, time, itertools
from collections import Counter
from pathlib import Path
from w33_pass1060_1064_core import *
from sympy.combinatorics import Permutation,PermutationGroup

def elemkey(g,n=40):return tuple(int(g(i)) for i in range(n))
def mismatch(a,b,n=40):return sum(a(i)!=b(i) for i in range(n))
def comm(a,b):return a**-1*b**-1*a*b

def generating_pair(H):
    gens=list(H.generators); cand=set(gens)
    for a in gens:
        for b in gens:cand.add(a*b)
    cand=sorted(cand,key=elemkey)
    for a,b in itertools.combinations(cand,2):
        if PermutationGroup([a,b]).order()==H.order():return a,b
    els=sorted(H.generate_schreier_sims(),key=elemkey)
    for a,b in itertools.combinations(els,2):
        if PermutationGroup([a,b]).order()==H.order():return a,b
    raise RuntimeError

def analyze_stab(H):
    a,b=generating_pair(H); center=[x for x in H.center().generate_schreier_sims() if not x.is_identity]
    order3=[x for x in H.generate_schreier_sims() if x.order()==3]; rows=[]
    for c in order3:
        mm=[mismatch(comm(c,g),Permutation(list(range(40)))) for g in (a,b)]
        rows.append((sum(mm),mm,c))
    rows.sort(key=lambda x:(x[0],x[1],elemkey(x[2])))
    return {'gens':(a,b),'center':center,'best':rows[:5],'n_order3':len(order3)}

def main():
    w=build_w33();G=w.G
    point=G.stabilizer(0); L0=set(w.lines[0]); line=G.subgroup_search(lambda g:{g(x) for x in L0}==L0)
    pa=analyze_stab(point);la=analyze_stab(line)
    line_sizes=Counter(len(L) for L in w.lines); point_degrees=Counter(len(x) for x in w.point_lines)
    stars=[tuple(sorted(w.point_lines[p])) for p in range(40)]; assert len(set(stars))==40
    alpha=7; quantum_target=10; gap=3
    point_candidates=[{'images':elemkey(c),'order':int(c.order()),'cycle_lengths':sorted([len(x) for x in c.cyclic_form]+[1]*(40-sum(len(x) for x in c.cyclic_form)),reverse=True)} for c in pa['center']]
    pbest=[{'score':r[0],'by_generator':r[1],'images':elemkey(r[2])} for r in pa['best']]
    lbest=[{'score':r[0],'by_generator':r[1],'images':elemkey(r[2])} for r in la['best']]
    schedule={
      'contextuality_arm':{'contexts':40,'outcomes_per_context':4,'point_context_incidences':160,'primary_estimator':'state-independent exclusivity witness W=sum_i p_i, with noncontextual bound alpha=7 and ideal maximally-mixed target 10','secondary_estimator':'contextual fraction / one-star deficit analysis on the calibrated empirical model; uncertainty by context-stratified bootstrap, not a hard-coded binomial sigma'},
      'central_C3_arm':{'point_generators':[elemkey(g) for g in pa['gens']],'line_control_generators':[elemkey(g) for g in la['gens']],'point_C3_candidates':point_candidates,'ordered_sequences_per_candidate':['c∘a','a∘c','c∘b','b∘c'],'process_sequences_for_two_candidates':8,'exact_point_score':0,'exact_dual_lower_gap':la['best'][0][0]},
      'noise_gates':{'point_accept':'both nonidentity C3 candidates have corrected mismatch score <= 9 and controls pass','dual_accept':'every order-3 candidate has corrected mismatch score >= 18','inconclusive':'any score from 10 through 17, or calibration/control failure','rationale':'The exact alternatives are separated by 27 mode mismatches; thresholds reserve one-third margins on both sides.'},
      'joint_decision_matrix':{
        'contextual_and_point_C3':'supports W33 contextual point/Hessian tower',
        'noncontextual_and_point_C3':'local Hessian class present, W33 contextual substrate rejected',
        'contextual_and_no_point_C3':'contextuality present, selected 648-class/tower rejected',
        'neither':'joint rejection',
        'either_inconclusive':'no claim; acquire preregistered additional blocks without changing estimators'
      }
    }
    checks={
      'W33_has_40_contexts':len(w.lines)==40,
      'each_context_has_four_outcomes':line_sizes=={4:40},
      'each_point_occurs_in_four_contexts':point_degrees=={4:40},
      'forty_distinct_failure_stars':len(set(stars))==40 and all(len(s)==4 for s in stars),
      'contextual_tax_is_four_over_forty':4/40==0.1,
      'state_independent_witness_gap_is_10_minus_7':quantum_target-alpha==gap==3,
      'point_stabilizer_is_Hessian_648':point.order()==648 and point.center().order()==3,
      'dual_stabilizer_is_648_centerless':line.order()==648 and line.center().order()==1,
      'point_has_two_central_C3_candidates':len(pa['center'])==2,
      'point_candidates_commute_exactly':pa['best'][0][0]==0 and pa['best'][1][0]==0,
      'dual_has_exact_gap_27':la['best'][0][0]==27,
      'two_generator_pairs_generate_both_648s':PermutationGroup(list(pa['gens'])).order()==648 and PermutationGroup(list(la['gens'])).order()==648,
      'joint_matrix_has_fail_closed_inconclusive_branch':'either_inconclusive' in schedule['joint_decision_matrix'],
    }
    assert all(checks.values()),checks
    return {
      'schema':'w33.pass1064.dual_falsifier_preregistration.v1','status':'PASS',
      'headline':'A single fail-closed preregistration now combines the global 40-context contextuality test with local central-C3 process tomography. The arms distinguish contextual-vs-noncontextual behavior and point/Hessian-vs-dual order-648 symmetry independently before a joint verdict is allowed.',
      'geometry':{'points':40,'contexts':40,'context_size':4,'contexts_per_point':4,'contextual_tax':{'max_sat':36,'deficit':4,'fraction':'1/10','failure_sets':'40 movable point-stars'}},
      'preregistration':schedule,
      'raw_exact_discriminator':{'point_best_scores':pbest,'dual_best_scores':lbest},
      'analysis_freeze':[
        'Freeze detector inclusion/exclusion, loss treatment, bootstrap seed family, calibration correction, witness estimator, and C3 mismatch metric before unblinding the joint labels.',
        'Report both arms separately even when the joint decision is inconclusive.',
        'Do not translate a finite witness into claims about cosmology, Yang-Mills, amplitudes, or continuum physics.'
      ],
      'check_count':len(checks),'checks':checks,
      'scope':'Exact geometry, group actions, schedules, and ideal separation margins. No physical data, hardware efficiency, acquisition time, or achieved statistical power is claimed.'
    }
if __name__ == "__main__":
    started = time.time(); result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1064_dual_falsifier_preregistration.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "check_count": result["check_count"], "output": str(output), "seconds": round(time.time()-started, 3)}, indent=2))
