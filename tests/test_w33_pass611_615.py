from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass611_spectral_snf_boundary.py',
 'w33_pass612_johnson_clique_homotopy.py',
 'w33_pass613_equivariant_groupoid_laplacian.py',
 'w33_pass614_fault_detecting_selector_code.py',
 'w33_pass615_sequential_wilson_falsifier.py',
]
def test_pass611_615_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
