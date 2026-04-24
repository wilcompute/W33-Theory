"""Supplement M - no full PSp(4,3)-invariant 600-cell skeleton on M_120."""

from scripts.w33_h4_orbital_no_go import compute_pair_orbitals


class TestM1PairOrbitals:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_state_count(self):
        assert self.summary["checks"]["state_count_is_120"]

    def test_transvection_generator_count(self):
        assert self.summary["checks"]["generator_count_is_40"]

    def test_pair_orbital_count(self):
        assert self.summary["checks"]["pair_orbital_count_is_4"]

    def test_pair_sizes_partition_all_pairs(self):
        assert self.summary["checks"]["pair_sizes_sum_to_all_pairs"]

    def test_orbital_degrees(self):
        assert self.summary["orbital_degrees"] == [2, 27, 36, 54]


class TestM2OrbitalGeometry:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_same_line_orbital(self):
        same = self.summary["orbitals"][0]
        assert same["degree"] == 2
        assert same["same_line_pairs"] == 120
        assert same["intersecting_line_pairs"] == 0
        assert same["disjoint_line_pairs"] == 0

    def test_intersecting_line_orbital(self):
        crossing = self.summary["orbitals"][2]
        assert crossing["degree"] == 36
        assert crossing["same_line_pairs"] == 0
        assert crossing["intersecting_line_pairs"] == 2160
        assert crossing["disjoint_line_pairs"] == 0

    def test_disjoint_line_orbitals(self):
        disjoint_degrees = [
            row["degree"]
            for row in self.summary["orbitals"]
            if row["disjoint_line_pairs"] > 0
        ]
        assert disjoint_degrees == [27, 54]


class TestM3NoGo:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_possible_invariant_degrees(self):
        assert self.summary["possible_invariant_degrees"] == [
            0,
            2,
            27,
            29,
            36,
            38,
            54,
            56,
            63,
            65,
            81,
            83,
            90,
            92,
            117,
            119,
        ]

    def test_no_degree_12_relation(self):
        assert self.summary["checks"]["no_invariant_degree_12_relation"]
        assert 12 not in self.summary["possible_invariant_degrees"]

    def test_no_full_symmetry_600_cell_skeleton(self):
        assert self.summary["theorem"]["no_full_psp43_invariant_600_cell_skeleton_on_M120"]

    def test_next_structure_requires_symmetry_breaking(self):
        assert "break PSp(4,3)" in self.summary["theorem"]["required_next_structure"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())
