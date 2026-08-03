#!/usr/bin/env python3
"""Idempotently integrate Passes 2967-2970 into blueprint and live atlas."""
from __future__ import annotations
import argparse,json
from pathlib import Path

BLUEPRINT_INPUT=r"\input{analysis/BT2967_BT2970_s6_curvature_chirality_route_blueprint_insert}"
HTML_MARKER="<!-- BT2967-BT2970-S6-CURVATURE-ROUTE-V1 -->"
HTML_SECTION=r'''
<!-- BT2967-BT2970-S6-CURVATURE-ROUTE-V1 -->
<section id="bt2967-bt2970-s6-curvature-route" style="max-width:1100px;margin:3rem auto;padding:1.5rem;border:1px solid #6f7f91;border-radius:12px;">
  <h2>Latest exact result: S6 spread curvature and route decoding</h2>
  <p><strong>Pass 2967.</strong> Every one of the 36 W(3,3) spreads gives the same gauge-invariant parity curvature. The 60 odd triangle holonomies form the exceptional ten-point two-graph; its switching class contains the Petersen graph and its full automorphism group is PΣL(2,9) ≅ S<sub>6</sub> of order 720. Every four-mode tetrahedron obeys the exact discrete Bianchi identity.</p>
  <p><strong>Pass 2968.</strong> Subtracting the certified baseline produces a binary [45,9,9] gauge code. The 120 triangle checks have rank 36, all nongauge odd-parity faults through weight 8 are detected, and all odd-parity faults through weight 4 are correctable modulo local slot gauge.</p>
  <p><strong>Pass 2969 correction.</strong> The minimum local Pauli receiver remains {YI,IY}, but its 0.788675 success is not the Helstrom bound. For squared overlap 1/3, unrestricted ideal success is 0.908248; adaptive individual measurements can attain the n-copy collective bound.</p>
  <p><strong>Pass 2970.</strong> Three pilots identify every one of the 23 nonidentity S4 faults on one edge; the curvature layer adds multi-edge correction for the odd-parity projection.</p>
  <p><strong>Boundary.</strong> These are exact finite routing and ideal receiver statements, not measured optical Berry phases, crosstalk results, loss budgets, or continuum gauge-field claims.</p>
</section>
'''.strip()

def insert_before(text,anchor,payload,marker):
 if marker in text:return text,False
 if anchor not in text:raise RuntimeError(f'missing anchor: {anchor!r}')
 return text.replace(anchor,payload+'\n'+anchor,1),True

def integrate(root,check=False):
 blueprint=root/'holonet_machine_blueprint.tex';index=root/'docs/index.html'
 if not blueprint.is_file():raise FileNotFoundError(blueprint)
 if not index.is_file():raise FileNotFoundError(index)
 b=blueprint.read_text(encoding='utf-8');i=index.read_text(encoding='utf-8')
 nb,bc=insert_before(b,r'\end{document}',BLUEPRINT_INPUT,BLUEPRINT_INPUT)
 ni,ic=insert_before(i,'</body>',HTML_SECTION,HTML_MARKER)
 if check and (bc or ic):raise SystemExit('Passes 2967-2970 are not fully integrated')
 if not check:
  if bc:blueprint.write_text(nb,encoding='utf-8',newline='\n')
  if ic:index.write_text(ni,encoding='utf-8',newline='\n')
 return {'blueprint_changed':bc,'index_changed':ic,'blueprint_integrated':BLUEPRINT_INPUT in nb,'index_integrated':HTML_MARKER in ni}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--check',action='store_true');args=parser.parse_args()
 print(json.dumps(integrate(args.root.resolve(),args.check),sort_keys=True))
if __name__=='__main__':main()
