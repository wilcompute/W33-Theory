#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX=(ROOT/'analysis/BT3257_cover_decoder_wedderburn_insert.tex').read_text()
HTML=(ROOT/'analysis/BT3257_cover_decoder_wedderburn_index_insert.html').read_text()
TEX_BEGIN='% BEGIN PASS 3250-3261 COVER DECODER WEDDERBURN';TEX_END='% END PASS 3250-3261 COVER DECODER WEDDERBURN'
HTML_BEGIN='<!-- BEGIN PASS 3250-3261 COVER DECODER WEDDERBURN -->';HTML_END='<!-- END PASS 3250-3261 COVER DECODER WEDDERBURN -->'
def replace_or_insert(path,insert,begin,end,anchor):
    raw=path.read_bytes();text=raw.decode('utf-8','surrogateescape')
    if begin in text:
        a=text.index(begin);b=text.index(end,a)+len(end);text=text[:a]+insert.strip()+text[b:]
    else:
        k=text.rfind(anchor);assert k>=0,(path,anchor);text=text[:k]+insert.strip()+'\n\n'+text[k:]
    path.write_bytes(text.encode('utf-8','surrogateescape'))
def main():
    for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        replace_or_insert(ROOT/name,TEX,TEX_BEGIN,TEX_END,'\\end{document}')
    replace_or_insert(ROOT/'docs/index.html',HTML,HTML_BEGIN,HTML_END,'</body>')
if __name__=='__main__':main()
