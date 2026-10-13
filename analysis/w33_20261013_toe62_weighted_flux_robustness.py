"""TOE62 bonus robustness theorem: global beta7 flux selection with up to
~14% independent per-link positive hopping amplitude errors.

The 238 noncontractible octagon count controls worst-case Fourier weights;
does NOT prove finite-beta dynamical or interacting robustness.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep
from w33_20261013_toe62_leading_flux_theorem import expected
ed,V,*_=prep();E=np.asarray(ed,int);V=np.asarray(V,int)
sing=np.array([79,77,77],float);cross=np.array([2,4,4],float)
def lower(e):return sing*(1-e)**8-2*cross*(1+e)**8
rat=(77/8)**(1/8)
limit=(rat-1)/(rat+1)
assert .13<limit<.15 and min(lower(.1))>0
assert min(lower(limit+.002))<0
def tr8(w,theta):
 z=w*np.exp(1j*V@theta);H=np.zeros((80,80),complex)
 for i,(a,b) in enumerate(E):H[a,b]=-z[i];H[b,a]=-np.conj(z[i])
 hh=H@H;h4=hh@hh
 return float(np.trace(h4@h4).real)
rng=np.random.default_rng(6227);pi=np.full(3,np.pi)
checks=[]
for eps in (.05,.10,.13):
 for trial in range(3):
  w=rng.uniform(1-eps,1+eps,len(E))
  tp=tr8(w,pi)
  for j in range(5):
   th=rng.uniform(-np.pi,np.pi,3)
   lhs=(tr8(w,th)-tp)/16
   rhs=float(lower(eps)@(1-np.cos(th-pi)))
   assert lhs+1e-7>=rhs,(eps,trial,j,lhs,rhs)
  checks.append({'relative_per_link_error_bound':eps,'seeded_trial':trial,
                 'rigorous_lower_coefficients':lower(eps).tolist()})
out={'status':'PASS_TOE62_14_PERCENT_HOPPING_ROBUST_HIGH_T_GLOBAL_FLUX',
'rigorous_uniform_link_weight_deviation_threshold':limit,
'verified_at_eps_0_1':lower(.1).tolist(),
'positive_lower_bound_at_eps_0_13':lower(.13).tolist(),
'random_weighted_graph_trace_checks':checks,
'theorem':"Let EVERY native hopping edge amplitude w_e independently lie in [1-epsilon,1+epsilon], with epsilon>=0. For each simple length8 winding cycle, the positive product of 8 edge amplitudes lies in [(1-epsilon)^8,(1+epsilon)^8]. Native winding census gives one-cycle Fourier single-axis counts (79,77,77) and cross-axis incidences (2,4,4). The same inequality 1-cos(x±y)<=2[(1-cos x)+(1-cos y)] bounds the weighted winding Fourier potential difference S_w(phi)-S_w(pi) below by sum_i [N_i(1-epsilon)^8-2C_i(1+epsilon)^8] (1-cos(phi_i-pi)). All three coefficients strictly positive for epsilon<[(77/8)^(1/8)-1]/[(77/8)^(1/8)+1] ≈0.1405. Therefore the leading beta^7 half-filled fermion holonomy energy still has a UNIQUE GLOBAL continuous U1 minimum at three-pi despite arbitrary nonuniform positive link hopping amplitudes bounded by this epsilon.",
'scope':"An analytic WORST-CASE robustness certificate for the beta7 leading term of one finite spinless tight-binding Hamiltonian, not a measured disorder threshold or finite/all-temperature phase robustness, not coupled quantum gauge backreaction, physical CP breaking, RG or observed standard-model couplings."}
(R/'data/w33_20261013_toe62_weighted_flux_robustness.json').write_text(json.dumps(out,indent=2)+'\n')
print('TOE62 robust epsilon',limit,'alpha .1',lower(.1).tolist(),flush=True)
