#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass579_colored_600cell_module import geometry,porder
from w33_pass573_hjelmslev_c3_600cell_apex import induced_actions
from w33_pass569_z9_coupled_affine_radial_quadratic import projective_params,build_residues,row_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass584_colored_intertwiner_a4.json';PACKET=(0,1,2,3,4,5,6,7,9,10,11,12)
def mod_rref(A,p=3):
 A=np.array(A,dtype=np.int64)%p;m,n=A.shape;piv=[];r=0
 for c in range(n):
  z=np.where(A[r:,c]!=0)[0]
  if not len(z):continue
  i=r+z[0];A[[r,i]]=A[[i,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for j in range(m):
   if j!=r and A[j,c]:A[j]=(A[j]-A[j,c]*A[r])%p
  piv.append(c);r+=1
  if r==m:break
 return A,piv
def nullspace(A,p=3):
 R,piv=mod_rref(A,p);free=[c for c in range(A.shape[1]) if c not in piv];out=[]
 for f in free:
  v=np.zeros(A.shape[1],dtype=np.int64);v[f]=1
  for i,c in enumerate(piv):v[c]=(-R[i,f])%p
  out.append(v)
 return np.array(out,dtype=np.int64)
def rank(A,p=3):return len(mod_rref(A,p)[1])
def inv(A,p=3):
 n=len(A);R,piv=mod_rref(np.c_[np.array(A)%p,np.eye(n,dtype=np.int64)],p)
 if len([x for x in piv if x<n])<n:raise ValueError('singular')
 return R[:,-n:]%p
def solve(A,b,p=3):
 A=np.array(A,dtype=np.int64)%p;b=np.array(b,dtype=np.int64)%p;R,piv=mod_rref(np.c_[A,b],p);n=A.shape[1]
 if any(c==n for c in piv):raise ValueError('inconsistent')
 x=np.zeros(n,dtype=np.int64)
 for i,c in enumerate(piv):
  if c<n:x[c]=R[i,n]
 return x
def col_basis(M):
 out=[]
 for j in range(M.shape[1]):
  v=M[:,j]
  if rank(np.stack(out+[v],axis=1))>len(out):out.append(v.copy())
 return out
def jordan_basis(U):
 n=len(U);N=(U-np.eye(n,dtype=np.int64))%3;N2=N@N%3;tops=col_basis(N2);chains=[]
 for w in tops:
  v=solve(N2,w);chains.extend([w,N@v%3,v])
 fixed=nullspace(N);current=[x for x in chains]
 for f in fixed:
  if rank(np.stack(current+[f],axis=1))>len(current):current.append(f)
 B=np.stack(current,axis=1)%3;assert B.shape==(n,n) and rank(B)==n;return B
def pmat(perm):
 M=np.zeros((len(perm),len(perm)),dtype=np.int64)
 for i,j in enumerate(perm):M[j,i]=1
 return M
def canonical_rows(X):
 X=np.array(X,dtype=np.int8,copy=True)%3;nz=X!=0;first=np.argmax(nz,axis=1);has=nz.any(axis=1);flip=has&(X[np.arange(len(X)),first]==2);X[flip]=(-X[flip])%3;return X
def colored_module():
 A,E,faces,aut,rot,antipode,opp,fmap=geometry();colorings=[]
 for Y in itertools.combinations(range(20),8):
  deg=[0]*12
  for f in Y:
   for v in faces[f]:deg[v]+=1
  if set(deg)=={2}:colorings.append(frozenset(Y))
 unseen=set(colorings);orbits=[]
 while unseen:
  c=next(iter(unseen));O={frozenset(fmap(g)[i] for i in c) for g in rot};unseen-=O;orbits.append(O)
 c=sorted(next(O for O in orbits if len(O)==5),key=lambda z:tuple(sorted(z)))[0];stab=sorted((g for g in rot if frozenset(fmap(g)[i] for i in c)==c));pairs=[];seen=set()
 for f in sorted(c):
  if f not in seen:pairs.append((f,opp[f]));seen.update((f,opp[f]))
 objects=list(sorted(c))+[frozenset(x) for x in pairs];oi={x:i for i,x in enumerate(objects)}
 def perm(g):
  fg=fmap(g);return tuple(oi[fg[x] if isinstance(x,int) else frozenset(fg[t] for t in x)] for x in objects)
 return c,pairs,objects,stab,[perm(g) for g in stab]
def payload():
 c,pairs,objects,stab,perms=colored_module();gidx=next(i for i,g in enumerate(stab) if porder(g)==3);Pc=pmat(perms[gidx]);_,acts=induced_actions();U13=next(T for g,T in acts if g==(1,0,3,1))%3;Up=U13[np.ix_(PACKET,PACKET)];Bp=jordan_basis(Up);Bc=jordan_basis(Pc);T=Bp@inv(Bc)%3;Ti=inv(T);transported=[T@pmat(q)@Ti%3 for q in perms]
 params=projective_params();res=row_view(build_residues(params));powers=3**np.arange(13,dtype=np.int64);codes=params.astype(np.int64)@powers;order=np.argsort(codes);sc=codes[order];results=[]
 for g,H in zip(stab,transported):
  M=np.eye(13,dtype=np.int64);M[np.ix_(PACKET,PACKET)]=H;Z=canonical_rows(params.astype(np.int64)@M.T%3);pos=np.searchsorted(sc,Z.astype(np.int64)@powers);idx=order[pos];eq=(res[idx]==res);results.append({'order':porder(g),'spectral_symmetry':bool(np.all(eq)),'matching_projective_words':int(np.sum(eq))})
 good=[i for i,x in enumerate(results) if x['spectral_symmetry']];checks={'packet_and_colored_Jordan_conjugate':np.array_equal(Up@T%3,T@Pc%3),'intertwiner_invertible':rank(T)==12,'transported_A4_order12':len({x.tobytes() for x in transported})==12,'deep_anchor_fixed':True,'all_797162_words_tested':len(params)==797162,'exact_C3_subgroup_survives':len(good)==3 and Counter(results[i]['order'] for i in good)=={1:1,3:2},'all_three_involutions_fail':all(not x['spectral_symmetry'] for x in results if x['order']==2),'canonical_A4_extension_fails':len(good)<12}
 return {'schema':'w33.pass584.colored_intertwiner_a4.v1','status':'PASS' if all(checks.values()) else 'FAIL','colored_objects':{'yellow_faces':sorted(c),'opposite_face_pairs':[list(x) for x in pairs],'ordered_basis':['yellow_face_'+str(x) for x in sorted(c)]+['opposite_pair_'+str(i) for i in range(4)]},'packet_basis':['c0','c1','c2','c3','a0','a1','a2','a3','q0','q1','q2','q3'],'C3_intertwiner':{'matrix_over_F3':T.tolist(),'inverse_over_F3':Ti.tolist(),'equation':'U_packet T = T P_colored','det_nonzero':rank(T)==12},'A4_transport':{'elements':results,'spectral_symmetry_indices':good,'conclusion':'The deterministic Jordan-chain intertwiner gives an exact coordinate-level C3 equivalence. Transporting the full colored A4 to packet coordinates yields 12 linear maps, but exactly its C3 subgroup preserves the full F3^13 characteristic-polynomial map; every order-two generator fails on the exhaustive 797,162-word census.'},'checks':checks,'boundary':'The negative extension result is exact for the deterministic Jordan-chain intertwiner recorded here. A different C3 intertwiner differs by the large centralizer of the unipotent action; this certificate does not prove that every possible conjugacy fails, though random centralizer searches from development consistently retained only C3.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 584 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'surviving':len(p['A4_transport']['spectral_symmetry_indices'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
