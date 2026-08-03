#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
INSERT=r'\input{analysis/BT2809_BT2815_seven_frontiers_insert}'

def patch(path:Path, marker:str):
    text=path.read_text()
    if INSERT in text: return False
    if marker not in text: raise RuntimeError(f'marker missing in {path}')
    path.write_text(text.replace(marker,INSERT+'%\n    '+marker,1))
    return True

def main():
    changed=[]
    for name,marker in [
      ('w33_paper.tex',r'\input{w33_paper_body.tex}'),
      ('photonic_holonet.tex',r'\input{photonic_holonet_body.tex}'),
    ]:
      if patch(ROOT/name,marker):changed.append(name)
    bp=ROOT/'holonet_machine_blueprint.tex'
    if bp.exists():
      text=bp.read_text()
      if INSERT not in text:
        marker=r'\tableofcontents'
        if marker not in text:raise RuntimeError('blueprint TOC marker missing')
        bp.write_text(text.replace(marker,marker+'\n'+INSERT,1));changed.append(bp.name)
    print('changed='+','.join(changed) if changed else 'already integrated')
if __name__=='__main__':main()
