#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass569_z9_coupled_affine_radial_quadratic import projective_params,build_residues,row_view
from w33_pass573_hjelmslev_c3_600cell_apex import induced_actions,projective_action_indices,canonical_rows

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass578_residual_collision_symmetry.json'

POW13=3**np.arange(13,dtype=np.int64)
E=np.array([[1,t,t*t] for t in range(3)],dtype=np.int64)%3

def invmod(A,p=3):
 A=np.concatenate((np.array(A,dtype=np.int64)%p,np.eye(len(A),dtype=np.int64)),axis=1);n=len(A)
 for c in range(n):
  i=next(i for i in range(c,n) if A[i,c]%p);A[[c,i]]=A[[i,c]]
  A[c]=A[c]*pow(int(A[c,c]),-1,p)%p
  for j in range(n):
   if j!=c and A[j,c]:A[j]=(A[j]-A[j,c]*A[c])%p
 return A[:,n:]
EI=invmod(E)

def to_values(P):
 return np.stack((P[:,:4],P[:,4:8],P[:,9:13]),axis=2)@E.T%3

def from_values(V,d):
 C=V@EI.T%3;out=np.zeros((len(V),13),dtype=np.int8)
 out[:,:4]=C[:,:,0];out[:,4:8]=C[:,:,1];out[:,8]=d;out[:,9:13]=C[:,:,2]
 return out

def indexer(params):
 codes=params.astype(np.int64)@POW13;order=np.argsort(codes);return order,codes[order]

def map_indices(params,order,sorted_codes,T):
 Y=canonical_rows((params.astype(np.int64)@T.T)%3)
 return order[np.searchsorted(sorted_codes,Y.astype(np.int64)@POW13)]

def c3_orbits(params,gen):
 order,sc=indexer(params);idx=map_indices(params,order,sc,gen)
 vis=np.zeros(len(params),bool);oid=np.empty(len(params),np.int32);orbs=[]
 for i in range(len(params)):
  if vis[i]:continue
  O=[];j=i
  while not vis[j]:vis[j]=True;O.append(j);j=int(idx[j])
  k=len(orbs)
  for x in O:oid[x]=k
  orbs.append(tuple(O))
 return idx,oid,orbs

def spectral_census(res,oid,orbs):
 _,inv,counts=np.unique(res,return_inverse=True,return_counts=True)
 sidx=np.argsort(inv,kind='stable');starts=np.r_[0,np.cumsum(counts[:-1])]
 census=Counter();dominant_pairs=0;fixed_triples=0
 for gid,n in enumerate(counts):
  ids=sidx[starts[gid]:starts[gid]+n];os=set(oid[ids].tolist());fixed=sum(len(orbs[o])==1 for o in os)
  census[(int(n),len(os),fixed)]+=1
  if n==6 and len(os)==2 and fixed==0:dominant_pairs+=1
  if n==3 and len(os)==3 and fixed==3:fixed_triples+=1
 return counts,census,dominant_pairs,fixed_triples

def wreath_search(params,res,order,sc):
 # Every function F3 -> F3 is quadratic, so natural coordinate changes are S3 wr S4 on
 # the four fibre-value triples, with the common deep anchor fixed.
 rng=np.random.default_rng(578);sample=np.unique(np.r_[np.arange(40),rng.integers(0,len(params),size=384)])
 Ps=params[sample];Vs=to_values(Ps);ds=Ps[:,8];target=res[sample]
 p3=list(itertools.permutations(range(3)));keepers=[]
 for pf in itertools.permutations(range(4)):
  V0=Vs[:,pf,:]
  for local in itertools.product(p3,repeat=4):
   W=np.empty_like(V0)
   for i,p in enumerate(local):W[:,i,:]=V0[:,i,p]
   Y=canonical_rows(from_values(W,ds));idx=order[np.searchsorted(sc,Y.astype(np.int64)@POW13)]
   if np.array_equal(res[idx],target):keepers.append((pf,local))
 full=[]
 for pf,local in keepers:
  ok=True;idx_parts=[]
  for lo in range(0,len(params),50000):
   P=params[lo:lo+50000];V=to_values(P);V0=V[:,pf,:];W=np.empty_like(V0)
   for i,p in enumerate(local):W[:,i,:]=V0[:,i,p]
   Y=canonical_rows(from_values(W,P[:,8]));idx=order[np.searchsorted(sc,Y.astype(np.int64)@POW13)]
   if not np.array_equal(res[idx],res[lo:lo+len(P)]):ok=False;break
   idx_parts.append(idx)
  if ok:full.append((pf,local,np.concatenate(idx_parts)))
 return {'tested':24*6**4,'sample_survivors':len(keepers),'global_projective_maps':len(full),
         'global_maps':[{'fibre_permutation':x[0],'local_level_permutations':x[1]} for x in full]}

def fixed_s3(params,res,c3idx):
 fixed=np.where(c3idx==np.arange(len(params)))[0];P=params[fixed];R=res[fixed]
 coords=(0,1,2,3,4,8,9);Y=P[:,coords];powers=3**np.arange(7,dtype=np.int64)
 codes=Y.astype(np.int64)@powers;order=np.argsort(codes);sc=codes[order]
 def canon(Z):
  nz=Z!=0;first=np.argmax(nz,axis=1);has=nz.any(axis=1);flip=has&(Z[np.arange(len(Z)),first]==2)
  W=Z.copy();W[flip]=(-W[flip])%3;return W
 cert=json.loads((ROOT/'data'/'w33_pass578_fixed_locus_monomial_search.json').read_text())
 lifts=[]
 for rec in cert['linear_lifts']:
  perm=tuple(rec['permutation']);bits=int(rec['sign_bits']);s=np.array([2 if bits>>j&1 else 1 for j in range(7)],dtype=np.int8)
  Z=canon(Y[:,perm]*s%3);idx=order[np.searchsorted(sc,Z.astype(np.int64)@powers)]
  if np.array_equal(R[idx],R):lifts.append((perm,bits,idx))
 maps=[];seen=set()
 for perm,bits,idx in lifts:
  key=idx.tobytes()
  if key not in seen:seen.add(key);maps.append(idx)
 vis=np.zeros(len(Y),bool);oid=np.empty(len(Y),np.int32);orbs=[]
 for i in range(len(Y)):
  if vis[i]:continue
  O={int(m[i]) for m in maps};k=len(orbs)
  for x in O:vis[x]=True;oid[x]=k
  orbs.append(tuple(sorted(O)))
 _,inv,counts=np.unique(R,return_inverse=True,return_counts=True)
 census=Counter();single=Counter();excess=0;triple_orbits=0;triple_fixed=0
 for gid,n in enumerate(counts):
  ids=np.where(inv==gid)[0];os=set(oid[ids]);sizes=tuple(sorted(len(orbs[o]) for o in os))
  census[(int(n),len(os),sizes)]+=1;excess+=len(os)-1
  if len(os)==1:single[int(n)]+=1
  if n==3 and sizes==(3,):triple_orbits+=1
  if n==3 and sizes==(1,1,1):triple_fixed+=1
 return {'fixed_projective_points':len(Y),'fixed_spectra':len(counts),'monomial_group_tested':cert['tested'],'linear_lifts':len(lifts),'projective_group_order':len(maps),'identification':'S3 acting on (c1,c2,c3), with the sign twist on odd permutations','orbit_histogram':dict(sorted(Counter(map(len,orbs)).items())),'projective_orbits':len(orbs),'residual_excess_after_S3':excess,'spectral_census':{str(k):v for k,v in sorted(census.items())},'single_orbit_fibres':dict(sorted(single.items())),'size3_S3_orbits':triple_orbits,'size3_three_fixed_points':triple_fixed}

def payload():
 params=projective_params();raw=build_residues(params);res=row_view(raw)
 _,acts=induced_actions();gen=next(T for g,T in acts if g==(1,0,3,1)).astype(np.int8)
 c3idx,oid,orbs=c3_orbits(params,gen);counts,census,paired,fixedtrip=spectral_census(res,oid,orbs)
 fix=fixed_s3(params,res,c3idx);order,sc=indexer(params);wreath=wreath_search(params,res,order,sc)
 combined_orbits=len(orbs)-fix['fixed_projective_points']+fix['projective_orbits']
 combined_excess=combined_orbits-len(counts)
 checks={
  'projective_words797162':len(params)==797162,
  'spectral_image221451':len(counts)==221451,
  'C3_orbits266450':len(orbs)==266450,
  'residual_excess44999':len(orbs)-len(counts)==44999,
  'dominant_two_orbit_fibres43873':paired==43873,
  'exceptional_fixed_triples23':fixedtrip==23,
  'natural_wreath_group_exhausted':wreath['tested']==31104,
  'natural_wreath_global_symmetry_is_C3':wreath['global_projective_maps']==3,
  'fixed_monomial_group_exhausted':fix['monomial_group_tested']==645120,
  'fixed_locus_symmetry_is_S3':fix['projective_group_order']==6,
  'fixed_locus_points1094':fix['fixed_projective_points']==1094,
  'fixed_locus_spectra147':fix['fixed_spectra']==147,
  'twenty_two_exceptional_triples_are_S3_orbits':fix['size3_S3_orbits']==22,
  'one_exceptional_triple_remains_fixed':fix['size3_three_fixed_points']==1,
  'combined_residual_excess44191':combined_excess==44191,
 }
 return {
  'schema':'w33.pass578.residual_collision_symmetry.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'C3_quotient':{'projective_words':len(params),'C3_orbits':len(orbs),'spectral_image':len(counts),'residual_collision_excess':len(orbs)-len(counts),'dominant_size6_two_C3_orbit_fibres':paired,'fixed_size3_fibres':fixedtrip,'fibre_decomposition':{str(k):v for k,v in sorted(census.items())}},
  'natural_global_search':wreath,
  'fixed_locus_S3':fix,
  'combined_partial_quotient':{'orbit_count':combined_orbits,'spectral_image':len(counts),'residual_collision_excess':combined_excess,'excess_removed_by_fixed_S3':44999-combined_excess},
  'conclusion':'The hidden shear C3 is the complete global symmetry inside the natural S3 wr S4 fibre-value relabelling group. On its 1,094-point fixed locus, the spectrum acquires an exact projective S3 symmetry; this explains 22 of the 23 exceptional fixed triples and removes 808 residual orbit excesses. No global involution extending C3 to S3, C3^2, or a Heisenberg group exists inside the exhausted natural relabelling group.',
  'checks':checks,
  'boundary':'The no-extension statement is exact for the natural fibre-value wreath group S3 wr S4 and the full monomial group on the seven-dimensional C3-fixed locus. It is not a no-go theorem for arbitrary nonlinear transformations of F3^13.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 578 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'residual':p['combined_partial_quotient']['residual_collision_excess']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
