from scripts.w33_h4_branch_selection_search import build_branch_selection_search_summary


def test_branch_selection_search_builds_the_exact_cover_model() -> None:
    summary = build_branch_selection_search_summary()

    assert summary["branch_model"] == {
        "base_carrier": "ordered_nonlocal_2_paths",
        "consistency_rule": "quadrangle_consistent_branch_choice",
        "ordered_path_count": 4320,
        "nonlocal_quadrangle_count": 1620,
        "target_cover_size": 540,
    }
    assert summary["incidence"] == {
        "ordered_path_completion_degree_distribution": {3: 4320},
        "quadrangle_ordered_path_degree_distribution": {8: 1620},
    }


def test_branch_selection_exact_cover_search_has_no_solution() -> None:
    summary = build_branch_selection_search_summary()
    search = summary["search"]

    assert search["found_exact_cover"] is False
    assert search["selected_quadrangle_count"] is None
    assert search["visited_search_nodes"] == 1106


def test_branch_selection_theorem_records_the_stronger_no_go() -> None:
    summary = build_branch_selection_search_summary()

    assert summary["theorem"] == {
        "the_strongest_quadrangle_consistent_global_branch_model_is_an_exact_cover_problem": True,
        "that_exact_cover_model_has_no_solution": True,
        "therefore_the_missing_selector_is_not_just_a_global_choice_of_540_nonlocal_quadrangles": True,
        "interpretation": (
            "A coherent branch law cannot be realized as a bare exact packet of 540 "
            "nonlocal quadrangles covering the 4320 ordered paths once each. The "
            "ordered-path S3 carrier needs additional cocycle/holonomy data beyond "
            "a raw quadrangle subset."
        ),
    }
    assert all(summary["checks"].values())