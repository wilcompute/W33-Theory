"""Native W33 projected two-boson *local* return invariants.
Rational Gaussian phases, exact reductions. Compare sorted 80 sites so an
artificially fixed detector label never masquerades as orbit discrimination.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_round17_interaction_trace_certificate as prior
from w33_20261009_round18_fixedU_resolvent_certificate import projected_returns
from w33_20261008_5state_ritz import geometry
def main():
 edges,*_=geometry()
 reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 results={}
 for p in (1000003,1000033):
  prior.MOD=p
  per_orbit=[]
  for o in reps:
   G=projected_returns(prior.phased_adj(edges,o['representative']),p,19)
   per_orbit.append({str(n):sorted(int(v) for v in np.diag(G[n][0])) for n in range(0,19,2)})
  classification={}
  for n in range(0,19,2):
   keys=[tuple(row[str(n)]) for row in per_orbit]
   groups=[[j for j in range(5) if keys[i]==keys[j]] for i in range(5) if i==next(k for k in range(5) if keys[k]==keys[i])]
   classification[str(n)]={'distinct_unlabelled_site_histograms':len(set(keys)),'groups':groups,
       'distinct_labeled_site_vectors':len(set(tuple(per_orbit[i][str(n)]) for i in range(5)))}
  first=next((n for n in classification if classification[n]['distinct_unlabelled_site_histograms']==5),None)
  print('LOCAL PROBE',p,'classes',[(n,v['distinct_unlabelled_site_histograms'],v['groups']) for n,v in classification.items()],'first',first,flush=True)
  results[str(p)]={'first_complete_histogram':first,'histogram_partitions':classification,'per_orbit_histogram':per_orbit}
 out={'schema':'w33.round19.local_doublon.v1','primes':results,'source':'Exact 80x80 G_n(x,y)=<xx|dGamma(A)^n|yy> for five W33 rational-phase orbit reps. Sort 80 diagonal return amplitudes in each configuration: relabel-invariant but still probes specified physical onsite basis.','scope':'Noninteracting two-boson local returns; any discrimination does NOT require U>0 and is NOT an orbit-invariant full-spectrum distinction. Magnetic phases are imposed.'}
 (ROOT/'data/w33_20261009_round19_local_doublon_probe.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
