#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGETS=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex']
INPUTS=[r'\input{analysis/BT1340_BT1344_cartan_atlas_selector_padic}',r'\input{analysis/BT1345_BT1349_basic_mixed_selector_runtime_fusion}',r'\input{analysis/BT1350_BT1354_brauer_basic_atlas_geometry_pdf}']
PART22=ROOT/'manuscripts/tex/part22_fano_synthesis.tex'
def ensure_once(path,line):
 text=path.read_text();text=text.replace(line+'\n','').replace(line,'');marker=r'\end{document}'
 if marker not in text:raise RuntimeError(f'{path}: no end document marker')
 path.write_text(text.replace(marker,'\n'+line+'\n\n'+marker,1))
def repair_part22():
 text=PART22.read_text();bad='PASS1150_SHIFTED_ADJACENCY_RETRACTION';good=r'PASS1150\_SHIFTED\_ADJACENCY\_RETRACTION'
 if bad in text:text=text.replace(bad,good)
 PART22.write_text(text);assert good in PART22.read_text()
def main():
 repair_part22()
 for target in TARGETS:
  for line in INPUTS:ensure_once(target,line)
  text=target.read_text()
  for line in INPUTS:assert text.count(line)==1
 print('PASS 1354: repaired Part XXII and integrated Passes 1340, 1345, and 1350 exactly once in both papers')
if __name__=='__main__':main()
