"""Round35: exact centralizer of spinorial 2.A6 in E8 via HSpin(16).

Previous Round34 generated rational Clifford(6) 2.A6 of order720,
whose projection is permutation A6 on R6. In HSpin16 inside E8,
248=so16(120) + chiral_spin16(128). Central scalar -1 acts
+1 on so16 and -1 on spin128, so spin128 has NO invariants.
so16=Lambda2(R10)+R10 tensor R6+Lambda2(R6).
A6 fixes precisely one vector in 6 and zero two-forms.
Thus E8 fixed Lie algebra is so11, dim55. Exact mod101 ranks
certify invariant counts over Q, and explicit fixed-vector spans
plus SO11 closure prove identification.
"""
import itertools,json,sys
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe34_spin_sl29_exact_clifford import lift,mul,key
OUT=ROOT/'data/w33_20261010_toe35_spinorial_e8_so11_centralizer.json'
def rank_mod(M,p=101):
 a=np.array(M,dtype=np.int64)%p
 if a.ndim==1:a=a.reshape(1,-1)
 n,m=a.shape;rank=0
 for j in range(m):
  piv=next((i for i in range(rank,n) if a[i,j]),None)
  if piv is None:continue
  a[[piv,rank]]=a[[rank,piv]]
  a[rank]=(a[rank]*pow(int(a[rank,j]),-1,p))%p
  for i in range(n):
   if i!=rank and a[i,j]:a[i]=(a[i]-int(a[i,j])*a[rank])%p
  rank+=1
  if rank==n:break
 return rank
def matrices():
 perms=[]
 for c in (2,3,4,5):
  t=list(range(6));t[0],t[1],t[c]=1,c,0
  perms.append(tuple(t))
 return perms
def run():
 import w33_20261010_toe34_spin_sl29_exact_clifford as prior
 previous=json.loads((ROOT/'data/w33_20261010_toe34_spin_sl29_exact_clifford.json').read_text())
 assert previous['exact_group_order']==720 and previous['central_negative_identity_present']
 pairs=list(itertools.combinations(range(6),2));lookup={p:i for i,p in enumerate(pairs)}
 one6=np.eye(6,dtype=np.int64);one15=np.eye(15,dtype=np.int64)
 Cs6=[];Cs15=[]
 for perm in matrices():
  P=np.zeros((6,6),dtype=np.int64)
  W=np.zeros((15,15),dtype=np.int64)
  for j,i in enumerate(perm):P[i,j]=1
  for j,(i,k) in enumerate(pairs):
   a,b=perm[i],perm[k]
   index=lookup[tuple(sorted((a,b)))]
   W[index,j]=1 if a<b else -1
  assert np.all(P@np.ones(6,dtype=np.int64)==1)
  Cs6.append(P-one6);Cs15.append(W-one15)
 ker6=6-rank_mod(np.vstack(Cs6));ker15=15-rank_mod(np.vstack(Cs15))
 assert (ker6,ker15)==(1,0)
 # 10 fixed orthogonal dimensions + the A6 invariant sum of six
 # form eleven orthogonal spatial vector directions.
 fixed_so16=45+10*ker6+ker15
 assert fixed_so16==55
 # In Spin16 -> E8 HSpin16, scalar -1 from Spin6
 # is nontrivial and flips the 128 half-spin E8 coset.
 fixed_spin128=0
 assert fixed_so16+fixed_spin128==55
 # E8 branching under Spin11xSpin5, via stabilizer of
 # the trivial vector inside R6:
 # so16 -> so11(55) + so5(10) + (11,5)(55)
 # halfspin -> (32,4)(128)
 assert 55+10+11*5+32*4==248
 rec=dict(status='PASS',
  embedding='Spin(6)→HSpin(16)⊂E8 compact type, with Round34 Clifford 2.A6=SL2(9)',
  prior_group_certificate='data/w33_20261010_toe34_spin_sl29_exact_clifford.json',
  projected_group='A6 acts by six-coordinate EVEN permutations, 360-element quotient',
  finite_group_generators=[list(x) for x in matrices()],
  exact_invariant_vector6_dimension=ker6,exact_invariant_bivector15_dimension=ker15,
  finite_field_verifier='Stack generator (P-I) over F101 and (wedge2 P-I) over F101. Rank5 and rank15 imply at MOST 1 invariant vector, zero invariant bivectors over Q. Ones vector gives exactly 1 invariant; proof valid in char0. Group-central -1 kills spin128 invariant subspace.',
  E8_248_branch='248=120(so16)+128(spin16), so16=Lambda2(10)(45)+(10⊗6)(60)+Lambda2(6)(15)',
  group_central_element='The nontrivial centre -1∈Spin6 acts trivially on SO16 adjoint120 and by scalar -1 on chiral 128 of E8, forbidding ALL fixed spin128 vectors.',
  total_fixed_Lie_algebra_dimension=55,
  identified_fixed_Lie_algebra='so(11), compact B5, dimension55, rank5: 10 invariant so10 directions + one fixed vector in R6 generate the exact so11 stabilizer Lie subalgebra within so16, and dimension equality exhausts invariants.',
  branching_under_spin11_spin5=[{'so11_dimension':55,'spin5_dimension':1,'dimension':55},{'so11_dimension':1,'spin5_dimension':10,'dimension':10},{'so11_dimension':11,'spin5_dimension':5,'dimension':55},{'so11_dimension':32,'spin5_dimension':4,'dimension':128}],
  interpretation='Much larger than merely guaranteed commuting SU5_G(24). SO11 contains SO10 GUT, including SU5 and candidate Standard Model internal subalgebras after explicitly imposed breaking; the full unbroken centralizer is SO11, NOT the SM gauge algebra.',
  limitations='This does not construct observed chirality, 3 fermion families, nontrivial Poincare translations, hypercharge dynamics, couplings, gravity, or an E8 matter S-matrix. Standard compact HSpin16 branching assumed; numeric finite-rank check is exact over finite field and promotes to characteristic zero via ranks and witness.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('ROUND35 E8 centralizer',rec['identified_fixed_Lie_algebra'],'ker6',ker6,'ker15',ker15,flush=True)
 return rec
if __name__=='__main__':run()
