from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass641_higher_2adic_commutant.py',
 'w33_pass642_conductor_torsion_map.py',
 'w33_pass643_multiplexed_guard_fibre.py',
 'w33_pass644_unbounded_matrix_eprocess.py',
 'w33_pass645_minimax_controller.py',
]
def test_pass641_645_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
