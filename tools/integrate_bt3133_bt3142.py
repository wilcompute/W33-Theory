#!/usr/bin/env python3
"""Idempotently integrate Passes 3133--3142 into all canonical front doors."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEX_FILES=[ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex',ROOT/'holonet_machine_blueprint.tex']
HTML=ROOT/'docs'/'index.html'
TEX_BEGIN='% BEGIN BT3133-BT3142 CERTIFYING ADAPTIVE INFERENCE'
TEX_END='% END BT3133-BT3142 CERTIFYING ADAPTIVE INFERENCE'
TEX_BLOCK=(f"\n{TEX_BEGIN}\n"
           "\\input{analysis/BT3133_BT3142_certifying_adaptive_inference_insert}\n"
           f"{TEX_END}\n")
HTML_BEGIN='<!-- BEGIN BT3133-BT3142 CERTIFYING ADAPTIVE INFERENCE -->'
HTML_END='<!-- END BT3133-BT3142 CERTIFYING ADAPTIVE INFERENCE -->'
HTML_BODY=(ROOT/'analysis'/'BT3133_BT3142_certifying_adaptive_inference_index_insert.html').read_text().strip()
HTML_BLOCK=f"\n{HTML_BEGIN}\n{HTML_BODY}\n{HTML_END}\n"

def replace_or_insert(text,begin,end,block,anchor):
    if begin in text:
        a=text.index(begin);b=text.index(end,a)+len(end)
        return text[:a]+block.strip('\n')+text[b:]
    pos=text.rfind(anchor)
    if pos<0:raise RuntimeError(f'anchor {anchor!r} not found')
    return text[:pos]+block+text[pos:]

def main():
    for path in TEX_FILES:
        src=path.read_text(encoding='utf-8')
        path.write_text(replace_or_insert(src,TEX_BEGIN,TEX_END,TEX_BLOCK,'\\end{document}'),encoding='utf-8')
    src=HTML.read_text(encoding='utf-8')
    HTML.write_text(replace_or_insert(src,HTML_BEGIN,HTML_END,HTML_BLOCK,'</body>'),encoding='utf-8')
    print('BT3133-BT3142 certifying adaptive inference integrated')
if __name__=='__main__':main()
