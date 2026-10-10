"""Round30 nonperiodic time cover of parallel finite AdS4 null graph.

An external Z clock orients edges, gives a strict causal partial order,
but null graph SRG(81,20,1,6) reaches ALL 81 positions in two ticks.
It is not dynamical 3+1 dimensional Lorentz space.
"""
from pathlib import Path
import json,math,numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass11831_11833_finite_ads4.json'
OUT=ROOT/'data/w33_20261009_toe30_finite_ads_Z_clock.json'
def run():
 existing=json.loads(SRC.read_text())
 assert existing['tangent']['light_cone_graph']['degree']==[20]
 v=81;k=20;lam=1;mu=6
 # Algebraic Cayley incidence A^2=kI+lambda A+mu(J-I-A).
 pair_type={'diagonal':k,'lightlike':lam,'nonlightlike':mu}
 two_step_total=k+(k*lam)+(v-1-k)*mu
 assert two_step_total==k*k # 20+20+60*6=400
 # Because all three counts positive the 2step future cone includes
 # every spatial position, even those not 1step null related.
 accessible={0:1,1:k,2:v,3:v,4:v,5:v}
 stationary=1/v
 # A/k Markov spectrum; no arbitrary high-q limit: 1,0.1,-0.35.
 P_spectrum=[dict(eigenvalue=1.,multiplicity=1),
             dict(eigenvalue=.1,multiplicity=60),
             dict(eigenvalue=-.35,multiplicity=20)]
 mixing=[]
 for t in (0,1,2,3,4,5,8,12):
  collision=(1+60*(.1)**(2*t)+20*(-.35)**(2*t))/81
  l2sq=(60*(.1)**(2*t)+20*(-.35)**(2*t))/81
  returnp=(1+60*(.1)**t+20*(-.35)**t)/81
  mixing.append(dict(tick=t,return_probability=returnp,
   square_L2_dist_from_uniform=l2sq,collision_probability=collision))
 assert abs(mixing[0]['return_probability']-1)<1e-12
 assert mixing[-1]['square_L2_dist_from_uniform']<1e-9
 result=dict(status='PASS',prior='The 81 tangent vectors, 20 null directions, finite group SL2(F9), spinor square map, and SRG(81,20,1,6) originate in parallel Pass11831–11833. Round29 proved finite translation-invariant strict chronology impossible. No claim of new finite AdS kinematics.',
  added_external_clock='Take spacetime event set Z x F3^4 and edges (t,x)->(t+1,x+v) with any of twenty nonzero finite null vectors v. The projection t into Z gives a strict acyclic chronology; it is an *external nonperiodic time input*, not spontaneously emergent.',
  future_support_size_after_exact_steps=accessible,
  exact_two_step_path_counts=pair_type,
  exact_two_step_path_count_identity='A²=20I+A+6(J-I-A): from any location all 81 locations are reachable at exactly two null ticks, with 20 return loops, 1 path to each of 20 neighbors and 6 to each of 60 nonneighbors.',
  causal_metric_obstruction='The causal future support saturates the finite 81-point spatial graph in 2 ticks; this fails a scale-extensive 3+1D light-cone growth law and has no physical length scale. The time extension is not Lorentz-invariant physical 3+1D Minkowski spacetime.',
  reversible_null_walk_spectrum=P_spectrum,
  random_walk_mixing_and_return=mixing,
  gauge_and_gravity_limits='No emergent Einstein equations, 4D continuum, spin2 graviton, experimentally calibrated clock or physical c. Additional geometry with unbounded spatial growth, nontrivial energy action and causal order remains necessary.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('Z CLOCK supports',accessible,'two-step all 81, mixing',mixing[3],flush=True)
 return result
if __name__=='__main__':run()
