"""TOE94: conditional, executable finite-shot ququart reconciliation and PA.

An explicitly assumed IID isotropic state supplies test/production errors.
One-sided Clopper-Pearson virtual phase error bound + conservative
ququart entropic uncertainty ledger. Two Hamming(7,4) syndrome planes,
seeded 2-universal verification, and Toeplitz extraction are executed.
No coherent-Eve security, trustless-device proof, authentication,
or physical finite-key QKD is claimed.
"""
from __future__ import annotations
import json,math,random
from scipy.stats import beta
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_conditional_key_ledger import xor_columns,correct_one_block,qary_max_entropy
N_TEST=4096
N_KEY=196
EPS_PE=.001
EPS_PA=1e-6
TAG=16
def phase_upper(k,n=N_TEST,epsilon=EPS_PE):
    if k==n:return 1.
    return float(beta.ppf(1-epsilon,k+1,n-k))
def estimate_key(k):
    qmax=phase_upper(k)
    per=max(0.,2-qary_max_entropy(qmax))
    hmin=N_KEY*per
    transcript=6*(N_KEY//7)+TAG+1
    pa_cost=2*math.log2(1/(2*EPS_PA))
    ell=max(0,math.floor(hmin-transcript-pa_cost))
    return {'test_errors':k,'test_pairs':N_TEST,'phase_error_upper_confidence':round(qmax,12),
      'min_entropy_per_ququart_lower':round(per,12),
      'raw_min_entropy_lower':round(hmin,9),
      'syndrome_bits':6*(N_KEY//7),'verification_tag_bits':TAG,
      'accept_flag_bits':1,'PA_penalty':round(pa_cost,9),
      'conditional_key_bits':ell}
def bin_planes(words):
    return [[(x>>j)&1 for x in words] for j in (0,1)]
def fix_binary_planes(a,b):
    aa,bb=[],[]
    syndromes=0
    for x,y in zip(bin_planes(a),bin_planes(b)):
        corrected=[]
        for start in range(0,N_KEY,7):
            target=x[start:start+7];noisy=y[start:start+7]
            corrected.extend(correct_one_block(noisy,xor_columns(target)))
            syndromes+=3
        aa.extend(x);bb.extend(corrected)
    assert len(aa)==len(bb)==2*N_KEY and syndromes==168
    return aa,bb
def universal_hash(bits,masks):
    packed=sum(x<<j for j,x in enumerate(bits))
    return tuple((packed&m).bit_count()%2 for m in masks)
def toeplitz_hash(bits,ell,seed):
    n=len(bits)
    assert len(seed)==n+ell-1 if ell else len(seed)==n-1
    z=sum(x<<j for j,x in enumerate(bits))
    result=[]
    for i in range(ell):
        mask=sum(seed[n-1+i-j]<<j for j in range(n))
        result.append((mask&z).bit_count()%2)
    return tuple(result)
def check_universal_small():
    n=3;ell=2;errors=0
    from itertools import product,combinations
    for a,b in combinations(range(2**n),2):
        A=[(a>>k)&1 for k in range(n)]
        B=[(b>>k)&1 for k in range(n)]
        collision=0
        for z in product((0,1),repeat=n+ell-1):
            collision+=int(toeplitz_hash(A,ell,z)==toeplitz_hash(B,ell,z))
        assert collision==2**(n-1)
        errors+=1
    return errors
def one_trial(seed,v=.995):
    r=random.Random(seed)
    q=3*(1-v)/4
    pe=sum(r.random()<q for _ in range(N_TEST))
    stats=estimate_key(pe)
    A=[r.randrange(4) for _ in range(N_KEY)]
    B=[x if r.random()>=q else x^r.choice((1,2,3)) for x in A]
    aa,bb=fix_binary_planes(A,B)
    masks=[r.getrandbits(len(aa)) for _ in range(TAG)]
    verified=universal_hash(aa,masks)==universal_hash(bb,masks)
    if verified:assert aa==bb,'Unexpected verification collision in synthetic run'
    ell=stats['conditional_key_bits']
    hashseed=[r.getrandbits(1) for _ in range(len(aa)+ell-1)]
    xa=toeplitz_hash(aa,ell,hashseed)
    xb=toeplitz_hash(bb,ell,hashseed)
    assert (not verified or xa==xb)
    return {'seed':seed,'test_errors':pe,'phase_error_upper_confidence':stats['phase_error_upper_confidence'],
      'actual_production_symbol_errors':sum(x!=y for x,y in zip(A,B)),
      'post_Hamming_remaining_bit_errors':sum(x!=y for x,y in zip(aa,bb)),
      'key_length_admitted':ell,'verification_accepted':verified,
      'matched_extracted_key_when_accepted':verified and xa==xb,
      'released_key_bits':ell if verified else 0}
def certificate():
    universality=check_universal_small()
    runs=[one_trial(94000+i) for i in range(20)]
    accepted=sum(x['verification_accepted'] for x in runs)
    assert universality==28
    assert all(x['test_errors']<=N_TEST for x in runs)
    assert all(x['matched_extracted_key_when_accepted'] for x in runs if x['verification_accepted'])
    return {'source_model':'IID trusted isotropic ququart source, independently held-out virtual conjugate basis phase-error tests and key measurements; phase errors Bernoulli with Q=3(1-v)/4. This is a synthetic conditional model, not calibrated experimental data.',
     'model_visibility':.995,'test_sample_count':N_TEST,'raw_key_pairs':N_KEY,
     'parameter_estimation_failure_budget':EPS_PE,
     'privacy_amplification_failure_budget':EPS_PA,
     'verification_wrong_accept_bound_if_uniform_seed':2**-TAG,
     'conditional_composable_sum_epsilon_under_all_stated_IID_and_trust_premises':EPS_PE+EPS_PA+2**-TAG,
     'protocol':'Generate held-out virtual conjugate basis phase tests; compute binomial one-sided CP upper Q; bound Hmin by a trusted ququart uncertainty relation; announce two Hamming syndromes per 7 raw ququarts; hash-verify with independent public 16-bit universal-2 seed; discard mismatches; extract Toeplitz hash using independent public uniform seed.',
     'finite_sampling_limit':'The CP bound is valid for IID Bernoulli virtual-basis sample rate, but does not apply to arbitrary correlated coherent attacks. A joint finite-size quantum sampling theorem and authenticated classical transcript are not provided.',
     'seed_warning':'The Python seeded random.Random calls are deterministic testing only, not cryptographic random number generation; masks and Toeplitz seeds are illustrative.',
     'toeplitz_exact_small_pair_collision_checks':universality,
     'trials':runs,'accepted_trials':accepted,
     'released_key_bits_total_over_20_synthetic_trials':sum(x['released_key_bits'] for x in runs)}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe94_qkd_finite_iid.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 print('QKD94',d['accepted_trials'],d['released_key_bits_total_over_20_synthetic_trials'],flush=True)
