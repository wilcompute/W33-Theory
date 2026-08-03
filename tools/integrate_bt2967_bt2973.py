#!/usr/bin/env python3
"""Idempotently integrate Passes 2967-2973 into blueprint and site."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MARK='BT2967-BT2973-OPTIMAL-INFORMATION-SYSTEM'
tex=ROOT/'holonet_machine_blueprint.tex'
html=ROOT/'docs/index.html'
tex_block=r'''
% BEGIN BT2967-BT2973-OPTIMAL-INFORMATION-SYSTEM
\section{Optimal live-controller architecture (Passes 2967--2973)}
The live information system retains four frame trits, ten spread-line labels, four
slots, and one encode/check sector.  It uses the native affine, $D_4$,
anti-symplectic, and isodual controls; binary joint ranking is deferred to archive,
export, or reset boundaries.  Twenty-three triangles are exactly optimal for
single-edge localization, a 29-triangle construction resolves all one- and two-edge
$D_4$ faults, and the deep-$M_{36}$ branch is reduced to six CNOTs and three
Hadamards by static wire relabeling.  The native controller group has order
$30{,}233{,}088$; the future-observation-minimal quotient has 6048 states but still
needs thirteen fixed bits.  A reversible $D_{12}$ logical clock partitions the 6480
controller states into 540 twelve-cycles.  These are logical and modeled results;
physical calibration, placement, and autonomous-clock behavior remain open.
% END BT2967-BT2973-OPTIMAL-INFORMATION-SYSTEM
'''
html_block='''
<!-- BEGIN BT2967-BT2973-OPTIMAL-INFORMATION-SYSTEM -->
<section id="bt2967-bt2973-optimal-information-system">
  <h2>Optimal information-system closure: Passes 2967–2973</h2>
  <p>The selected live architecture stays native and mixed-radix: four frame trits, ten OAM spread lines, four slots, and one encode/check sector. Binary ranking is deferred to archival or reset boundaries.</p>
  <ul>
    <li>23 triangles are exactly optimal for single-edge localization; 29 identify every one- and two-edge D4 fault in the frozen model.</li>
    <li>The deep-M36 branch is reduced from 15 to 9 Clifford gates by static wire relabeling.</li>
    <li>The native controller group has order 30,233,088; its minimal future-observation quotient has 6,048 states and still needs 13 bits.</li>
    <li>A reversible D12 logical phase clock splits 6,480 states into 540 twelve-tick cycles.</li>
  </ul>
  <p><strong>Boundary:</strong> optical counts are synthetic, compiler backend costs are model-dependent, and hardware timing and autonomous clock behavior remain unmeasured.</p>
</section>
<!-- END BT2967-BT2973-OPTIMAL-INFORMATION-SYSTEM -->
'''
def insert(path,block,end):
 if not path.exists(): return False
 s=path.read_text()
 if MARK in s: return False
 pos=s.rfind(end)
 s=(s[:pos]+block+s[pos:]) if pos>=0 else s+block
 path.write_text(s); return True
changed=[]
if insert(tex,tex_block,'\\end{document}'):changed.append(str(tex.relative_to(ROOT)))
if insert(html,html_block,'</body>'):changed.append(str(html.relative_to(ROOT)))
print('integrated' if changed else 'already integrated',', '.join(changed))
