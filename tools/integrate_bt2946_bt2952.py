#!/usr/bin/env python3
"""Idempotently integrate Passes 2946-2952 into wrappers, blueprint, and site."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INSERT=r"\input{analysis/BT2946_BT2952_seven_front_closure_insert}%"
BEGIN="<!-- BEGIN BT2946-BT2952 -->";END="<!-- END BT2946-BT2952 -->"
CARD=f'''{BEGIN}
<section id="bt2946-bt2952" class="research-update">
<h2>Passes 2946–2952: exact protected observation and hybrid OAM routing</h2>
<p>The global affine-support distance-four optimum is now exact: <strong>15 probes</strong>. The deep M36 branch is compiled to 15 Clifford gates plus two measurements, with an explicit circuit-level stochastic fault law.</p>
<p>A W33 spread supplies a <strong>10 OAM modes × 4 time/frequency slots</strong> address fabric. Corrected telemetry and routing fuse reversibly into one 12-bit rank for all 3,240 valid joint states.</p>
<p>The isodual <code>[8,4,4]_3</code> code is LCD with covering radius two, and its encode/check map obeys <code>D²=-I</code>, <code>D⁴=I</code>.</p>
</section>
{END}'''
def tex(path):
 text=path.read_text(encoding='utf-8')
 if INSERT in text:return False
 anchor=r"\input{analysis/BT2937_BT2945_global_code_landauer_oam_insert}%"
 if anchor in text:text=text.replace(anchor,anchor+'\n    '+INSERT)
 elif r"\end{document}" in text:text=text.replace(r"\end{document}",INSERT+'\n'+r"\end{document}")
 else:raise RuntimeError(f'no TeX anchor in {path}')
 path.write_text(text,encoding='utf-8');return True
def site(path):
 text=path.read_text(encoding='utf-8')
 if BEGIN in text:return False
 anchor='</main>' if '</main>' in text else '</body>'
 if anchor not in text:raise RuntimeError('no HTML anchor')
 path.write_text(text.replace(anchor,CARD+'\n'+anchor),encoding='utf-8');return True
def main():
 changed=[]
 for rel in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
  if tex(ROOT/rel):changed.append(rel)
 if site(ROOT/'docs/index.html'):changed.append('docs/index.html')
 print('changed:',', '.join(changed) if changed else 'none')
if __name__=='__main__':main()
