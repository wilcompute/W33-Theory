#!/usr/bin/env python3
"""Exact q=9 cubic moments WITHOUT enumerating 3,586,680 orbit supports.

Average a fixed seed over geometrically classified point triples; group
transitivity makes this equal the full orbit average for any representative
triple. Uses GF(9), distinguishes quadratic-character signs at q=1 mod 4.
"""
import sys,json,math,time
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from even_line_sets_gf import field
from symmetric_fast import fast_build
def main():
 t0=time.time();q=9;F,add0,mul0=field(q)
 add=np.array(add0,dtype=np.int16);mul=np.array(mul0,dtype=np.int16)
 inv={a:next(b for b in F if mul[a,b]==1) for a in F if a}
 neg={a:next(b for b in F if add[a,b]==0) for a in F}
 square={int(mul[x,x]) for x in range(1,q)}
 chi=np.array([0]+[1 if a in square else -1 for a in range(1,q)])
 assert len(square)==4 and chi[neg[1]]==1
 pts,lines=fast_build(q);v=len(pts);assert v==820 and len(lines)==820
 src=json.loads((ROOT/'analysis/search_drivers_12466/classify_q9.json').read_text())
 S=list(src['feasible'][0]['sample']);assert len(S)==48
 cover=np.zeros(v,dtype=np.int16)
 for j in S:cover[list(lines[j])]+=1
 assert sorted(set(cover))==[0,2] and int(sum(cover==2))==240
 x=np.where(cover==2,29,-12).astype(np.int64);assert x.sum()==0
 pid={p:i for i,p in enumerate(pts)}
 p=np.array(pts,dtype=np.int16)
 # omega = u0*v2+u1*v3-u2*v0-u3*v1 over GF9.
 o=add[mul[p[:,0,None],p[None,:,2]],mul[p[:,1,None],p[None,:,3]]]
 o=add[o,np.array([neg[z] for z in add[mul[p[:,2,None],p[None,:,0]],mul[p[:,3,None],p[None,:,1]]].ravel()]).reshape(v,v)]
 A=(o==0);np.fill_diagonal(A,False)
 assert np.all(A.sum(axis=1)==q*(q+1))
 counts=defaultdict(int);moments=defaultdict(int)
 for a in range(v):
  for b in range(a+1,v):
   c=np.arange(b+1,v,dtype=np.int32)
   if not len(c):continue
   edges=A[a,b].astype(int)+A[a,c].astype(int)+A[b,c].astype(int)
   prod=x[a]*x[b]*x[c]
   for n,name in ((3,'isotropic_line'),(2,'two_edges'),(1,'one_edge')):
    mask=(edges==n)
    if np.any(mask):
     counts[name]+=int(mask.sum())
     moments[name]+=int(prod[mask].sum())
   zero=(edges==0)
   if not np.any(zero):continue
   cc=c[zero];pp=prod[zero]
   quad=chi[mul[mul[o[a,b],o[b,cc]],o[cc,a]]]
   assert np.all(quad!=0)
   # Projective line span of distinct nonorthogonal a,b.
   span={b}
   for t in F:
    u=tuple(int(add[p[a,k],mul[t,p[b,k]]]) for k in range(4))
    z=next(y for y in u if y);inver=inv[z]
    uu=tuple(int(mul[inver,y]) for y in u)
    span.add(pid[uu])
   dependent=np.isin(cc,list(span))
   for dep,part in ((True,'nonisotropic_line'),(False,'independent')):
    for sign,lab in ((1,'plus'),(-1,'minus')):
     mask=(dependent==dep)&(quad==sign)
     name=part+'_'+lab
     counts[name]+=int(mask.sum())
     moments[name]+=int(pp[mask].sum())
  if (a+1)%100==0:print('Q9_CUBIC_PROGRESS',a+1,'of',v,'elapsed',round(time.time()-t0,1),flush=True)
 assert sum(counts.values())==math.comb(v,3),(sum(counts.values()),math.comb(v,3))
 # Gauge invariant cubic: average over point-orbit classes = class-sum for ONE seed / class size.
 table={k:{'triple_count':counts[k], 'sum_for_seed':moments[k],
   'orbit_average':str(Fraction(moments[k],counts[k])),'float':float(Fraction(moments[k],counts[k]))}
   for k in sorted(counts)}
 # Compute exact same-index moment and trace-free checksum.
 diag=Fraction(int(sum(x**3)),v)
 cov_diag=Fraction(int(sum(x**2)),v)
 assert diag.denominator==1 and cov_diag.denominator==1
 # E[(sum x)^3]=0, diagonal + 3 two-equal + 6 distinct.
 # x^2 =17x+348 on support (29²-(-12)²)/(29+12)=17,
 # and mean pair xixj = - mean diag /(v-1).
 pair_cov_avg=-cov_diag/Fraction(v-1)
 sum_i_ne_j= -v*diag/3 # note: E[x_i² x_j] sum_(i!=j) = - sum_i E[x_i³].
 target=v*diag/3
 check=sum(Fraction(moments[k]) for k in moments)
 assert check==target,(check,target)
 assert all(counts[k]>0 for k in counts)
 # Projective transitivity should be independently established; class sums alone
 # are NOT enough if an indexed orbit class further splits.
 out={'status':'PASS_EXACT_SEED_THIRD_MOMENTS_WITH_GROUP_ORBIT_CONDITIONAL',
 'q':9,'points':v,'hyperoval_lines':48,'twice_covered_points':240,
 'field_square_elements':sorted(square),'minus_one_is_square':True,
 'three_point_types':table,'three_point_type_count':len(table),
 'all_distinct_triplets':math.comb(v,3),'global_cubic_checksum':str(check),
 'single_point_cubic_moment':str(diag),'single_point_variance':str(cov_diag),
 'projective_transitivity_conditional':True,
 'line_unique_coefficient':len({table['isotropic_line']['orbit_average']} & set(vv['orbit_average'] for k,vv in table.items() if k!='isotropic_line'))==0,
 'elapsed_seconds':round(time.time()-t0,2),
 'scope':'Every class sum from a single known seed is EXACT. Interpreting as a single full-orbit tensor coefficient requires independently verifying G-transitivity on each of the seven classified triple types; the q9 support orbit size is from parallel Pass12525.'}
 outpath=ROOT/'data/w33_20261103_q9_seed_cubic_orbit_types.json'
 outpath.write_text(json.dumps(out,indent=2)+'\n')
 print('Q9_CUBIC_FINAL',json.dumps(out)[:6200],flush=True)
 return out
if __name__=='__main__':main()
