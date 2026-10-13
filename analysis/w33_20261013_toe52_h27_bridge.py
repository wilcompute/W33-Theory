"""TOE52 preliminary: H27 unipotent parabolic action on W33 40 lines."""
import numpy as np
import runpy
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=runpy.run_path(str(R/"analysis/w33_20261013_toe50_dual_cusp_spread_decoder.py"))
lines=x["lines"]; pts=x["x"]["P"]; ix=x["x"]["ix"]; canon=x["x"]["canon"]
n={tuple(l):j for j,l in enumerate(lines)}
J=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
Ms=[];perms=[]
for a in range(3):
 for b in range(3):
  for c in range(3):
   M=np.array([[1,a,c,b],[0,1,b,0],[0,0,1,0],[0,0,-a,1]],dtype=int)%3
   assert np.array_equal((M.T@J@M)%3,J%3)
   mapped=[]
   for l in lines:
    dest=tuple(sorted(ix[canon(tuple((M@np.array(pts[p]))%3))] for p in l))
    mapped.append(n[dest])
   assert len(set(mapped))==40
   Ms.append(M);perms.append(np.array(mapped))
assert len({tuple(M.flatten()) for M in Ms})==27
orbit=[];seen=set()
for i in range(40):
 if i in seen:continue
 o=sorted(set(p[i] for p in perms));orbit.append(o);seen.update(o)
print('orbits',[[len(z),z[:15]] for z in orbit])
print('fix',Counter(int(sum(p[i]==i for i in range(40))) for p in perms))
print('id',[(i,len(z)) for i,z in enumerate(orbit)])
print('sum',sum(len(o) for o in orbit))

# Validate H27 group and compare invariant multiplicities.
pdict={tuple(M.flatten()):i for i,M in enumerate(Ms)}
identity=pdict[tuple(np.eye(4,dtype=int).flatten())]
mult=np.array([[pdict[tuple(((X@Y)%3).flatten())] for Y in Ms] for X in Ms])
assert np.all(mult[:,identity]==np.arange(27)) and np.all(mult[identity,:]==np.arange(27))
orders=[]
for a in range(27):
 p=a;n=1
 while p!=identity:
  p=mult[p,a];n+=1
 assert n<=3
 orders.append(n)
center=[a for a in range(27) if all(mult[a,b]==mult[b,a] for b in range(27))]
assert len(center)==3
E=np.zeros((40,40))
for p in perms:
 E[p,np.arange(40)]+=1/27
assert np.max(abs(E@E-E))<1e-12
P0=x['J']/40;P24=.75*(x['G']-8*P0);P15=(x['B']@x['B'].T-90*P0)/18
ids=[float(np.trace(E@P)) for P in (P0,P24,P15)]
assert abs(sum(ids)-8)<1e-10
print('H27 exponent',Counter(orders),'center',center,'fixed dims 1/24/15',ids)

# Explicit K81 = 3 copies of the 27D left regular H27 action.
T=[]
for a in range(27):
 Q=np.zeros((27,27))
 Q[mult[a],np.arange(27)]=1
 T.append(np.kron(np.eye(3),Q))
S=[]
for p in perms:
 Q=np.zeros((40,40))
 Q[p,np.arange(40)]=1
 S.append(Q)
assert all(np.max(abs(T[a]@T[b]-T[mult[a,b]]))<1e-12 for a in range(27) for b in range(27))
rng=np.random.default_rng(52011)
C=rng.normal(size=(81,40))
A=sum(T[g]@C@S[g].T for g in range(27))/27
assert max(np.max(abs(T[g]@A-A@S[g])) for g in range(27))<2e-13
sector_details={}
for lbl,Uproj in [('full',np.eye(40)),('cusp25',P0+P24),('spread15',P15),('24',P24)]:
 ev,Z=np.linalg.eigh(Uproj)
 U=Z[:,ev>.5]
 D=A@U
 sv=np.linalg.svd(D,compute_uv=False)
 localrank=int(sum(sv>sv[0]*1e-9))
 sector_details[lbl]={'dimension':len(sv),'image_rank':localrank,'min_nonzero_sv':float(sv[localrank-1]),'max_sv':float(sv[0]),
                      'nullity':len(sv)-localrank}
 if lbl=='spread15':
  # Polar factor preserves intertwining because its Gram commutes with S_g.
  DD=D.T@D
  dd,V=np.linalg.eigh(DD)
  assert np.min(dd)>1e-12,dd
  F=D@(V@np.diag(dd**-.5)@V.T)
  assert np.linalg.norm(F.T@F-np.eye(15))<1e-11
  cov=max(np.max(abs(T[g]@F-F@(U.T@S[g]@U))) for g in range(27))
  assert cov<1e-10,cov
  rng2=np.random.default_rng(51009)
  errors=[]
  for _ in range(35):
   coeff=rng2.normal(size=15)
   errors.append(float(max(abs(F.T@(F@coeff)-coeff))))
  assert max(errors)<1e-11
  sector_details[lbl]['max_covariance_all27']=float(cov)
  sector_details[lbl]['max_reconstruction_35']=max(errors)
print('intertwiners',sector_details)
assert sector_details['full']['image_rank']<40
assert sector_details['cusp25']['image_rank']<25
assert sector_details['spread15']['image_rank']==15

# Multi-slice exact Reynolds projections and certified mod-101 ranks.
def rank_mod(A,p=101):
 X=np.array(A%p,dtype=np.int64).copy()
 r=0
 for col in range(X.shape[1]):
  pivot=next((j for j in range(r,X.shape[0]) if X[j,col]),None)
  if pivot is None:continue
  X[[r,pivot]]=X[[pivot,r]]
  X[r]=(X[r]*pow(int(X[r,col]),-1,p))%p
  for i in range(r+1,X.shape[0]):
   if X[i,col]:
    X[i]=(X[i]-int(X[i,col])*X[r])%p
  r+=1
  if r==X.shape[1]:break
 return r
# Integer projector numerators: N15=24 P15, N25=24 P25.
Aline=x['A'].astype(np.int64)
N15=8*np.eye(40,dtype=np.int64)-4*Aline+np.ones((40,40),dtype=np.int64)
N25=16*np.eye(40,dtype=np.int64)+4*Aline-np.ones((40,40),dtype=np.int64)
assert np.max(abs(N15/24-P15))<1e-12
assert np.max(abs(N25/24-(P0+P24)))<1e-12
rng=np.random.default_rng(52030)
seed=rng.integers(-2,3,size=(243,40),dtype=np.int64)
reyn=np.zeros_like(seed)
# 243 = nine disjoint left-regular 27D copies, grouped 3×81.
for g in range(27):
 inv=np.argsort(perms[g])
 incols=seed[:,inv]
 for k in range(9):
  outrows=mult[g]+27*k
  reyn[outrows,:]+=incols[27*k:27*(k+1),:]
def proper_covariance(reyn,k):
 for g in range(27):
  source=reyn[:81*k,perms[g]]
  target=np.zeros_like(source)
  for h in range(3*k):
   target[27*h+mult[g],:]=reyn[27*h:27*(h+1),:]
  # intertwiner A S_g= T_g A: source[:,source indices i]=A[:,p_g[i]]
  # target is T_g A, using push-forward row g*h.
  assert np.array_equal(source,target)
proper_covariance(reyn,3)
sizes={}
for k in [1,2,3]:
 Z=reyn[:81*k]
 sizes[str(k)]={"ambient":81*k,"full_integer_mod101_rank":rank_mod(Z),
 "even25_integer_mod101_rank":rank_mod(Z@N25),
 "spread15_integer_mod101_rank":rank_mod(Z@N15)}
assert [(sizes[str(k)]["full_integer_mod101_rank"]) for k in [1,2,3]]==[35,38,40]
assert [(sizes[str(k)]["even25_integer_mod101_rank"]) for k in [1,2,3]]==[23,25,25]
assert all(sizes[str(k)]["spread15_integer_mod101_rank"]==15 for k in [1,2,3])
# Polar isometry from exact rational intertwiner; numerical covariance check.
iso_checks={}
for label,k,Pj in [("spread15",1,P15),("even25",2,P0+P24),("full40",3,np.eye(40))]:
 vals,U=np.linalg.eigh(Pj)
 Q=U[:,vals>.5]
 W=reyn[:81*k].astype(float)@Q
 m=Q.shape[1]
 sing=np.linalg.svd(W,compute_uv=False)
 assert sing[-1]>1e-7,(label,sing[-1])
 Gram=W.T@W
 ev,V=np.linalg.eigh(Gram)
 F=W@(V@(np.diag(ev**(-.5)))@V.T)
 iso_err=float(np.max(abs(F.T@F-np.eye(m))))
 cov_err=0.
 for g in range(27):
  p=perms[g]
  left=np.zeros_like(F)
  for h in range(k*3):
   left[27*h+mult[g]]=F[27*h:27*(h+1)]
  Sg=np.zeros((40,40))
  Sg[p,np.arange(40)]=1
  right=F@(Q.T@Sg@Q)
  cov_err=max(cov_err,float(np.max(abs(left-right))))
 assert max(iso_err,cov_err)<1e-10,(label,iso_err,cov_err)
 iso_checks[label]={"source_dimension":m,"carrier_slices":k,
   "min_singular_integer_Reynolds":float(sing[-1]),
   "max_orthonormality_residual":iso_err,
   "max_covariance_27_group_elements":cov_err}
print('slice ranks',sizes,'isometries',iso_checks)

import json
from collections import Counter
certificate={
 "status":"TOE52_H27_K81_THREE_SLICE_EQUIVARIANT_EMBEDDING_WITH_MINIMUM_CARRIER_THEOREM",
 "H27_group_order":27,"center_order":len(center),"element_order_distribution":{str(j):int(v) for j,v in Counter(orders).items()},
 "H27_realization":"Nonabelian order-27 exponent-three symplectic unipotent point stabilizer; matrices M(a,b,c)=[[1,a,c,b],[0,1,b,0],[0,0,1,0],[0,0,-a,1]] mod3.",
 "W33_line_orbit_lengths":sorted([len(o) for o in orbit]),
 "H27_line_permutation_fixed_points_by_element":{str(j):int(v) for j,v in Counter(int(sum(p[i]==i for i in range(40))) for p in perms).items()},
 "H27_invariant_subspace_dimensions":{"all40":int(round(np.trace(E))),"constant1":int(round(ids[0])),"plus24":int(round(ids[1])),"minus15":int(round(ids[2])),"even25":int(round(ids[0]+ids[1]))},
 "one_K81_H27_restriction":"K81=Reg(H27)xReg(C3), hence as H27-module exactly 3 copies of 27D regular H27, and exactly 3 trivial representations.",
 "representation_theorem":"An injective H27-intertwiner must inject source invariant vectors into target invariant vectors. The source 15-,25-,40-dimensional sectors have 3,5,8 H27 invariants. Thus at least ceil(d_invariants/3)=1,2,3 separate K81 carriers are required respectively. Exact integer Reynolds-map mod101 ranks attain 15,25,40 with these carrier counts, proving sufficiency in characteristic zero; polar decomposition yields isometric H27-intertwiners. No full K81 or Sp4(3) intertwiner follows.",
 "number_of_H27_regular_copies_per_K81":3,
 "tested_81D_slice_counts":sizes,
 "integer_modulus_for_frozen_rank_certification":101,
 "integer_reynolds_projection":"Seed C chosen with fixed numpy seed 52030 and integer entries -2..2. A=sum_{g in H27} rho_target(g) C rho_line(g)^-1, no division. Its exact mod101 ranks certify lower bounds on characteristic-zero ranks.",
 "explicit_polar_isometries":iso_checks,
 "exact_integer_projector_numerators":{"N_spread15":"24P15=8I-4Aline+J","N_cusp25":"24P25=16I+4Aline-J"},
 "source_reference":"TOE50 exact 40-line 1+24+15 cusp/spread decomposition, Pass3694-3700 36 spreads; Holotrade 2026-09-26 three K81 carriers report and repo head b0264880d7c5.",
 "scientific_limits":"The choice of an abstract H27 isomorphism is fixed here using integer Heisenberg group law. The H27 subgroup of the 40-line permutation module is NOT automatically the physical H27 action on Holotrade fibers. No commuting action of the additional K81 C3 generator on source has been matched, no Sp4 extension, no photonic implementation or universality claim."}
(R/"data/w33_20261013_toe52_h27_K81_minimal_slices.json").write_text(json.dumps(certificate,indent=2)+"\n")
print("CERTIFICATE",json.dumps({k:certificate[k] for k in ["status","H27_line_permutation_fixed_points_by_element","H27_invariant_subspace_dimensions","tested_81D_slice_counts"]}))
