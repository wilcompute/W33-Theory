"""Exact projective realization plus an independent dense seed check."""
import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261119_h27_projective_period_index as m


class ProjectivePeriodIndexTests(unittest.TestCase):
    def test_dense_seed_commutators(self):
        w=np.exp(2j*np.pi/3)
        X=np.roll(np.eye(3,dtype=complex),1,axis=0)
        D=np.diag([1,1,w])
        bracket=lambda a,b:a@b@a.conj().T@b.conj().T
        C=bracket(X,D)
        self.assertTrue(np.allclose(C,np.diag([w,1,w*w])))
        self.assertTrue(np.allclose(bracket(X,C),w*np.eye(3)))
        self.assertTrue(np.allclose(bracket(D,C),np.eye(3)))

    def test_all_eight_exact_projective_cocycles(self):
        pairs=set()
        from itertools import product
        for a,b in product(range(3),repeat=2):
            if (a,b)==(0,0):continue
            p,q,r,s=next((p,q,r,s) for p,q,r,s in product(range(-2,3),repeat=4)
                         if p*s-q*r==1 and p%3==a and q%3==b)
            U=m.mul(m.power(m.X,p),m.power(m.D,r))
            V=m.mul(m.power(m.X,q),m.power(m.D,s))
            cert=m.certificate(U,V)
            pair=cert['torsion_cycle_pairing_exponents_mod3']
            self.assertEqual(pair,(a,b))
            self.assertEqual(cert['projective_product_checks'],729)
            self.assertEqual(cert['scalar_cocycle_checks'],19683)
            self.assertEqual(cert['projective_image_order'],27)
            self.assertEqual(cert['unitary_lift_group_order'],81)
            self.assertEqual(cert['E8_compensated_descent']['exact_unprojectivized_product_checks'],729)
            self.assertEqual(cert['E8_compensated_descent']['finite_E8_holonomy_image_order'],27)
            self.assertEqual(cert['E8_compensated_descent']['E8_parallel_adjoint_invariant_dimension'],30)
            pairs.add(pair)
        self.assertEqual(len(pairs),8)


if __name__=='__main__':unittest.main()
