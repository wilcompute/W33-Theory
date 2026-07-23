from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass621_integral_h2_lattice.py',
 'w33_pass622_ramification_atlas.py',
 'w33_pass623_hecke_generators_observables.py',
 'w33_pass624_optical_cube_decoder.py',
 'w33_pass625_anytime_poisson_eprocess.py',
]
def test_pass621_625_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
