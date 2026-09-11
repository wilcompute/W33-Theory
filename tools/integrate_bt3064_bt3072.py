#!/usr/bin/env python3
"""Idempotently integrate Passes 3064--3072 into all canonical front doors."""
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LINE='    \\input{analysis/BT3064_BT3072_belief_machine_insert}%'
TEX_BEGIN='% BEGIN BT3064-BT3072 BELIEF MACHINE';TEX_END='% END BT3064-BT3072 BELIEF MACHINE'
HTML_BEGIN='<!-- BEGIN BT3064-BT3072 BELIEF MACHINE -->';HTML_END='<!-- END BT3064-BT3072 BELIEF MACHINE -->'

def block(text,begin,end,new,anchor):
 if begin in text:
  a=text.index(begin);b=text.index(end,a)+len(end);return text[:a]+new.strip('\n')+text[b:]
 p=text.rfind(anchor)
 if p<0:raise RuntimeError(f'anchor {anchor!r} absent')
 return text[:p]+new+text[p:]

def wrapper(path):
 text=path.read_text()
 if LINE not in text:
  hits=list(re.finditer(r'^    \\input\{analysis/[^}]+\}%\s*$',text,re.M))
  if not hits:raise RuntimeError(f'no insert list in {path}')
  p=hits[-1].end();text=text[:p]+'\n'+LINE+text[p:]
 text=re.sub(r'(1821-)(\d+)( plus frame-Hoffman wrapper)',r'\g<1>3072\g<3>',text,count=1)
 path.write_text(text)

def main():
 wrapper(ROOT/'w33_paper.tex');wrapper(ROOT/'photonic_holonet.tex')
 bp=ROOT/'holonet_machine_blueprint.tex';text=bp.read_text();new=f'\n{TEX_BEGIN}\n\\input{{analysis/BT3064_BT3072_belief_machine_insert}}\n{TEX_END}\n';bp.write_text(block(text,TEX_BEGIN,TEX_END,new,'\\end{document}'))
 hp=ROOT/'docs'/'index.html';text=hp.read_text();new='\n'+(ROOT/'analysis'/'BT3064_BT3072_belief_machine_index_insert.html').read_text().strip()+'\n';hp.write_text(block(text,HTML_BEGIN,HTML_END,new,'</body>'))
 print('BT3064-BT3072 four-front-door integration complete')
if __name__=='__main__':main()
