"""Random-sentinel *impossibility* and quantitative burst-detection
specification for the W33 clipped frame-randomized optical protocol.

If a single shot in a frame may carry arbitrarily large corruption,
s<N randomly inspected sentinels cannot guarantee discovery:
P(miss)=(N-s)/N exactly. At N=200 and a 0.1% watchdog failure
budget one must inspect ALL N shots (s=199 leaves 0.5% miss).
For a sustained burst of b altered samples, exact hypergeometric
miss probability C(N-b,s)/C(N,s) gives finite coverage tradeoffs.

No unwarranted guarantee of m-compromised frames from a sampled
watchdog. Requires trusted full-stream clipping/dual-path monitor.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def miss(N,b,s):
 if s>N-b:return 0.
 return math.comb(N-b,s)/math.comb(N,s)
def certificate():
 N=200;B=1200;alpha=.001
 p199=miss(N,1,199)
 assert abs(p199-.005)<1e-14
 assert miss(N,1,200)==0.
 rows=[]
 for b in (1,2,5,10,20,40,80):
  for goal,alloc in [('single_bad_frame',alpha),('all_frames_union',alpha/B)]:
   feasible=[s for s in range(N+1) if miss(N,b,s)<=alloc]
   s=min(feasible)
   assert miss(N,b,s)<=alloc and (s==0 or miss(N,b,s-1)>alloc)
   rows.append(dict(corruptions_per_frame=b,coverage_model=goal,
                    minimum_independent_random_sentinels=s,
                    fraction_of_frame_sampled=s/N,
                    exact_miss_probability=miss(N,b,s)))
 rng=__import__('numpy').random.default_rng(714)
 sims={}
 for b,s in [(1,100),(40,30),(40,60)]:
  fixed=set(range(b));detected=0;Nrep=10000
  for _ in range(Nrep):
   sampled=set(rng.choice(N,s,replace=False))
   detected+=bool(fixed & sampled)
  expect=1-miss(N,b,s)
  assert abs(detected/Nrep-expect)<.025
  sims[f'b{b}_s{s}']=dict(detection_frequency=detected/Nrep,
                           exact_detection_probability=expect)
 return dict(status='PASS',frames= B,shots_per_frame=N,
   target_watchdog_missed_corruption_budget=alpha,
   one_unbounded_corrupt_shot_sentinel199_miss=p199,
   single_unbounded_corrupt_shot_requires_full_audit_at_0p1pct=True,
   calibration_sentinel_requirements=rows,seeded_simulations=sims,
   information_theoretic_impossibility='For an adversary choosing one shot to corrupt before secret uniformly sampled s of N slots, P(all sentinels miss)=(N-s)/N. Hence 200-shot frames and alpha_watch=0.001 require s=200 if a single unbounded corrupt shot can invalidate optical confidence. This is a simple sampling coverage bound independent of detector distribution.',
   viable_alternatives='Use trusted full-stream analog/digital clipping before frame averaging, continuous redundant interlock with quantified false-negative rate, or a certified deterministic max spike amplitude to absorb undetected faults in good-frame delta budget. Only then may the m-compromised-frame Hoeffding test claim unconditional size alpha.',
   trust_boundary='The hypergeometric burst bounds presume corruption locations are independent of secret sentinels; adaptive corruption able to avoid sentinel locations defeats them. It is not a hardware watchdog implementation or validated detector.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_sentinel_watchdog_limits.json').write_text(json.dumps(d,indent=2)+'\n')
 print('WATCHDOG',[(x['corruptions_per_frame'],x['coverage_model'],x['minimum_independent_random_sentinels']) for x in d['calibration_sentinel_requirements']])
