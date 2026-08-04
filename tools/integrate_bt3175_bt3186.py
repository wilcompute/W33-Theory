#!/usr/bin/env python3
"""Idempotently integrate Passes 3175-3186 into canonical front doors."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex',ROOT/'holonet_machine_blueprint.tex'];HTML=ROOT/'docs/index.html'
TB='% BEGIN BT3175-BT3186 CURVATURE ROUTED INFERENCE';TE='% END BT3175-BT3186 CURVATURE ROUTED INFERENCE';HB='<!-- BEGIN BT3175-BT3186 CURVATURE ROUTED INFERENCE -->';HE='<!-- END BT3175-BT3186 CURVATURE ROUTED INFERENCE -->'
TEX_BLOCK=f"\n{TB}\n\\input{{analysis/BT3175_BT3186_curvature_routed_inference_insert}}\n{TE}\n";HTML_BODY=(ROOT/'analysis/BT3175_BT3186_curvature_routed_inference_index_insert.html').read_text().strip();HTML_BLOCK=f"\n{HB}\n{HTML_BODY}\n{HE}\n"
def splice(text,begin,end,block,anchor):
    if begin in text:
        a=text.index(begin);b=text.index(end,a)+len(end);return text[:a]+block.strip('\n')+text[b:]
    p=text.rfind(anchor)
    if p<0:raise RuntimeError(f'missing anchor {anchor}')
    return text[:p]+block+text[p:]
def main():
    for p in TEX:p.write_text(splice(p.read_text(),TB,TE,TEX_BLOCK,'\\end{document}'))
    HTML.write_text(splice(HTML.read_text(),HB,HE,HTML_BLOCK,'</body>'))
    print('BT3175-BT3186 integrated')
if __name__=='__main__':main()
