"""Reproduce all five W33 tick/TOE continuation tracks."""
import importlib.util
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))

def load(filename,name):
    src=ROOT/"analysis"/filename
    spec=importlib.util.spec_from_file_location(name,src)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_four_quantum_tracks():
    results=load("w33_20261019_allfive_physics.py","five_physics").main()
    assert results["all_checks_pass"]
    phys=results["tracks"]
    assert abs(phys["microscopic"]["overlap_collinear"]-phys["microscopic"]["overlap_noncollinear"])<1e-12
    assert abs(phys["microscopic"]["theta_pi_over_two_kappa_per_gamma"]-2/9)<1e-12
    assert phys["phase"]["family_scans"][0]["temperature"]==0.2
    assert phys["echo"]["worst_numeric_residual"]<1e-12
    assert phys["echo"]["shots_per_config"]==1598
    assert phys["representation"]["Pauli_translation_80_actions_checked"]==80

def test_full_paper_structural_audit():
    # The audit executes itself at import and fails closed if source checks
    # fail. Check persisted JSON after replay.
    import json
    load("w33_20261019_allfive_forty_points_audit.py","five_audit")
    result=json.loads((ROOT/"data"/"w33_20261019_allfive_forty_points_audit.json").read_text())
    assert result["all_checks_pass"]
    assert result["module_count"]==15
    assert result["edition_comparison"]["extracted_pages"]==190
    assert result["unique_cert_labels"]>=500
    assert result["unresolved_evidence_labels_count"]>=0
