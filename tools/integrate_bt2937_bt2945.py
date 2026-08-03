#!/usr/bin/env python3
"""Idempotently integrate Passes 2937-2945 into canonical manuscripts and site."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INSERT=r"\input{analysis/BT2937_BT2945_global_code_landauer_oam_insert}%"
BEGIN="<!-- BEGIN BT2937-BT2945 -->"
END="<!-- END BT2937-BT2945 -->"
CARD=f'''{BEGIN}
<section id="bt2937-bt2945" class="research-update">
<h2>Passes 2937–2945: global protected support, Landauer diagnosis, and OAM</h2>
<p>The full affine-support orbit gives an exact distance-four bracket <strong>13 ≤ n ≤ 16</strong>. The 16-bit witness is the binary image of an isodual <code>[8,4,4]_3</code> code, enabling a four-trit syndrome decoder rather than an 81-word scan.</p>
<p>Every complete uniform 81-state diagnostic transcript has optimally compressed entropy <code>log2(81)</code>. OAM is optional abstractly but explicit in the selected photonic profile; the full W33 symmetry action has no 40-cycle, so a single cyclic OAM shift cannot be the whole address bus.</p>
</section>
{END}'''

def insert_tex(path):
    text=path.read_text(encoding='utf-8')
    if INSERT in text: return False
    anchor=r"\input{analysis/BT2854_BT2860_seven_frontiers_insert}%"
    if anchor in text: text=text.replace(anchor,anchor+'\n    '+INSERT)
    elif r"\end{document}" in text: text=text.replace(r"\end{document}",INSERT+'\n'+r"\end{document}")
    else: raise RuntimeError(f'no TeX anchor: {path}')
    path.write_text(text,encoding='utf-8'); return True

def insert_site(path):
    text=path.read_text(encoding='utf-8')
    if BEGIN in text: return False
    anchor='</main>' if '</main>' in text else '</body>'
    if anchor not in text: raise RuntimeError('no HTML anchor')
    path.write_text(text.replace(anchor,CARD+'\n'+anchor),encoding='utf-8'); return True

def main():
    changed=[]
    for rel in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        if insert_tex(ROOT/rel): changed.append(rel)
    if insert_site(ROOT/'docs'/'index.html'): changed.append('docs/index.html')
    print('changed:', ', '.join(changed) if changed else 'none')
if __name__=='__main__': main()
