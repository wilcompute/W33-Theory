from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5580_5585_reye_psl2_permutation_frame.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass5580_5585", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_q3_reye_projectivity_graph_and_rank():
    mod = load_module()
    row = mod.analyse(3)
    assert row["rows_psl2_order"] == 12
    assert row["columns_grid"] == 16
    assert row["row_weight"] == 4
    assert row["column_weight"] == 3
    assert row["char0_rank"] == 10
    assert row["binary_rank_measured"] == 8
    assert row["row_overlap_values"] == [0, 1]


def test_q5_family_member_and_gram_rank():
    mod = load_module()
    row = mod.analyse(5)
    assert row["rows_psl2_order"] == 60
    assert row["columns_grid"] == 36
    assert row["row_weight"] == 6
    assert row["column_weight"] == 10
    assert row["two_column_stabilizer"] == 2
    assert row["char0_rank"] == 26
    assert row["binary_rank_measured"] == 18
    assert row["row_overlap_values"] == [0, 1, 2]


def test_q3_explicit_order576_automorphism_subgroup():
    mod = load_module()
    cert = mod.q3_aut_group_certificate()
    assert cert["reye_flags"] == 48
    assert cert["same_parity_S4xS4_order"] == 288
    assert cert["with_transpose_inversion_order"] == 576
