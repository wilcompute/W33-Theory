#!/usr/bin/env python3
"""Idempotently integrate the Passes 2960-2966 theorem into the machine blueprint and site."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEX=ROOT/'holonet_machine_blueprint.tex'
HTML=ROOT/'docs/index.html'

TEX_BLOCK=r'''
% BEGIN BT2960-BT2966 PHYSICAL COMPILER
\input{analysis/BT2960_BT2966_physical_compiler_insert}
% END BT2960-BT2966 PHYSICAL COMPILER
'''.strip()
HTML_BLOCK=r'''
<!-- BEGIN BT2960-BT2966 PHYSICAL COMPILER -->
<section id="bt2960-bt2966-physical-compiler">
  <h2>Passes 2960–2966: physical compiler closure</h2>
  <p>The optimal 15-probe observer now factors through one minimum-incidence ternary parity mixer; all 36 W33 spreads generate the same nonabelian D4 routing curvature; and the valid frame-route compiler is an explicit 120-Toffoli, 79-CNOT reversible network.</p>
  <p>The optical channel profiles are synthetic engineering probes, while coherent M36 susceptibilities, the three-pilot route theorem, and the anti-symplectic phase transducer are exact for their stated finite models.</p>
</section>
<!-- END BT2960-BT2966 PHYSICAL COMPILER -->
'''.strip()

def insert_once(path:Path, block:str, sentinel:str, closing:str)->bool:
    text=path.read_text()
    if sentinel in text:return False
    if closing not in text:raise RuntimeError(f'{closing!r} missing from {path}')
    path.write_text(text.replace(closing,block+'\n'+closing,1))
    return True

def main():
    changed=[]
    if insert_once(TEX,TEX_BLOCK,'BEGIN BT2960-BT2966 PHYSICAL COMPILER','\\end{document}'):
        changed.append(str(TEX.relative_to(ROOT)))
    if insert_once(HTML,HTML_BLOCK,'BEGIN BT2960-BT2966 PHYSICAL COMPILER','</body>'):
        changed.append(str(HTML.relative_to(ROOT)))
    print({'changed':changed,'idempotent':not changed})
if __name__=='__main__':main()
