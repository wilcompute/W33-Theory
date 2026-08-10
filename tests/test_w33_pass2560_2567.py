from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def test_frozen_packet():
 r=subprocess.run([sys.executable,str(ROOT/'analysis/w33_pass2560_2567_verify_frozen.py')],capture_output=True,text=True,check=True);assert '"status": "PASS"' in r.stdout
def test_eleven_coloring_reconstructs():
 r=subprocess.run([sys.executable,str(ROOT/'analysis/w33_pass2561_verify_coloring11.py')],capture_output=True,text=True,check=True);assert 'e97f43322d50d58a103b9d61968f574612b80dd8f3f71c080fc290988ed92531' in r.stdout
def test_breakthrough_boundaries():
 u=json.loads((ROOT/'data/w33_pass2560_u6_singleton_orbit_harvest.json').read_text(encoding="utf-8"));f=json.loads((ROOT/'data/w33_pass2562_exact_character_fusion.json').read_text(encoding="utf-8"));s=json.loads((ROOT/'data/w33_pass2565_abstract_schlaefli_incidence.json').read_text(encoding="utf-8"));assert u['orbit_classification']['certified_singleton_lower_bound']==13633920;assert f['exact_submodule_assignment']['135']=='60+15+30+30';assert s['line_graph']['parameters']==[27,10,1,5]
