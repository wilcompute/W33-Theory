#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,collections,itertools,numpy as np
ROOT=Path(__file__).resolve().parents[1]
def jd(d):return json.dumps(d,sort_keys=True,separators=(',',':'),default=lambda x:x.item())
def dig(d):return hashlib.sha256(jd(d).encode()).hexdigest()
def rankmod(A,p):
 A=A.copy()%p;m,n=A.shape;r=0
 for c in range(n):
  q=next((i for i in range(r,m) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(m):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
 return r
cols=[int(x) for x in (ROOT/'data/w33_pass1848_syndrome_columns.txt').read_text().split()];H=np.zeros((45,240),dtype=np.int64)
for j,x in enumerate(cols):
 for i in range(45):H[i,j]=(x>>i)&1
S=json.loads((ROOT/'data/w33_pass2552_global_signatures720.json').read_text())['signatures'];T=[np.array(z['vector'],dtype=np.int64) for z in S];U=[3*t-4 for t in T];V=[H.T@t-4 for t in T]
D=collections.defaultdict(list)
for i,u in enumerate(U):D[int(u@u)].append(i)
shells=[]
for nu,inds in sorted(D.items()):
 vs=np.array([V[i] for i in inds]);ev=np.linalg.eigvalsh(vs.T@vs);nz=[round(float(x)) for x in ev if x>1e-5]
 hist=collections.Counter(map(int,vs[0]));assert all(collections.Counter(map(int,V[i]))==hist for i in inds)
 shells.append({'u_norm2':nu,'v_norm2':int(V[inds[0]]@V[inds[0]]),'signatures':len(inds),'weighted_covers':sum(S[i]['count'] for i in inds),'v_histogram':dict(hist),'tight_frame_nonzero_eigenvalue':nz[0],'tight_frame_rank':len(nz),'sum_zero':bool(np.all(vs.sum(0)==0))})
checks4={'720':len(T)==720,'rank20':np.linalg.matrix_rank(np.array(V))==20,'four_shells':len(shells)==4,'intertwiner':all(np.array_equal(H@(H.T@u),12*u) for u in U),'norm_scale':all(int(v@v)*3==int(u@u)*4 for u,v in zip(U,V)),'tight_frames':all(x['tight_frame_rank']==20 and x['sum_zero'] for x in shells)}
o4={'schema':'w33.pass2564.joint_octet_fourier_macwilliams.v1','status':'PASS_FOUR_EXACT_TIGHT_SHELLS_ON_COMMON_20D_OCTET_MODULE','shells':shells,'identities':['u=3t-4*1','v=H^T t-4*1=H^T u/3','HH^T u=12u','Hv=4u','||v||^2=(4/3)||u||^2'],'checks':checks4,'theorem':'The 720 nonlinear cover signatures map through the syndrome triangle incidence matrix to four exact zero-sum tight frames in the same 20-dimensional octet eigenspace. Their shell sizes are 45,270,135,270 and the map scales squared norm by 4/3.','boundary':'This is an exact spectral bridge; it does not alone determine all weight-six syndrome multiplicities.'};assert all(checks4.values());o4=json.loads(jd(o4));o4['sha256_without_hash_field']=dig(o4)
mod2=collections.defaultdict(list)
for i,v in enumerate(V):mod2[bytes((v%2).astype(np.uint8))].append(i)
patterns=[np.frombuffer(k,dtype=np.uint8) for k in mod2];P45=[p for p in patterns if int(p.sum())==64];P27=[p for p in patterns if int(p.sum())==160]
A27=np.zeros((27,27),int)
for i,j in itertools.combinations(range(27),2):
 if int(P27[i]@P27[j])==112:A27[i,j]=A27[j,i]=1
B27=A27@A27;lam={int(B27[i,j]) for i in range(27) for j in range(27) if i!=j and A27[i,j]};mu={int(B27[i,j]) for i in range(27) for j in range(27) if i!=j and not A27[i,j]}
inc=np.array([[int(a@b)==64 for b in P27] for a in P45],int);triples=[tuple(np.flatnonzero(r)) for r in inc];triangles={tuple(c) for c in itertools.combinations(range(27),3) if A27[c[0],c[1]] and A27[c[0],c[2]] and A27[c[1],c[2]]}
A45=(inc@inc.T>0).astype(int);np.fill_diagonal(A45,0);B=A45@A45;lam45={int(B[i,j]) for i in range(45) for j in range(45) if i!=j and A45[i,j]};mu45={int(B[i,j]) for i in range(45) for j in range(45) if i!=j and not A45[i,j]}
checks5={'72_patterns':len(patterns)==72,'45_weight64':len(P45)==45,'27_weight160':len(P27)==27,'srg27':all(A27.sum(1)==10) and lam=={1} and mu=={5},'45_all_triangles':len(triangles)==45 and set(triples)==triangles,'incidence_3_5':set(inc.sum(1))=={3} and set(inc.sum(0))=={5},'srg45_complement':all(A45.sum(1)==12) and lam45=={3} and mu45=={3}}
o5={'schema':'w33.pass2565.abstract_schlaefli_incidence.v1','status':'PASS_MOD2_COLLAPSE_IS_ABSTRACT_27_LINE_45_TRITANGENT_SCHLAEFLI_INCIDENCE','mod2_fibers':{'total':72,'weight64':45,'weight160':27,'fiber_size_histogram':dict(collections.Counter(map(len,mod2.values())))},'line_graph':{'parameters':[27,10,1,5],'edge_intersection':112},'tritangent_incidence':{'objects':45,'lines_per_object':3,'objects_per_line':5,'all_line_triangles':45},'tritangent_graph':{'parameters':[45,12,3,3],'relation':'complement of SRG(45,32,22,24)'},'checks':checks5,'theorem':'Reducing the 240-coordinate edge-phase vectors modulo two collapses the 720 signatures to 72 patterns. The 27 weight-160 patterns carry SRG(27,10,1,5); the 45 weight-64 patterns are exactly its 45 triangles, with incidence degrees 3 and 5. This is the abstract Schlaefli 27-line/45-tritangent incidence structure.','boundary':'This is a combinatorial identification of the abstract incidence structure; no algebraic cubic-surface coordinates are asserted.'};assert all(checks5.values());o5=json.loads(jd(o5));o5['sha256_without_hash_field']=dig(o5)
mod3=collections.defaultdict(list)
for i,v in enumerate(V):mod3[bytes((v%3).astype(np.uint8))].append(i)
pairs=[]
for inds in mod3.values():
 for a,b in itertools.combinations(inds,2):
  dt=T[a]-T[b];z=(H.T@dt)//3;assert np.all(H.T@dt%3==0);pairs.append((int(dt@dt),collections.Counter(map(int,dt)),int(z@z),collections.Counter(map(int,z))))
ptype={(x[0],tuple(sorted(x[1].items())),x[2],tuple(sorted(x[3].items()))) for x in pairs};composition=collections.Counter()
for inds in mod3.values():composition[tuple(sorted(int(U[i]@U[i]) for i in inds))]+=1
checks6={'rankF3_44':rankmod(H,3)==44,'360_classes':len(mod3)==360,'sizes_45_270_45':collections.Counter(map(len,mod3.values()))==collections.Counter({1:45,2:270,3:45}),'one_difference_type':len(ptype)==1,'405_pairs':len(pairs)==405}
o6={'schema':'w33.pass2566.mod3_signature_quotient.v1','status':'PASS_MOD3_EDGE_PHASE_QUOTIENT_HAS_360_CLASSES_AND_ONE_COLLISION_TYPE','rank_H_mod3':44,'class_size_histogram':dict(collections.Counter(map(len,mod3.values()))),'shell_composition_histogram':{str(k):v for k,v in composition.items()},'within_class_pair_type':{'pairs':len(pairs),'signature_difference':'four +3, four -3, thirty-seven 0','signature_difference_norm2':72,'edge_phase_quotient_difference':'48 +1, 48 -1, 144 0','edge_phase_difference_norm2':96},'checks':checks6,'theorem':'Modulo three, the 720 edge-phase vectors form exactly 360 residue classes: 45 singletons, 270 pairs, and 45 triples. Every one of the 405 within-class pairs has the same signed weight-eight signature difference and the same 96-norm edge-phase quotient difference.','boundary':'The quotient is exact, but no identification with an external 360-object geometry is asserted.'};assert all(checks6.values());o6=json.loads(jd(o6));o6['sha256_without_hash_field']=dig(o6)
for n,o,name in [(2564,o4,'joint_octet_fourier_macwilliams'),(2565,o5,'abstract_schlaefli_incidence'),(2566,o6,'mod3_signature_quotient')]:
 (ROOT/f'data/w33_pass{n}_{name}.json').write_text(jd(o)+'\n');print(n,o['sha256_without_hash_field'])
