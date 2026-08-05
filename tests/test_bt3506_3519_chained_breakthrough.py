import json
from pathlib import Path

from analysis.bt3506_3519_chained_breakthrough import build_certificate


def test_chained_breakthrough_matches_frozen_certificate():
    generated = build_certificate()
    frozen = json.loads(
        Path("data/PART_BT3506_BT3519_CHAINED_BREAKTHROUGH_results.json").read_text()
    )
    assert generated == frozen
    assert generated["status"] == "PASS_7_FRONTS"
    assert generated["semantic_sha256"] == (
        "7ad66eec9cbb1b3f207eb4215a348cb9a63e0be9ab7876e53209dbed3099a13f"
    )
    assert generated["characteristic_three_projector"]["projector_rank"] == 81
    assert generated["five_channel_hardware"]["minimum_binary_operations"] == 5
    assert generated["tomotope_lift"]["eight_cell_double_cover_solutions"] == 0
