#!/usr/bin/env python3
"""Idempotently integrate Passes 3163-3174 into all canonical front doors."""
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex',ROOT/'holonet_machine_blueprint.tex']
HTML=ROOT/'docs'/'index.html'
TB='% BEGIN BT3163-BT3174 PROOF CARRYING RUNTIME'
TE='% END BT3163-BT3174 PROOF CARRYING RUNTIME'
HB='<!-- BEGIN BT3163-BT3174 PROOF CARRYING RUNTIME -->'
HE='<!-- END BT3163-BT3174 PROOF CARRYING RUNTIME -->'
TEX_BLOCK=f"\n{TB}\n\\input{{analysis/BT3163_BT3174_proof_carrying_runtime_insert}}\n{TE}\n"
HTML_BODY=(ROOT/'analysis'/'BT3163_BT3174_proof_carrying_runtime_index_insert.html').read_text(encoding='utf-8').strip()
HTML_BLOCK=f"\n{HB}\n{HTML_BODY}\n{HE}\n"

def splice(text: str, begin: str, end: str, block: str, anchor: str) -> str:
    if begin in text:
        a=text.index(begin);b=text.index(end,a)+len(end)
        return text[:a]+block.strip('\n')+text[b:]
    p=text.rfind(anchor)
    if p<0: raise RuntimeError(f'missing anchor {anchor!r}')
    return text[:p]+block+text[p:]

def main() -> int:
    for p in TEX:
        s=p.read_text(encoding='utf-8')
        p.write_text(splice(s,TB,TE,TEX_BLOCK,'\\end{document}'),encoding='utf-8')
    s=HTML.read_text(encoding='utf-8')
    HTML.write_text(splice(s,HB,HE,HTML_BLOCK,'</body>'),encoding='utf-8')
    print('BT3163-BT3174 proof-carrying runtime integrated')
    return 0
if __name__=='__main__': raise SystemExit(main())
