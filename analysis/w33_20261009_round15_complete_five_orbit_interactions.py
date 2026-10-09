"""Complete the five 86,400-selector PSp orbit labels using three
native three-input/four-input incidence correlation witnesses.

Last round proved ALL five orbits exactly isospectral under any
single-photon Peierls flux. Nevertheless, source-conditioned
higher-order incidence correlators can distinguish them:

Cp=sum_x prod_i [x collinear p_i]
Cl=sum_L prod_i [L meets line_i]
J=sum_{x,i}(prod_j [x collinear p_j])*[x on line_i]

The 5 orbit signatures (Cp,Cl,J) are distinct. Each is PSp invariant.
Find SMALL INTEGER 3-correlation Hamiltonian coefficients selecting
each one of the five orbits with a strictly positive classical gap.
This closes the engineering selection problem at finite order for all
five group orbits, including three trivial-stabilizer ones.
NOT a fundamental microscopic interaction or actual 3-photon gate.
"""
import json,sys,itertools
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
def certificate():
 edges,N,*_=geometry();assert N.shape==(40,40)
 PP=(N@N.T)==1;LL=(N.T@N)==1
 orbit=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 results=[]
 for o in orbit:
  tri=o['representative'];p=[edges[z][0] for z in tri];l=[edges[z][1]-40 for z in tri]
  centers=np.all(PP[:,p],axis=1)
  transversals=np.all(LL[:,l],axis=1)
  cp=int(centers.sum());cl=int(transversals.sum())
  j=int(N[np.ix_(np.flatnonzero(centers),l)].sum())
  results.append(dict(representative=tri,orbit_size=o['orbit_size'],stabilizer_order=o['stabilizer_order'],
      common_point_correlator=cp,common_line_correlator=cl,
      incidence_weighted_four_body_correlator=j,signature=[cp,cl,j]))
 assert len({tuple(r['signature']) for r in results})==5
 assert sum(r['orbit_size'] for r in results)==86400
 # Tiny integer Hamiltonians: E(T)=w_p Cp(T)+w_l Cl(T)+w_j J(T)
 witnesses=[]
 vectors=[np.asarray(r['signature']) for r in results]
 for i,rr in enumerate(results):
  options=[]
  for w in itertools.product(range(-5,6),repeat=3):
   if not any(w):continue
   E=[int(np.dot(np.array(w),q)) for q in vectors]
   if E[i]<min(E[:i]+E[i+1:]):
    gap=min(E[:i]+E[i+1:])-E[i]
    options.append((sum(abs(x) for x in w),max(abs(x) for x in w),-gap,w,gap,E))
  assert options,(i,rr)
  best=min(options);w=best[3];gap=best[4];E=best[5]
  witnesses.append(dict(target_orbit_representative=rr['representative'],
     coefficients=[int(x) for x in w],ground_degeneracy=rr['orbit_size'],
     selected_ground_energy=E[i],first_orbit_gap=int(gap),
     five_orbit_energies=E))
 return dict(status='PASS',native_flag_orbits=len(results),optimal_selectors=86400,
  complete_five_PSp_signatures=results,distinct_signature_count=5,
  engineered_linear_orbit_selection_Hamiltonians=witnesses,
  theorem='The three PSp-invariant native incidence correlators Cp,Cl,J distinguish all five optimal three-flag orbits. For EACH orbit, explicit small integer coefficients of H=w1 Cp+w2 Cl+w3 J give a unique lowest ORBIT, finite positive class gap and correct group orbit degeneracy.',
  observable='Cp and Cl are triple-input coincidence/motif counts; J conditions a triple-point common-neighbor event on a selected line. They require information beyond the one-particle Peierls band eigenvalues, not necessarily many-body scattering.',
  limitation='These are engineered classical finite selector energies and incidence-pattern observables. No physical nonlinear interaction, three-photon gate, thermodynamic spontaneous symmetry breaking, emergent 3-space or Lorentzian gravitation has been derived.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round15_complete_five_orbit_interactions.json').write_text(json.dumps(d,indent=2)+'\n')
 print('FIVE SIGNATURES',[(x['signature'],x['orbit_size']) for x in d['complete_five_PSp_signatures']])
 print('FIVE HAMILTONIANS',[(x['coefficients'],x['first_orbit_gap']) for x in d['engineered_linear_orbit_selection_Hamiltonians']])
