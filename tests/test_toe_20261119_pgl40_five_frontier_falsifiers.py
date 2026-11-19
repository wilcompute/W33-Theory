"""Independent regression and falsifier tests for the 2026-11-19 six-frontier packet."""
import math
import pathlib
import sys
import unittest
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_pgl40_five_frontier_falsifiers as f
import toe_20261119_w33_40_qutrit_css as c


class PGL40Frontiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p,cls.A,cls.HX,cls.HZ=c.checks()

    def test_one_loop_SUSY_QCD_Nf_border(self):
        v=f.gauge_beta_audit()
        self.assertEqual([a["one_loop_b0"] for a in v["models"]],[0,-1])
        self.assertIn("does not imply",v["caution"])

    def test_nonflat_torus_Dirac_gap(self):
        v=f.charged_dirac_pulledback_flux()
        self.assertEqual(len(v["tested_compatible_U1_fluxes"]),4)
        self.assertTrue(all(a["product_Y7_untwisted_direction_gap_lower_bound"]==2.5
                            for a in v["tested_compatible_U1_fluxes"]))
        self.assertEqual(v["tested_compatible_U1_fluxes"][1]["T2_Dirac_zero_mode_number"],9)

    def test_four_MUB_exact_projector_and_shots(self):
        v=f.qutrit_mub_witness()
        self.assertEqual(v["total_detection_shots"],332)
        self.assertEqual(v["shots_per_basis"],83)
        self.assertGreater(v["launched_pulses_for_99pct_to_collect_shots_if_independent_eta0.7"],400)

    def test_three_spatial_cycle_refinement(self):
        v=f.continuum_refinement()
        errs=[r["relative_error"] for r in v["cycle_refinement_residuals"]]
        self.assertTrue(all(a>b for a,b in zip(errs,errs[1:])))
        self.assertEqual(v["base_fiber_Laplacian_spectrum"],{"0":1,"10":24,"16":15})

    def test_X_and_Z_lookup_are_injective(self):
        dx=f.build_decoder(self.HZ,1)
        dz=f.build_decoder(self.HX,2)
        self.assertEqual(len(dx),81)
        self.assertEqual(len(dz),3201)
        self.assertEqual(len(set(dx.keys())),81)
        self.assertEqual(len(set(dz.keys())),3201)

    def test_XZ_errors_decode_even_if_overlapping(self):
        self.assertEqual(f.syndrome_key([-1,0,1]),bytes([2,0,1]))
        dx=f.build_decoder(self.HZ,1)
        dz=f.build_decoder(self.HX,2)
        x=np.zeros(40,dtype=np.int8);z=np.zeros(40,dtype=np.int8)
        x[3]=2;z[3]=1;z[21]=2
        self.assertTrue(np.array_equal(dx[f.syndrome_key(self.HZ@x)],x))
        self.assertTrue(np.array_equal(dz[f.syndrome_key(self.HX@z)],z))

    def test_guaranteed_success_vs_noise(self):
        probabilities=[f.decoder_guaranteed_probability(p) for p in (0.,.001,.01,.02,.05,.10)]
        self.assertAlmostEqual(probabilities[0],1)
        self.assertTrue(all(0<=p<=1 for p in probabilities))
        self.assertTrue(all(a>=b for a,b in zip(probabilities,probabilities[1:])))

    def test_all_13_PGL_generators_preserve_stabilizer_spaces(self):
        pts,_,hx,hz=self.p,self.A,self.HX,self.HZ
        base_x=c.rref_mod3(hx);base_z=c.rref_mod3(hz)
        tested=0
        for i in range(4):
            for j in range(4):
                if i==j:continue
                g=np.eye(4,dtype=int);g[i,j]=1
                perm=f.projective_permutation(g,pts)
                self.assertTrue(np.array_equal(c.rref_mod3(hx[:,perm]),base_x))
                self.assertTrue(np.array_equal(c.rref_mod3(hz[:,perm]),base_z))
                tested+=1
        g=np.diag([2,1,1,1])
        perm=f.projective_permutation(g,pts)
        self.assertTrue(np.array_equal(c.rref_mod3(hx[:,perm]),base_x))
        self.assertTrue(np.array_equal(c.rref_mod3(hz[:,perm]),base_z))
        self.assertEqual(tested+1,13)

    def test_PGL_logical_transvection_nontrivial(self):
        report=f.pgl_code_symmetries()
        self.assertEqual(report["group_order"],12130560)
        self.assertEqual(report["ratio_to_fixed_W33_PSp4"],468)
        self.assertEqual(report["logical_dimension"],19)
        self.assertEqual(report["order_three_transvection_logical_order"],3)
        self.assertEqual(report["transvection_rank_T_minus_identity"],10)
        self.assertEqual(report["transvection_rank_square_T_minus_identity"],3)
        self.assertEqual(report["unipotent_logical_Jordan_block_multiplicities"],
                         {"size1":2,"size2":4,"size3":3})

    def test_uniform_T9_transversal_not_logical(self):
        report=f.pgl_code_symmetries()
        self.assertFalse(report["uniform_ninth_root_T_gate_is_transversal_logical"])
        self.assertEqual(report["relative_T9_phase_exponent_mod9"],4)
        # The X-stabilizer row h has 13 ones. Its phase differs from
        # the all-zero codeword by zeta_9^13, so +1 X-stabilizers fail.
        h=self.HX[0]
        self.assertEqual(int(np.sum(h**3))%9,4)

    def test_packet_returns_all_six_certificates(self):
        result=f.certify()
        self.assertEqual(len(result)-1,6)
        self.assertTrue(all("PASS" in v["status"] for v in
                            list(result.values())[1:]))

if __name__=="__main__":
    unittest.main()
