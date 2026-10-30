#!/usr/bin/env python3
"""W33/dual fixed-port optical discriminator with adversarial complex photon
Gram matrices separately chosen under either hypothesis. Bounds hold for
independent pure or independently mixed internal photons. This is not a
claim of a beyond-QM effect, nor protection against correlated losses.
"""
import json
from math import sqrt
import numpy as np
from scipy.stats import binom
DEN=15**6
def gram(v):
 p=[np.asarray(u,complex)/np.linalg.norm(u) for u in v]
 g=np.array([[np.vdot(a,b) for b in p] for a in p])
 x,y,z=abs(g[0,1])**2,abs(g[0,2])**2,abs(g[1,2])**2
 R=float(np.real(g[0,1]*g[1,2]*g[2,0]))
 return float(x),float(y),float(z),R
def numerators(x,y,z,R):
 return 17496*(1+x+y+z+2*R),3376+3376*x-1024*(y+z)-2048*R
def threshold(pW,pD,alpha=.001,max_n=500000):
 assert 0<=pD<pW<=1
 N=np.arange(1,max_n+1)
 k=np.asarray(binom.isf(alpha,N,pD),np.int64)+1
 fp=binom.sf(k-1,N,pD)
 k+=(fp>=alpha)
 fp=binom.sf(k-1,N,pD)
 fn=binom.cdf(k-1,N,pW)
 ok=(fp<alpha)&(fn<alpha)&(k<=N)
 if not ok.any():return dict(status="NO_FEASIBLE_N",searched=max_n)
 i=int(np.flatnonzero(ok)[0])
 assert not ok[:i].any()
 return dict(N=int(N[i]),threshold=int(k[i]),
             false_positive=float(fp[i]),false_negative=float(fn[i]),globally_minimal_in_scanned_range=True)
def verify():
 # Physically attainable separate worst-case Grams: three orthogonal (W);
 # photon internal vectors 0,1 coincide, 2 orthogonal (D).
 W0,_=numerators(*gram(np.eye(3)))
 _,D1=numerators(*gram([[1,0,0],[1,0,0],[0,1,0]]))
 assert (round(W0),round(D1))==(17496,6752)
 rng=np.random.default_rng(20261029)
 for _ in range(12000):
  v=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
  x,y,z,R=gram(v)
  assert abs(R)<=sqrt(x*y*z)+1e-11
  assert sqrt(x*y*z)<=(x+y+z)/3+1e-11
  assert 2*sqrt(x*y*z)<=y+z+1e-11
  W,D=numerators(x,y,z,R)
  assert W>=17496-1e-8 and D<=6752+1e-8
 budgets={str(eta):threshold(eta**3*17496/DEN,6752/DEN)
          for eta in (1.0,.98,.95,.9,.85)}
 assert budgets["1.0"]["N"]==43047
 assert budgets["0.95"]["N"]==66814
 assert budgets["0.9"]["N"]==115319
 gap=(17496-6752)/DEN
 return dict(status="PASS",fixed_input=[0,7,9],
             four_success_outputs="three-element subsets of [4,14,23,32]",
             exact_w33_min_numerator=17496,exact_dual_max_numerator=6752,
             both_extrema_are_attained=True,minimax_gap=gap,
             gram_variables="x=|g01|^2,y=|g02|^2,z=|g12|^2,R=Re(g01*g12*g20)",
             proof_W="W=17496*(1+x+y+z+2R)>=17496 since R>=-sqrt(xyz) and sqrt(xyz)<=(x+y+z)/3",
             proof_D="D=3376(1+x)-1024(y+z)-2048R<=3376(1+x)<=6752 since 2sqrt(xyz)<=y+z",
             pure_and_product_mixed_photons=True,
             separate_adversarial_internal_Gram_per_hypothesis=True,
             independent_not_necessarily_identically_distributed_trials=True,
             total_variation_separation_under_per_device_opnorm_eps="positive if eps < gap/6, using 3-photon TV<=3*eps for each device",
             per_device_opnorm_eps_strict_bound=gap/6,
             full_triple_survival_eta_min_to1_no_false_registration_budgets=budgets,
             random_complex_Gram_samples=12000,
             limitations="Unknown correlated input internal states, correlated trials, unbounded mode-specific loss, calibration and false clicks excluded. Conventional quantum optics only.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
