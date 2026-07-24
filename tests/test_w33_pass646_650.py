from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass646_2adic_deformation_functor.py',
 'w33_pass647_conductor_gauge_descent.py',
 'w33_pass648_dual_label_optical_prototype.py',
 'w33_pass649_partial_channel_matrix_eprocess.py',
 'w33_pass650_joint_science_diagnosis_game.py',
]
def test_pass646_650_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
