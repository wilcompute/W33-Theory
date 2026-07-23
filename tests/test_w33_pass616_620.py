from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'w33_pass616_arithmetic_core_factorization.py',
 'w33_pass617_h2_s8_module.py',
 'w33_pass618_hecke_compression.py',
 'w33_pass619_optimal_selector_code.py',
 'w33_pass620_adversarial_poisson_controller.py',
]
def test_pass616_620_certificates_are_reproducible():
 for name in SCRIPTS:
  subprocess.run([sys.executable,str(ROOT/'analysis'/name),'--check'],cwd=ROOT,check=True)
