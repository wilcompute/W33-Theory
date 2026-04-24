"""Supplement L - internal H4 shadow from W(3,3) line matchings."""

from scripts.w33_h4_line_matching_shadow import build_h4_shadow, perfect_matchings


def test_k4_has_three_perfect_matchings():
    line = (0, 1, 2, 3)
    matchings = perfect_matchings(line)
    assert len(matchings) == 3
    assert len(set(matchings)) == 3
    assert {edge for m in matchings for edge in m} == {
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    }


class TestL1LineMatchingCounts:
    @classmethod
    def setup_class(cls):
        cls.summary = build_h4_shadow()

    def test_w33_has_40_lines(self):
        assert self.summary["constants"]["w33_lines"] == 40
        assert self.summary["checks"]["line_count_is_40"]

    def test_w33_has_240_edges(self):
        assert self.summary["constants"]["w33_edges"] == 240
        assert self.summary["checks"]["edge_count_is_240"]

    def test_line_matching_state_count_is_120(self):
        assert self.summary["constants"]["line_matchings"] == 120
        assert self.summary["checks"]["state_count_is_120"]

    def test_three_states_per_line(self):
        assert self.summary["checks"]["three_states_per_line"]

    def test_two_edges_per_state(self):
        assert self.summary["checks"]["two_edges_per_state"]


class TestL2CoveringProperties:
    @classmethod
    def setup_class(cls):
        cls.summary = build_h4_shadow()

    def test_lines_cover_edges_once(self):
        assert self.summary["checks"]["six_edges_per_line"]
        assert self.summary["checks"]["line_edges_cover_w33_edges"]

    def test_matching_states_cover_edges_once(self):
        assert self.summary["checks"]["state_edges_cover_w33_edges"]
        assert self.summary["checks"]["each_edge_in_one_state"]

    def test_edge_to_state_is_total(self):
        assert len(self.summary["edge_to_state"]) == 240

    def test_states_times_two_recovers_edges(self):
        c = self.summary["constants"]
        assert c["states_times_two"] == c["w33_edges"] == 240

    def test_lines_times_q_recovers_h4_count(self):
        c = self.summary["constants"]
        assert c["lines_times_q"] == c["h4_root_count"] == 120


class TestL3PointIncidenceUniformity:
    @classmethod
    def setup_class(cls):
        cls.summary = build_h4_shadow()

    def test_four_lines_per_point(self):
        assert self.summary["checks"]["four_lines_per_point"]

    def test_twelve_states_per_point(self):
        assert self.summary["checks"]["twelve_states_per_point"]

    def test_state_uses_four_distinct_points(self):
        for state in self.summary["states"]:
            endpoints = {x for edge in state["matching"] for x in edge}
            assert len(endpoints) == 4
            assert tuple(sorted(endpoints)) == tuple(state["line"])


class TestL4E8H4Interpretation:
    @classmethod
    def setup_class(cls):
        cls.summary = build_h4_shadow()

    def test_internal_projection_theorem(self):
        assert self.summary["theorem"]["w33_edges_are_a_two_cover_of_line_matching_states"]

    def test_h4_root_count_matched(self):
        assert self.summary["theorem"]["line_matching_states_match_h4_root_count"]

    def test_e8_root_count_matched(self):
        assert self.summary["theorem"]["w33_edges_match_e8_root_count"]

    def test_projection_formula(self):
        assert (
            self.summary["theorem"]["internal_projection_formula"]
            == "40 lines * 3 matchings/line * 2 edges/matching = 240"
        )

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())
