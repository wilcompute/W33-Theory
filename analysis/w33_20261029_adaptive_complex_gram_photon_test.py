#!/usr/bin/env python3
"""Adaptive trial robustness of the W33-vs-dual three-photon test.

If for EVERY shot t and EVERY observed classical history H_(t-1),
P(success_t|H_(t-1),W33)>=pW, and
P(success_t|H_(t-1),dual)<=pD,
then the total success count is stochastically bounded below/above by
Binomial(N,pW) / Binomial(N,pD), WITHOUT independence or identical trial
probabilities. Conditional constraints (not mere marginals) are critical.

Proof: represent each Bernoulli shot using independent uniforms U_t and
the history-dependent conditional success probability p_t. Compare the
indicator 1[U_t<p_t] pointwise with 1[U_t<pW] or 1[U_t<pD].
Does NOT imply arbitrary temporally entangled photon states meet per-shot
independent product-Gram extrema or correlated noise calibration bounds.
"""
import json,math
from fractions import Fraction as F
from scipy.stats import binom
WMIN=17496/(15**6)
DMAX=6752/(15**6)
def small_exact_dynamic_program():
 # Test optimal adaptive adversary over p in [1/4,3/4].
 # Tail event "at least k successes" is nondecreasing in count, so
 # an adversary maximizing this event always chooses p=3/4.
 p=F(3,4); tested=0
 for N in range(1,10):
  for k in range(1,N+1):
   V=[F(int(j>=k)) for j in range(N+1)]
   for t in range(N,0,-1):
    assert all(V[j]<=V[j+1] for j in range(t))
    V=[(1-p)*V[j]+p*V[j+1] for j in range(t)]
   tail=sum(F(math.comb(N,j))*p**j*(1-p)**(N-j)
            for j in range(k,N+1))
   assert V[0]==tail
   tested+=1
 assert tested==45
 return tested
def verify():
 count=small_exact_dynamic_program()
 N=43047;k=43
 fp=float(binom.sf(k-1,N,DMAX))
 fn=float(binom.cdf(k-1,N,WMIN))
 assert fp<.001 and fn<.001
 # Prior producer exhaustively verified no smaller N meets both error constraints.
 # Reverify its immediate predecessor fails using the optimally chosen FP cutoff.
 Nprev=N-1
 cut=int(binom.isf(.001,Nprev,DMAX))+1
 if binom.sf(cut-1,Nprev,DMAX)>=.001:cut+=1
 assert not (binom.sf(cut-1,Nprev,DMAX)<.001 and
             binom.cdf(cut-1,Nprev,WMIN)<.001)
 return dict(status="PASS",hypotheses="W33 vs dual for the fixed three-photon four-output event",
   per_shot_Gram="May be chosen adaptively based on all previous classical shot outcomes, provided each shot's conditional state satisfies the previous three-independent-photon product-Gram theorem.",
   pW_conditional_floor=WMIN,pDual_conditional_ceiling=DMAX,
   N=43047,cutoff=43,fp_bound=fp,fn_bound=fn,
   exact_small_n_adaptive_dynamic_programs=count,
   theorem="Conditional Bernoulli endpoint coupling gives binomial stochastic domination even with arbitrary classical feedback correlations.",
   previous_globally_minimal_N_source="w33_20261029_adversarial_complex_gram_optical.py",
   validity="Extension of error guarantee, not a new physical protocol or reduction in photon count.",
   boundary="Cannot replace conditional probability bounds by unconditional means; not robust to arbitrary inter-trial quantum entanglement, detector-memory errors violating conditional bounds, or unknown history-dependent drift without uniform per-shot envelopes.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
