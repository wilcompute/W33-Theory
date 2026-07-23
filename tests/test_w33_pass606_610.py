from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass606_complete_twisted_snf.py',
 'w33_pass607_johnson_clique_pi1.py',
 'w33_pass608_torsion_symmetry_actions.py',
 'w33_pass609_tetrahedral_hardware_gauge.py',
 'w33_pass610_optimal_wilson_inference.py',
]
def test_pass606_610_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
