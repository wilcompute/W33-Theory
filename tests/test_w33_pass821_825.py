from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES={
 '821':'analysis/w33_pass821_gluing66_composition_series.py',
 '822':'analysis/w33_pass822_cut10_heisenberg_layer_and_flatblock_retraction.py',
 '823':'analysis/w33_pass823_integral_deformation_tower.py',
 '824':'analysis/w33_pass824_minimax_audit_stream_allocator.py',
 '825':'analysis/w33_pass825_facet_pruned_polyhedral_runtime.py',
}

def run(key,timeout=180):
 p=subprocess.run([sys.executable,str(ROOT/CASES[key]),'--check'],cwd=ROOT,text=True,capture_output=True,timeout=timeout)
 assert p.returncode==0,p.stdout+'\n'+p.stderr
 assert '"status": "PASS"' in p.stdout

def test_pass821_gluing66_composition_series():run('821')
def test_pass822_cut10_heisenberg_layer_and_flatblock_retraction():run('822')
def test_pass823_integral_deformation_tower():run('823')
def test_pass824_minimax_audit_stream_allocator():run('824')
def test_pass825_facet_pruned_polyhedral_runtime():run('825',timeout=300)
