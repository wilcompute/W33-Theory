#!/usr/bin/env python3
"""One-fault Pauli propagation on W33 optimized CSS checks, with one flag.
For a Z-type check h: flag and data controls, syndrome target:
CNOT(flag->syndrome), CNOT(data->syndrome) for each site, CNOT(flag->syndrome).
Flag is prepared |+> and measured X; syndrome prepared |0> and measured Z.
No claim of complete d=6 fault tolerance or multi-round decoding.
"""
import itertools,json
from collections import Counter
from w33_20261029_minimum_132_check_basis import CHECKS_HEX,graph,syndrome

def run_check(h):
 sites=[j for j in range(40) if h>>j&1]
 gates=[(41,40)]+[(j,40) for j in sites]+[(41,40)]
 stats=Counter();failures=[];unflagged_patterns=set();flagged_patterns=set()
 for idx,(a,b) in enumerate(gates):
  for pc,pd in itertools.product(range(4),repeat=2):
   if not(pc|pd):continue
   x=((pc&1)<<a)|((pd&1)<<b)
   z=(((pc>>1)&1)<<a)|(((pd>>1)&1)<<b)
   for ctrl,tgt in gates[idx+1:]:
    if x>>ctrl&1:x^=1<<tgt
    if z>>tgt&1:z^=1<<ctrl
   xd=x&((1<<40)-1);zd=z&((1<<40)-1)
   # Remove a measured Z-check stabilizer if doing so reduces support.
   wt=min((xd|zd).bit_count(),(xd|(zd^h)).bit_count())
   flag=(z>>41)&1
   stats[("flag" if flag else "no_flag",wt)]+=1
   if flag:flagged_patterns.add((xd,zd))
   else:unflagged_patterns.add((xd,zd))
   if wt>2 and not flag:failures.append((idx,pc,pd,hex(xd),hex(zd)))
 assert not failures
 # Include single initial Pauli preparation faults, which can flip readout;
 # check that none has unflagged damaging data propagation.
 for q in (40,41):
  for pauli in (1,2,3):
   x=(pauli&1)<<q;z=((pauli>>1)&1)<<q
   for ctrl,tgt in gates:
    if x>>ctrl&1:x^=1<<tgt
    if z>>tgt&1:z^=1<<ctrl
   xd=x&((1<<40)-1);zd=z&((1<<40)-1)
   wt=min((xd|zd).bit_count(),(xd|(zd^h)).bit_count())
   if wt>2 and not (z>>41&1):failures.append(("prep",q,pauli,wt))
 assert not failures
 return dict(data_weight=h.bit_count(),two_qubit_faults=15*len(gates),
             dangerous_flagged=sum(v for (f,w),v in stats.items() if f=="flag" and w>2),
             dangerous_unflagged=sum(v for (f,w),v in stats.items() if f=="no_flag" and w>2),
             max_unflagged_weight=max(w for(f,w),v in stats.items() if f=="no_flag" and v),
             distinct_flagged_final_data_errors=len(flagged_patterns),
             distinct_unflagged_final_data_errors=len(unflagged_patterns))

def verify():
 A=graph()
 totals=Counter();rows=[]
 for hhex in CHECKS_HEX:
  h=int(hhex,16)
  assert syndrome(A,h)==0
  row=run_check(h);rows.append(row)
  totals.update({"faults":row["two_qubit_faults"],
                 "flagged_dangerous":row["dangerous_flagged"],
                 "unflagged_dangerous":row["dangerous_unflagged"]})
 assert len(rows)==16
 assert totals["faults"]==15*(132+2*16)
 assert totals["unflagged_dangerous"]==0
 assert all(r["max_unflagged_weight"]<=2 for r in rows)
 return dict(status="PASS",check_count=16,Pauli_fault_insertions_after_all_CNOTs=totals["faults"],
             unflagged_data_errors_above_t2=0,
             flagged_data_errors_above_t2=totals["flagged_dangerous"],
             preps_tested_per_check=6,
             per_check=rows,
             gate_schedule="flag->syndrome, all data->syndrome, flag->syndrome",
             boundary="Single Pauli fault analysis only, ideal flag/readout, check-stabilizer equivalence only. Does not prove full d6 FT recovery, two faults, noisy measurement, scheduling across checks, or leakage.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
