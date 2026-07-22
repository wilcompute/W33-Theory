#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import sympy as sp
from w33_pass568_singer_intersection_design import gl4,inv,comp,conj_group,BLOCKS,ID,mv,order

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass574_singer_coherent_configuration.json'

def scheme_data():
 GL=gl4();invs={g:inv(g) for g in GL};part=frozenset(BLOCKS)
 H=frozenset(g for g in GL if frozenset(frozenset(mv(g,x) for x in b) for b in BLOCKS)==part)
 transport={}
 for g in GL:
  K=conj_group(g,H,invs[g]);transport.setdefault(K,g)
 objects=tuple(sorted(transport,key=lambda K:tuple(sorted(K))));idx={K:i for i,K in enumerate(objects)};base=idx[H]
 unseen=set(range(len(objects)));orbits=[]
 while unseen:
  s=min(unseen);O={idx[conj_group(h,objects[s],invs[h])] for h in H};unseen-=O;orbits.append(tuple(sorted(O)))
 orbits.sort(key=lambda O:(0 if base in O else 1,-len(O),O));relbase={j:r for r,O in enumerate(orbits) for j in O}
 n=len(objects);R=np.empty((n,n),dtype=np.int16)
 for i,X in enumerate(objects):
  t=transport[X];ti=invs[t]
  for j,Y in enumerate(objects):R[i,j]=relbase[idx[conj_group(ti,Y,t)]]
 d=len(orbits);p=np.zeros((d,d,d),dtype=np.int16)
 for k in range(d):
  y=next(j for j in range(n) if R[base,j]==k)
  for i in range(d):
   for j in range(d):p[i,j,k]=np.sum((R[base,:]==i)&(R[:,y]==j))
 return GL,H,objects,idx,transport,invs,base,orbits,R,p

def spectral_tables(p):
 u=sp.I*sp.sqrt(7)
 P=sp.Matrix([
  [1,60,60,60,60,60,15,15,5],
  [1,-4,-4,-36,-4,28,7,7,5],
  [1,-10,-10,18,-10,4,1,1,5],
  [1,6,6,-6,6,-12,-3,-3,5],
  [1,4-4*u,4+4*u,0,-8,4,-3,-1,-1],
  [1,4+4*u,4-4*u,0,-8,4,-3,-1,-1],
  [1,2,2,0,-4,-8,7,1,-1],
  [1,-3,-3,0,6,-3,-3,6,-1],
  [1,-4,-4,0,8,4,1,-5,-1],
 ])
 mult=(1,7,20,28,45,45,56,64,70);val=tuple(int(x) for x in P[0,:])
 character=True
 for r in range(9):
  for i in range(9):
   for j in range(9):
    if sp.simplify(P[r,i]*P[r,j]-sum(int(p[i,j,k])*P[r,k] for k in range(9)))!=0:character=False
 orth=True
 for r in range(9):
  for s in range(9):
   z=sp.simplify(sum(P[r,j]*sp.conjugate(P[s,j])/val[j] for j in range(9)))
   if sp.simplify(z-(sp.Rational(336,mult[r]) if r==s else 0))!=0:orth=False
 Q=sp.zeros(9)
 for i in range(9):
  for r in range(9):Q[i,r]=sp.simplify(sp.Rational(mult[r],val[i])*sp.conjugate(P[r,i]))
 pq=sp.simplify(P*Q-336*sp.eye(9))==sp.zeros(9)
 def fmt(x):return str(sp.simplify(x)).replace('sqrt(7)*I','i*sqrt(7)').replace('I','i')
 return P,Q,mult,val,character,orth,pq,[[fmt(x) for x in row] for row in P.tolist()],[[fmt(x) for x in row] for row in Q.tolist()]

def automorphism_certificate(H,objects,idx,invs,base,orbits,R):
 n=len(objects);r5=next(r for r,O in enumerate(orbits) if len(O)==5);N5=list(orbits[r5]);anchors=[base]+N5
 sig_counter=Counter(tuple(int(R[a,v]) for a in anchors) for v in range(n));pos={a:i for i,a in enumerate(anchors)}
 admissible=[]
 for perm in itertools.permutations(N5):
  amap={base:base,**dict(zip(N5,perm))}
  if not all(R[amap[a],amap[b]]==R[a,b] for a in anchors for b in anchors):continue
  reorder=[pos[amap[a]] for a in anchors]
  transformed=Counter(tuple(s[k] for k in reorder) for s,c in sig_counter.items() for _ in range(c))
  if transformed==sig_counter:admissible.append(perm)
 Himage=set();kernel=[]
 for h in H:
  perm=tuple(idx[conj_group(h,objects[x],invs[h])] for x in N5);Himage.add(perm)
  if perm==tuple(N5):kernel.append(h)
 def sig(v,A):return tuple(int(R[a,v]) for a in A)
 classes=defaultdict(list)
 for v in range(n):classes[sig(v,anchors)].append(v)
 extra_orbit=None
 for v in range(n):
  O={idx[conj_group(h,objects[v],invs[h])] for h in kernel}
  if len(O)==3 and set(classes[sig(v,anchors)])==O:extra_orbit=tuple(sorted(O));break
 assert extra_orbit is not None
 extra=extra_orbit[0];fixed=set(anchors+[extra]);history=[]
 while True:
  fs=sorted(fixed);cl=defaultdict(list)
  for v in range(n):
   if v not in fixed:cl[tuple(int(R[a,v]) for a in fs)].append(v)
  singles=[x[0] for x in cl.values() if len(x)==1]
  history.append({'fixed':len(fixed),'signature_classes':len(cl)+len(fixed),'maximum_class':max([len(x) for x in cl.values()] or [1]),'new_singletons':len(singles)})
  if not singles:break
  fixed.update(singles)
 upper=336*len(admissible)*len(extra_orbit)
 return {
  'valency5_relation':r5,'five_neighborhood':N5,
  'admissible_neighborhood_permutations':len(admissible),'candidate_H_image_on_neighborhood':len(Himage),
  'pointwise_neighborhood_kernel_order':len(kernel),'kernel_order_histogram':dict(sorted(Counter(order(g) for g in kernel).items())),
  'extra_signature_class':list(extra_orbit),'extra_choices_after_neighborhood_image':len(extra_orbit),
  'singleton_refinement_history':history,'pointwise_anchor_stabilizer_trivial':len(fixed)==n,
  'full_automorphism_upper_bound':upper,'candidate_GL42_order':20160,
  'proof':'The transitive GL(4,2) action gives a 20160-element color-automorphism subgroup. Fixing a base object permits at most 20 globally signature-compatible permutations of its five-neighborhood. After one such image, the selected extra vertex has at most three possible images. Once base, neighborhood, and that extra image are fixed, relational singleton refinement fixes all 336 vertices. Hence |Aut| <= 336*20*3=20160, so equality holds.'
 }

def payload():
 GL,H,objects,idx,transport,invs,base,orbits,R,p=scheme_data();P,Q,mult,val,ch,orth,pq,Ps,Qs=spectral_tables(p)
 transpose=[]
 for r in range(9):transpose.append(next(iter({int(R[j,i]) for i,j in zip(*np.where(R==r))})))
 aut=automorphism_certificate(H,objects,idx,invs,base,orbits,R)
 checks={
  'ambient_GL42_order20160':len(GL)==20160,
  'Singer_normalizer_order60':len(H)==60,
  'vertices336':len(objects)==336,
  'rank9':len(orbits)==9,
  'valencies_exact':tuple(map(len,orbits))==(1,60,60,60,60,60,15,15,5),
  'transpose_pair_exact':transpose==[0,2,1,3,4,5,6,7,8],
  'intersection_numbers_nonnegative_integral':bool(np.all(p>=0)),
  'commutative_Bose_Mesner_algebra':bool(np.array_equal(p,p.swapaxes(0,1))),
  'eigenmatrix_character_equations':ch,
  'eigenmatrix_orthogonality':orth,
  'PQ_equals_336I':pq,
  'multiplicities_exact':mult==(1,7,20,28,45,45,56,64,70) and sum(mult)==336,
  'automorphism_upper_equals_candidate':aut['full_automorphism_upper_bound']==20160,
  'full_color_automorphism_group_GL42_A8':aut['pointwise_anchor_stabilizer_trivial'] and aut['candidate_GL42_order']==20160,
 }
 return {
  'schema':'w33.pass574.singer_coherent_configuration.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'scheme':{'name':'Schurian association scheme of GL(4,2) on cosets of the Singer normalizer 15:4','order':336,'rank':9,'valencies':val,'transpose_relations':transpose,'commutative':True,'Gelfand_pair':'(GL(4,2), C15:C4)','intersection_numbers':p.tolist(),'intersection_sha256':hashlib.sha256(p.tobytes()).hexdigest()},
  'spectral':{'first_eigenmatrix':Ps,'second_eigenmatrix':Qs,'multiplicities':mult,'field':'Q(sqrt(-7))','permutation_module_dimensions':mult,'interpretation':'The 336-point permutation module is multiplicity-free. The two degree-45 constituents are complex conjugates, corresponding to the unique nonsymmetric transpose pair.'},
  'automorphisms':aut,
  'checks':checks,
  'boundary':'This is the exact rank-9 Schurian scheme at the GL(4,2) ~= A8 symmetry horizon. Numerical coincidences with E6/Witting dimensions are not promoted to an objectwise E6 embedding.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 574 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'rank':p['scheme']['rank'],'aut':p['automorphisms']['full_automorphism_upper_bound']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
