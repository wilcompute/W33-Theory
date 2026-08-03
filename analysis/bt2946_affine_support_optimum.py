#!/usr/bin/env python3
"""Pass 2946: prove the exact distance-four affine-support optimum is 15.

Run each heavy MILP in a separate process:
  --case local | n13 | n14_span_zero | n14_span_nonzero |
         n14_outside_span | double | witness | summary
"""
from __future__ import annotations
import argparse,itertools,json,time
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,vstack,hstack
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
def canon(a,b):
 w=tuple(a)+(b,);n=tuple((-x)%3 for x in w);return min(w,n)
def norm(a):
 i=next(i for i,x in enumerate(a) if x);s=pow(int(a[i]),-1,3);return tuple(s*x%3 for x in a)
def build(dim):
 seen=set();F=[]
 for a in itertools.product(range(3),repeat=dim):
  if not any(a):continue
  for b in range(3):
   c=canon(a,b)
   if c not in seen:seen.add(c);F.append((c[:-1],c[-1]))
 X=list(itertools.product(range(3),repeat=dim));pairs=list(itertools.combinations(range(len(X)),2))
 V=np.array([[int((sum(u*v for u,v in zip(a,x))+b)%3!=0) for a,b in F] for x in X],np.int8)
 S=np.array([[V[i,j]!=V[k,j] for j in range(len(F))] for i,k in pairs],np.int8)
 groups={}
 for j,(a,b) in enumerate(F):groups.setdefault(norm(a),[]).append(j)
 G=np.zeros((len(groups),len(F)),np.int8)
 for r,g in enumerate(groups.values()):G[r,g]=1
 return F,X,V,S,G,list(groups.values())
def solve(A,lb,ub,n,c=None,limit=300):
 t=time.time();r=milp(c=np.zeros(n) if c is None else c,integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(A,np.asarray(lb,float),np.asarray(ub,float)),options={'time_limit':limit,'mip_rel_gap':0,'presolve':True});return r,time.time()-t
def case_local():
 F,X,V,S,G,groups=build(3)
 A=vstack([csr_matrix(S),csr_matrix(np.ones((1,39))),csr_matrix(np.eye(1,39,0))]);r11,t11=solve(A,np.r_[np.full(351,4),11,1],np.r_[np.full(351,np.inf),11,1],39);assert r11.status==2
 rows=[hstack([csr_matrix(S),csr_matrix(np.zeros((351,13)))]),hstack([csr_matrix(np.ones((1,39))),csr_matrix(np.zeros((1,13)))]),hstack([csr_matrix(G),csr_matrix(-3*np.eye(13))]),hstack([csr_matrix(G),csr_matrix(-np.eye(13))])]
 lb=np.r_[np.full(351,4),12,np.zeros(13),np.full(13,-np.inf)];ub=np.r_[np.full(351,np.inf),12,np.full(13,np.inf),np.full(13,2)]
 row=np.zeros((1,52));row[0,0]=1;rows.append(csr_matrix(row));lb=np.r_[lb,1];ub=np.r_[ub,1];A=vstack(rows);c=np.r_[np.zeros(39),np.ones(13)]
 rmin,tmin=solve(A,lb,ub,52,c);rmax,tmax=solve(A,lb,ub,52,-c);assert rmin.success and rmax.success and round(rmin.fun)==4 and round(-rmax.fun)==4
 out={'status':'COMPLETE_EXACT_MILP','length11':'infeasible','length12':'feasible','complete_direction_triplets_min':4,'complete_direction_triplets_max':4,'runtime_seconds':{'length11':t11,'min':tmin,'max':tmax}}
 (DATA/'PART_BT2946_LOCAL_AG3_PROFILE_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
def global_case(name):
 F,X,V,S,G,groups=build(4);configs={'n13':(13,1,[0,3]),'n14_span_zero':(14,1,[0,3,6]),'n14_span_nonzero':(14,1,[0,3,7]),'n14_outside_span':(14,1,[0,3,12])};length,cap,fixes=configs[name]
 mats=[csr_matrix(S),csr_matrix(G),csr_matrix(np.ones((1,120)))];lb=np.r_[np.full(3240,4),np.zeros(40),length];ub=np.r_[np.full(3240,np.inf),np.full(40,cap),length]
 for f in fixes:mats.append(csr_matrix(np.eye(1,120,f)));lb=np.r_[lb,1];ub=np.r_[ub,1]
 r,dt=solve(vstack(mats),lb,ub,120);assert r.status==2 and not r.success
 out={'case':name,'status':'infeasible','fixed_features':fixes,'direction_cap':cap,'length':length,'runtime_seconds':dt,'solver_message':r.message};(DATA/f'PART_BT2946_{name.upper()}_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
def case_double():
 sols=[]
 for cs in itertools.product(range(3),repeat=3):
  for bs in itertools.product(range(3),repeat=3):
   if all(sorted((bs[i]+cs[i]*s)%3 for i in range(3))==[0,1,2] for s in range(3)):sols.append((cs,bs))
 assert sols and all(len(set(cs))==1 for cs,bs in sols)
 out={'status':'COMPLETE_EXACT_ENUMERATION','packet_solution_count':len(sols),'all_solution_slopes_constant':True,'proof':'On a flat a packet has offsets b_i+c_i s. Requiring all three F3 offsets for every s gives sum c_i^2=0 and sum c_i=0, hence c_1=c_2=c_3; this repeats one global direction three times, contradicting the cap two.','solutions':[{'c':list(c),'b':list(b)} for c,b in sols]};(DATA/'PART_BT2946_N14_DOUBLE_OBSTRUCTION_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
def case_witness():
 F,X,V,S,G,groups=build(4);dirs=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,1,1)];sel=[]
 for d in dirs:sel += [i for i,(a,b) in enumerate(F) if norm(a)==d]
 C=V[:,sel];hist=Counter(int(np.count_nonzero(C[i]!=C[j])) for i,j in itertools.combinations(range(81),2));assert len(set(map(tuple,C)))==81 and min(hist)==4
 out={'status':'COMPLETE_EXACT_WITNESS','length':15,'minimum_distance':4,'selected_feature_indices':sel,'selected_features':[{'a':list(F[i][0]),'b':F[i][1]} for i in sel],'pair_distance_histogram':{str(k):v for k,v in sorted(hist.items())},'construction':'binary full-three-offset image of the ternary [5,4,2]_3 single-parity-check code'};(DATA/'PART_BT2946_N15_WITNESS_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
def summarize():
 names=['LOCAL_AG3_PROFILE','N13','N14_SPAN_ZERO','N14_SPAN_NONZERO','N14_OUTSIDE_SPAN','N14_DOUBLE_OBSTRUCTION','N15_WITNESS'];d={n:json.loads((DATA/f'PART_BT2946_{n}_results.json').read_text()) for n in names}
 checks={'local_minimum12':d['LOCAL_AG3_PROFILE']['length11']=='infeasible','local12_four_triplets':d['LOCAL_AG3_PROFILE']['complete_direction_triplets_min']==d['LOCAL_AG3_PROFILE']['complete_direction_triplets_max']==4,'n13_infeasible':d['N13']['status']=='infeasible','n14_all_single_infeasible':all(d[n]['status']=='infeasible' for n in ['N14_SPAN_ZERO','N14_SPAN_NONZERO','N14_OUTSIDE_SPAN']),'n14_double_infeasible':d['N14_DOUBLE_OBSTRUCTION']['all_solution_slopes_constant'],'n15_distance4':d['N15_WITNESS']['minimum_distance']==4};assert all(checks.values())
 out={'schema':'w33.pass2946.affine_support_optimum.v1','status':'COMPLETE_EXACT','checks':checks,'check_count':len(checks),'minimum_length':15,'headline':'The exact affine-support distance-four optimum on the 81 frames is 15.','proof_summary':'Local AG(3,3) minimum 12 and four-triplet classification imply the direction cap. Length13 and all-single length14 are closed by orbit-reduced MILP. A doubled direction forces forbidden triple repetition. The [5,4,2]_3 full-offset image gives length15.'};(DATA/'PART_BT2946_AFFINE_SUPPORT_OPTIMUM_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['local','n13','n14_span_zero','n14_span_nonzero','n14_outside_span','double','witness','summary'],required=True);a=ap.parse_args();{'local':case_local,'n13':lambda:global_case('n13'),'n14_span_zero':lambda:global_case('n14_span_zero'),'n14_span_nonzero':lambda:global_case('n14_span_nonzero'),'n14_outside_span':lambda:global_case('n14_outside_span'),'double':case_double,'witness':case_witness,'summary':summarize}[a.case]()
if __name__=='__main__':main()
