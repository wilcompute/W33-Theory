"""Randomized exploration of the positive Witting POVM polytope vertex supports."""
import numpy as np
from scipy.optimize import linprog
from collections import Counter
from toe_20261122_round6_minimal_ic import get_mats

def sample(n=4000,seed=481):
 P,A,b=get_mats();rng=np.random.default_rng(seed);seen={};counts=Counter();found=[]
 for k in range(n):
  z=linprog(rng.normal(size=40),A_eq=A,b_eq=b,bounds=(0,None),method='highs')
  if not z.success:continue
  ids=tuple(np.where(z.x>1e-8)[0]);counts[len(ids)]+=1
  if ids not in seen:seen[ids]=z.x[np.array(ids)]
 print('vertices',len(seen),'size hist',Counter(len(x) for x in seen),'LP counts',counts,flush=True)
 keys=list(seen); bits=[sum(1<<j for j in x) for x in keys]
 match=Counter(); example=None
 for i in range(len(keys)):
  bi=bits[i]
  for j in range(i+1,len(keys)):
   n=(bi|bits[j]).bit_count()
   if n<=17:
    union=sorted(set(keys[i])|set(keys[j]));rank=np.linalg.matrix_rank(A[:,union])
    match[(n,rank)]+=1
    if n==17 and rank==16:
     example=(keys[i],keys[j],seen[keys[i]],seen[keys[j]]);print('17 supports FOUND',keys[i],keys[j],flush=True);return example,counts,seen
 print('overlap pair counts',match.most_common(18),flush=True)
 return None,counts,seen
if __name__=='__main__':sample(3000)
