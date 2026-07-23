from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass636_mod4_bockstein_lift.py',
 'w33_pass637_local_conductor_graph.py',
 'w33_pass638_endpoint_parity_fibre.py',
 'w33_pass639_matrix_covariance_cs.py',
 'w33_pass640_closed_loop_falsifier.py',
]
def test_pass636_640_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
