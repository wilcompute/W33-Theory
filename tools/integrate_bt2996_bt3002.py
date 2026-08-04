#!/usr/bin/env python3
"""Idempotently integrate Passes 2996-3002 into the machine blueprint and site."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEX=ROOT/'holonet_machine_blueprint.tex'
HTML=ROOT/'docs'/'index.html'

TEX_BEGIN='% BEGIN BT2996-BT3002 DEEP OPTIMAL INFORMATION'
TEX_END='% END BT2996-BT3002 DEEP OPTIMAL INFORMATION'
TEX_BLOCK=f'''\n{TEX_BEGIN}
\\input{{analysis/BT2996_BT3002_deep_optimal_information_insert}}
{TEX_END}\n'''

HTML_BEGIN='<!-- BEGIN BT2996-BT3002 DEEP OPTIMAL INFORMATION -->'
HTML_END='<!-- END BT2996-BT3002 DEEP OPTIMAL INFORMATION -->'
HTML_BLOCK=f'''\n{HTML_BEGIN}
<section id="bt2996-bt3002" class="research-update">
  <h2>Adaptive self-synchronizing information closure</h2>
  <p>The exact 23-triangle base resolves 44,848 of 48,826 D4 fault hypotheses. An adaptive escalation tree resolves every remaining case with at most two further triangles: worst case 25, uniform mean 23.0899, and sparse-prior mean 23.00624.</p>
  <p>Address transport has exact symplectic-transvection diameter two. The optimal balanced slot word <code>102332001123</code> supplies mod-12 synchronization while reusing the same three curvature pilots, so no extra pilot channel is introduced.</p>
  <p>Predictive control retains a fourteen-action decision variable rather than a sixteen-bit raw fault index; under the frozen sparse prior its entropy is 0.051734 bits. Global fixed-schedule minimality of 29 and laboratory optical performance remain open.</p>
</section>
{HTML_END}\n'''

def replace_or_insert(text,begin,end,block,anchor):
    if begin in text:
        a=text.index(begin); b=text.index(end,a)+len(end)
        return text[:a]+block.strip('\n')+text[b:]
    pos=text.rfind(anchor)
    if pos<0: return text+block
    return text[:pos]+block+text[pos:]

def main():
    tex=TEX.read_text()
    tex2=replace_or_insert(tex,TEX_BEGIN,TEX_END,TEX_BLOCK,'\\end{document}')
    TEX.write_text(tex2)
    html=HTML.read_text()
    html2=replace_or_insert(html,HTML_BEGIN,HTML_END,HTML_BLOCK,'</body>')
    HTML.write_text(html2)
    print('BT2996-BT3002 integration complete')

if __name__=='__main__': main()
