#!/usr/bin/env python3
"""Idempotently integrate Passes 2967-2970 into blueprint and live atlas."""
from __future__ import annotations
import argparse,json
from pathlib import Path
BI=r"\input{analysis/BT2967_BT2970_s6_curvature_chirality_route_blueprint_insert}";MARK='<!-- BT2967-BT2970-S6-CURVATURE-ROUTE-V1 -->'
CARD='''<!-- BT2967-BT2970-S6-CURVATURE-ROUTE-V1 -->
<section id="bt2967-bt2970-s6-curvature-route" style="max-width:1100px;margin:3rem auto;padding:1.5rem;border:1px solid #6f7f91;border-radius:12px;">
<h2>Latest exact result: S6 spread curvature and route decoding</h2>
<p><strong>Pass 2967.</strong> All 36 spreads give the same parity two-graph: 60 odd triangles, a Petersen switching representative, automorphism group PΣL(2,9) ≅ S<sub>6</sub>, and exact tetrahedral Bianchi identity.</p>
<p><strong>Pass 2968.</strong> The parity syndrome is a binary [45,9,9] gauge code with 36 independent checks, detection through weight 8 and correction through weight 4 modulo slot gauge.</p>
<p><strong>Pass 2969 correction.</strong> The 0.788675 two-Pauli receiver is not Helstrom-optimal; squared overlap 1/3 gives ideal unrestricted one-copy success 0.908248.</p>
<p><strong>Pass 2970.</strong> Three pilots identify one arbitrary S4 edge fault; curvature adds multi-edge correction for odd faults.</p>
<p><strong>Boundary.</strong> Exact finite routing and ideal receiver statements only—not measured loss, crosstalk, Berry phase, or continuum gauge claims.</p>
</section>'''
def ins(text,anchor,payload,marker):
 if marker in text:return text,False
 if anchor not in text:raise RuntimeError(f'missing anchor {anchor}')
 return text.replace(anchor,payload+'\n'+anchor,1),True
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--check',action='store_true');a=p.parse_args();root=a.root.resolve();bp=root/'holonet_machine_blueprint.tex';idx=root/'docs/index.html';b=bp.read_text();i=idx.read_text();nb,bc=ins(b,r'\end{document}',BI,BI);ni,ic=ins(i,'</body>',CARD,MARK)
 if a.check and (bc or ic):raise SystemExit('not integrated')
 if not a.check:
  if bc:bp.write_text(nb,newline='\n')
  if ic:idx.write_text(ni,newline='\n')
 print(json.dumps({'blueprint_changed':bc,'index_changed':ic,'blueprint_integrated':BI in nb,'index_integrated':MARK in ni},sort_keys=True))
if __name__=='__main__':main()
