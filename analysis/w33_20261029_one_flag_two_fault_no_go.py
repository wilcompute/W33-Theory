#!/usr/bin/env python3
"""Two-fault counterexample census for the W33 one-flag CSS-check schedule.
This is a deliberately NEGATIVE result: one flag suffices to detect dangerous
single CNOT faults but NOT all dangerous pairs of CNOT faults. Enumeration
within each check; not a full multi-check fault-tolerance simulation.
"""
import itertools,json
from collections import Counter
from w33_20261029_minimum_132_check_basis import CHECKS_HEX
DATA=(1<<40)-1

def final_faults(h):
 sites=[j for j in range(40) if h>>j&1]
 gates=[(41,40)]+[(j,40) for j in sites]+[(41,40)]
 out=[]
 for t,(a,b) in enumerate(gates):
  for pa,pb in itertools.product(range(4),repeat=2):
   if not(pa|pb):continue
   x=((pa&1)<<a)|((pb&1)<<b)
   z=(((pa>>1)&1)<<a)|(((pb>>1)&1)<<b)
   for u,v in gates[t+1:]:
    if (x>>u)&1:x^=1<<v
    if (z>>v)&1:z^=1<<u
   out.append((x,z,(t,a,b,pa,pb)))
 return out

def verify():
 hist=Counter();first=None;bad=0;all_pairs=0
 for j,s in enumerate(CHECKS_HEX):
  h=int(s,16);F=final_faults(h)
  for u in range(len(F)):
   for v in range(u+1,len(F)):
    all_pairs+=1
    x=F[u][0]^F[v][0];z=F[u][1]^F[v][1]
    if (z>>41)&1:continue
    dx=x&DATA;dz=z&DATA
    weight=min((dx|dz).bit_count(),(dx|(dz^h)).bit_count())
    hist[(h.bit_count(),weight)]+=1
    if weight>=3:
     bad+=1
     if first is None:first=dict(check_index=j,check_mask_hex=hex(h),
           first_fault=F[u][2],second_fault=F[v][2],
           dataX_hex=hex(dx),dataZ_hex=hex(dz),residual_weight=weight)
 assert bad==26112 and first["dataZ_hex"]=="0x38" and first["residual_weight"]==3
 assert all_pairs==15*(150*149//2)+(210*209//2)
 return dict(status="PROVED_ONE_FLAG_NOT_TWO_FAULT_TOLERANT",
   checks=16,two_CNOT_fault_pairs_enumerated=all_pairs,
   dangerous_unflagged_pairs=bad,first_explicit_counterexample=first,
   unflagged_weight_histogram={f"check_weight_{w}_residual_{d}":int(n) for (w,d),n in sorted(hist.items())},
   fault_model="Two independently placed nonidentity two-qubit Pauli faults after two distinct CNOTs of the same Z-check circuit; propagate through remaining CNOTs; quotient by measured stabilizer.",
   scope="A specific one-flag schedule fails against two faults, not a no-go for general flagged, verified-cat or repeated-syndrome fault tolerance.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
