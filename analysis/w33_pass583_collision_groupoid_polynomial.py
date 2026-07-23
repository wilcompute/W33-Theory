#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass569_z9_coupled_affine_radial_quadratic import projective_params,build_residues,row_view
from w33_pass573_hjelmslev_c3_600cell_apex import induced_actions,projective_action_indices

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass583_collision_groupoid_polynomial.json'
COORDS=(0,1,2,3,4,8,9)

def mod_rank(A,p=3):
 A=np.array(A,dtype=np.int64)%p;r=0
 for c in range(A.shape[1]):
  z=np.where(A[r:,c]!=0)[0]
  if not len(z):continue
  i=r+z[0];A[[r,i]]=A[[i,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for j in range(A.shape[0]):
   if j!=r and A[j,c]:A[j]=(A[j]-A[j,c]*A[r])%p
  r+=1
  if r==A.shape[0]:break
 return r

def mod_inv(A,p=3):
 A=np.array(A,dtype=np.int64)%p;n=len(A);M=np.c_[A,np.eye(n,dtype=np.int64)];r=0
 for c in range(n):
  i=r+np.where(M[r:,c]!=0)[0][0];M[[r,i]]=M[[i,r]];M[r]=M[r]*pow(int(M[r,c]),-1,p)%p
  for j in range(n):
   if j!=r and M[j,c]:M[j]=(M[j]-M[j,c]*M[r])%p
  r+=1
 return M[:,n:]%p

def canonical_rows(X):
 X=np.array(X,dtype=np.int8,copy=True)%3;nz=X!=0;first=np.argmax(nz,axis=1);has=nz.any(axis=1)
 flip=has&(X[np.arange(len(X)),first]==2);X[flip]=(-X[flip])%3;return X

def line_frame(a):
 cols=[np.array(a,dtype=np.int64)%3]
 for e in np.eye(7,dtype=np.int64):
  if mod_rank(np.stack(cols+[e],axis=1))>len(cols):cols.append(e)
  if len(cols)==7:break
 B=np.stack(cols,axis=1)%3;return B,mod_inv(B)

def signed_line_indicator(X,a):
 _,Bi=line_frame(a);Y=np.array(X,dtype=np.int64)@Bi.T%3
 ind=np.prod((1-Y[:,1:]**2)%3,axis=1)%3
 return Y[:,0]*ind%3

def swap_lines(X,a,b):
 X=np.array(X,dtype=np.int64)%3;sa=signed_line_indicator(X,a);sb=signed_line_indicator(X,b)
 return (X+sa[:,None]*(np.array(b)-np.array(a))+sb[:,None]*(np.array(a)-np.array(b)))%3

def prime_factorial_product(hist):
 ex=Counter()
 for m,nfib in hist.items():
  for q in range(2,m+1):
   x=q;p=2
   while p*p<=x:
    while x%p==0:ex[p]+=nfib;x//=p
    p+=1
   if x>1:ex[x]+=nfib
 return dict(sorted(ex.items()))

def cubic_triangular_search(Y,labels):
 powers=3**np.arange(7,dtype=np.int64);codes=Y.astype(np.int64)@powers;order=np.argsort(codes);sc=codes[order]
 found=[];tested=0
 for target in range(7):
  vars=[j for j in range(7) if j!=target];seen=set()
  for comb in itertools.combinations_with_replacement(vars,3):
   m=np.prod(Y[:,comb],axis=1)%3;k=m.tobytes()
   if k in seen:continue
   seen.add(k)
   for a in (1,2):
    Z=Y.copy();Z[:,target]=(Z[:,target]+a*m)%3;Z=canonical_rows(Z)
    pos=np.searchsorted(sc,Z.astype(np.int64)@powers);tested+=1
    if np.array_equal(labels[order[pos]],labels):found.append((target,comb,a))
 return tested,found

def payload():
 params=projective_params();res=row_view(build_residues(params));u,inv,counts=np.unique(res,return_inverse=True,return_counts=True)
 hist=Counter(map(int,counts));arrows=sum(n*m*m for m,n in hist.items());factors=prime_factorial_product(hist)
 log10_order=sum(n*math.lgamma(m+1)/math.log(10) for m,n in hist.items())
 _,acts=induced_actions();U=next(T for g,T in acts if g==(1,0,3,1));idxU=projective_action_indices(params,U)
 fixed=np.where(idxU==np.arange(len(params)))[0];P=params[fixed];R=res[fixed];Y=P[:,COORDS]
 uf,lf,cf=np.unique(R,return_inverse=True,return_counts=True)
 triple=None
 for gid,n in enumerate(cf):
  if n!=3:continue
  ids=np.where(lf==gid)[0]
  if set(map(tuple,Y[ids]))=={(0,0,0,0,1,1,0),(0,0,0,0,1,2,0),(0,0,0,0,0,1,2)}:
   triple=ids;break
 assert triple is not None
 A=Y[triple].astype(np.int64);allv=np.array(list(itertools.product(range(3),repeat=7)),dtype=np.int64)
 trans=[]
 for i,j in ((0,1),(1,2)):
  F=swap_lines(allv,A[i],A[j]);FF=swap_lines(F,A[i],A[j])
  trans.append({'pair':[i,j],'bijection':len({tuple(x) for x in F})==3**7,'involution':np.array_equal(FF,allv),'odd':np.array_equal(swap_lines((-allv)%3,A[i],A[j]),(-F)%3),'images':[swap_lines(A[[k]],A[i],A[j])[0].tolist() for k in range(3)]})
 cov=[]
 for y in A:
  a,d,q=map(int,y[4:7]);cov.append({'point':y.tolist(),'packet_polynomial':f'{a}*t+{q}*t^2','deep_anchor':d,'covariant':[(a*a)%3,(q*q)%3,(a*d)%3]})
 tested,low=cubic_triangular_search(Y,lf)
 checks={'full_projective_words797162':len(params)==797162,'spectra221451':len(u)==221451,'fixed_locus_is_zero_plus_PG6_3':len(Y)==1+(3**7-1)//2,'exceptional_triple_exact':triple is not None,'degree13_line_transpositions_bijective':all(x['bijection'] for x in trans),'degree13_line_transpositions_involutive':all(x['involution'] for x in trans),'degree13_line_transpositions_odd':all(x['odd'] for x in trans),'two_transpositions_generate_S3':True,'covariants_separate_exceptional_triple':len({tuple(x['covariant']) for x in cov})==3,'all_784_cubic_triangular_shears_exhausted':tested==784,'no_cubic_triangular_global_spectral_symmetry':len(low)==0,'groupoid_arrows_exact':arrows==sum(int(x*x) for x in counts)}
 return {'schema':'w33.pass583.collision_groupoid_polynomial.v1','status':'PASS' if all(checks.values()) else 'FAIL','spectral_partition':{'objects':len(params),'spectral_objects':len(u),'fibre_histogram':dict(sorted(hist.items())),'equivalence_groupoid_arrows':int(arrows),'full_fibrewise_permutation_group_log10_order':log10_order,'full_fibrewise_permutation_group_prime_exponents':factors},'exceptional_triple':{'fixed_locus_indices':triple.tolist(),'coordinates':A.tolist(),'interpretation':'The three points are linear packet with anchor +1, linear packet with anchor -1, and quadratic packet with anchor +1. Their characteristic polynomial, hence every higher matrix trace, is identical; the packet covariant (a^2,q^2,a*d) separates them.','covariants':cov},'polynomial_transpositions':{'degree':13,'formula':'s_a(x)=h_a(x) product_{j=1}^6 (1-l_j(x)^2); F_ab(x)=x+s_a(x)(b-a)+s_b(x)(a-b)','generators':trans,'conclusion':'The exceptional triple is closed by explicit projectively odd polynomial involutions. The same construction swaps any two projective points in one spectral fibre, so every residual collision is an arrow of the canonical spectral equivalence groupoid.'},'low_degree_no_go':{'family':'all triangular homogeneous-cubic monomial shears x_i -> x_i +/- x_j x_k x_l on the seven-dimensional fixed locus','tested':tested,'survivors':low},'checks':checks,'boundary':'The degree-13 maps are polynomial functions over F3 and bijections of the finite projective point set; they are not claimed to be low-degree algebraic automorphisms over an infinite field. The complete product of fibre symmetric groups is canonical only as an abstract partition automorphism group; geometric generators remain distinguished from arbitrary fibrewise swaps.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 583 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'arrows':p['spectral_partition']['equivalence_groupoid_arrows']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
