"""A27-coordinate product common cover, and a stronger mixed-cubic no-go.

This is a different common cover, not a quotient of the induced cover.
Goursat's lemma is classical. All finite groups use the native generators.
"""
import json
import pathlib
import sys

import numpy as np
import sympy as s
from sympy.combinatorics import Permutation,PermutationGroup

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import matrices
from w33_20261102_common_cover_interactions import gaussian_product


def build():
    old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    signed=[]
    for row in old['signed_generators']:
        p=row['permutation'];b=row['sign_bits'];assert p[0]==0 and b[0]==0
        signed.append([2*p[i]+(sign^b[i]) for i in range(27) for sign in range(2)])
    L=PermutationGroup(*[Permutation(p) for p in signed])
    assert L.order()==L.derived_subgroup().order()==30720
    _,blades,units,omega=matrices();U=(s.eye(4)+s.I*blades[15])/s.sqrt(2);units=units+[U]
    def modular(z):
        x=s.expand(z).subs(s.sqrt(2),6).subs(s.I,4);num,den=s.fraction(x)
        return int(num)*pow(int(den),-1,17)%17
    finite=[np.array([[modular(x) for x in row] for row in M.tolist()],dtype=np.int64) for M in units]
    vectors=[(1,0,0,0)];index={vectors[0]:0}
    for v in vectors:
        for M in finite:
            w=tuple(map(int,M@v%17))
            if w not in index:index[w]=len(vectors);vectors.append(w)
    assert len(vectors)==480 and all(tuple(int(i==j) for i in range(4)) in index for j in range(4))
    kperms=[[index[tuple(map(int,M@v%17))] for v in vectors] for M in finite]
    K=PermutationGroup(*[Permutation(p) for p in kperms]);assert K.order()==46080
    paired=[]
    for j,p in enumerate(kperms):paired.append((signed[j] if j<6 else list(range(54)))+[54+i for i in p])
    product=PermutationGroup(*[Permutation(p) for p in paired]);assert product.order()==30720*46080==1415577600
    # Reconstruct every old diagonal-kernel word on the actual spinor.
    interactions=json.loads((ROOT/'data/w33_20261102_common_cover_interactions.json').read_text())
    unitary=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    ugens=[tuple(x) for x in unitary['generator_doubled_integer_keys']]
    identity=tuple(int(2*x) for x in s.eye(4))+(0,)*16;fixed=set(range(27))
    for row in interactions['signed_kernel_word_witnesses']:
        M=identity
        for j in row['word']:M=gaussian_product(ugens[j],M)
        assert M in [identity,tuple(-x for x in identity)]
        fixed&={i for i,b in enumerate(row['sign_bits']) if not b}
    assert fixed=={0}
    variables=s.symbols('b:16');B=s.Matrix(4,4,variables)
    def constraints(gens):
        equations=[x for g in gens for x in g.T*B*g-B]
        A,_=s.linear_eq_to_matrix(equations,variables);return A
    before=constraints(units[:6]);after=constraints(units)
    assert before.rank()==15 and after.rank()==16
    assert all(s.simplify(g.T*omega*g)==omega for g in units[:6])
    moved=s.simplify(U.T*omega*U)
    assert s.Matrix.hstack(omega.reshape(16,1),moved.reshape(16,1)).rank()==2
    assert s.simplify(s.trace(omega.conjugate().T*moved))==0
    return dict(status='PASS_NATIVE27_PRODUCT_COVER_AND_MIXED_CUBIC_OBSTRUCTION',
        signed_scalar_order=30720,signed_scalar_derived_order=30720,linear_spinor_order=46080,
        faithful_spinor_GF17_vector_orbit=vectors,finite_spinor_generators=[M.tolist() for M in finite],
        paired_generators_degree534_1_based=[[i+1 for i in p] for p in paired],paired_group_order=1415577600,
        scalar_carrier_dimension=27,added_scalar_generator='I27',old_six_scalar_generators='Exactly the original signed native27 generators.',
        Goursat_proof='The paired image projects onto perfect L(order30720) and K(order46080). K has a normal2-group of order64 with quotient S6. Any common quotient Q has3-part at most3 because it divides |L|. Hence Q/image(P64) is a proper quotient of S6, so is1 orC2; Q is a2-group. As a quotient of perfect L it is perfect; a finite perfect2-group is trivial. Goursat gives L x K. Direct534-point Schreier-Sims order agrees.',
        scalar_coordinates_surviving_old_kernel=[0],old_bilinear_dimension=1,new_bilinear_dimension=0,
        old_bilinear=[[str(x) for x in row] for row in omega.tolist()],added_gate_transformed_bilinear=[[str(x) for x in row] for row in moved.tolist()],
        stronger_obstruction='For any linear action of the added generator on an unchanged27 whose first six generators are fixed as before, an invariant scalar-spinor-spinor tensor must already be phi0 times Omega. Invariance of this rank-one tensor under the added generator requires U^T Omega U proportional to Omega. The two matrices are orthogonal and independent, so no such nonzero tensor exists. This does not depend on choosing added scalar action I27.',
        tradeoff='A27-coordinate common cover exists and is far smaller than the induced cover, but its generated group is a direct product. It supplies no new holomorphic phi*psi*eta interaction of the prescribed two4-spinors. Hermitian, higher-degree and differently embedded matter interactions are not excluded.',
        boundary='Different common-cover construction, not a quotient contradicting the induced-cover obstruction and not a representation factoring through projective Clifford11520. No global minimum group order or physical matter interpretation is asserted.',
        reference='https://arxiv.org/abs/2603.17515')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_product_cover_coupling_tradeoff.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['paired_group_order'],d['scalar_carrier_dimension'],d['new_bilinear_dimension'],flush=True)
