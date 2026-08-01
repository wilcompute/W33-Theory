#!/usr/bin/env python3
"""Prepare syndrome columns and canonical frame supports for Pass 1838."""
from pathlib import Path
import sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1801_1805_common import build_geometry
d=build_geometry();K=np.asarray(d['K'],dtype=np.uint8);M=np.asarray(d['M'],dtype=np.uint8)
cols=[tuple(map(int,np.flatnonzero(K[:,j]))) for j in range(240)];assert all(len(x)==3 for x in cols)
(ROOT/'data'/'w33_pass1838_syndromes240.txt').write_text('\n'.join(str(sum(1<<i for i in x)) for x in cols)+'\n')
with (ROOT/'data'/'w33_pass1838_frames540.txt').open('w') as f:
 for row in M:
  s=np.flatnonzero(row);assert len(s)==4;f.write(' '.join(map(str,s))+'\n')
