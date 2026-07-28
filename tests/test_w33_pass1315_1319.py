"""Regression tests for Passes 1315-1319 exact frontier release."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "w33_pass1315_1319_exact_frontiers.json"

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def test_hecke_wedderburn_completion():
    d=load()["pass1315_literal_hecke_wedderburn"]
    assert d["hecke_dimension"]==26
    assert d["center_dimension"]==9
    assert d["complex_wedderburn_blocks"]=={"1":1,"6":2,"15":1,"15a":1,"20":3,"30":2,"60a":1,"64":2,"81_minus":1}
    assert sum(m*m for m in d["complex_wedderburn_blocks"].values())==26
    assert len(d["primitive_central_idempotents_relation_coefficients"])==9

def test_hashimoto_exact_decomposition():
    d=load()["pass1316_hashimoto_character_reexecution"]
    assert sum(x["degree"]*x["multiplicity"] for x in d["directed_edge_decomposition"])==480
    assert sum(x["degree"]*x["multiplicity"] for x in d["plus1_decomposition"])==201
    assert sum(x["degree"]*x["multiplicity"] for x in d["minus1_decomposition"])==200

def test_literal_species20_units():
    d=load()["pass1317_literal_species20_matrix_units"]
    assert d["rank"]==20
    assert d["denominator"]==51840
    assert d["trace_numerator"]==51840*20
    assert d["idempotent_identity"]=="N^2=51840*N"
    assert d["commutes_with_hashimoto"] is True
    assert len(d["pivot_columns"])==len(d["pivot_rows"])==20

def test_cross_carrier_hom_space():
    d=load()["pass1319_coset_hashimoto_hom"]
    assert d["hom_dimension"]==d["diagonal_orbit_count"]==6
    assert d["orbital_sizes"]==[51840,51840,51840,17280,17280,17280]
    assert sum(x["contribution"] for x in d["common_species"].values())==6
    assert d["zero_obstruction"] is False

def test_migration_is_fail_closed():
    d=load()
    assert d["pass1318_correction_migration"]["false_burnside_value"]=="43/5"
    assert d["pass1318_correction_migration"]["literal_orbit_count"]==26
    assert all(d["checks"].values())


def test_k9_chain_is_fail_closed():
    stale = [
        "analysis/w33_pass1260_a5_fixed_point_counts.py",
        "analysis/w33_pass1261_exact_hecke_constants.py",
        "analysis/w33_pass1263_k9_coset_verification.py",
        "analysis/w33_pass1268_k9_coset_table_gap_plan.py",
        "analysis/w33_pass1274_hecke_tensor_analytic.py",
        "analysis/w33_pass1266_theorem_ledger_v5.py",
        "analysis/w33_pass1272_theorem_ledger_v6.py",
        "analysis/w33_pass1277_theorem_ledger_v7.py",
        "PASS1258_1262_EXECUTION_RELEASE.md",
        "PASS1263_1267_EXECUTION_RELEASE.md",
        "PASS1268_1272_EXECUTION_RELEASE.md",
        "PASS1273_1277_EXECUTION_RELEASE.md",
    ]
    for rel in stale:
        text=(ROOT/rel).read_text(encoding="utf-8")
        assert "RETRACTED" in text
        assert "26" in text or rel.endswith(".py")


def test_namespace_registry_records_release_and_retraction():
    registry=json.loads((ROOT/"data/w33_pass_namespace_registry_v2.json").read_text(encoding="utf-8"))
    blocks={b["range"]:b for b in registry["canonical_blocks"]}
    assert blocks["1315-1319"]["status"]=="COMPLETE"
    assert blocks["1263-1272"]["status"]=="RETRACTED_BY_1318"
    assert blocks["1273-1277"]["status"]=="RETRACTED_BY_1318"
