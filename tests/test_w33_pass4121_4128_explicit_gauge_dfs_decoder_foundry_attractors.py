"""Focused regression for Passes 4121-4128."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_4121_4128_EXPLICIT_GAUGE_DFS_DECODER_FOUNDRY_ATTRACTORS_BONKERS.json"
VERIFY=ROOT/"analysis/w33_pass4121_4128_explicit_gauge_dfs_decoder_foundry_attractors.py"


def test_certificate_boundaries_and_status():
    d=json.loads(CERT.read_text())
    assert d["status"]=="PASS_EXACT_FULL_CARRIER_ANOMALY_CORRECTION_RELATIONAL_DFS_DECODER_FOUNDRY_AUDIT_ATTRACTOR_ORBITS_ISING_MIRROR_EP"
    assert d["pass4121_explicit_145_gauge_matrices"]["full_carrier_anomalies"]["SU3_cubed"]==-28
    assert d["pass4123_graph_aware_decoder"]["maximum_candidate_edges"]==20
    assert d["pass4126_bonkers_antiferromagnetic_Ising"]["cut_edges"]==160
    assert d["pass4128_bonkers_exceptional_point_sensor"]["simultaneous_EP2_blocks"]==15
    assert any("No derived Standard Model" in x for x in d["boundaries"])


def test_deterministic_verifier():
    p=subprocess.run([sys.executable,str(VERIFY)],cwd=ROOT,text=True,capture_output=True,check=True,timeout=60)
    out=json.loads(p.stdout.strip())
    assert out["decoder_max_candidate_edges"]==20
    assert out["crossings"]==1934
    assert out["maxcut"]==160
    assert out["simultaneous_EP2"]==15
