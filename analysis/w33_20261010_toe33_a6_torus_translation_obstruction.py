"""Round33 A6/PSp Lorentz torus translation embedding obstruction.

A5 Weyl reflection action W(A5)=S6 on its rank5 root lattice:
augmentation S={x in F3^6 : sum x=0}, with invariant vector
1=(1,...,1) since 6=0 mod3. Six-permutation A6 acts. Prove
no invariant 4D subgroup of its 3-torsion Cartan S.
"""
from pathlib import Path
import numpy as np,json,itertools,collections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe33_a6_torus_translation_obstruction.json'
def cycle(*a):
 x=list(range(6))
 for i,j in zip(a,a[1:]+a[:1]):x[i]=j
 return tuple(x)
def mul(p,q):return tuple(p[q[i]] for i in range(6))
def rank3(mat):
 M=np.asarray(mat,dtype=np.int16).copy()%3
 if M.ndim==1:M=M[None,:]
 m,n=M.shape;k=0
 for col in range(n):
  good=next((i for i in range(k,m) if M[i,col]),None)
  if good is None:continue
  M[[k,good]]=M[[good,k]]
  M[k]=M[k]* (1 if M[k,col]==1 else 2)%3
  for i in range(m):
   if i!=k and M[i,col]:M[i]=(M[i]-M[i,col]*M[k])%3
  k+=1
  if k==m:break
 return k
def run():
 gens=[cycle(0,1,j) for j in (2,3,4,5)]
 G={tuple(range(6))};todo=collections.deque(G)
 while todo:
  p=todo.popleft()
  for q in gens:
   z=mul(p,q)
   if z not in G:G.add(z);todo.append(z)
 assert len(G)==360,('not A6',len(G))
 basis=np.zeros((5,6),dtype=np.int16)
 for j in range(5):basis[j,j]=1;basis[j,5]=2
 matrices=[]
 for g in gens:
  mat=np.zeros((5,5),dtype=np.int16)
  for j in range(5):
   transformed=np.zeros(6,dtype=np.int16)
   for i in range(6):transformed[g[i]]=basis[j,i]
   mat[:,j]=transformed[:5]
  assert rank3(mat)==5
  matrices.append(mat)
 # invariant vector ones_6 has coordinates all ones in this basis
 c=np.ones(5,dtype=np.int16)
 assert all(np.all((M@c)%3==c) for M in matrices)
 # All 3^5 vectors under A6: their generated submodules have dims1
 # for C invariant constants or all5 for every other vector.
 counts=collections.Counter()
 for v in itertools.product(range(3),repeat=5):
  a=np.asarray(v,dtype=np.int16)
  if not np.any(a):continue
  orbit={tuple(a)};q=collections.deque([tuple(a)])
  while q:
   x=np.asarray(q.popleft(),dtype=np.int16)
   for M in matrices:
    y=tuple((M@x)%3)
    if y not in orbit:orbit.add(y);q.append(y)
  dim=rank3(list(orbit));counts[dim]+=1
 assert counts[1]==2 and counts[5]==240 and sum(counts.values())==242,counts
 # invariant linear functionals on S are none:
 # row vector f satisfying f M=f => rank stacked constraints=5.
 constraint=np.vstack([(M-np.eye(5,dtype=np.int16)).T for M in matrices])
 assert rank3(constraint)==5
 # no stable 4-dim subspace, but 4D quotient S/C exists.
 # Consequently an A6-module isomorphic to S/C cannot embed
 # as torus translations in S. This says nothing about non-Cartan
 # translations or different embedding, projective extension.
 res=dict(status='PASS',group='A6=W(A5) derived, PSL(2,9), order360',
  generators=[list(x) for x in gens],generator_order=360,
  Cartan_A5_3torsion_module='S={x∈F3^6: Σx=0}, dimension5, A6 permutes coordinates',
  invariant_ones_vector_dim=1,invariant_functional_dim=0,
  orbit_generated_submodule_dim_counts={str(k):int(v) for k,v in sorted(counts.items())},
  proper_nonzero_submodules='Exactly C=<ones>, dimension1, not a 4D A6-stable submodule',
  exact_four_dimensional_quotient='S/C has dimension4 and carries A6 representation, but is NONSPLITTING (not a submodule of S).',
  theorem='For this standard A5 root-torus 3-torsion action, there is NO 4D A6-stable subgroup implementing the 4D finite translations as an honest subgroup of T_A5[3]. The desired 4D module exists as quotient S/C but NOT a Lorentz-equivariant subspace of the five-dimensional A5 torus, since the extension 0→C→S→S/C→0 does not split.',
  scope='Verified exact finite F3 computations, closure order360 and exhaustive nonzero vector invariant spans. Does NOT rule out finite Poincare embedding in E8 using extra A2/A1 torus components, other 3-subgroups, or a non-Cartan construction. Not an observed physics theorem.',
  parallel_prior='Tits A5 in E8 Lorentz and su3+su2 commutant are published in parallel Pass11843; this is a new modular-translation representation test for a specific Tits torus.')
 OUT.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('A6 TORUS rank constraints',rank3(constraint),'submodules',dict(counts),flush=True)
 return res
if __name__=='__main__':run()
