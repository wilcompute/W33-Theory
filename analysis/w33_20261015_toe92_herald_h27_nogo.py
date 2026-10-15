"""TOE92 adversarial device check and exact H27 set-map obstruction.

Exact separable quantum product attack with basis-dependent selection,
plus stronger joint-outcome heralding attack with PERFECTLY BALANCED
per-basis acceptance. Establish cardinality obstruction to a total
equivariant map from Witting rays/edge events into regular H27 address
or oriented Schlaefli edge targets.
"""
from __future__ import annotations
import json
from fractions import Fraction
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
import numpy as np
def certificate():
 R=np.asarray(construct_witting_40_rays());B=[tuple(x) for x in find_tetrads(list(R))]
 r=R[0]
 P=[]
 for b in B:P.append(sum(abs(np.vdot(r,R[k]))**4 for k in b))
 P=[Fraction(1) if abs(float(p)-1)<1e-10 else Fraction(1,3) if abs(float(p)-1/3)<1e-10 else None for p in P]
 assert P.count(Fraction(1))==4 and P.count(Fraction(1,3))==36
 avg=sum(P)/40
 assert avg==Fraction(2,5)
 eta_min=Fraction(94,100);eta_max=Fraction(98,100)
 # For the *particular product state*, maximizing the ratio selects
 # high efficiency in four perfect contexts, low elsewhere.
 weighted=(4*eta_max+36*eta_min*Fraction(1,3))/(4*eta_max+36*eta_min)
 assert weighted>Fraction(2,5)
 universal=Fraction(2,5)*eta_max/eta_min
 assert weighted<=universal
 # Stronger loophole: joint matched-outcome selection.
 # For every basis choose to retain exactly t=1/3 of its total trials,
 # but accept ONLY those with matching outcomes; possible because p_B>=1/3.
 # Accept matched outcomes with probability alpha_B=(1/3)/p_B.
 # 4 perfect contexts: alpha=1/3, 36 other: alpha=1.
 t=Fraction(1,3)
 alphas=[t/p for p in P]
 assert set(alphas)=={Fraction(1,3),Fraction(1)}
 accept_by_basis=[p*alpha for p,alpha in zip(P,alphas)]
 assert all(a==t for a in accept_by_basis)
 retained_match=sum(p*alpha for p,alpha in zip(P,alphas))/sum(accept_by_basis)
 assert retained_match==1
 # Group theory obstruction:
 # If H27 acts *freely* on Y (regular 27 point addresses or all 270
 # oriented Schlaefli edges), equivariance f:X->Y forces every x to have
 # trivial stabilizer, hence X must be a disjoint union of 27-element
 # free orbits: |X| divisible by 27.
 sizes=[40,480]
 assert all(n%27!=0 for n in sizes)
 target_counts={'H27_regular_cubic_addresses':27,'Schlaefli_directed_edges':270,'Schlaefli_unoriented_edges':135}
 assert all(v%27==0 for v in target_counts.values())
 return {
  'quantum_state':'|Witting_ray_0><Witting_ray_0| on Alice tensor conjugate ray_0 pure projector on Bob (separable)',
  'basis_match_probabilities':{'p=1_contexts':4,'p=1/3_contexts':36},
  'unconditioned_uniform_basis_match':str(avg),
  'setting_efficiency_min':str(eta_min),'setting_efficiency_max':str(eta_max),
  'constructive_basis_efficiency_attack_conditional_match':str(weighted),
  'setting_efficiency_ratio_universal_separable_upper_bound':str(universal),
  'uniform_per_basis_acceptance_outcome_attack':{
    'accepted_fraction_each_of_40_bases':str(t),
    'accepted_fraction_globally':str(t),
    'conditioned_match':str(retained_match),
    'accept_probability_if_match_in_four_perfect_bases':str(Fraction(1,3)),
    'accept_probability_if_match_in_other_36_bases':str(Fraction(1)),
    'accept_probability_if_mismatch':'0',
    'adversary_capability':'A malicious joint coincidence/postselection unit compares Alice and Bob outcomes AFTER measurements and then flags acceptance, while maintaining identical 1/3 overall acceptance on every setting.',
    'security_conclusion':'PER-BASIS acceptance-rate equality is not sufficient by itself. Herald flag must be generated independently of both secret measurement outcomes (or constrain the full outcome-dependent instrument).'
   },
  'equivariant_total_set_map_no_go':{
    'group':'H27 acts regularly on 27 Schlaefli vertices, so freely on ordered edges and, because |H27| odd, freely on unoriented edges.',
    'source_cardinalities':[40,480],
    'target_cardinalities':target_counts,
    'source_mod_27':[40%27,480%27],
    'formal_proof':'If y=f(x) and f is H27-equivariant, then Stab(x) subset Stab(y). A free target implies Stab(x)=1; every domain orbit has 27 elements. Since 40 and 480 are not divisible by 27, no such total equivariant deterministic set map exists, for ANY H27 action on either source.',
    'minimum_discarded_points_for_free_subset_at_cardinality_level':13,
    'minimum_discarded_directed_events_for_free_subset_at_cardinality_level':21,
    'what_is_not_ruled_out':'Partial/symmetry-breaking maps, coarse-graining, linear equivariant maps between chain modules, stochastic channels, embedding after adding ancillas or changing group action, or genuinely engineered physical interfaces.'
  },
  'no_go_scope':'Mathematical cardinality obstruction and synthetic malicious herald model. Not an experimental detector attack or universal no-go for quantum CSS conversions.'}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe92_herald_h27_nogo.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 print('ATTACK',d['uniform_per_basis_acceptance_outcome_attack'],'NO GO',d['equivariant_total_set_map_no_go']['source_mod_27'])
