from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass601_twisted_torsion_anatomy.py',
 'w33_pass602_connection_gauge_quotient.py',
 'w33_pass603_outer_15_intertwiner.py',
 'w33_pass604_snub_coloring_selector.py',
 'w33_pass605_noise_aware_wilson_falsifier.py',
]
def test_pass601_605_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
