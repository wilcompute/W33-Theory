"""Independent dense carrier, Gysin-extension and compact-Wilson controls."""
import json
from pathlib import Path
import sys
import unittest
import numpy as np
import sympy as s
from sympy.matrices.normalforms import smith_normal_form
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_native_E8_Cfield_flat_gates as m


class NativeCfieldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=m.run()

    def test_native_cubic_against_dense_three_matrix_action(self):
        _,_,_,coords=m.native_data()
        reconstruction=json.loads((ROOT/'data/toe_20261113_h27_albert_cubic_coordinate_reconstruction.json').read_text())
        negative=set(reconstruction['signed_rephasing_negative_E6_indices'])
        rng=np.random.default_rng(191119)
        for name in ('X','D'):
            perm,phase=self.data['native_27_generators'][name]
            U=np.zeros((27,27),complex)
            for j in range(27):U[perm[j],j]=np.exp(2j*np.pi*phase[j]/18)
            for _ in range(5):
                v=rng.normal(size=27)+1j*rng.normal(size=27)
                def matrices(v):
                    out=np.zeros((3,3,3),complex)
                    for j,c in enumerate(coords):out[c]=(-1 if j in negative else 1)*v[j]
                    return out
                A,B,C=matrices(v);AA,BB,CC=matrices(U@v)
                f=lambda A,B,C:np.linalg.det(A)+np.linalg.det(B)+np.linalg.det(C)-np.trace(A@B@C)
                self.assertLess(abs(f(A,B,C)-f(AA,BB,CC)),1e-10)

    def test_clock_transport_full_dense_matrices(self):
        bridge=json.loads((ROOT/'data/w33_pass11471_11475_frames_currents_matching.json').read_text())['frame']['albert_bridge']
        raw=bridge['native_from_clock_basis']
        T=np.array(raw['real'])+1j*np.array(raw['imag'])
        G=T.conj().T@T
        zeta=np.exp(2j*np.pi/18)
        for name,packet in self.data['clock_generators'].items():
            W=np.zeros((27,27),complex)
            for row in packet['entries']:
                W[row['row'],row['column']]=sum((a+1j*b)*zeta**k for k,a,b in row['numerator_terms'])/row['denominator']
            perm,phase=self.data['native_27_generators'][name]
            U=np.zeros((27,27),complex)
            for j in range(27):U[perm[j],j]=zeta**phase[j]
            self.assertLess(np.max(abs(T@W-U@T)),2e-12)
            self.assertLess(np.max(abs(W.conj().T@G@W-G)),2e-11)

    def test_G2_roots_and_mixed_module(self):
        g=self.data['native_E6_invariants']
        self.assertEqual((g['invariant_E6_dimension'],g['Cartan_dimension']),(14,2))
        self.assertEqual(len(g['root_weights']),12)
        lengths={s.Rational(k):v for k,v in g['root_length_squared_counts'].items()}
        self.assertEqual(lengths,{s.Rational(1,12):6,s.Rational(1,4):6})
        self.assertEqual(self.data['native_mixed_81_invariants']['G2_singlets'],1)
        self.assertEqual(self.data['native_mixed_81_invariants']['cyclotomic_rank_lower_bound_mod19'],7)

    def test_integral_extension_distinguishes_split_control(self):
        for k in (1,-1,2,4):
            M=s.Matrix([[3,0],[k,3]])
            snf=smith_normal_form(M,domain=s.ZZ)
            self.assertEqual(sorted(abs(snf[j,j]) for j in range(2)),[1,9])
        split=smith_normal_form(s.Matrix([[3,0],[0,3]]),domain=s.ZZ)
        self.assertEqual(sorted(abs(split[j,j]) for j in range(2)),[3,3])
        d=self.data['Cfield_topology']
        self.assertEqual((d['p1_TY_mod9'],d['spin_lambda_p1_over2_mod9']),(6,3))
        self.assertEqual((2*d['spin_lambda_p1_over2_mod9'])%9,d['p1_TY_mod9'])

    def test_generic_compact_so8_pair_leaves_four_Cartans(self):
        basis=[]
        for i in range(8):
            for j in range(i+1,8):
                b=s.zeros(8);b[i,j]=1;b[j,i]=-1;basis.append(b)
        def cartan(values):
            A=s.zeros(8)
            for k,v in enumerate(values):A[2*k,2*k+1]=v;A[2*k+1,2*k]=-v
            return A
        A=cartan((1,3,7,11));B=cartan((2,5,13,17))
        equations=s.Matrix.hstack(*(s.Matrix.vstack((A*b-b*A).reshape(64,1),(B*b-b*B).reshape(64,1)) for b in basis))
        self.assertEqual(len(equations.nullspace()),4)
        self.assertEqual(self.data['flat_deformation_gate']['rank'],4+2)

    def test_color_and_weak_cannot_both_embed(self):
        g=self.data['SM_subalgebra_gate']
        self.assertEqual(g['minimal_faithful_real_dimension_for_su3_plus_su2'],9)
        self.assertEqual(g['minimal_real_irreducible_dimension_nontrivial_on_both_factors'],12)
        self.assertTrue(all(r['active_factor_mask']!=3 for r in g['real_irreducibles_through_dimension8']))
        self.assertFalse(g['SM_gauge_algebra_embeds_in_this_centralizer'])


if __name__=='__main__':unittest.main()
