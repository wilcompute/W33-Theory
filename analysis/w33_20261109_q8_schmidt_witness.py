#!/usr/bin/env python3
"""Schmidt-number witnesses from the three W33/Q8 eight-MUB Clifford cosets.

Exact proof: F8(rho)=sum_(b,j)(p_bj-1/9)^2 is convex in rho.
For a pure Schmidt-rank <=k state, F8=10/9-2/3*purity(rho_A)
<=10/9-2/(3*k). Convexity extends this tight bound to *all mixed*
states of Schmidt number <=k, k=1,2,3.

This is a known class of nonlinear purity/2-design entanglement witness,
specialized to the W33 Q8-coset frames. Not a TOE or experimental result.
"""
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
from w33_20261109_q8_design_purity import (
    I, mul, order, generators_as_unitaries, partial_purity, purity
)

def families():
    G=sorted(m for m in itertools.product(range(3), repeat=4)
             if (m[0]*m[3]-m[1]*m[2]) % 3 == 1)
    Q=frozenset(g for g in G if order(g) in (1,2,4))
    assert len(G)==24 and len(Q)==8
    cosets=sorted({frozenset(mul(g,q) for q in Q) for g in G},
                  key=lambda v: sorted(v))
    assert len(cosets)==3
    E=generators_as_unitaries(G)
    return [[E[g] for g in sorted(c)] for c in cosets]

def probabilities(E,rho):
    v=np.real(np.sum(E.conj()*(rho@E),axis=0))
    assert abs(sum(v)-1)<2e-11 and min(v)>-2e-11
    return np.clip(v,0,None)

def collision(rho,bases):
    return sum(float(p@p) for E in bases
               for p in [probabilities(E,rho)])-8/9

def schmidt_state(k):
    v=np.zeros(9,dtype=complex)
    for i in range(k):
        v[4*i]=1/math.sqrt(k)
    return np.outer(v,v.conj())

def random_unitary(rng):
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    q,r=np.linalg.qr(z)
    return q@np.diag(np.diag(r)/np.abs(np.diag(r)))

def checks(seed=20261109):
    B=families()
    rng=np.random.default_rng(seed)
    errors=[]
    tight=[]
    for k in (1,2,3):
        rho=schmidt_state(k)
        bound=10/9-2/(3*k)
        vals=[collision(rho,b) for b in B]
        errors.extend(abs(v-bound) for v in vals)
        tight.append({"schmidt_rank":k,"tight_bound":bound,
                      "observed_by_coset":vals})
    assert max(errors)<3e-11

    # Convex extension to *mixed* separable states and Schmidt-number-2 states.
    observed_max={1:float('-inf'),2:float('-inf')}
    mixture_checks=0
    for k in (1,2):
        for how_many in (1,2,4,12):
            for _ in range(14):
                weights=rng.dirichlet(np.ones(how_many))
                rho=np.zeros((9,9),complex)
                for a in weights:
                    x=rng.uniform(0,1,size=k)
                    x/=sum(x)
                    v=np.zeros(9,complex)
                    for i in range(k):
                        v[4*i]=math.sqrt(x[i])
                    v=np.kron(random_unitary(rng),random_unitary(rng))@v
                    rho+=a*np.outer(v,v.conj())
                vals=[collision(rho,b) for b in B]
                observed_max[k]=max(observed_max[k],*vals)
                errors.extend(abs(x-vals[0]) for x in vals)
                assert max(vals)<=10/9-2/(3*k)+3e-11
                mixture_checks+=1
    assert max(errors)<3e-11

    # Reference maximally entangled Choi ray: all cosets have F8=8/9,
    # but their paired-shot collision variances need not agree.
    rho=schmidt_state(3)
    per_basis_c=[[float(p@p) for E in bases
                  for p in [probabilities(E,rho)]] for bases in B]
    variance_coeff=[sum(c*(1-c) for c in row) for row in per_basis_c]
    expected=sorted([56/81,104/81,104/81])
    assert max(abs(a-b) for a,b in zip(sorted(variance_coeff),expected))<3e-11
    aligned=variance_coeff.index(min(variance_coeff))

    # Detection loophole: same uncalibrated outcome-dependent efficiency
    # in every basis, even across the three cosets.
    eta=np.array([0.63+0.045*j for j in range(9)])
    rho0=schmidt_state(1)
    distorted=[]
    calibrated=[]
    for bases in B:
        f_dist=f_corr=0.0
        for E in bases:
            p=probabilities(E,rho0)
            q=eta*p/float(eta@p)
            f_dist+=float(q@q)
            true_p=q/eta
            true_p/=sum(true_p)
            f_corr+=float(true_p@true_p)
        distorted.append(f_dist-8/9)
        calibrated.append(f_corr-8/9)
    assert min(distorted)>4/9+1e-6
    assert max(distorted)-min(distorted)<3e-11
    assert max(abs(x-4/9) for x in calibrated)<3e-11

    # Under ideal independent accepted shots, compare two outcomes per pair.
    # Every match is Bernoulli(c_b), and Hoeffding upper-tail gives
    # P(Fhat-F >= delta) <= exp(-M*delta^2/4).
    # An alpha one-sided lower bound is Fhat-sqrt(4log(1/alpha)/M).
    alpha=.05
    def power_at(M, bound):
        rad=math.sqrt(4*math.log(1/alpha)/M)
        # An aligned Choi ray has one deterministic basis and seven uniform.
        # Fhat=1/9+Binomial(7*M,1/9)/M, exactly.
        floor=math.floor(M*(bound+rad-1/9))
        return float(binom.sf(floor,7*M,1/9))
    minimum_M={}
    for k in (1,2):
        bound=10/9-2/(3*k)
        M=next(m for m in range(2,3500) if power_at(m,bound)>=.95)
        minimum_M[str(k)]={"pairs_per_basis":M,
                           "accepted_preparations_per_coset":16*M,
                           "reference_aligned_maxent_power":power_at(M,bound)}
    assert minimum_M['1']['pairs_per_basis']<minimum_M['2']['pairs_per_basis']
    assert power_at(minimum_M['2']['pairs_per_basis'],7/9)>=.95
    # Isotropic two-qutrit control:
    # rho=eta|Phi><Phi|+(1-eta)I/9 -> F8=(8/9)*eta^2,
    # witness thresholds are eta>1/sqrt2, eta>sqrt(7/8).
    iso_err=0.0
    for eta0 in (0,.25,.5,.625,1/math.sqrt(2),.75,math.sqrt(7/8),1):
        isotropic=eta0*rho+(1-eta0)*np.eye(9)/9
        iso_err=max(iso_err,*(abs(collision(isotropic,b)-8/9*eta0**2) for b in B))
    assert iso_err<3e-11

    return {
      'status':'PASS_EXACT_SCHMIDT_NUMBER_BOUNDS_NUMERIC_CONSISTENCY_AND_VARIANCE',
      'known_prior_art':'Purity separability, Schmidt number and complex unitary 2-design witness methods are known. Contribution is a W33 Q8 coset-specific proof, tight bounds and exact variance-control connection.',
      'tight_schmidt_number_bounds':tight,
      'witness':{'F8_greater_than_4_over_9':'Schmidt number at least 2 (mixed-state entanglement)',
                 'F8_greater_than_7_over_9':'Schmidt number 3 (genuine qutrit dimension)',
                 'convexity_argument':'F8 is a sum of squares of affine functionals in rho; mixture cannot exceed maximal pure Schmidt-k bound'},
      'random_mixtures_tested':mixture_checks,
      'largest_mixed_rank1_or_rank2_observed':observed_max,
      'max_coset_consistency_error':max(errors),
      'isotropic_F8_error':iso_err,
      'isotropic_visibility_cutoffs':{'entangled_witness':1/math.sqrt(2),
                                       'schmidt3_witness':math.sqrt(7/8)},
      'coset_pair_collision_var_times_M':variance_coeff,
      'aligned_coset_index':aligned,
      'paired_collision_variance_ratio_worst_to_best':max(variance_coeff)/min(variance_coeff),
      'maxent_basis_collision_profiles':per_basis_c,
      'product_state_outcome_dependent_loss':{
          'true_F8':4/9,'uncalibrated_F8_by_coset':distorted,
          'calibrated_F8_by_coset':calibrated,
          'false_entanglement_if_uncalibrated':True,
          'cross_coset_spread':max(distorted)-min(distorted)},
      'one_sided_hoeffding_radius':'sqrt(4*ln(1/alpha)/M), M independent shot pairs per basis',
      'aligned_maxent_exact_binomial_power_95pct':minimum_M,
      'limitations':'Ideal calibrated 9-outcome projective measurements, iid preparations, no loss, known settings. Only sufficient Schmidt number witnesses; physical nonlocal Bell entanglement not established by two internal DOFs of one photon. Not a TOE.'
    }

def main(path=None):
    o=checks()
    if path:
        Path(path).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS Q8 mixed Schmidt witness',json.dumps({
        'Schmidt1_threshold':4/9,'Schmidt2_threshold':7/9,
        'variance_ratio':o['paired_collision_variance_ratio_worst_to_best'],
        'false_product_positive':o['product_state_outcome_dependent_loss']['uncalibrated_F8_by_coset'][0],
        '95pct_power_shots_Schmidt3':o['aligned_maxent_exact_binomial_power_95pct']['2']['accepted_preparations_per_coset'],
        'random_mixtures_tested':o['random_mixtures_tested']}))
    return o
if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else None)
