from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass626_h2_2adic_extension.py',
 'w33_pass627_local_montes_atlas.py',
 'w33_pass628_matrix_wilson_hecke.py',
 'w33_pass629_optical_tolerance_region.py',
 'w33_pass630_composite_null_eprocess.py',
]
def test_pass626_630_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
