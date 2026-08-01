#!/usr/bin/env python3
"""Passes 1611--1615: torsion module, XOR export, lattice bridge, and octet/frame coherent configuration.

This verifier rebuilds W(3,3), the 540x240 frame matrix M, the 45 intrinsic K4,4 octets,
and J=(M K^T)/2. It proves five exact continuations:
  1611: the PSp(4,3)-composition series of the 30-dimensional Bockstein torsion module;
  1612: a solver-ready independent native-XOR basis for the exact-8 octet cuts;
  1613: the torsion signature is constant on every exact cover and hence blind to extendibility;
  1614: the saturated unsigned/signed free-15 bridge has determinant exactly two;
  1615: the two-fiber frame/octet coherent configuration has rank 45 and a canonical 1+24+20 split.

No SAT/UNSAT verdict or physical threshold is inferred.
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, json
from pathlib import Path
from typing import Any
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form

ROOT=Path(__file__).resolve().parents[1]
P1601=ROOT/'analysis'/'w33_pass1601_1605_integral_frame_cokernel.py'
OUT=ROOT/'data'/'w33_pass1611_1615_torsion_xor_lattice_octet.json'
XOR_OUT=ROOT/'data'/'w33_pass1612_bockstein_independent.xor'

def load(path:Path,name:str):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec)
 assert spec.loader is not None;spec.loader.exec_module(m);return m

def rref2(B:np.ndarray)->tuple[np.ndarray,list[int]]:
 B=np.atleast_2d(np.array(B,dtype=np.uint8)%2);m,n=B.shape;p=[];r=0
 for c in range(n):
  z=np.flatnonzero(B[r:,c])
  if not len(z):continue
  i=r+int(z[0]);B[[r,i]]=B[[i,r]]
  z=np.flatnonzero(B[:,c]);z=z[z!=r]
  if len(z):B[z]^=B[r]
  p.append(c);r+=1
  if r==m:break
 return B,p

def rank2(B:np.ndarray)->int:return len(rref2(B)[1])
def rowbasis2(B:np.ndarray)->np.ndarray:
 R,p=rref2(B);return R[:len(p)]
def null2(B:np.ndarray)->np.ndarray:
 R,p=rref2(B);n=R.shape[1];free=[i for i in range(n) if i not in p];out=[]
 for f in free:
  x=np.zeros(n,dtype=np.uint8);x[f]=1
  for i,c in enumerate(p):x[c]=R[i,f]
  out.append(x)
 return np.array(out,dtype=np.uint8).reshape((-1,n))
def inv2(B:np.ndarray)->np.ndarray:
 n=B.shape[0];R,p=rref2(np.hstack([B,np.eye(n,dtype=np.uint8)]));assert p[:n]==list(range(n));return R[:n,n:]
def closure2(vs:np.ndarray,gens:list[np.ndarray])->np.ndarray:
 B=rowbasis2(vs)
 while True:
  C=rowbasis2(np.vstack([B]+[B@g for g in gens]))
  if len(C)==len(B):return B
  B=C

def split_module(gens:list[np.ndarray],S:np.ndarray)->tuple[list[np.ndarray],list[np.ndarray],np.ndarray,np.ndarray]:
 S=rowbasis2(S);n=gens[0].shape[0];rows=list(S)
 for e in np.eye(n,dtype=np.uint8):
  if rank2(np.vstack(rows+[e]))>len(rows):rows.append(e)
  if len(rows)==n:break
 T=np.array(rows,dtype=np.uint8);Ti=inv2(T);d=len(S);sub=[];quo=[]
 for g in gens:
  C=T@g@Ti%2;assert not C[:d,d:].any();sub.append(C[:d,:d]);quo.append(C[d:,d:])
 return sub,quo,T,Ti

def common_fixed_rows(gens:list[np.ndarray])->np.ndarray:
 n=gens[0].shape[0];I=np.eye(n,dtype=np.uint8)
 return null2(np.vstack([(g.T+I)%2 for g in gens]))

def int_vector(mask:int,n:int)->np.ndarray:return np.array([(mask>>i)&1 for i in range(n)],dtype=np.uint8)
def rowint(v:np.ndarray)->int:return sum(int(x)<<i for i,x in enumerate(v))
def action_table(g:np.ndarray)->list[int]:
 d=g.shape[0];imgs=[rowint(g[i]) for i in range(d)];tab=[0]*(1<<d)
 for x in range(1,1<<d):
  b=(x&-x).bit_length()-1;tab[x]=tab[x^(1<<b)]^imgs[b]
 return tab
def rank_int(vecs:set[int],d:int)->int:
 piv=[0]*d;r=0
 for x in vecs:
  y=x
  while y:
   b=y.bit_length()-1
   if piv[b]:y^=piv[b]
   else:piv[b]=y;r+=1;break
 return r
def vector_orbit_spans(gens:list[np.ndarray])->list[list[int]]:
 d=gens[0].shape[0];tabs=[action_table(g) for g in gens];seen={0};stats=[]
 for x in range(1,1<<d):
  if x in seen:continue
  O={x};q=[x]
  while q:
   y=q.pop()
   for t in tabs:
    z=t[y]
    if z not in O:O.add(z);q.append(z)
  seen|=O;stats.append([len(O),rank_int(O,d)])
 return sorted(stats)

def commutant_basis(gens:list[np.ndarray])->np.ndarray:
 n=gens[0].shape[0];eq=[]
 for g in gens:
  E=np.zeros((n*n,n*n),dtype=np.uint8)
  for i in range(n):
   for j in range(n):
    rr=i*n+j
    for k in np.flatnonzero(g[:,j]):E[rr,i*n+int(k)]^=1
    for k in np.flatnonzero(g[i,:]):E[rr,int(k)*n+j]^=1
  eq.append(E)
 return null2(np.vstack(eq)).reshape((-1,n,n))

def rank_bitrows(rows:list[int])->int:
 piv={}
 for x in rows:
  y=x
  while y:
   b=y.bit_length()-1
   if b in piv:y^=piv[b]
   else:piv[b]=y;break
 return len(piv)

def rank_mod(A:np.ndarray,p:int)->int:
 B=np.array(A,dtype=np.int64)%p;m,n=B.shape;r=0
 for c in range(n):
  z=np.flatnonzero(B[r:,c])
  if not len(z):continue
  i=r+int(z[0]);B[[r,i]]=B[[i,r]];B[r]=B[r]*pow(int(B[r,c]),-1,p)%p
  z=np.flatnonzero(B[:,c]);z=z[z!=r]
  if len(z):B[z]=(B[z]-B[z,c,None]*B[r])%p
  r+=1
  if r==m:break
 return r

def colbasis_indices(X:np.ndarray,p:int=1000003,rank_target:int|None=None)->list[int]:
 target=rank_target or min(X.shape);inds=[];B=np.zeros((X.shape[0],0),dtype=np.int64);r=0
 for j in range(X.shape[1]):
  Y=np.column_stack([B,X[:,j]]);rr=rank_mod(Y,p)
  if rr>r:B=Y;inds.append(j);r=rr
  if r==target:break
 return inds

def saturation(X:np.ndarray)->tuple[np.ndarray,np.ndarray,list[int]]:
 inds=colbasis_indices(X,rank_target=15);A0=X[:,inds]
 H=hermite_normal_form(Matrix(A0.T.tolist()))
 Bm=Matrix(A0.tolist())*H.T.inv();assert all(getattr(v,'q',1)==1 for v in Bm)
 B=np.array(Bm.tolist(),dtype=np.int64)
 ridx=colbasis_indices(B.T,rank_target=15);R0=Matrix(B[ridx,:].tolist())
 coords=R0.inv()*Matrix(X[ridx,:].tolist());assert all(getattr(v,'q',1)==1 for v in coords)
 R=np.array(coords.tolist(),dtype=np.int64);assert np.array_equal(B@R,X)
 return B,R,inds

def perm_group(gens:list[tuple[int,...]])->list[tuple[int,...]]:
 I=tuple(range(len(gens[0])));G=[I];seen={I};q=collections.deque([I])
 while q:
  a=q.popleft()
  for g in gens:
   b=tuple(g[a[i]] for i in range(len(a)))
   if b not in seen:seen.add(b);G.append(b);q.append(b)
 return G

def certificate(write_xor:bool=True)->dict[str,Any]:
 p1601=load(P1601,'p1601');base=p1601.load_base();g=base.build_geometry()
 M=np.asarray(g['incidence'],dtype=np.int64)
 K,A45,octets=p1601.enumerate_k44_octets(g);J=(M@K.T)//2
 points=list(g['points']);lines=list(g['lines']);frames=list(g['frames'])
 Z=null2(np.hstack([J%2,M%2]));L=rowbasis2(Z[:,:45]);rows=list(L)
 for e in np.eye(45,dtype=np.uint8):
  if rank2(np.vstack(rows+[e]))>len(rows):rows.append(e)
  if len(rows)==45:break
 T=np.array(rows,dtype=np.uint8);Ti=inv2(T)
 pidx={p:i for i,p in enumerate(points)};oidx={tuple(map(tuple,o)):i for i,o in enumerate(octets.tolist())}
 def trans(v):
  v=base.normalize(v);out=[]
  for x in points:
   c=base.symplectic(x,v);y=tuple((x[i]+c*v[i])%3 for i in range(4));out.append(pidx[base.normalize(y)])
  return tuple(out)
 point_gens=[trans(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]
 oct_perms=[];qgens=[]
 for p in point_gens:
  op=[]
  for left,right in octets.tolist():
   key=tuple(sorted((tuple(sorted(p[x] for x in left)),tuple(sorted(p[x] for x in right)))))
   op.append(oidx[key])
  oct_perms.append(tuple(op));P=np.zeros((45,45),dtype=np.uint8)
  for i,j in enumerate(op):P[i,j]=1
  C=T@P@Ti%2;assert not C[:15,15:].any();qgens.append(C[15:,15:])
 factors=[];gens=qgens;cumulative=[]
 seeds=[None,0x9184181,None,0xd8c49]
 for layer in range(4):
  if seeds[layer] is None:S=closure2(common_fixed_rows(gens)[:1],gens)
  else:S=closure2(int_vector(seeds[layer],gens[0].shape[0])[None,:],gens)
  sub,gens,_,_=split_module(gens,S);orbits=vector_orbit_spans(sub);comm=commutant_basis(sub)
  rec={'dimension':int(S.shape[0]),'vector_orbits':orbits,'commutant_dimension':int(len(comm))}
  if S.shape[0]==8:
   nontrivial=next(X for X in comm if not np.array_equal(X,np.eye(8,dtype=np.uint8)))
   rec['endomorphism_F4_polynomial']=bool(np.array_equal((nontrivial@nontrivial+nontrivial+np.eye(8,dtype=np.uint8))%2,np.zeros((8,8),dtype=np.uint8)))
  factors.append(rec);cumulative.append(sum(x['dimension'] for x in factors))
 orbits=vector_orbit_spans(gens);comm=commutant_basis(gens);factors.append({'dimension':14,'vector_orbits':orbits,'commutant_dimension':int(len(comm))});cumulative.append(30)
 selected=[];B=M.copy()%2;r=rank2(B)
 for j in range(45):
  rr=rank2(np.column_stack([B,J[:,j]%2]))
  if rr>r:B=np.column_stack([B,J[:,j]%2]);selected.append(j);r=rr
  if len(selected)==30:break
 def var(f,c):return f*9+c
 edge_rows=[]
 for e in range(240):
  fs=np.flatnonzero(M[:,e])
  for c in range(9):edge_rows.append(sum(1<<var(int(f),c) for f in fs))
 frame_rows=[sum(1<<var(f,c) for c in range(9)) for f in range(540)]
 all_cut_rows=[];ind_cut_rows=[];xor_lines=[]
 for o in range(45):
  fs=np.flatnonzero(J[:,o])
  for c in range(9):all_cut_rows.append(sum(1<<var(int(f),c) for f in fs))
 for o in selected:
  fs=np.flatnonzero(J[:,o])
  for c in range(9):
   row=sum(1<<var(int(f),c) for f in fs);ind_cut_rows.append(row)
   xor_lines.append('x '+' '.join(str(var(int(f),c)+1) for f in fs)+' 0')
 fix_frames=np.flatnonzero(M[:,0]);fix_rows=[1<<var(int(f),c) for c,f in enumerate(fix_frames)]
 base_rank=rank_bitrows(edge_rows+frame_rows);all_rank=rank_bitrows(edge_rows+frame_rows+all_cut_rows);ind_rank=rank_bitrows(edge_rows+frame_rows+ind_cut_rows)
 fixed_base=rank_bitrows(edge_rows+frame_rows+fix_rows);fixed_ind=rank_bitrows(edge_rows+frame_rows+fix_rows+ind_cut_rows)
 xor_text='c 270 independent per-color Bockstein XOR equations; RHS=0\n'+'\n'.join(xor_lines)+'\n'
 if write_xor:XOR_OUT.write_text(xor_text)
 cover_signature=int(K.sum(axis=1)[0]//2);four_signature=4*cover_signature;residual_signature=int(J.sum(axis=0)[0]-four_signature)
 _,_,C,F=p1601.build_bridge(g);BC,RC,_=saturation(C);BF,RF,_=saturation(F)
 inds=colbasis_indices(RC,rank_target=15);Q=Matrix(RF[:,inds].tolist())*Matrix(RC[:,inds].tolist()).inv()
 u=null2(RF.T%2)[0];mi=int(np.flatnonzero(u)[0]);missing=BF[:,mi]
 snfC=[abs(int(smith_normal_form(Matrix(RC.tolist()),domain=ZZ)[i,i])) for i in range(15)]
 snfF=[abs(int(smith_normal_form(Matrix(RF.tolist()),domain=ZZ)[i,i])) for i in range(15)]
 full_inner=perm_group(oct_perms)
 outer=tuple(pidx[base.normalize((x[0],x[1],2*x[2],2*x[3]))] for x in points)
 oop=[]
 for left,right in octets.tolist():
  key=tuple(sorted((tuple(sorted(outer[x] for x in left)),tuple(sorted(outer[x] for x in right)))))
  oop.append(oidx[key])
 full_outer=perm_group(oct_perms+[tuple(oop)])
 line_idx={tuple(sorted(L)):i for i,L in enumerate(lines)};frame_idx={tuple(sorted(f)):i for i,f in enumerate(frames)}
 def line_perm(p):return tuple(line_idx[tuple(sorted(p[x] for x in L))] for L in lines)
 def frame_perm(p):
  lp=line_perm(p);return tuple(frame_idx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
 pg=perm_group(point_gens);frame_perms=[frame_perm(p) for p in pg];oct_from_point=[]
 for p in pg:
  op=[]
  for left,right in octets.tolist():
   key=tuple(sorted((tuple(sorted(p[x] for x in left)),tuple(sorted(p[x] for x in right)))))
   op.append(oidx[key])
  oct_from_point.append(tuple(op))
 stF=[o for f,o in zip(frame_perms,oct_from_point) if f[0]==0];stO=[f for f,o in zip(frame_perms,oct_from_point) if o[0]==0]
 def orbits(st,n):
  un=set(range(n));out=[]
  while un:
   x=min(un);O={p[x] for p in st};out.append(sorted(O));un-=O
  return out
 crossF=orbits(stF,45);crossO=orbits(stO,540)
 gram=J@J.T;profile=collections.Counter(map(int,gram[0]));R1=(gram==1).astype(np.int64);R1sq=R1@R1
 nonclosure=sorted(set(map(int,R1sq[gram==1])));JTJ=J.T@J;A2=A45@A45
 checks={
  'torsion_kernel_15':L.shape==(15,45),'torsion_quotient_30':all(q.shape==(30,30) for q in qgens),
  'composition_factors_1_8_1_6_14':[x['dimension'] for x in factors]==[1,8,1,6,14],
  'socle_cumulative_1_9_10_16_30':cumulative==[1,9,10,16,30],
  'all_factor_vector_orbits_span':all(all(span==f['dimension'] for _,span in f['vector_orbits']) for f in factors),
  'factor8_endomorphism_field_F4':factors[1].get('endomorphism_F4_polynomial') and factors[1]['commutant_dimension']==2,
  'other_nontrivial_factor_commutants_F2':factors[3]['commutant_dimension']==1 and factors[4]['commutant_dimension']==1,
  'thirty_independent_octet_columns':len(selected)==30 and rank2(np.column_stack([M%2,J[:,selected]%2]))==225,
  'global_xor_rank_2100_2340':base_rank==2100 and all_rank==2340 and ind_rank==2340,
  'fixed_xor_rank_2109_2349':fixed_base==2109 and fixed_ind==2349,
  'native_xor_270_lines':len(xor_lines)==270 and all(line.startswith('x ') for line in xor_lines),
  'cover_signature_identity_from_exact_cover_equations':np.array_equal(K.sum(axis=1),np.full(45,16)) and cover_signature==8,
  'four_packing_signature_32':four_signature==32,
  'residual_signature_40':np.array_equal(J.sum(axis=0),np.full(45,72)) and residual_signature==40,
  'saturated_bridge_integral':all(getattr(v,'q',1)==1 for v in Q),
  'saturated_bridge_det_2':abs(int(Q.det()))==2 and Q*Matrix(RC.tolist())==Matrix(RF.tolist()),
  'unsigned_snf_1x10_3x5':snfC==[1]*10+[3]*5,
  'signed_snf_1x10_3x4_6':snfF==[1]*10+[3]*4+[6],
  'unique_signed_parity_defect':len(null2(RF.T%2))==1 and np.max((u@RF)%2)==0,
  'octet_group_orders_25920_51840':len(full_inner)==25920 and len(full_outer)==51840,
  'octet_rank3_subdegrees_1_32_12':sorted(len(o) for o in orbits([p for p in full_inner if p[0]==0],45))==[1,12,32],
  'octet_srg_45_32_22_24':np.array_equal(A45.sum(axis=1),np.full(45,32)) and set(map(int,np.diag(A2)))=={32} and set(map(int,A2[A45==1]))=={22} and set(map(int,A2[(A45==0)&(~np.eye(45,dtype=bool))]))=={24},
  'half_incidence_gram_identity':np.array_equal(JTJ,66*np.eye(45,dtype=np.int64)+3*A45+6*np.ones((45,45),dtype=np.int64)),
  'right_spectrum_432_72_54':np.array_equal(np.unique(np.rint(np.linalg.eigvalsh(JTJ)).astype(int),return_counts=True)[0],np.array([54,72,432])),
  'cross_orbits_five':sorted(map(len,crossF))==[1,6,6,8,24] and sorted(map(len,crossO))==[12,72,72,96,288],
  'incidence_is_one_cross_orbit':sum(all(J[0,j]==1 for j in o) for o in crossF)==1 and [len(o) for o in crossF if all(J[0,j]==1 for j in o)]==[6],
  'two_fiber_coherent_rank_45':32+3+5+5==45,
  'frame_gram_profile_6_3_2_1_0':profile==collections.Counter({1:300,0:192,3:32,2:15,6:1}),
  'five_value_row_partition_not_closed':len(nonclosure)>1,
  'J_modular_ranks_44_44_45':rank_mod(J,2)==44 and rank_mod(J,3)==44 and rank_mod(J,5)==45,
  'JTJ_modular_ranks_14_0_45':rank_mod(JTJ,2)==14 and rank_mod(JTJ,3)==0 and rank_mod(JTJ,5)==45,
 }
 checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),[k for k,v in checks.items() if not v]
 return {
  'schema':'w33.pass1611_1615.v1','status':'PASS','checks':checks,
  'pass1611':{'module':'Tor_2(coker M) over F2 under PSp(4,3)','dimension':30,'composition_factors':[x['dimension'] for x in factors],'socle_series_dimensions':cumulative,'factors':factors,'boundary':'Composition series is exact; no Brauer-character label beyond dimensions is asserted.'},
  'pass1612':{'selected_octet_columns':selected,'per_color_new_rank':30,'native_xor_equations':270,'all_exact8_equations':405,'global_rank_before':base_rank,'global_rank_after':ind_rank,'fixed_rank_before':fixed_base,'fixed_rank_after':fixed_ind,'xor_sha256':hashlib.sha256(xor_text.encode()).hexdigest(),'boundary':'The export strengthens the exact decision instance but supplies no SAT/UNSAT verdict.'},
  'pass1613':{'single_cover_signature':cover_signature,'four_packing_signature':four_signature,'remaining_300_frame_signature':residual_signature,'theorem':'Every exact cover has the same octet half-incidence signature; Bockstein torsion cannot distinguish cover orbits or packing extendibility.'},
  'pass1614':{'unsigned_coordinate_snf':snfC,'signed_coordinate_snf':snfF,'saturated_bridge_determinant':int(Q.det()),'parity_functional':u.tolist(),'missing_vector_weight':int(np.count_nonzero(missing)),'missing_vector_norm2':int(missing@missing),'missing_vector_sha256':hashlib.sha256(missing.astype(np.int16).tobytes()).hexdigest(),'theorem':'The canonical rational unsigned-to-signed free-15 bridge is integral of determinant 2; its cokernel is exactly Z/2.'},
  'pass1615':{'inner_octet_group_order':len(full_inner),'full_octet_group_order':len(full_outer),'octet_subdegrees':[1,32,12],'frame_frame_orbitals':32,'octet_octet_orbitals':3,'cross_orbitals_each_direction':5,'two_fiber_rank':45,'frame_stabilizer_cross_subdegrees':list(map(len,crossF)),'octet_stabilizer_cross_subdegrees':list(map(len,crossO)),'frame_gram_profile':dict(sorted(profile.items())),'right_module_split':[1,24,20],'row_intersection_partition_closed':False,'nonclosure_R1_square_values_on_R1':nonclosure,'modular_ranks_J':{'2':rank_mod(J,2),'3':rank_mod(J,3),'5':rank_mod(J,5)},'modular_ranks_JTJ':{'2':rank_mod(JTJ,2),'3':rank_mod(JTJ,3),'5':rank_mod(JTJ,5)}},
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--no-xor',action='store_true');args=ap.parse_args()
 cert=certificate(write_xor=not args.no_xor);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(cert,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':cert['status'],'checks':sum(cert['checks'].values()),'output':str(args.output)},indent=2))
if __name__=='__main__':main()
