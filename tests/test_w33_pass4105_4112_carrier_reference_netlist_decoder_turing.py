import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_pass4105_4112_verifier():
    p=subprocess.run([sys.executable,str(ROOT/'analysis/w33_pass4105_4112_carrier_reference_netlist_decoder_turing.py')],cwd=ROOT,text=True,capture_output=True,check=True)
    out=json.loads(p.stdout)
    assert out['status']=='PASS_EXACT_CARRIER_AUDIT_MULTIUSE_REFERENCE_NETLIST_DECODER_TURING_CONSENSUS_NAVIGATION_HUCKEL'
    assert out['carrier_dimensions']==[99,145]
    assert out['decoder_sigma6']>0.44
    assert min(out['turing_purities'])>1-1e-12

def test_release_files_exist():
    for rel in [
        'data/PART_4105_4112_CARRIER_REFERENCE_NETLIST_DECODER_TURING_BONKERS.json',
        'data/w33_pass4105_sector_faithful_carrier.json',
        'data/w33_pass4107_router_fabrication_netlist.json']:
        assert (ROOT/rel).is_file()
