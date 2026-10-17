#!/usr/bin/env python3
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[1]
INPUT=r'    \input{analysis/BT3003_BT3011_seven_front_optimal_information_insert}%\n'
PREV=r'    \input{analysis/BT2967_BT2973_optimal_information_system_insert}%\n'
TEX_BLOCK=r'''
% BEGIN BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION
\input{analysis/BT3003_BT3011_seven_front_optimal_information_blueprint_insert}
% END BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION
'''.strip()
HTML_BLOCK=r'''
<!-- BEGIN BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION -->
<section id="bt3003-bt3011-seven-front-optimal-information">
  <h2>Passes 3003–3011: typed optimal-information closure</h2>
  <p>The six general-isotropic M36 pilot hits collapse to one 729-element symmetry orbit; a new 28-triangle diagnostic separates all 48,826 one- and two-edge D4 fault hypotheses; and the 540 skew-line objects carry a natural 3×4 flag fiber giving the exact 6,480-state geometric bundle.</p>
  <p>The golden controller is now typed as an A4 syndrome shell outside a protected D4 core. An 89/233 Christoffel scheduler crossed with the D12 clock gives a reversible 2,796-tick calibration calendar, while component-resolved Bayesian stopping replaces fixed-copy chirality repetition. Exhaustive M36 completion and observed hardware evidence remain separately gated.</p>
</section>
<!-- END BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION -->
'''.strip()
def wrappers(check=False):
 for name in ['w33_paper.tex','photonic_holonet.tex']:
  p=ROOT/name;text=p.read_text()
  if INPUT.strip() not in text:
   if check:raise SystemExit(f'{name}: insert absent')
   if PREV not in text:raise RuntimeError(f'{name}: predecessor anchor absent')
   p.write_text(text.replace(PREV,PREV+INPUT,1))
def block(path,body,sentinel,anchor,check=False):
 p=ROOT/path;text=p.read_text()
 if sentinel not in text:
  if check:raise SystemExit(f'{path}: block absent')
  if anchor not in text:raise RuntimeError(f'{path}: anchor absent')
  p.write_text(text.replace(anchor,body+'\n'+anchor,1))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args();wrappers(a.check)
 block('holonet_machine_blueprint.tex',TEX_BLOCK,'BEGIN BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION','\\end{document}',a.check)
 block('docs/index.html',HTML_BLOCK,'BEGIN BT3003-BT3011 SEVEN FRONT OPTIMAL INFORMATION','</body>',a.check)
 print({'check':a.check,'integrated':True})
if __name__=='__main__':main()
