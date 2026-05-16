"""Part DCCLXVII -- axis-syndrome nilpotent / octahedral codec tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge import (  # noqa: E402
    DIRECTED,
    H1,
    KLM,
    OUT_PATH,
    block_nilpotent,
    build_bridge,
    directed_octahedral_turns,
    local_axis_syndrome_basis,
    nilpotent_data,
    nilpotent_increment,
    octahedral_turn_data,
    rank_mod3,
    write_bridge,
)


def test_summary_connects_12_24_480_960_and_162() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["signed_axis_count"] == 6
    assert summary["local_axis_syndrome_slots"] == 12
    assert summary["local_directed_turns"] == 24
    assert summary["global_fusion_slots"] == DIRECTED == 480
    assert summary["global_klm_primitives"] == KLM == 960
    assert summary["global_extension_dimension"] == 162
    assert summary["global_nilpotent_rank"] == H1 == 81
    assert summary["all_identities_hold"] is True


def test_local_basis_is_signed_axis_times_two_state_extension() -> None:
    basis = local_axis_syndrome_basis()
    labels = {entry["label"] for entry in basis}

    assert len(basis) == 12
    assert "accepted:+B23" in labels
    assert "return:-B12" in labels
    assert {entry["role"] for entry in basis} == {"accepted", "return"}
    assert {entry["axis"] for entry in basis} == {"B23", "B31", "B12"}
    assert {entry["sign"] for entry in basis} == {1, -1}


def test_directed_turns_are_the_klm_rail_cover_of_octahedral_edges() -> None:
    turns = directed_octahedral_turns()
    data = octahedral_turn_data()

    assert len(turns) == 24
    assert data["undirected_edge_count"] == 12
    assert data["each_undirected_edge_has_two_directions"] is True
    assert all(len(turn["edge_key"]) == 2 for turn in turns)
    assert {turn["role"] for turn in turns} == {"accepted", "return"}
    assert {turn["klm_rail"] for turn in turns} == {0, 1}


def test_each_local_slot_resolves_to_two_directed_turns() -> None:
    turns = directed_octahedral_turns()
    by_slot: dict[tuple[int, str], int] = {}
    for turn in turns:
        key = (turn["source_index"], turn["role"])
        by_slot[key] = by_slot.get(key, 0) + 1

    assert len(by_slot) == 12
    assert set(by_slot.values()) == {2}


def test_reduced_nilpotent_is_square_zero_rank_one_over_f3() -> None:
    n = nilpotent_increment()

    assert n.tolist() == [[0, 1], [0, 0]]
    assert np.array_equal((n @ n) % 3, np.zeros((2, 2), dtype=int))
    assert rank_mod3(n) == 1


def test_local_12_slot_nilpotent_has_image_equals_kernel_six() -> None:
    data = nilpotent_data(copy_count=6)

    assert data["dimension"] == 12
    assert data["rank"] == 6
    assert data["kernel_dimension"] == 6
    assert data["image_dimension"] == 6
    assert data["square_zero"] is True


def test_global_h1_nilpotent_is_the_0_81_162_81_0_extension() -> None:
    data = nilpotent_data(copy_count=81)

    assert data["dimension"] == 162
    assert data["rank"] == 81
    assert data["kernel_dimension"] == 81
    assert data["image_dimension"] == 81
    assert data["square_zero"] is True


def test_block_nilpotent_rank_is_copy_count_for_multiple_scales() -> None:
    for copies in (1, 3, 6, 81):
        n = block_nilpotent(copies)
        assert rank_mod3(n) == copies
        assert np.array_equal((n @ n) % 3, np.zeros_like(n))


def test_all_identities_hold_and_boundary_is_honest() -> None:
    payload = build_bridge()

    assert all(payload["identities"].values())
    assert "does not construct a universal non-Clifford" in payload["honesty_boundary"]
    assert "finite QEC version of the ouroboros loop" in payload["snake_eats_tail_read"]


def test_index_exposes_dccxvii_architecture_lock() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Axis-Syndrome\n              Nilpotent / Octahedral Codec Bridge" in text
    assert "<code>960=40&times;24</code>" in text
    assert "<code>0&rarr;81&rarr;162&rarr;81&rarr;0</code>" in text


def test_write_and_reload() -> None:
    out = write_bridge()
    assert out == OUT_PATH
    data = json.loads(out.read_text(encoding="utf-8"))

    assert data["summary"]["all_identities_hold"] is True
    assert data["qec_extension"]["exact_sequence"] == "0 -> 81 -> 162 -> 81 -> 0"
