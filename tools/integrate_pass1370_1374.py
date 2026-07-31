#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INSERT=r'\input{analysis/BT1370_BT1374_five_frontiers}'
TARGETS=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex']
def integrate(path):
 text=path.read_text(); count=text.count(INSERT)
 if count>1: raise SystemExit(f'duplicate {INSERT} in {path}')
 if count==0:
  marker='\\end{document}'
  if marker not in text: raise SystemExit(f'missing end document in {path}')
  text=text.replace(marker,INSERT+'\n\n'+marker,1);path.write_text(text)
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 if a.check:
  for path in TARGETS:
   if path.read_text().count(INSERT)!=1:raise SystemExit(f'integration drift: {path}')
 else:
  for path in TARGETS:integrate(path)
 print('PASS integration 1370-1374')
if __name__=='__main__':main()
