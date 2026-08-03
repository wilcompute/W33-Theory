from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(path):
 p=subprocess.run([sys.executable,str(ROOT/path)],cwd=ROOT,check=True,capture_output=True,text=True,timeout=240);assert 'PASS 10 / 10' in p.stdout
def test_exact_continuation():
 for path in ['analysis/bt2967_oam_holonomy_s6_two_graph.py','analysis/bt2968_curvature_route_code.py','analysis/bt2969_chirality_receiver_correction.py','analysis/bt2970_layered_route_fault_architecture.py']:run(path)
 assert json.loads((ROOT/'data/PART_BT2967_OAM_HOLONOMY_S6_TWO_GRAPH_results.json').read_text())['classification']['automorphism_group_order']==720
 assert json.loads((ROOT/'data/PART_BT2968_CURVATURE_ROUTE_CODE_results.json').read_text())['code']['parameters']=='[45,9,9]_2'
 assert json.loads((ROOT/'data/PART_BT2969_CHIRALITY_RECEIVER_CORRECTION_results.json').read_text())['unrestricted_single_copy_helstrom_success_decimal']==0.908248290463863
 assert json.loads((ROOT/'data/PART_BT2970_LAYERED_ROUTE_FAULT_ARCHITECTURE_results.json').read_text())['layer_A']['cases']==8280
def test_integrator(tmp_path):
 (tmp_path/'docs').mkdir();(tmp_path/'holonet_machine_blueprint.tex').write_text('\\begin{document}\n\\end{document}\n');(tmp_path/'docs/index.html').write_text('<html><body></body></html>')
 tool=ROOT/'tools/integrate_bt2967_bt2970_blueprint_index.py';subprocess.run([sys.executable,str(tool),'--root',str(tmp_path)],check=True);subprocess.run([sys.executable,str(tool),'--root',str(tmp_path),'--check'],check=True)
