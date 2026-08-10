import json
from pathlib import Path

from analysis.bt3729_3742_five_front_website_restore import build_certificate


def test_pass3729_3742_certificate_matches_frozen():
    generated = build_certificate()
    frozen = json.loads(
        Path("data/PART_BT3729_BT3742_FIVE_FRONT_WEBSITE_RESTORE_results.json").read_text(encoding="utf-8")
    )
    assert json.loads(json.dumps(generated)) == frozen
    assert generated["semantic_sha256"] == (
        "c6e5e73fb5a18d9add4c1643d52df31413280b0e5cd157294ca686f8df32a299"
    )
    assert generated["website_restore"]["restored_index_blob"] == (
        "41a8d733f42da18282fa276f5d2fa82bac7516f6"
    )
    assert generated["fronts"]["cubic_transversal"]["live_interval"] == [106, 178]
    assert generated["fronts"]["tomotope_rank_four"]["completion_grid_orders"] == [
        [96, 96, 192], [192, 96, 96], [96, 192, 96]
    ]
    assert generated["fronts"]["modular_159_filtration"]["middle30_exact_sequence"] == (
        "0 -> 1+5+10 -> M30 -> 14 -> 0"
    )
    assert generated["fronts"]["gewirtz_rounding"]["gewirtz_srg_candidates"] == 0
