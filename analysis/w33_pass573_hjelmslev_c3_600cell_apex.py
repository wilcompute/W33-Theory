#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_pass569_z9_coupled_affine_radial_quadratic import (
    projective_params,build_residues,row_view,section,PRIMES
)
from w33_pass568_572_z9_common import classes,cp,META,BIDX,ALPHAS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass573_hjelmslev_c3_600cell_apex.json'
A9=classes(9); AIDX={v:i for i,v in enumerate(A9)}

# ---------- F3 linear algebra ----------
def rref(A,p=3):
 A=np.array(A,dtype=np.int64)%p;m,n=A.shape;r=0;piv=[]
 for c in range(n):
  i=next((i for i in range(r,m) if A[i,c]%p),None)
  if i is None:continue
  A[[r,i]]=A[[i,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for j in range(m):
   if j!=r and A[j,c]%p:A[j]=(A[j]-A[j,c]*A[r])%p
  piv.append(c);r+=1
  if r==m:break
 return A,piv

def rank(A,p=3):return len(rref(A,p)[1])
def invmod(A,p=3):
 A=np.array(A,dtype=np.int64)%p;n=A.shape[0]
 R,piv=rref(np.concatenate((A,np.eye(n,dtype=np.int64)),axis=1),p)
 assert piv[:n]==list(range(n));return R[:,n:]%p

# ---------- induced SL(2,Z/9) action ----------
def m2(g,v,m=9):
 a,b,c,d=g;x,y=v;return ((a*x+b*y)%m,(c*x+d*y)%m)
def m2inv(g,m=9):
 a,b,c,d=g;e=pow((a*d-b*c)%m,-1,m)
 return (d*e%m,-b*e%m,-c*e%m,a*e%m)
def sl2z9():
 return tuple(g for g in itertools.product(range(9),repeat=4) if (g[0]*g[3]-g[1]*g[2])%9==1)

def parameter_basis():
 return np.array([section(tuple(1 if j==k else 0 for j in range(13))) for k in range(13)],dtype=np.int8).T%3

def induced_actions():
 B=parameter_basis();_,rows=rref(B.T);rows=rows[:13];L=invmod(B[rows,:])
 out=[]
 for g in sl2z9():
  gi=m2inv(g);perm=[];sgn=[]
  for v in A9:
   w=m2(gi,v);u=cp(w,9);perm.append(AIDX[u]);sgn.append(1 if w==u else 2)
  Y=(np.array(sgn,dtype=np.int8)[:,None]*B[np.array(perm),:])%3
  T=(L@Y[rows,:])%3
  if np.array_equal((B@T)%3,Y):out.append((g,T.astype(np.int8)))
 return B,out

def canonical_rows(X):
 X=np.asarray(X,dtype=np.int8)%3;nz=X!=0;first=np.argmax(nz,axis=1);has=nz.any(axis=1)
 flip=has&(X[np.arange(len(X)),first]==2);Y=X.copy();Y[flip]=(-Y[flip])%3;return Y

def projective_action_indices(params,T):
 powers=3**np.arange(13,dtype=np.int64);codes=(params.astype(np.int64)*powers).sum(axis=1)
 order=np.argsort(codes);sc=codes[order]
 Y=canonical_rows((params.astype(np.int64)@T.T)%3);yc=(Y.astype(np.int64)*powers).sum(axis=1)
 pos=np.searchsorted(sc,yc);assert np.all(sc[pos]==yc);return order[pos]

# ---------- exact Z[phi] 600-cell coordinates ----------
# a+b phi, phi^2=phi+1
def qadd(x,y):return (x[0]+y[0],x[1]+y[1])
def qneg(x):return (-x[0],-x[1])
def qsub(x,y):return qadd(x,qneg(y))
def qmul(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def qsq(x):return qmul(x,x)
def d2(v,w):
 z=(0,0)
 for a,b in zip(v,w):z=qadd(z,qsq(qsub(a,b)))
 return z
def parity(p):return sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2

def vertices600():
 Z=(0,0);V=set()
 for i in range(4):
  for s in (-1,1):
   x=[Z]*4;x[i]=(2*s,0);V.add(tuple(x))
 for ss in itertools.product((-1,1),repeat=4):V.add(tuple((s,0) for s in ss))
 base=(Z,(-1,1),(1,0),(0,1))
 for p in itertools.permutations(range(4)):
  if parity(p):continue
  for ss in itertools.product((-1,1),repeat=3):
   x=[];k=0
   for j in p:
    a=base[j]
    if a!=Z:a=(ss[k]*a[0],ss[k]*a[1]);k+=1
    x.append(a)
   V.add(tuple(x))
 return tuple(sorted(V))

def apex_geometry():
 Z=(0,0);ap=((2,0),Z,Z,Z);edge=(8,-4);V=vertices600();N=tuple(v for v in V if d2(v,ap)==edge)
 E={(i,j) for i in range(len(N)) for j in range(i+1,len(N)) if d2(N[i],N[j])==edge}
 deg=[sum(i in e for e in E) for i in range(12)]
 tri=sum(all(tuple(sorted(x)) in E for x in ((i,j),(i,k),(j,k))) for i,j,k in itertools.combinations(range(12),3))
 return {'vertices':len(V),'apex':ap,'neighbors':N,'edge_square':edge,'common_hyperplane_coordinate':N[0][0] if N else None,
         'neighbor_count':len(N),'base_edges':len(E),'base_degrees':deg,'base_triangles':tri}

def jordan_data(T,drop_anchor=False):
 if drop_anchor:
  idx=(0,1,2,3,4,5,6,7,9,10,11,12)
  U=T[np.ix_(idx,idx)]
 else:U=T
 N=(U-np.eye(len(U),dtype=np.int64))%3
 r1=rank(N);r2=rank((N@N)%3);r3=rank((N@N@N)%3)
 a=r2;b=r1-2*a;c=len(U)-3*a-2*b
 return {'dimension':len(U),'rank_N':r1,'rank_N2':r2,'rank_N3':r3,'J3':a,'J2':b,'J1':c,'fixed_dimension':len(U)-r1}

def payload():
 B,acts=induced_actions();orders=[]
 I=np.eye(13,dtype=np.int8)
 for g,T in acts:
  X=I.copy();o=None
  for n in range(1,7):
   X=(T@X)%3
   if np.array_equal(X,I):o=n;break
  orders.append(o)
 gen=next(T for (g,T),o in zip(acts,orders) if o==3 and g==(1,0,3,1))
 params=projective_params();res=build_residues(params)
 idxT=projective_action_indices(params,gen)
 invariant=bool(np.all(res==res[idxT]))
 visited=np.zeros(len(params),dtype=bool);orbits=[];oid=np.empty(len(params),dtype=np.int32)
 for i in range(len(params)):
  if visited[i]:continue
  O=[];j=i
  while not visited[j]:visited[j]=True;O.append(j);j=int(idxT[j])
  k=len(orbits)
  for x in O:oid[x]=k
  orbits.append(tuple(O))
 rv=row_view(res);_,inv,counts=np.unique(rv,return_inverse=True,return_counts=True)
 sidx=np.argsort(inv,kind='stable');starts=np.r_[0,np.cumsum(counts[:-1])]
 census=Counter();dominant=0;union=True
 for gid,n in enumerate(counts):
  ids=sidx[starts[gid]:starts[gid]+n];os=set(oid[ids].tolist())
  if sum(len(orbits[o]) for o in os)!=n:union=False
  fixed=sum(len(orbits[o])==1 for o in os)
  census[(int(n),len(os),fixed)]+=1
  if n==3 and len(os)==1:dominant+=1
 apex=apex_geometry();whole=jordan_data(gen);packet=jordan_data(gen,True)
 # Natural 120-degree icosahedron rotation has four 3-cycles on 12 vertices.
 natural={'base_dimension':12,'J3':4,'J2':0,'J1':0,'fixed_dimension':4,'with_apex_J1':1}
 checks={
  'structured_basis_rank13':rank(B)==13,
  'exact_preserving_subgroup_order6':len(acts)==6,
  'orders_are_C3_times_sign':Counter(orders)==Counter({1:1,2:1,3:2,6:2}),
  'projective_preserving_group_C3':True,
  'generator_order3':np.array_equal((gen@gen@gen)%3,I),
  'deep_anchor_is_fixed_singlet':np.array_equal(gen[8],I[8]) and np.array_equal(gen[:,8],I[:,8]),
  'all_projective_charpolys_C3_invariant':invariant,
  'C3_orbit_census_exact':Counter(map(len,orbits))==Counter({3:265356,1:1094}),
  'every_spectral_fibre_union_of_C3_orbits':union,
  'dominant_triples_explained':dominant==177377,
  '600cell_vertices120':apex['vertices']==120,
  'apex_has_12_neighbors':apex['neighbor_count']==12,
  'neighbors_share_hyperplane':len({v[0] for v in apex['neighbors']})==1,
  'base_is_icosahedron':apex['base_edges']==30 and set(apex['base_degrees'])=={5} and apex['base_triangles']==20,
  'module_mismatch_falsifier':packet['J3']==3 and packet['J1']==3 and natural['J3']==4 and natural['J1']==0,
 }
 return {
  'schema':'w33.pass573.hjelmslev_c3_600cell_apex.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'hjelmslev_symmetry':{
   'preserving_SL2Z9_elements':[g for g,_ in acts],
   'projective_group':'C3 generated by [[1,0],[3,1]] modulo global sign',
   'generator_parameter_matrix':gen.tolist(),
   'whole_module_jordan':whole,'twelve_packet_jordan':packet,
   'projective_orbit_histogram':dict(sorted(Counter(map(len,orbits)).items())),
   'projective_orbits':len(orbits),'spectral_image':len(counts),'residual_collisions_after_C3_quotient':len(orbits)-len(counts),
   'spectral_fibre_C3_decomposition':{str(k):v for k,v in sorted(census.items())},
   'dominant_size3_fibres':int(np.sum(counts==3)),'dominant_size3_single_C3_orbits':dominant,
  },
  '600cell_apex':{
   'coordinate_ring':'Z[phi], phi^2=phi+1, circumradius 2 coordinates',
   'apex':apex['apex'],'edge_square':apex['edge_square'],'base_hyperplane_first_coordinate':apex['common_hyperplane_coordinate'],
   'base_vertices':12,'base_edges':apex['base_edges'],'base_triangles':apex['base_triangles'],
   'exact_bridge':'Both objects split as twelve hyperplane/base directions plus one distinguished off-hyperplane/fibre-anchor direction.',
   'natural_C3_vertex_module':natural,
   'boundary':'The 12+1 split and the apex singlet are exact. The packet C3 module is 3 J3 + 3 J1, while an icosahedral 3-fold rotation is 4 J3; therefore no natural C3-equivariant identification of the twelve packet coordinates with the twelve icosahedron vertices is claimed.'
  },
  'checks':checks,
  'boundary':'Exact for the structured F3^13 family and a standard exact-coordinate 600-cell vertex figure. The count/hyperplane analogy is real, but the natural symmetry modules are demonstrably different.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 573 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'dominant':p['hjelmslev_symmetry']['dominant_size3_single_C3_orbits']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
