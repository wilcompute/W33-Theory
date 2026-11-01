import pathlib
import sys
import unittest
import itertools
import numpy as np

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'analysis'))
import w33_20261031_chiral_tetrahedron_strange_bridge as T


class ChiralTetrahedronBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=T.build()

    def test_exact_cyclic_completion_faces(self):
        self.assertEqual(len(self.d['oriented_tetrahedra']),810)
        for f in T.faces(self.d['oriented_tetrahedra'][0]):
            self.assertEqual(T.exact_trace(f),(1,2))
        self.assertNotEqual(T.exact_trace((0,0,0)),(1,2))

    def test_positive_quantum_gap_and_common_kernel(self):
        labels=self.d['canonical_native_ticks']
        H=sum(T.PI[a] for a in labels)/2
        self.assertTrue(np.allclose(np.linalg.eigvalsh(H),[0]*3+[1]*6))
        Q=np.eye(9)-H
        for a in labels:self.assertLess(np.linalg.norm(T.PI[a]@Q),1e-12)

    def test_ninety_sic_families_match_existing_factorisations(self):
        self.assertEqual(len(self.d['local_SIC_families']),90)
        self.assertTrue(all(len(f['tetrahedron_indices'])==9 for f in self.d['local_SIC_families']))
        self.assertEqual(self.d['existing_factorisations_exactly_matched'],45)
        self.assertEqual(sorted(self.d['native_to_old_point_map']),list(range(40)))

    def test_jones_recursion_gives_filtered_complement(self):
        path=[0,4,2]
        f=np.eye(9,dtype=complex)
        for n,p in enumerate(path,1):
            ratio=np.sin(n*np.pi/6)/np.sin((n+1)*np.pi/6)
            f=f-ratio*np.sqrt(3)*f@T.PI[3*p]@f
        Q=np.eye(9)-sum(T.PI[a] for a in self.d['canonical_native_ticks'])/2
        R=np.kron(np.diag([1.,0.,0.]),np.eye(3))
        self.assertLess(np.linalg.norm(f-R@Q),1e-12)
        self.assertAlmostEqual(self.d['normalized_complement_Wigner']['L1'],5/3)

    def test_tetrahedron_saturates_every_energy_bound_and_reverses_orientation(self):
        t=self.d['oriented_tetrahedra'][0];opposite=(t[1],t[0],t[2],t[3])
        for K,lam in ((2.,.2),(2.,-1.),(3.,2.)):
            labels=t if lam>0 else opposite
            pair=2-4*K/3
            energy=sum(pair for _ in itertools.combinations(labels,2))
            energy-=lam*sum(np.trace(T.PI[a]@T.PI[b]@T.PI[c]).imag for a,b,c in T.faces(labels))
            self.assertAlmostEqual(energy,6*pair-4*abs(lam)/np.sqrt(3))
        self.assertTrue(np.allclose(sum(T.PI[a] for a in t),sum(T.PI[a] for a in opposite)))

    def test_second_complex_basis_preserves_complement_and_loops(self):
        rng=np.random.default_rng(8109720)
        U=np.linalg.qr(rng.normal(size=(9,9))+1j*rng.normal(size=(9,9)))[0]
        t=self.d['oriented_tetrahedra'][0]
        moved={a:U@T.PI[a]@U.conj().T for a in t}
        Q=np.eye(9)-sum(T.PI[a] for a in t)/2
        self.assertLess(np.linalg.norm(np.eye(9)-sum(moved.values())/2-U@Q@U.conj().T),1e-12)
        for a,b,c in T.faces(t):
            self.assertAlmostEqual(np.trace(moved[a]@moved[b]@moved[c]).imag,1/np.sqrt(3))


if __name__=='__main__':unittest.main()
