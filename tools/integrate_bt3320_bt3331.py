#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX=(ROOT/'analysis/BT3330_global_cover_quantum_hypercube_insert.tex').read_text()
HTML=(ROOT/'analysis/BT3330_global_cover_quantum_hypercube_index_insert.html').read_text()
MARK='\\label{sec:global-cover-quantum-hypercube}'
for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
 p=ROOT/name
 if not p.exists(): continue
 s=p.read_text()
 if MARK not in s:
  pos=s.rfind('\\end{document}')
  if pos<0: raise SystemExit(f'missing end document: {name}')
  s=s[:pos]+'\n'+TEX+'\n'+s[pos:];p.write_text(s)
p=ROOT/'docs/index.html'
if p.exists():
 s=p.read_text()
 if 'id="bt3320-3331-global-cover-quantum-hypercube"' not in s:
  pos=s.lower().rfind('</main>')
  if pos<0: pos=s.lower().rfind('</body>')
  if pos<0: raise SystemExit('missing HTML insertion point')
  s=s[:pos]+HTML+'\n'+s[pos:];p.write_text(s)
print('integrated BT3320-BT3331 front doors')
