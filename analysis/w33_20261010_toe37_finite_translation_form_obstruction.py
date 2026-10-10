"""TOE37 track2: A6 Minkowski quotient F3^4: invariant forms & Heisenberg test.
Exact A6 3cycle action on S/<ones>, S=sum-zero vectors in F3^6.
Invariant symmetric quadratic form versus alternating commutator.
A nonabelian central F3 Heisenberg extension with nonzero
commutator requires invariant alternating form on F3^4.
"""
from pathlib import Path
import itertools,json,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe35_spinorial_e8_so11_centralizer import matrices
OUT=ROOT/'data/w33_20261010_toe37_finite_translation_form_obstruction.json'
def rank3(A):
 a=np.asarray(A,dtype=np.int64).copy()%3;n,m=a.shape;rank=0
 for j in range(m):
  found=next((i for i in range(rank,n) if a[i,j]),None)
  if found is None:continue
  a[[rank,found]]=a[[found,rank]]
  a[rank]=a[rank]*pow(int(a[rank,j]),-1,3)%3
  for i in range(n):
   if i!=rank and a[i,j]:a[i]=(a[i]-int(a[i,j])*a[rank])%3
  rank+=1
 return rank
def rep4(perm):
 # quotient S / <(1,...,1)>, choose e_0-e_5,..,e_3-e_5
 G=np.zeros((4,4),dtype=np.int64)
 for i in range(4):
  v=np.zeros(6,dtype=np.int64);v[perm[i]]+=1;v[perm[5]]-=1
  a=v[:5]
  G[:,i]=(a[:4]-a[4])%3
 return G
def run():
 gens=[rep4(p) for p in matrices()]
 assert len(gens)==4
 Gram=(np.eye(4,dtype=np.int64)+np.ones((4,4),dtype=np.int64))%3
 assert rank3(Gram)==4
 assert all(np.all((g.T@Gram@g-Gram)%3==0) for g in gens)
 basis=[]
 for a,b in itertools.combinations(range(4),2):
  J=np.zeros((4,4),dtype=np.int64);J[a,b]=1;J[b,a]=-1;basis.append(J)
 forms=np.vstack([np.array([(g.T@J@g-J)%3 for J in basis]).reshape(6,16).T for g in gens])
 rank=rank3(forms)
 invariant_alt=6-rank
 print('TOE37 finite SO4minus forms sym-rank',rank3(Gram),'alt invariant dim',invariant_alt,flush=True)
 full5=[]
 for perm in matrices():
  T=np.zeros((5,5),dtype=np.int64)
  for i in range(5):
   v=np.zeros(6,dtype=np.int64);v[perm[i]]+=1;v[perm[5]]-=1
   T[:,i]=v[:5]%3
  assert np.all((T@np.ones(5,dtype=np.int64)-np.ones(5,dtype=np.int64))%3==0)
  full5.append(T)
 invariant_functional_dim=5-rank3(np.vstack([T.T-np.eye(5,dtype=np.int64) for T in full5]))
 assert invariant_functional_dim==0
 assert (3**5*720,3**4*720)==(174960,58320)
 out=dict(status='PASS',prime=3,
   full_five_dim_translation_action_mod3=[T.tolist() for T in full5],
   invariant_functional_dimension_on_S=invariant_functional_dim,
   abstract_spinorial_finite_Poincare_group_order=174960,
   order_after_quotient_by_central_constant=58320,
   abstract_semidirect_presentation='G=F3^5 ⋊ 2.A6, 2.A6 acts on translations through A6 permutations of six sum-zero coordinates; central spin -1 acts trivially on translations. The A6-fixed constant vector c gives central Z3, with F3^5/<c> Minkowski F3^4. No A6-equivariant complement exists because no invariant linear functional on S.',
   important_embedding_boundary='Abstract group with explicit F3 matrices and earlier Clifford 720 spin lift, NOT an actual 248-dimensional E8 embedding of all noncentral translations.',
   A6_generator_matrices_mod3=[g.tolist() for g in gens],
   quotient_module='M=S/<1>, S={(x0,...,x5) in F3^6: sum x_i=0}, dim M=4. A6 acts via 6-coordinate even permutations.',
   Gram_symmetric_mod3=Gram.tolist(),Gram_nondegenerate=True,
   alternating_constraint_rank=rank,alternating_invariant_dimension=invariant_alt,
   actual_nontrivial_Heisenberg_central_extension_compatible=bool(invariant_alt>0),
   conceptual_boundary='This is the 360-element A6 quadratic Minkowski quotient, not the faithful 720-element spinor Di. A nonabelian class-two F3 central extension E with commutator E/Z x E/Z -> Z3 requires invariant nonzero alternating form. If invariant dimension is0, no such construction for THIS A6 action with centre fixed. The earlier NON-SPLIT abelian S extension Z3.M does not need an alternating commutator and is not ruled out. No E8 embedding of full translations tested by this module calculation.',
   Lorentz_spinorial_warning='To represent a nontrivial spinorial double-cover action on M, its centre acts trivially on M by projection A6; a distinct spinor representation handles fermions.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
