import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_exact_packet_regenerates():
    proc=subprocess.run([sys.executable,str(ROOT/'analysis/w33_pass4129_4136_anomaly_gates_decoder_hybrid_orbits.py')],cwd=ROOT,text=True,capture_output=True,check=True,timeout=120)
    out=json.loads(proc.stdout.strip().splitlines()[-1])
    assert out['semantic_sha256']=='e8a48ff8074816830fedd753bd76f10daa9c16eddc604a6e1654fb32b3b605dd'
    assert out['lambda10_signs']==33264
    assert out['lambda16_signs']==432
    assert out['theta_total']==133920
    assert out['hybrid_depth']==9
