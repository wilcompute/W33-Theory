"""Canonical 81-qutrit finite Weyl/Heisenberg phase space from the
integral Levi cycle lattice, actual PSp transvections and contragredient
electric variables; finite two-qutrit matrix sanity checks.
No Hilbert-space materialization of dimension 3^81.
"""
from pathlib import Path
import json,sys,cmath,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain,integer_cycle_basis
from w33_pass1081_1086_core import transvection_perm,line_perm
from w33_pass1081_1086_core import rank_mod
def symp(pair,pair2,p=3):
 x,z=pair;a,b=pair2
 return int((np.dot(z,a)-np.dot(b,x))%p)
def coefficient_group():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,D,M,L=chain()
 Z,chords=integer_cycle_basis(flags)
 gram=(Z.T@Z)%3
 assert rank_mod(gram,3)==81
 basis=np.eye(81,dtype=np.int64)
 records=[]
 for seed in (0,1,4,5,13):
  gp=transvection_perm(pts[seed],pts,ix);lp=line_perm(gp,lines,li)
  fperm=[fi[(gp[p],lp[l])] for p,l in flags]
  new=np.zeros_like(Z);new[fperm]=Z
  A=new[chords]
  assert np.array_equal(Z@A,new)
  A3=A@A@A
  assert np.array_equal(A3,basis)
  dual=(A@A).T%3 # = A^-T
  assert np.array_equal((A.T@gram@A)%3,gram)
  assert np.array_equal((A.T@dual)%3,basis%3)
  # Symplectic direct sum (x,z)->(A x,A^{-T} z)
  rng=np.random.default_rng(seed)
  for _ in range(10):
   x,z,a,b=[rng.integers(0,3,size=81,dtype=np.int64) for k in range(4)]
   before=symp((x,z),(a,b))
   after=symp(((A@x)%3,(dual@z)%3),((A@a)%3,(dual@b)%3))
   assert before==after
  records.append(dict(seed=seed,cycle_matrix_order=3,mod3_rank_A_minus_I=rank_mod((A-basis)%3,3),
    electric_dual_formula='A^-T mod3 = (A²)^T mod3',canonical_gram_preserved=True,
    phase_space_pairing_preserved=True,
    electric_support_from_first_generator=int(np.count_nonzero(dual[:,0]%3)),
    magnetic_support_from_first_generator=int(np.count_nonzero(A[:,0]%3))))
 return records

def pauli_sanity():
 w=np.exp(2j*np.pi/3)
 X=np.roll(np.eye(3,dtype=complex),1,axis=0)
 Z=np.diag([1,w,w*w])
 assert np.max(np.abs(Z@X-w*X@Z))<1e-12
 def W(x,z):return np.linalg.matrix_power(X,int(x))@np.linalg.matrix_power(Z,int(z))
 rng=np.random.default_rng(2109)
 worst=0.
 for _ in range(100):
  a,b,c,d=(int(v) for v in rng.integers(0,3,size=4))
  lhs=W(a,b)@W(c,d)
  rhs=(w**((b*c)%3))*W((a+c)%3,(b+d)%3)
  worst=max(worst,float(np.max(np.abs(lhs-rhs))))
 assert worst<1e-12
 # A single arbitrary basis-choice electric/magnetic Hamiltonian is
 # a conditional finite model, no W33-invariant local charge selection.
 H=-(X+X.conj().T+Z+Z.conj().T)
 ev=np.linalg.eigvalsh(H)
 return dict(weyl_relation='Z X = omega X Z',product_phase='omega^(b*c)',
  max_100_random_exact_3by3_product_error=worst,
  single_qutrit_example_H_eigenvalues=[float(v) for v in ev],
  example_ground_gap=float(ev[1]-ev[0]))

def main():
 rec=coefficient_group();test=pauli_sanity()
 out=dict(status='PASS',cycle_rank=81,field='F3',
    physical_pauli_symplectic_dimension=162,heisenberg_group_order='3^163',Schrodinger_Hilbert_dimension='3^81',
    mod3_gram_perfect=True,group_action_records=rec,weyl_3by3_validation=test,
    theorem='The 81D mod3 Levi cycle space V is noncanonically coordinate-isomorphic to F3^81 but canonically pairs with V*=Hom_F3(V,F3). H=V + V* has standard nondegenerate alternating form <(x,z),(a,b)>=z.a - b.x. For every G automorphism represented integrally by A on cycles, diag(A,A^-T) preserves this symplectic form exactly. For the five actual PSp transvections, A^3=I, hence A^-T=(A²)^T. The central extension Heis(H) has order 3^(2*81+1) and unique fixed nontrivial-central-character irrep Hilbert dimension 3^81.',
    obstruction='Native individual cycle coordinates depend on a chosen spanning tree. Local single-qutrit kinetic terms in those 81 coordinates are not invariant under the full PSp group, and the finite Heisenberg algebra by itself chooses neither a local Hamiltonian nor causal propagation.',
    physical_status='Quantum information algebra follows exactly. No novel arbitrary 81-qutrit device or realistic local stabilizer Hamiltonian follows. Small explicit qutrit spectrum is merely a tunable control.')
 (ROOT/'data/w33_20261009_toe21_doubled_qutrit_heisenberg.json').write_text(json.dumps(out,indent=2)+'\n')
 print('QUANTUM',len(rec),'Weyl error',test['max_100_random_exact_3by3_product_error'],'gap',test['example_ground_gap'],flush=True)
 return out
if __name__=='__main__':main()
