from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass631_mod2_ext_fingerprint.py',
 'w33_pass632_montes_okutsu_stage0.py',
 'w33_pass633_minimal_wilson_fibre.py',
 'w33_pass634_correlated_optical_decoder.py',
 'w33_pass635_joint_optical_eprocess_design.py',
]
def test_pass631_635_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
