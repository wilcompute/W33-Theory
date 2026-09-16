#!/usr/bin/env python3
"""What part of the 45 E6 tritangent Pauli phase data can be gauge invariant?

An individual product of Pauli/Chevalley generators around a tritangent is not
canonical: the exact E8->Pauli lift explicitly permits homogeneous rephasing of
its 80 generators (cocycle gauge).  If phi in F3^45 denotes any transported
central-Pauli triangle phase assignment, rephasing the 27 E6 minuscule vertices
changes phi by R^T a, where R is the 27x45 line/tritangent incidence matrix.
Therefore gauge-invariant linear phase observables are the vectors in ker R.

The repository's Pass7364 already proved the stronger integral identity
    R N = 3 Q
for the 45x36 tritangent/double-six matrix N.  Hence mod 3, im N is contained in
ker R.  Exact ranks are rank_3 R=21 and rank_3 N=14, so
    dim ker R = 24,
    dim H1 = dim(ker R / im N) = 10.
Thus the canonical cubic boundary data reduce any genuinely new mod-3
multi-triangle holonomy to at most ten independent homology classes.

Crucial boundary: the E6 minuscule 27 and the two-qutrit F3^4 Pauli carrier are
different G-sets.  No canonical explicit 27->Pauli-degree transport is currently
certified.  Consequently this file does NOT fabricate numerical phases for the
45 triangles.  It proves the exact gauge/homology target that such a transport
would have to populate.  Individual zeta_12 phases are not physical invariants;
only the central mu3 extension class and homological combinations can survive.
"""
from __future__ import annotations
import importlib.util,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e6_tritangent_pauli_holonomy_frontier.json'

def load(name):
 p=ROOT/'analysis'/(name+'.py');s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def rankp(A,p=3):
 A=np.asarray(A,dtype=np.int64).copy()%p;r=0
 for c in range(A.shape[1]):
  z=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if z is None:continue
  A[[r,z]]=A[[z,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
 return r

def main(write=True):
 # Rebuild the classical cubic carriers using the same shared base as Pass7364.
 base=load('w33_pass4992_4999_common').build_base();T=base['tritangents'];DS=base['DS']
 R=np.zeros((27,45),dtype=np.int64)
 for j,t in enumerate(T):R[list(t),j]=1
 N=1-np.asarray(base['M'],dtype=np.int64)
 Q=np.zeros((27,36),dtype=np.int64)
 for i in range(27):
  for j,D in enumerate(DS):Q[i,j]=int(i not in D)
 assert np.array_equal(R@N,3*Q)
 rR=rankp(R,3);rN=rankp(N,3);assert (rR,rN)==(21,14)
 ker=45-rR;h1=ker-rN;assert (ker,h1)==(24,10)
 # All individual gauge-invariant commutator phases of a qutrit Pauli extension
 # lie in mu_3.  A central qutrit-Pauli phase is a Clifford/stabilizer operation,
 # so a single triangle phase cannot by itself supply non-Clifford magic.
 out={
  'schema':'w33.e6_tritangent_pauli_holonomy_frontier.v1','status':'PASS',
  'headline':'The 45 E6 tritangent phases cannot be treated as 45 canonical Pauli holonomies. Vertex/cocycle rephasing acts through the rank-21 incidence map R^T, leaving a 24-dimensional space of gauge-invariant linear combinations. The canonical double-six boundary map has rank 14 inside that space mod 3, so only H1 dimension 10 remains as an essential homological phase target.',
  'cubic_complex':{'R_shape':[27,45],'N_shape':[45,36],'identity':'R N = 3 Q','rank_F3_R':rR,'rank_F3_N':rN,'gauge_invariant_functional_space_dim':ker,'essential_H1_dim':h1},
  'pauli_boundary':{'individual_zeta12_triangle_phase':'gauge dependent under homogeneous generator rephasing','gauge_invariant_pair_commutator':'mu_3 central Pauli phase','single_triangle_nonClifford_magic':False},
  'new_target':'Construct a certified transport from the E6 minuscule 27/tritangent carrier to an enriched Pauli/VOA carrier, evaluate the induced 45-vector phi, and pair it with a basis of the ten H1 classes. A nonzero H1 class is the first place a genuinely global cubic phase obstruction can live.',
  'prior_art':['analysis/w33_pass7364_7366_integral_27_45_36_complex.py','analysis/w33_e6_45_tritangent_zero_sum_bridge.py','data/w33_e8_pauli_cocycle_lift.json'],
  'boundary':'This is an exact gauge/homology reduction, not an evaluated physical magic witness. No canonical 27-to-Pauli-degree transport is presently certified, so numerical tritangent holonomies are intentionally not invented.',
  'checks':{'45_tritangents':len(T)==45,'36_double_sixes':len(DS)==36,'RN_eq_3Q':True,'rank_R_21':True,'rank_N_14':True,'ker_dim_24':True,'H1_dim_10':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
