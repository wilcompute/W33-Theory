#!/usr/bin/env python3
"""Repro driver for canonical Pass10837-10900 packet."""
from __future__ import annotations
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
 'analysis/w33_pass10837_10844_d26_extension_defect_resolution.py',
 'analysis/w33_pass10845_10852_normalizer_jordan_pg24.py',
 'analysis/w33_pass10853_10860_fixed_tree_affine_frame.py',
 'analysis/w33_pass10861_10868_local_pairing_global_no_go.py',
 'analysis/w33_pass10869_10876_hj10_p1f9_test.py',
 'analysis/w33_pass10877_10884_hj10_split_p1f9_geometry.py',
 'analysis/w33_pass10885_10892_c2_tate_ext_defect.py',
]
def main():
    for rel in SCRIPTS:
        subprocess.run([sys.executable,str(ROOT/rel)],cwd=ROOT,check=True)
    print({'status':'PASS','scripts':len(SCRIPTS),'packet':'10837-10900'})
if __name__=='__main__':main()
