#!/usr/bin/env python3
"""BT1797: local patcher for docs/index.html.

The live index file is large. This patcher is committed as the exact reproducible
edit: run from the repo root to insert the H27 correction box once.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'docs' / 'index.html'
MARKER = 'BT1797_H27_CORRECTION_BOX'
SNIPPET = '''
<!-- BT1797_H27_CORRECTION_BOX BEGIN -->
<section id="bt1797-h27-correction" class="card evidence-card">
  <h2>BT1797 correction: raw 27, Payne 27, and Schläfli/E6 are distinct</h2>
  <p><strong>Raw local shell.</strong> In <code>W(3,3)=SRG(40,12,2,4)</code>, fixing a point gives
    <code>1 + 12 + 27</code>. The induced graph on the 27 non-neighbours is the affine
    Heisenberg bulk: 27 vertices, 108 edges, and internal degree 8. It is not yet the
    Schläfli graph and not yet <code>GQ(2,4)</code>.</p>
  <p><strong>Payne transform.</strong> Adding the nine Heisenberg vertical fibres to the 36 old
    <code>W(3,3)</code> triples gives the Payne-derived geometry
    <code>GQ(2,4)=SRG(27,10,1,5)</code>. These 45 triples are the tritangent-plane support.</p>
  <p><strong>Schläfli/E6 dual.</strong> The complement of that Payne collinearity graph is the
    Schläfli skew graph <code>SRG(27,16,10,8)</code>, recovering the cubic-surface/E6 package:
    27 lines, 45 tritangents, 72 sixers, and 36 double-sixes.</p>
  <p><strong>BT1788 bridge.</strong> The 18 nonconcurrent Hesse table triples are not 18 H27 support
    lines by relabelling. BT1795 finds a non-affine 27-point transport sending all 18
    nonconcurrent triples onto H27 support and no concurrent triples onto support.</p>
</section>
<!-- BT1797_H27_CORRECTION_BOX END -->
'''

def main() -> None:
    if not INDEX.exists():
        raise SystemExit(f'missing {INDEX}')
    text = INDEX.read_text(encoding='utf-8')
    if MARKER in text:
        print('BT1797 marker already present; no change')
        return
    anchor = '<main'
    pos = text.find(anchor)
    if pos >= 0:
        # Insert after the opening main tag.
        close = text.find('>', pos)
        if close >= 0:
            new = text[:close+1] + SNIPPET + text[close+1:]
        else:
            new = SNIPPET + text
    else:
        pos = text.rfind('</body>')
        new = text[:pos] + SNIPPET + text[pos:] if pos >= 0 else text + SNIPPET
    backup = INDEX.with_suffix('.html.bak_bt1797')
    backup.write_text(text, encoding='utf-8')
    INDEX.write_text(new, encoding='utf-8')
    print(f'inserted BT1797 correction box into {INDEX}; backup {backup}')

if __name__ == '__main__':
    main()
