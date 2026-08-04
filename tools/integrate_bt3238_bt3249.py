#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEX_INSERT=(ROOT/'analysis/BT3248_switch_gauge_spiral_insert.tex').read_text(encoding='utf-8')
HTML_INSERT=(ROOT/'analysis/BT3248_switch_gauge_spiral_index_insert.html').read_text(encoding='utf-8')
TEX_BEGIN='% BEGIN PASS 3238-3249 SWITCH GAUGE SPIRAL'; TEX_END='% END PASS 3238-3249 SWITCH GAUGE SPIRAL'
HTML_BEGIN='<!-- BEGIN PASS 3238-3249 SWITCH GAUGE SPIRAL -->'; HTML_END='<!-- END PASS 3238-3249 SWITCH GAUGE SPIRAL -->'

def splice(path:Path, insert:str, begin:str, end:str, anchor:str):
    raw=path.read_text(encoding='utf-8',errors='surrogateescape')
    if begin in raw:
        a=raw.index(begin); b=raw.index(end,a)+len(end)
        new=raw[:a]+insert.strip()+raw[b:]
    else:
        at=raw.rfind(anchor)
        if at<0: raise RuntimeError(f'anchor {anchor!r} missing in {path}')
        new=raw[:at].rstrip()+'\n\n'+insert.strip()+'\n\n'+raw[at:]
    path.write_text(new,encoding='utf-8',errors='surrogateescape')

def main():
    for name in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        splice(ROOT/name,TEX_INSERT,TEX_BEGIN,TEX_END,'\\end{document}')
    html=ROOT/'docs/index.html'
    raw=html.read_text(encoding='utf-8',errors='surrogateescape')
    anchor='</main>' if '</main>' in raw else '</body>'
    splice(html,HTML_INSERT,HTML_BEGIN,HTML_END,anchor)
    print('PASS integrated Passes 3238-3249 into four canonical front doors')
if __name__=='__main__':main()
