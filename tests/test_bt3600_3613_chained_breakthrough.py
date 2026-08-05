import json
from pathlib import Path

from analysis.bt3600_3613_chained_breakthrough import build_certificate


def test_chained_certificate_matches_frozen():
    generated = build_certificate()
    frozen = json.loads(
        Path("data/PART_BT3600_BT3613_CHAINED_BREAKTHROUGH_results.json").read_text()
    )
    assert generated == frozen
    assert generated["semantic_sha256"] == (
        "a08844aa7ec3a6be578dece00e455c1868ad8b4c833d912ebe02b7f014077f17"
    )
    assert generated["theorems"]["characteristic_three_projector"]["projector_rank"] == 81
    assert generated["theorems"]["five_channel_hardware"]["minimum_binary_operations"] == 5
    assert generated["theorems"]["tomotope_lift"]["eight_cell_double_cover_solutions"] == 0
