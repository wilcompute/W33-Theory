"""Source-native cubic *necessary* non-Abelian tensor invariant sieve.
No false implication from charge-neutral/R-allowed to nonzero CFT amplitude.
Specific tested representations SU3 x SU2_L x SU4_H x SU2_H.
"""
from pathlib import Path
import sys,json,math
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P

def su2_ok(vals):
    n=sum(abs(v)==2 for v in vals)
    return n in (0,2) # for at most 3 reps (all 1 or 2)
def su3_ok(vals):
    non=[v for v in vals if abs(v)!=1]
    return not non or (len(non)==2 and sorted(non)==[-3,3]) or (len(non)==3 and len(set(non))==1 and abs(non[0])==3)
def su4_ok(vals):
    non=[v for v in vals if abs(v)!=1]
    if not non:return True
    if len(non)==2:
        return sorted(non)==[-4,4] or non==[6,6] or sorted(non)==[-6,-6] # 6 is self-dual
    if len(non)==3:
        return sorted(non)==[4,4,6] or sorted(non)==[-4,-4,6] or sorted(non)==[-4,4,1] # last can't occur (len3)
    return False
def main():
 raw,prior,fields,support,q=P.load()
 names=sorted(fields)
 den=math.lcm(*(x.denominator for v in q.values() for x in v))
 ch=[tuple(int(x*den) for x in q[n]) for n in names]
 pairs=defaultdict(list)
 for i in range(len(names)):
  for j in range(i,len(names)):
   pairs[tuple(ch[i][k]+ch[j][k] for k in range(9))].append((i,j))
 neutral=[]
 for k,v in enumerate(ch):
  for i,j in pairs[tuple(-x for x in v)]:
   if j<=k: neutral.append(tuple(names[t] for t in (i,j,k)))
 survivors=[m for m in neutral if P.selection(m,fields)]
 hist=Counter(); fail=[]; reps=Counter()
 for mono in survivors:
  dims=[tuple(map(int,fields[n]['dim'].split(','))) for n in mono]
  reps[tuple(sorted(dims))]+=1
  s3,s2,s4,h2=(tuple(d[k] for d in dims) for k in range(4))
  ok=(su3_ok(s3),su2_ok(s2),su4_ok(s4),su2_ok(h2))
  hist[str(ok)]+=1
  if not all(ok): fail.append(dict(fields=mono,reps=dims,su3_su2_su4_su2=ok))
 print('REP TOP',reps.most_common(14),flush=True)
 print('NONABELIAN',len(survivors),len(fail),dict(hist),'EXAMPLES',fail[:5],flush=True)
 # SU4 unknown higher-dimensional rep? Distinguish if any values beyond +-4/6
 present=sorted({abs(int(f['dim'].split(',')[2])) for f in fields.values()})
 assert all(x in (1,4,6) for x in present),present
 out=dict(status='PASS',initial_U1_R_nonR_necessary_candidates=len(survivors),
  necessary_nonabelian_irrep_tensor_mask=hist,failed_group_theory_filters=fail,
  surviving_full_nonabelian_and_R_count=len(survivors)-len(fail),
  irrep_absolute_SU4_dims=present,
  cubic_channel_coverage='SU3 (1,3,3bar), SU2 doublet parity, SU4 (1,4,4bar,6 self-dual). Not a proof of actual gamma/space group/worldsheet correlator.',
  parallel_branch_boundary='This is the frozen Z6-II 176-field benchmark, not the new parallel 33-model Z6-I Pass11810-11815 up-Yukawa texture. Do not transfer selection numbers between orbifolds.',
  scope='Only necessary gauge-representation existence; nonzero contraction might vanish for repeated identical commuting chiral fields, and all worldsheet amplitude data remain absent.')
 (ROOT/'data/w33_20261009_round19_heterotic_nonabelian_cubic.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
