#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX=(ROOT/'analysis/BT3272_hamming_orbifold_dual_guard_insert.tex').read_text()
HTML=(ROOT/'analysis/BT3272_hamming_orbifold_dual_guard_index_insert.html').read_text()
TB='% BEGIN PASS 3262-3273 HAMMING ORBIFOLD DUAL GUARD';TE='% END PASS 3262-3273 HAMMING ORBIFOLD DUAL GUARD'
HB='<!-- BEGIN PASS 3262-3273 HAMMING ORBIFOLD DUAL GUARD -->';HE='<!-- END PASS 3262-3273 HAMMING ORBIFOLD DUAL GUARD -->'
def replace_or_insert(path,insert,begin,end,anchor):
 raw=path.read_bytes();text=raw.decode('utf-8','surrogateescape')
 if begin in text:
  a=text.index(begin);b=text.index(end,a)+len(end);text=text[:a]+insert.strip()+text[b:]
 else:
  k=text.rfind(anchor);assert k>=0,(path,anchor);text=text[:k]+insert.strip()+'\n\n'+text[k:]
 path.write_bytes(text.encode('utf-8','surrogateescape'))
def main():
 for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
  replace_or_insert(ROOT/name,TEX,TB,TE,'\\end{document}')
 replace_or_insert(ROOT/'docs/index.html',HTML,HB,HE,'</body>')
if __name__=='__main__':main()
