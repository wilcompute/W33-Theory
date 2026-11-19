"""Independent regressions: synthetic causet -> torus -> U1 flux -> overlap index.

All topology is reconstructed from a provided binary incidence. U1 gauge field,
oriented 2D Clifford operator and Wilson regulator remain explicitly SUPPLIED.
"""
from __future__ import annotations
import pathlib,sys,unittest,math
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_torus_overlap_flux_v9 as m
import toe_20261105_overlap_flux_chirality_index as old

class OrderRecoveredTorusOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=m.main()
        cls.cases=cls.report["cases"]
        cls.bad=cls.report["orientation_regulator_noise_obstructions"]

    def test_all_five_grid_sizes_executed(self):
        self.assertEqual([row["n"] for row in self.cases],[5,6,7,8,9])

    def test_both_independent_homologies_equal_torus(self):
        for row in self.cases:
            self.assertEqual(row["nerve_homology"]["bettis_0_1_2"],[1,2,1])
            self.assertEqual(row["cellular_betti"],[1,2,1])

    def test_causal_incidence_has_degree_four_in_both_layers(self):
        for n in (5,6,7,8,9):
            R=m.torus_incidence(n)
            self.assertTrue(np.all(R.sum(axis=0)==4))
            self.assertTrue(np.all(R.sum(axis=1)==4))

    def test_nerve_maximal_simplex_has_four_vertices(self):
        for row in self.cases:
            n=row["n"]
            self.assertEqual(row["nerve_homology"]["simplex_counts_0_to_3"],
                             [n*n,4*n*n,4*n*n,n*n])

    def test_nerve_boundary_ranks_on_5x5(self):
        self.assertEqual(self.cases[0]["nerve_homology"]["boundary_ranks_1_to_3"],
                         [24,74,25])

    def test_nerves_have_h1_two_for_all_sizes(self):
        self.assertTrue(all(row["nerve_homology"]["bettis_0_1_2"][1]==2 for row in self.cases))

    def test_Euler_characteristic_zero_and_cell_counts(self):
        for row in self.cases:
            n=row["n"];N=n*n
            self.assertEqual(row["V_E_F"],[N,2*N,N])
            self.assertEqual(row["Euler"],0)

    def test_cell_boundary_ranks_expected_torus(self):
        for row in self.cases:
            N=row["n"]**2
            self.assertEqual(row["cellular_boundary_ranks"],[N-1,N-1])

    def test_recovered_graph_is_four_regular(self):
        rec=m.recover_torus(m.torus_incidence(5))
        self.assertTrue(all(len(adjs)==4 for adjs in rec["graph"].values()))

    def test_each_recovered_square_is_an_induced_four_cycle(self):
        rec=m.recover_torus(m.torus_incidence(5))
        G=rec["graph"]
        for face in rec["faces"]:
            self.assertEqual(len(set(face)),4)
            for a,b in zip(face,face[1:]+face[:1]):
                self.assertIn(b,G[a])
            self.assertNotIn(face[2],G[face[0]])
            self.assertNotIn(face[3],G[face[1]])

    def test_every_edge_meets_two_square_faces(self):
        rec=m.recover_torus(m.torus_incidence(5))
        counts={}
        for face in rec["faces"]:
            for a,b in zip(face,face[1:]+face[:1]):
                key=tuple(sorted((a,b)))
                counts[key]=counts.get(key,0)+1
        self.assertEqual(len(counts),50)
        self.assertTrue(all(c==2 for c in counts.values()))

    def test_coordinate_recovery_covers_each_vertex_once(self):
        for n in (5,7):
            rec=m.recover_torus(m.torus_incidence(n))
            self.assertEqual(len(rec["coordinate"]),n*n)
            self.assertEqual(len(set(rec["coordinate"].values())),n*n)

    def test_coordinate_edges_match_recovered_graph_not_supplied_list(self):
        rec=m.recover_torus(m.torus_incidence(5))
        inv=rec["inverse_coordinate"];G=rec["graph"];n=rec["n"]
        for (x,y),v in inv.items():
            self.assertEqual(G[v],{inv[((x+dx)%n,(y+dy)%n)]
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))})

    def test_flux_is_uniform_in_all_plaquettes(self):
        rec=m.recover_torus(m.torus_incidence(7))
        for Q in (-1,0,1):
            _,_,f=m.gauge_shifts(rec,Q)
            self.assertEqual(f["recovered_flux_Q"],Q)
            self.assertAlmostEqual(f["min_plaquette_angle"],2*math.pi*Q/49,places=12)
            self.assertAlmostEqual(f["max_plaquette_angle"],2*math.pi*Q/49,places=12)

    def test_overlap_index_matches_flux_for_all_five_sizes(self):
        for row in self.cases:
            self.assertEqual([x["index"] for x in row["flux_cases"]],[1,0,-1])

    def test_zero_flux_spectra_have_zero_index(self):
        for row in self.cases:
            self.assertEqual(row["flux_cases"][1]["input_flux_Q"],0)
            self.assertEqual(row["flux_cases"][1]["index"],0)

    def test_kernel_is_gapped_and_Hermitian(self):
        for row in self.cases:
            for x in row["flux_cases"]:
                self.assertGreater(x["Hermitian_kernel_gap"],1e-6)
                self.assertLess(x["Hermitian_residual"],1e-10)

    def test_Ginsparg_Wilson_relation_on_actual_inferred_graph(self):
        obj=self.cases[0]["flux_cases"][2]
        self.assertLess(obj["GW_Frobenius_residual"],1e-10)

    def test_nonzero_index_gives_at_least_one_overlap_zero_mode(self):
        obj=self.cases[0]["flux_cases"][2]
        self.assertGreaterEqual(obj["zero_mode_count"],1)

    def test_independent_prior_Wilson_builder_agrees_on_index_sign(self):
        for Q in (-1,0,1):
            prior=old.check(5,Q,1.,compute_overlap=(Q==1))
            rec=next(x for x in self.cases[0]["flux_cases"] if x["input_flux_Q"]==Q)
            self.assertEqual(prior["index_minus_half_eta"],rec["index"])

    def test_regulator_mass_branch_changes_chiral_index_without_order_change(self):
        regs=self.bad["regulator_mass_branch_and_external_flux_scan"]
        for row in regs:
            q=row["external_flux"]
            self.assertEqual([x["index"] for x in row["two_mass_branches"]],[-q,q])

    def test_quantized_flux_plus_or_minus_two_supported_on_reconstructed_graph(self):
        data=self.bad["regulator_mass_branch_and_external_flux_scan"]
        self.assertEqual(data[0]["two_mass_branches"][0]["index"],2)
        self.assertEqual(data[-1]["two_mass_branches"][0]["index"],-2)

    def test_same_causal_relation_can_give_multiple_indices(self):
        regs=self.bad["regulator_mass_branch_and_external_flux_scan"]
        self.assertEqual(len(set(r["two_mass_branches"][0]["index"] for r in regs)),5)

    def test_independent_antichain_and_witness_relabelings_preserve_homology_and_index(self):
        r=self.report["independent_site_relabeling"]
        self.assertTrue(r["independent_random_antichain_and_witness_relabeling"])
        self.assertEqual(r["new_inferred_cellular_betti"],[1,2,1])
        self.assertEqual(r["after_relabel_flux_and_index"]["index"],-1)

    def test_local_U1_frame_gauge_covariance(self):
        r=self.report["local_U1_frame_covariance"]
        self.assertEqual(r["before"]["index"],r["after"]["index"])
        self.assertAlmostEqual(r["before"]["Hermitian_kernel_gap"],
                               r["after"]["Hermitian_kernel_gap"],delta=1e-10)
        self.assertLess(r["after"]["GW_Frobenius_residual"],1e-10)

    def test_causal_relation_has_orientation_reversing_automorphism(self):
        self.assertTrue(self.bad["reflection_swap_xy_is_causal_relation_automorphism"])
        self.assertEqual(self.bad["spatial_orientation_reversal_determinant"],-1)
        self.assertFalse(self.bad["can_recover_preferred_oriented_Chern_sign_from_order_alone"])

    def test_reflection_is_automorphism_independently_by_matrix_permutation(self):
        n=7;R=m.torus_incidence(n)
        perm=np.array([(j%n)*n+(j//n) for j in range(n*n)])
        self.assertTrue(np.array_equal(R,R[np.ix_(perm,perm)]))

    def test_all_100_single_incidence_deletions_destroy_minimal_nerve_b2(self):
        self.assertEqual(self.bad["independent_single_incidence_deletions_tested"],100)
        self.assertEqual(self.bad["single_deletions_destroying_B2"],100)
        self.assertEqual(self.bad["single_deletion_result_Betti_histogram"],{"(1, 2, 0)":100})

    def test_one_bad_causal_relation_falsifies_exact_torus_nerve(self):
        R=m.torus_incidence(5)
        R[0,0]=0
        self.assertEqual(m.dowker_homology(R)["bettis_0_1_2"],[1,2,0])
        with self.assertRaises(ValueError):
            m.recover_torus(R)

    def test_rank_mod2_over_64_bits_does_not_overflow(self):
        cols=[(1<<75)^(1<<4),(1<<74)^(1<<4),(1<<75)^(1<<74)]
        self.assertEqual(m.rank2(cols),2)

    def test_topology_alone_does_not_derive_3plus1_chiral_SM(self):
        self.assertFalse(self.report["TOE_solved"])
        self.assertFalse(self.report["causal_3plus1_Dirac_derived"])
        self.assertIn("topological U1 gauge flux Q",self.report["supplied_inputs"])
        self.assertIn("Wilson regulator mass branch and sign",self.report["supplied_inputs"])

    def test_four_torus_spin_structures_exist_but_not_selected(self):
        r=self.report["flat_Z2_spin_structure_spectral_controls"]
        self.assertEqual(r["spin_structure_torsor_size"],"2^b1=4 for b1(T2;Z2)=2")
        self.assertTrue(r["spin_choices_are_supplied_as_flat_Z2_boundary_links"])
        self.assertEqual(len(r["flux_and_spin_twists"][0]["four_spin_twists"]),4)

    def test_no_flux_spin_boundary_conditions_change_zero_modes_not_index(self):
        r=self.report["flat_Z2_spin_structure_spectral_controls"]["flux_and_spin_twists"][0]
        self.assertEqual(r["flux_Q"],0)
        self.assertEqual([x["index"] for x in r["four_spin_twists"]],[0,0,0,0])
        self.assertEqual([x["overlap_zero_modes"] for x in r["four_spin_twists"]],[2,0,0,0])

    def test_unit_flux_index_independent_of_all_four_spin_structures(self):
        r=self.report["flat_Z2_spin_structure_spectral_controls"]["flux_and_spin_twists"][1]
        self.assertEqual(r["flux_Q"],1)
        self.assertEqual([x["index"] for x in r["four_spin_twists"]],[-1,-1,-1,-1])
        self.assertEqual([x["overlap_zero_modes"] for x in r["four_spin_twists"]],[1,1,1,1])

    def test_spin_twist_GW_identity_all_eight_backgrounds(self):
        r=self.report["flat_Z2_spin_structure_spectral_controls"]
        for flux in r["flux_and_spin_twists"]:
            for row in flux["four_spin_twists"]:
                self.assertLess(row["GW_residual"],1e-10)

    def test_redundancy_benchmark_runs_200_trials_per_replication(self):
        rows=self.report["engineered_redundancy_noise_control"]["results"]
        self.assertEqual([x["replicas_per_antichain_cell_k"] for x in rows],[1,2,4])
        self.assertTrue(all(x["trials"]==200 for x in rows))

    def test_redundancy_analytic_sufficient_event_probability(self):
        for row in self.report["engineered_redundancy_noise_control"]["results"]:
            k=row["replicas_per_antichain_cell_k"];p=.05
            bound=(1-(1-(1-p)**4)**k)**25
            self.assertAlmostEqual(row["analytical_sufficient_event_probability"],bound,places=14)

    def test_engineered_redundancy_improves_topology_sufficient_event_probability(self):
        rows=self.report["engineered_redundancy_noise_control"]["results"]
        measured=[x["empirical_full_torus_nerve_fraction"] for x in rows]
        self.assertLess(measured[0],measured[1])
        self.assertLess(measured[1],measured[2])
        self.assertLess(measured[0],.05)
        self.assertGreater(measured[-1],.95)

    def test_homology_recovered_not_sufficient_for_local_Dirac_graph(self):
        rows=self.report["engineered_redundancy_noise_control"]["results"]
        middle=rows[1]
        self.assertGreater(middle["empirical_full_torus_nerve_fraction"],.4)
        self.assertLess(middle["empirical_top4_weighted_graph_exact_fraction"],.2)

    def test_redundancy_does_not_create_physical_spacetime(self):
        r=self.report["engineered_redundancy_noise_control"]
        self.assertIn("engineered",r["crucial_limitation"])
        self.assertFalse(self.report["causal_3plus1_Dirac_derived"])

if __name__=="__main__":unittest.main()
