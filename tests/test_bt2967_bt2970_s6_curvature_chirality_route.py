from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(path):
 completed=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,check=True,capture_output=True,text=True,timeout=240)
 assert 'PASS 10 / 10' in completed.stdout

def test_exact_verifiers():
 for path in [
  'analysis/bt2967_oam_holonomy_s6_two_graph.py',
  'analysis/bt2968_curvature_route_code.py',
  'analysis/bt2969_chirality_receiver_correction.py',
  'analysis/bt2970_layered_route_fault_architecture.py',
 ]:run(path)

def test_frozen_certificates():
 expected={
  'PART_BT2967_OAM_HOLONOMY_S6_TWO_GRAPH_results.json':('classification','automorphism_group_order',720),
  'PART_BT2968_CURVATURE_ROUTE_CODE_results.json':('code','parameters','[45,9,9]_2'),
  'PART_BT2969_CHIRALITY_RECEIVER_CORRECTION_results.json':(None,'unrestricted_single_copy_helstrom_success_decimal',0.908248290463863),
  'PART_BT2970_LAYERED_ROUTE_FAULT_ARCHITECTURE_results.json':('layer_A','cases',8280),
 }
 for name,(section,key,value) in expected.items():
  payload=json.loads((ROOT/'data'/name).read_text())
  actual=payload[section][key] if section else payload[key]
  assert actual==value
  assert all(payload['checks'].values())

def test_integrator_idempotence(tmp_path):
 (tmp_path/'docs').mkdir()
 (tmp_path/'holonet_machine_blueprint.tex').write_text('\\begin{document}\nX\n\\end{document}\n')
 (tmp_path/'docs/index.html').write_text('<html><body>X</body></html>\n')
 tool=ROOT/'tools/integrate_bt2967_bt2970_blueprint_index.py'
 first=subprocess.run([sys.executable,str(tool),'--root',str(tmp_path)],check=True,capture_output=True,text=True)
 assert json.loads(first.stdout)['blueprint_changed']
 second=subprocess.run([sys.executable,str(tool),'--root',str(tmp_path)],check=True,capture_output=True,text=True)
 assert not json.loads(second.stdout)['blueprint_changed']
 subprocess.run([sys.executable,str(tool),'--root',str(tmp_path),'--check'],check=True)
