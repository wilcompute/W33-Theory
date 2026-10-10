"""The natural E6 27-line PERMUTATION representation tensored with a
trivial A2 triplet cannot be PSp-equivariantly Steinberg-81.
This rules out a naive identification, not all Lie subgroup embeddings.
"""
import json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe24_e8_representation_obstruction.json'
def run():
 # Repository Pass4659 proves a single PSp(4,3) orbit of 27 lines on
 # cubic surface and Schlaefli SRG(27,10,1,5), meeting graph.
 source=json.loads((ROOT/'data/PART_W33_PASS4659_INTERNAL_E6_27_36_45_TRIANGLE.json').read_text())
 assert source['internal_carriers']['lines27']==27
 assert source['27x36']['meeting_graph']=='SRG(27,10,1,5)'
 assert source['action_level_45_bridge']['stabilizer_order']==576
 # 27-dimensional permutation representation contains invariant constant
 # vector. Its eigenprojectors for PSp-invariant meeting adjacency
 # carry dimensions 1,20,6, all proper invariant subspaces.
 n,k,lam,mu=27,10,1,5
 r=sp.sqrt((lam-mu)**2+4*(k-mu))
 eig1=sp.simplify((lam-mu+r)/2)
 eig2=sp.simplify((lam-mu-r)/2)
 assert (eig1,eig2)==(1,-5)
 m1=sp.solve([sp.Eq(sp.Symbol('x')+sp.Symbol('y'),26),
             sp.Eq(k+eig1*sp.Symbol('x')+eig2*sp.Symbol('y'),0)],
             [sp.Symbol('x'),sp.Symbol('y')])
 assert m1=={sp.Symbol('x'):20,sp.Symbol('y'):6}
 # Tensor with trivial A2 triplet = direct sum of three
 # 27-dimensional permutation modules, containing 3 independent
 # fixed vectors. Previous W33 Steinberg81 irreducibility excludes any.
 out=dict(status='PASS',group='PSp(4,3), simple finite group order 25920',
  existing_source='analysis/w33_pass4659_internal_e6_27_36_45_triangle.py, exact 27 Schlaefli carrier and PSp action; analysis/bt1688_exact_h1_character_irreducibility.py and Round21 integral Levi bridge, 81D irreducible Steinberg.',
  permutation27_adjacency_spectrum={'10':1,'1':20,'-5':6},
  natural_permutation27_dim=27,
  tensor27_trivial3_decomposition='3*(1+20+6), so has >=3-dimensional G-fixed vectors',
  steinberg81_invariant_vectors=0,
  canonical_Hom_dim='dim Hom_PSp(St81, Perm27 tensor C3_triv)=0',
  theorem='A PSp-equivariant identification of the W33 irreducible Steinberg-81 with the NAIVE E6 27-line permutation module tensored with a TRIVIAL A2 triplet is impossible. Its dimensions coincide (81=27*3), but invariant-vector multiplicities are 0 vs 3, and target is reducible. This is a hard representation-theoretic obstruction to that specified model, not to a fundamentally different E8 matter embedding.',
  physical_scope='One cannot promote the proven PSp-equivariant 45 tritangent dictionary to a canonical 81D matter intertwiner by taking three copies of the 27-line permutation representation. Need explicit nontrivial factors/projective actions or different symmetry breaking; E8 Jacobi is unaffected.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('E8 obstruction: 81 Steinberg fixed0 vs 27perm times 3 fixed3',flush=True)
 return out
if __name__=='__main__':run()
